import os
#Run 0
chiplabel="2mm/"
lcf_file = "OverlapSi_lcf"
grid_label = '128x128'
#grid_dir=chiplabel+'32x32/'
#grid_dir=chiplabel+'25x25/'
grid_dir=chiplabel+grid_label+'/'
#grid_dir=chiplabel+'4x4/'

#grid_label = '32x32'
#grid_label = '4x4'
"""
bg = 100
#bg = 20
os.system('time python3 CRICoolingTool.py Tests_withHotSpot/'+lcf_file+'_UniformPD_'+str(bg)+'Wcm2.csv Tests_withHotSpot/defaultHybridWick.config  Tests_withHotSpot/modelParamsHybridWick.config --gridSteadyFile ' + grid_dir+'HybridWickRunUniformPD_'+str(bg)+'.csv')
######os.system('cp ../results/'+grid_dir+'twophaseRunUniformPD_'+ str(bg)+'.csv /home/prachis/EDA_Validation/'+grid_dir+'twophaseRunUniformPD_'+str(bg)+'.grid.steady')
"""

#""" Non-uniform
bg = 50
#hs = 100
hs = 2000
#python3 -m cProfile -o cri.pyprof
#os.system('time python3 CRICoolingTool.py Tests_withHotSpot/'+lcf_file+'_NonUniformPD_'+str(bg)+'_'+str(hs)+'Wcm2.csv Tests_withHotSpot/defaultOverlapSi.config  Tests_withHotSpot/modelParamsOverlapSi.config_'+grid_label+' --gridSteadyFile ' + grid_dir+'OverlapSiRunNonUniformPD_'+str(bg)+'_'+str(hs)+'.csv')
#os.system('python3 -m cProfile -o cri.pyprof CRICoolingTool.py Tests_withHotSpot/'+lcf_file+'_NonUniformPD_'+str(bg)+'_'+str(hs)+'Wcm2.csv Tests_withHotSpot/defaultOverlapSi.config  Tests_withHotSpot/modelParamsOverlapSi.config_'+grid_label+' --gridSteadyFile ' + grid_dir+'OverlapSiRunNonUniformPD_'+str(bg)+'_'+str(hs)+'.csv')
os.system('time python3 CRICoolingTool.py ../lcf_files/Tests_withHotSpot/'+lcf_file+'_NonUniformPD_'+str(bg)+'_'+str(hs)+'Wcm2.csv ../config_files/Tests_withHotSpot/defaultOverlapSi.config  ../modelParams_files/Tests_withHotSpot/modelParamsOverlapSi.config_'+grid_label+' --gridSteadyFile ../results/' + grid_dir+'OverlapSiRunNonUniformPD_'+str(bg)+'_'+str(hs)+'.csv')
os.system('scp ../results/'+grid_dir+'OverlapSiRunNonUniformPD_'+ str(bg)+'_'+str(hs)+'.csv prachis@128.197.127.15:/home/prachis/EDA_Validation/'+grid_dir+'OverlapSiMyToolRunNonUniformPD_'+str(bg)+'_'+str(hs)+'Wcm2.grid.steady')
#"""
