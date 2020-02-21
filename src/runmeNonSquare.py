import os
#Run 0
chiplabel="2x5mm"
lcf_file = chiplabel+"_lcf"
#grid_dir=chiplabel+'/10x4/'
#grid_dir=chiplabel+'/40x4/'
grid_dir=chiplabel+'/40x8/'


#"""
bgpd = [50,100,100,150,200]
#bgpd = [50]
for bg in bgpd:
    os.system('python3 CRICoolingTool.py Tests_withHotSpot/'+lcf_file+'_UniformPD_'+str(bg)+'Wcm2.csv Tests_withHotSpot/defaultNonSquare.config  Tests_withHotSpot/modelParamsNonSquare.config --gridSteadyFile ' + grid_dir+'MyToolRunUniformPD_'+str(bg)+'Wcm2.csv')
    os.system('cp ../results/'+grid_dir+'MyToolRunUniformPD_'+ str(bg)+'Wcm2.csv /home/prachis/EDA_Validation/'+grid_dir+'MyToolRunUniformPD_'+str(bg)+'Wcm2.grid.steady')
#"""

#""" Non-uniform

bgpd = [50]
hspd = [500,1000,1500,2000]
#hspd = [500]
hs_loc=['center','edge','corner','multiple']
for bg in bgpd:
    for hs in hspd:
        for loc in hs_loc:
            os.system('python3 CRICoolingTool.py Tests_withHotSpot/'+lcf_file+'_NonUniformPD_'+loc+str(bg)+'_'+str(hs)+'Wcm2.csv Tests_withHotSpot/defaultNonSquare.config  Tests_withHotSpot/modelParamsNonSquare.config --gridSteadyFile ' + grid_dir+'MyToolRunNonUniformPD_'+loc+str(bg)+'_'+str(hs)+'Wcm2.csv')
            os.system('cp ../results/'+grid_dir+'MyToolRunNonUniformPD_'+loc+ str(bg)+'_'+str(hs)+'Wcm2.csv /home/prachis/EDA_Validation/'+grid_dir+'MyToolRunNonUniformPD_'+loc+str(bg)+'_'+str(hs)+'Wcm2.grid.steady')

#"""
