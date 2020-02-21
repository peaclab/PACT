import os
#Run 0
chiplabel="2mm"
lcf_file = "lcf_4"
coolant ="water/"
#coolant ="r134a/"
#coolant ="r141b/"
grid_dir=chiplabel+'/64x64/'+coolant


#"""
bg = 100
#bg = 20
os.system('python3 CRICoolingTool.py Tests_withHotSpot/'+lcf_file+'_UniformPD_'+str(bg)+'Wcm2.csv Tests_withHotSpot/default2Phase.config  Tests_withHotSpot/modelParams2Phase.config --gridSteadyFile ' + grid_dir+'2PhaseRunUniformPD_'+str(bg)+'.csv')
os.system('cp ../results/'+grid_dir+'2PhaseRunUniformPD_'+ str(bg)+'.csv /home/prachis/EDA_Validation/'+grid_dir+'2PhaseRunUniformPD_'+str(bg)+'.grid.steady')
#"""

#""" Non-uniform
bg = 50
hs = 300
#bg = 20
#hs = 75
os.system('python3 CRICoolingTool.py Tests_withHotSpot/'+lcf_file+'_NonUniformPD_'+str(bg)+'_'+str(hs)+'Wcm2.csv Tests_withHotSpot/default2Phase.config  Tests_withHotSpot/modelParams2Phase.config --gridSteadyFile ' + grid_dir+'2PhaseRunNonUniformPD_'+str(bg)+'_'+str(hs)+'.csv')
os.system('cp ../results/'+grid_dir+'2PhaseRunNonUniformPD_'+ str(bg)+'_'+str(hs)+'.csv /home/prachis/EDA_Validation/'+grid_dir+'2PhaseRunNonUniformPD_'+str(bg)+'_'+str(hs)+'.grid.steady')
#"""
