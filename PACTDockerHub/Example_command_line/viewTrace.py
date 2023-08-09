from matplotlib import pyplot as plt
with open("example.block.transient.csv",'r') as myfile:
	lines = myfile.readlines()
	array = []
	count = 0 
	for line in lines:
		if line[0] == "2":
			if count%3==0:
				line = line.strip().split(' ')
				array.append(float(line[-1]))
			count+=1
print(array)
plt.plot(array)
plt.savefig("Ttrace.png")
