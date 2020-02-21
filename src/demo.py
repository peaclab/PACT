import os
import sys, argparse
#print(len(sys.argv))

#print(sys.argv[1])
#import configparser

#DEMO 0: Successful Execution
if(sys.argv[1] == '0'):
    os.system('python3 CRICoolingTool.py demo/Layer_lcf.csv demo/default.config  demo/modelParams.config')

################################ LAYER FILE TESTS ######################################
#DEMO 1: Floorplan file not specified in the layer file
if(sys.argv[1] == '1'):
    os.system('python3 CRICoolingTool.py demo/MissingFloorplan_lcf.csv default.config  demo/modelParams.config')

#DEMO 2: Floorplan file does not exist
if(sys.argv[1] == '2'):
    os.system('python3 CRICoolingTool.py demo/FloorplanDoesNotExist_lcf.csv default.config  demo/modelParams.config')

#DEMO 3: Layer file does not exist
if(sys.argv[1] == '3'):
    os.system('python3 CRICoolingTool.py demo/NoSuchFile.csv default.config  demo/modelParams.config')

#DEMO 4: Thickness not specified in the layer file
if(sys.argv[1] == '4'):
    os.system('python3 CRICoolingTool.py demo/MissingThickness_lcf.csv default.config  demo/modelParams.config')
    

################################ CONFIG FILE TESTS ######################################
#DEMO 5: Label (e.g., Si) of a block not defined in the config file
if(sys.argv[1] == '5'):
    os.system('python3 CRICoolingTool.py demo/Layer_lcf.csv demo/MissingLabelDefinition.config  demo/modelParams.config')

#DEMO 6: Label (e.g., TIM) of a block not defined in the overwritten config file
if(sys.argv[1] == '6'):
    os.system('python3 CRICoolingTool.py demo/Layer_MissingLabelDef_lcf.csv demo/default.config  demo/modelParams.config')


################################ NODELPARAMS FILE TESTS ######################################
#DEMO 7: 'library' not defined for a label
if(sys.argv[1] == '7'):
    os.system('python3 CRICoolingTool.py demo/Layer_lcf.csv demo/default.config  demo/modelParams_MissingLibrary.config')

#DEMO 8: 'library_name' not defined for a label, i.e., parameters needed by the library are not defined.
if(sys.argv[1] == '8'):
    os.system('python3 CRICoolingTool.py demo/Layer_lcf.csv demo/default.config  demo/modelParams_MissingLibraryProperties.config')

#DEMO 9: 'library_name' section not defined, i.e., parameters needed by the library are not defined.
if(sys.argv[1] == '9'):
    os.system('python3 CRICoolingTool.py demo/Layer_lcf.csv demo/default.config  demo/modelParams_MissingLibraryNameSection.config')

#DEMO 10: Missing properties in config file. The properties are needed by the modeling library in the modelParams File.
if(sys.argv[1] == '10'):
    os.system('python3 CRICoolingTool.py demo/Layer_lcf.csv demo/defaultMissingProperty.config  demo/modelParams.config')
