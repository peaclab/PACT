import sys
import numpy as np
import pandas as pd
import math
import Solid as LibSi
import TwoPhaseVC as LibTwoPhase
import Solid as LibCu
import Solid as LibNoPackage
import HybridWick as LibHybridWick


class GridManager:
    def __init__(self,config_grid):
        #print("GridManager.py __init__()")
        self.grid_dict=config_grid
        #print("PRACHIII DDDDD rows and cols:",self.grid_dict['rows'],self.grid_dict['cols'])
        self.Lock = np.zeros((int(self.grid_dict['rows']),int(self.grid_dict['cols'])))
        self.Rx = np.zeros((int(self.grid_dict['rows']),int(self.grid_dict['cols'])))
        self.Ry = np.zeros((int(self.grid_dict['rows']),int(self.grid_dict['cols'])))
        self.Rz = np.zeros((int(self.grid_dict['rows']),int(self.grid_dict['cols'])))
        self.C = np.zeros((int(self.grid_dict['rows']),int(self.grid_dict['cols'])))
        self.I = np.zeros((int(self.grid_dict['rows']),int(self.grid_dict['cols'])))
        self.g2bmap = np.empty([int(self.grid_dict['rows']),int(self.grid_dict['cols'])],dtype="<U10")
        self.vector_evaluateRC = np.vectorize(self.evaluateRC,otypes=[None])
        #print(type(self.grid_dict))
        #print(self.grid_dict['type'],self.grid_dict['granularity'])
        return

    def add_label_config_mode_dict(self,label_config_dict,defaultConfig, label_mode_dict):
        self.label_config_dict = label_config_dict
        self.label_mode_dict = label_mode_dict
        self.config=defaultConfig
        return

    def reset_label_config_dict(self):
        self.label_config_dict = self.label_config_dict.fromkeys(self.label_config_dict,0)

    def createGrids(self, chipstack,label_config_dict):
        self.length = round(chipstack.length,8)
        self.width = round(chipstack.width,8)
        self.initTemp = chipstack.initTemp
        #print("createGrids")
        if (self.grid_dict['type']=='Uniform') and (self.grid_dict['granularity']=='Grid'):
            return self.createUniformGrids(chipstack,label_config_dict)
        return chipstack

    def createUniformGrids(self, chipStack,label_config_dict):
        #self.label_config_dict=label_config_dict
        #print("createUniformGrids")
        rows = int(self.grid_dict['rows'])
        cols = int(self.grid_dict['cols'])
        #grid_length = round(chipStack.length/cols,6)
        #grid_width = round(chipStack.width/rows,6)
        grid_length = chipStack.length/cols
        self.grid_width = chipStack.width/rows
        self.grid_length = chipStack.length/cols
        grid_width = chipStack.width/rows
        print(rows,"x",cols,"; grid_length and width:",grid_length,grid_width)
        if (grid_length*cols != chipStack.length) or (grid_width*rows != chipStack.width):
            print("Unifrom grids cannot be formed. Choose a multiple of 2 or 5 as rows and columns")
            sys.exit(2)
        #self.Layers_data.apply(self.disp, args=(5,6))
        layers = chipStack.Layers_data
        a = [chipStack.Layers_data.loc[i].flp_df['X'] for i in layers.index]
        #print(type(a))
        chipStack.Layers_data = chipStack.Layers_data.apply(self.calculate_boundary_grids, args=(grid_length, grid_width,chipStack.num_layers))
        #print("CreateBoundaryGrids successfully completeed")
        #####RESUME ABOVE####
        """
        layers = chipStack.Layers_data.to_frame()
        print("Check1",type(layers),layers)
        print("Check2",type(chipStack.Layers_data),chipStack.Layers_data)
        #layers = layers.apply(self.calculate_boundary_grids, args=(grid_length, grid_width))
        #chipStack.Layers_data = chipStack.Layers_data.apply(self.createUniformGridsWithOccupancy, args=(grid_length, grid_width))
        #print(type(layers))
        #print(type(layers.loc[0].flp_df['X']))
        print("Index",layers.index)
        """
        return chipStack

    def disp(self,x,a,b):
        print(a,b,type(x))
        print("1")
        print(x.flp_df['X'])
        print("2")
        return

    """Original
    def calculate_boundary_grids(self, layer_obj,grid_length,grid_width):
        #print("calculate_boundary_grids")
        #try:

        print("Layer",layer_obj.layer_num)
        print(self.label_config_dict.keys())
        thickness = layer_obj.thickness
        for (label,cfile) in self.label_config_dict.keys():
            #print (label,cfile)
            if(label=='Si'):
                self.label_config_dict[(label,cfile)]=LibSi.defineGridProperties(grid_length,grid_width,thickness,self.config._sections['Si'])
                #print(label_config_dict[(label,cfile)])
            if(label=='TwoPhase'):
                self.label_config_dict[(label,cfile)]=LibTwoPhase.defineGridProperties(grid_length,grid_width,thickness,self.config._sections['TwoPhase'])
                #print(label_config_dict[(label,cfile)])
            if(label=='TIM'):
                self.label_config_dict[(label,cfile)]=LibTIM.defineGridProperties(grid_length,grid_width,thickness,self.config._sections['TIM'])

        self.Rx = np.zeros(self.Rx.shape)
        self.Ry = np.zeros(self.Ry.shape)
        self.Rz = np.zeros(self.Rz.shape)
        self.C = np.zeros(self.C.shape)
        self.I = np.zeros(self.I.shape)
        self.Lock = np.zeros(self.Lock.shape)
        self.g2bmap = np.empty(self.g2bmap.shape,dtype="<U10")
        flp_df = layer_obj.flp_df
        print(flp_df)
        #print(type(flp_df))
        #print(flp_df)
        flp_df['grid_left_x']= flp_df.apply(lambda x: math.floor(float(x.X)/grid_width), axis=1)
        #flp_df['grid_bottom_y']= flp_df.apply(lambda x: math.floor(float(x.Y)/grid_length),axis=1)
        flp_df['grid_bottom_y']= flp_df.apply(lambda x: int(self.grid_dict['rows']) - math.floor(float(x.Y)/grid_length) - 1,axis=1)
        temp_x = flp_df.apply(lambda x: (float(x.X)+float(x['Length (m)']))/grid_width, axis=1)#Panda Series
        temp_y = flp_df.apply(lambda x: (float(x.Y)+float(x['Width (m)']))/grid_length, axis=1)
        flp_df['grid_right_x'] = temp_x.apply(lambda x : math.floor(x) if math.ceil(x) != math.floor(x) else math.floor(x)-1)
        #flp_df['grid_top_y'] = temp_y.apply(lambda x : math.floor(x) if math.ceil(x) != math.floor(x) else math.floor(x)-1)
        flp_df['grid_top_y'] = temp_y.apply(lambda x : int(self.grid_dict['rows']) -  math.floor(x) if math.ceil(x) != math.floor(x) else int(self.grid_dict['rows']) -math.floor(x))
        #print(flp_df)
        layer_obj.flp_df = flp_df
        #print(type(layer_obj.flp_df),type(layer_obj))

        X_vals = flp_df['X'].values
        Y_vals = flp_df['Y'].values
        length_vals=flp_df['Length (m)'].values
        height_vals=flp_df['Width (m)'].values
        PowerDensities = flp_df['Power'].values / (length_vals * height_vals)

        left_x_vals=flp_df['grid_left_x'].values
        right_x_vals=flp_df['grid_right_x'].values
        top_y_vals=flp_df['grid_top_y'].values
        bottom_y_vals=flp_df['grid_bottom_y'].values
        label_config_arr = list(zip(flp_df['Label'].values, flp_df['ConfigFile'].values))
        listCoords=list(zip(left_x_vals,right_x_vals,bottom_y_vals,top_y_vals))
        #print(label_config_arr)
        #print(listCoords)
        block_counter=np.arange(left_x_vals.size)
        #print(block_counter)
        self.vector_evaluateRC(X_vals,Y_vals,length_vals, height_vals, PowerDensities,left_x_vals,right_x_vals,bottom_y_vals,top_y_vals,flp_df['Label'].values,flp_df['ConfigFile'].values,block_counter,grid_length,grid_width)
        layer_obj.Rx = self.Rx
        layer_obj.Ry = self.Ry
        layer_obj.Rz = self.Rz
        layer_obj.C = self.C
        layer_obj.I = self.I
        layer_obj.Lock = self.Lock
        layer_obj.g2bmap = self.g2bmap
        #print("Rx",layer_obj.Rx)
        #print("Ry",layer_obj.Ry)
        #print("Rz",layer_obj.Rz)
        #print("C",layer_obj.C)
        #print("I",layer_obj.I)
        #print(layer_obj.Lock)
        #print("g2bmap",layer_obj.g2bmap)
        #print("Hello")
        return layer_obj
    """

    def calculate_boundary_grids(self, layer_obj,grid_length,grid_width, num_layers):
        #print("calculate_boundary_grids")
        #try:
        #print("Calculate_boundary_grids for Layer",layer_obj.layer_num,"out of num_layers=",num_layers)
        #print("shape",self.Rx.shape)
        #print(self.label_config_dict.keys())
        thickness = layer_obj.thickness
        rows = int(self.grid_dict['rows'])
        cols = int(self.grid_dict['cols'])
        #print("thickness",layer_obj.thickness)
        self.Rx = np.zeros(self.Rx.shape)
        self.Ry = np.zeros(self.Ry.shape)
        self.Rz = np.zeros(self.Rz.shape)
        self.C = np.zeros(self.C.shape)
        self.I = np.zeros(self.I.shape)
        self.Lock = np.zeros(self.Lock.shape)
        self.g2bmap = np.empty(self.g2bmap.shape,dtype="<U10")
        flp_df = layer_obj.flp_df
        label_ll = flp_df['Label'].unique()
        #print(label_ll)

        if(layer_obj.layer_num < num_layers-1):
            ####FIND BOUNDARIES###
            #flp_df['grid_left_x']= flp_df.apply(lambda x: math.floor(round(float(x.X)/grid_width,8)), axis=1)
            X_vals = np.round(flp_df['X'].values,8)
            Y_vals = np.round(flp_df['Y'].values,8)
            length_vals = np.round(flp_df['Length (m)'].values,8)
            height_vals = np.round(flp_df['Width (m)'].values,8)
            temp_x_vals = (X_vals + length_vals)/grid_length
            temp_y_vals = (Y_vals + height_vals)/grid_width
            grid_left_x = np.floor(X_vals/grid_length)
            grid_bottom_y= rows - np.floor(Y_vals/grid_width) - 1
            ceil = np.ceil(temp_x_vals)
            floor = np.floor(temp_x_vals)
            #grid_right_x = ceil - 1 if np.array_equal(ceil,floor) else floor
            #print("1",grid_right_x)
            grid_right_x = np.where(ceil==floor,ceil - 1,floor)

            ceil = np.ceil(temp_y_vals)
            floor = np.floor(temp_y_vals)
            grid_top_y = np.where(ceil == floor,rows - floor,rows - ceil)
            #grid_top_y = rows - floor if np.array_equal(ceil,floor) else rows - ceil
            PowerDensities = flp_df['Power'].values / (length_vals * height_vals)
            flp_df['grid_left_x']= flp_df.apply(lambda x: math.floor(round(float(x.X)/grid_length,8)), axis=1)
            flp_df['grid_bottom_y']= flp_df.apply(lambda x: int(self.grid_dict['rows']) - math.floor(round(float(x.Y)/grid_width,8)) - 1,axis=1)
            temp_x = flp_df.apply(lambda x: (round(float(x.X),8)+round(float(x['Length (m)']),8))/grid_length, axis=1).round(8) #Panda Series
            temp_y = flp_df.apply(lambda x: (round(float(x.Y),8)+round(float(x['Width (m)']),8))/grid_width, axis=1).round(8)
            flp_df['grid_right_x'] = temp_x.apply(lambda x : math.floor(x) if math.ceil(x) != math.floor(x) else math.ceil(x) - 1 )
            flp_df['grid_top_y'] = temp_y.apply(lambda x : int(self.grid_dict['rows']) -  math.ceil(x) if math.ceil(x) != math.floor(x) else int(self.grid_dict['rows']) -math.floor(x))
            #print(np.array_equal(grid_left_x, flp_df['grid_left_x'].values))
            #print(np.array_equal(grid_bottom_y ,flp_df['grid_bottom_y']. values))
            #print(np.array_equal(grid_right_x, flp_df['grid_right_x'].values))
            #print(np.array_equal(grid_top_y, flp_df['grid_top_y'].values))
            #sys.exit(2)
            layer_obj.flp_df = flp_df
            ####debug####
            #if (layer_obj.layer_num== 0):
            #    print(PowerDensities)
            ############
            left_x_vals = np.round(flp_df['grid_left_x'].values,8)
            right_x_vals = np.round(flp_df['grid_right_x'].values,8)
            top_y_vals = np.round(flp_df['grid_top_y'].values,8)
            bottom_y_vals = np.round(flp_df['grid_bottom_y'].values,8)
            label_vals = flp_df['Label'].values
            label_config_arr = list(zip(label_vals, flp_df['ConfigFile'].values))
            listCoords1=list(zip(grid_left_x,grid_right_x,grid_bottom_y,grid_top_y))
            listCoords=list(zip(left_x_vals,right_x_vals,bottom_y_vals,top_y_vals))
            print("*******************listCoords*************8: match?", listCoords1 == listCoords)
            #print(label_config_arr)
            #print(listCoords)
            block_counter=np.arange(left_x_vals.size)
            #print(block_counter)
            #print(self.label_config_dict.keys())
            #sys.exit(2)
            if (type(self.initTemp)==float):
                grid_temperatures = np.full((rows,cols),float(self.initTemp))
            for (label,cfile) in self.label_config_dict.keys() :
                #print (label,cfile)
                if(label in label_ll and self.label_mode_dict[label]=='single'):
                    if(label=='Si'):
                        #print("1")
                        self.label_config_dict[(label,cfile)]=LibSi.defineGridProperties(grid_length,grid_width,thickness,self.config._sections['Si'])
                        #print(label_config_dict[(label,cfile)])
                    elif(label=='TwoPhaseVC'):
                        #print("3")
                        self.label_config_dict[(label,cfile)]=LibTwoPhase.defineGridProperties(grid_length,grid_width,thickness,self.config._sections['TwoPhaseVC'])
                        #print(label_config_dict[(label,cfile)])
                    elif(label=='Cu'):
                        #print("3")
                        self.label_config_dict[(label,cfile)]=LibCu.defineGridProperties(grid_length,grid_width,thickness,self.config._sections['Cu'])
                    elif(label=='NoPackage'):
                        #print("4")
                        self.label_config_dict[(label,cfile)]=LibNoPackage.defineGridProperties(grid_length,grid_width,thickness,self.config._sections['NoPackage'])

                elif(label in label_ll and self.label_mode_dict[label]=='matrix'):
                    #print(label,self.label_mode_dict[label],label_ll)
                    #if(label=='HybridWick'):
                    #    print("DEUGPRACHI")
                    #sys.exit(2)
                    if(label=='HybridWick'):
                        #grid_labels = np.full((int(self.grid_dict['rows']),int(self.grid_dict['cols'])),"HybridWick")
                        #print("Matrix", label)
                        properties = self.config._sections['HybridWick']
                        properties.update([("grid_temperatures",grid_temperatures)])
                        self.label_config_dict[(label,cfile)]=LibHybridWick.defineGridPropertiesMatrix(label,grid_length,grid_width,thickness,properties)
                    if(label=='Si'):
                        #print("Matrix", label)
                        properties = self.config._sections['Si']
                        properties.update([("grid_rows",rows)])
                        properties.update([("grid_cols",cols)])
                        self.label_config_dict[(label,cfile)]=LibSi.defineGridPropertiesMatrix(grid_length,grid_width,thickness,properties)

                    self.Rx +=  self.label_config_dict[(label,cfile)]['Rx']
                    self.Ry += self.label_config_dict[(label,cfile)]['Ry']
                    self.Rz += self.label_config_dict[(label,cfile)]['Rz']
                    self.C += self.label_config_dict[(label,cfile)]['Capacitance']
                    self.I += self.label_config_dict[(label,cfile)]['I']
                    break
                        #self.g2bmap[topY+1:bottomY,leftX+1:rightX]= "B"+str(block_idx)+"_1"

                        #sys.exit(2)
                        
            print(flp_df)
            #sys.exit(0)
                #print("hey there layer",layer_obj.layer_num)
                #for x in label_ll:
                #    print('single' in self.label_mode_dict[x])
            self.vector_evaluateRC(X_vals,Y_vals,length_vals, height_vals, PowerDensities,left_x_vals,right_x_vals,bottom_y_vals,top_y_vals,label_vals,flp_df['ConfigFile'].values,block_counter,grid_length,grid_width)

                #sys.exit(0)
            #print("Lateral Heat Flow for layer",layer_obj.layer_num,"is",layer_obj.LateralHeatFlow)
            if(str(layer_obj.LateralHeatFlow) == 'True'):
                print("Lateral Heat Flow is TRUE for layer",layer_obj.layer_num)
                layer_obj.Rx = self.Rx
                layer_obj.Ry = self.Ry
            else:
                print("Lateral Heat Flow is FALSE for layer",layer_obj.layer_num)
                layer_obj.Rx = np.ones(self.Rx.shape) * math.inf
                layer_obj.Ry = np.ones(self.Rx.shape) * math.inf

            layer_obj.Rz = self.Rz
            layer_obj.C = self.C
            layer_obj.I = self.I
            layer_obj.Lock = self.Lock
            layer_obj.g2bmap = self.g2bmap

            if(layer_obj.layer_num == num_layers-2):
                self.noPackage_grid_left_x = flp_df['grid_left_x']
                self.noPackage_grid_right_x = flp_df['grid_right_x']
                self.noPackage_grid_bottom_y = flp_df['grid_bottom_y']
                self.noPackage_grid_top_y = flp_df['grid_top_y']
                self.noPackage_g2bmap = self.g2bmap
                self.noPackage_Lock = self.Lock
                #print("Earlier no PAckage resistances: Rx and Ry",self.Rx,self.Ry)
                #self.noPackage_Rx = self.Rx
                #self.noPackage_Ry = self.Ry
            #if(layer_obj.layer_num == 1):
                #print("VC Layer!!! Rz values:")
                #print(layer_obj.Rz)
                #print(layer_obj.Rx, layer_obj.Ry)
                #layer_obj.Rx = np.ones(self.Rx.shape) * math.inf
                #layer_obj.Ry = np.ones(self.Rx.shape) * math.inf

        else:
            #print("NoPackageLayer")
            #print("layer_obj.LateralHeatFlow =",layer_obj.LateralHeatFlow )
            #print("layer_obj.VerticalHeatFlow =",layer_obj.VerticalHeatFlow )
            #sys.exit(2)
            flp_df['grid_left_x']=self.noPackage_grid_left_x 
            flp_df['grid_right_x']=self.noPackage_grid_right_x 
            flp_df['grid_bottom_y']=self.noPackage_grid_bottom_y
            flp_df['grid_top_y']=self.noPackage_grid_top_y 
            #print(grid_length,grid_width,thickness,self.config._sections['NoPackage'])
            if(layer_obj.LateralHeatFlow or layer_obj.VerticalHeatFlow):
                for (label,cfile) in self.label_config_dict.keys():
                    #print ("PRACHI",label,cfile)
                    if(label=='NoPackage'):
                        #print("4")
                        NoPackage_info=LibNoPackage.defineGridProperties(grid_length,grid_width,thickness,self.config._sections['NoPackage'])
                        break
            #layer_obj.Rx = np.full((int(self.grid_dict['rows']),int(self.grid_dict['cols'])),np.inf)
            #layer_obj.Ry = np.full((int(self.grid_dict['rows']),int(self.grid_dict['cols'])),np.inf)

            #print(layer_obj.LateralHeatFlow)
            if (str(layer_obj.LateralHeatFlow) == 'True'):
                #print("noPackage layer has lateral TRUE")
                layer_obj.Rx = np.ones(self.Rx.shape) * NoPackage_info['Rx']
                layer_obj.Ry = np.ones(self.Ry.shape) * NoPackage_info['Ry']
                #layer_obj.Rx = self.noPackage_Rx
                #layer_obj.Ry = self.noPackage_Ry
            else:
                #print("noPackage layer has lateral FALSE")
                layer_obj.Rx = np.ones(self.Rx.shape) * math.inf
                layer_obj.Ry = np.ones(self.Ry.shape) * math.inf


            #print(layer_obj.VerticalHeatFlow)
            if (str(layer_obj.VerticalHeatFlow) == 'True'):
                #print("noPackage layer has vertical TRUE")
                r_amb = 1/(float(self.config.get('NoPackage','htc'))*grid_length*grid_width) + NoPackage_info['Rz']
                #r_amb = layer_obj.Rz + np.full((int(self.grid_dict['rows']),int(self.grid_dict['cols'])),r_amb)
            else:
                #print("noPackage layer has vertical FALSE (i.e., direct connection to ambient")
                r_amb = 1/(float(self.config.get('NoPackage','htc'))*grid_length*grid_width)
            #print("Rz",layer_obj.Rz)

            #layer_obj.Rx = self.noPackage_Rx
            #layer_obj.Ry = self.noPackage_Ry
            #print("noPackage:")
            
            #r_amb = 1/(float(self.config.get('NoPackage','htc'))*grid_length*grid_width)
            #print("r_amb =", r_amb)
            layer_obj.Rz = np.full((int(self.grid_dict['rows']),int(self.grid_dict['cols'])),r_amb)
            #print("Rz",layer_obj.Rz)
            layer_obj.C = np.ones((int(self.grid_dict['rows']),int(self.grid_dict['cols'])),dtype=float)
            val, unit = self.config.get('Init','ambient').split()
            if (unit=='K' or unit == 'Kelvin'):
                val = round(float(val),6)
            elif (unit=='C' or 'Celsius'):
                val = round(float(val),6) + 273.15
            #P_noPackage = round(val/r_amb,6)
            P_noPackage = val/r_amb
            print("PRACHI: (NoPackage) r_amb and Power(per_grid) for dummy layer are",r_amb,P_noPackage)
            layer_obj.I = np.full((int(self.grid_dict['rows']),int(self.grid_dict['cols'])),P_noPackage)
            layer_obj.Lock = self.noPackage_Lock
            layer_obj.g2bmap = self.noPackage_g2bmap
            layer_obj.flp_df = flp_df
            layer_obj.r_amb = r_amb

        #np.set_printoptions(threshold=np.inf)
        #####Undo below prints if you want more detailed insights
        #print("Layer",layer_obj.layer_num)
        #print("Rx",layer_obj.Rx)
        #print("Ry",layer_obj.Ry)
        #print("Rz",layer_obj.Rz)
        #print("C",layer_obj.C)
        #print("I",layer_obj.I)
        #print(layer_obj.Lock)
        #print("g2bmap",layer_obj.g2bmap)
        #try:
        #    print("r_amb =",layer_obj.r_amb,"in layer",layer_obj.layer_num)
        #except:
        #    print("r_amb not in Layer",layer_obj.layer_num)
            #pass
        #print("Hello")
        return layer_obj

    """
    def createUniformGridsWithOccupancy(self, layer_obj, grid_length, grid_width):
        df_cols = ["Name","i","j", "Occupancy",]
        gridCell_df = pd.DataFrame()
        return
    """

    ###RESUME HERE###
    def evaluateRC(self, X,Y,length,width, PowerDensity,leftX,rightX,bottomY,topY,label,config,block_idx,grid_length, grid_width):
        area = grid_length * grid_width
        #power = round(PowerDensity * area,8)
        power = PowerDensity * area
        ##3Undo below two comments
        #print("power:",power)
        #print (X,Y,length, width,PowerDensity,leftX,rightX,bottomY,topY,label,config,block_idx)

        #print(self.label_config_dict[(label,config)]['Rx'])
        #print(type(leftX))
        #Rx[leftX+1:rightX,bottomY+1:topY]= self.label_config_dict[(label,config)]['Rx']
        """
        self.Rx[leftX+1:rightX,bottomY+1:topY]= self.label_config_dict[(label,config)]['Rx']
        self.Ry[leftX+1:rightX,bottomY+1:topY]= self.label_config_dict[(label,config)]['Ry']
        self.Rz[leftX+1:rightX,bottomY+1:topY]= self.label_config_dict[(label,config)]['Rz']
        self.C[leftX+1:rightX,bottomY+1:topY]= self.label_config_dict[(label,config)]['Capacitance']
        self.I[leftX+1:rightX,bottomY+1:topY]= self.label_config_dict[(label,config)]['I']
        self.Occupancy[leftX+1:rightX,bottomY+1:topY] +=1
        """
        #print("PRACHIIIIIII",self.label_config_dict[(label,config)]['Rx'])
        #self.Rx[topY+1:bottomY,leftX+1:rightX]= np.round(self.label_config_dict[(label,config)]['Rx'],8)
        #self.Ry[topY+1:bottomY,leftX+1:rightX]= np.round(self.label_config_dict[(label,config)]['Ry'],8)
        #self.Rz[topY+1:bottomY,leftX+1:rightX]= np.round(self.label_config_dict[(label,config)]['Rz'],8)
        #self.C[topY+1:bottomY,leftX+1:rightX]= np.round(self.label_config_dict[(label,config)]['Capacitance'],8)
        #self.I[topY+1:bottomY,leftX+1:rightX]= round(power + round(self.label_config_dict[(label,config)]['I'],8),8)
        ###ADDED BELOW August PRACHIIIIIIIIIIIIIII
        print("\nPRACHI Debug 1: Start")
        print ("X,Y,length, width,PowerDensity,leftX,rightX,bottomY,topY,label,config,block_idx:")
        print (X,Y,length, width,PowerDensity,leftX,rightX,bottomY,topY,label,config,block_idx)
        if(self.label_mode_dict[label]=='matrix' and PowerDensity == 0):
            print("matrix mode in evaluate RC with zero power density")
            self.Lock[topY:bottomY+1,leftX:rightX+1] +=1

        elif(PowerDensity != 0 ):
            length_lb_o = round((leftX+1)*grid_length - X,8)
            length_rb_o =  round((X+length) - (rightX)*grid_length,8)
            length_lt_o = length_lb_o
            length_rt_o = length_rb_o
            #width_lb_o = round((self.width - Y ) - bottomY*grid_width,8)
            width_lb_o = round((int(self.grid_dict['rows']) - bottomY )*grid_width  - Y,8)
            width_rb_o = width_lb_o
            #width_lt_o = round((self.width - Y - width) - (topY-1)*grid_width,8)
            width_lt_o = round((topY + 1) * grid_width  - (self.width - Y - width),8)
            width_rt_o = width_lt_o
            if((length_lb_o == length_rb_o == grid_length) and (width_lb_o == width_lt_o == grid_width)):
                print("Block",block_idx,"is not sharing its boundaries")
            #if(length_lb_o == grid_length and ):
                #self.C[topY:bottomY+1,leftX:rightX+1]= self.label_config_dict[(label,config)]['Capacitance']
                self.I[topY:bottomY+1,leftX:rightX+1]= power + self.label_config_dict[(label,config)]['I']
                self.Lock[topY:bottomY+1,leftX:rightX+1] +=1
                #self.g2bmap[topY:bottomY+1,leftX:rightX+1]= "B"+str(block_idx)+"_1"
            else:
                lb_o = np.round(length_lb_o * width_lb_o / (area),8)
                rb_o = np.round(length_rb_o * width_rb_o / (area),8)
                lt_o = np.round(length_lt_o *  width_lt_o / (area),8)
                rt_o = np.round(length_rt_o * width_rt_o / (area),8)
                left_edge_cells_o = round(length_lb_o / grid_length,8)
                right_edge_cells_o = round(length_rb_o / grid_length,8)
                top_edge_cells_o = round(width_lt_o /grid_width,8)
                bottom_edge_cells_o = round(width_lb_o / grid_width,8)
                edge_cells_o = {'lb_o':lb_o,'rb_o':rb_o,'lt_o':lt_o,'rt_o':rt_o,'left_edge_cells_o':left_edge_cells_o, 'right_edge_cells_o':right_edge_cells_o, 'top_edge_cells_o':top_edge_cells_o, 'bottom_edge_cells_o':bottom_edge_cells_o}

                mask = np.ones((bottomY - topY + 1, rightX - leftX + 1))
                mask[:,0] = left_edge_cells_o
                mask[:,-1] = right_edge_cells_o
                mask[0,:] = top_edge_cells_o
                mask[-1,:] = bottom_edge_cells_o 
                mask[0,0] = lt_o
                mask[0,-1] = rt_o
                mask[-1,-1] = rb_o
                mask[-1,0] = lb_o 

        #if(self.label_mode_dict[label]=='single'):
            #print("single mode in evaluate RC")
            #lb -> left bottom, rb -> right bottom, lt -> left top, rt -> right top; remember that indices start from 0. Hence + 1
            """
            length_lb_o = (leftX)*grid_length - X 
            length_rb_o = (rightX+1)*grid_length - (X+length)
            length_lt_o = length_lb_o
            length_rt_o = length_rb_o
            width_lb_o = (bottomY+1)*grid_width - (self.width - Y )
            width_rb_o = width_lb_o
            width_lt_o = topY*grid_width - (self.width - Y - width)
            width_rt_o = width_lt_o
            """
            """ REstructuring
            #length_lb_o = round(X - (leftX-1)*grid_length,8)
            #length_lb_o = round((leftX+1)*grid_length - X,8)
            #length_rb_o =  round((X+length) - (rightX)*grid_length,8)
            #length_lt_o = length_lb_o
            #length_rt_o = length_rb_o
            #width_lb_o = round((int(self.grid_dict['rows']) - bottomY )*grid_width  - Y,8)
            #width_rb_o = width_lb_o
            #width_lt_o = round((topY + 1) * grid_width  - (self.width - Y - width),8)
            #width_rt_o = width_lt_o
            #print("length_lb_o" , length_lb_o , "; length_rb_o" , length_rb_o ,"; length_lt_o" , length_lt_o , "; length_rt_o" , length_rt_o \
            #    , "; width_lb_o" ,width_lb_o , "; width_rb_o" , width_rb_o , "; width_lt_o" , width_lt_o , "; width_rt_o" , width_rt_o )
            #set_length = { length_lb_o, length_rb_o}
            #set_width = {width_lb_o, width_lt_o} 
            if((length_lb_o == length_rb_o == grid_length) and (width_lb_o == width_lt_o == grid_width)):
                print("Block",block_idx,"is not sharing its boundaries")
            #if(length_lb_o == grid_length and ):
                self.Rx[topY:bottomY+1,leftX:rightX+1]= self.label_config_dict[(label,config)]['Rx']
                self.Ry[topY:bottomY+1,leftX:rightX+1]= self.label_config_dict[(label,config)]['Ry']
                self.Rz[topY:bottomY+1,leftX:rightX+1]= self.label_config_dict[(label,config)]['Rz']
                self.C[topY:bottomY+1,leftX:rightX+1]= self.label_config_dict[(label,config)]['Capacitance']
                self.I[topY:bottomY+1,leftX:rightX+1]= power + self.label_config_dict[(label,config)]['I']
                #print("PRACHIIIIIII",self.label_config_dict[(label,config)]['I'])
                self.Lock[topY:bottomY+1,leftX:rightX+1] +=1
                #print(self.g2bmap)
                self.g2bmap[topY:bottomY+1,leftX:rightX+1]= "B"+str(block_idx)+"_1"
            #PRACHI Debug
            else:
                #self.Rx[topY+1:bottomY,leftX+1:rightX]= self.label_config_dict[(label,config)]['Rx']
                #print(self.label_config_dict[(label,config)]['Rx'])
                #sys.exit(2)
                #self.Ry[topY+1:bottomY,leftX+1:rightX]= self.label_config_dict[(label,config)]['Ry']
                #self.Rz[topY+1:bottomY,leftX+1:rightX]= self.label_config_dict[(label,config)]['Rz']
                #self.C[topY+1:bottomY,leftX+1:rightX]= self.label_config_dict[(label,config)]['Capacitance']
                #self.I[topY+1:bottomY,leftX+1:rightX]= power + self.label_config_dict[(label,config)]['I']
                #print("PRACHIIIIIII",self.label_config_dict[(label,config)]['I'])
                #self.Lock[topY+1:bottomY,leftX+1:rightX] +=1
                #print(self.g2bmap)
                #self.g2bmap[topY+1:bottomY,leftX+1:rightX]= "B"+str(block_idx)+"_1"
                #self.g2bmap[topY+1:bottomY,leftX+1:rightX]= np.core.defchararray.add(self.g2bmap[topY+1:bottomY,leftX+1:rightX],"B"+str(block_idx)+"_1 ")
                gridArea= grid_length*grid_width
                lb_o = np.round(length_lb_o * width_lb_o / (area),8)
                rb_o = np.round(length_rb_o * width_rb_o / (area),8)
                lt_o = np.round(length_lt_o *  width_lt_o / (area),8)
                rt_o = np.round(length_rt_o * width_rt_o / (area),8)
                #print("length_lb_o, length_rb_o, width_lb_o, width_lt_o: ",length_lb_o, length_rb_o, width_lb_o, width_lt_o)
                #if(block_idx==4):
                #    print("lb_o, rb_o, lt_o, rt_o: ",lb_o, rb_o, lt_o, rt_o)
                #    sys.exit(2)

                #rounds below were originially 2
                left_edge_cells_o = round(length_lb_o / grid_length,8)
                right_edge_cells_o = round(length_rb_o / grid_length,8)
                top_edge_cells_o = round(width_lt_o /grid_width,8)
                bottom_edge_cells_o = round(width_lb_o / grid_width,8)
                #if(block_idx==4):
                    #print(bottom_edge_cells_o)
                    #sys.exit(2)
                edge_cells_o = {'lb_o':lb_o,'rb_o':rb_o,'lt_o':lt_o,'rt_o':rt_o,'left_edge_cells_o':left_edge_cells_o, 'right_edge_cells_o':right_edge_cells_o, 'top_edge_cells_o':top_edge_cells_o, 'bottom_edge_cells_o':bottom_edge_cells_o}
                #print(block_idx,edge_cells_o)
                #if(block_idx==4):
                #    sys.exit(2)
                

                #print("left_edge_cells_o,right_edge_cells_o,top_edge_cells_o,bottom_edge_cells_o",left_edge_cells_o,right_edge_cells_o,top_edge_cells_o,bottom_edge_cells_o)
                mask = np.ones((bottomY - topY + 1, rightX - leftX + 1))
                #print(mask.shape)
                #if(block_idx==2):
                #    print(bottomY, topY, rightX, leftX)
                #if(block_idx==4):
                #    sys.exit(0)
                mask[:,0] = left_edge_cells_o
                mask[:,-1] = right_edge_cells_o
                mask[0,:] = top_edge_cells_o
                mask[-1,:] = bottom_edge_cells_o 
                mask[0,0] = lt_o
                mask[0,-1] = rt_o
                mask[-1,-1] = rb_o
                mask[-1,0] = lb_o 
                ##Values for boundary cells:
                #print(mask)
                #Left boundary
                #inf_mask = (self.Rx != 0)
                #print(inf_mask)
                #inf_mask = (self.Ry != 0)
                #print(inf_mask)
                #inf_mask = (self.Rz != 0)
                #print(inf_mask)
                #sys.exit(2)
                """
                if(self.label_mode_dict[label]=='single'):
                    a = self.Rx[topY:bottomY+1,leftX:rightX+1]
                    a = np.reciprocal(a, where = a !=0, out = np.zeros_like(a))
                    self.Rx[topY:bottomY+1,leftX:rightX+1]= np.reciprocal( a +  mask * (1/self.label_config_dict[(label,config)]['Rx']))

                    a = self.Ry[topY:bottomY+1,leftX:rightX+1]
                    a = np.reciprocal(a, where = a !=0, out = np.zeros_like(a))
                    self.Ry[topY:bottomY+1,leftX:rightX+1]= np.reciprocal( a +  mask * (1/self.label_config_dict[(label,config)]['Ry']))

                    a = self.Rz[topY:bottomY+1,leftX:rightX+1]
                    a = np.reciprocal(a, where = a !=0, out = np.zeros_like(a))
                    self.Rz[topY:bottomY+1,leftX:rightX+1]= np.reciprocal( a +  mask * (1/self.label_config_dict[(label,config)]['Rz']))

                    self.I[topY:bottomY+1,leftX:rightX+1] += mask * (power + self.label_config_dict[(label,config)]['I'])
                    self.Lock[topY:bottomY+1,leftX:rightX+1] += mask

                elif(self.label_mode_dict[label]=='matrix'):
                    self.I[topY:bottomY+1,leftX:rightX+1] += mask * (power + self.label_config_dict[(label,config)]['I'])
                    self.Lock[topY:bottomY+1,leftX:rightX+1] += mask

                        #self.C[topY:bottomY+1,leftX:rightX+1]= 1
                        #if(block_idx==4):
                         #   print(self.Rx)
                         #   print(self.Ry)
                         #   print(self.Rz)
                         #   print(self.I)
                         #   sys.exit(2)
            
                #print(self.g2bmap)
                
                """ Original (more recent than OLD (below)
                for key,val in edge_cells_o.items():
                    if(key=='lt_o'):
                        i1,i2,j1,j2=[topY,topY+1,leftX,leftX+1]
                    elif(key=='rt_o'):
                        i1,i2,j1,j2=[topY,topY+1,rightX,rightX+1]
                    elif(key=='lb_o'):
                        i1,i2,j1,j2=[bottomY,bottomY+1,leftX,leftX+1]
                    elif(key=='rb_o'):
                        i1,i2,j1,j2=[bottomY,bottomY+1,rightX,rightX+1]
                    elif(key=='left_edge_cells_o'):
                        i1,i2,j1,j2=[topY+1,bottomY,leftX,leftX+1]
                    elif(key=='right_edge_cells_o'):
                        i1,i2,j1,j2=[topY+1,bottomY,rightX,rightX+1]
                    elif(key=='top_edge_cells_o'):
                        i1,i2,j1,j2=[topY,topY+1,leftX+1,rightX]
                    elif(key=='bottom_edge_cells_o'):
                        i1,i2,j1,j2=[bottomY,bottomY+1,leftX+1,rightX]

                    if (val >= 0.95): #OCCUPANCY_THRESHOLD=0.95
                        self.Lock[i1:i2,j1:j2] = 1
                        self.Rx[i1:i2,j1:j2]= self.label_config_dict[(label,config)]['Rx']
                        self.Ry[i1:i2,j1:j2]= self.label_config_dict[(label,config)]['Ry']
                        self.Rz[i1:i2,j1:j2]= self.label_config_dict[(label,config)]['Rz']
                        self.C[i1:i2,j1:j2]= self.label_config_dict[(label,config)]['Capacitance']
                        #self.I[i1:i2,j1:j2]= np.round(val* (power + self.label_config_dict[(label,config)]['I']),6)
                        self.I[i1:i2,j1:j2]= val* (power + self.label_config_dict[(label,config)]['I'])
                        self.g2bmap[i1:i2,j1:j2]="B"+str(block_idx)+"_1"
                    elif (val > 0):
                        print("val:",val,"..Sharing Threshold!!!!....")
                        self.Rx[i1:i2,j1:j2] =  np.reciprocal(np.reciprocal(self.Rx[i1:i2,j1:j2]) + (val * 
                            1/self.label_config_dict[(label,config)]['Rx']))
                        self.Ry[i1:i2,j1:j2] =  np.reciprocal(np.reciprocal(self.Ry[i1:i2,j1:j2]) + (val * 
                            1/self.label_config_dict[(label,config)]['Ry']))
                        self.Rz[i1:i2,j1:j2] =  np.reciprocal(np.reciprocal(self.Rz[i1:i2,j1:j2]) + (val * 
                            1/self.label_config_dict[(label,config)]['Rz']))
                        self.C[i1:i2,j1:j2] += val * self.label_config_dict[(label,config)]['Capacitance']
                        self.I[i1:i2,j1:j2] +=  val * (power + self.label_config_dict[(label,config)]['I'])
                        self.g2bmap[i1:i2,j1:j2]="B"+str(block_idx)+"_"+str(val)
                """




                """OLD

                if (left_edge_cells_o >= 0.95):
                    self.Lock[topY+1:bottomY,leftX] = 1
                    self.Rx[topY+1:bottomY,leftX]= self.label_config_dict[(label,config)]['Rx']
                    self.Ry[topY+1:bottomY,leftX]= self.label_config_dict[(label,config)]['Ry']
                    self.Rz[topY+1:bottomY,leftX]= self.label_config_dict[(label,config)]['Rz']
                    self.C[topY+1:bottomY,leftX]= self.label_config_dict[(label,config)]['Capacitance']
                    self.I[topY+1:bottomY,leftX]= power*left_edge_cells_o, self.label_config_dict[(label,config)]['I']
                    self.g2bmap[topY+1:bottomY,leftX]="B"+str(block_idx)+"_1"
                    #self.g2bmap[topY+1:bottomY,leftX+1:rightX]= np.core.defchararray.add(self.g2bmap[topY+1:bottomY,leftX+1:rightX],"B"+str(block_idx)+"_1 ")
                elif (self.Lock[topY+1:bottomY,leftX] != 1):
                    self.Rx[topY+1:bottomY,leftX] =  np.reciprocal(np.reciprocal(self.Rx[topY+1:bottomY,leftX]) + (left_edge_cells_o * 
                        1/self.label_config_dict[(label,config)]['Rx']))
                    self.Ry[topY+1:bottomY,leftX] =  np.reciprocal(np.reciprocal(self.Ry[topY+1:bottomY,leftX]) + (left_edge_cells_o * 
                        1/self.label_config_dict[(label,config)]['Ry']))
                    self.Rz[topY+1:bottomY,leftX] =  np.reciprocal(np.reciprocal(self.Rz[topY+1:bottomY,leftX]) + (left_edge_cells_o * 
                        1/self.label_config_dict[(label,config)]['Rz']))
                    self.C[topY+1:bottomY,leftX] += left_edge_cells_o * self.label_config_dict[(label,config)]['Capacitance']
                    self.I[topY+1:bottomY,leftX] +=  left_edge_cells_o * (power + self.label_config_dict[(label,config)]['I'])
                    self.g2bmap[topY+1:bottomY,leftX]="B"+str(block_idx)+"_"+str(left_edge_cells_o)

                """ 
        #elif(self.label_mode_dict[label]=='matrix' and PowerDensity != 0):
        #    print("matrix mode in evaluate RC with non-zero power density")
        #    self.I[topY:bottomY+1,leftX:rightX+1] += power

        #    self.Lock[topY:bottomY+1,leftX:rightX+1] +=1
            #print(self.g2bmap)
            #self.g2bmap[topY:bottomY+1,leftX:rightX+1]= "B"+str(block_idx)+"_1"

        #self.Occupancy,[leftX+1:rightX,bottomY+1:topY],1)
        #print(self.Rx.shape)
        #Occupancy[leftX+1:rightX,bottomY+1:topY]=1
        return 

    def addLibraries(self, lib_dict):
        self.lib_dict=lib_dict
        return

    """
    def evaluateGridProperties(self,model):
        for key_label,val_library in model.lib_dict.items():
            print(key_label,val_library)
            exec("import %s as Lib%s" % (val_library,key_label))
            print globals()
            print locals()
        print(LibSi)
        
        for (label,cfile) in model.label_config_dict.keys():
            print (label,cfile)
            if(label=='Si'):
                model.label_config_dict[(label,cfile)]=LibSi.defineGridProperties(1,2,3,4,config._sections['Si'])
                print(model.label_config_dict[(label,cfile)])
            if(label=='TwoPhase'):
                model.label_config_dict[(label,cfile)]=LibTwoPhase.defineGridProperties(1,2,3,4,config._sections['TwoPhase'])
                print(model.label_config_dict[(label,cfile)])
            if(label=='TIM'):
                model.label_config_dict[(label,cfile)]=LibTIM.defineGridProperties(1,2,3,4,config._sections['TIM'])
                print(model.label_config_dict[(label,cfile)])
        return
    """
    def grid2blockmap(self):
        pass

        
