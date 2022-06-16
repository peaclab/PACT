# Two-Phase Vapor Chambers (VCs) with Micropillar Wick Evaporators (ITherm'19, ISLPED'19 [7,8])


This folder contains scripts and files used to run two-phase VCs with micropillar wick evaporators discussed in these papers [7,8]. 

For a detailed discussion of the simulation setup and experimental results, please refer to our papers [7,8].

![](/image/microVC.PNG)

Figure (a) is the schematic of the vapor chamber, Figure (b) is the front view of the micropillar wick, and Figure (c) is the top view of the micropillar wick.


To run two-phase VCs with hybrid wick evaporators simulations, go to the scripts folder and run the following script:
```python
python qsub_MicroWick.py
```

The steady-state simulation grid results are saved in the /results folder.
If you want to modify the structure of the micropillar wick, change the corresponding config file in the config_files folder.

Two-phase VCs with micropillar wick evaporators only support steady-state simulation with the SuperLU library. The temperature_dependent option in the model parameter file needs to be set to False.
