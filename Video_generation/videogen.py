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

#USER INPUTS
parser = argparse.ArgumentParser()
parser.add_argument('transient_data_file',action='store')
parser.add_argument('--overlay',dest='overlay_image',action='store',default=None)
parser.add_argument('--min',dest='vmin',action='store',type=float,default=None)
parser.add_argument('--max',dest='vmax',action='store',type=float,default=None)
parser.add_argument('--fps',dest='fps',action='store',type=int,default=5)
parser.add_argument('--layer',dest='layer',action='store',type=int,default=0)
parser.add_argument('--dpi',dest='dpi',action='store',type=int,default=100)
#READ PARSER ARGUUMENTS
parser_args = parser.parse_args()
transient_data_file = parser_args.transient_data_file
overlay_image = parser_args.overlay_image
use_overlay = overlay_image != None
vmin = parser_args.vmin
vmax = parser_args.vmax
fps = parser_args.fps
layer = parser_args.layer
dpi = parser_args.dpi
#SET OUTPUT PATHS
output_path = transient_data_file.rstrip(''.join(Path(transient_data_file).suffixes))
output_name = os.path.basename(output_path)
video_file = output_path+'.avi'
frame_folder = output_path+'_frames/'
grid_rows, grid_cols = getDimensions(transient_data_file,layer)
if(grid_rows==0 or grid_cols==0):
    print("Error: Invalid data file.")
    sys.exit(2)
print(output_name)
print(grid_rows,'x',grid_cols)
print("video path: "+video_file)
print("image folder path: "+frame_folder)
#Delete any previous images folder and make a new one
folder_path = Path(frame_folder)
if folder_path.exists() and folder_path.is_dir():
    shutil.rmtree(folder_path)
os.makedirs(frame_folder)
#Read data from file
print("Reading file...",end="\r")
df_l = readFormatInput(transient_data_file,grid_rows,grid_cols)
print("                   ",end="\r")
#Automatically calculate min and max heatmap valus if not specified
if vmin == None:
    vmin = df_l.min().min()-273.15
if vmax == None:
    vmax = df_l.max().max()-273.15
print("vmin:",vmin)
print("vmax:",vmax)
#Set heatmap colors
start = 0.0
stop = 1.0
number_of_lines= 1000
cm_subsection = np.linspace(start, stop, number_of_lines) 
colors = [ matplotlib.cm.jet(x) for x in cm_subsection ]  
#Generate video Frames
i=0
if(use_overlay):
    overlay =  cv2.imread(overlay_image,cv2.IMREAD_UNCHANGED)
for index, row in df_l.iterrows():
    print("frame: "+str(i),end="\r")
    newRow = np.array(row)
    newRow = newRow.reshape(grid_rows,grid_cols)-273.15
    plot = sns.heatmap(newRow,cmap=colors,xticklabels=False, yticklabels=False,cbar_kws={'label':'Temperature($^\circ C$)'}, vmin=vmin, vmax = vmax)
    plot.set_aspect("equal")
    if(use_overlay):
        plot.imshow(overlay, alpha=0.3, zorder=1, aspect=plot.get_aspect(), interpolation='none', extent=plot.get_xlim()+plot.get_ylim())
    plot.get_figure().savefig(f"{frame_folder}{output_name}_{i}.png",dpi=dpi,bbox_inches = 'tight',pad_inches = 0)
    plot.get_figure().clf()
    i+=1

make_video(frame_folder,video_file)
print("Done.                  ")
