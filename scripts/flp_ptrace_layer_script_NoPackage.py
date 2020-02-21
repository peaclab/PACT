#### This is only for NoPackage Validation with ITherm ####
import pandas as pd

#square chip#
chiplabel="12_6mm"
chip_x = 0.0126 #12.6mm
block_x = 0.0126 #12.6 mm; only onle block
num_blocks_x = int(chip_x / block_x)
total_blocks = num_blocks_x*num_blocks_x

######Floorplan###############
fname = "../flp_files/Tests_withHotSpot/"+chiplabel+"_flp.csv"
fpartial = "Tests_withHotSpot/"+chiplabel+"_flp.csv"
df = pd.DataFrame([],columns=['UnitName','X','Y','Length (m)','Width (m)','ConfigFile','Label'])
x_coord=0
y_coord=0
label='Si'
for i in range(num_blocks_x):
    x_coord=0
    for j in range(num_blocks_x):
        uname="Unit_"+str(i)+"_"+str(j)
        cfile=''
        ff = pd.DataFrame([[uname,round(x_coord,6),round(y_coord,6),round(block_x,6),round(block_x,6),cfile,label]],columns=['UnitName','X','Y','Length (m)','Width (m)','ConfigFile','Label'])
        df = df.append(ff)
        x_coord += block_x
    y_coord += block_x
#print(df)
df.to_csv(fname,index=False)
############################

############## Uniform Ptrace and LCF #################
powerdensity = [20,30,40,50]
for p_num, PD in enumerate(powerdensity):
    power = round(PD * 100 * 100 * block_x * block_x,8) 
    df = pd.DataFrame([],columns=['UnitName','Power'])
    print(PD,"W/cm2 (Uniform)")
    print("power:",power)
    pname = "../ptrace_files/Tests_withHotSpot/"+chiplabel+"_UniformPD_"+str(PD)+"Wcm2_ptrace.csv"
    ppartial = "Tests_withHotSpot/"+chiplabel+"_UniformPD_"+str(PD)+"Wcm2_ptrace.csv"
    for i in range(num_blocks_x):
        x_coord=0
        for j in range(num_blocks_x):
            uname="Unit_"+str(i)+"_"+str(j)
            ff = pd.DataFrame([[uname,round(power,8)]],columns=['UnitName','Power'])
            df = df.append(ff)
    #print(df)
    df.to_csv(pname,index=False)

    lname = "../lcf_files/Tests_withHotSpot/"+chiplabel+"_lcf_UniformPD_"+str(PD)+"Wcm2.csv"
    print(lname,pname)
    df1 = pd.DataFrame([],columns=['Layer','FloorplanFile','Thickness (m)','PtraceFile','LateralHeatFlow'])
    ff1 = pd.DataFrame([[0,fpartial,0.0001,ppartial,True]],columns=['Layer','FloorplanFile','Thickness (m)','PtraceFile','LateralHeatFlow'])
    df1 = df1.append(ff1)
    #print(df1)
    df1.to_csv(lname,index=False)
##############################
