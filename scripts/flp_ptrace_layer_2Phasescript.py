import pandas as pd

#square chip#
chip_x = 0.002 #2mm
block_x = 0.0005 #500um
chiplabel="2mm"
num_blocks_x = int(chip_x / block_x)
total_blocks = num_blocks_x*num_blocks_x

######Floorplan###############
fname0 = "../flp_files/Tests_withHotSpot/L0_flp_4.csv"
fpartial0 = "Tests_withHotSpot/L0_flp_4.csv"
fname1 = "../flp_files/Tests_withHotSpot/L1_flp_4.csv"
fpartial1 = "Tests_withHotSpot/L1_flp_4.csv"
df0 = pd.DataFrame([],columns=['UnitName','X','Y','Length (m)','Width (m)','ConfigFile','Label'])
df1 = pd.DataFrame([],columns=['UnitName','X','Y','Length (m)','Width (m)','ConfigFile','Label'])
x_coord=0
y_coord=0
label0='Si'
label1='TwoPhaseVC'
for i in range(num_blocks_x):
    x_coord=0
    for j in range(num_blocks_x):
        uname="Unit_"+str(i)+"_"+str(j)
        cfile=''
        ff = pd.DataFrame([[uname,round(x_coord,6),round(y_coord,6),round(block_x,6),round(block_x,6),cfile,label0]],columns=['UnitName','X','Y','Length (m)','Width (m)','ConfigFile','Label'])
        df0 = df0.append(ff)
        ff = pd.DataFrame([[uname,round(x_coord,6),round(y_coord,6),round(block_x,6),round(block_x,6),cfile,label1]],columns=['UnitName','X','Y','Length (m)','Width (m)','ConfigFile','Label'])
        df1 = df1.append(ff)
        x_coord += block_x
    y_coord += block_x
#print(df)
df0.to_csv(fname0,index=False)
df1.to_csv(fname1,index=False)
############################

###### Uniform PTrace ###### and ###### LCF #######
#powerdensity = [100]
powerdensity = [20]
for p_num, PD in enumerate(powerdensity):
    power = round(PD *block_x*block_x*100*100,4)
#power = [0.05,0.25]
#for p_num, p in enumerate(power):
    df = pd.DataFrame([],columns=['UnitName','Power'])
    #PD = round(p/(block_x*block_x*100*100),3)
    print(PD,"W/cm2")
    pname = "../ptrace_files/Tests_withHotSpot/"+chiplabel+"_UniformPD_"+str(PD)+"Wcm2_ptrace.csv"
    ppartial = "Tests_withHotSpot/"+chiplabel+"_UniformPD_"+str(PD)+"Wcm2_ptrace.csv"
    for i in range(num_blocks_x):
        x_coord=0
        for j in range(num_blocks_x):
            uname="Unit_"+str(i)+"_"+str(j)
            ff = pd.DataFrame([[uname,power]],columns=['UnitName','Power'])
            df = df.append(ff)
    #print(df)
    df.to_csv(pname,index=False)

    lname = "../lcf_files/Tests_withHotSpot/lcf_4_UniformPD_"+str(PD)+"Wcm2.csv"
    print(lname,pname)
    df1 = pd.DataFrame([],columns=['Layer','FloorplanFile','Thickness (m)','PtraceFile','LateralHeatFlow'])
    ff1 = pd.DataFrame([[0,fpartial0,0.0001,ppartial,True]],columns=['Layer','FloorplanFile','Thickness (m)','PtraceFile','LateralHeatFlow'])
    df1 = df1.append(ff1)
    ff1 = pd.DataFrame([[1,fpartial1,0.0001,'',True]],columns=['Layer','FloorplanFile','Thickness (m)','PtraceFile','LateralHeatFlow'])
    df1 = df1.append(ff1)
    #print(df1)
    df1.to_csv(lname,index=False)
##############################

###### Non-Uniform PTrace ###### and ###### LCF #######
#bgpd = [50]
#hspd = [100,200,300]
bgpd = [20]
hspd = [25,50,75]

hs_loc = {'1HS':10} #run_idx=3 #2mm 
for bg in bgpd:
    for hs in hspd:
        bg_power = round(bg *block_x*block_x*100*100,4)
        hs_power = round(hs *block_x*block_x*100*100,4)
        df = pd.DataFrame([],columns=['UnitName','Power'])
        #print(PD,"W/cm2")
        pname = "../ptrace_files/Tests_withHotSpot/"+chiplabel+"_NonUniformPD_"+str(bg)+"_"+str(hs)+"Wcm2_ptrace.csv"
        ppartial = "Tests_withHotSpot/"+chiplabel+"_NonUniformPD_"+str(bg)+"_"+str(hs)+"Wcm2_ptrace.csv"
        for i in range(num_blocks_x):
            x_coord=0
            for j in range(num_blocks_x):
                uname="Unit_"+str(i)+"_"+str(j)
                if(i*num_blocks_x + j  == hs_loc['1HS']):
                    ff = pd.DataFrame([[uname,round(hs_power,6)]],columns=['UnitName','Power'])
                else:
                    ff = pd.DataFrame([[uname,round(bg_power,6)]],columns=['UnitName','Power'])

                df = df.append(ff)
        #print(df)
        df.to_csv(pname,index=False)

        lname = "../lcf_files/Tests_withHotSpot/lcf_4_NonUniformPD_"+str(bg)+"_"+str(hs)+"Wcm2.csv"
        print(lname,pname)
        df1 = pd.DataFrame([],columns=['Layer','FloorplanFile','Thickness (m)','PtraceFile','LateralHeatFlow'])
        ff1 = pd.DataFrame([[0,fpartial0,0.0001,ppartial,True]],columns=['Layer','FloorplanFile','Thickness (m)','PtraceFile','LateralHeatFlow'])
        df1 = df1.append(ff1)
        ff1 = pd.DataFrame([[1,fpartial1,0.0001,'',True]],columns=['Layer','FloorplanFile','Thickness (m)','PtraceFile','LateralHeatFlow'])
        df1 = df1.append(ff1)
        #print(df1)
        df1.to_csv(lname,index=False)
##############################
