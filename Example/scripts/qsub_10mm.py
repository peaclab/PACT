import os,sys

#grid_rows=['40']
#grid_rows= ['5']
grid_rows= ['40','80','160']
grid_cols =  grid_rows
grids_ll = [x+'x'+y for (x,y) in zip(grid_rows,grid_cols)]
print(grids_ll)
htc_ll = ['1e4', '1e5', '1e6']
#htc_ll = ['1e5']
chiplabel='10mm'
folder = '../Example/'
lcf = folder + 'lcf_files/'+chiplabel+"_lcf"
modelParams = folder+'modelParams_files/modelParams10mm.config'
runName = 'MyToolRun'
grid_folder = folder+'results/'+chiplabel+"/"



for grids in grids_ll:
    log_file = folder + "logs/"+chiplabel+"_"+grids+".log"
    scp_folder="/projectnb/peaclab-cri-cooling/EDAToolDevelopment/Zihao_ToolCopy/steady_temperature/"
    modelParamsFile = modelParams + '_'+grids
    for htc in htc_ll:
        configFile = folder + 'config_files/default_htc_' + htc + '_' + chiplabel + '.config'
        #"""
        ### Non - Uniform Power density ####
        bgpd = [50]
        #hspd = [500,1000,1500,2000]
        hspd = [500]
        pdenType = 'NonUniformPD'
        for bg_idx, bg in enumerate(bgpd):
            for hs_idx, hs in enumerate(hspd):
                pdenVal = str(bg) + '_'+ str(hs)
                lcf_file = lcf + "_" + pdenType + "_" + pdenVal + "Wcm2.csv"
                outfile = "MyToolRun_htc_"+htc+"_"+pdenType + "_"+pdenVal+"Wcm2_"+grids + ".grid.steady"
                grid_file = grid_folder + outfile
                scp_file = folder + outfile
                os.system('10mm.sh '+ lcf_file + ' ' + configFile + ' ' + modelParamsFile + ' ' + grid_file + ' ' + scp_file + ' ' + log_file)
        #"""

        """
        ### Uniform Power density ####
        bgpd = [50,100,150,200] *5 
        #bgpd = [50]
        pdenType = 'UniformPD'
        for bg_idx, bg in enumerate(bgpd):
            pdenVal = str(bg)
            lcf_file = lcf + "_" + pdenType + "_" + pdenVal + "Wcm2.csv"
            outfile = "MyToolRun_htc_"+htc+"_"+pdenType + "_"+pdenVal+"Wcm2_"+grids+".grid.steady"
            grid_file = grid_folder + outfile
            scp_file = scp_folder + outfile
            os.system('10mm.sh '+ lcf_file + ' ' + configFile + ' ' + modelParamsFile + ' ' + grid_file + ' ' + scp_file + ' ' + log_file)
            #os.system('OverlapSi.sh '+ chiplabel + ' '+ folder + ' '+ lcf_file +' ' +configFile + ' ' + modelParamsFile + ' ' + pdenType + ' ' + pdenVal + ' ' + scp_dir + ' ' + grid_rows + ' ' + grid_cols + ' ' + runName)
        """
