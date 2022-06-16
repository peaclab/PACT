import os

grid_rows = ['128']
#grid_rows = ['16']
#grid_rows= ['16','32','64']
grid_cols = grid_rows
grids_ll = [x+'x'+y for (x, y) in zip(grid_rows, grid_cols)]
print(grids_ll)
# chiplabel='2mm'
chiplabel = '20mm_1HS'
#coolants = ["water"]
#coolants = ["r141b"]
# coolants = ["r245fa"]
#coolant = "r141b"
coolants = ["r245fa", "water", "r141b"]

folder = '../HybridWick/'
lcf = folder + 'lcf_files/'+chiplabel+"_hybridWick_lcf"
modelParams = folder+'modelParams_files/modelParamsHybridWick.config'
config = folder + 'config_files/defaultHybridWick.config'
Name = 'HybridWick_'+chiplabel
grid_folder = folder+'results/HybridWick/'
scp_folder = "/HybridWick/"

for grids in grids_ll:
    log_file = folder + "logs/"+chiplabel+"_hybridWick_"+grids+".log"
    modelParamsFile = modelParams + '_'+grids
    ### Non-uniform ####
    # """
    pdenType = 'NonUniformPD'
    # hspd = [500]
    hspd = [100, 500, 1500, 2000]
    #hspd = [1000]
    bg = 50
    for coolant in coolants:
        coolant_dir = coolant+"/"
        # scp_dir="/home/prachis/EDA_Validation/"+chiplabel+"/"+grid_rows+"x"+grid_cols+"/"+coolant_dir
        #htc = [coolant + "_case"+ i for i in ["1","2"]]
        htc = [coolant + "_case" + i for i in ["1"]]
        for hs_idx, hs in enumerate(hspd):
            pdenVal = str(bg)+'_'+str(hs)
            lcf_file = lcf + "_"+pdenType + "_" + pdenVal + "Wcm2.csv"
            for hh in htc:
                configFile = config + "_" + hh
                runName = Name+'_' + hh
                outfile = runName + "_" + pdenType + "_"+pdenVal+"Wcm2_"+grids + ".grid.steady"
                grid_file = grid_folder + outfile
                scp_file = scp_folder + outfile
                print('HybridWick.sh ' + lcf_file + ' ' + configFile + ' ' +
                      modelParamsFile + ' ' + grid_file + ' ' + scp_file + ' ' + log_file)
                os.system('HybridWick.sh ' + lcf_file + ' ' + configFile + ' ' +
                          modelParamsFile + ' ' + grid_file + ' ' + scp_file + ' ' + log_file)

    # """
    """
    ### Uniform Power density ####
    #bgpd = [40,80,120,160,200]
    pdenType = 'UniformPD'
    #bgpd = [100,200]*4
    bgpd = [100]
    for coolant in coolants:
        coolant_dir = coolant+"/"
        #scp_dir="/home/prachis/EDA_Validation/"+chiplabel+"/"+grid_rows+"x"+grid_cols+"/"+coolant_dir
        #htc = [coolant + "_case"+ i for i in ["1","2"]]
        htc = [coolant + "_case"+ i for i in ["1", "2"]]
        for bg in bgpd:
            pdenVal = str(bg)
            lcf_file = lcf + "_"+pdenType + "_" + pdenVal + "Wcm2.csv"
            for hh in htc:
                configFile =  config + "_" + hh
                runName = Name+'_' + hh
                outfile = runName + "_" + pdenType + "_"+pdenVal+"Wcm2_"+grids + ".grid.steady"
                grid_file = grid_folder + outfile 
                scp_file = scp_folder + outfile
                os.system('HybridWick.sh ' + lcf_file + ' ' +configFile + ' ' + modelParamsFile + ' ' + grid_file + ' ' + scp_file + ' ' + log_file )
    """
