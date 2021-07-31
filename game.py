import time
import pygame
from pygame.locals import *
import numpy as np
from matplotlib import pyplot as plt
import random

#start pygame
pygame.init()

#set window size
screen_width = 1400
screen_height = 800

#set clock for fps
clock = pygame.time.Clock()
fps = 60

#initialize window
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Platformer')

#load images
bg_img = pygame.image.load('background_pixel.png')

#tile size for grid
tile_size = 50

#scaling from number of tiles to number of pixels
#assume we have square screen
scaling = screen_height / tile_size

#player sprite dimensions
player_height = 2*tile_size
player_width = 1*tile_size

#draw game grid
def draw_grid():
    for line in range(0,int(screen_width/tile_size)):
        pygame.draw.line(screen, (255,255,255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255,255,255), (line * tile_size, 0), (line * tile_size, screen_width))


#define the player class
class Player():
    def __init__(self, x, y, data):
        #initialize player sprite and coordinates
        img = pygame.image.load('conor.png')
        self.image = pygame.transform.scale(img, (player_width,player_height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jump_acceleration = int(0.9*tile_size)
        self.is_jump = False
        self.walk_speed = int(tile_size/5)

    def update(self):     
    
        #get keypress
        key = pygame.key.get_pressed()
        dx = 0
        dy = 0
        
        if key[pygame.K_LEFT]:
            dx-=self.walk_speed
        elif key[pygame.K_RIGHT]:
            dx+=self.walk_speed
        
        if key[pygame.K_SPACE]:
            #no double jumping
            if self.is_jump == False:
                self.vel_y -= self.jump_acceleration
                self.is_jump = True
        
        #set terminal velocity equal to initial jump acceleration 
        if self.vel_y < (self.jump_acceleration):
            self.vel_y += int(self.jump_acceleration/10)
 
        #set downwards displacement from velocity
        dy = self.vel_y        

        #collision checking
        for tile in world.tile_list:
            #check for y-dir collision
            #tile has format tile(picture,rectangle object)
            #pass a rectangle object representing where the character wants to 
            #go to implement pre-emptive collision checking
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if jumping, i.e below block and hitting roof
                if self.vel_y < 0:
                    #touch top of sprite to roof
                    dy = tile[1].bottom - self.rect.top
                #else we are landing on a block
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                self.vel_y = 0
                self.is_jump = False
            elif tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0

        #update co-ordinates
        self.rect.x += dx
        self.rect.y += dy
 

        #check we are not leaving the map
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy=0
            self.is_jump = False
        elif self.rect.top < 0: 
            self.rect.top = 0
            dy=0
        if (self.rect.x + self.rect.width) > screen_width:
            self.rect.x = screen_width - self.rect.width
            dx = 0
        if (self.rect.x < 0):
            self.rect.x = 0
            dx = 0
           
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
"""world_data = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                       [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
"""
#procedurally generate level
[height,width] = [int(screen_height/tile_size),int(screen_width/tile_size)]
world_data = np.zeros([height,width])

def likelihood(i,j,height,width):
    return np.sqrt(i**2 + j**2)/ np.sqrt(height**2 + width**2)

for i in range(height):
    for j in range(width):
        p = likelihood(i,j,height,width)/3.5
        if random.uniform(0,1) < p:
            world_data[i,j] = 1

#initialize world object
world = World(world_data)
#initialize player object
player = Player(100,5*tile_size-player_height,world_data)

#start game logic loop
run = True
while run == True:
    #set fps
    clock.tick(fps)

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
