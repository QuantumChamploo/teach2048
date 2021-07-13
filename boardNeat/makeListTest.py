from bareSnake import snakeGame

a = snakeGame()
def makeList(mat):
	hld = []
	for i in mat:
		for j in i:
			#print(j)
			hld.append(j)
	return hld


print(a.toString())
print("east")
print(a.propDirect([10, 0]))
print("south")
print(a.propDirect([0, 10]))
print("west")
print(a.propDirect([-10, 0]))
print("north")
print(a.propDirect([0, -10]))

print("south east")
print(a.propDirect([10, 10]))
print("south west")
print(a.propDirect([-10, 10]))
print("north east")
print(a.propDirect([10, -10]))
print("north west")
print(a.propDirect([-10, -10]))
print(makeList(a.sight))