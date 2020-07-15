import argparse 

parser= argparse.ArgumentParser(description= 'Generates power map')
parser.add_argument('--deff',type=str,required=True, metavar='',help='Path to the routed def file')
parser.add_argument('--gridsize',type=int,required=True, metavar='',help='gridsize')
args= parser.parse_args()






fp=open(args.deff)
gridsize=args.gridsize
power_blocks=[0.0]*gridsize*gridsize
xcoord_blocks=[]
ycoord_blocks=[]
mylines=[]


listline=fp.readlines()
mylines=[]

for line in listline:
        mylines.append(line.split())

for i in range(len(mylines)):
        if(len(mylines[i])!=0):
                if(mylines[i][0]=='DIEAREA'):
                        break

xdim=int(mylines[i][6])
ydim=int(mylines[i][7])

fp=open('./outputhotspot')
listlines=fp.readlines()

for line in listlines:
	mylines.append(line.split())

for i in range(len(mylines)):
	mylines[i][0]=float(mylines[i][0])
	mylines[i][1]=float(mylines[i][1])
	mylines[i][2]=float(mylines[i][2])

flags=[1]*len(mylines)
block_index=-1

for i in range(0,xdim-1,int(xdim/gridsize)):
        for j in range(0,ydim-1,int(ydim/gridsize)):
                xcoord_blocks.append(i)
                ycoord_blocks.append(j)
                block_index=block_index+1
                for z in range(len(mylines)):
                        if(flags[z]):
                                if(i<=mylines[z][1]<i+xdim/gridsize and j<=mylines[z][2]<j+ydim/gridsize):
                                        flags[z]=0
                                        power_blocks[block_index]=power_blocks[block_index]+mylines[z][0]


for i in range(len(power_blocks)):
        st='%s %s %s %s\n'%(int(xdim/gridsize),int(ydim/gridsize),xcoord_blocks[i],ycoord_blocks[i])
        with open("flp", "a") as f:
                f.write(st)

for i in range(len(power_blocks)):
        st='%s '%(power_blocks[i])
        with open("ptrace", "a") as f:
                f.write(st)



