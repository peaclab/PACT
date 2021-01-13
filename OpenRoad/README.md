# OpenROAD Test Cases (Section IV-D)
This folder contains all the necessary files to run simulations with the industrial standard-cell level inputs described in Section IV-D of our paper [1].
For a detailed discussion of the simulation setup and experimental results, please refer to our paper [1].
The statistics of the realistic MPSoCs from the OpenROAD benchmark set are shown as follows:

<p align="center">
<img src= "/image/OpenRoad.png" />
</p>

All the data are generated from the OpenROAD project [5] and import to PACT through the interface described in the ~/src/OpenROAD folder.
Users can manipulate the number of grids used in the simulations in the modelParams files located in the /modelParams_files folder. 
The flp_files and ptrace_files folders contain all the floorplans as well as the power traces of the OpenROAD MPSoCs listed in the table above.
To run OpenRPAD MPSoCs simulations (i.e., PicoSoC), go to the scripts folder and run the following commands:

```python
python qsub_Pico.py
```
Users can change the floorplan utilization level inside of the python script.
The steady-state simulation grid results as well as the last step transient simulation results are saved in /results folder. The transient grid level simulation results are saved in ~/src/RC_transient.cir.csv. The transient grid level simulation results are saved in ~/OpenRoad/results/{Chip_folder}/{Chip_Name}{utlization}_{grid num}.gird.block.transient.csv.
