from bareSnake import snakeGame

a = snakeGame()

a.toString()
a.move_up()

a.toString()
a.move_left()
a.toString()
a.move_left()
a.toString()

a.move_left()
a.toString()
a.move_left()
a.toString()
a.move_left()
a.toString()
a.move_down()
a.move_straight()
a.toString()
a.toString()
a.move_right()
a.toString()
a.move_straight()
a.toString()
a.move_straight()
a.toString()
a.move_straight()
a.toString()
a.move_straight()
a.toString()
a.move_straight()
a.toString()

for i in range(50000):
	b = snakeGame()
	print(b.toString())
