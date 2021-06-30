# PACT: A Standard Cell Level to Architectural Level Parallel Compact Thermal Simulator
# Introduction
PACT is a SPICE-based PArallel Compact Thermal simulator (PACT) that enables fast and accurate standard-cell-level to architecture-level steady-state and transient parallel thermal simulation. PACT utilizes the advantages of multi-core processing (OpenMPI) and includes several solvers to speed up both steady-state and transient simulations. PACT can be easily extended to model a variety of emerging integration and cooling technologies, such as 3D stacking, liquid cooling via microchannels, and others, by simply modifying the thermal netlist. PACT can be also used in conjunction with popular architecture-level performance and power simulators to evaluate thermal profiles of processors. 

The simulation flow of PACT is shown in the following image.

<!-- ![](/image/PACTflow.PNG|width=100) -->
<center><img src="/image/PACTflow.PNG" width="600" height="300">

PACT takes a configuration file, a floorplan file, a layer (lcf) file, a parameter (modelParams) file, and a power trace (ptrace) file as inputs and outputs the steady-state/transient temperature results.
<!---
The config file describes the material property, initial temperature, as well as cooling package information. The floorplan file describes the chip information that includes chip size, number of blocks, block sizes and location, and block material property. Lcf file stands for the layer configuration file, which basically shows the layer stack with cooling information. Ptrace file allocates the power number for each active block inside the chip stack. ModelParams file shows the simulation information (e.g., steady-state/transient, solver type, number of grids, package information, etc.)
-->
More details about PACT can be found in our TCAD paper [1].


All the source codes that are located inside the /src folder include the SuperLU solver as well as the SPICE solvers. Steady-state and transient SPICE-based solvers are named as SPICE_steady and SPICE_transient, respectively.


# Requirements
PACT is written in Python and uses __Xyce 6.12__ as the backend SPICE engine.

* Required Python version: > 3.6.5

* Required Python libraries: sys, numpy, pandas, math, os, scipy, argparse, configparser.

* Users can directly install the correct version of the Python packages through the following commands:
```
pip install -r requirements.txt
```

The above libraries are sufficient for the users to run PACT with the SuperLU solver. For users who want to run PACT with the SPICE engine, one needs to install either __Xyce 6.12__ serial version or __Xyce 6.12__ parallel version.

Installation guideline for __Xyce 6.12__: 

* https://xyce.sandia.gov/
* https://xyce.sandia.gov/documentation/BuildingGuide.html

Users who want to run parallel thermal simualtions with PACT need to install __Xyce 6.12__ parallel version and __OpenMPI 3.1.4__:

* https://www.open-mpi.org/

It is recommended to use Linux or macOS to run PACT. To enable sequential and parallel thermal simulations with PACT on Windows, users have to use __Cygwin__ to build the __Xyce 6.12__ and __OpenMPI 3.1.4__ and run PACT using the __Cygwin__ terminal. __Cygwin__ download link:

* https://www.cygwin.com/


If __Xyce 6.12__ and __OpenMPI 3.1.4__ have already been installed in your Linux server, then you can simply load the following dependencies to load Xyce and OpenMPI.
```
module load python3/3.6.5 gcc/5.5.0 fftw/3.3.8 netcdf/4.6.1 blis/0.6.0 openmpi/3.1.4 xyce/6.12
```


# Usage
1. Config file (i.e., [./Example/config_files/](./Example/config_files/)) describes the layer material properties.
    1. Thickness defines the layer thickness.
    2. HTC is the heat transfer coefficient between the ambient and the heat sink.
    3. Thermal resistivity and specific heat capacity are used to calculate the thermal resistor and capacitor values.
    4. [Init] defines the ambient temperature.
    5. Users can select the heat sink as well as its parameters.
2. Floorplan (i.e., [./Example/flp_files/](./Example/flp_files/) (.CSV file)) describes the chip floorplan.
    1. Depending on the desired simulation granularity, users can define a standard-cell-level chip floorplan with a large number of units or an architecture-level floorplan that includes microarchitectural hardware blocks.
    2. UnitName is the name of the unit.
    3. X and Y define the location of the unit.
    4. Length (m) and Width (m) describe the unit size.
    5. Label describes the material or the cooling property of the unit.
    6. Users can ignore the configfile option for now. The configfile option is for enabling two-phase vapor chamber with micropillar wick evaporators and hybrid wick evaporators. We will release these two emerging cooling packages in the later version of PACT.
3.  Layer configuration file (i.e., [./Example/lcf_files/](./Example/lcf_files/) (.CSV file)) describes the layer stack.
    1. Layer describes the layer number; all layers are stacked vertically starting from layer 0, where layer 0 is the closest from the package/heat sink.
    2. Floorplan file describes the floorplan for the specific layer.
    3. PtraceFile: if a layer is active (consumes power), then its corresponding power trace file needs to be specified here.
4. Power trace file (i.e., [./Example/ptrace_files/](./Example/ptrace_files/) (.CSV file)) provides the transient power consumption.
    1. UnitName is the name of the unit in the floorplan.
    2. Power (W) is the power consumption for the unit.
5. Model parameter files (i.e., [./Example/modelParams_files/](./Example/modelParams_files/)):
    1. [PATH] defines the path to the library, ptrace, flp.
    2. [Simulation] defines the simulation type (e.g, steady-state or transient). 
    3. [Solver] selects the solver (SuperLU, SPICE_steady, SPICE_transient).
    4. [Grid] is the number of grid cells used in the simulation. 
    5. Users can also define the heat sink characteristics, cooling properties, and other cooling options.
6. Command to run simulation with PACT:
    ```python
    python PACT.py <lcf_file> <config_file> <modelParams_file> --gridSteadyFile <grid_file>
    ```
    For steady-state simulation, the grid_file specifies the steady-state grid temperature output of the PACT simulation. For transient simulation, the last step transient grid temperature results will be saved in grid_file. In the meantime, both the transient grid temperature traces and the transient block temperature traces will be saved.

# Options for Solvers: 
We divide the solver section into high-level solvers as well as low-level solvers. High-level solvers include SuperLU and SPICE solvers.
Low-level solvers include KLU, KSparse, TRAP, BE, etc.
## High-level solvers
Go to the '[Solver]' section in the modelParam file and modify both the solver name as well as the wrapper file. For using the SPICE solver, you have to have the __Xyce 6.12__ installed on your system. Supported high-level solvers are listed below:

### SuperLU (only for steady-state): 

* Name = SuperLU
* Wrapper = SuperLU.py
* SuperLU solver does not support modeling liquid cooling, medium cost heat sink, or parallel thermal simulation.

### SPICE_steady (.OP):

* Name = SPICE_steady
* Wrapper = SPICESolver_steady.py

Steady-state SPICE solver grid temperature files are saved as {ChipName}.cir.csv. Steady-state SPICE solver log files are saved as {ChipName}.log. The steady-state block-level temperatures will be printed in the terminal.

### SPICE_transient (.TRAN):

* Name = SPICE_transient
* Wrapper = SPICESolver_transient.py

Users can modify the step_size, total_simualtion_time, and ptrace_step_size options under the [Simulation] section in modelParams_files to redefine the simulation step size and simulation time, and ptrace step size of the transient simulation, respectively.
Transient SPICE solver grid temperature files are saved as {ChipName}.cir.csv. Transient SPICE solver block temperature files are saved as {ChipName}.block.transient.csv. SPICE solver log files are saved as {ChipName}.log. The last step block_level transient temperature results will be printed in the terminal.

## Low-level solvers
To change the low-level solver types for SPICE solver, users need to modify the ll_steady_solver or ll_transient_solver option under the [Solver] section in  modelParams_files. Note that, SuperLU solver does not support low-level solver.

Available solvers and usage can be found in [1] and Xyce user guide:

https://xyce.sandia.gov/downloads/_assets/documents/Users_Guide.pdf

## Iterative Solver Convergence Issue
When doing steady-state simulations with iterative solvers such as AztecOO, for some of the problems, there might be a convergence issue. PACT will 
report "time step too small" error. To avoid this, users need to change the steady-state solver for both steady-state and transient to direct solvers such as KLU or KSparse. We set the DC analysis (steady-state) solver as KLU for transient simulation as default. 

# Enable Parallel Thermal Simulation:
To enable Parallel Thermal Simulation with PACT, users need to install the __Xyce 6.12__ parallel version and __OpenMPI 3.1.4__.
One needs to modify the number_of_core option in the modelParams_files [Simulation] section to change the number of cores used in the PACT parallel simulation. Note that, to run parallel simulations on a Linux server, users need to start an interactive session by running _qrsh_ or _qsh_. Or, users can submit batch jobs by using _qsub_. Note that, SuperLU solver does not support parallel thermal simulation, it only supports sequential thermal simulation. If the users are running PACT with serial version of __Xyce 6.12__, please set number_of_core to 1.

# Enable Transient Thermal Simulation with an Initial Temperature File:
To enable transient thermal simulation with an initial temperature file, users should typically first run a steady-state simulation to generate the initial temperature file (e.g., {ChipName}.cir.ic). Then, users need to set init_file = True in the [Simulation] section in modelParams.config file. Then PACT will include the initial temperature file as the initial temperatures for each node and carry out the transient simulation. Note that the grid resolution for steady-state simulation and transient simulation have to be the same (Xyce SPICE engine will raise an error if the grid resolution does not match). We recommend always running a steady-state simulation first before running a transient simulation with an initial temperature file. 

# Modeling Emerging On-Chip Cooling Methods
The current version of PACT includes a medium-cost heat sink adopted from HotSpot [2], a fixed-air convection HTC heat sink, and models for liquid cooling via microchannels. 

We have also built emerging cooling packages such as thermoelectric coolers [6] and two-phase vapor chambers with micropillar wick and hybrid wick evaporators [7,8,9]. We will add these cooling models to the PACT repository later on. 

# OpenROAD Interface:
Please go to the [./src/OpenRoad/](./src/OpenRoad/) folder for more information.

# Example Command Line Test Case:
The Example_command_line folder contains all the necessary files to run steady-state and transient simulations of a 10mmX10mm chip with a 500um hot spot placed at the center. The example_ptrace.csv contains 3 power traces. For steady-state simulation, PACT will average the power trace for each block and perform steady-state simulations. For transient simulation, PACT with SPICE_transient solver will run with a user-defined ptrace step size, a simulation step size, and a total simulation time. Users can define these 3 parameters in example_modelParams.config. 

The default heat sink is a medium-cost heat sink adopted from HotSpot [2]. Users can uncomment the [NoPackage] and [NoPackage_sec] labels and comment out [HeatSink] and [HeatSink_sec] labels in example_modelParams.config to enable the fixed-air convection heat sink. In addition, users also need to uncomment the [NoPackage] label and comment out the [HeatSink] label in the example.config file.

Users can run this command line test case by typing the following command inside the Example_command_line folder:
```python
python ../src/PACT.py example_lcf.csv example.config example_modelParams.config --gridSteadyFile example.grid.steady
```
The layerwise grid temperature results will be saved as example.grid.steady.layer0 and example.grid.steady.layer1. Here layer0 is the processor and layer1 is the cooling package. The steady-state and transient SPICE simulation grid temperature results will be saved as example.cir.csv. The transient block temperature results will be saved as example.block.transient.csv. The SPICE simulation log information will be saved as example.log.

Note that, this command line test case assumes the users have already installed the __Xyce 6.12__ parallel version and __OpenMPI 3.1.4__. If the users have not installed these two software, please change the solver to SuperLU and change the heat sink to NoPackage. If the users are running the serial version of PACT, please make sure you set the number_of_core option in the example_modelParams.config to 1. 


# Example Script Test Cases:
We have provided several script test cases in the Example folder for the users to test.

* The test chip sizes are set to 5mmX5mm, 10mmX10mm, and 20mmX20mm.
* We include uniform power density test cases of [40-200] W/cm<sup>2</sup>.
* We have also included non-uniform power density test cases with a background power density of 50 W/cm<sup>2</sup> and hot spot power density of [500-2000] W/cm<sup>2</sup>. 
* Users can choose the location of the hot spot as well as the number of hot spots by change the __hs_loc__ option in "qsub_Hetero_500um.py" scipt to ['center', 'edge', 'corner','multiple_center','multiple_offcenter']. The detailed non-uniform floorplans can be found in /Example/flp_files/ folder.
* To test heterogeneity within a layer (e.g., due to TSVs in a 3D-stacked chip), we also include chips with heterogeneous materials such as silicon and copper. Users can edit and run "qsub_Hetero_500um.py". The detailed floorplans can be found in /Example/flp_files/ folder.
* The cooling package is set to fixed air convection HTC, users can change the HTC based on their need. 
* Users can also choose a different number of grids used in the simulation (e.g., 40X40, 80X80, 160X160, etc.). Users can specify the number of grids used in the simulation as a multiple of 2 and 5 or as a power of 2.

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

__qsub_Hetero_500um.py__: steady-state and transient analysis for chips with heterogeneous layers (Copper and Silicon) with chip sizes of 5mm,10mm, and 20mm with non-uniform power density profiles. Users can select different hot spot locations and the number of hot spots.

Note that, these example script test cases assume the users have already installed the __Xyce 6.12__ parallel version and __OpenMPI 3.1.4__.
If the users haven't installed these two software, please change the solver to SuperLU. If the users are running PACT with serial version of __Xyce 6.12__, please make sure you set the number_of_core option in the modelParams files to 1. 

Users can also modify the corresponding modelParam files in the /Example/modelParams_files/ to select the simulation type as well as the solver.

For simulation using SPICE solvers, users can find the SPICE solver grid temperature simulation results located in /Example/results/{ChipName} folder as {ChipName}.cir.csv. Users can also find the SPICE transient block temperature results in /Example/results/ folder as {ChipName}.block.transient.csv. The SPICE solver log files are located in /Example/results/{ChipName} folder as {ChipName}.log. For simulation using SuperLU, users can find the grid temperature simulation results and log files in /Example/results/ and /Example/logs/ folders. For steady-state simulation, the block-level temperature results will be printed in the terminal. For transient simulation, the last step of the block-level transient temperature results will be printed in the terminal. 

Example block-level temperature output:
<!-- ![](/image/output.PNG) -->
<center><img src="/image/output.PNG" width="600" height="300">
Here layer0 is the processor and layer1 is the cooling package. 

# Citation and License:

PACT is licensed under GNU General Public License v3.0 license.
If you use PACT for your publications, please cite our TCAD paper [1].

# Developers:

* Prachi Shukla, Boston University
* Zihao Yuan, Boston University
* Sofiane Chetoui, Brown University
* Carlton Knox, Boston University
* Sean Nemtzow, Boston University 

If you have any questions regarding PACT, please send emails to yuan1z@bu.edu.

# Principal Investigators:

Prof. Ayse K. Coskun, Boston University, http://people.bu.edu/acoskun

Prof. Sherief Reda, Brown University, https://scale.engin.brown.edu/pages/sreda.html

# Acknowledgment

PACT has been partially funded by the NSF CRI (CI-NEW) grant #1730316/1730003/1730389 and NSF CCF grant #1910075/1909027.

Some of the features in the PACT frontend have been implemented with inspiration from HotSpot [2], such as the structure of the network of grid cells and blocks, file structure (e.g., lcf, flp, ptrace files), and the building of the matrices for the SuperLU solver. This is a design decision to ease the use of PACT for the community.

# References
[1] Z. Yuan, P. Shukla, S. Chetoui, S. Nemtzow, S. Reda and A. K. Coskun, "PACT: An Extensible Parallel Thermal Simulator for Emerging Integration and Cooling Technologies," to appear in IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems, 2021, doi:10.1109/TCAD.2021.3079166.

[2] Kevin Skadron, Mircea R. Stan, Wei Huang, Sivakumar Velusamy, Karthik Sankaranarayanan, and David Tarjan. "Temperature-aware microarchitecture," in Proceedings of the 30th annual international symposium on Computer architecture (ISCA '03). Association for Computing Machinery, New York, NY, USA, 2–13. doi:10.1145/859618.859620.

[3] Prachi Shukla, Ayse K. Coskun, Vasilis F. Pavlidis, and Emre Salman. "An Overview of Thermal Challenges and Opportunities for Monolithic 3D ICs," in Proceedings of the Great Lakes Symposium on VLSI (GLSVLSI '19). Association for Computing Machinery, New York, NY, USA, 439–444. doi:10.1145/3299874.3319485.

[4] Ayse Coskun, Furkan Eris, Ajay Joshi, Andrew B. Kahng, Yenai Ma, and Vaishnav Srinivas. "A cross-layer methodology for design and optimization of networks in 2.5D systems," in Proceedings of the International Conference on Computer-Aided Design (ICCAD '18). Association for Computing Machinery, New York, NY, USA, Article 101, 1–8. doi:https:10.1145/3240765.3240768.

[5] Tutu Ajayi, Vidya A. Chhabria, Mateus Fogaça, Soheil Hashemi, Abdelrahman Hosny, Andrew B. Kahng, Minsoo Kim, Jeongsup Lee, Uday Mallappa, Marina Neseem, Geraldo Pradipta, Sherief Reda, Mehdi Saligane, Sachin S. Sapatnekar, Carl Sechen, Mohamed Shalan, William Swartz, Lutong Wang, Zhehong Wang, Mingyu Woo, and Bangqi Xu. "Toward an Open-Source Digital Flow: First Learnings from the OpenROAD Project," in Proceedings of the 56th Annual Design Automation Conference (DAC '19). Association for Computing Machinery, New York, NY, USA, Article 76, 1–4. doi:10.1145/3316781.3326334.

[6] F. Kaplan, M. Said, S. Reda and A. K. Coskun, "LoCool: Fighting Hot Spots Locally for Improving System Energy Efficiency," in IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems, vol. 39, no. 4, pp. 895-908, April 2020, doi:10.1109/TCAD.2019.2902355.

[7] Z. Yuan, G. Vaartstra, P. Shukla, S. Reda, E. Wang and A. K. Coskun, "Two-Phase Vapor Chambers with Micropillar Evaporators: A New Approach to Remove Heat from Future High-Performance Chips," in Proceeding of the 18th IEEE Intersociety Conference on Thermal and Thermomechanical Phenomena in Electronic Systems (ITherm), 2019, pp. 456-464, doi:10.1109/ITHERM.2019.8757412.

[8] Z. Yuan, G. Vaartstra, P. Shukla, S. Reda, E. Wang and A. K. Coskun, "Modeling and Optimization of Chip Cooling with Two-Phase Vapor Chambers," in Proceeding of the IEEE/ACM International Symposium on Low Power Electronics and Design (ISLPED), 2019, pp. 1-6, doi:10.1109/ISLPED.2019.8824965.

[9] Z. Yuan, G. Vaartstra, P. Shukla, Zhengmao Lu, E. Wang, S. Reda, and A. K. Coskun, "A Learning-Based Thermal Simulation Framework for Emerging Two-Phase Cooling Technologies," in Proceeding of the Design, Automation & Test in Europe Conference & Exhibition (DATE), 2020, pp. 400-405, doi:10.23919/DATE48585.2020.9116480.






