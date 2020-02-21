import os

#bgpd = [20,30,40,50]
#hspd = [500,750,1000,1350,1500]

#hs_loc = ['corner','multiple_center','multiple_offcenter']
hs_loc = ['center','corner','edge','multiple_center','multiple_offcenter']
bgpd = [30,50]
hspd = [500,1000,1500]
#bgpd = [30]
#hspd = [500,1500]

fname=''
grid='40'
#grid='80'
#chiplabel='10mm'
#chiplabel='20mm'
chiplabel='5mm'
flp_file = chiplabel+"_flp"
lcf_file = chiplabel+"_lcf"
scp_dir="/home/prachis/EDA_Validation/"+chiplabel+"/"+grid+"x"+grid
grid_dir=chiplabel+'/'+grid+'x'+grid+'/'

### Non-uniform ####
"""
for bg_idx, bg in enumerate(bgpd):
    for hs_idx, hs in enumerate(hspd):
        for loc in hs_loc:
            os.system('python3 CRICoolingTool.py Tests_withHotSpot/'+lcf_file+'_NonUniformPD_'+loc+str(bg)+'_'+str(hs)+'Wcm2.csv Tests_withHotSpot/default.config  Tests_withHotSpot/modelParams.config --gridSteadyFile ' + grid_dir+'MyToolRun_NonUniformPD_'+loc+str(bg)+'_'+str(hs)+'Wcm2.csv')
            os.system('cp ../results/'+grid_dir+'MyToolRun_NonUniformPD_'+loc+str(bg)+'_'+str(hs)+'Wcm2.csv /home/prachis/EDA_Validation/'+grid_dir+'MyToolRun_'+loc+str(bg)+'_'+str(hs)+'Wcm2.grid.steady')
"""
### Uniform Power density ####
#"""
#bgpd = [40,80,120,160,200]
#bgpd = [80,120,160,200]
bgpd = [80]
for bg_idx, bg in enumerate(bgpd):
    os.system('python3 CRICoolingTool.py Tests_withHotSpot/'+lcf_file+'_UniformPD_'+str(bg)+'Wcm2.csv Tests_withHotSpot/default.config  Tests_withHotSpot/modelParams.config --gridSteadyFile ' + grid_dir+'MyToolRun_UniformPD_'+str(bg)+'Wcm2.csv')
####    os.system('cp ../results/'+grid_dir+'MyToolRun_UniformPD_'+str(bg)+'Wcm2.csv /home/prachis/EDA_Validation/'+grid_dir+'MyToolRun_'+str(bg)+'Wcm2.grid.steady')
#"""
