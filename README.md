# PACT: A Standard Cell Level to Architectural Level Parrallel Compact Thermal Simulator
## Introduction
PACT is a SPICE-based PArallel Compact Thermal simulator (PACT) that enables fast and accurate standard cell level to architectural level steady-state and transient parallel thermal simulation. PACT utilizes the advantages of multi-core processing (OpenMPI) and includes several solvers to speed up both steady-state and transient simulations. PACT can be easily extended to model a variety of emerging integration and cooling technologies, such as 3D stacking, liquid cooling via microchannels, and others, by simply modifying the thermal netlist. PACT can be also used with popular architectural level performance and power simulators to evaluate the thermal profile. 

The simulation flow of PACT is shown in the following image.

![](/image/PACTflow.PNG)

PACT takes config file, floorplan file, lcf file, modelParams file, and ptrace file as inputs and outputs the steady-state/transient temperature results.

The config file describes the material property, initial temperature, as well as cooling package information. The floorplan file describes the chip information that includes chip size, number of blocks, block sizes and location, and block material property. Lcf file stands for the layer configuration file, which basically shows the layer stack with cooling information. Ptrace file allocates the power number for each active block inside the chip stack. ModdelParams file shows the simulation information (e.g., steady-state/transient, solver type, number of grids, package information, etc.)

More details about PACT can be found in [1].




All the source code are located inside the /src folder include the SuperLU solver as well as the SPICE solvers. SPICE solvers are currently seperate into SPICE_steady and SPICE_transient. 


# Requirements
PACT is written in python and use __Xyce 6.12__ as the backend SPICE engine. It would be better to use Linux to run PACT. 

Required Python version: > 3.6.5

Required Python libraries: sys, numpy, pandas, math, os, scipy, argparse, configparser.

Above library is enough for the Users to run PACT with SuperLU solver. For users who want to run PACT with SPICE engine. One need to install either __Xyce 6.12__ serial version or __Xyce 6.12__ parallel version.

Installation guideline for __Xyce 6.12__: 

https://xyce.sandia.gov/

https://xyce.sandia.gov/documentation/BuildingGuide.html

# Usage
1. Config file (config_files): describe the layer material properties
    1. thickness define the layer thichness.
    2. htc define the heat transfer coeffcient of the layer.
    3. thermal resistivity and specific heat capacity are used to calculate the thermal resistor and capacitor values.
    4. [Init] defines the initial temperature as well as the ambient temperature.
2. floorplan (flp_files): decribe the chip floorplan
    1.
# Example Input and outputs
To run thermal simulations, go to /RuntimeAnalysis/scripts/ and run qsub_10mm.py, qsub_20mm.py, and qsub_Hetero_500um.py . You can choose various synthetic power profiles and floorplans within the python script. 

# Options for Solvers: 

go to the /RuntimeAnalysis/modelParams_files/ and find the 'modelparam' file you want to modify. Go to the '[Solver]' section and modfiy both the solver name as well as the wrapper file. For using SPICE solver, you have to have the __Xyce 6.12__ installed in your system. Supported solvers are listed below:


## SuperLU (only for steady state): 

name = SuperLU

wrapper = SuperLU.py

## SPICE_steady (.OP):

name = SPICE_steady

wrapper = SPICESolver_steady.py

Steady-state grid temperature files are saved in ~/src folder as RC_steady_prachi.cir.csv

## SPICE_transient (.TRAN):

name = SPICE_transient

wrapper = SPICESolver_transient.py

Note that, using SPICE transient will create an error. This error is for mapping the steady-state grid temperatrues back to block temperatrues. You can ignore the error. 

transient grid temperature files are saved in ~/src folder as RC_transient_prachi.cir.csv

# Potential Error and Solutions: 

Error: cannot find grid mode, go to the 'modelparam' file and add "grid_mode = max" in the '[Grid]' section.

Error: no 'Cu', uncomment the '[Cu]' section in the 'modelparam' file.

# Reference:
[1] Zihao Yuan, Sofiane Chetoui, Sean Nemtzow, Sherief Reda, and Ayse K. Coskun, “PACT: An Extensible Parallel Thermal Simulator for Emerging Integration and Cooling Technologies”. To be submitted to __IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems (TCAD),__ 2020.

# Action Items:
Clean up the repo 

Rewrite Readme and include more details

Define a universal path for the user to directly use

Aditya test

Release the first version of the tool

HotSpot medium cost heat sink

Liquid cooling via microchannels


