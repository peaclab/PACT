import sys, argparse,  os
import configparser
from configparser import NoSectionError, NoOptionError
import pandas as pd
import numpy as np
#from ChipStack import *
from ChipStack import ChipStack
#from Layer import Layer
from GridManager import GridManager
#from Model import *
from SuperLUSolver import SuperLUSolver
from SPICESolver_steady import SPICE_steadySolver
from SPICESolver_transient import SPICE_transientSolver
#from HeatMap import *
#import TemperatureDependent as LibTemperatureDependent 
#import time
#import cProfile , pstats, io
#import SimulatedAnnealing as SA
#import ExhaustiveSearch as ES


#import DefaultSolid as LibSi

def gridTemperatureToFile(arr, layer_num):
    arr_flat = np.round(arr.flatten(),6)
    L_df = pd.DataFrame(arr_flat)
    L_df.to_csv(gridSteadyFile+".layer"+str(layer_num),header=False)

def gridTemp2File(arr):
    global counter
    np.savetxt(gridSteadyFile+".layer"+str(counter), arr, delimiter="\n",fmt="%.2f")
    counter += 1

def display_df_dict():
    print ('------------ Config File Data stored as dictionary (Showing \'Si\' in default config file) ----------------')
    print (config.sections())
    print (config._sections['Si'])
    print ('\n\n------------ ModelParams Data also stored as dictionary (Showing \'Grid\' in the modelParams File ----------------')
    print (modelParams._sections['Grid'])
    print ('\n\n------------ LCF Data stored as a panda frame ----------------')
    print (lcf_df)
    print ('\n\n------------ INIT Temperature is of double datatype ----------------')
    print (initTemp)
    print ('-------------------------------------------------------------\n\n')

def display_args():
    print ('------------ Printing command line arguments ----------------')
    print ('lcfFile:',lcfFile)
    print ('configFile:',configFile)
    print ('modelParamsFile:',modelParamsFile)
    print ('initFile:',initFile)
    print ('steadyFile:',steadyFile)
    print ('gridSteadyFile:',gridSteadyFile)
    print ('-------------------------------------------------------------\n\n')
#print ('ARGV      :', sys.argv[1:])

###################!!! Default Paths to the LCF, ModelParams, ad config files !!!#########
#home_path = '/home/prachis/GitHub/CRI-Cooling-Tool/' # <- Edit this only based on tool's home directory
"""
home_path = './../' #One directory up
lcf_path = home_path+'lcf_files/'
lib_path = home_path+'lib/'
config_path = home_path+'config_files/'
modelParams_path = home_path+'modelParams_files/'
init_path = home_path+'init_files/'
steady_path = home_path+'steady_files/'
ptrace_path = home_path+'ptrace_files/'
results_path = home_path+'results/'
heatMaps_path = home_path+'results/heat_maps/'
"""
###################!!! Parser Starts !!!#######################

######! Command-Line Arguments Description !######
#pr = cProfile.Profile()
parser = argparse.ArgumentParser(prog='PACT',)
parser.add_argument('lcfFile',action='store')
parser.add_argument('configFile', action='store')
parser.add_argument('modelParamsFile', action='store')
parser.add_argument('--init', action='store',dest='initFile')
parser.add_argument('--steady', action='store',dest='steadyFile')
parser.add_argument('--gridSteadyFile', action='store',dest='gridSteadyFile')
### Display Arguments  ###
#print(parser.parse_args())

### Create absolute file paths ###
#lcfFile = lcf_path + parser.parse_args().lcfFile
#configFile = config_path + parser.parse_args().configFile
#modelParamsFile = modelParams_path + parser.parse_args().modelParamsFile
#gridSteadyFile = results_path + parser.parse_args().gridSteadyFile
parser_args =parser.parse_args() 
lcfFile = parser_args.lcfFile
defaultConfigFile = parser_args.configFile
modelParamsFile = parser_args.modelParamsFile
gridSteadyFile = parser_args.gridSteadyFile
#print(gridSteadyFile)
#heatMapFile = heatMaps_path + parser.parse_args().gridSteadyFile.split('.csv')[0]+'.pdf'

if (parser_args.initFile is not None):
    #initFile = init_path + parser.parse_args().initFile
    initFile = parser.parse_args().initFile
else:
    initFile = None
if (parser_args.steadyFile is not None):
    steadyFile = parser_args.steadyFile
else:
    steadyFile = None

### Display Arguments  ###
#display_args()
#sys.exit(2)

######! Read Layer File !######
thickness_layers={}
try:
    lcf_df = pd.read_csv(lcfFile, lineterminator="\n")
    if(lcf_df['Thickness (m)'].isnull().values.any()):
        print('Error:','Thickness (m) must be specified for each layer')
        sys.exit(2)
    thickness_layers=lcf_df.set_index("Layer").to_dict()["Thickness (m)"]
    if(lcf_df['FloorplanFile'].isnull().values.any()):
        print('Error:','Floorplan File must be specified for each layer')
        sys.exit(2)
except FileNotFoundError:
    print('Error:','Layer File does not exist:',lcfFile)
    sys.exit(2)

#print(thickness_layers)
######! Read Default config file !######
### Default read format: ordered dictionary ###
defaultConfig = configparser.ConfigParser()
try:
    defaultConfig.read(defaultConfigFile)
except FileNotFoundError:
    print('Error:','Config File does not exist:',configFile)
    sys.exit(2)
#####! Get noPackage properties !######
#NoPackage_config = config['NoPackage']
#print(float(NoPackage_config.get('htc')))
#print(float(NoPackage_config.get('r_convec (K/W)')))

######! Read ModelParams file !######
modelParams = configparser.ConfigParser()
try:
    modelParams.read(modelParamsFile)
except FileNotFoundError:
    print('Error:','ModelParams File does not exist:',modelParamsFile)
    sys.exit(2)

### Ordered dictionary with all parameters ###
#modelParams_dict = {}
#modelParams_dict['Grid'] = modelParams._sections['Grid']
#modelParams_dict['Solver'] = modelParams._sections['Solver']
#print(modelParams_dict)

#pd.options.display.max_colwidth=10000

######! Add absolute floorplan file paths !######
"""
try:
    #lcf_df['FloorplanFile']=lcf_df['FloorplanFile'].apply(lambda x : modelParams['Path']['flp']+x )
    lcf_df['FloorplanFile']= modelParams['Path']['flp']+lcf_df['FloorplanFile'].values  
    #lcf_df['LateralHeatFlow'] = lcf_df['LateralHeatFlow'].fillna('')
    #DEBUG: print(lcf_df['FloorplanFile'])
    #DEBUG: 
    #print(lcf_df['LateralHeatFlow'])
except TypeError:
    print('This is unreachable code, I think')
    print('Error: Each FloorplanFile entry in the lcf file must be non-empty and of \'string\' type')
    sys.exit(2)
"""

#####! Add a noPackage Layer !####
num_layers = lcf_df['Layer'].max()
#noPackage_layer = lcf_df[lcf_df['Layer']==num_layers]
#print("PRACHI debug:",num_layers)
lcf_df.loc[:,'VerticalHeatFlow']=True #Add Vetical True for all other layers
if "NoPackage" in modelParams:
    noPackage_layer = pd.DataFrame([],columns=['FloorplanFile','Layer','PtraceFile','LateralHeatFlow','VerticalHeatFlow','Thickness (m)'])
    noPackage_layer.loc[0,'FloorplanFile']=lcf_df.loc[num_layers,'FloorplanFile']
    noPackage_layer.loc[0,'Layer']=num_layers+1
    noPackage_layer.loc[0,'PtraceFile']=None
    noPackage_layer.loc[0,'LateralHeatFlow']=modelParams.get('NoPackage','LateralHeatFlow')
    noPackage_layer.loc[0,'VerticalHeatFlow']=modelParams.get('NoPackage','VerticalHeatFlow')
    noPackage_layer.loc[0,'Thickness (m)']=defaultConfig.get('NoPackage','thickness (m)')
    noPackage_layer.loc[0,'ConfigFile']=defaultConfigFile
    lcf_df = lcf_df.append(noPackage_layer,sort=False)
    thickness_layers[num_layers+1] = float(defaultConfig.get('NoPackage','thickness (m)'))
if "HeatSink" in modelParams:
    HeatSpreader_layer = pd.DataFrame([],columns=['FloorplanFile','Layer','PtraceFile','LateralHeatFlow','VerticalHeatFlow','Thickness (m)'])
    HeatSpreader_layer.loc[0,'FloorplanFile']=lcf_df.loc[num_layers,'FloorplanFile']
    HeatSpreader_layer.loc[0,'Layer']=num_layers+1
    HeatSpreader_layer.loc[0,'PtraceFile']=None
    HeatSpreader_layer.loc[0,'LateralHeatFlow']=modelParams.get('HeatSink','LateralHeatFlow')
    HeatSpreader_layer.loc[0,'VerticalHeatFlow']=modelParams.get('HeatSink','VerticalHeatFlow')
    HeatSpreader_layer.loc[0,'Thickness (m)']=defaultConfig.get('HeatSink','heatspreader_thickness (m)')
    HeatSpreader_layer.loc[0,'ConfigFile']=defaultConfigFile
    lcf_df = lcf_df.append(HeatSpreader_layer,sort=False,ignore_index=True)
    thickness_layers[num_layers+1] = float(defaultConfig.get('HeatSink','heatsink_thickness (m)'))
    HeatSink_layer = pd.DataFrame([],columns=['FloorplanFile','Layer','PtraceFile','LateralHeatFlow','VerticalHeatFlow','Thickness (m)'])
    HeatSink_layer.loc[0,'FloorplanFile']=lcf_df.loc[num_layers,'FloorplanFile']
    HeatSink_layer.loc[0,'Layer']=num_layers+2
    HeatSink_layer.loc[0,'PtraceFile']=None
    HeatSink_layer.loc[0,'LateralHeatFlow']=modelParams.get('HeatSink','LateralHeatFlow')
    HeatSink_layer.loc[0,'VerticalHeatFlow']=modelParams.get('HeatSink','VerticalHeatFlow')
    HeatSink_layer.loc[0,'Thickness (m)']=defaultConfig.get('HeatSink','heatsink_thickness (m)')
    HeatSink_layer.loc[0,'ConfigFile']=defaultConfigFile
    lcf_df = lcf_df.append(HeatSink_layer,sort=False,ignore_index=True)
    thickness_layers[num_layers+2] = float(defaultConfig.get('HeatSink','heatsink_thickness (m)'))
#sys.exit(0)
#lcf_df = lcf_df.append(pd.Series([num_layers+1,lcf_df.loc[num_layers,'FloorplanFile'],defaultConfig.get('NoPackage','thickness (m)'), '',modelParams.get('NoPackage','LateralHeatFlow'), modelParams.get('NoPackage','VerticalHeatFlow')], index=lcf_df.columns ), ignore_index=True)
#print(lcf_df)
#sys.exit(2)
#print(thickness_layers)
#sys.exit(2)
#print(lcf_df)

######! Check for missing data !######
### Read all unique floorplan files names ###
flp_files = lcf_df['FloorplanFile'].unique()
#print(flp_files)


### Create tuples of config_file and floorplan_file to check if the details of the  materials to be modeled are present ###
config_label_df = pd.DataFrame()
for ff in flp_files:
   # print(ff)
    try:
        ff_df = pd.read_csv(ff,lineterminator='\n')
       # print(ff_df)
    except FileNotFoundError:
        print('Error: Floorplan file not found',ff)
        sys.exit(2)
    #ff_df['ConfigFile'] =ff_df['ConfigFile'].fillna(parser.parse_args().configFile)
    #DEBUG: print(ff_df)

    #config_label_df = config_label_df.append(ff_df[['ConfigFile','Label']].drop_duplicates(), ignore_index=True)[['ConfigFile','Label']].drop_duplicates()
    config_label_df = config_label_df.append(ff_df[['ConfigFile','Label']].drop_duplicates(), ignore_index=True)
#print(config_label_df)
config_label_df.drop_duplicates(inplace=True)
config_label_df['ConfigFile'] = config_label_df['ConfigFile'].fillna(defaultConfigFile)
#print(config_label_df)
#DEBUG: 
#config_label_df['ConfigFile'] = config_path + config_label_df['ConfigFile']


##### No Package Data ####
#default_config_file = config_path + parser.parse_args().configFile
#print (config_label_df['ConfigFile'])
###################

#np.unique(a.set_index(['fname','lname']).index.values)
config_label_dict = {k: g["Label"].tolist() for k,g in config_label_df.groupby("ConfigFile")}
if "NoPackage" in modelParams:
    config_label_dict[defaultConfigFile] = config_label_dict[defaultConfigFile] + ['NoPackage']
if "HeatSink" in modelParams:
    config_label_dict[defaultConfigFile] = config_label_dict[defaultConfigFile] + ['HeatSink']
#config_label_dict[default_config_file] = config_label_dict[default_config_file] + ['NoPackage']
#print(config_label_dict)
##### debuf for No Package #####
#print(config_label_dict)
#sys.exit(2)
#########

list_of_labels = config_label_df['Label'].unique()
if "NoPackage" in modelParams:
    list_of_labels = np.append(list_of_labels,['NoPackage'],axis=0)
if "HeatSink" in modelParams:
    list_of_labels = np.append(list_of_labels,['HeatSink'],axis=0)

#print(list_of_labels,type(list_of_labels),list_of_labels.shape)
virtual_node_labels = {x: modelParams.get(x,'virtual_node') for x  in list_of_labels}
label_mode = {x: modelParams.get(x,'mode') for x in list_of_labels}
#print(label_mode)
#virtual_node_labels['NoPackage'] = 'bottom_center'
#print(virtual_node_labels)
#sys.exit(0)
#DEBUG: print (list_of_labels)
#DEBUG: print (config_label_dict)

### Ordered dictionary with all material properties from the specified config file ###
MaterialProp_dict = {}
#modelParams_dict['Grid'] = modelParams._sections['Grid']
#modelParams_dict['Solver'] = modelParams._sections['Solver']
#print(modelParams_dict)

#lib_dict={}
label_properties_dict = {}
for ll in list_of_labels:
    ######! Read Config file !######
    try:
        #if not (os.path.exists(modelParams.get(ll,'library'))):
        lib_location = modelParams.get(ll,'library')
        #if not (os.path.exists(lib_path+modelParams.get(ll,'library'))):
       # if not (os.path.exists(modelParams.get(ll,'library'))):
       #     print('ERROR: Library for the label',ll,':',modelParams.get(ll,'library'),'not found in',modelParamsFile)
       #     sys.exit(2)
        ######Below contains all libraries that should be imported###
        #lib_dict[ll]=lib_location.split(".")[0]
    except NoOptionError:
        print('ERROR: Library (used for thermal modeling) not defined for the label \'',ll, '\'')
        sys.exit(2)
    try:
        lib_name = modelParams.get(ll,'library_name')
        if(lib_name==''):
            print('ERROR: Library_name is null for the label \'',ll, '\'')
            sys.exit(2)
        lib = modelParams[lib_name]
    except NoOptionError:
        print('ERROR: Library_name not defined for the label \'',ll, '\'')
        sys.exit(2)
    #except NoSectionError:
        #print('ERROR: Section \'',lib_name,'\'not defined for the label \'',ll, '\'')
        #sys.exit(2)
    except KeyError:
        print('ERROR: Section \'',lib_name,'\'not defined for the label \'',ll, '\'')
        sys.exit(2)
    #    print("HELLO")
        #pass
    try:
        label_properties_dict[ll]=modelParams.get(lib_name,'properties')
    except (NoOptionError, KeyError):
        print("\'properties\' not defined for the label",ll,"in the modelParams file")
        sys.exit(2)

#print (label_properties_dict.items())
#print (label_properties_dict)
#DEBUG: print (label_properties_dict.items())
######! Check for missing data !######
label_prop_dict={}
config = configparser.ConfigParser()
for cf in config_label_dict.keys():
    ######! Read Config file !######
    if(cf == defaultConfigFile):
        config = defaultConfig
        #print("TRUE")
        #sys.exit(2)
    else:
        config.read(cf)
    for l in config_label_dict[cf]:
        #print(l)
        #sys.exit(2)
        try:
            properties = [option for option in config[l]]
            properties_needed = [x.strip() for x in label_properties_dict[l].split(',')]
            label_prop_dict[l]=properties_needed

            #x = config.get(l,'label') #'label' is a default attribute; any defined key will have an empty 'label'

            #START EDITING HERE#
            MaterialProp_dict.update({(cf,l): config._sections[l]})
            if not (set(properties_needed).issubset(set(properties))):
                #print(set(properties_needed))
                #print(set(properties))
                #print(set(properties_needed).difference(set(properties)))
                print("ERROR: Mising information about \'", section,"\'in",cf)
                print("Please ensure all the properties in the modelParams file are specified in the config file.")
                sys.exit(2)

        except (NoSectionError):
            print('ERROR: Label \'',l ,'\' not defined in ',cf)
            sys.exit(2)
        """ The commented code is no longer needed
        try:
            if (modelParams[l].getboolean('coolingTechnique')):
                try:
                    if not (os.path.exists(modelParams.get(l,'library'))):
                        print('Library for cooling technique',l,':',modelParams.get(l,'library'),'does not exist in',modelParamsFile)
                        sys.exit(2)
                except NoOptionError:
                    print(l, 'is a cooling technique and currently does not have a library implemented for its modeling')
                    sys.exit(2)
        except KeyError:
            pass
        """
#print("PRACHI CHECK", MaterialProp_dict)
#exec("import %s as Lib%s" % (lib_location.split(".")[0],ll))
######! check if all the properties (needed for modeling) are present in the config file !#######
"""
cf_parser = configparser.ConfigParser()
label_prop_dict={}
for cf, section_list in config_label_dict.items():
    cf_parser.read(cf)
    for section in section_list:
        properties = [option for option in cf_parser[section]]
        properties_needed = [x.strip() for x in label_properties_dict[section].split(',')]
        label_prop_dict[section]=properties_needed
        
        if not (set(properties_needed).issubset(set(properties))):
            #print(set(properties_needed))
            #print(set(properties))
            print("ERROR: Mising information about \'", section,"\'in",cf)
            print("Please ensure all the properties in the modelParams file are specified in the config file.")
            sys.exit(2)
"""
#sys.exit(2)
        #print(properties)
#print("PRACHIPRACHI",label_prop_dict)
#sys.exit(2)
#################################################################print("SUCCESS: All the label properties in the modelParams file are specified in the config files.")
######! print the dictionary !######
#print(MaterialProp_dict)
#sys.exit(2)

######! Read Default config file !######
#config = configparser.ConfigParser()
#config.read(configFile)

### Read initFile ###
#""" Uncomeent for future use
if (initFile is None):
    val, unit = defaultConfig['Init']['Temperature'].split()
    if (unit=='K' or unit == 'Kelvin'):
        initTemp = float(val)
    elif (unit=='C' or 'Celsius'):
        initTemp = float(val) - 273.15
else:
    initTemp = pd.read_csv(initFile,lineterminator="\n")
#"""
#print (parser.parse_args().initFile, initTemp)

########
#lcf_df['FloorplanFile']=lcf_df['FloorplanFile'].apply(lambda x : modelParams['Path']['flp']+x )
#print("BEFORE:",lcf_df)
#lcf_df['PtraceFile'] = lcf_df[lcf_df['PtraceFile'].notnull()]['PtraceFile'].apply(lambda x : modelParams['Path']['ptrace']+x)
#lcf_df['PtraceFile'] = lcf_df['PtraceFile'].apply(lambda x : modelParams['Path']['ptrace']+x if (x != None or x != np.nan) else x) 

###PRACHI: Uncomment below if needed##
#lcf_df['PtraceFile'] = lcf_df['PtraceFile'].apply(lambda x : modelParams['Path']['ptrace']+x if (type(x)==str and x!= None) else x) 
#lcf_df['PtraceFile'] = np.where(lcf_df['PtraceFile'] != '' , modelParams['Path']['ptrace'] + lcf_df['PtraceFile'], '') 
    #lcf["H"] = np.where(df["F"].str.contains("an"), 1, 0)
#print("AFTER",lcf_df)
#lcf_df['PtraceFile'] = lcf_df[lcf_df['PtraceFile'].notnull()]['PtraceFile'].apply(lambda x : modelParams['Path']['ptrace']+x)
#print(lcf_df)
#sys.exit(2)

"""
#####! Add a noPAckage Layer !####
num_layers = lcf_df['Layer'].max()
print("PRACHI debug:",num_layers)
noPackage_layer = lcf_df[lcf_df['Layer']==num_layers]
noPackage_layer['Layer']=num_layers+1
noPackage_layer['PtraceFile']=None
noPackage_layer['LateralHeatFlow']=modelParams.get('NoPackage','LateralHeatFlow')
noPackage_layer['Thickness (m)']=config.get('NoPackage','thickness (m)')
lcf_df = lcf_df.append(noPackage_layer)
"""
#DEBUG: print (lcf_df)

######! Display all panda frames and dictionaries !#######
#display_df_dict()
####PROFILE#####
#################
#print("----------------------------- All the data goes to the constructor for the class ChipStack-------------------------\n\n")
######! Create a Chipstack (Internally creates Layers)!######
#print(lcf_df)
#print(noPackage_layer)
#print(defaultConfig,defaultConfigFile,virtual_node_labels)
chipStack = ChipStack(lcf_df, defaultConfig, initTemp, defaultConfigFile,virtual_node_labels)
#print (lcf_df, config, initTemp)
#print (chipStack.display_Floorplans())
###chipStack.display_Floorplans('0')
#print(chipStack.Layers_data[0].num_ptraces)
#sys.exit(2)

#print("Checkpoint1")
######! ModelParams File as Dictionary !######
#print (modelParams._sections)
#print (modelParams._sections['TEC'])
#print (modelParams._sections['TEC'].get('transient'))
#print (modelParams._sections['TIM'].get('transient'))

#####Storing model details###

#model = Model()
#model.add_lib_dict(lib_dict)
#model.add_label_prop_dict(label_prop_dict)
#model.add_config_label_dict(config_label_dict)
#print(model.label_config_dict)
#print("PRACHI123",lib_dict)

######! Create Grids !#####
#print(type(chipStack))
gridManager = GridManager(modelParams._sections['Grid'])
#gridManager.addLibraries(lib_dict)

#print(gridManager.lib_dict)
#chipStack.display_Floorplans()

#gridManager.evaluateGridProperties(model)
#chipStack = gridManager.createGrids(chipStack)
#chipStack.display_Floorplans()

####TRYING TO Calculate resistance###### (In-progress)
#conditional imports of libraries
"""
for key_label,val_library in lib_dict.items():
    #print(key_label,val_library)
    exec("import %s as Lib%s" % (val_library,key_label))
"""
"""
#print ("HH",label_properties_dict.items())
label='Si'
prop = label_prop_dict[label]
#print(prop)
Si_properties = {x:float(config._sections[label].get(x)) for x in prop}
#for key,val in Si_properties.items():
    #print(key,val)
#Si_properties = {'thermalresistivity ((m-k)/w)':100,'specificheatcapacity (j/m^3k)':500 }
#rx,ry,rz,Cap,I = LibSi.defineGridProperties(1,2,3,1,Si_properties)
#LibSi_out={}
#LibSi_out[]
#if (label=="Si"):
#    import DefaultSolid as LibSi

#LibSi_out = LibSi.defineGridProperties(1,2,3,1,config._sections[label])
#print(LibSi.defineGridProperties(1,2,3,1,config._sections[label]))


#rx,ry,rz,Cap,I = LibSi.defineGridProperties(1,2,3,1,config._sections[label])
#print(rx,ry,rz,Cap,I)
#print ("Ye lo",LibSi_out['Rx'])
"""

###Unique pairs of label and config file###
#print ("PRACHI",config_label_dict)
#print(config_label_dict.keys())
#sys.exit(2)
#print(thickness_layers)
#label_config_dict = dict.fromkeys([(x,y.split("/config_files/")[1]) for y in config_label_dict.keys() for x in config_label_dict[y]])
label_config_dict = dict.fromkeys([(x,y) for y in config_label_dict.keys() for x in config_label_dict[y]])
#print(label_config_dict)
#sys.exit(0)
gridManager.add_label_config_mode_dict(label_config_dict,config,label_mode)
#print("PRACHI 12412",gridManager.label_config_dict)
#print(label_config_dict.items())
"""
for (label,cfile) in label_config_dict.keys():
    #print (label,cfile)
    if(label=='Si'):
        label_config_dict[(label,cfile)]=LibSi.defineGridProperties(1,2,3,config._sections['Si'])
        #print(label_config_dict[(label,cfile)])
    if(label=='TwoPhase'):
        label_config_dict[(label,cfile)]=LibTwoPhase.defineGridProperties(1,2,3,config._sections['TwoPhase'])
        #print(label_config_dict[(label,cfile)])
    if(label=='TIM'):
        label_config_dict[(label,cfile)]=LibTIM.defineGridProperties(1,2,3,config._sections['TIM'])
        #print(label_config_dict[(label,cfile)])
"""
chipStack = gridManager.createGrids(chipStack,label_config_dict)
#chipStack.display_Floorplans()
#######SOLVER#####
ambient_T = config._sections['Init'].get('ambient')
ambient_T = float(ambient_T.split(' ')[0])
print(ambient_T)
if modelParams._sections['Solver'].get('name') == 'SuperLU':
    print("high-level solver = SuperLU")
    exec("solver = %sSolver(modelParams._sections['Solver'].get('name'))" % (modelParams._sections['Solver'].get('name')) )

elif  modelParams._sections['Solver'].get('name') == 'SPICE_steady':
    print("high-level solver = SPICE_steady")
    print(f"low-level solver = {modelParams._sections['Solver'].get('ll_steady_solver')}")
    exec("solver = %sSolver(modelParams._sections['Solver'].get('name'),%s,modelParams._sections['Solver'].get('ll_steady_solver'),%s)" % (modelParams._sections['Solver'].get('name'),modelParams._sections['Simulation'].get('number_of_core'),ambient_T))

elif  modelParams._sections['Solver'].get('name') == 'SPICE_transient':
    print("high-level solver = SPICE_transient")
    os.system("rm -rf RC_transient_block_temp.csv")
    print(f"low-level solver = {modelParams._sections['Solver'].get('ll_transient_solver')}")
    exec("solver = %sSolver(modelParams._sections['Solver'].get('name'),%s,modelParams._sections['Solver'].get('ll_transient_solver'),modelParams._sections['Simulation'].get('step_size'),modelParams._sections['Simulation'].get('total_simulation_time'),modelParams._sections['Simulation'].get('ptrace_step_size'),%s)" % (modelParams._sections['Solver'].get('name'),modelParams._sections['Simulation'].get('number_of_core'),ambient_T ))

######## Zihao should modify the wrapper class (SuperLUSolver) #########
#solver = SuperLUSolver(modelParams._sections['Solver'].get('name'))#" % (modelParams._sections['Solver'].get('name')) )
#solver = SPICE_steadySolver(modelParams._sections['Solver'].get('name'))#" % (modelParams._sections['Solver'].get('name')) )
#solver = SPICESolver_transient(modelParams._sections['Solver'].get('name'))#" % (modelParams._sections['Solver'].get('name')) )
#######################################

#solver = SuperLUSolver(modelParams._sections['Solver'].get('name'))
#sys.exit(2)
#############solver.display_solver()
grid_rows=modelParams._sections['Grid'].get('rows')
grid_cols=modelParams._sections['Grid'].get('cols')
#print("Debug PRACHI***** grid_rows, grid_cols:",grid_rows,grid_cols)
#sys.exit(2)
num_layers = chipStack.num_layers

############# Zihao: see this; DO NOT change ################
#print("Debug PRACHI***** chipStacl.Layers_data.items() list:",list(chipStack.Layers_data.items()))
solver_properties={'grid_rows':grid_rows,'grid_cols':grid_cols,'num_layers':num_layers}
dict_Rx = {chipStack.Layers_data[x].layer_num:chipStack.Layers_data[x].Rx for x in chipStack.Layers_data.keys()}
dict_Ry = {chipStack.Layers_data[x].layer_num:chipStack.Layers_data[x].Ry for x in chipStack.Layers_data.keys()}
dict_Rz = {chipStack.Layers_data[x].layer_num:chipStack.Layers_data[x].Rz for x in chipStack.Layers_data.keys()}
dict_C = {chipStack.Layers_data[x].layer_num:chipStack.Layers_data[x].C for x in chipStack.Layers_data.keys()}
dict_I = {chipStack.Layers_data[x].layer_num:chipStack.Layers_data[x].I for x in chipStack.Layers_data.keys()}
dict_Conv = {chipStack.Layers_data[x].layer_num:chipStack.Layers_data[x].Conv for x in chipStack.Layers_data.keys()}
dict_others = {chipStack.Layers_data[x].layer_num:chipStack.Layers_data[x].others for x in chipStack.Layers_data.keys()}
dict_g2bmap = {chipStack.Layers_data[x].layer_num:chipStack.Layers_data[x].g2bmap for x in chipStack.Layers_data.keys()}
dict_virtual_nodes = {chipStack.Layers_data[x].layer_num:chipStack.Layers_data[x].virtual_node for x in chipStack.Layers_data.keys()}
# Ensure there is no singular R matrix 
for key,value in dict_Rx.items():
    value[value==0.0]=1e-6
for key,value in dict_Ry.items():
    value[value==0.0]=1e-6
for key,value in dict_Rz.items():
    value[value==0.0]=1e-6
solver_properties['Rx']=dict_Rx
solver_properties['Ry']=dict_Ry
solver_properties['Rz']=dict_Rz
solver_properties['C']=dict_C
solver_properties['I']=dict_I
solver_properties['Conv']=dict_Conv
solver_properties['others']=dict_others
solver_properties['g2bmap']=dict_g2bmap
solver_properties['others']=dict_others
#print("Printing dictionary")
#print("HELLLLOOOOOO",solver_properties['others'])
#print("HELLLLOOOOOO",solver_properties['Conv'])
#print("HELLLLOOOOOO",solver_properties['g2bmap'])
#sys.exit(0)
solver_properties['layer_virtual_nodes']=dict_virtual_nodes
solver_properties['factor_virtual_nodes']=modelParams._sections['VirtualNodes']
solver_properties['r_amb']=chipStack.Layers_data[num_layers-1].r_amb
#solver_properties.update({'Rx':{x:y} =chipStack.LayersData.apply(lambda x : x.Rx)
#print("Printing dictionary")
#print(label_config_dict)
#sys.exit(2)

############Zihao: see this; DO NOT modify#############
grid_temperature = solver.getTemperature(solver_properties)
#sys.exit(2)
#print(modelParams.get('Simulation','temperature_dependent'))
#sys.exit(2)
#print("PRACHI",hybrid_wick_properties)
if(str(modelParams.get('Simulation','temperature_dependent'))=='True'):
    #print("Temperature Dependent Mode")
    mode = 'temperature_dependent'
    count = 0
    #solver_properties['mode'] = 'Temperature Dependent'
    convergence = float(modelParams.get('Simulation','convergence'))
    deltaT = convergence + 1
    deltaLayer = 1
    hybrid_wick_properties = MaterialProp_dict[(defaultConfigFile,"HybridWick")]
    grid_length = gridManager.grid_length
    grid_width = gridManager.grid_width
    lcf_df.set_index('Layer',inplace=True)
    #print(lcf_df)
    thickness = thickness_layers[deltaLayer] 
    #print(thickness)
    #print(lcf_df['LateralHeatFlow'])
    while(deltaT > convergence):
        grid_temperature_old = np.copy(grid_temperature[deltaLayer])
        #print("Before",solver_properties['Rz'])
        #solver_properties.update(LibTemperatureDependent.getTemperatureDependentProperties(grid_length,\
        solver_properties = LibTemperatureDependent.getTemperatureDependentProperties(grid_length,\
            grid_width,thickness,grid_temperature_old,hybrid_wick_properties)
        #print(solver_properties)
        
        #print("After",solver_properties['Rz'])
        #print(solver_properties)
        grid_temperature = solver.getTemperature(solver_properties,mode)
        deltaT = np.max(abs(grid_temperature[deltaLayer] - grid_temperature_old))
        #print(deltaT)
        #sys.exit(2)
        count += 1
        if(count == 100):
            print("ERROR: No Convergence")
            sys.exit(2)
    
    print("num iterations:",count)
'''
if modelParams._sections['Solver'].get('name') == 'SPICE_transient':
     with open("RC_transient.cir.csv","r")as myfile:
         for num, lines in enumerate(myfile):
             if num!=0:
                 tmp = np.asarray(list(map(float,lines.split(',')[1:])))
                 reshape = tmp.reshape(int(num_layers),int(grid_rows),int(grid_cols))
                 with open("RC_transient_block_temp.csv","a") as myfile:
                     myfile.write("step "+str(num-1)+" ")
                 #print(reshape)
                 gridManager.grid2block(chipStack, reshape, modelParams.get('Grid','grid_mode'),transient=True)
'''
gridManager.grid2block(chipStack, grid_temperature,modelParams.get('Grid','grid_mode'))

#chipStack.display_Floorplans()
#pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)

#print("Back in CRI.py")
#print(virtual_node_labels)
#block_temperature = gridManager.g2bmap(chipStack,grid_temperature)
####print("0",grid_temperature)
#heat_map, num_layers = createHeatMap(grid_temperature,1)
"""
for ll in range(num_layers):
    plt.figure()
    ax = sns.heatmap(grid_temperature[ll],cmap="coolwarm")
    fig = ax.get_figure()
    ######CHANGE BELOW#################
    fig.savefig(heatMapFile+"_L"+str(ll)+".pdf")
#print("Layer0:\n",np.round(grid_temperature[0],6))
#print("Layer1:\n",np.round(grid_temperature[1],6))
#print("Layer2:\n",np.round(grid_temperature[2],6))
#print("2",arr_flat)
#arr_flat.tofile('foo.csv',sep='\n',format='%2.2f')
#print(L0_df)
"""
################UNCOMMENT the 3 below BELOW#################
#arr_flat = np.round(grid_temperature[0].flatten(),6)
#L0_df = pd.DataFrame(arr_flat)
#L0_df.to_csv(gridSteadyFile,header=False)

#print(grid_temperature.shape,grid_temperature.shape[0])
#for x in range(grid_temperature.shape[0]):
#    arr_flat = np.round(grid_temperature[x],6)
#    L_df = pd.DataFrame(arr_flat)
#    L_df.to_csv(gridSteadyFile+".layer"+str(x),header=False)
grid_temperature  = grid_temperature.reshape(num_layers,-1)
global counter
counter = 0
np.apply_along_axis(gridTemp2File,1,grid_temperature)

    #gridTemperatureToFile(grid_temperature[x],x)
#print("Tmax:",round(max(arr_flat)-273.15,2))

#L0_df.to_csv("/home/prachis/EDA_Validation/Run6_L0.grid.steady",header=False)

