import numpy as np
#from numpy import *

#""" Orginal:
def defineGridProperties(length, height,thickness,properties):
    #print(length, height,thickness,properties)
    ro = float(properties['thermalresistivity ((m-k)/w)'])
    sp = float(properties['specificheatcapacity (j/m^3k)'])
    #Rx = round(ro*length/(height*thickness),6)
    #Ry = round(ro*height/(length*thickness),6)
    
    #Rz = round(ro*thickness/(length*height),6)
    Rx = ro*length/(height*thickness)
    Ry = ro*height/(length*thickness)
    Rz = ro*thickness/(length*height)
    #Zihao use this capacitance to validate with COMSOL
    #Capacitance=1*sp*length*height*thickness
    Capacitance=0.33*sp*thickness*length*height
    #print('Zihao Single cap ********************',Capacitance)
   
    I=0
    direction='z'
    out = {"Rx":Rx,"Ry":Ry,"Rz":Rz,"Capacitance":Capacitance,"I":I,"direction":direction}
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
    print('Zihao matrix cap ********************',capacitance)
    
    I = np.zeros((grid_rows,grid_cols))
    direction='0'
    out = {"Rx":Rx,"Ry":Ry,"Rz":Rz,"Capacitance":Capacitance,"I":I,"direction":direction}
    return out
