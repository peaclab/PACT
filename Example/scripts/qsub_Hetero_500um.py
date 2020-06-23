import os,sys


htc_ll = ['1e4', '1e5', '1e6']
#htc_ll = ['1e5']
hs_loc = ['center','edge','corner','multiple_center','multiple_offcenter']
#hs_loc = ['center','edge','corner']
#hs_loc = ['corner']

#"""
#For interactive jobs, run one 'chiplabel' at a time
for n in range(0,1):
    if n==0:
        chiplabel='10mm_500um_Hetero'
        grid_rows= ['20','40','80','160','320']
        #grid_rows= ['20','40','80','160']
        #grid_rows= ['40']
#"""
    elif n==1:
#"""
        chiplabel='20mm_500um_Hetero'
        grid_rows= ['10']
        #grid_rows= ['40','80','160']
        #grid_rows= ['320']
#"""
    elif n==2:
#"""
        chiplabel='5mm_500um_Hetero'
        grid_rows= ['10','20','40','80','160']
        #grid_rows= ['10','20','40','80']
        #grid_rows= ['160']
#"""

    #hs_loc = ['edge']
    grid_cols =  grid_rows
    grids_ll = [x+'x'+y for (x,y) in zip(grid_rows,grid_cols)]
    print(grids_ll)
    folder = '../Example/'
    lcf = folder + 'lcf_files/'+chiplabel+"_lcf"
    modelParams = folder+'modelParams_files/modelParamsSi_500um.config'
    runName = 'MyToolRun'
    grid_folder = folder+'results/'+chiplabel+"/"


    for grids in grids_ll:
        log_file = folder + "logs/"+chiplabel+"_"+grids+".log"
        scp_folder="/home/prachis/EDA_Validation/Example/"+chiplabel+"/"
        modelParamsFile = modelParams + '_'+grids
        for htc in htc_ll:
            #configFile = folder + 'config_files/default_htc_' + htc + '_' + chiplabel + '.config'
            configFile = folder + 'config_files/default_htc_' + htc + '_Hetero_500um.config'
            #"""
            ### Non - Uniform Power density ####
            #bgpd = [30,50]
            bgpd = [50]
            #hspd = [500,1000,1500,2000]
            #hspd = [1500,2000]
            hspd = [1500]
            #bgpd = [30]
            #hspd = [500]
            pdenType = 'NonUniformPD'
            for bg_idx, bg in enumerate(bgpd):
                for hs_idx, hs in enumerate(hspd):
                    for loc in hs_loc:
                        pdenVal = loc+str(bg) + '_'+ str(hs)
                        lcf_file = lcf + "_" + pdenType + "_" + pdenVal + "Wcm2.csv"
                        outfile = "MyToolRun_htc_"+htc+"_"+pdenType + "_"+pdenVal+"Wcm2_"+grids + ".grid.steady"
                        grid_file = grid_folder + outfile
                        scp_file = scp_folder + outfile
                        os.system('Si_500um.sh '+ lcf_file + ' ' + configFile + ' ' + modelParamsFile + ' ' + grid_file + ' ' + scp_file + ' ' + log_file)
            #"""

            """
            ### Uniform Power density ####
            bgpd = [40,80,120,160,200]
            #bgpd = [40]
            pdenType = 'UniformPD'
            for bg_idx, bg in enumerate(bgpd):
                pdenVal = str(bg)
                lcf_file = lcf + "_" + pdenType + "_" + pdenVal + "Wcm2.csv"
                outfile = "MyToolRun_htc_"+htc+"_"+pdenType + "_"+pdenVal+"Wcm2_"+grids+".grid.steady"
                grid_file = grid_folder + outfile
                scp_file = scp_folder + outfile
                os.system('Si_500um.sh '+ lcf_file + ' ' + configFile + ' ' + modelParamsFile + ' ' + grid_file + ' ' + scp_file + ' ' + log_file)
                #os.system('OverlapSi.sh '+ chiplabel + ' '+ folder + ' '+ lcf_file +' ' +configFile + ' ' + modelParamsFile + ' ' + pdenType + ' ' + pdenVal + ' ' + scp_dir + ' ' + grid_rows + ' ' + grid_cols + ' ' + runName)
            """
