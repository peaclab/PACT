import os,sys

#grid_rows=['40']
#grid_rows= ['5']
grid_rows= ['256']
grid_cols =  grid_rows
grids_ll = [x+'x'+y for (x,y) in zip(grid_rows,grid_cols)]
print(grids_ll)
htc_ll = ['1e5']
#htc_ll = ['1e5']
chiplabel='sparc'
folder = '../OpenRoad/'
lcf = folder + 'lcf_files/'+chiplabel
modelParams = folder+'modelParams_files/modelParamssparc.config'
runName = 'MyToolRun'
grid_folder = folder+'results/'+chiplabel+"/"



for grids in grids_ll:
    log_file = folder + "logs/"+chiplabel+"_"+grids+".log"
    scp_folder="/projectnb/peaclab-cri-cooling/EDAToolDevelopment/Zihao_ToolCopy/steady_temperature/"
    modelParamsFile = modelParams + '_'+grids
    for htc in htc_ll:
        configFile = folder+'config_files/' + chiplabel +'_htc_'+htc+'.config'
        #configFile = folder+'config_files/default_htc_'+htc+'_'+'10mm'+'.config'
        utilization = ['85','90','95']
        for util in utilization:
            lcf_file = lcf+util+'_lcf.csv'	
            outfile = chiplabel+util+"_"+grids+'.grid.steady'
            grid_file = grid_folder+outfile
            scp_file = folder+outfile
            os.system('sparc.sh '+ lcf_file + ' ' + configFile + ' ' + modelParamsFile + ' ' + grid_file + ' ' + scp_file + ' ' + log_file)

