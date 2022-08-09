# Two-Phase Vapor Chambers (VCs) with Micropillar Wick Evaporators (ITherm'19, ISLPED'19 [7,8])


This folder contains scripts and files used to run two-phase VCs with micropillar wick evaporators discussed in these papers [7,8]. 

Please refer to our papers for a detailed discussion of the simulation setup and experimental results [7,8].

![](/image/MicropillarVC.PNG)

Figure (a) is the schematic of the vapor chamber, Figure (b) is the front view of the micropillar wick, and Figure (c) is the top view of the micropillar wick.


To run two-phase VCs with micropillar wick evaporators simulations, go to the scripts folder and run the following script:
```python
python qsub_MicroWick.py
```

The steady-state simulation grid results are saved in the /results folder.
If you want to modify the micropillar wick's structure, change the config file in the config_files folder.

Two-phase VCs with micropillar wick evaporators only support steady-state simulation with the SuperLU library. The temperature_dependent option in the model parameter file must be set to False.
