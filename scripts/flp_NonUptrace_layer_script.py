import pandas as pd

#square chip#
run="Run7"
#chip_x = 0.01 #10mm
#chip_x = 0.005 #5mm
#block_x = 0.0005 #500um
chip_x = 0.02 #20mm
block_x = 0.001 #1mm
num_blocks_x = int(chip_x / block_x)
total_blocks = num_blocks_x*num_blocks_x
#chiplabel="5mm"
chiplabel="20mm"

######Floorplan###############
#fname = "../flp_files/Tests_withHotSpot/L0_flp_1.csv" #10mm
#fpartial = "Tests_withHotSpot/L0_flp_1.csv"
#fname = "../flp_files/Tests_withHotSpot/L0_flp_2.csv" #5mm
#fpartial = "Tests_withHotSpot/L0_flp_2.csv"
fname = "../flp_files/Tests_withHotSpot/L0_flp_3.csv" #5mm
fpartial = "Tests_withHotSpot/L0_flp_3.csv"
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
bgpd = [20,30,40,50]
hspd = [500,750,1000,1350,1500]
#hs_loc = {'1HS':210} #run_idx=7 #10mm
#hs_loc = {'1HS':45} #run_idx=7 #5mm
hs_loc = {'1HS':210} #run_idx=7 #20mm w/ 1mm blocks
run_idx=7 #Run index starts from here
run="Run"
p_idx=0
fname=''
for bg_idx, bg in enumerate(bgpd):
    for hs_idx, hs in enumerate(hspd):
        df = pd.DataFrame([],columns=['UnitName','Power'])
        bg_power = round(bg*block_x*block_x*100*100,6)
        hs_power = round(hs*block_x*block_x*100*100,6)
        #print(bg_power,hs_power)
        #pname = "../ptrace_files/Tests_withHotSpot/P"+str(p_idx)+"_NonUniformPD"+str(bg)+"_"+str(hs)+"Wcm2_ptrace.csv"
        #ppartial = "Tests_withHotSpot/P"+str(p_idx)+"_NonUniformPD"+str(bg)+"_"+str(hs)+"Wcm2_ptrace.csv"
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
        #lname = "../lcf_files/Tests_withHotSpot/L0_lcf_1_NonUniformP"+str(p_idx)+".csv"
        #lname = "../lcf_files/Tests_withHotSpot/L0_lcf_2_NonUniformP"+str(p_idx)+".csv"
        lname = "../lcf_files/Tests_withHotSpot/L0_lcf_3_NonUniformP"+str(p_idx)+".csv"
        df1 = pd.DataFrame([],columns=['Layer','FloorplanFile','Thickness (m)','PtraceFile','LateralHeatFlow'])
        ff1 = pd.DataFrame([[0,fpartial,0.00015,ppartial,True]],columns=['Layer','FloorplanFile','Thickness (m)','PtraceFile','LateralHeatFlow'])
        df1 = df1.append(ff1)
        #print(df1)
        df1.to_csv(lname,index=False)
        p_idx += 1

##############################
