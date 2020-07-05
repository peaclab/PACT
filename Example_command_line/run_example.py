import os

#os.system("python ../src/PACT.py example_lcf_2ptraces.csv example.config example_modelParams_SuperLU.config --gridSteadyFile example.grid.steady")
#Next 2 runs should generate the same output#
os.system("python ../src/PACT.py example_lcf.csv example.config example_modelParams_SuperLU.config --gridSteadyFile example.grid.steady")
os.system("python ../src/PACT.py example_lcf_2ptraces_same.csv example.config example_modelParams_SuperLU.config --gridSteadyFile example.grid.steady")
#os.system("python ../src/PACT.py example_lcf_2ptraces.csv example.config  example_modelParams.config --gridSteadyFile example.grid.steady") # For Zihao
