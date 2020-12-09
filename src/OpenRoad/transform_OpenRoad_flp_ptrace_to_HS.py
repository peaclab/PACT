import sys
flp = sys.argv[1]
ptrace = sys.argv[2]
i = 0
flag = 0
with open(flp,'r') as myfile:
	lines = myfile.readlines()
	#print(lines[-1].split(' ')[-1])
	if int(lines[-1].split(' ')[-1])==0:
		flag = 1
		lines = lines[:-1]
	with open('hotspot.flp','w') as myfile_t:
		for line in lines:
			line = line.strip('\n')
			#print(line)
			myfile_t.write('unit_{} '.format(i))
			temp = line.split(' ')
			for item in temp:
				myfile_t.write(str(float(item)/2000e6)+' ')
			myfile_t.write('\n')
			i+=1
	with open('hotspot.ptrace','w') as myfile_t:
		with open(ptrace,'r') as myfile:
			for line in myfile:
				line = line.strip('\n ')
				temp = line.split(' ')
				if flag==1:
		    			temp.pop()
				sum = 0
			for item in temp:
				sum+=float(item)
			print(f"total power (W):{sum}")
			for i in range(0,len(temp)):
				myfile_t.write('unit_{} '.format(i))
			myfile_t.write('\n')
			myfile_t.write(' '.join(temp)+'\n')
