# Two-Phase Vapor Chambers (VCs) with Hybrid Wick Evaporators (DATE'20 [9])


This folder contains scripts and files used to run two-phase VCs with hybrid wick evaporators and a learning-based temperature-dependent HTC simulation framework discussed in this paper [9]. We also include an example run script for running the proposed multi-start simulated annealing (MSA) optimization method.

For a detailed discussion of the simulation setup and experimental results, please refer to our paper [9].

![](/image/VC.PNG)

Figure (a) is the schematic of the vapor chamber, and Figure (b) is the schematic of the hybrid wick.

The valid parameter range for hybrid wick is show in the following table:
<p align = "center">
  <img src="/image/HybridParam.png">
</p>

Users also need to use the dry_out.py script to test whether the current hybrid wick structure satisfies the dry-out constraint.

To run two-phase VCs with hybrid wick evaporators simulations, go to the scripts folder and run the following script:
```python
python qsub_2mmHybridWick.py
```

To run MSA, go to the scripts folder and run the following script:
```python
python qsub_HybridWick_simulatedannealing.py
```
The steady-state simulation grid results are saved in the /results folder.
If you want to modify the structure of the hybrid wick, change the corresponding config file in the config_files folder.

Two-phase VCs with hybrid wick evaporators only support steady-state simulation with the SuperLU library. The temperature_dependent option in the model parameter file needs to be set to True, and the temperature_dependent_library option needs to be set to TemperatureDependent.py.
