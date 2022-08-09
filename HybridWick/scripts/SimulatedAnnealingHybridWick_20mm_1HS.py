import os
import sys
import configparser
import dry_out_F2 as dry_out
import pandas as pd
import random
import math

chiplabel = "20mm_1HS"
lcf = sys.argv[1]
cFile = sys.argv[2]
modelParamsFile = sys.argv[3]
gridSteady = sys.argv[4]
coolants = ["water", "r245fa", "r141b"]
#coolants = ["r245fa"]
a = lcf.split("lcf_files/")[1]
maxPD = int(sys.argv[5])
# scpFile=sys.argv[5]
# logFile=sys.argv[6]
# os.chdir("/projectnb/peaclab-cri-cooling/EDAToolDevelopment/CRI-Cooling-Tool/src/")
#print ('Number of arguments:', len(sys.argv), 'arguments.')
#print ('Argument List:', str(sys.argv))
#opt_coolant = 0
#count = 4096*3
#count = 4096
wick_df = pd.DataFrame()
config = configparser.ConfigParser()

for coolant in coolants:
    gridSteadyFile = gridSteady + "_" + \
        chiplabel + "_" + str(maxPD) + "_" + coolant
    configFile = cFile + "_"+coolant
    config.read(configFile)
    for i in range(0, 10):
        # initialize parameter
        count = 0
        T_target = 65  # target T
        T = 1  # init T
        delta = 0.9  # decay rate
        iterate = 100  # 100 iteration
        t = random.uniform(0.9, 1)
        dp = random.uniform(0.15, 0.2)
        phi = random.uniform(0.4, 0.6)
        ar = random.uniform(0.5, 2)
        sf = random.uniform(0.1, 0.4)
        w = random.uniform(6, 8)
        #w = random.uniform(2,8)
        #t = 1
        #dp = 0.2
        #phi = 0.5
        #ar = 1
        #sf = 0.1
        #w = 6
        while dry_out.hotspot_dry_out(t, dp, phi, ar, sf, w, coolant) < maxPD:
            if count == 100:
                break
            else:
                if coolant == "r141b":
                    #t = random.uniform(0.9,1)
                    #t = 0.25
                    t = random.choice([0.25, 1])
                    #dp = random.uniform(0.15,0.2)
                    #dp = random.unform(0.05,0.1)
                    dp = 0.05
                    #phi = random.uniform(0.4,0.6)
                    phi = 0.2
                    #ar = random.uniform(0.5,2)
                    ar = 2
                    #sf = random.uniform(0.1,0.4)
                    sf = 0.2
                    w = 8
                    #w = random.uniform(6,8)
                    #w = random.uniform(2,8)
                elif coolant == "r245fa":
                    t = 1
                    dp = 0.05
                    phi = 0.2
                    ar = 2
                    sf = 0.2
                    w = 8
                #w = random.uniform(2,8)
                print('dry_out happens')
                count += 1

                ###Make config File#
                ##Call Tool###
                ##Find Max###
        config['HybridWick'] = {"thickness (t)": t, "pore diameter (dp)": dp, "porosity (phi)": phi, "aspect ratio (ar)": ar,
                                "solid fraction (sf)": sf, "width (w)": w, "Tsat": "323.15 K", "coolant": coolant,
                                "grid_temperatures": "273.15 K", "silicon thermalresistivity ((m-k)/w)": 0.0077}
        with open(configFile+"_SA_"+chiplabel+"_"+str(maxPD), 'w') as confFile:
            config.write(confFile)
        os.system("python PACT.py " + lcf + " " + configFile+"_SA_" + chiplabel + "_" +
                  str(maxPD) + " " + modelParamsFile + " --gridSteadyFile " + gridSteadyFile)
        df = pd.read_csv(gridSteadyFile+".layer0", header=None,
                         sep=",", lineterminator="\n")
        df.columns = ["T"]
        y = max(df["T"]) - 273.15
        while T > 0.01 and iterate > 0:
            para = random.sample(
                ('t_new', 'dp_new', 'phi_new', 'ar_new', 'sf_new', 'w_new'), 1)
            # print(para,'\n')
            if para[0] == 't_new':
                t_new = float(t) + random.sample((-1, 1), 1)[0]*0.01*T
                dp_new = dp
                phi_new = phi
                ar_new = ar
                sf_new = sf
                w_new = w

            elif para[0] == 'dp_new':
                dp_new = float(dp) + random.sample((-1, 1), 1)[0]*0.05*T
                t_new = t
                phi_new = phi
                ar_new = ar
                sf_new = sf
                w_new = w

            elif para[0] == 'phi_new':
                phi_new = float(phi) + random.sample((-1, 1), 1)[0]*0.2*T
                dp_new = dp
                t_new = t
                ar_new = ar
                sf_new = sf
                w_new = w

            elif para[0] == 'ar_new':
                ar_new = float(ar) + random.sample((-1, 1), 1)[0]*0.5*T
                dp_new = dp
                phi_new = phi
                t_new = t
                sf_new = sf
                w_new = w

            elif para[0] == 'sf_new':
                sf_new = float(sf) + random.sample((-1, 1), 1)[0]*0.1*T
                dp_new = dp
                phi_new = phi
                ar_new = ar
                t_new = t
                w_new = w

            elif para[0] == 'w_new':
                w_new = float(w) + random.sample((-1, 1), 1)[0]*2*T
                dp_new = dp
                phi_new = phi
                ar_new = ar
                sf_new = sf
                t_new = t

            if (t_new > 1 or t_new < 0.25) or (dp_new < 0.05 or dp_new > 0.2) or (phi_new < 0.2 or phi_new > 0.5) or (ar_new < 0.5 or ar_new > 2) or (sf_new < 0.1 or sf_new > 0.4) or (w_new < 2 or w_new > 8):
                pass

            else:
                # print('pass11111111111111111111111111111111111111111111111111111111')
                # if dry_out.hotspot_dry_out(t_new,dp_new,phi_new,ar_new,sf_new,w_new,coolant)<maxPD:
                #print('dry_out = {}\n'.format(dry_out.hotspot_dry_out(t_new,dp_new,phi_new,ar_new,sf_new,w_new,coolant)))
                # else:
                if dry_out.hotspot_dry_out(t_new, dp_new, phi_new, ar_new, sf_new, w_new, coolant) > maxPD:
                    # print('pass2222222222222222222222222222222222222222222222222222222')

                    config['HybridWick'] = {"thickness (t)": t_new, "pore diameter (dp)": dp_new, "porosity (phi)": phi_new, "aspect ratio (ar)": ar_new,
                                            "solid fraction (sf)": sf_new, "width (w)": w_new, "Tsat": "323.15 K", "coolant": coolant,
                                            "grid_temperatures": "273.15 K", "silicon thermalresistivity ((m-k)/w)": 0.0077}
                    with open(configFile+"_SA_"+chiplabel+"_"+str(maxPD), 'w') as confFile:
                        config.write(confFile)
                    #cmd = "python CRI-Cooling-Tool " + lcf + " " + configFile+"_exh " + modelParamsFile + " --gridSteadyFile " + gridSteadyFile
                    os.system("python PACT.py " + lcf + " " + configFile+"_SA_" + chiplabel + "_" + str(
                        maxPD) + " " + modelParamsFile + " --gridSteadyFile " + gridSteadyFile)
                    # print(os.getcwd())
                    # os.system(cmd)
                    df = pd.read_csv(gridSteadyFile+".layer0",
                                     header=None, sep=",", lineterminator="\n")
                    df.columns = ["T"]
                    y_new = max(df["T"]) - 273.15

                    if y_new <= y:
                        t = t_new
                        dp = dp_new
                        phi = phi_new
                        ar = ar_new
                        sf = sf_new
                        w = w_new
                        y = y_new
                        T = T * delta
                        # print('accept')
                    else:
                        p = (math.exp(-(y_new-y)/(y*T)))
                        if random.uniform(0, 1) < p:
                            t = t_new
                            dp = dp_new
                            phi = phi_new
                            ar = ar_new
                            sf = sf_new
                            w = w_new
                            y = y_new
                            T = T * delta
                            #print('still accept')

            iterate -= 1

        if count < 100 and dry_out.hotspot_dry_out(t, dp, phi, ar, sf, w, coolant) > maxPD:
            wick_df = wick_df.append(pd.DataFrame([[coolant, t, dp, phi, ar, sf, w, y]], columns=[
                                     'coolant', 't', 'dp', 'phi', 'ar', 'sf', 'w', 'Tmax']))

min_wick_df = wick_df[wick_df["Tmax"] == min(wick_df["Tmax"])]
min_wick_df.to_csv("../HybridWick/results/SimulatedAnnealing/" +
                   chiplabel+"_"+str(maxPD)+"_"+a, sep=",")
