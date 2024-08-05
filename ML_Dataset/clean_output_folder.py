#!/usr/bin/env python
import os
os.chdir('outputs')
outputs = os.listdir()

for file in outputs:
    if ".cir.csv" not in file:
        path = os.getcwd()
        os.remove(f"{path}/{file}")