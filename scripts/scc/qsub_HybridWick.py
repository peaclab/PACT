import os

grid_rows='10'
grid_cols='10'
chiplabel='2mm'
lcf_file = "hybridWick_lcf"
coolants = ["water"]
#coolant = "r141b"
#coolant = "r245fa"
#coolants = ["r245fa","water","r141b"]

folder = 'Tests_withHotSpot/'
configFile = 'defaultHybridWick.config'
modelParamsFile = 'modelParamsHybridWick.config'
Name = 'MyToolRunHybridWick'
#htc = [coolant + "_case"+ i for i in ["2"]]
#print(htc)

### Non-uniform ####
#"""
pdenType = 'NonUniformPD'
bgpd = [50] # for water
#hspd = [100,500,1000]
hspd = [1000]
#hspd = [100]

#bgpd = [20] ###for other two coolants
#hspd = [25,50,75]
bg = 50
for coolant in coolants:
    coolant_dir = coolant+"/"
    scp_dir="/home/prachis/EDA_Validation/"+chiplabel+"/"+grid_rows+"x"+grid_cols+"/"+coolant_dir
    htc = [coolant + "_case"+ i for i in ["1","2"]]
    for hs_idx, hs in enumerate(hspd):
        for hh in htc:
            runName = Name+'_' + hh
            pdenVal = str(bg)+'_'+str(hs)
            #os.system('twophase.sh '+ chiplabel + ' '+ folder + ' '+ lcf_file +' ' +configFile + ' ' + modelParamsFile+'_'+htc[hs_idx] + ' ' + pdenType + ' ' + pdenVal + ' ' + scp_dir + ' ' + grid_rows + ' ' + grid_cols + ' ' + runName)
            os.system('HybridWick.sh '+ chiplabel + ' '+ folder + ' '+ lcf_file +' ' +configFile +'_'+hh + ' ' + modelParamsFile + ' ' + pdenType + ' ' + pdenVal + ' ' + scp_dir + ' ' + grid_rows + ' ' + grid_cols + ' ' + runName + ' '+coolant)

"""

### Uniform Power density ####
#bgpd = [40,80,120,160,200]
pdenType = 'UniformPD'
bgpd = [100,200]
#bgpd = [100]
for coolant in coolants:
    coolant_dir = coolant+"/"
    scp_dir="/home/prachis/EDA_Validation/"+chiplabel+"/"+grid_rows+"x"+grid_cols+"/"+coolant_dir
    htc = [coolant + "_case"+ i for i in ["1","2"]]
    for bg in bgpd:
        pdenVal = str(bg)
        for hh in htc:
            runName = Name+'_' + hh
            os.system('HybridWick.sh '+ chiplabel + ' '+ folder + ' '+ lcf_file +' ' +configFile +'_'+hh + ' ' + modelParamsFile + ' ' + pdenType + ' ' + pdenVal + ' ' + scp_dir + ' ' + grid_rows + ' ' + grid_cols + ' ' + runName + ' ' + coolant)
    #os.system('Si_only.sh '+ chiplabel + ' '+ folder + ' '+ lcf_file +' ' +configFile + ' ' + modelParamsFile + ' ' + pdenType + ' ' + pdenVal + ' ' + scp_dir + ' ' + grid_rows + ' ' + grid_cols + ' ' + runName)
"""
