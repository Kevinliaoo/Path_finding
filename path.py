import pygame
import math 
import random

# ----- Constants ----- 
WIDTH = 600
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
OBSTACLE_COLOR = (0, 0, 0)
FREE_COLOR = (255, 255, 255)
END_COLOR = (0, 21, 255)
PURPLE = (185, 8, 255)
LINE_COLOR = (168, 166, 158)
START_COLOR = (255, 135, 8)
OPEN_COLOR = (52, 235, 180)

# Display setting
WIN = pygame.display.set_mode ((WIDTH, WIDTH))
pygame.display.set_caption ("Path finding algorithm visualization")

# ----- Classes -----
class Pixel: 
	# Spot

	def __init__ (self, row, column, width, total_rows): 
		self.row = row
		self.column = column
		self.width = width
		self.x = row * width
		self.y = column * width
		self.color = FREE_COLOR
		self.name = "FREE"
		self.neighbors = []
		self.total_rows = total_rows
		self.dijkstraDistance = 0	# For Dijkstra algorithm
		self.G = 0		# Distance from starting node
		self.H = 0		# Distance from end node
		self.F = 0		# G + H
		self.previous = None

	def getCoords (self): 
		# get_pos
		return self.row, self.column

	def getColor (self): 
		"""
		"RED" --> A* path
		"GREEN" --> Searching path
		"OBSTACLE" --> Obstacle
		"START" --> Start point
		"END" --> End point
		"FREE" --> Free pixel
		"PURPLE" --> Dijkstra path
		"OPEN" --> A star open 
		"""
		return self.name

	def setColor (self, name, color):
		self.name = name
		self.color = color

	def draw (self, window): 
		pygame.draw.rect (window, self.color, (self.x, self.y, self.width, self.width))

	def updateNeighbors (self, grid): 
		self.neighbors = []
		# Down neighbor
		if self.row < self.total_rows - 1 and not grid[self.row+1][self.column].getColor() == "OBSTACLE":
			self.neighbors.append (grid[self.row+1][self.column])
		# Up neighbor
		if self.row > 0 and not grid[self.row-1][self.column].getColor() == "OBSTACLE":
			self.neighbors.append (grid[self.row-1][self.column])
		# Right neighbor
		if self.column < self.total_rows - 1 and not grid[self.row][self.column+1].getColor() == "OBSTACLE":
			self.neighbors.append (grid[self.row][self.column+1])
		# Left neighbor
		if self.column > 0 and not grid[self.row][self.column-1].getColor() == "OBSTACLE":
			self.neighbors.append (grid[self.row][self.column-1])

	def __lt__ (self, other): 
		"""
		Less than
		"""
		return False

class Queue: 

	def __init__ (self): 
		self._queue = []

	def enqueue (self, value): 
		self._queue.append (value)

	def dequeue (self): 
		self._queue.pop(0)

	def next (self): 
		try: 
			return self._queue[0]
		except: 
			return False

	def isEmpty (self): 
		return len (self._queue) == 0

	def see (self): 
		print (len(self._queue))

class PriorityQueue: 

	def __init__ (self): 
		self.queue = {}

	def isNone (self): 
		return len(self.queue) == 0

	def enqueue (self, data, priority): 
		if priority in self.queue: 
			temp = self.queue[priority]
			temp.add (data)
			self.queue[priority] = temp

		else: 
			self.queue[priority] = {data}

	def dequeue (self): 

		if len(self.queue) == 0: 
			return False

		else: 
			minPriority = min (self.queue.keys())
			guest = self.queue[minPriority]

			if len(guest) == 1: 
				self.queue.pop (minPriority)

			return guest.pop()

# ----- Functions -----
def heuristic (pixel1, pixel2):
	"""
	Returns the Manhattan distance.
	:param pixel1: Pixel
	:param pixel2: Pixel
	:returns: int
	""" 
	x1, y1 = pixel1.getCoords()
	x2, y2 = pixel2.getCoords()
	return abs (x1 - x2) + abs (y1 - y2)

def makeGrid (rows, width): 
	"""
	This function constructs and returns the matrix grid.
	:param rows: int
	:param width: int
	:returns: list
	"""
	grid = []
	size = width // rows

	for i in range (rows): 
		temp = []
		for j in range (rows): 
			pixel = Pixel (i, j, size, rows)
			if i == 0 or j == 0 or i == rows-1 or j == rows-1: 
				pixel.setColor ("OBSTACLE", OBSTACLE_COLOR)
			temp.append (pixel)
		grid.append (temp)

	return grid

def drawLines (window, rows, width): 
	"""
	This function draws the grid lines in the window.
	:param window: pygame.Surface
	:param rows: int
	:param width: int
	"""
	size = width // rows

	for i in range (rows): 
		pygame.draw.line (window, LINE_COLOR, (0, i * size), (width, i * size))

		for j in range (rows): 
			pygame.draw.line (window, LINE_COLOR, (j * size, 0), (j * size, width))

def draw (window, grid, rows, width): 
	"""
	This functions draws on the grid. 
	First, it draws each pixel, 
	then, overdraws with the gridlines. 
	:param window: pygame.Surface
	:param grid: list
	:param rows: int
	:param width: int
	"""
	window.fill (FREE_COLOR)

	for line in grid: 
		
		for pixel in line: 
			pixel.draw (window)

	drawLines (window, rows, width)
	pygame.display.update()

def getClickedPosition (position, rows, width): 
	"""
	This function returns the grid position. 
	It translates the clicked coordenates to the grid matrix position.
	:param position: tuple
	:param rows: int
	:param width: int
	:returns: tuple
	"""
	size = width // rows
	y, x = position
	row = y // size
	col = x // size
	return row, col

def Dijkstra (drawFunc, grid, start, end): 
	"""
	Runs Dijkstra path finding algorith.
	"""
	pygame.display.set_caption ("Running Dijkstra algorithm...")
	queue = Queue()
	# Starts from end 
	for neighbor in end.neighbors: 
		neighbor.setColor ("GREEN", GREEN)
		neighbor.dijkstraDistance = 1
		queue.enqueue (neighbor)

	run = True
	# Path finding
	while run:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		if queue.isEmpty(): 
			run = False

		# Get all the neighbors of next in queue
		nxt = queue.next()
		if nxt == False: 
			# Error, could not find the path
			return False

		for n in nxt.neighbors: 
			# Found the goal 
			if n == start: 
				run = False
			if n.name != "FREE": 
				continue

			else: 
				n.setColor ("GREEN", GREEN)
				n.dijkstraDistance = nxt.dijkstraDistance + 1
				queue.enqueue (n)

		queue.dequeue()
		drawFunc()

	# Get path
	temp = start
	while True: 
		# Printing the path from start to end
		nearest = getNearestNeighbor(temp)
		temp = nearest
		if temp == end: 
			break
		nearest.setColor ("PURPLE", PURPLE)
		drawFunc()

def aStar (drawFunc, grid, start, end): 
	"""
	Runs Dijkstra path finding algorith.
	"""
	pygame.display.set_caption ("Running A* algorithm...")
	queue = PriorityQueue()

	# Start from startpoint
	for n in start.neighbors: 
		n.previous = start
		n.setColor ("OPEN", OPEN_COLOR)
		n.G = 1
		n.H = heuristic (n, end)
		n.F = 1 + heuristic (n, end)
		queue.enqueue (n, n.F)

	run = True
	while run:
		drawFunc()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		if queue.isNone(): 
			# Path not found
			run = False

		nxt = queue.dequeue()
		if nxt == False:
			# Path not found 
			return False

		nxt.setColor ("GREEN", GREEN)
		for i in nxt.neighbors: 
			if end == i: 
				end.previous = nxt
				run = False
			if i.name == "FREE": 
				i.previous = nxt
				i.setColor ("OPEN", OPEN_COLOR)
				i.G = nxt.G + 1
				i.H = heuristic (i, end)
				i.F = i.H + i.G
				queue.enqueue (i, i.F)

	temp = end
	while True: 
		# Printing the path from end to start
		temp = temp.previous
		if temp == start: 
			break
		temp.setColor ("RED", RED)
		drawFunc()

def getNearestNeighbor (pixel): 
	"""
	This function returns the neightbor pixel with the smallest distance to the endpoint. 
	:param pixel: Pixel
	:returns: Pixel
	"""
	distances = []
	pixels = []

	for n in pixel.neighbors: 
		if n.name == "END": 
			return n
		if n.name == "GREEN": 
			distances.append (n.dijkstraDistance)
			pixels.append (n)

	minValue = min (distances)
	minIndex = distances.index (minValue)
	return (pixels[minIndex])

def generateRandom (grid): 
	"""
	This function randomly generates a map. 
	:param grid: grid
	:returns: grid
	"""
	points = 500
	while points > 0: 
		x = random.randint(1, len(grid)-1)
		y = random.randint(1, len(grid)-1)

		if grid[y][x].name == "FREE": 
			grid[y][x].setColor ("OBSTACLE", OBSTACLE_COLOR)
			points -= 1

	return grid

def main (window, width): 
	"""
	Main function
	"""
	ROWS = 40
	grid = makeGrid (ROWS, width)

	start = None	# Startpoint
	end = None		# Endpoint
	run = True 		# Run
	started = False	# Algorithm running
	mapGen = False

	while run: 
		draw (WIN, grid, ROWS, WIDTH)	# Refresh screen

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				run = False

			if event.type == pygame.KEYDOWN: 

				# Press P to randomly generate a map 
				if event.key == pygame.K_p and started == False and mapGen == False:
					grid = generateRandom(grid)
					mapGen = True

				# Press R to restart the game once the algorithm finished executing
				if event.key == pygame.K_r and started:
					pygame.display.set_caption ("Path finding algorithm visualization")
					started = False
					start = None
					end = None
					mapGen = False
					grid = makeGrid (ROWS, width)

				# Press C to clear the grid
				if event.key == pygame.K_c and started: 
					pygame.display.set_caption ("Path finding algorithm visualization")
					started = False
					newGrid = makeGrid (ROWS, width)

					for y, row in enumerate (grid): 

						for x, pixel in enumerate (row): 

							if pixel.name == "OBSTACLE" or pixel.name == "START" or pixel.name =="END": 
								newGrid[y][x] = pixel

					grid = newGrid

			if started: 
				# Block following events once the event was excecuted
				continue

			if pygame.mouse.get_pressed()[0]:
				# Left mouse button
				# Add obstacles
				position = pygame.mouse.get_pos()
				row, col = getClickedPosition (position, ROWS, width)
				pixel = grid[row][col]
				if not start and pixel != end: 
					# First, place the start position 
					start = pixel 
					start.setColor ("START", START_COLOR)
				elif not end and pixel != start: 
					# Secondly, place the end position
					end = pixel 
					end.setColor ("END", END_COLOR)
				elif pixel != end and pixel != start: 
					# At last, place obstacles
					pixel.setColor ("OBSTACLE", OBSTACLE_COLOR)

			elif pygame.mouse.get_pressed()[2]: 
				# Right mouse button
				# Remove obstacles
				position = pygame.mouse.get_pos()
				row, col = getClickedPosition (position, ROWS, width)
				
				# Do not allow to delete the border
				if row == 0 or col == 0 or row == len(grid)-1 or col == len(grid)-1:
					continue

				pixel = grid[row][col]
				pixel.setColor ("FREE", FREE_COLOR)
				if pixel == start: 
					start = None
				elif pixel == end: 
					end = None

			if event.type == pygame.KEYDOWN: 

				# Run A* algorithm
				if event.key == pygame.K_a and not started: 

					if start == None and end == None: 
						continue
					started = True
						
					for row in grid: 
						for pixel in row: 
							pixel.updateNeighbors (grid)

					result = aStar (lambda: draw(WIN, grid, ROWS, WIDTH), grid, start, end)
					if result == False: 
						pygame.display.set_caption ("Could not find any path!")
					else: 
						pygame.display.set_caption ("Shortest path found!")

				# Run Dijkstra algorith
				if event.key == pygame.K_d and not started: 

					if start == None or end == None: 
						continue
					started = True

					for row in grid: 
						for pixel in row: 
							pixel.updateNeighbors (grid)

					result = Dijkstra (lambda: draw(WIN, grid, ROWS, WIDTH), grid, start, end)
					if result == False: 
						pygame.display.set_caption ("Could not find any path!")
					else: 
						pygame.display.set_caption ("Shortest path found!")
					
	pygame.quit()

if __name__ == '__main__':
	main(WIN, WIDTH)