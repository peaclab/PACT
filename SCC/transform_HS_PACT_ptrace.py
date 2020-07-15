import os
from pathlib import Path
ptrace_dir = os.getcwd()
ptrace_path = f"{ptrace_dir}/HotSpot_ptrace/"
ptraces = Path(ptrace_path).glob("**/*ptrace")
for ptrace in ptraces:
	unit_name = []
	ptrace_val = []
	with open(ptrace,"r") as hsptrace:
		ptrace_name = str(ptrace).split('/')[-1].split('.')[0]
		print(ptrace_name)			
		hsptrace = hsptrace.readlines()
		unit_name = str(hsptrace[0]).strip().split('\t')
		ptrace_val = str(hsptrace[1]).strip().split('\t')
	with open(f"ptrace_files/{ptrace_name}_ptrace.csv","w") as pactptrace:
		pactptrace.write("UnitName,Power\n")
		for idx,val in enumerate(unit_name):
			pactptrace.write(f"{unit_name[idx]},{ptrace_val[idx]}\n")
	#	pactptrace.write(f"unit_16384,0\n")
