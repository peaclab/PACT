#!/usr/bin/env python

import csv

with open('Intel.cir') as fin, open('Intel.cir.csv', 'w') as fout:
    o=csv.writer(fout)
    for line in fin:
        o.writerow(line.split())