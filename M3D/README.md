# Monolithic 3D Test Cases (Section IV-C)
This folder contains all the necessary files to run simulations described in Section IV-C of our paper [1].
For a detailed discussion of the simulation setup and experimental results, please refer to our paper [1].
The layer configration file and power traces are adopted from a recent work [3].
<p align="center">
<img src= "https://github.com/yuan1z/PACT/tree/master/image/M3D.png" />
</p>
Users can manipulate the power number in ptrace_files/liquid_ptrace.csv. 
Users can also change the liquid flow velocity in /modelParams_files/modelParams_liquid.config.
To run liquid cooling simulations, go to scripts and run the following commands:
```python
python liquid.py
```
The steady-state simulation grid results as well as the last step transient simulation results are saved in /results folder.
If you want to modify the number of channels in the liquid cooling layers, make sure you change the liquid_flp.csv as well as the num_of_channels option in liquid.config.
The transient grid level simulation results are saved in ~/src/RC_transient.cir.csv. 
The transient grid level simulation results are saved in ~/src/RC_transient_block_temp.csv. 
