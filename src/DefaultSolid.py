def defineGridProperties(length, height,thickness,properties):
    #print(length, height,thickness,properties)
    ro = float(properties['thermalresistivity ((m-k)/w)'])
    sp = float(properties['specificheatcapacity (j/m^3k)'])
    Rx = round(ro*length/(height*thickness),6)
    Ry = round(ro*height/(length*thickness),6)
    Rz = round(ro*thickness/(length*height),6)
    Capacitance=1*sp*length*height*thickness
    I=0
    direction='z'
    out = {"Rx":Rx,"Ry":Ry,"Rz":Rz,"Capacitance":Capacitance,"I":I,"direction":direction}
    #out = {"R":{"Rx":Rx,"Ry":Ry,"Rz":Rz},"Capacitance":Capacitance,"I":{"I":I,"direction":direction}}
    #return Rx,Ry,Rz,Capacitance,I
    return out
