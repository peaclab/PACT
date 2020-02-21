import pandas as pd
import math
#from Layer import *
from Layer import Layer

class ChipStack:
    def __init__(self,lcf_df,config_df,initTemp,defaultConfigFile,virtual_node_locations):
        self.create_InitTemp(initTemp)
        self.create_Layer_data(lcf_df,defaultConfigFile,virtual_node_locations)
        self.getChipDimensions()
        self.create_Config_dict(config_df)
        self.getVirtualNodes()
        #self.add_ConfigData(config_df)
        return

    def create_Layer_data(self,lcf_df,defaultConfigFile,virtual_node_locations):
        self.num_layers=lcf_df['Layer'].count()
        lcf_df = lcf_df.sort_values('Layer',ascending=True)
        lcf_df = lcf_df.reset_index(drop=True)
        self.Layers_data = lcf_df.apply(lambda x : Layer(x,defaultConfigFile,virtual_node_locations),axis=1) #Panda series
        self.Layers_data[self.num_layers-1].flp_df['Label']='NoPackage'
        #Added
        #self.Layers_data[self.num_layers-1].VerticalHeatFlow = lcf_df[lcf_df['Layer']==self.num_layers-1]['VerticalHeatFlow']
        #self.display_Floorplans('All')
        return

    def getChipDimensions(self):
        length = set(x.length for y,x in self.Layers_data.items())
        width = set(x.width for y,x in self.Layers_data.items())
        if (len(length) != 1) and (len(width)!=1):
            print("length/width mismatch between layers")
            sys.exit(2)
        self.length = round(float(length.pop()),6)
        self.width = round(float(width.pop()),6)
        print("length and width:",self.length,self.width)
        return

    def create_Config_dict(self,config_df):
        self.Config_dict = pd.DataFrame()
        return
    
    def create_InitTemp(self,initTemp):
        if isinstance(initTemp, pd.DataFrame):
            self.initTemp = initTemp
        elif isinstance(initTemp , float):
            self.initTemp = initTemp
        return

    #def add_ConfigData(self,config_df):
        #return

    def updateConfigNaN(self,defaultConfigFile):
        self["ConfigFile"].fillna(defaultConfigFile)

    def display_Floorplans(self, flag='All'):
        if (flag == 'All'):
            for key, value in self.Layers_data.items():
                print("-------- Floorplan for Layer",self.Layers_data[key].layer_num,"--------")
                #print("-------- Floorplan for Layer",key,"--------")
                print(self.Layers_data[key].flp_df,"\n")
                #print(type(self.Layers_data[key].flp_df))
        else:
            for key, value in self.Layers_data.items():
                if(int(self.Layers_data[key].layer_num)==int(flag)):
                    print("-------- Floorplan for Layer",self.Layers_data[key].layer_num,"--------")
                    #print("-------- Floorplan for Layer",key,"--------")
                    print(self.Layers_data[key].flp_df,"\n")
        return

    def getVirtualNodes(self):
        self.layers_virtual_nodes = {self.Layers_data[x].layer_num : self.Layers_data[x].virtual_node for x in range(self.num_layers) }
        return

