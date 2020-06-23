#!/bin/sh -l
module load python3/3.6.5


date
hostname
pushd ${PWD}/../../src 
results="${PWD}/../results/"
log="${PWD}/../log/"

lcf=$1
config=$2
modelParams=$3
grid_file=$4
scp_file=$5
log_file=$6

echo "lcffile = $lcf"
echo "config file=  $config"
echo "model params file =  $modelParams"
echo "grid file = $grid_file"
echo "scp file =  $scp_file"
echo "log file =  $log_file"

#python -m cProfile -o cri_10x10.pyprof CRICoolingTool.py "${lcf}" "${config}" "${modelParams}" "--gridSteadyFile" "${grid_file}"
#time -ao ${log_file} python CRICoolingTool.py "${lcf}" "${config}" "${modelParams}" "--gridSteadyFile" "${grid_file}"
time python CRICoolingTool.py "${lcf}" "${config}" "${modelParams}" "--gridSteadyFile" "${grid_file}"
#time dist/CRICoolingTool/CRICoolingTool "${lcf}" "${config}" "${modelParams}" "--gridSteadyFile" "${grid_file}"
#scp ${grid_file}.layer0 prachis@128.197.176.170:${scp_file}


#time  python CRICoolingTool.py "${lcf}" "${config}" "${modelParams}" "--gridSteadyFile" "${grid_file}"


popd 
date


