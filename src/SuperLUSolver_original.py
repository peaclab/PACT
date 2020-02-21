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

    def getTemperature(self,dict_properties):
        #self.vector_buildMatrixA = np.vectorize(self.buildMatrixA,otypes=[None])
        #print("SuperLU_wrapper")
        nr = int(dict_properties['grid_rows'])
        nc = int(dict_properties['grid_cols'])
        nl = int(dict_properties['num_layers'])
        layerVN = dict_properties['layer_virtual_nodes']
        factorVN = dict_properties['factor_virtual_nodes']
        r_amb=dict_properties['r_amb']
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
        nnz = 5*nr*nc-2*(nr+nc)
        nnz = nnz*nl
        nnz = nnz + 2*(nl-1)*nr*nc
        nnz1= nl*nr*nc + 2*(nl-1)*nr*nc + 2*nl*(nr-1)*nc +  2*nl*nr*(nc-1)
        #print("nnz:",nnz,"nnz1:",nnz1)
        #nnz = 5*nr*nc-2*(nr+nc)
        #nnz = nnz*(nl-1) + 2*(nr*nc)
        #nnz = nnz + (nl-2)*nr*nc
        #print("nnz:",nnz)
        #nnz2 = nnz + 2*(nl-1)*nr*nc
        cooData = np.zeros((nnz))
        cooX = np.zeros((nnz))
        cooY = np.zeros((nnz))
        #print(self.A)
        Rx = dict_properties['Rx']
        Ry = dict_properties['Ry']
        Rz = dict_properties['Rz']
        C = dict_properties['C']
        I = dict_properties['I']

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
        addY={0:1,1:-1,2:-nc,3:nc,4:-nr*nc,5:nr*nc} # 0...6 correspond to [Re,Rw,Rn,Rs,Ra,Rb]
        prod = nr*nc
        #print("PRACHI!!!!!!!!! Debug:nl, nr, nc",nl,nr,nc)
        #sys.exit(2)
        for grididx in range(nl*nr*nc):
            layer = int(grididx / (nr*nc))
            row = int((grididx - layer*(nr*nc))/nc) 
            col = int( grididx - (layer*(nr*nc)+row*nc))
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
                #Rw = np.double(Rx[layer][row][col-1]/2 + Rx[layer][row][col]/2)
                #if(Rw < 1):
                #    print("PRACHI Rw:",Rw)
                #Rw = round(Rx[layer][row][col-1]/2 + Rx[layer][row][col]/2,6)
                Rw = Rx[layer][row][col-1]/2 + Rx[layer][row][col]/2
                #Rw = Rx[layer][row][col-1]
            else:
                Rw = math.inf
            if(col < (nc-1)):
                #Re = np.double(Rx[layer][row][col+1]/2 + Rx[layer][row][col]/2)
                #Re = round(Rx[layer][row][col+1]/2 + Rx[layer][row][col]/2,6)
                Re = Rx[layer][row][col+1]/2 + Rx[layer][row][col]/2
                #Re = Rx[layer][row][col+1]
                #if(Re < 1):
                #    print("PRACHI Re:",Re)
            else:
                Re = math.inf
            if(row > 0):
                #Rn = np.double(Ry[layer][row-1][col]/2 + Ry[layer][row][col]/2)
                #Rn = round(Ry[layer][row-1][col]/2 + Ry[layer][row][col]/2,6)
                Rn = Ry[layer][row-1][col]/2 + Ry[layer][row][col]/2
                #Rn = Ry[layer][row-1][col] 
                #if(Rn < 1):
                #    print("PRACHI Rn:",Rn)
            else:
                Rn = math.inf;
            if(row < nr-1):
                #Rs = np.double(Ry[layer][row+1][col]/2 + Ry[layer][row][col]/2)
                #Rs = round(Ry[layer][row+1][col]/2 + Ry[layer][row][col]/2,6)
                Rs = Ry[layer][row+1][col]/2 + Ry[layer][row][col]/2
                #Rs = Ry[layer][row+1][col]
                #if(Rs < 1):
                #    print("PRACHI Rs:",Rs)
            else:
                Rs = math.inf
            if(layer > 0):
                #Ra = round(int(factorVN[layerVN[layer-1]])*Rz[layer-1][row][col] + \
                #        (1-int(factorVN[layerVN[layer]]))*Rz[layer][row][col],6)
                Ra = int(factorVN[layerVN[layer-1]])*Rz[layer-1][row][col] + \
                        (1-int(factorVN[layerVN[layer]]))*Rz[layer][row][col]
                #Ra = Rz[layer-1][row][col]
            else:
                Ra = math.inf
            if(layer < nl-1):
                #print(layer,factorVN[layerVN[layer]])
                #Rb = round(int(factorVN[layerVN[layer]])*Rz[layer][row][col] + \
                #        (1-int(factorVN[layerVN[layer+1]]))*Rz[layer+1][row][col],6)
                Rb = int(factorVN[layerVN[layer]])*Rz[layer][row][col] + \
                        (1-int(factorVN[layerVN[layer+1]]))*Rz[layer+1][row][col]
                #Rb = Rz[layer][row][col] 
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
            if(layer==nl-1):
                dia_val += 1/r_amb 
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
        size=nl*nr*nc
        print("curidx:",curidx,"nnz:",nnz,"size:",size)
        #A_csc = np.round(csc_matrix((cooData,(cooX,cooY)),shape=(size,size)),10)
        A_csc = csc_matrix((cooData,(cooX,cooY)),shape=(size,size))
        #A_csc = np.double(csc_matrix((cooData,(cooX,cooY)),shape=(size,size)))
        #print("Determinant of the computed CSC matrix:",linalg.det(A_csc.toarray()))#,sla.inv(A_csc))
        nn =0
        f = open("Coo.txt","w")
        for nn in range (curidx):
            f.write(str(int(cooX[nn]))+"\t"+str(int(cooY[nn]))+"\t"+str("{:.6f}".format(cooData[nn])))
            f.write("\n")
        f.close()
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
        b=[]
        for key,value in I.items():
            b = np.append(b,value.flatten())
        #b = np.round(np.reshape(b,(size,1)),8)
        b = np.reshape(b,(size,1))
        #b = np.reshape(b,(size,1))
        #for row in list(b):
        #    print(row,",")
        #print(A_csc.toarray())
        #print("\n")
        ######print(b[0:4096])
        ####print("PRACHIIIII DEBUGGGG!!!!")
        ###print(np.where(b == 0.078125))
        print("Sending matrix to SuperLU")
        lu = sla.splu(A_csc,permc_spec='MMD_AT_PLUS_A',diag_pivot_thresh=0.001,options=dict(Fact='DOFACT',Equil=False,SymmetricMode=True))
        print("SuperLU ends")
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
        x = lu.solve(b)
        y = np.round(x-273.15,6)
        reshape_y = y.reshape(nl,nr,nc)
        reshape_x = x.reshape(nl,nr,nc)
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
    """
    def buildMatrixA(self,a,curidx):
        print("Hey")
        print(type(a))
        print(curidx)
        return
    """
