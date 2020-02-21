import configparser

config = configparser.ConfigParser()
config['DEFAULT'] = {'Thickness (m)': '0.0001', 'label': ''}


config['Si'] = {}
config['Si']['ThermalResistivity ((m-K)/W)'] = '0.1'
config['Si']['SpecificHeatCapacity (J/m^3K)'] = '1750000'

config['TIM'] = {}
config['TIM']['ThermalResistivity ((m-K)/W)'] = '0.25'
config['TIM']['SpecificHeatCapacity (J/m^3K)'] = '1750000'
config['TIM']['Thickness (m)'] = '0.00002'

config['Init'] = {}
config['Init']['Ambient'] = '323 K'
config['Init']['Temperature'] = '350 K'

config['TEC'] = {}
config['TEC']['P-N'] = '49'
config['TEC']['SeebeckCoefficient'] = '187e-6'
config['TEC']['ThermalContactResistance (m2K/W)'] = '9e-6'
config['TEC']['ElectricalContactResistance (Ohm.m^2)'] = '1.1e-10'
config['TEC']['ElectricalResistivity (Ohm.m)'] = '1.64e-5'
config['TEC']['Current (A)'] = '0'

with open('default.config', 'w') as configfile:
    config.write(configfile)

config.read('default1.config')
config.sections()

print (config['Si']['Thickness (m)'])
print (config['TIM']['Thickness (m)'])
