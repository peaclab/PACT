def defineGridProperties(width, height, thickness, properties):
    #print(width, height,thickness,properties)
    ro = float(properties['silicon thermalresistivity ((m-k)/w)'])
    htc = float(properties['htc'])
    #Rx = round(ro*width/(height*thickness),6)
    #Ry = round(ro*height/(width*thickness),6)
    #Rz = round(1/(width*height*htc),6)
    Rx = ro*width/(height*thickness)
    Ry = ro*height/(width*thickness)
    Rz = 1/(width*height*htc)
    Capacitance = 0
    I = 0
    direction = '0'
    out = {"Rx": Rx, "Ry": Ry, "Rz": Rz, "Capacitance": Capacitance,
           "I": I, "direction": direction, "Conv": 0}
    #out = {"R":{"Rx":Rx,"Ry":Ry,"Rz":Rz},"Capacitance":Capacitance,"I":{"I":I,"direction":direction}}
    # return Rx,Ry,Rz,Capacitance,I
    return out
