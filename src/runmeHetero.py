import os
#Run 0
chiplabel="Hetero_2mm"
lcf_file = chiplabel+"_lcf"
#grid_dir=chiplabel+'/64x64/'
grid_dir=chiplabel+'/64x64/'


#"""
bgpd = [50,100,100,150,200]
#bgpd = [20]
for bg in bgpd:
    os.system('python3 CRICoolingTool.py Tests_withHotSpot/'+lcf_file+'_UniformPD_'+str(bg)+'Wcm2.csv Tests_withHotSpot/defaultHetero.config  Tests_withHotSpot/modelParamsHetero.config --gridSteadyFile ' + grid_dir+'MyToolRunUniformPD_'+str(bg)+'Wcm2.csv')
    os.system('cp ../results/'+grid_dir+'MyToolRunUniformPD_'+ str(bg)+'Wcm2.csv /home/prachis/EDA_Validation/'+grid_dir+'MyToolRunUniformPD_'+str(bg)+'Wcm2.grid.steady')
#"""

#""" Non-uniform

bgpd = [50]
hspd = [500,1000,1500,2000]
#hspd = [500]

for bg in bgpd:
    for hs in hspd:
        os.system('python3 CRICoolingTool.py Tests_withHotSpot/'+lcf_file+'_NonUniformPD_'+str(bg)+'_'+str(hs)+'Wcm2.csv Tests_withHotSpot/defaultHetero.config  Tests_withHotSpot/modelParamsHetero.config --gridSteadyFile ' + grid_dir+'MyToolRunNonUniformPD_'+str(bg)+'_'+str(hs)+'Wcm2.csv')
        os.system('cp ../results/'+grid_dir+'MyToolRunNonUniformPD_'+ str(bg)+'_'+str(hs)+'Wcm2.csv /home/prachis/EDA_Validation/'+grid_dir+'MyToolRunNonUniformPD_'+str(bg)+'_'+str(hs)+'Wcm2.grid.steady')

#"""
