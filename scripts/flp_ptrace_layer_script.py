import pandas as pd

#square chip#
run="Run2"
#chip_x = 0.01 #10mm
#chip_x = 0.005 #5mm
#block_x = 0.0005 #500um
#chiplabel="5mm"
chip_x = 0.02 #20mm
block_x = 0.001 #1mm
chiplabel="20mm"
num_blocks_x = int(chip_x / block_x)
total_blocks = num_blocks_x*num_blocks_x

######Floorplan###############
#fname = "../flp_files/Tests_withHotSpot/L0_flp_1.csv"
#fpartial = "Tests_withHotSpot/L0_flp_1.csv"
#fname = "../flp_files/Tests_withHotSpot/L0_flp_2.csv"
#fpartial = "Tests_withHotSpot/L0_flp_2.csv"
fname = "../flp_files/Tests_withHotSpot/L0_flp_3.csv"
fpartial = "Tests_withHotSpot/L0_flp_3.csv"
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

###### PTrace ###### and ###### LCF #######
#power = [0.1,0.2,0.3,0.4,0.5]
power = [0.2,0.4,0.6,0.8,1.0]
for p_num, p in enumerate(power):
    df = pd.DataFrame([],columns=['UnitName','Power'])
    PD = round(p/(block_x*block_x*100*100),3)
    print(PD,"W/cm2")
    #pname = "../ptrace_files/Tests_withHotSpot/P"+str(p_num)+"_UniformPD"+str(PD)+"Wcm2_ptrace.csv"
    #ppartial = "Tests_withHotSpot/P"+str(p_num)+"_UniformPD"+str(PD)+"Wcm2_ptrace.csv"
    pname = "../ptrace_files/Tests_withHotSpot/"+chiplabel+"_P"+str(p_num)+"_UniformPD"+str(PD)+"Wcm2_ptrace.csv"
    ppartial = "Tests_withHotSpot/"+chiplabel+"_P"+str(p_num)+"_UniformPD"+str(PD)+"Wcm2_ptrace.csv"
    for i in range(num_blocks_x):
        x_coord=0
        for j in range(num_blocks_x):
            uname="Unit_"+str(i)+"_"+str(j)
            ff = pd.DataFrame([[uname,round(p,6)]],columns=['UnitName','Power'])
            df = df.append(ff)
    #print(df)
    df.to_csv(pname,index=False)
    #lname = "../lcf_files/Tests_withHotSpot/L0_lcf_1_P"+str(p_num)+".csv"
    #lname = "../lcf_files/Tests_withHotSpot/L0_lcf_2_P"+str(p_num)+".csv"
    lname = "../lcf_files/Tests_withHotSpot/L0_lcf_3_P"+str(p_num)+".csv"
    df1 = pd.DataFrame([],columns=['Layer','FloorplanFile','Thickness (m)','PtraceFile','LateralHeatFlow'])
    ff1 = pd.DataFrame([[0,fpartial,0.00015,ppartial,True]],columns=['Layer','FloorplanFile','Thickness (m)','PtraceFile','LateralHeatFlow'])
    df1 = df1.append(ff1)
    #print(df1)
    df1.to_csv(lname,index=False)
##############################
