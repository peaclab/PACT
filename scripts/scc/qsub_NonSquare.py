import os

grid_rows='40'
grid_cols='16'
chiplabel='2x5mm'
lcf_file = chiplabel+"_lcf"
scp_dir="/home/prachis/EDA_Validation/"
folder = 'Tests_withHotSpot/'
configFile = 'defaultNonSquare.config'
modelParamsFile = 'modelParamsNonSquare.config'
runName = 'MyToolRun'

### Non-uniform ####
#"""
pdenType = 'NonUniformPD'
hs_loc = ['center','corner','edge','multiple']
#hs_loc = ['center']
bgpd = [50]
hspd = [500,1000,1500,2000]
for bg_idx, bg in enumerate(bgpd):
    for hs_idx, hs in enumerate(hspd):
        for loc in hs_loc:
            pdenVal = loc+str(bg)+'_'+str(hs)
            os.system('NonSquare.sh '+ chiplabel + ' '+ folder + ' '+ lcf_file +' ' +configFile + ' ' + modelParamsFile + ' ' + pdenType + ' ' + pdenVal + ' ' + scp_dir + ' ' + grid_rows + ' ' + grid_cols + ' ' + runName)



#"""
### Uniform Power density ####
#bgpd = [40,80,120,160,200]
bgpd = [50,100,150,200]
pdenType = 'UniformPD'
for bg_idx, bg in enumerate(bgpd):
    pdenVal = str(bg)
    os.system('NonSquare.sh '+ chiplabel + ' '+ folder + ' '+ lcf_file +' ' +configFile + ' ' + modelParamsFile + ' ' + pdenType + ' ' + pdenVal + ' ' + scp_dir + ' ' + grid_rows + ' ' + grid_cols + ' ' + runName)
#"""
