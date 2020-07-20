Overview
--------

This folder contains the required scripts to obtain the power map of a design using its RTL files. The folder contains the following files:  
  
1- Openstaparser.py : this script takes as input the DEF and the library files, and returns the power consumption and the coordinates of each standard gate in the design using Resizer.  
2- gridmesh.py : this script takes as input the DEF file, the output file generated by Openstaparser.py and the grid size. The script returns the power consumption and the coordinates of each block in the grid.  
3- Script_template : this file is used by the Openstaparser.py while calling resizer.  

Prerequisites
-------------

The following tools and files are required to run the flow, use the provided links to setup the tools:
  
1- Openroad flow for "Synthesis, Placement and routing" to convert the RTL files to a DEF file. Use the following link to setup the tool: [OpenRoad Flow.](https://github.com/The-OpenROAD-Project/OpenROAD-flow/tree/master/flow)    
2- Resizer is used for power estimation. Use the following link to setup the tool: [Resizer.](https://github.com/The-OpenROAD-Project-Attic/Resizer)    
3- The library files : lib and lef files.  


Launching the flow
------------------

After installing the previously mentioned tools and generating the DEF file, the following steps are required to generate the power map:  
  
  
1- Launch the Openparser.py python file by providing:  
  - The path to the DEF file  
  - The path to the LEF file  
  - The path to the LIB file  
  - The path to the LEF file
  - The clock period of the design    
  - The path to resizer binary files  
 
2- In the same folder Launch  the gridmesh.py  python file by providing:  
  - The path to the DEF file  
  - The gridsize  
  
  ```
$ python3 Openstaparser.py --deff ./routed.def --lef merged.lef --lib sc12_cln65lp_base_lvt_tt_typical_max_1p20v_25c.lib --clk 0.5 --resizer /local-disk/tools/OpenROAD/alpha-release/openroad/OpenROAD-2019-07-30_05-17/bin/resizer
$ python3 gridmesh.py --deff ./routed.def --gridsize 128
```
  


The flow generates two files:  
1- flp : contains the dimensions and the coordinates of each block in the grid.  
2- ptrace : contains the power values of each block in the grid. 

Addtional scripts
------------------

1- transform_OpenRoad_flp_ptrace_to_HS.py: transform the OpenRoad flp and ptrace to HotSpot flp and ptrace.

```python
$ python transform_OpenRoad_flp_ptrace_to_HS.py <flp> <ptrace>
```
  

2- transform_HS_PACT_flp.py: transform the HotSpot flp to PACT flp.

3- transform_HS_PACT_ptrace.py: transform the HotSpot ptrace to PACT ptrace.