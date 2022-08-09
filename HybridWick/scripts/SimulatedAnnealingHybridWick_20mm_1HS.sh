#!/bin/sh -l
module load python3/3.6.5


date
hostname
pushd ${PWD}/../../src
lcf=$1
config=$2
modelParams=$3
grid_file=$4
scp_file=$5
log_file=$6
maxPD=$7

echo "lcffile = $lcf"
echo "config file=  $config"
echo "model params file =  $modelParams"
echo "grid file = $grid_file"
echo "scp file =  $scp_file"
echo "log file =  $log_file"

time  python ../HybridWick/scripts/SimulatedAnnealingHybridWick_20mm_1HS.py "${lcf}" "${config}" "${modelParams}" "${grid_file}" "${maxPD}"


#scp ${grid_file}.layer0 prachis@128.197.127.15:${scp_file}

#popd 
date



