import numpy as np 

def makeList(mat):
	hld = []
	for i in mat:
		for j in i:
			print(j)
			hld.append(j)
	return hld

a = np.ones((3,2))

b = makeList(a)

print(b)