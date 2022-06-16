import os

grid_rows = ['16', '32', '64', '128']
#grid_rows= ['128']
grid_cols = grid_rows
grids_ll = [x+'x'+y for (x, y) in zip(grid_rows, grid_cols)]
print(grids_ll)
coolants = ["water"]
#coolants = ["r134a","water","r141b"]

folder = '../MicroWick/'
chiplabel = "2mm"
lcf = folder + 'lcf_files/'+chiplabel+"_TwoPhaseVC_lcf"
modelParams = folder+'modelParams_files/modelParamsTwoPhaseVC.config'
config = folder + 'config_files/defaultTwoPhaseVC.config'
Name = 'TwoPhaseVC_'+chiplabel
grid_folder = folder+'results/'
scp_folder = "/TwoPhaseVC/"

#configFile = 'default2Phase.config'
#modelParamsFile = 'modelParams2Phase.config'

for grids in grids_ll:
    log_file = folder + "logs/"+chiplabel+"_MicroWick_"+grids+".log"
    modelParamsFile = modelParams + '_'+grids
    for coolant in coolants:
        htc_ll = [coolant + "_height" + h for h in ['30', '40', '50']]
        #htc_ll = [coolant + "_height"+ h for h in ['30']]
        for htc in htc_ll:
            ### Non-uniform ####
            # """
            configFile = config + "_" + htc
            pdenType = 'NonUniformPD'
            bgpd = [50]  # for water
            hspd = [100, 200, 300]

            # bgpd = [20] ###for other two coolants
            #hspd = [25,50,75]

            for bg_idx, bg in enumerate(bgpd):
                for hs_idx, hs in enumerate(hspd):
                    runName = Name+'_' + htc
                    pdenVal = str(bg)+'_'+str(hs)
                    lcf_file = lcf + "_"+pdenType + "_" + pdenVal + "Wcm2.csv"
                    outfile = runName + "_" + pdenType + "_"+pdenVal+"Wcm2_"+grids + ".grid.steady"
                    grid_file = grid_folder + outfile
                    scp_file = scp_folder + outfile
                    os.system('MicroWick.sh ' + lcf_file + ' ' + configFile + ' ' +
                              modelParamsFile + ' ' + grid_file + ' ' + scp_file + ' ' + log_file)
                    #os.system('twophase.sh '+ chiplabel + ' '+ folder + ' '+ lcf_file +' ' +configFile +'_'+htc[hs_idx] + ' ' + modelParamsFile + ' ' + pdenType + ' ' + pdenVal + ' ' + scp_dir + ' ' + grid_rows + ' ' + grid_cols + ' ' + runName + ' '+coolant)

            """
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
            """
