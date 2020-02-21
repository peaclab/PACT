import numpy as np
import pandas as pd
#import sys

col =['coolant','thickness (t)','pore diameter (dp)','porosity (phi)','aspect ratio (ar)','solid fraction (sf)','width (w)','correlation'] 
htc_correlation = pd.DataFrame(columns = col)
#water case 1
#HTC = 2093.243*(T-323.15)+128015.32

#water case 2
#HTC = 1514.35*(T-323.15)+71790

#water case 3
#HTC = 2088.83*(T-323.15)+89802

#r245fa case 1
#HTC = -3383.526*(T-323.15)+789876

#r245fa case 2
#HTC = -4215.25*(T-323.15)+706299.68

#r245fa case 3
#HTC = -21236.2079*(T-323.15)+1308858

#r141b case 1
#HTC = -2976.22*(T-323.15)+655915.33

#r141b case 2
#HTC = -2255.928*(T-323.15)+527649.715

#All measurements are in um
htc_correlation=htc_correlation.append(pd.DataFrame([['water','0.45','0.12','0.4','2.5','0.25','4',lambda T: {x:2093.243*(x-323.15)+128015.32 for x in T} ]] ,columns=col))
htc_correlation=htc_correlation.append(pd.DataFrame([['water','0.3','0.1','0.2','1','0.2','5',lambda T: {x:1514.35*(x-323.15)+71790 for x in T} ]] ,columns=col))
htc_correlation=htc_correlation.append(pd.DataFrame([['r245fa','0.45','0.12','0.4','2.5','0.25','4',lambda T: {x:-3383.526*(x-323.15)+789876 for x in T} ]] ,columns=col))
htc_correlation=htc_correlation.append(pd.DataFrame([['r245fa','0.3','0.1','0.2','1','0.2','5',lambda T: {x:-4215.25*(x-323.15)+706299.68 for x in T} ]] ,columns=col))
htc_correlation=htc_correlation.append(pd.DataFrame([['r141b','0.45','0.12','0.4','2.5','0.25','4',lambda T: {x:-2976.22*(x-323.15)+655915.33 for x in T} ]] ,columns=col))
htc_correlation=htc_correlation.append(pd.DataFrame([['r141b','0.3','0.1','0.2','1','0.2','5',lambda T: {x:-2255.928*(x-323.15)+527649.715 for x in T} ]] ,columns=col))
#htc_correlation=htc_correlation.append(pd.DataFrame([['water','3','1','1','1','1','1',lambda T: 30*(T-323.15)+100]],columns=col))

coolant = ''
t = '' #properties['thickness (t)']
dp ='' #properties['pore diameter (dp)']
phi ='' #properties['porosity (phi)']
ar = '' #properties['aspect ratio (ar)']
sf = '' #properties['solid fraction (sf)']
w = '' #properties['width (w)']
prod = '' #width*height
ro = 0.0 
correlation = lambda: None
Rz = np.zeros(1)


def defineGridPropertiesMatrix(label,width, height,thickness,properties):
    global Rz, coolant, t, dp, phi, ar, sf, w, prod, ro, correlation
    gridTemperatures = properties['grid_temperatures']
    #gridTemperatures = np.round(properties['grid_temperatures'],6)
    #gridTemperatures[0][0]=100
    #gridTemperatures[0][1]=200
    #gridLabels = properties['grid_labels']
    ro = float(properties['silicon thermalresistivity ((m-k)/w)'])
    #gridLabels[0][0]="dfsd"
    #grid_rows = properties['grid_rows']
    #grid_cols = properties['grid_rows']
    #num_layers = properties['num_layers']
    coolant= properties['coolant']
    #col =['coolant','thickness (t)','pore diameter (dp)','porosity (phi)','aspect ratio (ar)','solid fraction (sf)','width (w)','correlation'] 
    t = properties['thickness (t)']
    dp = properties['pore diameter (dp)']
    phi = properties['porosity (phi)']
    ar = properties['aspect ratio (ar)']
    sf = properties['solid fraction (sf)']
    w = properties['width (w)']
    prod = width*height
    #htc_correlation = pd.DataFrame(columns = col)
    #htc_correlation=htc_correlation.append(pd.DataFrame([['water','1','1','1','1','1','1',lambda T: {x:10*(x-323.15)+100 for x in T} ]] ,columns=col))
    #htc_correlation=htc_correlation.append(pd.DataFrame([['water','2','1','1','1','1','1',lambda T: 20*(T-323.15)+100]],columns=col))
    #htc_correlation=htc_correlation.append(pd.DataFrame([['water','3','1','1','1','1','1',lambda T: 30*(T-323.15)+100]],columns=col))
    #T = [323.15,200]
    T = list(np.unique(gridTemperatures))
    #print(T)
    #list of a dictionary
    correlation = htc_correlation[(htc_correlation['coolant']==coolant) & (htc_correlation['thickness (t)'] == t) & (htc_correlation['pore diameter (dp)'] == dp) & \
        (htc_correlation['porosity (phi)'] == phi) & (htc_correlation['aspect ratio (ar)'] == ar ) & (htc_correlation['solid fraction (sf)'] == sf) & (htc_correlation['width (w)'] == w ) ]['correlation'].iloc[0]
    T_HTC_dict = correlation(T)
    #T_HTC_dict = htc_correlation[(htc_correlation['coolant']=='water') & (htc_correlation['thickness (t)'] == t) & (htc_correlation['pore diameter (dp)'] == dp) & \
    #    (htc_correlation['porosity (phi)'] == phi) & (htc_correlation['aspect ratio (ar)'] == ar ) & (htc_correlation['solid fraction (sf)'] == sf) & (htc_correlation['width (w)'] == w ) ]['correlation'].iloc[0](T)

    #print("PRACHIIIIIIIIIIIIIII",T_HTC_dict, type(T_HTC_dict))#, type(T_HTC_dict[0]))
    #print("PRACHIIIIIIIIIIIIIII",T_HTC_list)
    Rz_val = {T: 1/(htc*prod) for (T,htc) in T_HTC_dict.items()}
    #print(gridTemperatures.shape, gridLabels.shape)
    Rz = np.zeros(gridTemperatures.shape)
    Capacitance = np.zeros(gridTemperatures.shape)
    I = np.zeros(gridTemperatures.shape)
    for (T,rz) in Rz_val.items():
        print(T)
        #mask = (gridLabels == label) & (gridTemperatures == T)
        mask = (gridTemperatures == T)
        Rz[mask] = rz
    #print(Rz) 
    #mask_xy = (gridLabels == label)
    rx = ro*width/(height*thickness)
    ry = ro*height/(width*thickness)
    Rx = np.full(gridTemperatures.shape,rx)
    Ry = np.full(gridTemperatures.shape,ry)
    #Rx[mask_xy] = rx
    #Ry[mask_xy] = ry
    direction='0'
    out = {"Rx":Rx,"Ry":Ry,"Rz":Rz,"Capacitance":Capacitance,"I":I,"direction":direction}
    #print(Rx,Ry,Rz,I)
    #print (out) 
    #sys.exit(2)
    return out 
    #return {"Rx":Rx}

def TemperatureDependentRz(width, height, thickness, gridTemperatures, properties):
    global Rz, coolant, t, dp, phi, ar, sf, w, prod, ro, correlation
    #T = list(np.unique(gridTemperatures.round(2)))
    T = list(np.unique(gridTemperatures))
    T_HTC_dict = correlation(T)
    #T_HTC_dict = htc_correlation[(htc_correlation['coolant']=='water') & (htc_correlation['p1'] == p1) & (htc_correlation['p2'] == p2) & \
    #    (htc_correlation['p3'] == p3) & (htc_correlation['p4'] == p4 ) & (htc_correlation['p5'] == p5) & (htc_correlation['p6'] == p6 ) ]['correlation'].iloc[0](T)

    Rz_val = {T: 1/(htc*prod) for (T,htc) in T_HTC_dict.items()}
    #print(gridTemperatures.shape, gridLabels.shape)
    #Rz = np.zeros(gridTemperatures.shape)
    Rz.fill(0)
    for (T,rz) in Rz_val.items():
        #mask = (gridLabels == label) & (gridTemperatures == T)
        #mask = (gridTemperatures.round(2) == T)
        mask = (gridTemperatures == T)
        #Rz[mask] = round(rz,2)
        Rz[mask] = rz
    #print(Rz)
    #sys.exit(2)
    return Rz
