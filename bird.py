
import pygame
import math

class Bird():
	def __init__(self, x, y, width, height, speed = 5):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.animations = {}
		self.movement = [0, 0]
		self.speed = speed
		self.frame = 0
		self.is_jumping = False
		self.jump_height = -8
		self.vertical_momentum = 0
		self.angle = 0
		self.step = 0
		
	def set_animation(self, key: int, animations):
		self.animations[key] = {} 
		self.animations[key]['frames'] = animations
		self.animations[key]['len'] = len(animations)
	
	def move(self):
		self.x += self.speed
		if self.is_jumping:
			self.vertical_momentum = 0
			self.is_jumping = False
			return
		self.y += self.vertical_momentum
		self.vertical_momentum += 1
		if self.vertical_momentum > 4:
			self.vertical_momentum = 4

		if self.angle > 45:
			self.angle = 45
		if self.angle < -45:
			self.angle = -45

		if self.vertical_momentum <= 0:
			self.angle += 15
		else:
			self.angle -= 10

	def jump(self, amount=10):
		self.y -= amount
	
	def bird_pause_anim(self, step, amplitude, screen_width):
		self.y = (-1 * math.sin(self.step * step) * amplitude) + screen_width
		self.step += 0.02

	def render(self, screen, scroll = 0, debug=False):

		if debug:
			pygame.draw.rect(screen, (0, 255, 255), (self.x - scroll[0], self.y - scroll[1], self.width, self.height))
			pygame.draw.rect(screen, (255, 0, 0), ((self.x-2) - scroll[0], (self.y-2) - scroll[1], self.width+4, self.height+4), 1)
			return

		if self.frame + 1 > self.animations['idle']['len']:
			self.frame = 0

		current_frame = self.animations['idle']['frames'][self.frame]
		surface = pygame.Surface((int(current_frame.get_width() + 10), int(current_frame.get_height() + 10)))
		surface = surface.convert()
		surface.set_colorkey((0, 0, 0))

		surface.blit( 
			pygame.transform.rotate(current_frame, self.angle), 
			( int(surface.get_width() * 0.5 - current_frame.get_width() * 0.5), 
			int(surface.get_height() * 0.5) - current_frame.get_height() * 0.5 )
		)

		self.width = int(surface.get_width() * 1.1)
		self.height = int(surface.get_height() * 1.1)

		screen.blit(
			pygame.transform.scale(surface, (self.width, self.height)), 
			(self.x - scroll[0], self.y - scroll[1])
		)


		self.frame += 1