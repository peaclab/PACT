import numpy as np
#from numpy import *

#""" Orginal:
def defineGridProperties(length, height,thickness,properties,chip_length,chip_width):
    #print(length, height,thickness,properties)
    hk_ro = 1/float(properties['heatsink_thermalconductivity (w/(m-k))'])
    hk_sp = float(properties['heatsink_specificheatcapacity (j/m^3k)'])
    #Rx = round(ro*length/(height*thickness),6)
    #Ry = round(ro*height/(length*thickness),6)
    con_r = float(properties['convection_r (k/w)'])
    con_c = float(properties['convection_cap (j/k)'])
    heatsink_side = float(properties['heatsink_side (m)'])
    heatsink_thickness = float(properties['heatsink_thickness (m)'])
    heatspreader_side = float(properties['heatspreader_side (m)'])
    heatspreader_thickness = float(properties['heatspreader_thickness (m)'])
    hs_ro = 1/float(properties['heatspreader_thermalconductivity (w/(m-k))'])
    hs_sp = float(properties['heatspreader_specificheatcapacity (j/m^3k)'])
    #Rz = round(ro*thickness/(length*height),6)
    hk_Rx = hk_ro*length/(height*thickness)
    hk_Ry = hk_ro*height/(length*thickness)
    hk_Rz = hk_ro*thickness/(length*height)
    hs_Rx = hs_ro*length/(height*thickness)
    hs_Ry = hs_ro*height/(length*thickness)
    hs_Rz = hs_ro*thickness/(length*height)
    Conv = 0
    #Zihao use this capacitance to validate with COMSOL
    #Capacitance=1*sp*length*height*thickness
    hk_cap=0.33*hk_sp*thickness*length*height
    hs_cap=0.33*hs_sp*thickness*length*height
    #print('Zihao Single cap ********************',Capacitance)
   
    I=0
    direction='z'
    out = {"Rx":hs_Rx,"Ry":hs_Ry,"Rz":hs_Rz,"Capacitance":hs_cap,"I":I,"direction":direction,"Conv":Conv}
    #out = {"R":{"Rx":Rx,"Ry":Ry,"Rz":Rz},"Capacitance":Capacitance,"I":{"I":I,"direction":direction}}  
    #return Rx,Ry,Rz,Capacitance,I
    return out
"""
def defineGridProperties(length, height,thickness,properties,out):
    #print(length, height,thickness,properties)
    ro = float(properties['thermalresistivity ((m-k)/w)'])
    sp = float(properties['specificheatcapacity (j/m^3k)'])
    #Rx = round(ro*length/(height*thickness),6)
    #Ry = round(ro*height/(length*thickness),6)
    #Rz = round(ro*thickness/(length*height),6)
    #Rx = double(ro*length/(height*thickness))
    #Ry = double(ro*height/(length*thickness))
    #Rz = double(ro*thickness/(length*height))
    out['Rx'] = ro*length/(height*thickness)
    out['Ry'] = ro*height/(length*thickness)
    out['Rz'] = ro*thickness/(length*height)
    #Capacitance=1*sp*length*height*thickness
    out['C']=0
    out['I']=0
    out['direction']=0
    #out = {"R":{"Rx":Rx,"Ry":Ry,"Rz":Rz},"Capacitance":Capacitance,"I":{"I":I,"direction":direction}}
    #return Rx,Ry,Rz,Capacitance,I
    #return out
"""

def defineGridPropertiesMatrix(length, height,thickness,properties):
    grid_rows = properties['grid_rows']
    grid_cols = properties['grid_cols']
    ro = float(properties['thermalresistivity ((m-k)/w)'])
    sp = float(properties['specificheatcapacity (j/m^3k)'])
    rx = ro*length/(height*thickness)
    ry = ro*height/(length*thickness)
    rz = ro*thickness/(length*height)
    #cap=1*sp*length*height*thickness
    Rx = np.full((grid_rows,grid_cols),rx)
    Ry = np.full((grid_rows,grid_cols),ry)
    Rz = np.full((grid_rows, grid_cols),rz)
    #Capacitance = np.full((grid_rows, grid_cols),cap)
    #Capacitance = np.zeros((grid_rows,grid_cols))
    capacitance=0.33*sp*thickness*length*height
    Capacitance  = np.full((grid_rows,grid_cols),capacitance)
    Conv = 0
    print('Zihao matrix cap ********************',capacitance)
    
    I = np.zeros((grid_rows,grid_cols))
    direction='0'
    out = {"Rx":Rx,"Ry":Ry,"Rz":Rz,"Capacitance":Capacitance,"I":I,"direction":direction, "Conv":Conv}
    return out
