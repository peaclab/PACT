import sys
import numpy as np
import pandas as pd
import math
#import Solid as LibSi
#import Solid as LibCu
#import Solid as LibNoPackage
import Solid as LibSolid
import Liquid as LibLiquid
import HybridWick_LookupTable as LibHybridWick
#import TwoPhaseVC as LibTwoPhase
import sys

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
        self.Conv = np.zeros((int(self.grid_dict['rows']),int(self.grid_dict['cols'])))
        self.others = {}
        #self.I = np.zeros((int(self.grid_dict['rows']),int(self.grid_dict['cols'])))
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
        self.I = np.zeros((int(chipstack.num_ptrace_lines),int(self.grid_dict['rows']),int(self.grid_dict['cols'])))
        #print(self.I.shape,self.Rx.shape)
        self.length = round(chipstack.length,20)
        self.width = round(chipstack.width,20)
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
        print(f"chipstack length {chipStack.length}")
        print(f"chipstack width {chipStack.width}")
	#Zihao modify it to 20 decimal points
        grid_length = round(chipStack.length/cols,40)
        self.grid_width = round(chipStack.width/rows,40)
        self.grid_length = round(chipStack.length/cols,40)
        grid_width = round(chipStack.width/rows,40)
        print(rows,"x",cols,"; grid_length and width:",grid_length,grid_width)
        if (round(grid_length*cols,20) != chipStack.length) or (round(grid_width*rows,20) != chipStack.width):
            print("grid_length*cols:",grid_length*cols,"chipStacl.length:",chipStack.length,\
                "grid_width*rows:",grid_width*rows,"chipStack.width:",chipStack.width)
            print("Unifrom grids cannot be formed. Choose a multiple of 2 or 5 as rows and columns")
           # sys.exit(2)
        #self.Layers_data.apply(self.disp, args=(5,6))
        layers = chipStack.Layers_data
        a = [chipStack.Layers_data.loc[i].flp_df['X'] for i in layers.index]
        #print(type(a))
        chipStack.Layers_data = chipStack.Layers_data.apply(self.calculate_boundary_grids, args=(grid_length, grid_width,chipStack.num_layers))
        #print("CreateBoundaryGrids successfully completeed")
        return chipStack

    def disp(self,x,a,b):
        print(a,b,type(x))
        print("1")
        print(x.flp_df['X'])
        print("2")
        return


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
        self.Conv = np.zeros(self.Conv.shape)
        #print(label_ll)

        self.power_densities = 0
        if(layer_obj.layer_num < num_layers-1):
            ####FIND BOUNDARIES###
            #flp_df['grid_left_x']= flp_df.apply(lambda x: math.floor(round(float(x.X)/grid_width,8)), axis=1)
            X_vals = np.round(flp_df['X'].values,20)
            Y_vals = np.round(flp_df['Y'].values,20)
            length_vals = np.round(flp_df['Length (m)'].values,20)
            height_vals = np.round(flp_df['Width (m)'].values,20)
            label_vals = flp_df['Label'].values
            pd_vector_shape = (length_vals * height_vals).shape[0]
            #print(pd_vector_shape)
            PowerDensities = flp_df['Power'].values / (length_vals * height_vals)
            #print(type(PowerDensities), PowerDensities.shape, PowerDensities)
            ptrace_df = flp_df.filter(regex='^Power',axis=1)
            #print(ptrace_df)
            ptrace_mat = ptrace_df.values
            #print(ptrace_mat.shape,ptrace_mat)
            layer_obj.add_power_densities(ptrace_mat / (length_vals * height_vals).reshape((pd_vector_shape,1)))
            self.power_densities = layer_obj.power_densities

            #data / vector.reshape((3,1))
            #print(self.power_densities)
            #print("Works!")
            #sys.exit(0)

            flp_df['grid_left_x']= flp_df.apply(lambda x: math.floor(round(float(x.X)/grid_length,40)), axis=1)
            flp_df['grid_bottom_y']= flp_df.apply(lambda x: int(self.grid_dict['rows']) - math.floor(round(float(x.Y)/grid_width,40)) - 1,axis=1)
            temp_x = flp_df.apply(lambda x: (round(float(x.X),20)+round(float(x['Length (m)']),20))/grid_length, axis=1).round(40) #Panda Series
            temp_y = flp_df.apply(lambda x: (round(float(x.Y),20)+round(float(x['Width (m)']),20))/grid_width, axis=1).round(40)
            flp_df['grid_right_x'] = temp_x.apply(lambda x : math.floor(x) if math.ceil(x) != math.floor(x) else math.ceil(x) - 1 )
            flp_df['grid_top_y'] = temp_y.apply(lambda x : int(self.grid_dict['rows']) -  math.ceil(x) if math.ceil(x) != math.floor(x) else int(self.grid_dict['rows']) -math.floor(x))

            #print(flp_df)

            #left_x = set(flp_df['grid_left_x'].values)
            #right_x = set(flp_df['grid_right_x'].values)
            #top_y = set(flp_df['grid_top_y'].values)
            #bottom_y = set(flp_df['grid_bottom_y'].values)
            #print(bool(left_x & right_x))
            #print(bool(top_y & bottom_y))

            #if(layer_obj.layer_num == 0):
            #    sys.exit(2)
            #layer_obj.flp_df = flp_df
            ####debug####
            #if (layer_obj.layer_num== 0):
            #    print(PowerDensities)
            ############

            left_x_vals = np.round(flp_df['grid_left_x'].values,40)
            right_x_vals = np.round(flp_df['grid_right_x'].values,40)
            top_y_vals = np.round(flp_df['grid_top_y'].values,40)
            bottom_y_vals = np.round(flp_df['grid_bottom_y'].values,40)
            label_config_arr = list(zip(label_vals, flp_df['ConfigFile'].values))
            #listCoords=list(zip(grid_left_x,grid_right_x,grid_bottom_y,grid_top_y))
            #listCoords1=list(zip(left_x_vals,right_x_vals,bottom_y_vals,top_y_vals))

            #print("*******************listCoords*************8: match?", listCoords1 == listCoords)
            #print(label_config_arr)
            #print(listCoords)
            #block_counter=np.arange(grid_left_x.size)
            block_counter=np.arange(left_x_vals.size)
            #print(block_counter)
            #print(self.label_config_dict.keys())
            #sys.exit(2)
            for (label,cfile) in self.label_config_dict.keys() :
                #print (label,cfile)
                if(label in label_ll and self.label_mode_dict[label]=='single'):
                    if(label=='Si'):
                        #print("1")
                        #self.label_config_dict[(label,cfile)]=LibSi.defineGridProperties(grid_length,grid_width,thickness,self.config._sections['Si'])
                        self.label_config_dict[(label,cfile)]=LibSolid.defineGridProperties(grid_length,grid_width,thickness,self.config._sections['Si'])
                        #print(self.label_config_dict[(label,cfile)])
                        #sys.exit(0)
                    elif(label=='TwoPhaseVC'):
                        #print("3")
                        self.label_config_dict[(label,cfile)]=LibTwoPhase.defineGridProperties(grid_length,grid_width,thickness,self.config._sections['TwoPhaseVC'])
                        #print(label_config_dict[(label,cfile)])
                    elif(label=='Cu'):
                        #print("3")
                        #self.label_config_dict[(label,cfile)]=LibCu.defineGridProperties(grid_length,grid_width,thickness,self.config._sections['Cu'])
                        self.label_config_dict[(label,cfile)]=LibSolid.defineGridProperties(grid_length,grid_width,thickness,self.config._sections['Cu'])
                        #print(self.label_config_dict[(label,cfile)])
                    #Zihao add this for Mono3D simulation
                    elif(label=='Diel'):
                        #print("3")
                        #self.label_config_dict[(label,cfile)]=LibCu.defineGridProperties(grid_length,grid_width,thickness,self.config._sections['Cu'])
                        self.label_config_dict[(label,cfile)]=LibSolid.defineGridProperties(grid_length,grid_width,thickness,self.config._sections['Diel'])
                        #print(self.label_config_dict[(label,cfile)])
                    elif(label=='Metal'):
                        #print("3")
                        #self.label_config_dict[(label,cfile)]=LibCu.defineGridProperties(grid_length,grid_width,thickness,self.config._sections['Cu'])
                        self.label_config_dict[(label,cfile)]=LibSolid.defineGridProperties(grid_length,grid_width,thickness,self.config._sections['Metal'])
                    elif(label=='Metal7_8'):
                        #print("3")
                        #self.label_config_dict[(label,cfile)]=LibCu.defineGridProperties(grid_length,grid_width,thickness,self.config._sections['Cu'])
                        self.label_config_dict[(label,cfile)]=LibSolid.defineGridProperties(grid_length,grid_width,thickness,self.config._sections['Metal7_8'])
                    elif(label=='Liq'):
                        #print("3")
                        #self.label_config_dict[(label,cfile)]=LibCu.defineGridProperties(grid_length,grid_width,thickness,self.config._sections['Cu'])
                        self.label_config_dict[(label,cfile)]=LibLiquid.defineGridProperties(grid_length,grid_width,thickness,self.config._sections['Liq'])
                    elif(label=='NoPackage'):
                        #print("4")
                        #self.label_config_dict[(label,cfile)]=LibNoPackage.defineGridProperties(grid_length,grid_width,thickness,self.config._sections['NoPackage'])
                        self.label_config_dict[(label,cfile)]=LibSolid.defineGridProperties(grid_length,grid_width,thickness,self.config._sections['NoPackage'])
                        #print(self.label_config_dict[(label,cfile)])
    
                    for key in self.label_config_dict[(label,cfile)].keys():
                        if key.endswith("_constant"):
                            layer_obj.update_others_constants(key, self.label_config_dict[(label,cfile)][key])
			
                elif(label in label_ll and self.label_mode_dict[label]=='matrix'):
                    #print(label,self.label_mode_dict[label],label_ll)
                    #if(label=='HybridWick'):
                    #    print("DEUGPRACHI")
                    #sys.exit(2)
                    if(label=='HybridWick'):
                        #grid_labels = np.full((int(self.grid_dict['rows']),int(self.grid_dict['cols'])),"HybridWick")
                        #print("Matrix", label)
                        if (type(self.initTemp)==float):
                            grid_temperatures = np.full((rows,cols),float(self.initTemp))
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
                    self.Conv += self.label_config_dict[(label,cfile)]['Conv']
                    break
                        #self.g2bmap[topY+1:bottomY,leftX+1:rightX]= "B"+str(block_idx)+"_1"

                        #sys.exit(2)
            #for key in self.label_config_dict[(label,cfile)].keys():
            #    if key.endswith("_constant"):
            #        layer_obj.update_others_constants(val, self.others[val])
            #    else:
            #        print(val, "does not end with")
            #print(type(self.label_config_dict[(label,cfile)]))

            #print(flp_df.loc[780])
                #print("hey there layer",layer_obj.layer_num)
                #for x in label_ll:
                #    print('single' in self.label_mode_dict[x])
            #print("*************************************Zihao:",self.C)
		
            self.vector_evaluateRC(X_vals,Y_vals,length_vals, height_vals, PowerDensities,left_x_vals,right_x_vals,bottom_y_vals,top_y_vals,label_vals,flp_df['ConfigFile'].values,block_counter,grid_length,grid_width, layer_obj.layer_num)

                #sys.exit(0)
            #print("Lateral Heat Flow for layer",layer_obj.layer_num,"is",layer_obj.LateralHeatFlow)
            if(str(layer_obj.LateralHeatFlow) == 'True'):
                #print("Lateral Heat Flow is TRUE for layer",layer_obj.layer_num)
                layer_obj.Rx = self.Rx
                layer_obj.Ry = self.Ry
            else:
                #print("Lateral Heat Flow is FALSE for layer",layer_obj.layer_num)
                layer_obj.Rx = np.ones(self.Rx.shape) * math.inf
                layer_obj.Ry = np.ones(self.Rx.shape) * math.inf

            layer_obj.Rz = self.Rz
            layer_obj.C = self.C
            layer_obj.Conv = self.Conv
            #print("others:",self.others)
#Zihao 
            layer_obj.I = self.I
            layer_obj.Lock = self.Lock
            layer_obj.g2bmap = self.g2bmap

            if(layer_obj.layer_num == num_layers-2):
                self.noPackage_grid_left_x = flp_df['grid_left_x']
                self.noPackage_grid_right_x = flp_df['grid_right_x']
                self.noPackage_grid_bottom_y = flp_df['grid_bottom_y']
                self.noPackage_grid_top_y = flp_df['grid_top_y']
                #self.noPackage_grid_left_x = grid_left_x
                #self.noPackage_grid_right_x = grid_right_x
                #self.noPackage_grid_bottom_y = grid_bottom_y
                #self.noPackage_grid_top_y = grid_top_y
                #self.noPackage_g2bmap = self.g2bmap
                #self.noPackage_g2bmap = np.full((rows,cols),"NoPackage"))
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
                        #NoPackage_info=LibNoPackage.defineGridProperties(grid_length,grid_width,thickness,self.config._sections['NoPackage'])
                        NoPackage_info=LibSolid.defineGridProperties(grid_length,grid_width,thickness,self.config._sections['NoPackage'])
                        break
            #layer_obj.Rx = np.full((int(self.grid_dict['rows']),int(self.grid_dict['cols'])),np.inf)
            #layer_obj.Ry = np.full((int(self.grid_dict['rows']),int(self.grid_dict['cols'])),np.inf)

            #print(layer_obj.LateralHeatFlow)
            if (str(layer_obj.LateralHeatFlow) == 'True'):
                #print("noPackage layer has lateral TRUE")
                layer_obj.Rx = np.ones(self.Rx.shape) * NoPackage_info['Rx']
                layer_obj.Ry = np.ones(self.Ry.shape) * NoPackage_info['Ry']
                layer_obj.C = np.ones(self.C.shape) * NoPackage_info['Capacitance']
                #layer_obj.Ry = self.noPackage_Ry
            else:
                #print("noPackage layer has lateral FALSE")
                layer_obj.Rx = np.ones(self.Rx.shape) * math.inf
                layer_obj.Ry = np.ones(self.Ry.shape) * math.inf
                layer_obj.C = np.ones(self.C.shape) * NoPackage_info['Capacitance']
            layer_obj.Conv = np.ones(self.Conv.shape) * NoPackage_info['Conv']



            #print(layer_obj.VerticalHeatFlow)
            if (str(layer_obj.VerticalHeatFlow) == 'True'):
                #print("noPackage layer has vertical TRUE")
                #r_amb = round(1/(float(self.config.get('NoPackage','htc'))*grid_length*grid_width) + NoPackage_info['Rz'],6)
                r_amb = 1/(float(self.config.get('NoPackage','htc'))*grid_length*grid_width) + NoPackage_info['Rz']
                #r_amb = layer_obj.Rz + np.full((int(self.grid_dict['rows']),int(self.grid_dict['cols'])),r_amb)
            else:
                #print("noPackage layer has vertical FALSE (i.e., direct connection to ambient")
                #r_amb = round(1/(float(self.config.get('NoPackage','htc'))*grid_length*grid_width),6)
                r_amb = 1/(float(self.config.get('NoPackage','htc'))*grid_length*grid_width)
            #print("Rz",layer_obj.Rz)

            #layer_obj.Rx = self.noPackage_Rx
            #layer_obj.Ry = self.noPackage_Ry
            #print("noPackage:")
            
            #r_amb = 1/(float(self.config.get('NoPackage','htc'))*grid_length*grid_width)
            #print("r_amb =", r_amb)
            layer_obj.Rz = np.full((int(self.grid_dict['rows']),int(self.grid_dict['cols'])),r_amb)
            #print("Rz",layer_obj.Rz)
            #layer_obj.C = np.ones((int(self.grid_dict['rows']),int(self.grid_dict['cols'])),dtype=float)
            val, unit = self.config.get('Init','ambient').split()
            if (unit=='K' or unit == 'Kelvin'):
                val = round(float(val),6)
            elif (unit=='C' or 'Celsius'):
                val = round(float(val),6) + 273.15
            #P_noPackage = round(val/r_amb,6)
            P_noPackage = val/r_amb
            #print("PRACHI: (NoPackage) r_amb and Power(per_grid) for dummy layer are",r_amb,P_noPackage)
            #layer_obj.I = np.full((int(self.grid_dict['rows']),int(self.grid_dict['cols'])),P_noPackage)
            #PRACHI: check the below statement
            layer_obj.I = np.full((self.I.shape),P_noPackage)
            layer_obj.Lock = self.noPackage_Lock
            #layer_obj.g2bmap = self.noPackage_g2bmap
            layer_obj.g2bmap = np.full((rows,cols),"NoPackage")
            layer_obj.flp_df = flp_df
            layer_obj.r_amb = r_amb

        #np.set_printoptions(threshold=np.inf)
        #####Undo below prints if you want more detailed insights
        #print("Layer",layer_obj.layer_num)
        #print("Rx",np.max(layer_obj.Rx), np.min(layer_obj.Rx),layer_obj.Rx)
        #print("Ry",np.max(layer_obj.Ry), np.min(layer_obj.Ry),layer_obj.Ry)
        #print("Rz",np.max(layer_obj.Rz), np.min(layer_obj.Rz),layer_obj.Rz)
        #print("C",layer_obj.C)
        #print("I",layer_obj.I)
        #if(layer_obj.layer_num == 1):
        #    sys.exit(2)

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
    def evaluateRC(self, X,Y,length,width, PowerDensity,leftX,rightX,bottomY,topY,label,config,block_idx,grid_length, grid_width, layer_num):
        ##3Undo below two comments
        #print("power:",power)
        #print (X,Y,length, width,PowerDensity,leftX,rightX,bottomY,topY,label,config,block_idx)

        #print("\nPRACHI Block",block_idx)
        #print ("X,Y,length, width,PowerDensity,leftX,rightX,bottomY,topY,label,config,block_idx:")
        #print (X,Y,length, width,PowerDensity,leftX,rightX,bottomY,topY,label,config,block_idx)
        if(self.label_mode_dict[label]=='matrix' and PowerDensity == 0):
            #print("matrix mode in evaluate RC with zero power density...EXITING")
            self.Lock[topY:bottomY+1,leftX:rightX+1] +=1
            return

        area = grid_length * grid_width
        #power = round(PowerDensity * area,6)
        power = PowerDensity * area
        #print(self.power_densities)
        power_mat = self.power_densities[block_idx] * area
        
        power_mat_reshape = np.reshape(power_mat, (len(power_mat),1,1), order='C')
        #print(type(power_mat),power_mat[0],power_mat)
        #Zihao Debug
        #print(power_mat)
        #print(power_mat_reshape)
        #if block_idx == 4:
        #    sys.exit(0)
        mode = self.label_mode_dict[label]
        length_lb_o = round((leftX+1)*grid_length - X,40)
        length_rb_o =  round((X+length) - (rightX)*grid_length,40)
        length_lt_o = length_lb_o
        length_rt_o = length_rb_o
        width_lb_o = round((int(self.grid_dict['rows']) - bottomY )*grid_width  - Y,40)
        width_rb_o = width_lb_o
        width_lt_o = round((topY + 1) * grid_width  - (self.width - Y - width),40)
        width_rt_o = width_lt_o

        if((length_lb_o == length_rb_o == grid_length) and (width_lb_o == width_lt_o == grid_width)):
            #print("Block",block_idx,"is not sharing its boundaries")
            #self.I[topY:bottomY+1,leftX:rightX+1] += power #+ self.label_config_dict[(label,config)]['I']
            #print(topY,bottomY,leftX,rightX)
            #print("PRACHI: Reshape:",power_mat_reshape.shape,self.I[:,topY:bottomY+1,leftX:rightX+1].shape)
            #sys.exit(0)
            self.I[:,topY:bottomY+1,leftX:rightX+1] +=  power_mat_reshape #power_mat[:,np.newaxis]  #+ self.label_config_dict[(label,config)]['I']
            #print(self.I.shape, self.I)
            #print(self.I[0])
            #sys.exit(0)
            self.Lock[topY:bottomY+1,leftX:rightX+1] +=1
            self.g2bmap[topY:bottomY+1,leftX:rightX+1]= label
            if (mode == 'single'):
                #self.Rz[topY:bottomY+1,leftX:rightX+1]= np.reciprocal( a +  mask * (1/self.label_config_dict[(label,config)]['Rz']))
                self.Rx[topY:bottomY+1,leftX:rightX+1]= self.label_config_dict[(label,config)]['Rx']
                self.Ry[topY:bottomY+1,leftX:rightX+1]= self.label_config_dict[(label,config)]['Ry']
                self.Rz[topY:bottomY+1,leftX:rightX+1]= self.label_config_dict[(label,config)]['Rz']
                self.C[topY:bottomY+1,leftX:rightX+1]= self.label_config_dict[(label,config)]['Capacitance']
              #  print(self.C)
              #  sys.exit(0)

            return
            #self.g2bmap[topY:bottomY+1,leftX:rightX+1]= "B"+str(block_idx)+"_1"
        else:
            #print("Boundary sharing for block",block_idx,"...Shouldn't be the case")
            #print("Boundary sharing for block",block_idx)
            lb_o = np.round(length_lb_o * width_lb_o / (area),40)
            rb_o = np.round(length_rb_o * width_rb_o / (area),40)
            lt_o = np.round(length_lt_o *  width_lt_o / (area),40)
            rt_o = np.round(length_rt_o * width_rt_o / (area),40)
            left_edge_cells_o = round(length_lb_o / grid_length,40)
            right_edge_cells_o = round(length_rb_o / grid_length,40)
            top_edge_cells_o = round(width_lt_o /grid_width,40)
            bottom_edge_cells_o = round(width_lb_o / grid_width,40)
            edge_cells_o = {'lb_o':lb_o,'rb_o':rb_o,'lt_o':lt_o,'rt_o':rt_o,'left_edge_cells_o':left_edge_cells_o, 'right_edge_cells_o':right_edge_cells_o, 'top_edge_cells_o':top_edge_cells_o, 'bottom_edge_cells_o':bottom_edge_cells_o}
            #print(edge_cells_o)

            #print(self.I.shape,self.I.shape[0])

            mask = np.ones((bottomY - topY + 1, rightX - leftX + 1))
            mask[:,0] = left_edge_cells_o
            mask[:,-1] = right_edge_cells_o
            mask[0,:] = top_edge_cells_o
            mask[-1,:] = bottom_edge_cells_o 
            mask[0,0] = lt_o
            mask[0,-1] = rt_o
            mask[-1,-1] = rb_o
            mask[-1,0] = lb_o 
            conditions = [mask >= 0.9]
            choice = [label]
            #mask2[1:2,2:3] = np.select([mask[1:2,2:3]>= 0.5],["Liq"])
            self.g2bmap[topY:bottomY+1,leftX:rightX+1] = np.select(conditions, choice)

            mask_I = np.ones((self.I.shape[0],bottomY - topY + 1, rightX - leftX + 1))
            mask_I[:,:,0] = left_edge_cells_o
            mask_I[:,:,-1] = right_edge_cells_o
            mask_I[:,0,:] = top_edge_cells_o
            mask_I[:,-1,:] = bottom_edge_cells_o 
            mask_I[:,0,0] = lt_o
            mask_I[:,0,-1] = rt_o
            mask_I[:,-1,-1] = rb_o
            mask_I[:,-1,0] = lb_o 

            np.set_printoptions(threshold=np.inf)
            #print(mask)
            #if block_idx==1:
            #    print(mask_I)
                #sys.exit(0)
            # print(mask_I)
            #self.I[topY:bottomY+1,leftX:rightX+1] += mask * power
            #print(self.I[:topY:bottomY+1,leftX:rightX+1])
            #print("I's shape:",self.I[:topY:bottomY+1,leftX:rightX+1].shape)
            #print("mask_I 'shape:",mask_I.shape,'power_mat  shape:',power_mat_reshape.shape)
            #print("product shape:",(mask_I * power_mat_reshape).shape)
            #print("power_mat_reshape block ",block_idx, ":",power_mat_reshape)
            mask_I = mask_I * power_mat_reshape
            #if block_idx==1:
                #print(mask_I)
                #sys.exit(0)
            #placeholder_mat = np.zeros_like(self.I[:,topY:bottomY+1,leftX:rightX+1])
            placeholder_mat = np.zeros_like(self.I)
            #print(placeholder_mat)
            #placeholder_mat[:mask_I.shape[0], :mask_I.shape[1], :mask_I.shape[2]] = mask_I 
            #Zihao debug:
            #print(mask_I,leftX,rightX)
            placeholder_mat[:, topY:bottomY+1,leftX:rightX+1] = mask_I 
	    
            #print(placeholder_mat)
            #a = self.I[:topY:bottomY+1,leftX:rightX+1]
            #print("placeholder shape:",placeholder_mat.shape)
            #print("I sub array shape:",(self.I[:topY:bottomY+1,leftX:rightX+1]).shape)
            #print("I sub array shape:",a.shape, bottomY,topY,rightX,leftX)
            #sys.exit(0)
            #if block_idx == 4:
            #    print("Before")
            #    print(self.I[0])
            #    print(placeholder_mat)
            #self.I[:topY:bottomY+1,leftX:rightX+1] += placeholder_mat
            self.I += placeholder_mat
            #if block_idx == 4:
            #    print("After")
            #    print(self.I[0])
            #    sys.exit(0)
            self.Lock[topY:bottomY+1,leftX:rightX+1] += mask

            if(self.label_mode_dict[label]=='single'):
                #print("single mode in evaluate RC with non-zero power density")
                a = self.Rx[topY:bottomY+1,leftX:rightX+1]
                a = np.reciprocal(a, where = a !=0, out = np.zeros_like(a))
                self.Rx[topY:bottomY+1,leftX:rightX+1]= np.reciprocal( a +  mask * (1/self.label_config_dict[(label,config)]['Rx']))

                a = self.Ry[topY:bottomY+1,leftX:rightX+1]
                a = np.reciprocal(a, where = a !=0, out = np.zeros_like(a))
                self.Ry[topY:bottomY+1,leftX:rightX+1]= np.reciprocal( a +  mask * (1/self.label_config_dict[(label,config)]['Ry']))

                a = self.Rz[topY:bottomY+1,leftX:rightX+1]
                a = np.reciprocal(a, where = a !=0, out = np.zeros_like(a))
                self.Rz[topY:bottomY+1,leftX:rightX+1]= np.reciprocal( a +  mask * (1/self.label_config_dict[(label,config)]['Rz']))
                #self.C[topY:bottomY+1,leftX:rightX+1]= self.label_config_dict[(label,config)]['Capacitance']
                #Prachi: Zihao, maybe you should do this
                self.C[topY:bottomY+1,leftX:rightX+1] += mask * self.label_config_dict[(label,config)]['Capacitance']

                #Prachi: Zihao, check the formula
                self.Conv[topY:bottomY+1,leftX:rightX+1] += mask * self.label_config_dict[(label,config)]['Conv']
            ###DEBUG
            """
            if(block_idx==4):
                print(self.Rx)
                print(self.Ry)
                print(self.Rz)
                print(self.I)
                sys.exit(2)
            """
            return
        return 

    def addLibraries(self, lib_dict):
        self.lib_dict=lib_dict
        return

    #Should also send steady file as an optional argument
    def grid2block(self,chipStack,gridTemperatures,block_mode,transient=False):
        #chipStack.Layers_data = chipStack.Layers_data.apply(self.calculate_block_temperatures, \
         #   args=(gridTemperatures,block_mode,transient))
        chipStack.Layers_data.apply(self.calculate_block_temperatures, \
            args=(gridTemperatures,block_mode,transient))
        return

    def calculate_block_temperatures(self,layer_obj,gridTemperatures,block_mode,transient):
        layer_num = layer_obj.layer_num
        flp = layer_obj.flp_df
        #block_mode = 'avg'
        if(block_mode == 'max'):
            #layer_obj.flp_df['BlockTemperature'] = flp.apply(lambda x : np.round(np.max((gridTemperatures[layer_num])\
            #    [int(x.grid_left_x):int(x.grid_right_x)+1, int(x.grid_top_y):int(x.grid_bottom_y)+1]) - 273.15,2),axis=1)
            #flp.apply(lambda x : print(np.amax((gridTemperatures[layer_num])\
            #    [int(x.grid_top_y):int(x.grid_bottom_y)+1, int(x.grid_left_x):int(x.grid_right_x)+1]) - 273.15),axis=1)
            layer_obj.flp_df['BlockTemperature'] = flp.apply(lambda x : round(np.max((gridTemperatures[layer_num])\
                [int(x.grid_top_y):int(x.grid_bottom_y)+1, int(x.grid_left_x):int(x.grid_right_x)+1]) - 273.15,3),axis=1)
        elif(block_mode == 'min'):
            layer_obj.flp_df['BlockTemperature'] = flp.apply(lambda x : round(np.min((gridTemperatures[layer_num])\
                [int(x.grid_top_y):int(x.grid_bottom_y)+1, int(x.grid_left_x):int(x.grid_right_x)+1]) - 273.15,3),axis=1)
        elif(block_mode == 'avg'):
            layer_obj.flp_df['BlockTemperature'] = flp.apply(lambda x : round(np.mean((gridTemperatures[layer_num])\
                [int(x.grid_top_y):int(x.grid_bottom_y)+1, int(x.grid_left_x):int(x.grid_right_x)+1]) - 273.15,3),axis=1)
       # print('Layer',layer_num,":\n",layer_obj.flp_df[['UnitName','BlockTemperature']])
        if transient == False:
            print(f'layer number:{layer_num}') 
            print(layer_obj.flp_df[['UnitName','BlockTemperature']])
        else:
            with(open("RC_transient_block_temp.csv","a")) as myfile:
                myfile.write(f'layer number:{layer_num}')
                pd.options.display.max_rows = 600
                myfile.write(str(layer_obj.flp_df[['UnitName','BlockTemperature']])+'\n')
        return
        

        
