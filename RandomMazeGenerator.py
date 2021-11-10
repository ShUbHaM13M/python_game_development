
import pygame
import sys
import math
import random
import time
import os

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

screenWidth = 400
screenHeight = 400
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Maze Generator")
# pygame.display.set_icon(pygame.image.load('mazeIcon.png'))

clock = pygame.time.Clock()

cellSize = 28
cols = math.floor(screenWidth / cellSize)
rows = math.floor(screenHeight / cellSize)

grid = [0 for i in range(cols)]
for i in range(cols):
    grid[i] = [0 for x in range(rows)]

current = None
stack = []

def _get1D_Index(x, y):
    if x < 0 or y < 0 or x > cols - 1 or y > rows - 1: 
        return None
    else: return x + y * cols

class Cell(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.isVisited = False
        self.walls = [True, True, True, True] #[Top, Right, Bottom, Left]

    def addNeighbors(self):

        x, y = self.x, self.y
        neighbors = []

        #Top
        if y > 0 and grid[x][y - 1].isVisited == False:
            neighbors.append(grid[x][y - 1])
        #Right
        if x < cols - 1 and grid[x + 1][y].isVisited == False:
            neighbors.append(grid[x + 1][y])
        #Bottom
        if y < rows - 1 and grid[x][y + 1].isVisited == False:
            neighbors.append(grid[x][y + 1])
        #Left
        if x > 0 and grid[x - 1][y].isVisited == False:
            neighbors.append(grid[x - 1][y])

        if len(neighbors) > 0:
            randomCell = random.randint(0, len(neighbors) - 1)
            return grid[neighbors[randomCell].x][neighbors[randomCell].y]
        else: return None
    
    def highlight(self):
        pygame.draw.rect(screen, (0, 110, 250), (self.x * cellSize, self.y * cellSize, cellSize, cellSize))
    
    def render(self):

        x = self.x * cellSize
        y = self.y * cellSize

        if self.isVisited:
            pygame.draw.rect(screen, GREEN, (self.x * cellSize, self.y * cellSize, cellSize, cellSize))
        
        if self.walls[0] == True:
            pygame.draw.line(screen, WHITE, (x           , y)           , (x + cellSize, y), 2)
        if self.walls[1] == True:
            pygame.draw.line(screen, WHITE, (x + cellSize, y)           , (x + cellSize, y + cellSize), 2)
        if self.walls[2] == True:
            pygame.draw.line(screen, WHITE, (x + cellSize, y + cellSize), (x           , y + cellSize), 2)
        if self.walls[3] == True:
            pygame.draw.line(screen, WHITE, (x           , y + cellSize), (x           , y), 2)
            
        
for x in range(rows):
    for y in range(cols):
        grid[x][y] = Cell(x, y)

current = grid[0][0]


def removeWalls(a, b):

    x = a.x - b.x
    y = a.y - b.y
    #[0]Top [1]Right [2]Bottom [3]Left
    if x == 1:
        a.walls[3] = False
        b.walls[1] = False
    elif y == 1:
        a.walls[0] = False
        b.walls[2] = False
    elif x == -1:
        a.walls[1] = False
        b.walls[3] = False
    elif y == -1:
        a.walls[2] = False
        b.walls[0] = False


def draw():

    global current    

    for x in range(cols):
        for y in range(rows):
            grid[x][y].render()

    current.isVisited = True
    current.highlight()
    next = current.addNeighbors()

    if next:
        next.isVisited = True
        stack.append(current)

        removeWalls(current, next)

        current = next
    elif len(stack) > 0: 
        current = stack.pop()
    
    pygame.display.flip()
    pygame.display.update()


isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

    clock.tick(60)
    draw()
        

pygame.quit()
sys.exit()