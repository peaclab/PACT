import numpy as np
# Calcualte thermal resistance and capacitance, conection coeffcient for liquid cooling grid cell


def defineGridProperties(length, height, thickness, properties):
    ro = float(properties['thermalresistivity ((m-k)/w)'])
    sp = float(properties['specificheatcapacity (j/m^3k)'])
    if thickness/length < 1:
        aspect_ratio = thickness/length
    else:
        aspect_ratio = length/thickness
    Nusselt_number = 8.235 * (1 - 2.0421 * aspect_ratio + 3.0853 * pow(aspect_ratio, 2) - 2.4765 * pow(
        aspect_ratio, 3) + 1.0578 * pow(aspect_ratio, 4) - 0.1861 * pow(aspect_ratio, 5))
    Nusselt_number = round(Nusselt_number, 2)
    hydraulic_diameter = (2 * thickness * length)/(length+thickness)
    htc = (1/ro) * Nusselt_number/hydraulic_diameter
    area = length * thickness
    Conv = sp*float(properties['coolant_velocity (m/s)'])*area

    Rx = 1/(htc*thickness*height)
    Ry = ro*height/(length*thickness)
    Rz = 2/(htc*(length*height))
    print(f"aspect_ratio {aspect_ratio}")
    print(f"Nusselt_number {Nusselt_number}")
    print(f"Hydraulic_diameter {hydraulic_diameter}")
    print(f"htc {htc}")
    print(f"specific heat: {sp}")
    print(f"area {area}")
    print(f"coolant_velocity:{float(properties['coolant_velocity (m/s)'])} ")
    print(f"Conv: {Conv}")
    print(Rx, Rz)
    # use this capacitance to validate with COMSOL
    # Capacitance=1*sp*length*height*thickness
    Capacitance = 0.33*sp*thickness*length*height
    I = 0
    direction = 'z'
    out = {"Rx": Rx, "Ry": Ry, "Rz": Rz, "Capacitance": Capacitance, "I": I, "direction": direction,
           "Conv": Conv, "inlet_T_constant": properties["inlet_temperature (celsius)"]}
    return out
