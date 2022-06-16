import numpy as np

# Calculate thermal resistance


def getr(conductivity, thickness, area):
    return thickness/(conductivity*area)
# Calculate thermal capacitance


def getcap(sp_heat, thickness, area):
    return 0.33*sp_heat*thickness*area
# Calculate thermal resistance and capacitance for Heat Spreader and Heat Sink extra nodes
# Single mode


def defineGridProperties(length, height, thickness, properties, chip_length, chip_height):
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
    hk_Rz = hk_ro*heatsink_thickness / \
        (length*height)+con_r*(heatsink_side*heatsink_side)/(length*height)
    hs_Rx = hs_ro*length/(height*heatspreader_thickness)
    hs_Ry = hs_ro*height/(length*heatspreader_thickness)
    hs_Rz = hs_ro*heatspreader_thickness/(length*height)
    Conv = 0
    # use this capacitance to validate with COMSOL
    # Capacitance=1*sp*length*height*thickness
    hk_cap = 0.33*hk_sp*heatsink_thickness*length*height
    hs_cap = 0.33*hs_sp*heatspreader_thickness*length*height
    # Extra thermal resistors
    r_sp1_x = getr(1/hs_ro, (heatspreader_side-chip_length)/4.0,
                   (heatspreader_side+3*chip_height)/4.0*heatspreader_thickness)
    r_sp1_y = getr(1/hs_ro, (heatspreader_side-chip_height)/4.0,
                   (heatspreader_side+3*chip_length)/4.0*heatspreader_thickness)
    r_hs1_x = getr(1/hk_ro, (heatspreader_side-chip_length)/4.0,
                   (heatspreader_side+3*chip_height)/4.0*heatsink_thickness)
    r_hs1_y = getr(1/hk_ro, (heatspreader_side-chip_height)/4.0,
                   (heatspreader_side+3*chip_length)/4.0*heatsink_thickness)
    r_hs2_x = getr(1/hk_ro, (heatspreader_side-chip_length)/4.0,
                   (3*heatspreader_side+chip_height)/4.0*heatsink_thickness)
    r_hs2_y = getr(1/hk_ro, (heatspreader_side-chip_height)/4.0,
                   (3*heatspreader_side+chip_length)/4.0*heatsink_thickness)
    r_hs = getr(1/hk_ro, (heatsink_side-heatspreader_side)/4.0,
                (heatsink_side+3*heatspreader_side)/4.0*heatsink_thickness)
    r_sp_per_x = getr(1/hs_ro, heatspreader_thickness,
                      (heatspreader_side+chip_height)*(heatspreader_side-chip_length)/4.0)
    r_sp_per_y = getr(1/hs_ro, heatspreader_thickness,
                      (heatspreader_side+chip_length)*(heatspreader_side-chip_height)/4.0)
    r_hs_c_per_x = getr(1/hk_ro, heatsink_thickness, (heatspreader_side +
                        chip_height)*(heatspreader_side-chip_length)/4.0)
    r_hs_c_per_y = getr(1/hk_ro, heatsink_thickness, (heatspreader_side +
                        chip_length)*(heatspreader_side-chip_height)/4.0)
    r_hs_per = getr(1/hk_ro, heatsink_thickness, (heatsink_side *
                    heatsink_side-heatspreader_side*heatspreader_side)/4.0)
    r_amb_c_per_x = con_r*(heatsink_side*heatsink_side) / \
        ((heatspreader_side+chip_height)*(heatspreader_side-chip_length)/4.0)
    r_amb_c_per_y = con_r*(heatsink_side*heatsink_side) / \
        ((heatspreader_side+chip_length)*(heatspreader_side-chip_height)/4.0)
    r_amb_per = con_r*(heatsink_side*heatsink_side)/((heatsink_side *
                                                      heatsink_side-heatspreader_side*heatspreader_side)/4.0)
    # Extra thermal capacitors
    c_sp_per_x = getcap(hs_sp, heatspreader_thickness,
                        (heatspreader_side+chip_height)*(heatspreader_side-chip_length)/4.0)
    c_sp_per_y = getcap(hs_sp, heatspreader_thickness,
                        (heatspreader_side+chip_length)*(heatspreader_side-chip_height)/4.0)
    c_hs_c_per_x = getcap(hk_sp, heatsink_thickness, (heatspreader_side +
                          chip_height)*(heatspreader_side-chip_length)/4.0)
    c_hs_c_per_y = getcap(hk_sp, heatsink_thickness, (heatspreader_side +
                          chip_length)*(heatspreader_side-chip_height)/4.0)
    c_hs_per = getcap(hk_sp, heatsink_thickness, (heatsink_side *
                      heatsink_side-heatspreader_side*heatspreader_side)/4.0)
    c_amb_c_per_x = 0.33*con_c/(heatsink_side*heatsink_side)*(
        (heatspreader_side+chip_height)*(heatspreader_side-chip_length)/4.0)
    c_amb_c_per_y = 0.33*con_c/(heatsink_side*heatsink_side)*(
        (heatspreader_side+chip_length)*(heatspreader_side-chip_height)/4.0)
    c_amb_per = 0.33*con_c/(heatsink_side*heatsink_side)*(
        (heatsink_side*heatsink_side-heatspreader_side*heatspreader_side)/4.0)

    I = 0
    direction = 'z'
    out = {"Rx": hk_Rx, "Ry": hk_Ry, "Rz": hk_Rz, "Capacitance": hk_cap, "I": I, "direction": direction, "Conv": Conv, "r_sp1_x_constant": r_sp1_x, "r_sp1_y_constant": r_sp1_y, "r_hs1_x_constant": r_hs1_x, "r_hs1_y_constant": r_hs1_y, "r_hs2_x_constant": r_hs2_x, "r_hs2_y_constant": r_hs2_y, "r_hs_constant": r_hs, "r_sp_per_x_constant": r_sp_per_x, "r_sp_per_y_constant": r_sp_per_y, "r_hs_c_per_x_constant": r_hs_c_per_x, "r_hs_c_per_y_constant": r_hs_c_per_y,
           "r_hs_per_constant": r_hs_per, "r_amb_c_per_x_constant": r_amb_c_per_x, "r_amb_c_per_y_constant": r_amb_c_per_y, "r_amb_per_constant": r_amb_per, "c_sp_per_x_constant": c_sp_per_x, "c_sp_per_y_constant": c_sp_per_y, "c_hs_c_per_x_constant": c_hs_c_per_x, "c_hs_c_per_y_constant": c_hs_c_per_y, "c_hs_per_constant": c_hs_per, "c_amb_c_per_x_constant": c_amb_c_per_x, "c_amb_c_per_y_constant": c_amb_c_per_y, "c_amb_per_constant": c_amb_per}
    return out
# Matrix mode


def defineGridPropertiesMatrix(length, height, thickness, properties):
    grid_rows = properties['grid_rows']
    grid_cols = properties['grid_cols']
    ro = float(properties['thermalresistivity ((m-k)/w)'])
    sp = float(properties['specificheatcapacity (j/m^3k)'])
    rx = ro*length/(height*thickness)
    ry = ro*height/(length*thickness)
    rz = ro*thickness/(length*height)
    Rx = np.full((grid_rows, grid_cols), rx)
    Ry = np.full((grid_rows, grid_cols), ry)
    Rz = np.full((grid_rows, grid_cols), rz)
    capacitance = 0.33*sp*thickness*length*height
    Capacitance = np.full((grid_rows, grid_cols), capacitance)
    Conv = 0
    print('Zihao matrix cap ********************', capacitance)

    I = np.zeros((grid_rows, grid_cols))
    direction = '0'
    out = {"Rx": Rx, "Ry": Ry, "Rz": Rz, "Capacitance": Capacitance,
           "I": I, "direction": direction, "Conv": Conv}
    return out
