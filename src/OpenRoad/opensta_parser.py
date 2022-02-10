"""

Generates power map

optional arguments:
  -h, --help  show this help message and exit
  --lib       Path to the library file
  --lef       Path to the lef file
  --deff      Path to the routed def file
  --resizer   Path to resizer binary files
  --clk       Clock period of the design"""


import os
import argparse
from pathlib import Path 



def read_file(filepath):
	try:
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


#Parses arguments from the command line 

def ParseArg():
	parser = argparse.ArgumentParser(description= 'Generates power map')
	parser.add_argument('--lib',type=str,required=True,metavar='', help='Path to the library file')
	parser.add_argument('--lef',type=str,required=True, metavar='',help='Path to the lef file')
	parser.add_argument('--deff',type=str,required=True, metavar='',help='Path to the routed def file')
	parser.add_argument('--resizer',type=str,required=True, metavar='',help='Path to resizer binary files')
	parser.add_argument('--clk',type=str,required=True, metavar='',help='Clock period of the design')
	return parser.parse_args()
	


#Writes a script file to be used by resizer 
		
def ScriptTemplate(args):
	line='read_liberty '
	line='%s %s %s'%(line,args.lib,'\n')
	write_file("Script_template",line)

	
	line='read_lef '
	line='%s %s %s'%(line,args.lef,'\n')
	write_file("Script_template",line)


	line='read_def '
	line='%s %s %s'%(line,args.deff,'\n')
	write_file("Script_template",line)


	line='create_clock -name clk -period '
	line='%s %s %s %s'%(line,args.clk,'{clk}','\n')
	write_file("Script_template",line)


	

#Parses the def file and returns the coordinates and the list of instances, as well as the associated resizer command

def ParseDef(args):
	inst=[]
	xcoord=[]
	ycoord=[]
	listline=read_file(args.deff)
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
	return command, xcoord,ycoord,inst;




# Runs resizer and parses its output to generate the output file that contains the coordinates and the power of each instance

def RunResizer(args,command,xcoord,ycoord,inst):
	stamylines=[]
	stainst=[]
	stapower=[]
	write_file("Script_template",command)
	exec_command='%s %s'%(args.resizer,' -exit Script_template')
	os.system(exec_command)
	stalistline=read_file('out')


	for line in stalistline:
		stamylines.append(line.split())

	for i in range(3,len(stamylines)):
		stapower.append(stamylines[i][3])
		stainst.append(stamylines[i][4])


	for i in range(len(stapower)):
		st=stapower[i]
		st='%s %s %s \n'%(st,xcoord[inst.index(stainst[i])],ycoord[inst.index(stainst[i])])
		write_file("outputhotspot",st)


if __name__ == "__main__":
	args=ParseArg()
	script_file = Path('Script_template')
	if script_file.is_file():
		print("Removing script template file")
		os.remove('Script_template')

	output_file = Path('outputhotspot')
	if output_file.is_file():
		print("Removing output file")
		os.remove('outputhotspot')
		
	ScriptTemplate(args)
	print("Parsing DEF file...")
	command,xcoord,ycoorrd,inst=ParseDef(args)
	print("Running Resizer...")
	RunResizer(args,command,xcoord,ycoorrd,inst)
	print("Script done. Output file is outputhotspot")
	os.rename('Script_template', 'Script_template_saved')
	
	
	

