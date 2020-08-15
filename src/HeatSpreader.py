import numpy as np
# Calcualte thermal resistance and capacitance for extra heat spreader nodes
# Single mode
def defineGridProperties(length, height,thickness,properties,chip_length,chip_width):
    hk_ro = 1/float(properties['heatsink_thermalconductivity (w/(m-k))'])
    hk_sp = float(properties['heatsink_specificheatcapacity (j/m^3k)'])
    con_r = float(properties['convection_r (k/w)'])
    con_c = float(properties['convection_cap (j/k)'])
    heatsink_side = float(properties['heatsink_side (m)'])
    heatsink_thickness = float(properties['heatsink_thickness (m)'])
    heatspreader_side = float(properties['heatspreader_side (m)'])
    heatspreader_thickness = float(properties['heatspreader_thickness (m)'])
    hs_ro = 1/float(properties['heatspreader_thermalconductivity (w/(m-k))'])
    hs_sp = float(properties['heatspreader_specificheatcapacity (j/m^3k)'])
    hk_Rx = hk_ro*length/(height*heatsink_thickness)
    hk_Ry = hk_ro*height/(length*heatsink_thickness)
    hk_Rz = hk_ro*heatsink_thickness/(length*height)
    hs_Rx = hs_ro*length/(height*heatspreader_thickness)
    hs_Ry = hs_ro*height/(length*heatspreader_thickness)
    hs_Rz = hs_ro*heatspreader_thickness/(length*height)
    Conv = 0
    #use this capacitance to validate with COMSOL
    #Capacitance=1*sp*length*height*thickness
    hk_cap=0.33*hk_sp*heatsink_thickness*length*height
    hs_cap=0.33*hs_sp*heatspreader_thickness*length*height
   
    I=0
    direction='z'
    out = {"Rx":hs_Rx,"Ry":hs_Ry,"Rz":hs_Rz,"Capacitance":hs_cap,"I":I,"direction":direction,"Conv":Conv}
    return out
# Matrix mode
def defineGridPropertiesMatrix(length, height,thickness,properties):
    grid_rows = properties['grid_rows']
    grid_cols = properties['grid_cols']
    ro = float(properties['thermalresistivity ((m-k)/w)'])
    sp = float(properties['specificheatcapacity (j/m^3k)'])
    rx = ro*length/(height*thickness)
    ry = ro*height/(length*thickness)
    rz = ro*thickness/(length*height)
    Rx = np.full((grid_rows,grid_cols),rx)
    Ry = np.full((grid_rows,grid_cols),ry)
    Rz = np.full((grid_rows, grid_cols),rz)
    capacitance=0.33*sp*thickness*length*height
    Capacitance  = np.full((grid_rows,grid_cols),capacitance)
    Conv = 0
    print('Zihao matrix cap ********************',capacitance)
    
    I = np.zeros((grid_rows,grid_cols))
    direction='0'
    out = {"Rx":Rx,"Ry":Ry,"Rz":Rz,"Capacitance":Capacitance,"I":I,"direction":direction, "Conv":Conv}
    return out
