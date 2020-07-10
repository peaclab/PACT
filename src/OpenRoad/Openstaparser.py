import os

fp=open('./routed.def')
listline=fp.readlines()

mylines=[]
for line in listline:
	mylines.append(line.split())

for i in range(len(mylines)):
	if(len(mylines[i])!=0):
		if(mylines[i][0]=='COMPONENTS'):
			break

start=i+1

for j in range(start,len(mylines)):
        if(len(mylines[j])!=0):
                if(mylines[j][0]=='END'):
                        break

end=j
inst=[]
xcoord=[]
ycoord=[]

for i in range(start,end):
	if(len(mylines[i])>1):
		inst.append(mylines[i][1])
		xcoord.append(mylines[i][mylines[i].index('(')+1])
		ycoord.append(mylines[i][mylines[i].index('(')+2])

for i in range(len(inst)):
	inst[i]=inst[i].replace('\\','')

command='report_power -instances "'

for i in range(0,len(inst)):
	command='%s %s'%(command,inst[i])

command='%s" > out'%(command)


with open("script", "a") as f:
	f.write(command)


os.system('/local-disk/tools/OpenROAD/alpha-release/openroad/OpenROAD-2019-07-30_05-17/bin/resizer -exit script')

fp=open('out')
stalistline=fp.readlines()

stamylines=[]
stainst=[]
stapower=[]

for line in stalistline:
         stamylines.append(line.split())

for i in range(3,len(stamylines)):
	stapower.append(stamylines[i][3])
	stainst.append(stamylines[i][4])


for i in range(len(stapower)):
	st=stapower[i]
	st='%s %s %s \n'%(st,xcoord[inst.index(stainst[i])],ycoord[inst.index(stainst[i])])
	with open("outputhotspot", "a") as f:
		f.write(st)


