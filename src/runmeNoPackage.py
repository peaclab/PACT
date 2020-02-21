###This is only for validating the No Package model in Itherm#####
import os

fname=''
grid='100'
chiplabel='12_6mm'
flp_file = chiplabel+"_flp"
lcf_file = chiplabel+"_lcf"
scp_dir="/home/prachis/EDA_Validation/"+chiplabel+"/"+grid+"x"+grid
grid_dir=chiplabel+'/'+grid+'x'+grid+'/'

htc_val = ['htc_1e6','htc_1e5','htc_1e4']
#htc_val = ['htc_1e4']
### Uniform Power density ####
bgpd = [20,30,40,50]
#bgpd = [50]
for bg_idx, bg in enumerate(bgpd):
    for htc in htc_val: 
        os.system('python3 CRICoolingTool.py Tests_withHotSpot/'+lcf_file+'_UniformPD_'+str(bg)+'Wcm2.csv Tests_withHotSpot/default_'+htc+'.config  Tests_withHotSpot/modelParamsNoPackage.config --gridSteadyFile ' + grid_dir+'MyToolRun_UniformPD_'+str(bg)+'Wcm2_'+htc+'.csv')
        os.system('cp ../results/'+grid_dir+'MyToolRun_UniformPD_'+str(bg)+'Wcm2_'+htc+'.csv /home/prachis/EDA_Validation/'+grid_dir+'MyToolRun_'+str(bg)+'Wcm2_'+htc+'.grid.steady')
#"""
