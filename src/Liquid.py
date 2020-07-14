import numpy as np
#from numpy import *

#""" Orginal:
def defineGridProperties(length, height,thickness,properties):
    ro = float(properties['thermalresistivity ((m-k)/w)'])
    sp = float(properties['specificheatcapacity (j/m^3k)'])
    
    Rx = ro*length/(height*thickness)
    Ry = ro*height/(length*thickness)
    Rz = ro*thickness/(length*height)
    #Zihao use this capacitance to validate with COMSOL
    #Capacitance=1*sp*length*height*thickness
    Capacitance=0.33*sp*thickness*length*height
    #dummy conv value, copy from hotspot
    Conv = 0.001045 
    #Prachi: Zihao, you shold do something like this (see below)
    # Conv = Write the formula using length, height,thickness,properties
    I=0
    direction='z'
    #Zihao: Prachi, please pass conv and inlet temperature, also the liquid grid cell label to SPICE engine, thx
    #Prachi: I am sending a constant value called 'inlet_T_constant', a matrix for 'Conv', and a matrix for 'g2bmap'. the matrices should be read the same way as Rx, Ry, or Rz
    out = {"Rx":Rx,"Ry":Ry,"Rz":Rz,"Capacitance":Capacitance,"I":I,"direction":direction,"Conv":Conv,"inlet_T_constant":properties["inlet_temperature (celsius)"]}
    return out

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
"""
