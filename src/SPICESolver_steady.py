import sys
import numpy as np
import math
import os
class SPICE_steadySolver:
    def __init__(self,name,num_core,ll_solver,ambient):
        self.name = name
        self.num_core = num_core
        self.ll_solver = ll_solver
        self.ambient = ambient
        return

    def display_solver(self):
        print(self.name)
        return

    def update(self):
        self.cooData.fill(0)
        self.cooX.fill(0)
        self.cooY.fill(0)
        #print(self.dict_properties_update['update'])
        for (layer,prop) in self.dict_properties_update['update'].items():
            if(prop=='Rz'):
                #print("Before:",self.dict_properties["Rz"])
                #print("Before:",self.Rz)
                #self.Rz[layer] = self.dict_properties['Rz'][layer]
                self.dict_properties['Rz'].update(self.dict_properties_update["Rz"])
                self.Rz.update(self.dict_properties_update['Rz'])
                #print("After:",self.dict_properties["Rz"])
                #print("After:",self.Rz)
            elif(prop=='Rx'):
                self.dict_properties['Rx'].update(self.dict_properties_update["Rx"])
                self.Rx.update(self.dict_properties_update['Rx'])
                #self.Rx[layer] = self.dict_properties['Rx'][layer]
            elif(prop=='Ry'):
                self.dict_properties['Ry'].update(self.dict_properties_update["Ry"])
                self.Ry.update(self.dict_properties_update['Ry'])
                #self.Ry[layer] = self.dict_properties['Ry'][layer]
            elif(prop=='C'):
                self.dict_properties['C'].update(self.dict_properties_update["C"])
                self.C.update(self.dict_properties_update['C'])
                #self.C[layer] = self.dict_properties['C'][layer]
            elif(prop=='I'):
                self.dict_properties['I'].update(self.dict_properties_update["I"])
                self.I.update(self.dict_properties_update['I'])
                #self.I[layer] = self.dict_properties['I'][layer]
                for key,value in self.I.items():
                    self.b = np.append(self.b,value.flatten())
                self.b = np.reshape(self.b,(self.size,1))
        return

    def setup(self):
        self.nr = int(self.dict_properties['grid_rows'])
        self.nc = int(self.dict_properties['grid_cols'])
        self.nl = int(self.dict_properties['num_layers'])
        self.layerVN = self.dict_properties['layer_virtual_nodes']
        self.factorVN = self.dict_properties['factor_virtual_nodes']
        self.r_amb= self.dict_properties['r_amb']
        self.size= self.nl * self.nr * self.nc
        self.col_limit = self.nc - 1
        self.row_limit = self.nr - 1
        self.layer_limit = self.nl - 1
        #print("PRACHI1",layerVN)
        #print("PRACHI2",factorVN)
        
        #Num of non-zeros
        #each layer Five diagonal  : c*r, c*(r-1), (c-1)*r, c*(r-1), (c-1)*r
        #vertical connections      : 2*(nl-1)*nr*nc
        #sp and hs layer peripheral: 2 * 2 * (2*nr+2*nc)
        #diaganal for pkg nodes    : EXTRA
        #between pkg nodes         : 2 * 2 * 4
        #

        #print("nl nr nc",nl,nr,nc)
        #self.nnz = 5*nr*nc-2*(nr+nc)
        #self.nnz = nnz*nl
        #self.nnz = nnz + 2*(nl-1)*nr*nc
        self.nnz = self.nl * self.nr * self.nc + 2 * (self.nl-1) * self.nr * self.nc + 2 * self.nl * (self.nr-1) * \
            self.nc +  2 * self.nl * self.nr * (self.nc-1)
        self.addY={0:1,1:-1,2:-self.nc,3:self.nc,4:-self.nr*self.nc,5:self.nr*self.nc} # 0...6 correspond to [Re,Rw,Rn,Rs,Ra,Rb]
        self.prod = self.nr*self.nc
        #print("nnz:",nnz,"nnz1:",nnz1)
        #nnz = 5*nr*nc-2*(nr+nc)
        #nnz = nnz*(nl-1) + 2*(nr*nc)
        #nnz = nnz + (nl-2)*nr*nc
        #print("nnz:",nnz)
        #nnz2 = nnz + 2*(nl-1)*nr*nc

        self.cooData = np.zeros((self.nnz))
        self.cooX = np.zeros((self.nnz))
        self.cooY = np.zeros((self.nnz))
        #print(self.A)
        #shold I replace self.Rx with self.dict_properties['Rx'] in this python file?
        self.Rx = self.dict_properties['Rx']
        self.Ry = self.dict_properties['Ry']
        self.Rz = self.dict_properties['Rz']
        self.C = self.dict_properties['C']
        self.I = self.dict_properties['I']
        self.Conv = self.dict_properties['Conv']
        self.glabels = self.dict_properties['g2bmap']
        self.liq_layer = []
        for layer,label in self.glabels.items():
            if 'Liq' in label:
                self.liq_layer.append(layer)
        if 'inlet_T_constant' in self.dict_properties['others'][1].keys():
            self.inlet_T_constant = float(self.dict_properties['others'][1]['inlet_T_constant'])
        #print(self.I)
        #print(self.I_avg)
        #self.r_amb_reciprocal = round(1/self.r_amb,6)
        self.r_amb_reciprocal = 1/self.r_amb
        self.I_avg ={}
        for key,value in self.I.items():
             self.I_avg[key] = np.mean(value,axis=0)
        #self.r_amb_reciprocal = 1/self.r_amb 
        # self.b=[]
        #for key,value in self.I.items():
         #   self.b = np.append(self.b,value.flatten())
        #self.b = np.reshape(self.b,(self.size,1))
        return
        
    def getTemperature(self,dict_properties, mode=None):
        #self.dict_properties = dict_properties
        res = [] 
        #self.vector_buildMatrixA = np.vectorize(self.buildMatrixA,otypes=[None])
        #print("SuperLU_wrapper")
        if(mode==None):
            self.dict_properties = dict_properties
            self.setup()
        elif(mode=='temperature_dependent'):
            #print("temperature_dependent mode")
            self.dict_properties_update = dict_properties
            self.update()
            #sys.exit(2)
        #print(Rx[0][0][0])
        #print(self.Rz)
        """
        Without detailed_3d:
        if (j>0) Rw = find_res_3D(l,i,j-1,model,1)
        if(j < nc-1) Re = find_res_3D(l,i,j+1,model,1); else Re = LARGENUM;
        if(i > 0)    Rn = find_res_3D(l,i-1,j,model,2); else Rn = LARGENUM;
        if(i < nr-1) Rs = find_res_3D(l,i+1,j,model,2); else Rs = LARGENUM;
        if(l > 0)    Ra = find_res_3D(l-1,i,j,model,3); else Ra = LARGENUM;
        if(l < nl-1) Rb = find_res_3D(l,i,j,model,3);   else Rb = LARGENUM;

        With Detailed_3D:
        if(j > 0)    Rw = find_res(l,i,j-1,model,1)/2 + find_res(l,i,j,model,1)/2; else Rw = LARGENUM;
                if(j < nc-1) Re = find_res(l,i,j+1,model,1)/2 + find_res(l,i,j,model,1)/2; else Re = LARGENUM;
                if(i > 0)    Rn = find_res(l,i-1,j,model,2)/2 + find_res(l,i,j,model,2)/2; else Rn = LARGENUM;
                if(i < nr-1) Rs = find_res(l,i+1,j,model,2)/2 + find_res(l,i,j,model,2)/2; else Rs = LARGENUM;
                if(l > 0)    Ra = find_res(l-1,i,j,model,3); else Ra = LARGENUM;
                if(l < nl-1) Rb = find_res(l, i, j, model,3); else Rb = LARGENUM;

        """
        with open('RC_steady.cir','w') as myfile:
                myfile.write(".title spice solver\n")
                myfile.write(f"Vg GND 0 {self.ambient}\n")
                if 'inlet_T_constant' in self.dict_properties['others'][1].keys():
                   myfile.write(f"Vin INLET 0 {self.inlet_T_constant+273.15}\n")
                curidx=0
		#print("PRACHI!!!!!!!!! Debug:nl, nr, nc",nl,nr,nc)
                for grididx in range(self.size):
                    layer = int(grididx / self.prod)
                    row = int((grididx - layer*self.prod)/self.nc) 
                    col = int( grididx - (layer*(self.prod)+row*self.nc))
                    if (col > 0):
                        Rw = self.Rx[layer][row][col-1]/2 + self.Rx[layer][row][col]/2
                    else:
                        #Rw = math.inf
                        Rw = 100000000
                    if(col < (self.col_limit)):
                        Re = self.Rx[layer][row][col+1]/2 + self.Rx[layer][row][col]/2
                    else:
                        #Re = math.inf
                        Re = 100000000
                    if(row > 0):
                        Rn = self.Ry[layer][row-1][col]/2 + self.Ry[layer][row][col]/2
                    else:
                       # Rn = math.inf;
                        Rn = 10000000
                    if(row < self.row_limit):
                        Rs = self.Ry[layer][row+1][col]/2 + self.Ry[layer][row][col]/2
                    else:
                        #Rs = math.inf
                        Rs = 10000000
                    if(layer > 0):
                        Ra = float(self.factorVN[self.layerVN[layer-1]])*self.Rz[layer-1][row][col] + \
                        (1-float(self.factorVN[self.layerVN[layer]]))*self.Rz[layer][row][col]
                    else:
                        #Ra = math.inf
                        Ra = 100000000
                    """
                    if(layer < self.layer_limit):
                        if layer in self.liq_layer:
                            Rb = 0.5*self.Rz[layer][row][col] 
                        elif layer+1 in self.liq_layer:
                            Rb =  self.Rz[layer][row][col]+0.5*self.Rz[layer+1][row][col] 
                        else:
                            Rb = self.Rz[layer][row][col]
                    else: 
                        #Rb = math.inf
                        Rb = 100000000
                    """
                    if(layer < self.layer_limit):
                        Rb = float(self.factorVN[self.layerVN[layer]])*self.Rz[layer][row][col] + \
                        (1-float(self.factorVN[self.layerVN[layer+1]]))*self.Rz[layer+1][row][col]
                    else: 
                        #Rb = math.inf
                        Rb = 100000000
                #current
                    #if self.I[layer][row][col]!=0:
		    #Zihao: I don't know why both layer1 and layer2 has power in this case, the ptrace and flp shows only the first layers has power. I need to ask prachi about this self.I.items.
                    #if layer == 0:
                    #PRACHI:
                    """
                    Zihao modify this. self.I[layer] is now a 3D array
                    Take average and buil self.I_average;
                    """
                    if layer!= self.layer_limit and self.I_avg[layer][row][col]!=0:
                        myfile.write("I_{}_{}_{} GND Node{}_{}_{} {}A\n".format(layer,row,col,layer, row, col, self.I_avg[layer][row][col])) #Replace self.I with self.I_average
                #east resistance
                    if col != self.col_limit:
                        myfile.write("R_{}_{}_{}_1 Node{}_{}_{} Node{}_{}_{} {}\n".format(layer,row,col,layer, row, col,layer,row,col+1,Re))
                #north resistance
                    if row != self.row_limit:	    
                        #not liquid grid cell
                        if self.glabels[layer][row][col]!='Liq':
                            myfile.write("R_{}_{}_{}_2 Node{}_{}_{} Node{}_{}_{} {}\n".format(layer,row,col,layer, row, col,layer,row+1,col,Rs))
                        #liquid grid cell
                        else:
                            if row == 0:
                                #inlet
                                myfile.write("G_%d_%d_%d INLET Node%d_%d_%d INLET 0 %s\n"%(layer,row,col,layer,row,col,self.Conv[layer][row][col]))
                                #channel
                            else:
                                myfile.write("G_%d_%d_%d Node%d_%d_%d Node%d_%d_%d VALUE = {(V(Node%d_%d_%d)+V(Node%d_%d_%d))/2*%s}\n"%(layer,row,col,layer,row-1,col,layer,row,col,layer,row-1,col,layer,row,col,self.Conv[layer][row][col]))
                    if row == self.row_limit and self.glabels[layer][row][col] == 'Liq':
                        #last channel
                        myfile.write("G_%d_%d_%d Node%d_%d_%d Node%d_%d_%d VALUE = {(V(Node%d_%d_%d)+V(Node%d_%d_%d))/2*%s}\n"%(layer,row,col,layer,row-1,col,layer,row,col,layer,row-1,col,layer,row,col,self.Conv[layer][row][col]))
                        #outlet
                        myfile.write("G_%d_%d_%d Node%d_%d_%d INLET Node%d_%d_%d 0 %s\n"%(layer,row+1,col,layer,row,col,layer,row,col,self.Conv[layer][row][col]))
                #above resistance
                    if layer != self.layer_limit: 
                        myfile.write("R_{}_{}_{}_3 Node{}_{}_{} Node{}_{}_{} {}\n".format(layer,row,col,layer, row, col,layer+1,row,col,Rb))
                    else:
                        myfile.write("R_{}_{}_{}_3 Node{}_{}_{} GND {}\n".format(layer,row,col,layer, row, col,self.r_amb))
                myfile.write('.OP\n')
                #disable zoltan for mono3D simulation
                #myfile.write(f'.OPTIONS LINSOL TYPE={self.ll_solver} TR_PARTITION = 0\n')
                myfile.write(f'.OPTIONS LINSOL TR_PARTITION = 0\n')
               # myfile.write(f'.OPTIONS LINSOL TYPE={self.ll_solver}\n')
                myfile.write('.PRINT DC FORMAT=CSV PRECISION=4 ')
                for grididx in range(self.size):
                    layer = int(grididx / self.prod)
                    row = int((grididx - layer*self.prod)/self.nc) 
                    col = int( grididx - (layer*(self.prod)+row*self.nc))
                    myfile.write("V(Node{}_{}_{}) ".format(layer,row,col))
                myfile.write("\n")
                myfile.write(".SAVE TYPE=IC\n")
                myfile.write(".end\n")
        if int(self.num_core)<=1:
            os.system("Xyce RC_steady.cir -l RC_steady.log")
        else:
            os.system(f"mpirun -np {self.num_core} Xyce -l RC_steady.log RC_steady.cir")
        with open('RC_steady.cir.csv','r') as myfile:
            tmp = np.asarray(list(map(float,list(myfile)[1][:].split(','))))
            reshape_x = tmp.reshape(self.nl,self.nr,self.nc)
        #os.system("cp RC_steady.cir.csv ../Example/results/RC_steady.cir.csv")
        #os.system("rm -rf RC_steady.cir.csv")
        return reshape_x
