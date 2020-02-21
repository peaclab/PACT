import pandas as pd

#square chip#
chip_x = 0.002 #2mm
block_x = 0.0005 #500um
chiplabel="Hetero_2mm"
width=[.002,.00075,0.0005,0.00075,0.002]
height=[.00075,0.0005,0.0005,0.0005,.00075]
x = [0,0,0.00075,0.00125,0]
y = [0,0.00075,0.00075,0.00075,0.00125]
label = ['Cu','Si','Cu','Si','Si']
total_blocks = 5

######Floorplan###############
fname0 = "../flp_files/Tests_withHotSpot/"+chiplabel+".csv"
fpartial0 = "Tests_withHotSpot/"+chiplabel+".csv"
#fpartial0 = "Tests_withHotSpot/L0_twophase.csv"
#fname1 = "../flp_files/Tests_withHotSpot/L1_twophase.csv"
#fpartial1 = "Tests_withHotSpot/L1_twophase.csv"
df0 = pd.DataFrame([],columns=['UnitName','X','Y','Length (m)','Width (m)','ConfigFile','Label'])
#df1 = pd.DataFrame([],columns=['UnitName','X','Y','Length (m)','Width (m)','ConfigFile','Label'])
x_coord=0
y_coord=0
for idx, i in enumerate(range(total_blocks)):
    uname="Block_"+str(i)
    cfile=''
    w = width[idx]
    h = height [idx]
    x_coord = x[idx]
    y_coord = y[idx]
    ff = pd.DataFrame([[uname,round(x_coord,6),round(y_coord,6),round(w,6),round(h,6),cfile,label[idx]]],columns=['UnitName','X','Y','Length (m)','Width (m)','ConfigFile','Label'])
    df0 = df0.append(ff)
#print(df)
df0.to_csv(fname0,index=False)

#ff = pd.DataFrame([['Block_0',0,0,round(chip_x,6),round(chip_x,6),cfile,label1]],columns=['UnitName','X','Y','Length (m)','Width (m)','ConfigFile','Label'])
#df1 = df1.append(ff)
#df1.to_csv(fname1,index=False)
############################

###### Uniform PTrace ###### and ###### LCF #######
powerdensity = [50,100,150,200]
#powerdensity = [20]
for p_num, PD in enumerate(powerdensity):
    power = [ round(PD * 100 * 100 * (i*j),6) for (i,j) in zip (width,height)] 
    df = pd.DataFrame([],columns=['UnitName','Power'])
    print(PD,"W/cm2")
    print("power",power)
    pname = "../ptrace_files/Tests_withHotSpot/"+chiplabel+"_UniformPD_"+str(PD)+"Wcm2_ptrace.csv"
    ppartial = "Tests_withHotSpot/"+chiplabel+"_UniformPD_"+str(PD)+"Wcm2_ptrace.csv"
    for idx, i in enumerate(range(total_blocks)):
        uname="Block_"+str(i)
        ff = pd.DataFrame([[uname,power[idx]]],columns=['UnitName','Power'])
        df = df.append(ff)
    print(df)
    df.to_csv(pname,index=False)

    lname = "../lcf_files/Tests_withHotSpot/"+chiplabel+"_lcf_UniformPD_"+str(PD)+"Wcm2.csv"
    print(lname,pname)
    df1 = pd.DataFrame([],columns=['Layer','FloorplanFile','Thickness (m)','PtraceFile','LateralHeatFlow'])
    ff1 = pd.DataFrame([[0,fpartial0,0.0001,ppartial,True]],columns=['Layer','FloorplanFile','Thickness (m)','PtraceFile','LateralHeatFlow'])
    df1 = df1.append(ff1)
    #ff1 = pd.DataFrame([[1,fpartial1,0.0001,'',True]],columns=['Layer','FloorplanFile','Thickness (m)','PtraceFile','LateralHeatFlow'])
    #df1 = df1.append(ff1)
    #print(df1)
    df1.to_csv(lname,index=False)
##############################

###### Non-Uniform PTrace ###### and ###### LCF #######
bgpd = [50]
hspd = [500,1000,1500,2000]
#bgpd = [20]
#hspd = [25,50,75]

for bg in bgpd:
    for hs in hspd:
        PD = [bg] * 2 + [hs] + [bg]*2
        power = []
        for p_idx, p in enumerate(PD):
            power = power +  [round(p * 100 * 100 * (width[p_idx]*height[p_idx]),6)]
        print(power)
        df = pd.DataFrame([],columns=['UnitName','Power'])
        #print(PD,"W/cm2")
        pname = "../ptrace_files/Tests_withHotSpot/"+chiplabel+"_NonUniformPD_"+str(bg)+"_"+str(hs)+"Wcm2_ptrace.csv"
        ppartial = "Tests_withHotSpot/"+chiplabel+"_NonUniformPD_"+str(bg)+"_"+str(hs)+"Wcm2_ptrace.csv"
        for idx, i in enumerate(range(total_blocks)):
            uname="Block_"+str(i)
            ff = pd.DataFrame([[uname,round(power[idx],6)]],columns=['UnitName','Power'])
            df = df.append(ff)
        print(df)
        df.to_csv(pname,index=False)

        lname = "../lcf_files/Tests_withHotSpot/"+chiplabel+"_lcf_NonUniformPD_"+str(bg)+"_"+str(hs)+"Wcm2.csv"
        print(lname,pname)
        df1 = pd.DataFrame([],columns=['Layer','FloorplanFile','Thickness (m)','PtraceFile','LateralHeatFlow'])
        ff1 = pd.DataFrame([[0,fpartial0,0.0001,ppartial,True]],columns=['Layer','FloorplanFile','Thickness (m)','PtraceFile','LateralHeatFlow'])
        df1 = df1.append(ff1)
        #ff1 = pd.DataFrame([[1,fpartial1,0.0001,'',True]],columns=['Layer','FloorplanFile','Thickness (m)','PtraceFile','LateralHeatFlow'])
        #df1 = df1.append(ff1)
        #print(df1)
        df1.to_csv(lname,index=False)
##############################
