import configparser

config = configparser.ConfigParser()

config['DEFAULT'] ={}
config['DEFAULT']['Label']=''

config['Path'] ={}
config['Path']['Home']='/home/prachis/GitHub/CRI-Cooling-Tool/'
config['Path']['Library']=config['Path']['Home']+'lib/'
config['Path']['Flp']=config['Path']['Home']+'flp_files/'
config['Path']['Ptrace']=config['Path']['Home']+'ptrace_files/'
config['Path']['Config']=config['Path']['Home']+'config_files/'

config['Solver'] = {}
config['Solver']['Name'] = 'SuperLU'

config['Grid'] = {}
config['Grid']['Type'] = 'Uniform'
config['Grid']['Granularity'] = 'Grid'
config['Grid']['Rows'] = '2'
config['Grid']['Cols'] = '2'

config['TIM'] = {}
config['TIM']['Thickness (m)'] = '0.00002'
config['TIM']['Transient'] = 'True'

config['TEC'] = {}
config['TEC']['Library'] = config['Path']['Library']+'TEC.py'
config['TEC']['ModelLayers'] = '3'
config['TEC']['Materials'] = 'Ceramic, Cu, Ceramic'
config['TEC']['PowerOutFile'] =config['Path']['Home']+'output/tec.tecout'
config['TEC']['Transient'] = 'False'

config ['Si'] = {}
config['Si']['Transient']= 'True'

with open('modelParams.config', 'w') as configfile:
    config.write(configfile)
