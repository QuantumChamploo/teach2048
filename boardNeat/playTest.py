from bareSnake import snakeGame

a = snakeGame()

loop = True

while loop:
    print(a.direction)
    print(a.pos[0])
    print(a.pos[1])
    print(a.gameOver)
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

    print(a.nearWall())
    print(a.pos)

    x = input("enter a command \n")
    if x == "a":
        a.move_left()
        #print(a.toString())
    if x == "s":
        a.move_down()
        #print(a.toString())
    if x == "d":
        a.move_right()
        #print(a.toString())
    if x == "w":
        a.move_up()
        #print(a.toString())
    if x == "h":
        loop = False
    if a.checkGame() == False:
        print("you died")
        loop = False