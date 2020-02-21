import pandas as pd

#square chip#
#chiplabel="10mm"
#chip_x = 0.01 #10mm
#chip_x = 0.005 #5mm
#block_x = 0.0005 #500um

#chiplabel="20mm"
#chip_x = 0.02 #20mm
#block_x = 0.0005 #1mm
#num_blocks_x = int(chip_x / block_x)
#total_blocks = num_blocks_x*num_blocks_x

chiplabel="5mm"
chip_x = 0.005 #20mm
block_x = 0.0005 #500um
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
powerdensity = [40,80,120,160,200]
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

############## Non - Uniform Ptrace and LCF #################
#bgpd = [20,30,40,50]
#hspd = [500,750,1000,1350,1500]
# For 10mm locations = {'center':[],'edge':[int(num_blocks_x/2)], 'corner':[0],'multiple_center':[189,190,209,210],'multiple_offcenter':[104,115,304,315]}
#locations = {'center':210}

bgpd = [30,50]
hspd = [500,1000,1500]
print(num_blocks_x)
#20mm location: hs_loc = ['center','edge','corner','multiple_center','multiple_offcenter']
#locations = {'center':[820],'edge':[int(num_blocks_x/2)], 'corner':[0],'multiple_center':[819,820,859,860],'multiple_offcenter':[409,430,1209,1230]}

hs_loc = ['center','edge','corner','multiple_center','multiple_offcenter']
locations = {'center':[55],'edge':[int(num_blocks_x/2)], 'corner':[0],'multiple_center':[44,45,54,55],'multiple_offcenter':[22,27,72,77]}

for bg in bgpd:
    bg_power = round(bg * 100 * 100 * block_x * block_x,8) 
    for hs in hspd:
        hs_power = round(hs * 100 * 100 * block_x * block_x,8) 
        for loc in hs_loc:
            df = pd.DataFrame([],columns=['UnitName','Power'])
            #print(PD,"W/cm2")
            pname = "../ptrace_files/Tests_withHotSpot/"+chiplabel+"_NonUniformPD_"+loc+str(bg)+"_"+str(hs)+"Wcm2_ptrace.csv"
            ppartial = "Tests_withHotSpot/"+chiplabel+"_NonUniformPD_"+loc+str(bg)+"_"+str(hs)+"Wcm2_ptrace.csv"
            for i in range(num_blocks_x):
                x_coord=0
                for j in range(num_blocks_x):
                    uname="Unit_"+str(i)+"_"+str(j)
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
