import os
#import sys, argparse
#import configparser

#os.system('python3 CRICoolingTool.py ../lcf_files/Layer_lcf.csv ../config_files/default.config  ../modelParams_files/modelParams.config')
#os.system('python3 CRICoolingTool.py Layer_lcf.csv default.config  modelParams.config')

#os.system('python3 -m cProfile -o cri.pyprof CRICoolingTool.py Layer_lcf.csv default.config  modelParams.config')

##Tests_withHotSpot
#Run 1 grid = 4x4
#os.system('python3 CRICoolingTool.py Tests_withHotSpot/L0_lcf.csv Tests_withHotSpot/default.config  Tests_withHotSpot/modelParams.config --gridSteadyFile 4x4Run1.csv')

#Run 1' grid = 8x8
#os.system('python3 CRICoolingTool.py Tests_withHotSpot/L0_lcf.csv Tests_withHotSpot/default.config  Tests_withHotSpot/modelParams.config --gridSteadyFile 8x8Run1.csv')

#Run 1'' grid = 16x16
#os.system('python3 CRICoolingTool.py Tests_withHotSpot/L0_lcf.csv Tests_withHotSpot/default.config  Tests_withHotSpot/modelParams.config --gridSteadyFile 16x16Run1.csv')

#Run 2
#os.system('python3 CRICoolingTool.py Tests_withHotSpot/L0_lcf_1_P0.csv Tests_withHotSpot/default.config  Tests_withHotSpot/modelParams.config')

#Run 3
#os.system('python3 CRICoolingTool.py Tests_withHotSpot/L0_lcf_1_P1.csv Tests_withHotSpot/default.config  Tests_withHotSpot/modelParams.config')

#Run 4
#os.system('python3 CRICoolingTool.py Tests_withHotSpot/L0_lcf_1_P2.csv Tests_withHotSpot/default.config  Tests_withHotSpot/modelParams.config')

#Run 5
#os.system('python3 CRICoolingTool.py Tests_withHotSpot/L0_lcf_1_P3.csv Tests_withHotSpot/default.config  Tests_withHotSpot/modelParams.config')

#Run 6
#os.system('python3 CRICoolingTool.py Tests_withHotSpot/L0_lcf_1_P4.csv Tests_withHotSpot/default.config  Tests_withHotSpot/modelParams.config')

#Run 7
run_idx=7 #For non-uniform
#chiplabel="5mm"
#lcf_file = "L0_lcf_2"
chiplabel="20mm"
lcf_file = "L0_lcf_3"
# chiplabel not added for 10 mm
grid_dir=chiplabel+'/100x100/'
#grid_dir='40x40/'
#grid_dir=''
#"""
for i in range(20): #For non-uniform
    os.system('python3 CRICoolingTool.py Tests_withHotSpot/'+lcf_file+'_NonUniformP'+str(i)+'.csv Tests_withHotSpot/default.config  Tests_withHotSpot/modelParams.config --gridSteadyFile ' + grid_dir+'Run'+str(run_idx)+'.csv')
    os.system('cp ../results/'+grid_dir+'Run'+ str(run_idx)+'.csv /home/prachis/EDA_Validation/'+grid_dir+'Run'+str(run_idx)+'_L0.grid.steady')
    run_idx += 1
#"""
#"""
#run_idx = 2 #For uniform
run_idx = 3 #For uniform
#for i in range(5): #For uniform
for i in range(1,5): #For uniform
    os.system('python3 CRICoolingTool.py Tests_withHotSpot/'+lcf_file+'_P'+str(i)+'.csv Tests_withHotSpot/default.config  Tests_withHotSpot/modelParams.config --gridSteadyFile ' + grid_dir+'Run'+str(run_idx)+'.csv')
    os.system('cp ../results/'+grid_dir+'Run'+ str(run_idx)+'.csv /home/prachis/EDA_Validation/'+grid_dir+'Run'+str(run_idx)+'_L0.grid.steady')
    run_idx += 1
#"""    
    ######Below: 20x20 grids#####
    #os.system('python3 CRICoolingTool.py Tests_withHotSpot/L0_lcf_1_NonUniformP'+str(i)+'.csv Tests_withHotSpot/default.config  Tests_withHotSpot/modelParams.config --gridSteadyFile ' + 'Run'+str(run_idx)+'.csv')
    #os.system('cp ../results/Run'+ str(run_idx)+'.csv /home/prachis/EDA_Validation/Run'+str(run_idx)+'_L0.grid.steady')
    #run_idx += 1
