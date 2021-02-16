#!/bin/bash
#$ -N Mono3D_transient_64_8
#$ -j y
#$ -V
#$ -pe mpi_8_tasks_per_node 8
python Haswell.py
echo $NSLOTS

