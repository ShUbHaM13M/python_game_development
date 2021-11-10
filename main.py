
from cell import Cell, State
import pygame
import sys
import random
pygame.init()
from pygame.locals import *
import copy

SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Game of life')
clock = pygame.time.Clock()
FPS = 10

grid = []
grid_size = 15
cols = SCREEN_WIDTH // grid_size
rows = SCREEN_HEIGHT // grid_size

for x in range(cols):
	grid.append([])
	for y in range(rows):
		state = random.randint(0, 1)
		grid[x].append(Cell(x, y, cell_size=grid_size, state=state))

is_running = True
offset = 2
start_simulation = False

def generate_random():
	for x in range(cols):
		for y in range(rows):
			grid[x][y].state = random.randint(0, 1)

def clear_grid(_grid) -> None:
	for x in range(cols):
		for y in range(rows):
			_grid[x][y].state = 0

def count_neighbours(_grid, x, y):
	cell = _grid[x][y]
	alive_neighbours = 0
	for i in range(-1, 2):
		for j in range(-1, 2):
			_x = (cell.x + i + cols) % cols
			_y = (cell.y + j + rows) % rows
			neighbour = _grid[_x][_y]
			if neighbour.x == cell.x and neighbour.y == cell.y:
				continue
			if neighbour.state == 1: alive_neighbours += 1
	return alive_neighbours

def next_generation():
	next = copy.deepcopy(grid)
	clear_grid(next)
	for x in range(cols):
		for y in range(rows):
			cell = grid[x][y]
			alive_neighbours = count_neighbours(grid, x, y)
			
			if cell.state == 0 and alive_neighbours == 3:
				next[x][y].state = 1
			elif cell.state == 1 and (alive_neighbours < 2 or alive_neighbours > 3):
				next[x][y].state = 0
			else: 
				next[x][y].state = grid[x][y].state
	
	return next

def draw():
	screen.fill((0, 0, 0))

	for x in range(cols):
		for y in range(rows):
			grid[x][y].draw(screen)

while is_running:
	for event in pygame.event.get():
		if event.type == QUIT:
			is_running = False

		if not start_simulation and pygame.mouse.get_pressed()[0]:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			x = mouse_x // (SCREEN_WIDTH // cols)
			y = mouse_y // (SCREEN_HEIGHT // rows)
			cell = grid[x][y]
			if cell.state:
				grid[x][y].state = 0
			else: grid[x][y].state = 1
		
		if event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				is_running = False
			if event.key == K_SPACE:
				start_simulation = not start_simulation
			if not start_simulation and event.key == K_c:
				clear_grid(grid)
			if event.key == K_RIGHT:
				grid = next_generation()
			if event.key == K_r:
				generate_random()


	draw()
	if start_simulation:
		grid = next_generation()
	pygame.display.update()
	clock.tick(FPS)

pygame.quit()
sys.exit()
