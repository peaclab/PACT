import os

grid_rows='128'
grid_cols='128'
chiplabel='2mm'
lcf_file = "OverlapSi_lcf"
scp_dir="/home/prachis/EDA_Validation/"+chiplabel+"/"+grid_rows+"x"+grid_cols+"/"
folder = 'Tests_withHotSpot/'
modelParamsFile = 'modelParamsOverlapSi.config'+'_'+grid_rows+"x"+grid_cols
configFile = 'defaultOverlapSi.config'
runName = 'MyToolRun'

"""
### Non - Uniform Power density ####
bgpd = [50]
#hspd = [100,2000]
hspd = [2000]
#bgpd = [20,30,40,50]
pdenType = 'NonUniformPD'
for bg_idx, bg in enumerate(bgpd):
    for hs_idx, hs in enumerate(hspd):
        pdenVal = str(bg) + '_'+ str(hs)
        os.system('OverlapSi.sh '+ chiplabel + ' '+ folder + ' '+ lcf_file +' ' +configFile + ' ' + modelParamsFile + ' ' + pdenType + ' ' + pdenVal + ' ' + scp_dir + ' ' + grid_rows + ' ' + grid_cols + ' ' + runName)
"""

#"""
### Uniform Power density ####
bgpd = [50]
#bgpd = [20,30,40,50]
pdenType = 'UniformPD'
for bg_idx, bg in enumerate(bgpd):
    pdenVal = str(bg)
    os.system('OverlapSi.sh '+ chiplabel + ' '+ folder + ' '+ lcf_file +' ' +configFile + ' ' + modelParamsFile + ' ' + pdenType + ' ' + pdenVal + ' ' + scp_dir + ' ' + grid_rows + ' ' + grid_cols + ' ' + runName)
#"""
