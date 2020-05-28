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
PACT is written in python and uses __Xyce 6.12__ as the backend SPICE engine. It would be better to use Linux to run PACT. 

Required Python version: > 3.6.5

Required Python libraries: sys, numpy, pandas, math, os, scipy, argparse, configparser.

The above libraries are enough for the users to run PACT with SuperLU solver. For users who want to run PACT with SPICE engine. One needs to install either __Xyce 6.12__ serial version or __Xyce 6.12__ parallel version.

Installation guideline for __Xyce 6.12__: 

https://xyce.sandia.gov/

https://xyce.sandia.gov/documentation/BuildingGuide.html

For users who want to run parallel thermal simualtions with PACT, one need to install __OpenMPI 3.1.4__:

https://www.open-mpi.org/

# Usage
1. Config file (config_files): describe the layer material properties
    1. Thickness defines the layer thickness.
    2. HTC define the heat transfer coefficient of the layer.
    3. Thermal resistivity and specific heat capacity are used to calculate the thermal resistor and capacitor values.
    4. [Init] defines the initial temperature as well as the ambient temperature.
2. Floorplan (flp_files): describe the chip floorplan
    1. Depends on the simulation granularity, users can define a standard cell level chip floorplan with a large number of units or an architectural level floorplan with realistic hardware blocks.
    2. UnitName is the name of the unit.
    3. X and Y define the location of the unit.
    4. Length (m) and Width (m) describe the unit size.
    5. Label describes the material or the cooling property of the unit.
    6. Users can ignore the configfile option for now.
3.  Layer configuration file (lcf_files): describe the layer stack
    1. Layer: describe the layer number, all layers are stacked vertically starting from layer 0
    2. Floorplan file: describe the floorplan for the specific layer
    3. PtraceFile: if the layer is active (consume power), then the corresponding power trace file to that layer needs to be specified here.
4. Power trace file (ptrace_files):
    1. UnitName: the name of the unit in the floorplan.
    2. Power (W): the power consumption for the unit.
5. Model parameter files (modelParams_files):
    1. [PATH]: define the path to the library, ptrace, flp
    2. [Simulation]: define the simulation type 
    3. [Solver]: Selection of the solver (SuperLU, SPICE_steady, SPICE_transient)
    4. [Grid]: number of girds used in the simulation. 

# Options for Solvers: 
We divide the solver section into high-level solvers as well as low-level solvers. High-level solvers include SuperLU and SPICE solvers.
Low-level solvers include KLU, KSparse, TRAP, BE, etc.
## High-level solvers
Go to the '[Solver]' section in the modelParam file and modify both the solver name as well as the wrapper file. For using SPICE solver, you have to have the __Xyce 6.12__ installed in your system. Supported high-level solvers are listed below:


### SuperLU (only for steady-state): 

name = SuperLU

wrapper = SuperLU.py

### SPICE_steady (.OP):

name = SPICE_steady

wrapper = SPICESolver_steady.py

Steady-state grid temperature files are saved in ~/src folder as RC_steady.cir.csv

### SPICE_transient (.TRAN):

name = SPICE_transient

wrapper = SPICESolver_transient.py

Note that, using SPICE transient will create an error. This error is for mapping the steady-state grid temperatures back to block temperatures. You can ignore the error. 

transient grid temperature files are saved in ~/src folder as RC_transient.cir.csv

## Low-level solvers
To change the low-level solver types for SPICE solver, users need to modify the SPICESolver.steady.py or SPICESolver.transient.py.
For transient simulation, change the following line:
```python
myfile.write('.Option TIMEINT METHOD=TRAP\n')
```
Users can modify the solver by changing the method name.

For steady-state simulation, change the following line:
```python
myfile.write('.OPTIONS LINSOL TYPE=KLU\n')
```
Users can modify the solver by changing the type name.

Available solvers and usage can be found in [1] and Xyce user guide:

https://xyce.sandia.gov/downloads/_assets/documents/Users_Guide.pdf

# Enable Parallel Thermal Simulation:

# Example Inputs and outputs
To run thermal simulations, go to /RuntimeAnalysis/scripts/ and run qsub_10mm.py, qsub_20mm.py, and qsub_Hetero_500um.py . You can choose various synthetic power profiles and floorplans within the python script. 



# Reference:
[1] Zihao Yuan, Sofiane Chetoui, Sean Nemtzow, Sherief Reda, and Ayse K. Coskun, “PACT: An Extensible Parallel Thermal Simulator for Emerging Integration and Cooling Technologies”. To be submitted to _IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems (TCAD),_ 2020.

# Action Items:

Define a universal path for the user to directly use

Aditya test

Release the first version of the tool

HotSpot medium cost heat sink

Liquid cooling via microchannels


