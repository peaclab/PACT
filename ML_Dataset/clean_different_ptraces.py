#!/usr/bin/env python
import os

os.chdir('different_ptraces')
folders = os.listdir()
for folder in folders:
    os.chdir(f'{folder}')
    files = os.listdir()
    for file in files:
        if "scaled" not in file:
            path = os.getcwd()
            print(path)
            os.remove(f"{file}")
    os.chdir('../')