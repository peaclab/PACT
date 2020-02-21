import HybridWick_LookupTable as HybridWick
#import HybridWick as HybridWick
def getTemperatureDependentProperties(grid_length,grid_width,thickness,grid_temperature_old,hybrid_wick_properties):
    Rz = HybridWick.TemperatureDependentRz(grid_length,grid_width,thickness,grid_temperature_old,hybrid_wick_properties)
    out = {"Rz":{1:Rz}, "update":{1:"Rz"}}
    return out
    
