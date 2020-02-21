import sys
import numpy as np
from scipy.sparse import csc_matrix, linalg as sla,coo_matrix,csr_matrix
from scipy import linalg
import math

class SuperLUSolver:
    def __init__(self,name):
        self.name = name
        return

    def display_solver(self):
        print(self.name)
        return

    def update(self,dict_properties_update):
        #self.cooData.fill(0)
        #self.cooX.fill(0)
        #self.cooY.fill(0)
        #print(self.dict_properties_update['update'])
        for (layer,prop) in dict_properties_update['update'].items():
            if(prop=='Rz'):
                #print("Before:",self.dict_properties["Rz"])
                #print("Before:",self.Rz)
                #self.Rz[layer] = self.dict_properties['Rz'][layer]

                #self.dict_properties['Rz'].update(dict_properties_update["Rz"])
                self.Rz.update(dict_properties_update['Rz'])
                #print("After:",self.dict_properties["Rz"])
                #print("After:",self.Rz)
            elif(prop=='Rx'):
                #self.dict_properties['Rx'].update(dict_properties_update["Rx"])
                self.Rx.update(dict_properties_update['Rx'])
                #self.Rx[layer] = self.dict_properties['Rx'][layer]
            elif(prop=='Ry'):
                #self.dict_properties['Ry'].update(dict_properties_update["Ry"])
                self.Ry.update(dict_properties_update['Ry'])
                #self.Ry[layer] = self.dict_properties['Ry'][layer]
            elif(prop=='C'):
                #self.dict_properties['C'].update(dict_properties_update["C"])
                self.C.update(dict_properties_update['C'])
                #self.C[layer] = self.dict_properties['C'][layer]
            elif(prop=='I'):
                #self.dict_properties['I'].update(dict_properties_update["I"])
                self.I.update(dict_properties_update['I'])
                #self.I[layer] = self.dict_properties['I'][layer]
                for key,value in self.I.items():
                    self.b = np.append(self.b,value.flatten())
                self.b = np.reshape(self.b,(self.size,1))
        return

    def setup(self, dict_properties):
        self.nr = int(dict_properties['grid_rows'])
        self.nc = int(dict_properties['grid_cols'])
        self.nl = int(dict_properties['num_layers'])
        self.layerVN = dict_properties['layer_virtual_nodes']
        self.factorVN = dict_properties['factor_virtual_nodes']
        self.r_amb= dict_properties['r_amb']
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

        #self.cooData = np.zeros((self.nnz))
        #self.cooX = np.zeros((self.nnz))
        #self.cooY = np.zeros((self.nnz))
        #print(self.A)
        #shold I replace self.Rx with self.dict_properties['Rx'] in this python file?
        self.Rx = dict_properties['Rx']
        self.Ry = dict_properties['Ry']
        self.Rz = dict_properties['Rz']
        self.C = dict_properties['C']
        self.I = dict_properties['I']
        self.r_amb_reciprocal = 1/self.r_amb 
        self.b=[]
        for key,value in self.I.items():
            self.b = np.append(self.b,value.flatten())
        self.b = np.reshape(self.b,(self.size,1))
        #print(self.b)
        return
        
    def getTemperature(self,dict_properties, mode=None):
        #self.dict_properties = dict_properties
        
        #self.vector_buildMatrixA = np.vectorize(self.buildMatrixA,otypes=[None])
        #print("SuperLU_wrapper")
        if(mode==None):
            #self.dict_properties = dict_properties
            self.setup(dict_properties)
        elif(mode=='temperature_dependent'):
            print("temperature_dependent mode")
            #self.dict_properties_update = dict_properties
            self.update(dict_properties)
            #sys.exit(2)
        #print(Rx[0][0][0])
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

        curidx=0
        #print("PRACHI!!!!!!!!! Debug:nl, nr, nc",nl,nr,nc)
        #sys.exit(2)
        size = self.size
        prod = self.prod
        Rx = self.Rx
        Ry = self.Ry
        Rz = self.Rz
        print("One''''")
        for grididx in range(size):
            layer = int(grididx / prod)
            row = int((grididx - layer*prod)/self.nc) 
            col = int( grididx - (layer*prod+row*self.nc))
            #col = int((grididx - layer*(nr*nc))/nr)
            #xoffset = layer*nr*nc
            #yoffset = layer*nr*nc
            """
            if(curidx >=95):
                print("curidx:",curidx,"grididx:",grididx,"layer:",layer,"row:",row,"col:",col)
            """
            #print(grididx,layer,row,col)
            #print("grididx:",grididx,"xoffset:",xoffset,"yoffset:",yoffset)
            if (col > 0):
                #Rw = self.Rx[layer][row][col-1]/2 + self.Rx[layer][row][col]/2
                Rw = Rx[layer][row][col-1]/2 + Rx[layer][row][col]/2
            else:
                Rw = math.inf
            if(col < (self.col_limit)):
                #Re = self.Rx[layer][row][col+1]/2 + self.Rx[layer][row][col]/2
                Re = Rx[layer][row][col+1]/2 + Rx[layer][row][col]/2
            else:
                Re = math.inf
            if(row > 0):
                #Rn = self.Ry[layer][row-1][col]/2 + self.Ry[layer][row][col]/2
                Rn = Ry[layer][row-1][col]/2 + Ry[layer][row][col]/2
            else:
                Rn = math.inf;
            if(row < self.row_limit):
                #Rs = self.Ry[layer][row+1][col]/2 + self.Ry[layer][row][col]/2
                Rs = Ry[layer][row+1][col]/2 + Ry[layer][row][col]/2
            else:
                Rs = math.inf
            if(layer > 0):
                #Ra = int(self.factorVN[self.layerVN[layer-1]])*self.Rz[layer-1][row][col] + \
                #        (1-int(self.factorVN[self.layerVN[layer]]))*self.Rz[layer][row][col]
                Ra = int(self.factorVN[self.layerVN[layer-1]])*Rz[layer-1][row][col] + \
                        (1-int(self.factorVN[self.layerVN[layer]]))*Rz[layer][row][col]
            else:
                Ra = math.inf
            if(layer < self.layer_limit):
                #Rb = int(self.factorVN[self.layerVN[layer]])*self.Rz[layer][row][col] + \
                #        (1-int(self.factorVN[self.layerVN[layer+1]]))*self.Rz[layer+1][row][col]
                Rb = int(self.factorVN[self.layerVN[layer]])*Rz[layer][row][col] + \
                        (1-int(self.factorVN[self.layerVN[layer+1]]))*Rz[layer+1][row][col]
            else: 
                Rb = math.inf
                #Rb = 0.00000001
            """
            if(curidx >=95):
                print("Re:",Re,"Rw:",Rw,"Rn:",Rn,"Rs:",Rs,"Ra:",Ra,"Rb:",Rb)
            """
            """
            if(layer ==2):
                print("Re:",Re,"Rw:",Rw,"Rn:",Rn,"Rs:",Rs,"Ra:",Ra,"Rb:",Rb)
            """
            addY = self.addY
            nnz = self.nnz 
            cooData = np.zeros((nnz))
            cooX = np.zeros((nnz))
            cooY = np.zeros((nnz))
            dia_val = 0
            for val_idx,val in enumerate([Re,Rw,Rn,Rs,Ra,Rb]):
                if(val!=math.inf):
                    #print(val)
                    #if(layer==1):
                        #print("Debug",val_idx,val)
                    #print(val_idx,curidx)
                    #cooX[curidx] = grididx+xoffset
                    cooX[curidx] = grididx
                    #if(layer==1):
                        #print("X:",grididx+xoffset)
                    #cooY[curidx] = grididx+addY[val_idx]+yoffset
                    cooY[curidx] = grididx+addY[val_idx]
                    #if(layer==1):
                        #print("Y:",grididx+addY[val_idx]+yoffset)
                    #cooData[curidx] = round(-1.0/val,6) 
                    cooData[curidx] = -1.0/val 
                    #cooData[curidx] = np.double(-1.0/val) 
                    ###Debug###
                    #if(val == 0):
                    #    print("val:",val, "val_idx(Re,Rw,Rn,Rs,Ra,Rb):",val_idx,"layer:",layer,"row:",row,"col:",col)
                    ###Debug ends
                    curidx += 1 
                    #####print("Debugi1:",curidx,grididx)
                    dia_val += 1.0/val
                    #if(layer ==2):
                        #print("cooData[curidx]:",cooData[curidx], "dia_val:",dia_val)
            ###########print("Debug:",curidx,grididx)
            #cooX[curidx] = grididx+xoffset
            #cooY[curidx] = grididx+yoffset
            cooX[curidx] = grididx
            cooY[curidx] = grididx
            if(layer==self.layer_limit):
                dia_val += self.r_amb_reciprocal 
                #print("PRACHI: dia_val value added for top dummy layer is:",dia_val)
            cooData[curidx] = dia_val
            #cooData[curidx] = round(dia_val,6)
            #cooData[curidx] = np.double(dia_val)
            curidx += 1

        #"""Debug:
        #print("Final Curidx:",curidx,"should be equal to nnz:",nnz)
        #print("If mismatch, check if it's because of lateral disabled in any layer")
        #print("PRACHI (NaN / infinity)")
        """
        print("cooData", np.isnan(cooData).any())
        print("cooX", np.isnan(cooX).any())
        print("cooY", np.isnan(cooY).any())
        """
        #np.set_printoptions(threshold=np.inf)
        #print(cooData.shape)
        #print("cooData", np.isfinite(cooData).all())
        #print("cooX", np.isfinite(cooX).all())
        #print("cooY", np.isfinite(cooY).all())

        """
        print("Printing cooX")
        print(len(cooX),cooX)
        print("Printing cooY")
        print(len(cooY),cooY)
        print("Printing cooData")
        print(len(cooData),cooData)
        print("Printing (cooX,cooY)=cooV")
        for ii in range (curidx):
            print("(",cooX[ii],",",cooY[ii],"=",cooData[ii])
        #print(cooRow)
        #print(cooCol)
        #print(cooData)
        #
        """
        #self.vector_buildMatrixA(self.,self.curidx)
        #self.vector_buildMatrixA(X_vals,Y_vals,length_vals, height_vals, PowerDensities,left_x_vals,right_x_vals,bottom_y_vals,top_y_vals,flp_df['Label'].values,flp_df['ConfigFile'].values,block_counter,grid_length,grid_width)

        #mtx_size=nl*nr*nc
        #size=nr*nc
        #print("curidx:",curidx,"nnz:",self.nnz,"size:",self.size)
        #A_csc = np.round(csc_matrix((cooData,(cooX,cooY)),shape=(size,size)),10)
        print("One")
        sys.exit(0)
        A_csc = csc_matrix((cooData,(cooX,cooY)),shape=(size,size))
        #A_csc = np.double(csc_matrix((cooData,(cooX,cooY)),shape=(size,size)))
        print("Determinant of the computed CSC matrix:",linalg.det(A_csc.toarray()))#,sla.inv(A_csc))
        nn =0

        ### Uncomment below for more debugging
        #f = open("Coo.txt","w")
        #for nn in range (curidx):
        #    f.write(str(int(cooX[nn]))+"\t"+str(int(cooY[nn]))+"\t"+str("{:.6f}".format(cooData[nn])))
        #    f.write("\n")
        #f.close()
        ##########################3

        #f = open("A.txt","w")
        #for nn in range (nnz):
        #for nn in range (curidx):
        #    f.write(str(A_csc.data[nn]))
        #    f.write("\n")
        #f.close()
        ###print(A_csc.data)
        ####print(A_csc.indices)
        ####print(A_csc.indptr)
        ####print(A_csc.toarray())
        #for row in list(A_csc.toarray()):
        #    for elem in row:
        #        print(elem, end=", ")
        #A_csr = csr_matrix(A_csc)
        #print(A_csc)
        #b = np.reshape(b,(size,1))
        #for row in list(b):
        #    print(row,",")
        #print(A_csc.toarray())
        #print("\n")
        ######print(b[0:4096])
        #print(self.b)
        #f = open("B_power.txt","w")
        #for nn in range (self.b.size):
        #    f.write(str(self.b[nn]).replace('[','').replace(']',''))
        #    #f.write(*self.b[nn])
        #    f.write("\n")
        #f.close()
        ####print("PRACHIIIII DEBUGGGG!!!!")
        ###print(np.where(b == 0.078125))
        #print("Sending matrix to SuperLU")
        lu = sla.splu(A_csc,permc_spec='MMD_AT_PLUS_A',diag_pivot_thresh=0.001,options=dict(Fact='DOFACT',Equil=False,SymmetricMode=True))
        #print("SuperLU ends")
        #lu = sla.splu(A_csc,options=dict(Equil=True,SymmetricMode=True))
        #lu = sla.splu(A_csc)
        #print(lu.perm_r)
        #print(lu.perm_c)
        #print(lu.L.A)
        #print(lu.U.A)
        """
        try:
            i = sla.inv(A_csc)
            print("A_csc is NOT a singular matrix\n")
            lu = sla.splu(A_csc)
        except np.linalg.LinAlgError as err:
            print("A_csc is a singular matrix\n")
        """
        #x = np.round(lu.solve(b),8)
        x = lu.solve(self.b)
        #y = np.round(x-273.15,6)
        #reshape_y = y.reshape(nl,nr,nc)
        reshape_x = x.reshape(self.nl,self.nr,self.nc)
        #print(b.shape[0],b.shape[1])
        #print(A_csc.shape[0],A_csc.shape[1])
        #print(x)
        #print(reshape_x)
        #print (y)

        ##Debug below:
        #check_b=[]
        #check_b = np.round(A_csc.dot(x),6)
        #print(check_b)
        #print(b==check_b)
        ######## Debug end
        #print(A_csc.dor(x))
        #A_array = A_csc.toarray()
        #print(A_array)
        return reshape_x
