import pandas as pd
import math
from Layer import Layer
import sys


class ChipStack:
    def __init__(self, lcf_df, config_df, initTemp, defaultConfigFile, virtual_node_locations):
        self.create_InitTemp(initTemp)
        self.create_Layer_data(lcf_df, defaultConfigFile,
                               virtual_node_locations, config_df)
        self.getChipDimensions()
        self.create_Config_dict(config_df)
        self.getVirtualNodes()
        return

    def create_Layer_data(self, lcf_df, defaultConfigFile, virtual_node_locations, config_df):
        self.num_layers = lcf_df['Layer'].count()
        lcf_df = lcf_df.sort_values('Layer', ascending=True)
        lcf_df = lcf_df.reset_index(drop=True)
        self.Layers_data = lcf_df.apply(lambda x: Layer(
            x, defaultConfigFile, virtual_node_locations), axis=1)  # Panda series
        if "NoPackage" in config_df:
            self.Layers_data[self.num_layers-1].flp_df['Label'] = 'NoPackage'
            self.Layers_data[self.num_layers-1].virtual_node = 'bottom_center'
        if "HeatSink" in config_df:
            self.Layers_data[self.num_layers-2].flp_df['Label'] = 'HeatSink'
            self.Layers_data[self.num_layers-1].flp_df['Label'] = 'HeatSink'
            self.Layers_data[self.num_layers-2].virtual_node = 'bottom_center'
            self.Layers_data[self.num_layers-1].virtual_node = 'bottom_center'

        self.num_ptrace_lines = max(
            [x.get_num_ptrace_lines() for y, x in self.Layers_data.items()])
        return

    def getChipDimensions(self):
        length = set(x.length for y, x in self.Layers_data.items())
        width = set(x.width for y, x in self.Layers_data.items())
        if (len(length) != 1) and (len(width) != 1):
            print("length/width mismatch between layers")
            sys.exit(2)
        self.length = round(float(length.pop()), 20)
        self.width = round(float(width.pop()), 20)
        return

    def create_Config_dict(self, config_df):
        self.Config_dict = pd.DataFrame()
        return

    def create_InitTemp(self, initTemp):
        if isinstance(initTemp, pd.DataFrame):
            self.initTemp = initTemp
        elif isinstance(initTemp, float):
            self.initTemp = initTemp
        return

    def updateConfigNaN(self, defaultConfigFile):
        self["ConfigFile"].fillna(defaultConfigFile)

    def display_Floorplans(self, flag='All'):
        if (flag == 'All'):
            for key, value in self.Layers_data.items():
                print("-------- Floorplan for Layer",
                      self.Layers_data[key].layer_num, "--------")
                print(self.Layers_data[key].flp_df, "\n")
        else:
            for key, value in self.Layers_data.items():
                if(int(self.Layers_data[key].layer_num) == int(flag)):
                    print("-------- Floorplan for Layer",
                          self.Layers_data[key].layer_num, "--------")
                    print(self.Layers_data[key].flp_df, "\n")
        return

    def getVirtualNodes(self):
        self.layers_virtual_nodes = {
            self.Layers_data[x].layer_num: self.Layers_data[x].virtual_node for x in range(self.num_layers)}
        return
