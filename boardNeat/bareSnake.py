import sys, time, random
import numpy as np
np.set_printoptions(threshold=np.inf,linewidth=1000)

# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 25

# Window size
frame_size_x = 300
frame_size_y = 200


class snakeGame():
	def __init__(self):
		self.pos = [100, 50]
		self.body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
		self.food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
		self.food_spawn = True
		self.direction = 'right'
		self.change_to = self.direction
		self.score = 0
		self.gameOver = False
		self.history = []
		self.history.append(self.toString())
		self.popCount = 0

	def move_up(self):
		if self.direction != 'down':
			self.direction = 'up'
			self.pos[1] -= 10
		self.moveGrow()
		self.history.append(self.toString())
	def move_down(self):
		if self.direction != 'up':
			self.direction = 'down'
			self.pos[1] += 10
		self.moveGrow()
		self.history.append(self.toString())
	def move_left(self):
		if self.direction != 'right':
			self.direction = 'left'
			self.pos[0] -= 10
		self.moveGrow()
		self.history.append(self.toString())
	def move_right(self):
		if self.direction != 'left':
			self.direction = 'right'
			self.pos[0] += 10
		self.moveGrow()
		self.history.append(self.toString())
	def move_straight(self):
		if self.direction == 'right':
			self.move_right()
		if self.direction == 'left':
			self.move_left()
		if self.direction == 'down':
			self.move_down()
		if self.direction == 'up':
			self.move_up()


	def moveGrow(self):
		self.body.insert(0,list(self.pos))
		if self.pos[0] == self.food_pos[0] and self.pos[1] == self.food_pos[1]:
			self.score += 1
			self.popCount = 0
			self.food_spawn = False
		else:
			self.popCount += 1
			self.body.pop()
		if not self.food_spawn:
			self.food_pos = [random.randrange(1, (frame_size_x//10)-1) * 10, random.randrange(1, (frame_size_y//10)-1) * 10]
		self.food_spawn = True

	def checkGame(self):
		if self.pos[0] < 0 or self.pos[0] > frame_size_x - 20:
			self.gameOver = True
			return False
		if self.pos[1] < 0 or self.pos[1] > frame_size_y - 20:
			self.gameOver = True
			return False
		for block in self.body[1:]:
			if self.pos[0] == block[0] and self.pos[1] == block[1]:
				self.gameOver = True
				return False
		# print('x pos is')
		# print(self.pos[0])
		# print('y pos is')
		# print(self.pos[1])
		return True
	def toString(self):
		hld = np.zeros((int(frame_size_y/10),int(frame_size_x/10)))
		for val in self.body:
			x = int(val[0]/10)
			y = int(val[1]/10)
			# print('x is')
			# print(x)
			# print('y is')
			# print(y)
			hld[y,x] = 1
		foodX = self.food_pos[0]//10
		foodY = self.food_pos[1]//10
		hld[foodY,foodX] = -1
		return hld
		#print(hld)




