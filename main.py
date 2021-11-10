from typing import List
import pygame
import os
import random
from pygame.locals import *
import sys

pygame.init()

from bird import Bird
from pipe import Pipe

SCREEN_WIDTH, SCREEN_HEIGHT = 400, 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
display = pygame.Surface((200, 250))
pygame.display.set_caption("Crappy bird")

background = pygame.image.load('assets\\sprites\\background\\Background1.png').convert()
tile1 = pygame.image.load('assets\\sprites\\tileset\\Tile-1.png').convert()
tile2 = pygame.image.load('assets\\sprites\\tileset\Tile-2.png').convert()

pipe_img = pygame.image.load('assets\\sprites\\tileset\\pipe-1.png').convert()
pipe_img.set_colorkey((255, 255, 255))

is_running = True
clock = pygame.time.Clock()
font = pygame.font.Font(None, 42)
current_score = 0

def load_animations(animation_dir: str):
	current_dir, _ = os.path.split(os.path.abspath(__file__))
	dir = current_dir + animation_dir
	animations = []
	for file in os.listdir(dir):
		if file.endswith(".png"):
			animations.append(pygame.image.load(f'{dir}\{file}').convert_alpha())

	return animations

bird = Bird(SCREEN_WIDTH * 0.25 - 16, SCREEN_HEIGHT * 0.25 - 16, 16, 16)
bird.set_animation('idle', load_animations('\\assets\\sprites\\player\\bird2'))

def check_inputs():
	global is_running
	global start_game
	for event in pygame.event.get():
		if event.type == QUIT:
			is_running = False
		
		key_pressed = pygame.key.get_pressed()
		mouse_pressed = pygame.mouse.get_pressed()

		if key_pressed[K_SPACE] or mouse_pressed[0]:
			if not start_game: 
				start_game = True
				return
			bird.vertical_momentum = bird.jump_height
			
		if key_pressed[K_ESCAPE]:
			start_game = not start_game


def generate_pipe(index=0):
	top_pipe_length = random.uniform(0.2, 1.5)
	bottom_pipe_length = 1.8 - top_pipe_length
	top_pipe = Pipe(top_pipe_length, pipe_img)
	bottom_pipe = Pipe(bottom_pipe_length, pipe_img)
	return [top_pipe, bottom_pipe, index]

def reset_game():
	bird.x = SCREEN_WIDTH * 0.25 - 16
	bird.y = SCREEN_HEIGHT * 0.25 - 16
	bird.angle = 0

def render(camera_pos):
	global bgX
	global pipe_lengths
	global pipeX
	global pipes
	global bird_rect
	global current_score
	global can_score_points

	display.fill((0, 0, 0))
	display.blit(background, (0, 0))

	score_text = font.render(str(current_score), False, (255, 255, 255))

	if start_game:
		bgX -= 4
		if bgX < tile1.get_width() * -1: bgX = 0
		pipes_to_remove = []
		generate_new_pipes = False

		for pipe in pipes:
			index = pipe[2]
			x = index * distance_between_pipes + SCREEN_WIDTH - camera_pos[0]

			pipe[0].render(display, x, 0)
			bottom_pipe_y = SCREEN_HEIGHT * 0.5 - pipe[1].img.get_height() - tile1.get_height()
			pipe[1].render(display, x, bottom_pipe_y)

			bird_rect = pygame.Rect(bird.x - camera_pos[0], bird.y - camera_pos[1], bird.width, bird.height)

			collider = pygame.Rect( 
				(x + pipe[0].img.get_width(), 0, distance_between_pipes - pipe[0].img.get_width(), 250)
			)

			if bird_rect.colliderect(collider):
				if can_score_points: current_score = index + 1

			if (index + 1) % 9 == 0 and x + pipe[0].img.get_width() < 0:
				generate_new_pipes = True
		
		if generate_new_pipes:
			generate_new_pipes = False
			prev_index = pipes[len(pipes) - 1][2]
			pipes[:] = [generate_pipe(new_pipe_index) for new_pipe_index in range(prev_index, prev_index + 10)]

	else:
		bgX -= 2
		if bgX < tile1.get_width() * -1: bgX = 0

	for i in range(5):
		display.blit(tile2, (i * tile1.get_width() + bgX, SCREEN_HEIGHT * 0.5 - tile2.get_height()))

	bird.render(display, scroll=camera_pos, debug=False)

	score_text_x = display.get_width() * 0.5 - score_text.get_width() * 0.35
	score_text_y = display.get_height() * 0.20 - score_text.get_height() * 0.5
	display.blit(score_text, (score_text_x, score_text_y))

	screen.blit(pygame.transform.scale(display, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))


def main():
	global start_game
	global bird_rect
	true_scroll = [0, 0]
	while is_running:

		true_scroll[0] += (bird.x - true_scroll[0] - 50) / 5
		scroll = true_scroll.copy()
		scroll[0] = int(scroll[0])

		if start_game:
			for pipe in pipes:
				bird_rect = pygame.Rect(bird.x - scroll[0], bird.y - scroll[1], bird.width, bird.height)
				if bird_rect.colliderect(pipe[0].rect) or bird_rect.colliderect(pipe[1].rect):
					start_game = False
					reset_game()
					
			bird.move()
		else:
			bird.bird_pause_anim(step=6, amplitude=14, screen_width=250 * 0.5)

		check_inputs()
		render(scroll)
		pygame.display.update()
		clock.tick(24)

if __name__ == '__main__':
	bgX = 0
	distance_between_pipes = 150
	pipes = [generate_pipe(index) for index in range(10)]
	bird_rect = None
	can_score_points = True

	start_game = False
	is_running = True
	main()
	pygame.quit()
	sys.exit()