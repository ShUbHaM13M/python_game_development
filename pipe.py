
import pygame

class Pipe():
	def __init__(self, length, pipe_image, x=0, y=0):
		self.img = pygame.transform.scale(
			pipe_image, 
			(pipe_image.get_width(), int(pipe_image.get_height() * length))
		)
		self.rect = self.img.get_rect()
	
	def render(self, screen, x, y):
		self.rect = pygame.Rect(x, y, self.img.get_width(), self.img.get_height())
		screen.blit(self.img, (x, y))
	
	