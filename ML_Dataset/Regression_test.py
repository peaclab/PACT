#!/usr/bin/env python
import numpy as np
import pandas as pd
import re
import os
from pathlib import Path
import shutil
import sys
import argparse
import csv

import seaborn as sns 
import matplotlib.pyplot as plt 
from sklearn import preprocessing, svm 
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression 

kelvin_offset = 273.15

def getDimensions(file, layer):
    columns = pd.read_csv(file, nrows=1)
    nrows = 0
    ncols = 0
    while f'V(NODE{layer}_{nrows}_0)' in columns:
        nrows += 1
    while f'V(NODE{layer}_0_{ncols})' in columns:
        ncols += 1
    return nrows, ncols


def readFormatInput(file, n_rows, n_cols, layer):
    column = [f'V(NODE{layer}_{row}_{col})' for row in range(n_rows) for col in range(n_cols)]
    df_l = pd.read_csv(file, usecols=column)
    return df_l

def getTemp(file):
    grid_rows, grid_cols = getDimensions(file, 4)
    df_l = readFormatInput(file, grid_rows, grid_cols, 4)
    df_l -= kelvin_offset



# for file in outputs:
#     if ".cir.csv" not in file:
#         path = os.getcwd()
#         os.remove(f"{path}/{file}")

#248 train, rest are test
os.chdir('different_ptraces')
folders = os.listdir()


ptrace_files_path = []

for folder in folders:
    os.chdir(f'{folder}')
    files = os.listdir()
    for file in files:
        if "scaled" in file:
            path = os.getcwd()
            ptrace_files_path.append(f"{path}/{file}")
            os.chdir('../')
os.chdir('../')

os.chdir('outputs')
outputs = os.listdir()
temp_files_paths = []

for file in outputs:
    path = os.getcwd()
    temp_files_paths.append(f"{path}/{file}")
os.chdir('../')


#matching powertrace and temperature outputs 
fixed_list = []
for i in range(len(ptrace_files_path)):
    for file in temp_files_paths:
        if f"output{i}.cir.csv" in file:
            fixed_list.append(file)


df = pd.DataFrame()
df['Powertrace'] = ptrace_files_path
df['Temperatures'] = fixed_list





X = np.array(df['Powertrace']).reshape(-1,1)
Y = np.array(getTemp(df['Temperatures'])).reshape(-1,1)



print(ptrace_files_path[0])













"""
Need to:

only get temperatures of active layers: 1,4
adjust for kelvin?

Take a random powertrace, then get the temperatures on the layer.
Create a DataFrame which contains powertraces and the file locations for the temperature outputs 

add up power usage then divide up over the grid based on width length + thickness
Grid: 100x100
100 nodes
find a way to divide up power to each node

#Run get Temperature again and delete all unecessary files. 


"""







