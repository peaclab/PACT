import sys
import numpy as np
from scipy.sparse import csc_matrix, linalg as sla,coo_matrix,csr_matrix
import math

class SuperLUSolver:
    def __init__(self,name):
        self.name = name
        return

    def display_solver(self):
        print(self.name)
        return

    def update(self):
        self.cooData.fill(0)
        self.cooX.fill(0)
        self.cooY.fill(0)
        for (layer,prop) in self.dict_properties_update['update'].items():
            if(prop=='Rz'):
                self.dict_properties['Rz'].update(self.dict_properties_update["Rz"])
                self.Rz.update(self.dict_properties_update['Rz'])
            elif(prop=='Rx'):
                self.dict_properties['Rx'].update(self.dict_properties_update["Rx"])
                self.Rx.update(self.dict_properties_update['Rx'])
            elif(prop=='Ry'):
                self.dict_properties['Ry'].update(self.dict_properties_update["Ry"])
                self.Ry.update(self.dict_properties_update['Ry'])
            elif(prop=='C'):
                self.dict_properties['C'].update(self.dict_properties_update["C"])
                self.C.update(self.dict_properties_update['C'])
            elif(prop=='I'):
                self.dict_properties['I'].update(self.dict_properties_update["I"])
                self.I.update(self.dict_properties_update['I'])
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
        self.nnz = self.nl * self.nr * self.nc + 2 * (self.nl-1) * self.nr * self.nc + 2 * self.nl * (self.nr-1) * \
            self.nc +  2 * self.nl * self.nr * (self.nc-1)
        self.addY={0:1,1:-1,2:-self.nc,3:self.nc,4:-self.nr*self.nc,5:self.nr*self.nc} # 0...6 correspond to [Re,Rw,Rn,Rs,Ra,Rb]
        self.prod = self.nr*self.nc
        self.cooData = np.zeros((self.nnz))
        self.cooX = np.zeros((self.nnz))
        self.cooY = np.zeros((self.nnz))
        self.Rx = self.dict_properties['Rx']
        self.Ry = self.dict_properties['Ry']
        self.Rz = self.dict_properties['Rz']
        self.C = self.dict_properties['C']
        self.I = self.dict_properties['I']
        self.r_amb_reciprocal = 1/self.r_amb
        self.b=[]
        for key,value in self.I.items():
            mean_value = np.average(value,axis=0)
            self.b = np.append(self.b,mean_value.flatten())
        self.b = np.reshape(self.b,(self.size,1))
        return
        
    def getTemperature(self,dict_properties, mode=None):
        if(mode==None):
            self.dict_properties = dict_properties
            self.setup()
        elif(mode=='temperature_dependent'):
            self.dict_properties_update = dict_properties
            self.update()
        curidx=0
        for grididx in range(self.size):
            layer = int(grididx / self.prod)
            row = int((grididx - layer*self.prod)/self.nc) 
            col = int( grididx - (layer*(self.prod)+row*self.nc))
            if (col > 0):
                Rw = self.Rx[layer][row][col-1]/2 + self.Rx[layer][row][col]/2
            else:
                Rw = math.inf
            if(col < (self.col_limit)):
                Re = self.Rx[layer][row][col+1]/2 + self.Rx[layer][row][col]/2
            else:
                Re = math.inf
            if(row > 0):
                Rn = self.Ry[layer][row-1][col]/2 + self.Ry[layer][row][col]/2
            else:
                Rn = math.inf;
            if(row < self.row_limit):
                Rs = self.Ry[layer][row+1][col]/2 + self.Ry[layer][row][col]/2
            else:
                Rs = math.inf
            if(layer > 0):
                Ra = int(self.factorVN[self.layerVN[layer-1]])*self.Rz[layer-1][row][col] + \
                        (1-int(self.factorVN[self.layerVN[layer]]))*self.Rz[layer][row][col]
            else:
                Ra = math.inf
            if(layer < self.layer_limit):
                Rb = int(self.factorVN[self.layerVN[layer]])*self.Rz[layer][row][col] + \
                        (1-int(self.factorVN[self.layerVN[layer+1]]))*self.Rz[layer+1][row][col]
            else: 
                Rb = math.inf
            dia_val = 0
            for val_idx,val in enumerate([Re,Rw,Rn,Rs,Ra,Rb]):
                if(val!=math.inf):
                    self.cooX[curidx] = grididx
                    self.cooY[curidx] = grididx+self.addY[val_idx]
                    self.cooData[curidx] = -1.0/val 
                    curidx += 1 
                    dia_val += 1.0/val
            self.cooX[curidx] = grididx
            self.cooY[curidx] = grididx
            if(layer==self.layer_limit):
                dia_val += self.r_amb_reciprocal 
            self.cooData[curidx] = dia_val
            curidx += 1
        A_csc = csc_matrix((self.cooData,(self.cooX,self.cooY)),shape=(self.size,self.size))
        nn =0
        lu = sla.splu(A_csc,permc_spec='MMD_AT_PLUS_A',diag_pivot_thresh=0.001,options=dict(Fact='DOFACT',Equil=False,SymmetricMode=True))
        x = lu.solve(self.b)
        reshape_x = x.reshape(self.nl,self.nr,self.nc)
        return reshape_x
