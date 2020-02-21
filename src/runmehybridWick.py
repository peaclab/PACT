import os
#Run 0
chiplabel="2mm"
lcf_file = "hybridWick_lcf"
coolant ="water/"
#coolant ="r134a/"
#coolant ="r141b/"
grid_dir=chiplabel+'/32x32/'+coolant


#"""
bg = 100
#bg = 20
os.system('time python3 CRICoolingTool.py Tests_withHotSpot/'+lcf_file+'_UniformPD_'+str(bg)+'Wcm2.csv Tests_withHotSpot/defaultHybridWick.config  Tests_withHotSpot/modelParamsHybridWick.config --gridSteadyFile ' + grid_dir+'HybridWickRunUniformPD_'+str(bg)+'.csv')
######os.system('cp ../results/'+grid_dir+'twophaseRunUniformPD_'+ str(bg)+'.csv /home/prachis/EDA_Validation/'+grid_dir+'twophaseRunUniformPD_'+str(bg)+'.grid.steady')
#"""

""" Non-uniform
bg = 50
hs = 100
#bg = 20
#hs = 25
os.system('python3 CRICoolingTool.py Tests_withHotSpot/'+lcf_file+'_NonUniformPD_'+str(bg)+'_'+str(hs)+'Wcm2.csv Tests_withHotSpot/default2Phase.config  Tests_withHotSpot/modelParams2Phase.config --gridSteadyFile ' + grid_dir+'twophaseRunNonUniformPD_'+str(bg)+'_'+str(hs)+'.csv')
os.system('cp ../results/'+grid_dir+'twophaseRunNonUniformPD_'+ str(bg)+'_'+str(hs)+'.csv /home/prachis/EDA_Validation/'+grid_dir+'twophaseRunNonUniformPD_'+str(bg)+'_'+str(hs)+'.grid.steady')
"""
