import pandas as pd

#square chip#
run="Run3"
chip_x = 0.002 #2mm
block_x = 0.0005 #500um
chiplabel="2mm"
num_blocks_x = int(chip_x / block_x)
total_blocks = num_blocks_x*num_blocks_x
chiplabel="2mm"

######Floorplan###############
fname0 = "../flp_files/Tests_withHotSpot/L0_flp_4.csv"
fpartial0 = "Tests_withHotSpot/L0_flp_4.csv"
fname1 = "../flp_files/Tests_withHotSpot/L1_flp_4.csv"
fpartial1 = "Tests_withHotSpot/L1_flp_4.csv"
df0 = pd.DataFrame([],columns=['UnitName','X','Y','Length (m)','Width (m)','ConfigFile','Label'])
df1 = pd.DataFrame([],columns=['UnitName','X','Y','Length (m)','Width (m)','ConfigFile','Label'])
"""
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
"""
############################

###### PTrace ###### and ###### LCF #######
bgpd = [50]
hspd = [100,200,300]
hs_loc = {'1HS':10} #run_idx=3 #2mm 
run_idx=3 #Run index starts from here
run="Run"
p_idx=0
fname=''
for bg_idx, bg in enumerate(bgpd):
    for hs_idx, hs in enumerate(hspd):
        df = pd.DataFrame([],columns=['UnitName','Power'])
        bg_power = round(bg*block_x*block_x*100*100,6)
        hs_power = round(hs*block_x*block_x*100*100,6)
        pname = "../ptrace_files/Tests_withHotSpot/"+chiplabel+"_P"+str(p_idx)+"_NonUniformPD"+str(bg)+"_"+str(hs)+"Wcm2_ptrace.csv"
        ppartial = "Tests_withHotSpot/"+chiplabel+"_P"+str(p_idx)+"_NonUniformPD"+str(bg)+"_"+str(hs)+"Wcm2_ptrace.csv"

        for i in range(num_blocks_x):
            x_coord=0
            for j in range(num_blocks_x):
                uname="Unit_"+str(i)+"_"+str(j)
                if(i*num_blocks_x + j  == hs_loc['1HS']):
                    #print("HEYYY",i*num_blocks_x+j)
                    ff = pd.DataFrame([[uname,round(hs_power,6)]],columns=['UnitName','Power'])
                else:
                    ff = pd.DataFrame([[uname,round(bg_power,6)]],columns=['UnitName','Power'])
                df = df.append(ff)
        print(df)
        df.to_csv(pname,index=False)

        lname = "../lcf_files/Tests_withHotSpot/lcf_4_NonUniformP"+str(p_idx)+".csv"
        df1 = pd.DataFrame([],columns=['Layer','FloorplanFile','Thickness (m)','PtraceFile','LateralHeatFlow'])
        ff1 = pd.DataFrame([[0,fpartial0,0.0001,ppartial,True]],columns=['Layer','FloorplanFile','Thickness (m)','PtraceFile','LateralHeatFlow'])
        df1 = df1.append(ff1)
        ff1 = pd.DataFrame([[1,fpartial1,0.0001,'',True]],columns=['Layer','FloorplanFile','Thickness (m)','PtraceFile','LateralHeatFlow'])
        df1 = df1.append(ff1)
        #print(df1)
        df1.to_csv(lname,index=False)
        p_idx += 1
##############################
