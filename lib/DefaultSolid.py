def defineGridProperties(width, height,thickness,occupancy,properties):
    print(length, width, height,occupancy,properties)
    ro = properties['thermalresistivity ((m-k)/w)']
    sp = properties['specificheatcapacity (j/m^3k)']
    Rx = round(occupancy*ro*width/(height*thickness),6)
    Ry = round(occupancy*ro*height/(width*thickness),6)
    Rz = round(occupancy*ro*thickness/(width*thickness),6)
    Capacitance=1*sp*width*height*thickness*occupancy
    I=None
    return Rx,Ry,Rz,Capacitance,I
