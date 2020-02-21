import os

#grid_rows='40'
#grid_cols='40'
#chiplabel='5mm'
#grid_rows='80'
#grid_cols='80'
grid_rows='160'
grid_cols='160'
chiplabel='20mm'
lcf_file = chiplabel+"_lcf"
scp_dir="/home/prachis/EDA_Validation/"
folder = 'Tests_withHotSpot/'
configFile = 'default.config'
modelParamsFile = 'modelParams.config'
runName = 'MyToolRun'

### Non-uniform ####
"""
pdenType = 'NonUniformPD'
#hs_loc = ['corner','multiple_center','multiple_offcenter']
hs_loc = ['center','corner','edge','multiple_center','multiple_offcenter']
#hs_loc = ['center']
bgpd = [30,50]
hspd = [500,1000,1500]
#bgpd = [30]
#hspd = [500]
for bg_idx, bg in enumerate(bgpd):
    for hs_idx, hs in enumerate(hspd):
        for loc in hs_loc:
            pdenVal = loc+str(bg)+'_'+str(hs)
            os.system('Si_only.sh '+ chiplabel + ' '+ folder + ' '+ lcf_file +' ' +configFile + ' ' + modelParamsFile + ' ' + pdenType + ' ' + pdenVal + ' ' + scp_dir + ' ' + grid_rows + ' ' + grid_cols + ' ' + runName)



"""
### Uniform Power density ####
#bgpd = [40,80,120,160,200]
bgpd = [80,120,160,200]
pdenType = 'UniformPD'
#bgpd = [40,80]
for bg_idx, bg in enumerate(bgpd):
    pdenVal = str(bg)
    os.system('Si_only.sh '+ chiplabel + ' '+ folder + ' '+ lcf_file +' ' +configFile + ' ' + modelParamsFile + ' ' + pdenType + ' ' + pdenVal + ' ' + scp_dir + ' ' + grid_rows + ' ' + grid_cols + ' ' + runName)
#"""
