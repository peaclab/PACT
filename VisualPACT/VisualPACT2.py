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
import subprocess
import csv


def getDimensions(file, layer):
    columns = pd.read_csv(file, nrows=1)
    nrows = 0
    ncols = 0
    while f'V(NODE{layer}_{nrows}_0)' in columns:
        nrows += 1
    while f'V(NODE{layer}_0_{ncols})' in columns:
        ncols += 1
    return nrows, ncols


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
parser.add_argument('--lcf', dest='layer_configuration_file', action='store')
# READ PARSER ARGUUMENT
parser_args = parser.parse_args()
transient_data_file = parser_args.transient_data_file
overlay_image = parser_args.overlay_image
use_overlay = overlay_image != None
tmin = parser_args.tmin
tmax = parser_args.tmax
fps = parser_args.fps
lcf_file = parser_args.layer_configuration_file
M3D = False

# lcf_rows, lcf_cols = getDimensions(lcf_file, layer)
# if(lcf_rows==0 or lcf_cols==0):
# print("ERROR: Invalid data file or nonexistant layer.")
# sys.exit(2)

# check if chip is M3D
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

subprocess.Popen(f"VisualPACT.py {transient_data_file} --layer {ptrace_layers[0]}")

