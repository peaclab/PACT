#!/usr/bin/env python
import matplotlib
matplotlib.use('Agg')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
import re
import os
from pathlib import Path
import shutil
import sys
import argparse

def getDimensions(file,layer):
    columns = pd.read_csv(file,nrows=1)
    nrows=0
    ncols=0
    while f'V(NODE{layer}_{nrows}_0)' in columns:
        nrows+=1
    while f'V(NODE{layer}_0_{ncols})' in columns:
        ncols+=1
    return nrows,ncols

def readFormatInput(file,n_rows,n_cols):
    column = [f'V(NODE{layer}_{row}_{col})' for row in range(n_rows) for col in range(n_cols)]
    df_l = pd.read_csv(file,usecols = column)
    return df_l

def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)

def make_video(image_folder,video_name):
    path = sorted_alphanumeric(os.listdir(image_folder))

    images = [img for img in path if img.endswith(".png")]

    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, fps, (width,height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()

def make_transparent_overlay(overlay):
    h, w, c = overlay.shape
    # append Alpha channel -- required for BGRA (Blue, Green, Red, Alpha)
    overlay_transparent_bg = np.concatenate([overlay, np.full((h, w, 1), 255, dtype=np.uint8)], axis=-1)
    # create a mask where white pixels ([255, 255, 255]) are True
    threshold=128
    white = np.all(overlay >= [threshold, threshold, threshold], axis=-1)
    black=np.all(overlay <= [threshold, threshold, threshold], axis=-1)
    # change the values of Alpha to 0 for all the white pixels
    overlay_transparent_bg[white, -1] = 0
    overlay_transparent_bg[black,:] = 0
    overlay_transparent_bg[black,-1] = 255
    return overlay_transparent_bg

#USER INPUTS
parser = argparse.ArgumentParser()
parser.add_argument('transient_data_file',action='store')
parser.add_argument('--overlay',dest='overlay_image',action='store',default=None)
parser.add_argument('--min',dest='tmin',action='store',type=float,default=None)
parser.add_argument('--max',dest='tmax',action='store',type=float,default=None)
parser.add_argument('--fps',dest='fps',action='store',type=int,default=5)
parser.add_argument('--layer',dest='layer',action='store',type=int,default=0)
parser.add_argument('--dpi',dest='dpi',action='store',type=int,default=100)
parser.add_argument('--K',dest='use_kelvin',action='store',type=bool,default=False)
parser.add_argument("--steady",dest='steady_state',action='store',type=bool,default=False)
parser.add_argument('--font_scale',dest='font_scale',action='store',type=float,default=1)

#READ PARSER ARGUUMENTS
parser_args = parser.parse_args()
transient_data_file = parser_args.transient_data_file
overlay_image = parser_args.overlay_image
use_overlay = overlay_image != None
tmin = parser_args.tmin
tmax = parser_args.tmax
fps = parser_args.fps
if fps < 1:
    print("ERROR: FPS must be a positive integer.")
    sys.exit(2)
layer = parser_args.layer
dpi = parser_args.dpi
font_scale = parser_args.font_scale
kelvin_offset=273.15
if(parser_args.use_kelvin):
    kelvin_offset=0
steady_state=parser_args.steady_state
#SET OUTPUT PATHS
output_path = transient_data_file.rstrip(''.join(Path(transient_data_file).suffixes))
output_name = os.path.basename(output_path)
video_file = output_path+'.avi'
if steady_state:
    frame_folder = os.path.dirname(transient_data_file)+'/steadyframes/'
else:
    frame_folder = output_path+'_frames/'
grid_rows, grid_cols = getDimensions(transient_data_file,layer)
if(grid_rows==0 or grid_cols==0):
    print("ERROR: Invalid data file or nonexistant layer.")
    sys.exit(2)
print(output_name)
print(grid_rows,'x',grid_cols)
print("video path: "+os.path.abspath(video_file))
print("image folder path: "+os.path.abspath(frame_folder)+'/')
#Delete any previous images folder and make a new one
folder_path = Path(frame_folder)
if not steady_state:
    if folder_path.exists() and folder_path.is_dir():
        shutil.rmtree(folder_path)
    os.makedirs(frame_folder)
else:
    if (not folder_path.exists()):
        os.makedirs(frame_folder)
#Read data from file
print("Reading file...",end="\r")
df_l = readFormatInput(transient_data_file,grid_rows,grid_cols)
print("                   ",end="\r")
#Automatically calculate min and max heatmap valus if not specified
auto_tmin = df_l.min().min()-kelvin_offset
auto_tmax = df_l.max().max()-kelvin_offset
if tmin == None:
    tmin = auto_tmin
if tmax == None:
    tmax = auto_tmax
print(f"data temperature range: {auto_tmin} C to {auto_tmax} C")
print("TMIN:",tmin,'C')
print("TMAX:",tmax,'C')
if tmin > auto_tmax or tmax < auto_tmin:
    print("ERROR: Specified TMIN and TMAX range is outuside of actual data range.")
    sys.exit(2)
if tmin == tmax:
    print("ERROR: TMIN and TMAX have the same value.")
    sys.exit(2)
if tmin > tmax:
    print("WARNING: TMIN value is greater than TMAX value.")
#Set heatmap colors
start = 0.0
stop = 1.0
number_of_lines= 1000
cm_subsection = np.linspace(start, stop, number_of_lines) 
colors = [ matplotlib.cm.jet(x) for x in cm_subsection ]  
#Generate video Frames
i=0
sns.set(font_scale=font_scale)
if(use_overlay):
    overlay =  cv2.imread(overlay_image,cv2.IMREAD_UNCHANGED)
    overlay_transparent_bg = make_transparent_overlay(overlay)
for index, row in df_l.iterrows():
    print("frame: "+str(i),end="\r")
    newRow = np.array(row)
    newRow = newRow.reshape(grid_rows,grid_cols)-kelvin_offset
    plot = sns.heatmap(newRow,cmap=colors,xticklabels=False, yticklabels=False,cbar_kws={'label':'Temperature($^\circ C$)'}, vmin=tmin, vmax=tmax)
    plot.set_aspect("equal")
    if(use_overlay):
        plot.imshow(overlay_transparent_bg,  zorder=1, aspect=plot.get_aspect(), interpolation='none', extent=plot.get_xlim()+plot.get_ylim())
    plot.get_figure().savefig(f"{frame_folder}{output_name}_{i}.png",dpi=dpi,bbox_inches = 'tight',pad_inches = 0)
    plot.get_figure().clf()
    i+=1

if not steady_state:
    make_video(frame_folder,video_file)
print("Done.                  ")
