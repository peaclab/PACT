#!/bin/sh -l
module load python3/3.6.5


date
hostname
pushd /projectnb/peaclab-cri-cooling/EDAToolDevelopment/CRI-Cooling-Tool/src/
results="/projectnb/peaclab-cri-cooling/EDAToolDevelopment/CRI-Cooling-Tool/results/"
log="/projectnb/peaclab-cri-cooling/EDAToolDevelopment/CRI-Cooling-Tool/log/"

chiplabel=$1
folder=$2
lcf=$3
config=$4
modelParams=$5
pdenType=$6
pdenVal=$7
scp_dir=${8}
grid_rows=${9}
grid_cols=${10}
run_name=${11}

lcf_file=${folder}${lcf}_${pdenType}_${pdenVal}Wcm2.csv
config_file=${folder}${config}
modelParams_file=${folder}${modelParams}_${grid_rows}x${grid_cols}
grid_dir=${chiplabel}/${grid_rows}x${grid_cols}/
grid_file=${run_name}_${pdenType}_${pdenVal}Wcm2.csv
scp_file=${scp_dir}${grid_dir}${run_name}_${pdenType}_${pdenVal}Wcm2.grid.steady

echo "lcffile = $lcf_file"
echo "config file=  $config_file"
echo "model params file =  $modelParams_file"
echo "grid_files directory = $grid_dir"
echo "grid file = $grid_file"
echo "scp file =  $scp_file"

#time -ao ${log}${run_name}_${chiplabel}_${grid_rows}x${grid_cols}_Si_only.log python CRICoolingTool.py "${lcf_file}" "${config_file}" "${modelParams_file}" "--gridSteadyFile" "${grid_dir}${grid_file}"
#scp ${results}${grid_dir}${grid_file} prachis@128.197.127.15:${scp_file}

popd 
date



