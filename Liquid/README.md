# Liquid cooling via microchannel Test Cases (Section IV-C)
![](/image/chipstack.PNG)

* This folder contains all the necessary files to run simulations described in the Section IV-C of our paper [1].

* Users can manipulate the power number in ptrace_files/liquid_ptrace.csv. 

* Users can also change the liquid flow velocity in /modelParams_files/modelParams_liquid.config

* To run liquid cooling simulations, go to scripts and run the following commands:
```python
python liquid.py
```
The steady-state simulation grid results as well as the last step transient simulation results are saved in /results folder.

The transient grid level simulation results are saved in ~/src/RC_transient.cir.csv. 

The transient grid level simulation results are saved in ~/src/RC_transient_block_temp.csv. 
