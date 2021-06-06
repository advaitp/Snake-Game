import pygame 
import random
import tkinter as tk 
from tkinter import messagebox

class cube(object) :
	rows = 20
	width = 400
	def __init__(self, start, color = (0,0,255), dirx = 1, diry = 0) :
		# start is tuple of x and y cordinates (x, y)
		self.pos = start 
		self.color = color
		self.dirx = dirx
		self.diry = diry

	def move(self, dirx, diry) :
		self.diry = diry
		self.dirx = dirx
		# get the current position of the cube 
		self.pos = (self.pos[0]+self.dirx, self.pos[1]+self.diry)

	def draw(self, surface, rows = rows, width = width) :
		dist = self.width // self.rows 
		# get the current x and y of the box in the grid
		i = self.pos[0]
		j = self.pos[1]
		pygame.draw.rect(surface, self.color, (i*dist, j*dist, dist, dist))

class snake(object) :
	body = []
	def __init__(self, color, pos) :
		self.head = cube(pos)
		self.color = color
		self.body.append(self.head)
		self.dirx = 0
		self.diry = 1
		self.turns = {}

	def move(self) :
		for event in pygame.event.get() : 
  
		# if event object type is QUIT 
		# then quitting the pygame 
		# and program both. 
			if event.type == pygame.QUIT : 
	  
				# deactivates the pygame library 
				pygame.quit() 
	  
			else :
				# list of keys pressed
				keys = pygame.key.get_pressed()	

				for key in keys :
					if keys[pygame.K_LEFT] :
						self.dirx = -1
						self.diry = 0 
						# direction of head is represented by turns at particular position (x, y)
						self.turns[self.head.pos[:]] = [self.dirx, self.diry]


					elif keys[pygame.K_RIGHT] :
						self.dirx = 1
						self.diry = 0 
						# direction of head is represented by turns
						self.turns[self.head.pos[:]] = [self.dirx, self.diry]

					elif keys[pygame.K_UP] :
						self.dirx = 0
						self.diry = -1
						# direction of head is represented by turns
						self.turns[self.head.pos[:]] = [self.dirx, self.diry]

					elif keys[pygame.K_DOWN] :	
						self.dirx = 0
						self.diry = 1
						# direction of head is represented by turns
						self.turns[self.head.pos[:]] = [self.dirx, self.diry]

				# add the turns to each cube of the snake body 
				for i, c in enumerate(self.body) :
					if c.pos[:] in self.turns :
						c.move(self.turns[c.pos[:]][0], self.turns[c.pos[:]][1])
						# if i == len(self.body) :
						# 	self.turns.pop(c.pos[:])
					else :
						# check whether snake has crossed the boundaries	
						if c.dirx == -1 and c.pos[0] <= 0 : c.pos = (c.rows - 1, c.pos[1])
						elif c.dirx == 1 and c.pos[0] >= c.rows-1 : c.pos = (0, c.pos[1])
						elif c.diry == -1 and c.pos[1] <= 0 : c.pos = (c.pos[0], c.rows - 1)
						elif c.diry == 1 and c.pos[1] >= c.rows-1  : c.pos = (c.pos[0], 0)
						# random movement
						else : c.move(c.dirx, c.diry)

	# draw the snake current 
	def draw(self, surface) :
		for i, c in enumerate(self.body) :
			c.draw(surface)				


	def addCube(self) :
		tail = self.body[-1]
		dx, dy = tail.dirx, tail.diry
		# Snake catching the snack 
		if dx == 1 and dy == 0 :
			self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
		elif dx == -1 and dy == 0 :
			self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
		elif dx == 0 and dy == 1 :
			self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
		elif dx == 0 and dy == -1 :
			self.body.append(cube((tail.pos[0], tail.pos[1]+1)))

		# After adding the snack to the tail change the direction according to its tail direction
		self.body[-1].dirx, self.body[-1].diry = dx, dy	


	def reset(self, pos) :
		self.body = []
		self.head = cube(pos)
		self.body.append(self.head)
		self.turns = {}	
		self.dirx = 0
		self.diry = 1
							

def drawGrid(surface, rows, w) :
	spacing = w // rows
	x, y = 0, 0
	for j in range(rows) :
		x += spacing 
		y += spacing 

		# draw the line 
		pygame.draw.line(surface, (255,255,255), (x, 0), (x, w))
		pygame.draw.line(surface, (255,255,255), (0, y), (w, y))



def window(surface) :
	global rows, width, snake, snack
	# fill the surface with some color
	surface.fill((0,0,0))

	# draw grid on suface
	drawGrid(surface, rows, width)
	snake.draw(surface)
	snack.draw(surface)
	# Draws the surface object to the screen.   
	pygame.display.update()

def random_snack(rows, snake) :

	positions = snake.body
	while True :
		# Randomly create snack at any position except the position of snake body 
		x = random.randrange(rows)
		y = random.randrange(rows)

		if len(list(filter(lambda x:x.pos == (x,y), positions))) > 0 :
			continue
		else :
			break

	# return the random position of the snack
	return (x, y)		

def Message(subject, content) :
	root= tk.Tk()
	root.attributes("-topmost", True)
	root.withdraw()
	messagebox.showinfo(subject, content)
	try :
		root.destroy()
	except :
		pass	



def main() :
	# activate the pygame library 
	# initiate pygame and give permission 
	# to use pygame's functionality. 
	pygame.init()
	global width, rows, snake, snack

	# assigning values to X and Y variable 
	width = 400
	height = 400
	rows = 20 
	  
	# create the display surface object 
	# of specific dimension..e(X, Y). 
	display_surface = pygame.display.set_mode((width, height )) 

	# create the snake object from snake class
	snake = snake((0,0,255), (10,10))

	# create the snack object
	snack = cube(random_snack(rows, snake), color = (0,255,0))

	flag = True
	# create a clock object
	clock = pygame.time.Clock()

	while flag :
		# keep a delay
		pygame.time.delay(50)

		# use clock tick to control the frame rate speed at which snake should move
		clock.tick(10)

		# move the snake object using the keys 
		snake.move()

		# check if he head of snake has touched the snack
		if snake.body[0].pos == snack.pos : 
			# create new snack and add to snake
			snake.addCube()
			snack = cube(random_snack(rows, snake), color = (0,255,0))
			# snake.body.append(snack)

		for x in range(len(snake.body)) :
			if snake.body[x].pos in list(map(lambda x : x.pos , snake.body[x+1:])) :
				print(f'Your Score is {len(snake.body)}')
				Message(r'Game Over !', r'Play Again...')
				snake.reset((10,10))
				break



		# display the screen
		window(display_surface)

		for event in pygame.event.get() : 
  
		# if event object type is QUIT 
		# then quitting the pygame 
		# and program both. 
			if event.type == pygame.QUIT : 
	  
				# deactivates the pygame library 
				pygame.quit() 
	  
				# quit the program. 
				quit() 
			
			# Draws the surface object to the screen.   
			pygame.display.update()  

if __name__ == "__main__" :
	main()