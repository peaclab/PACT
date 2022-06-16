# Two-Phase Vapor Chambers (VCs) with Hybrid Wick Evaporators (DATE'20 [9])


This folder contains scripts and files used to run two-phase VCs with hybrid wick evaporators and learning-based temperature-dependent HTC simulation framework discussed in this paper [9]. We also include a example run script for running the proposed Multi-start simulated annealing approach (MSA).

For a detailed discussion of the simulation setup and experimental results, please refer to our paper [9].

![](/image/VC.PNG)



The valid parameter range for hybrid wick is show in the following table:
![](/image/HybridParam.png)




To run liquid cooling simulations, go to the scripts folder and run the following commands:
```python
python liquid.py
```
The steady-state simulation grid results as well as the last step transient simulation results are saved in /results folder.
If you want to modify the number of channels in the liquid cooling layers, make sure you change the liquid_flp.csv as well as the num_of_channels option in liquid.config.
The transient grid level simulation results are saved in ~/Liquid/results/liquid/liquid_{gridnum}.cir.csv. 
The transient block level simulation results are saved in ~/Liquid/results/liquid/liquid_{grid num}.block.transient.csv. 
