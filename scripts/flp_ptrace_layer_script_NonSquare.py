import pandas as pd

#square chip#
#chiplabel="10mm"
#chip_x = 0.01 #10mm
#chip_x = 0.005 #5mm
#block_x = 0.0005 #500um

chiplabel="2x5mm"
chip_x = 0.002 #2mm
chip_y = 0.005 #5mm
block_x = 0.0005 #500um
block_y = 0.0005 #500um
num_blocks_x = int(chip_x / block_x)
num_blocks_y = int(chip_y / block_y)
print(num_blocks_x,num_blocks_y)
total_blocks = num_blocks_x*num_blocks_y

######Floorplan###############
fname = "../flp_files/Tests_withHotSpot/"+chiplabel+"_flp.csv"
fpartial = "Tests_withHotSpot/"+chiplabel+"_flp.csv"
df = pd.DataFrame([],columns=['UnitName','X','Y','Length (m)','Width (m)','ConfigFile','Label'])
x_coord=0
y_coord=0
label='Si'
for i in range(num_blocks_y):
    x_coord=0
    for j in range(num_blocks_x):
        uname="Unit_"+str(i)+"_"+str(j)
        cfile=''
        ff = pd.DataFrame([[uname,round(x_coord,6),round(y_coord,6),round(block_x,6),round(block_x,6),cfile,label]],columns=['UnitName','X','Y','Length (m)','Width (m)','ConfigFile','Label'])
        df = df.append(ff)
        x_coord += block_y
    y_coord += block_y
#print(df)
df.to_csv(fname,index=False)
############################

############## Uniform Ptrace and LCF #################
powerdensity = [50,100,150,200]
for p_num, PD in enumerate(powerdensity):
    power = round(PD * 100 * 100 * block_x * block_y,8) 
    df = pd.DataFrame([],columns=['UnitName','Power'])
    print(PD,"W/cm2 (Uniform)")
    print("power:",power)
    pname = "../ptrace_files/Tests_withHotSpot/"+chiplabel+"_UniformPD_"+str(PD)+"Wcm2_ptrace.csv"
    ppartial = "Tests_withHotSpot/"+chiplabel+"_UniformPD_"+str(PD)+"Wcm2_ptrace.csv"
    for i in range(num_blocks_y):
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

############## Non - Uniform Ptrace and LCF #################
bgpd = [50]
hspd = [500,1000,1500,2000]
center_loc = [17,18,21,22]
multiple_loc = [5,14,26,34]
hs_loc = ['center','edge','corner','multiple']
locations = {'center':center_loc,'edge':[int(num_blocks_x/2)], 'corner':[0],'multiple':multiple_loc}

for bg in bgpd:
    bg_power = round(bg * 100 * 100 * block_x * block_y,8) 
    for hs in hspd:
        hs_power = round(hs * 100 * 100 * block_x * block_y,8) 
        for loc in hs_loc:
            df = pd.DataFrame([],columns=['UnitName','Power'])
            #print(PD,"W/cm2")
            pname = "../ptrace_files/Tests_withHotSpot/"+chiplabel+"_NonUniformPD_"+loc+str(bg)+"_"+str(hs)+"Wcm2_ptrace.csv"
            ppartial = "Tests_withHotSpot/"+chiplabel+"_NonUniformPD_"+loc+str(bg)+"_"+str(hs)+"Wcm2_ptrace.csv"
            for i in range(num_blocks_y):
                x_coord=0
                for j in range(num_blocks_x):
                    uname="Unit_"+str(i)+"_"+str(j)
                    #if(num_blocks_x*i + j in locations[loc]):
                    if(num_blocks_x*i + j in locations[loc]):
                        ff = pd.DataFrame([[uname,round(hs_power,8)]],columns=['UnitName','Power'])
                    else:
                        ff = pd.DataFrame([[uname,round(bg_power,8)]],columns=['UnitName','Power'])
                    df = df.append(ff)
            #print(df)
            df.to_csv(pname,index=False)

            lname = "../lcf_files/Tests_withHotSpot/"+chiplabel+"_lcf_NonUniformPD_"+loc+str(bg)+"_"+str(hs)+"Wcm2.csv"
            print(lname,pname)
            df1 = pd.DataFrame([],columns=['Layer','FloorplanFile','Thickness (m)','PtraceFile','LateralHeatFlow'])
            ff1 = pd.DataFrame([[0,fpartial,0.0001,ppartial,True]],columns=['Layer','FloorplanFile','Thickness (m)','PtraceFile','LateralHeatFlow'])
            df1 = df1.append(ff1)
            #print(df1)
            df1.to_csv(lname,index=False)
##############################
