#!/usr/bin/env python
import matplotlib
matplotlib.use('Agg')
import sys
import argparse
import subprocess
import csv



# Read User Inputs
parser = argparse.ArgumentParser()
parser.add_argument('transient_data_file', action='store')
parser.add_argument('--overlay', dest='overlay_image', action='store', default=None)
parser.add_argument('--min', dest='tmin', action='store', type=float, default=None)
parser.add_argument('--max', dest='tmax', action='store', type=float, default=None)
parser.add_argument('--fps', dest='fps', action='store', type=int, default=5)
parser.add_argument('--layer', dest='layer', action='store', type=int, default=0)
parser.add_argument('--dpi', dest='dpi', action='store', type=int, default=100)
parser.add_argument('--K', dest='use_kelvin', action='store', type=bool, default=False)
parser.add_argument("--steady", dest='steady_state', action='store', type=bool, default=False)
parser.add_argument('--font_scale', dest='font_scale', action='store', type=float, default=1)
parser.add_argument('--lcf', dest='layer_configuration_file', action='store', default = None)
# READ PARSER ARGUUMENT
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
lcf_file = parser_args.layer_configuration_file
M3D = False
dpi = parser_args.dpi
font_scale = parser_args.font_scale
kelvin_offset = 273.15
if (parser_args.use_kelvin):
    kelvin_offset = 0
steady_state = parser_args.steady_state

#Read lcf, find all layers with powertraces, and check if chip is M3D
ptrace_layers = []
rows = []
with open(lcf_file, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    fields = next(csvreader)
    for row in csvreader:
        rows.append(row)
for i, row in enumerate(rows):
    if row[3] != '':
        ptrace_layers.append(i)
if len(ptrace_layers) > 1:
    M3D = True

#Run visualPACT for each layer
for i in range(len(ptrace_layers)):
    string = f"python VisualPACT.py {transient_data_file} --layer {ptrace_layers[i]} --M3D {M3D}"
    if use_overlay: string += f" --overlay {overlay_image}"
    if tmin != None: string += f" --min {tmin}"
    if tmax != None: string += f" --max {tmax}"
    if fps != 5: string += f" --fps {fps}"
    if dpi != 100: string += f" --dpi {dpi}"
    if font_scale != 1: string += f" --font_scale {font_scale}"
    if kelvin_offset == 0: string += f" --K True"
    if steady_state: string += f" --steady True"
    subprocess.Popen(string, shell=True)
