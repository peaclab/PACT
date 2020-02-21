import os

grid_rows='100'
grid_cols='100'
chiplabel='12_6mm'
lcf_file = chiplabel+"_lcf"
scp_dir="/home/prachis/EDA_Validation/"+chiplabel+"/"+grid_rows+"x"+grid_cols+"/Lateral_TRUE_Vertical_TRUE/"
folder = 'Tests_withHotSpot/'
modelParamsFile = 'modelParamsNoPackage.config'
runName = 'MyToolRun'

#"""
### Uniform Power density ####
#bgpd = [40,80,120,160,200]
bgpd = [20,30,40,50]
pdenType = 'UniformPD'
htc_val = ['htc_1e6','htc_1e5','htc_1e4']
#bgpd = [40,80]
for bg_idx, bg in enumerate(bgpd):
    for htc in htc_val: 
        configFile = 'default_'+htc+'.config'
        pdenVal = str(bg)
        os.system('NoPackage.sh '+ chiplabel + ' '+ folder + ' '+ lcf_file +' ' +configFile + ' ' + modelParamsFile + ' ' + pdenType + ' ' + pdenVal + ' ' + scp_dir + ' ' + grid_rows + ' ' + grid_cols + ' ' + runName + ' ' + htc)
#"""
