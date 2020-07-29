# Monolithic 3D Test Cases (Section IV-A)
This folder contains all the necessary files to run simulations described in Section IV-A of our paper [1].
For a detailed discussion of the simulation setup and experimental results, please refer to our paper [1].
The layer configration file and power traces are adopted from a recent work [3].

<p align="center">
<img src= "/image/M3D.png" />
</p>

Users can manipulate the power number in ptrace_files/M3D_tier0_ptrace.csv and ptrace_files/M3D_tier1_ptrace.csv. 
Users can also change the layer configurations in /lcf_files/M3D_lcf.csv.
To run M3D simulations, go to scripts folder and run the following commands:

```python
python M3D.py
```

The steady-state simulation grid results as well as the last step transient simulation results are saved in /results folder.
The transient grid level simulation results are saved in ~/src/RC_transient.cir.csv. 
The transient grid level simulation results are saved in ~/src/RC_transient_block_temp.csv. 
