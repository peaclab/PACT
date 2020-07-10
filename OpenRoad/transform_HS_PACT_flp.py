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
			line = line.strip().split(' ')
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
