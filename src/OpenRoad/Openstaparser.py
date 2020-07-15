import os
import argparse 

parser= argparse.ArgumentParser(description= 'Generates power map')
parser.add_argument('--lib',type=str,required=True,metavar='', help='Path to the library file')
parser.add_argument('--lef',type=str,required=True, metavar='',help='Path to the lef file')
parser.add_argument('--deff',type=str,required=True, metavar='',help='Path to the routed def file')
parser.add_argument('--resizer',type=str,required=True, metavar='',help='Path to resizer binary files')
parser.add_argument('--clk',type=str,required=True, metavar='',help='Clock period of the design')

args= parser.parse_args()
line='read_liberty '
line='%s %s %s'%(line,args.lib,'\n')
f = open("Script_template", "a")
f.write(line)
f.close


line='read_lef '
line='%s %s %s'%(line,args.lef,'\n')
f = open("Script_template", "a")
f.write(line)
f.close

line='read_def '
line='%s %s %s'%(line,args.deff,'\n')
f = open("Script_template", "a")
f.write(line)
f.close

line='create_clock -name clk -period '
line='%s %s %s %s'%(line,args.clk,'{clk}','\n')
f = open("Script_template", "a")
f.write(line)
f.close





fp=open(args.deff)
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


exec_command='%s %s'%(args.resizer,' -exit script')
os.system(exec_command)

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


