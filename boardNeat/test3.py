from bareSnake import snakeGame

a = snakeGame()

a.move_up()
a.move_up()
a.move_up()
a.move_up()
a.move_up()
for i in a.history:
	print(i)


print(a.toString())
print(a.propDirect([10,0]))
print(a.propDirect([0,10]))
print(a.propDirect([-10,0]))
print(a.propDirect([0,-10]))

print(a.propDirect([10,10]))
print(a.propDirect([-10,10]))
print(a.propDirect([10,-10]))
print(a.propDirect([-10,-10]))
print("asdf")