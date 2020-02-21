import os

grid_rows='64'
grid_cols='64'
chiplabel='2mm'
lcf_file = "twophase_lcf"
coolant = "water"
#coolant = "r141b"
#coolant = "r134a"

coolant_dir = coolant+"/"
scp_dir="/home/prachis/EDA_Validation/"+chiplabel+"/"+grid_rows+"x"+grid_cols+"/"+coolant_dir
folder = 'Tests_withHotSpot/'
configFile = 'default2Phase.config'
modelParamsFile = 'modelParams2Phase.config'
runName = 'MyToolRunTwophase'
htc = [coolant + "_height"+ h for h in ['30','40','50']]

### Non-uniform ####
#"""
pdenType = 'NonUniformPD'
bgpd = [50] # for water
hspd = [100,200,300]
#hspd = [100]

#bgpd = [20] ###for other two coolants
#hspd = [25,50,75]

for bg_idx, bg in enumerate(bgpd):
    for hs_idx, hs in enumerate(hspd):
        runName = 'MyToolRunTwophase_' + htc[hs_idx]
        pdenVal = str(bg)+'_'+str(hs)
        #os.system('twophase.sh '+ chiplabel + ' '+ folder + ' '+ lcf_file +' ' +configFile + ' ' + modelParamsFile+'_'+htc[hs_idx] + ' ' + pdenType + ' ' + pdenVal + ' ' + scp_dir + ' ' + grid_rows + ' ' + grid_cols + ' ' + runName)
        os.system('twophase.sh '+ chiplabel + ' '+ folder + ' '+ lcf_file +' ' +configFile +'_'+htc[hs_idx] + ' ' + modelParamsFile + ' ' + pdenType + ' ' + pdenVal + ' ' + scp_dir + ' ' + grid_rows + ' ' + grid_cols + ' ' + runName + ' '+coolant)



#"""
### Uniform Power density ####
#bgpd = [40,80,120,160,200]
pdenType = 'UniformPD'
bgpd = 100
pdenVal = str(bgpd)
#bgpd = [40,80]
for hh in htc:
    runName = 'MyToolRunTwophase_' + hh
    os.system('twophase.sh '+ chiplabel + ' '+ folder + ' '+ lcf_file +' ' +configFile +'_'+hh + ' ' + modelParamsFile + ' ' + pdenType + ' ' + pdenVal + ' ' + scp_dir + ' ' + grid_rows + ' ' + grid_cols + ' ' + runName + ' ' + coolant)
    #os.system('Si_only.sh '+ chiplabel + ' '+ folder + ' '+ lcf_file +' ' +configFile + ' ' + modelParamsFile + ' ' + pdenType + ' ' + pdenVal + ' ' + scp_dir + ' ' + grid_rows + ' ' + grid_cols + ' ' + runName)
#"""
