import os
from pathlib import Path
flp_dir = os.getcwd()
flp_path = f"{flp_dir}/HotSpot_flp/"
flps = Path(flp_path).glob("**/*flp")
for flp in flps:
	flp_mat = []
	with open(flp,"r") as hsflp:
		flp_name = str(flp).split('/')[-1].split('.')[0]
		print(flp_name)
		for line in hsflp:
			line = line.strip().split('\t')
			line[1],line[3] = line[3],line[1]
			line[2],line[4] = line[4],line[2]
			line.append('')
			line.append('Si')
			flp_mat.append(",".join(line))
			#print(" ".join(line))
	with open(f"flp_files/{flp_name}_flp.csv","w") as pactflp:
		pactflp.write("UnitName,X,Y,Length (m),Width (m),ConfigFile,Label\n")
		for item in flp_mat:
			pactflp.write(item+"\n")
'''
		line = item.split(',')
		print(line[1],line[2],line[3],line[4])
		if float(line[1])+float(line[3])< float(line[2])+float(line[4]):
			unit_name = line[0].split('_')[-1] 
			new_unit_name = 'unit_'+str(int(unit_name)+1)
			gap = round(float(line[2])+float(line[4])-float(line[1])-float(line[3]),10)
			newline = [1,2,3,4,5]
			newline[1] = round(float(line[1])+float(line[3]),10)
			newline[2] = 0.0
			newline[3] = gap
			newline[4] = round(float(line[2])+float(line[4]),10)
			pactflp.write(new_unit_name+','+str(newline[1])+','+str(newline[2])+','+str(newline[3])+','+str(newline[4])+',,'+'Si')
		elif float(line[1])+float(line[3])> float(line[2])+float(line[4]):
			unit_name = line[0].split('_')[-1] 
			new_unit_name = 'unit_'+str(int(unit_name)+1)
			gap = round(float(line[1])+float(line[3])-float(line[2])-float(line[4]),10)
			newline = [1,2,3,4,5]
			newline[1] = 0.0
			newline[2] = round(float(line[2])+float(line[4]),10)
			newline[3] = round(float(line[1])+float(line[3]),10)
			newline[4] = gap
			pactflp.write(new_unit_name+','+str(newline[1])+','+str(newline[2])+','+str(newline[3])+','+str(newline[4])+',,'+'Si')
'''			
