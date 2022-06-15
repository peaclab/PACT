import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from joblib import dump, load
#import sys
#import cProfile , pstats, io
#pr = cProfile.Profile()

#import sys

col = ['coolant', 'thickness (t)', 'pore diameter (dp)', 'porosity (phi)',
       'aspect ratio (ar)', 'solid fraction (sf)', 'width (w)', 'correlation']

coolant = ''
t = ''  # properties['thickness (t)']
dp = ''  # properties['pore diameter (dp)']
phi = ''  # properties['porosity (phi)']
ar = ''  # properties['aspect ratio (ar)']
sf = ''  # properties['solid fraction (sf)']
w = ''  # properties['width (w)']
prod = ''  # width*height
ro = 0.0
Rz = np.zeros(1)

# pr.enable()
water_lr = load('../MLModels/water_regression.joblib')
water_scale = load('../MLModels/water_scaler.joblib')
r245fa_lr = load('../MLModels/r245fa_regression.joblib')
r245fa_scale = load('../MLModels/r245fa_scaler.joblib')
r141b_lr = load('../MLModels/r141b_regression.joblib')
r141b_scale = load('../MLModels/r141b_scaler.joblib')
# pr.disable()
#s = io.StringIO()
#sortby = 'cumulative'
#ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
# ps.print_stats()
#print (s.getvalue())


def defineGridPropertiesMatrix(label, width, height, thickness, properties):
    global Rz, coolant, t, dp, phi, ar, sf, w, prod, ro

    gridTemperatures = properties['grid_temperatures']
    #gridTemperatures = np.round(properties['grid_temperatures'],6)
    # gridTemperatures[0][0]=100
    # gridTemperatures[0][1]=200
    #gridLabels = properties['grid_labels']
    ro = float(properties['silicon thermalresistivity ((m-k)/w)'])
    # gridLabels[0][0]="dfsd"
    #grid_rows = properties['grid_rows']
    #grid_cols = properties['grid_rows']
    #num_layers = properties['num_layers']
    coolant = properties['coolant']
    #col =['coolant','thickness (t)','pore diameter (dp)','porosity (phi)','aspect ratio (ar)','solid fraction (sf)','width (w)','correlation']
    t = properties['thickness (t)']
    dp = properties['pore diameter (dp)']
    phi = properties['porosity (phi)']
    ar = properties['aspect ratio (ar)']
    sf = properties['solid fraction (sf)']
    w = properties['width (w)']
    prod = width*height
    T = list(np.unique(gridTemperatures))
    l = len(T)
    coolant_df = pd.DataFrame({'t [um]': [t]*l, 'dp [um]': [dp]*l, 'phi': [phi]*l, 'AR': [
                              ar]*l, 'SF': [sf]*l, 'w [um]': [w]*l, 'T': [float(item)-323.15 for item in T]})
    if coolant == 'water':
        coolant_df = water_scale.transform(coolant_df)
        HTC = water_lr.predict(coolant_df)

    elif coolant == 'r245fa':
        coolant_df = r245fa_scale.transform(coolant_df)
        HTC = r245fa_lr.predict(coolant_df)

    elif coolant == 'r141b':
        coolant_df = r141b_scale.transform(coolant_df)
        HTC = r141b_lr.predict(coolant_df)

    T_HTC_dict = dict(zip(T, HTC))

    Rz_val = {T: 1/(htc*prod) for (T, htc) in T_HTC_dict.items()}
    #print(gridTemperatures.shape, gridLabels.shape)
    Rz = np.zeros(gridTemperatures.shape)
    Capacitance = np.zeros(gridTemperatures.shape)
    I = np.zeros(gridTemperatures.shape)
    for (T, rz) in Rz_val.items():
        # print(T)
        #mask = (gridLabels == label) & (gridTemperatures == T)
        mask = (gridTemperatures == T)
        Rz[mask] = rz
    # print(Rz)
    #mask_xy = (gridLabels == label)
    rx = ro*width/(height*thickness)
    ry = ro*height/(width*thickness)
    Rx = np.full(gridTemperatures.shape, rx)
    Ry = np.full(gridTemperatures.shape, ry)
    #Rx[mask_xy] = rx
    #Ry[mask_xy] = ry
    direction = '0'
    out = {"Rx": Rx, "Ry": Ry, "Rz": Rz,
           "Capacitance": Capacitance, "I": I, "direction": direction}
    # print(Rx,Ry,Rz,I)
    #print (out)
    # sys.exit(2)
    return out
    # return {"Rx":Rx}


def TemperatureDependentRz(width, height, thickness, gridTemperatures, properties):
    global Rz, coolant, t, dp, phi, ar, sf, w, prod, ro, lr, scale
    T = list(np.unique(gridTemperatures))
    l = len(T)
    coolant_df = pd.DataFrame({'t [um]': [t]*l, 'dp [um]': [dp]*l, 'phi': [phi]*l, 'AR': [
                              ar]*l, 'SF': [sf]*l, 'w [um]': [w]*l, 'T': [float(item)-323.15 for item in T]})
    if coolant == 'water':
        coolant_df = water_scale.transform(coolant_df)
        HTC = water_lr.predict(coolant_df)

    elif coolant == 'r245fa':
        coolant_df = r245fa_scale.transform(coolant_df)
        HTC = r245fa_lr.predict(coolant_df)

    elif coolant == 'r141b':
        coolant_df = r141b_scale.transform(coolant_df)
        HTC = r141b_lr.predict(coolant_df)

    T_HTC_dict = dict(zip(T, HTC))

    Rz.fill(0)
    Rz_val = {T: 1/(htc*prod) for (T, htc) in T_HTC_dict.items()}
    #print(gridTemperatures.shape, gridLabels.shape)
    Rz = np.zeros(gridTemperatures.shape)

    for (T, rz) in Rz_val.items():
        mask = (gridTemperatures == T)
        Rz[mask] = rz
    return Rz
