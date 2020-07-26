"""usage: gridmesh.py [-h] --deff  --gridsize

Generates power map

optional arguments:
  -h, --help   show this help message and exit
  --deff       Path to the routed def file
  --gridsize   gridsize"""

import argparse 
import sys
import os.path



def read_file(filepath):
	try:
		if(os.path.exists(filepath)==False):
			print("Error ! the following file does not exist : ",filepath)
			exit()
		with open(filepath, 'r') as f:
			return f.readlines()
	except IOError:
		 print('Could not read the following file:',filepath)
	
		
def write_file(filepath,line):
	try:		
		with open(filepath, 'a') as f:
			f.write(line)
		f.close()
	except IOError:
		print('Could not write in the following file:',filepath)


# Parses the arguments from the command line
def ParseArg():
	parser= argparse.ArgumentParser(description= 'Generates power map')
	parser.add_argument('--deff',type=str,required=True, metavar='',help='Path to the routed def file')
	parser.add_argument('--gridsize',type=int,required=True, metavar='',help='gridsize')
	return parser.parse_args()



# Parses the design dimensions from the def file
def DesignDim(args):	
	mylines=[]
	
	listline=read_file(args.deff)

	for line in listline:
		mylines.append(line.split())

	for i in range(len(mylines)):
		if(len(mylines[i])!=0):
			if(mylines[i][0]=='DIEAREA'):
				break

	xdim=int(mylines[i][6])
	ydim=int(mylines[i][7])
	return xdim,ydim;


# Generates the grid " flp" contains the coordinates and dimensions and "ptrace" contains the power values
def GenerateGrid(args,xdim,ydim):
	mylines=[]
	power_blocks=[0.0]*args.gridsize*args.gridsize
	xcoord_blocks=[]
	ycoord_blocks=[]
	listlines=read_file('outputhotspot')
	
	for line in listlines:
		mylines.append(line.split())
		
	for i in range(len(mylines)):
		mylines[i][0]=float(mylines[i][0])
		mylines[i][1]=float(mylines[i][1])
		mylines[i][2]=float(mylines[i][2])

	flags=[1]*len(mylines)
	block_index=-1
	
	for i in range(0,xdim-1,int(xdim/args.gridsize)):
		for j in range(0,ydim-1,int(ydim/args.gridsize)):
			xcoord_blocks.append(i)
			ycoord_blocks.append(j)
			block_index=block_index+1
			for z in range(len(mylines)):
				if(flags[z]):
					if(i<=mylines[z][1]<i+xdim/args.gridsize and j<=mylines[z][2]<j+ydim/args.gridsize):
						flags[z]=0
						power_blocks[block_index]=power_blocks[block_index]+mylines[z][0]

	for i in range(len(power_blocks)):
		st='%s %s %s %s\n'%(int(xdim/args.gridsize),int(ydim/args.gridsize),xcoord_blocks[i],ycoord_blocks[i])
		write_file('flp',st)

	for i in range(len(power_blocks)):
		st='%s '%(power_blocks[i])
		write_file('ptrace',st)



if __name__ == "__main__":
	args= ParseArg()
	xdim,ydim= DesignDim(args)
	GenerateGrid(args,xdim,ydim)
	


