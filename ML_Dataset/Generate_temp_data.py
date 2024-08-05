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



#print(os.getcwd())
os.chdir('different_ptraces/')


PACT_path = '/usr4/spclpgm/zhoua25/PACT/ML_Dataset/tier0_ptrace.csv'


folders = os.listdir()

ptrace_files_path = []

#getting path of all the ptrace files
for folder in folders:
    os.chdir(f'{folder}')
    files = os.listdir()
    for file in files:
        if "scaled" in file:
            path = os.getcwd()
            ptrace_files_path.append(f"{path}/{file}")
            os.chdir('../')
    


print(ptrace_files_path[0], ptrace_files_path[1])








    


temp_files_paths = []
#running PACT for each of the files and storing the data
i = 311
for file in ptrace_files_path[311:]:
    print(f"Output: {i}")
    if os.path.exists(PACT_path):#Replace and move ptrace file
        os.remove(PACT_path)
        i += 1
    shutil.copy2(file, PACT_path)
    os.system(f"python /usr4/spclpgm/zhoua25/PACT/src/PACT.py /usr4/spclpgm/zhoua25/PACT/ML_Dataset/M3D_lcf.csv /usr4/spclpgm/zhoua25/PACT/ML_Dataset/Intel.config /usr4/spclpgm/zhoua25/PACT/ML_Dataset/modelParams_Intel.config --gridSteadyFile /usr4/spclpgm/zhoua25/PACT/ML_Dataset/outputs/output{i}.grid.steady")
    



    


