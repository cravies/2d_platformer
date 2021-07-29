import pygame
from pygame.locals import *
import numpy as np

#start pygame
pygame.init()

#set window size
screen_width = 1000
screen_height = 1000

#initialize window
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Platformer')

#load images
bg_img = pygame.image.load('background.jpg')

#tile size for grid
tile_size = 100

#draw game grid
def draw_grid():
    for line in range(0,10):
        pygame.draw.line(screen, (255,255,255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255,255,255), (line * tile_size, 0), (line * tile_size, screen_width))


#define the world, i.e where we have platorms
class World():
    
    def __init__(self, data):
        """passes an array of integers data, either 0 or 1.
        if it is a 0, there is just the background. Blocks are on 1."""

        self.tile_list = []

        #load images
        block_img = pygame.image.load('block.png')

        [grid_height, grid_width] = np.shape(data)

        #iterate over grid rows
        for i in range(grid_height):
            #iterate over grid cols
            for j in range(grid_width):
                if data[i][j] == True:
                    #draw a block to the screen
                    print("tile {},{} has a block".format(i,j))
                    img = pygame.transform.scale(block_img, (tile_size,tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = j * tile_size
                    img_rect.y = i * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)

    def draw(self):
        #draw the loaded blocks to the screen
        for tile in self.tile_list:
            print(tile)
            screen.blit(tile[0],tile[1])


#define grid
world_data = np.zeros([10,10])
world_data[5][0] = 1
world_data[5][1] = 1
world_data[5][2] = 1
world_data[5][5] = 1
world_data[5][6] = 1
world_data[5][7] = 1

#initialize world object
world = World(world_data)

#start game logic loop
run = True
while run == True:

    #draw screen
    screen.blit(bg_img, (0,0))

    #draw blocks
    world.draw()

    #draw grid
    draw_grid()

    #process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

#exit game
pygame.quit()
