import pygame
from pygame.locals import *
import numpy as np
from matplotlib import pyplot as plt
import random

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

#scaling from number of tiles to number of pixels
#assume we have square screen
scaling = screen_height / tile_size

#player sprite dimensions
player_height = 200
player_width = 100

#draw game grid
def draw_grid():
    for line in range(0,10):
        pygame.draw.line(screen, (255,255,255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255,255,255), (line * tile_size, 0), (line * tile_size, screen_width))


#define the player class
class Player():
    def __init__(self, x, y, data):
        #initialize player sprite and coordinates
        img = pygame.image.load('sprite.jpg')
        self.image = pygame.transform.scale(img, (player_width,player_height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.data = data
        #initialize world grid with pixels that represent tiles
        self.world_grid = np.zeros([screen_height, screen_width])
        self.player_grid = np.zeros([screen_height, screen_width])
        #generate this from tile grid
        for i in range(screen_width):
            for j in range(screen_height):
                self.world_grid[i,j] = world_data[int(i/screen_height * scaling),int(j/screen_width * scaling)]
        #(self.rect.y, self.rect.y + player_height)
        #(self.rect.x, self.rect.x + player_width)
        #orientation is swapped for numpy indexing
        for i in range(self.rect.y, self.rect.y+player_height):
            for j in range(self.rect.x, self.rect.x+player_width):
                self.player_grid[i,j] = 1

    def update(self):

        #update coordinates and draw player

        #get keypress
        key = pygame.key.get_pressed()
        dx = 0
        dy = 0

        if key[pygame.K_LEFT]:
            dx-=4
        elif key[pygame.K_RIGHT]:
            dx+=4
        
        if key[pygame.K_UP]:
            dy-=4
        elif key[pygame.K_DOWN]:
            dy+=4
        
        #check for collisions with updated player grid
        test_grid = np.zeros([screen_height,screen_width])
        """we want a small margin so that it doesn't detect a collision when 
        we are just standing on a platform"""
        margin = 3
        for i in range(self.rect.y+dy+margin,self.rect.y+player_height+dy-margin):
            for j in range(self.rect.x+dx+margin, self.rect.x+player_width+dx-margin):
                test_grid[i,j] = 1
        
        if np.any(np.logical_and(test_grid,self.world_grid)):
            dx = 0
            dy = 0
        else:
            self.player_grid = test_grid

        #occasionally plot what is happening
        #if random.randrange(0,10):
        #    plt.imshow(self.player_grid+self.world_grid)
        #    plt.show()

        #update co-ordinates
        self.rect.x += dx
        self.rect.y += dy

        #draw sprite
        screen.blit(self.image,self.rect)

        print("updating, x={}, y={}".format(self.rect.x,self.rect.y))

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
            #format of tile is:
            #tile = [image, coordinates]
            screen.blit(tile[0],tile[1])


#define grid
world_data = np.zeros([10,10])
world_data[4][3] = 1
world_data[4][4] = 1
world_data[5][0] = 1
world_data[5][1] = 1
world_data[5][2] = 1
world_data[5][5] = 1
world_data[5][6] = 1
world_data[5][7] = 1

#initialize world object
world = World(world_data)
#initialize player object
player = Player(100,5*tile_size-player_height,world_data)

#start game logic loop
run = True
while run == True:

    #draw screen
    screen.blit(bg_img, (0,0))

    #draw blocks
    world.draw()

    #draw grid
    draw_grid()

    #draw player to screen
    player.update()
    

    #process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

#exit game
pygame.quit()
