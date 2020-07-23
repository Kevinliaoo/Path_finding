import pygame
import math 
from queue import PriorityQueue

# ----- Constants ----- 
WIDTH = 800
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TURQOISE = (8, 201, 255)
PURPLE = (185, 8, 255)
GREY = (168, 166, 158)
ORANGE = (255, 135, 8)

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
		self.color = WHITE
		self.neighbors = []
		self.total_rows = total_rows

	def getCoords (self): 
		# get_pos
		return self.row, self.column

	def isClosed (self): 
		return self.color == RED

	def isOpen (self): 
		return self.color == GREEN

	def isObstacle (self): 
		# is_barrier
		return self.color == BLACK

	def isStart (self): 
		return self.color == ORANGE

	def isEnd (self): 
		return self.color == TURQOISE

	def reset (self): 
		self.color = WHITE

	def makeClosed (self): 
		self.color = RED

	def makeOpen (self): 
		self.color = GREEN

	def makeObstacle (self): 
		self.color = BLACK

	def makeEnd (self): 
		self.color = TURQOISE

	def makePath (self): 
		self.color = PURPLE

	def makeStart (self): 
		self.color = ORANGE

	def draw (self, window): 
		pygame.draw.rect (window, self.color, (self.x, self.y, self.width, self.width))

	def updateNeighbors (self, grid): 
		self.neighbors = []
		# Down neighbor
		if self.row < self.total_rows - 1 and not grid[self.row+1][self.column].isObstacle():
			self.neighbors.append (grid[self.row+1][self.column])
		# Up neighbor
		if self.row > 0 and not grid[self.row-1][self.column].isObstacle():
			self.neighbors.append (grid[self.row-1][self.column])
		# Right neighbor
		if self.column < self.total_rows - 1 and not grid[self.row][self.column+1].isObstacle():
			self.neighbors.append (grid[self.row][self.column+1])
		# Left neighbor
		if self.column > 0 and not grid[self.row][self.column-1].isObstacle():
			self.neighbors.append (grid[self.row][self.column-1])

	def __lt__ (self, other): 
		"""
		Less than
		"""
		return False

# ----- Functions -----
def heuristic (pixel1, pixel2):
	"""
	Returns the Manhattan distance.
	""" 
	x1, y1 = pixel1
	x2, y2 = pixel2
	return abs (x1 - x2) + abs (y1 - y2)

def makeGrid (rows, width): 
	"""
	This function constructs and returns the matrix grid.
	"""
	grid = []
	size = width // rows

	for i in range (rows): 
		temp = []
		for j in range (rows): 
			pixel = Pixel (i, j, size, rows)
			temp.append (pixel)
		grid.append (temp)

	return grid

def drawLines (window, rows, width): 
	"""
	This function draws the grid lines in the window.
	"""
	size = width // rows

	for i in range (rows): 
		pygame.draw.line (window, GREY, (0, i * size), (width, i * size))

		for j in range (rows): 
			pygame.draw.line (window, GREY, (j * size, 0), (j * size, width))

def draw (window, grid, rows, width): 
	"""
	This functions draws on the grid. 
	First, it draws each pixel, 
	then, overdraws with the gridlines. 
	"""
	window.fill (WHITE)

	for line in grid: 
		
		for pixel in line: 
			pixel.draw (window)

	drawLines (window, rows, width)
	pygame.display.update()

def getClickedPosition (position, rows, width): 
	"""
	This function returns the grid position. 
	It translates the clicked coordenates to the grid matrix position.
	"""
	size = width // rows
	y, x = position
	row = y // size
	col = x // size
	return row, col

def main (window, width): 
	"""
	Main function
	"""
	ROWS = 50
	grid = makeGrid (ROWS, width)

	start = None	# Startpoint
	end = None		# Endpoint
	run = True 		# Run
	started = False	# Algorithm running

	while run: 
		draw (WIN, grid, ROWS, WIDTH)	# Refresh screen

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				run = False

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
					start.makeStart()
				elif not end and pixel != start: 
					# Secondly, place the end position
					end = pixel 
					end.makeEnd()
				elif pixel != end and pixel != start: 
					# At last, place obstacles
					pixel.makeObstacle() 

			elif pygame.mouse.get_pressed()[2]: 
				# Right mouse button
				# Remove obstacles
				position = pygame.mouse.get_pos()
				row, col = getClickedPosition (position, ROWS, width)
				pixel = grid[row][col]
				pixel.reset()
				if pixel == start: 
					start = None
				elif pixel == end: 
					end = None

			if event.type == pygame.KEYDOWN: 

				if event.key == pygame.K_SPACE and not started: 
					started = True
					
					for row in grid: 
						for pixel in row: 
							pixel.updateNeighbors(grid)

					# aStartAlgorithm (lambda: draw(WIN, grid, ROWS, WIDTH), grid, start, end)

	pygame.quit()

if __name__ == '__main__':
	main(WIN, WIDTH)