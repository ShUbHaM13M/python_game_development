
from enum import Enum
import pygame

class State(Enum):
	DEAD = 0
	ALIVE = 1

class Cell(object):
	def __init__(self, x: int, y: int, cell_size=10, state=State.DEAD):
		self.x = x
		self.y = y
		self.cell_size = cell_size
		self.offset = 2
		self.state = state

	def __repr__(self):
		return(f'Cell at: ({self.x}, {self.y}), state: {self.state}')
	
	def __bool__(self):
		return True if self.state == 1 else False

	def draw(self, screen, color=(255, 255, 255)):
		is_dead = self.state
		pygame.draw.rect(
			screen,
			(0, 0, 0),
			(self.x * self.cell_size, self.y * self.cell_size, self.cell_size, self.cell_size),
			1
		)
		pygame.draw.rect(
			screen, 
			color,
			(self.x * self.cell_size + self.offset, self.y * self.cell_size + self.offset, self.cell_size - self.offset, self.cell_size - self.offset),
			is_dead
		)
