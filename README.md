# PACT: A Standard Cell Level to Architectural Level Parallel Compact Thermal Simulator
# Introduction
PACT is a SPICE-based PArallel Compact Thermal simulator (PACT) that enables fast and accurate standard cell level to architectural level steady-state and transient parallel thermal simulation. PACT utilizes the advantages of multi-core processing (OpenMPI) and includes several solvers to speed up both steady-state and transient simulations. PACT can be easily extended to model a variety of emerging integration and cooling technologies, such as 3D stacking, liquid cooling via microchannels, and others, by simply modifying the thermal netlist. PACT can be also used with popular architectural level performance and power simulators to evaluate the thermal profile. 

The simulation flow of PACT is shown in the following image.

![](/image/PACTflow.PNG)

PACT takes config file, floorplan file, lcf file, modelParams file, and ptrace file as inputs and outputs the steady-state/transient temperature results.
<!---
The config file describes the material property, initial temperature, as well as cooling package information. The floorplan file describes the chip information that includes chip size, number of blocks, block sizes and location, and block material property. Lcf file stands for the layer configuration file, which basically shows the layer stack with cooling information. Ptrace file allocates the power number for each active block inside the chip stack. ModelParams file shows the simulation information (e.g., steady-state/transient, solver type, number of grids, package information, etc.)
-->
More details about PACT can be found in [1].




All the source codes are located inside the /src folder include the SuperLU solver as well as the SPICE solvers. Steady-state and transient SPICE-based solvers are named as SPICE_steady and SPICE_transient, respectively.


# Requirements
PACT is written in python and uses __Xyce 6.12__ as the backend SPICE engine.

* Required Python version: > 3.6.5

* Required Python libraries: sys, numpy, pandas, math, os, scipy, argparse, configparser.

The above libraries are enough for the users to run PACT with SuperLU solver. For users who want to run PACT with SPICE engine. One needs to install either __Xyce 6.12__ serial version or __Xyce 6.12__ parallel version.

Installation guideline for __Xyce 6.12__: 

* https://xyce.sandia.gov/

* https://xyce.sandia.gov/documentation/BuildingGuide.html

For users who want to run parallel thermal simualtions with PACT, one need to install __Xyce 6.12__ parallel version and __OpenMPI 3.1.4__:

* https://www.open-mpi.org/

It's recommended to use Linux and macOS to run PACT. To enable sequential and parallel thermal simulation with PACT on Windows, users have to use __Cygwin__ to build the __Xyce 6.12__ and __OpenMPI 3.1.4__ and run PACT using __Cygwin__ terminal. __Cygwin__ download link:

* https://www.cygwin.com/


If __Xyce 6.12__ and __OpenMPI 3.1.4__ have already been installed in your Linux server, then you can simply load the following dependencies to load Xyce and OpenMPI.
```
module load python3/3.6.5 gcc/5.5.0 fftw/3.3.8 netcdf/4.6.1 blis/0.6.0 openmpi/3.1.4 xyce/6.12
```


# Usage
1. Config file (i.e., Example/config_files): describe the layer material properties
    1. Thickness defines the layer thickness.
    2. HTC is the heat transfer coefficient between the ambient and the heat sink.
    3. Thermal resistivity and specific heat capacity are used to calculate the thermal resistor and capacitor values.
    4. [Init] defines the initial temperature as well as the ambient temperature.
    5. Users can select the heat sink as well as its parameters.
2. Floorplan (i.e., Example/flp_files (.CSV file)): describe the chip floorplan
    1. Depends on the simulation granularity, users can define a standard cell level chip floorplan with a large number of units or an architectural level floorplan with realistic hardware blocks.
    2. UnitName is the name of the unit.
    3. X and Y define the location of the unit.
    4. Length (m) and Width (m) describe the unit size.
    5. Label describes the material or the cooling property of the unit.
    6. Users can ignore the configfile option for now.
3.  Layer configuration file (i.e., Example/lcf_files (.CSV file)): describe the layer stack
    1. Layer: describe the layer number, all layers are stacked vertically starting from layer 0
    2. Floorplan file: describe the floorplan for the specific layer
    3. PtraceFile: if the layer is active (consume power), then the corresponding power trace file to that layer needs to be specified here.
4. Power trace file (i.e., Example/ptrace_files (.CSV file)):
    1. UnitName: the name of the unit in the floorplan.
    2. Power (W): the power consumption for the unit.
5. Model parameter files (i.e., Example/modelParams_files):
    1. [PATH]: define the path to the library, ptrace, flp
    2. [Simulation]: define the simulation type 
    3. [Solver]: Selection of the solver (SuperLU, SPICE_steady, SPICE_transient)
    4. [Grid]: number of girds used in the simulation. 
    5. Users can also define the heat sink library, cooling properties, and cooling options.
6. Command to run simulation with PACT:
    ```python
    python PACT.py <lcf_file> <config_file> <modelParams_file> --gridSteadyFile <grid_file>
    ```
    For steady-state simulation, the grid_file specific the steady-state grid temperature output of PACT simulation. For transient simulation, the last step transient grid temperature results will be saved in grid_file.
# Options for Solvers: 
We divide the solver section into high-level solvers as well as low-level solvers. High-level solvers include SuperLU and SPICE solvers.
Low-level solvers include KLU, KSparse, TRAP, BE, etc.
## High-level solvers
Go to the '[Solver]' section in the modelParam file and modify both the solver name as well as the wrapper file. For using SPICE solver, you have to have the __Xyce 6.12__ installed in your system. Supported high-level solvers are listed below:

### SuperLU (only for steady-state): 

* Name = SuperLU

* Wrapper = SuperLU.py

### SPICE_steady (.OP):

* Name = SPICE_steady

* Wrapper = SPICESolver_steady.py

Steady-state SPICE solver grid temperature files are saved as RC_steady.cir.csv. Steady-state SPICE solver log files are saved as RC_steady.log. The steady-state block-level temperatures will be printed in the terminal.

### SPICE_transient (.TRAN):

* Name = SPICE_transient

* Wrapper = SPICESolver_transient.py

Users can modify the step_size, total_simualtion_time, and ptrace_step_size options under the [Simulation] section in modelParams_files to redefine the simulation step size and simulation time, and ptrace step size of the transient simulation, respectively.
Transient SPICE solver grid temperature files are saved as RC_transient.cir.csv. Transient SPICE solver block temperature files are saved as RC_transient_block_temp.csv. SPICE solver log files are saved as RC_transioent.log. The last step block_level transient temperature results will be printed in the terminal.

## Low-level solvers
To change the low-level solver types for SPICE solver, users need to modify the ll_steady_solver or ll_transient_solver option under the [Solver] section in  modelParams_files. Note that, SuperLU solver does not support low-level solver.

Available solvers and usage can be found in [1] and Xyce user guide:

https://xyce.sandia.gov/downloads/_assets/documents/Users_Guide.pdf

# Enable Parallel Thermal Simulation:
To enable Parallel Thermal Simulation with PACT, users need to install the __Xyce 6.12__ parallel version and __OpenMPI 3.1.4__.
One needs to modify the number_of_core option in the modelParams_files [Simulation] section to change the number of cores used in the PACT parallel simulation. Note that, to run parallel simulations on a Linux server, users need to start an interactive session by running _qrsh_ or _qsh_. Or, users can submit batch jobs by using _qsub_. Note that, SuperLU solver does not support parallel thermal simulation, it only supports sequential thermal simulation. If the users are running PACT with serial version of __Xyce 6.12__, please set number_of_core to 1.

# OpenROAD Interface:
Please go to the ~/src/OpenRoad folder for more information.

# Example Command Line Test Case:
The Example_command_line folder contains all the necessary files to run steady-state and transient simulations of a 10mmX10mm chip with a 500um hot spot placed at the center. The example_ptrace.csv contains 3 power traces. For steady-state simulation, PACT will average the power trace for each block and perform steady-state simulations. For transient simulation, PACT with SPICE_transient solver will performance transient simulation with user-defined ptrace step size, simulation step size, and total simulation time. User can define these 3 parameters in example_modelParans.config. The default heat sink is a medium-cost heat sink adopted from HotSpot [2] Users can uncomment the [NoPackge] and [NoPackage_sec] labels and comment out [HeatSink] and [HeatSink_sec] labels in example_modelParams.config to enable the fixed-air convection heat sink. In addtion, users also need to uncomment the [NoPackage] label and comment out the [HeatSink] label in the example.config file.
Users can run this command line test case by typing the following command inside the Example_command_line folder:

```python
    python ../src/PACT.py example_lcf.csv example.config example_modelParams.config --gridSteadyFile example.grid.steady
```
The layerwise grid temperature results will be saved as example.grid.steady.layer0 and example.grid.steady.layer1. Here layer0 is the processor and layer1 is the cooling package. The steady-state and transient SPICE simulation grid temperature results will be saved as RC_steady.cir.csv and RC_transient.cir.csv. The transient block temperature results will be saved as RC_transient_block_temp.csv. The SPICE simulation log information will be saved as RC_steady.log or RC_transient.log.


Note that, this command line test case assumes the users have already installed the __Xyce 6.12__ parallel version and __OpenMPI 3.1.4__. If the users haven't installed these two software, please change the solver to SuperLU. If the users are running PACT with serial version of PACT, please make sure you set the number_of_core option in the example_modelParams.config to 1. 


# Example Script Test Cases:
We have provided several script test cases in the Example folder for the users to test.

* The test chip sizes are set to 5mmX5mm, 10mmX10mm, and 20mmX20mm.

* We include uniform power density test cases of [40-200] W/cm<sup>2</sup>.

* We have also included non-uniform power density test cases with a background power density of 50 W/cm<sup>2</sup> and hot spot power density of [500-2000] W/cm<sup>2</sup>. 

* Users can choose the location of the hot spot as well as the number of hot spots by change the __hs_loc__ option in "qsub_Hetero_500um.py" scipt to ['center', 'edge', 'corner','multiple_center','multiple_offcenter']. The detailed non-uniform floorplans can be found in /Example/flp_files/ folder.

* To test the heterogeneity, we also include chips with heterogeneous materials such as silicon and copper. 

* The cooling package is set to fixed air convection HTC, users can change the HTC based on their need. 

* Users can also choose a different number of grids used in the simulation (e.g., 40X40, 80X80, 160X160, etc.). Users can specify the number of grids used in the simulation as multiple of 2 and 5 or as a power of 2.

To run thermal simulations, go to /Example/scripts/ and run qsub_10mm.py, qsub_20mm.py, and qsub_Hetero_500um.py as shown below:

```
    $cd Example/scripts/
    $python qsub_10mm.py
```
or

```
    $cd Example/scripts/
    $python qsub_20mm.py
```

or

```
    $cd Example/scripts/
    $python qsub_Hetero_500um.py
```

You can choose various synthetic power profiles, floorplans, and test cases within the python script. 

__qsub_10mm.py__: steady-state and transient analysis for homogeneous chips with a chip size of 10mm with both uniform power density and non-uniform power density profiles.

__qsub_20mm.py__: steady-state and transient analysis for homogeneous chips with a chip size of 20mm with both uniform power density and non-uniform power density profiles.

__qsub_Hetero_500um.py__: steady-state and transient analysis for heterogeneous chips (Copper and Silicon) with chip sizes of 5mm,10mm, and 20mm with non-uniform power density profiles. Users can select different hot spot locations and the number of hot spots.

Note that, these example script test cases assume the users have already installed the __Xyce 6.12__ parallel version and __OpenMPI 3.1.4__.
If the users haven't installed these two software, please change the solver to SuperLU. If the users are running PACT with serial version of __Xyce 6.12__, please make sure you set the number_of_core option in the modelParams files to 1. 

Users can also modify the corresponding modelParam files in the /Example/modelParams_files/ to select the simulation type as well as the solver.

For simulation using SPICE solvers, users can find the SPICE solver grid temperature simulation results located in /src/ folder as RC_steady.cir.csv or RC_transient.cir.csv. Users can also find the SPICE transient block temperature results in /src/ folder as RC_transient_block_temp.csv. The SPICE solver log files are located in /src/ folder as RC_steady.log or RC_transient.log. For simulation using SuperLU, users can find the grid temperature simulation results and log files in /Example/results/ and /Example/logs/ folders. For steady-state simulation, the block-level temperature results will be printed in the terminal. For transient simulation, the last step of the block-level transient temperature results will be printed in the terminal. 

Example block-level temperature output:

![](/image/output.PNG)

Here layer0 is the processor and layer1 is the cooling package. 

# Developers:

* Prachi Shukla

* Zihao Yuan

* Sofiane Chetoui

* Sean Nemtzow 

If you have any questions regarding PACT, please send emails to yuan1z@bu.edu.

# Principal Investigator (PI):

Prof.Ayse K Coskun from Boston University

https://www.bu.edu/eng/profile/ayse-coskun/

Prof. Shereif Reda from Brown University

https://vivo.brown.edu/display/sreda

# Acknowledgment

PACT has been partially funded by the NSF CRI (CI-NEW) grant #1730316/1730003/1730389. Some of the features in PACT frontend have been implemented with inspiration from HotSpot [2], such as the structure of the network of grid cells and blocks, file structure (e.g., lcf, flp, ptrace files), and the building of the matrices for the superLU solver. This is a design decision to ease the use of PACT for the community.

# Reference:
[1] Zihao Yuan, Prachi Shukla, Sofiane Chetoui, Sean Nemtzow, Sherief Reda, and Ayse K. Coskun, “PACT: An Extensible Parallel Thermal Simulator for Emerging Integration and Cooling Technologies”. To be submitted to _IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems (TCAD)_, 2020.

[2] Skadron, K., Stan, M. R., Huang, W., Velusamy, S., Sankaranarayanan, K., and Tarjan, D. "Temperature-aware microarchitecture." _ACM SIGARCH Computer Architecture News_, 2003.

[3] Shukla, Prachi, et al. "An overview of thermal challenges and opportunities for monolithic 3D ICs." _Proceedings of the 2019 on Great Lakes Symposium on VLSI_, 2019.

[4] Coskun, A., Eris, F., Joshi, A., Kahng, A. B., Ma, Y., and Srinivas, V. "A cross-layer methodology for design and optimization of networks in 2.5 d systems." _Proceedings of the International Conference on Computer-Aided Design_, 2018.

[5] Ajayi, Tutu, et al. "Toward an open-source digital flow: First learnings from the openroad project." _Proceedings of the 56th Annual Design Automation Conference_, 2019.






