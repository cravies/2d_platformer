import time
import pygame
from pygame.locals import *
import numpy as np
from matplotlib import pyplot as plt
from numpy import genfromtxt
import random
from PIL import Image
import copy


"""File table of contents:
- Window and system initialization
- Load graphics
- Utility functions (draw game grid, parse gifs)
- Player, world, and enemy classes
- Create game objects (enemies and player, world)
- Game loop 
"""


#########-WINDOW AND SYSTEM STUFF-###################################################################

#start pygame
pygame.init()

#set window size
screen_width = 1400
screen_height = 800

#tile size for grid
tile_size = 50

#scaling from number of tiles to number of pixels
#assume we have square screen
scaling = screen_height / tile_size

#initialize window
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Platformer')

#set clock for fps
clock = pygame.time.Clock()
fps = 60

##############-UTILITY FUNCTIONS-###################################################################

#draw game grid
def draw_grid():
    for line in range(0,int(screen_width/tile_size)):
        pygame.draw.line(screen, (255,255,255), (0, line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen, (255,255,255), (line * tile_size, 0), (line * tile_size, screen_width))

#import player walking gif
def split_animated_gif(gif_file_path):
    ret = []
    gif = Image.open(gif_file_path)
    for frame_index in range(gif.n_frames):
        gif.seek(frame_index)
        frame_rgba = gif.convert("RGBA")
        pygame_image = pygame.image.fromstring(
            frame_rgba.tobytes(), frame_rgba.size, frame_rgba.mode
        )
        ret.append(pygame_image)
    return ret

########-LOAD GRAPHICS-###############

#initialize font for score
myfont = pygame.font.SysFont('monospace', 60)

#load images
bg_img = pygame.image.load('./images/background_pixel.png')
heart_img = pygame.image.load('./images/heart.png')
heart_img = pygame.transform.scale(heart_img,(tile_size,tile_size))

#player sprite dimensions
player_height = 2*tile_size - 1
player_width = int(1*tile_size)

#enemy sprite dimensions
enemy_height = 1*tile_size - 1
enemy_width = 1*tile_size

#movement gifs for player and enemies
walking_right_gif = split_animated_gif('./images/walking.gif')
walking_left_gif = split_animated_gif('./images/walking_left.gif')
walking_right_mining_gif = split_animated_gif('./images/mining.gif')
enemy_gif = split_animated_gif('./images/enemy.gif')

################-PLAYER, WORLD, AND ENEMY CLASSES-###################################################

#define the player class
class Player():
    def __init__(self, x, y):
        #initialize player sprite and coordinates
        img_right = pygame.image.load('./images/walking.gif')
        img_mining_right = pygame.image.load('./images/mining.gif')
        img_left = pygame.image.load('./images/walking_left.gif')
        self.index_right = 0
        self.index_mining_right = 0
        self.index_left = 0
        self.counter_right = 0
        self.counter_mining_right = 0
        self.counter_left = 0
        self.anim_right = []
        self.anim_mining_right = []
        self.anim_left = []
        self.is_anim_right = False
        self.is_anim_left = False
        self.hurt_cooldown = 0
        self.jump_cooldown = 0
        self.hearts=3
        #load walking animation for walking right
        for img in walking_right_gif:
            img = pygame.transform.scale(img,(player_width,player_height))
            #append image 3 times to slow down animation
            self.anim_right += [img] * 3
        #load walking animation for walking left
        for img in walking_left_gif:
            img = pygame.transform.scale(img,(player_width,player_height))
            #append image 3 times to slow down animation
            self.anim_left += [img] * 3
        #load walking animation for walking right while mining
        for img in walking_right_mining_gif:
            img = pygame.transform.scale(img,(player_width,player_height))
            #append image 3 times to slow down animation
            self.anim_mining_right += [img] * 3
        self.image = self.anim_right[self.index_right]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jump_acceleration = int(0.8*tile_size)
        self.is_jump = False
        self.is_mining = False
        self.walk_speed = int(tile_size/(fps/10))
        self.level_count = 0
    
    def update(self):     
    
        #get keypress
        key = pygame.key.get_pressed()
        self.dx = 0
        self.dy = 0

        #check for horizontal movement. If so, animate.
        #default is NO animation
        self.is_anim_right = False        
        self.is_anim_left = False
        if key[pygame.K_LEFT]:
            self.dx-=self.walk_speed
            self.is_anim_left = True
        elif key[pygame.K_RIGHT]:
            self.is_anim_right = True
            self.dx+=self.walk_speed

        #dig mechanic (remove a block the player is facing)
        #default is NO digging
        self.is_mining = False
        if key[pygame.K_UP]:
            self.is_mining = True
        
        #special event handling so that player does not hold down jump 
        if key[pygame.K_SPACE]:
            #no double jumping
            if self.is_jump == False and self.jump_cooldown == 0:
                #jump cooldown (stops player holding down space)
                self.jump_cooldown = int(fps/3)
                self.vel_y -= self.jump_acceleration
                self.is_jump = True
    
        #set terminal velocity equal to initial jump acceleration * 1.5 (we can fall a bit faster than we jump) 
        if self.vel_y < (self.jump_acceleration):
            self.vel_y += int(self.jump_acceleration/10)
        else:
        #can't get too fast
            self.vel_y = self.jump_acceleration 
        #set downwards displacement from velocity
        self.dy = self.vel_y        

        #collision checking
        for index, tile in enumerate(world.tile_list):
            #check for y-dir collision
            #tile has format tile(picture,rectangle object)
            #pass a rectangle object representing where the character wants to 
            #go to implement pre-emptive collision checking
            if tile[1].colliderect(self.rect.x, self.rect.y + self.dy, self.width, self.height):
                #check if jumping, i.e below block and hitting roof
                if self.vel_y < 0:
                    #touch top of sprite to roof
                    self.dy = tile[1].bottom - self.rect.top
                #else we are landing on a block
                elif self.vel_y >= 0:
                    self.dy = tile[1].top - self.rect.bottom
                    #we have landed back on a block, set is_jump to be false.
                    self.is_jump = False
                self.vel_y = 0
            elif tile[1].colliderect(self.rect.x + self.dx, self.rect.y, self.width, self.height):
                if self.is_mining:
                    #dig through the block
                    #make sure world tile list is still an array
                    print(type(world.tile_list))
                    if isinstance(world.tile_list,np.ndarray):
                        world.tile_list = world.tile_list.tolist()
                    world.tile_list.pop(index)
                    self.digging = False
                else: #otherwise bump into block
                    self.dx = 0


    def draw(self):
        #update co-ordinates
        self.rect.x += self.dx
        self.rect.y += self.dy

        #update cooldown for taking damage and jumping
        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1
        if self.hurt_cooldown > 0:
            self.hurt_cooldown -= 1
 
        #update animation if we are walking right
        if self.is_anim_right:
            self.index_right += 1
            self.image = self.anim_right[self.index_right % len(self.anim_right)]

        #update animation if we are walking left
        if self.is_anim_left:
            self.index_left += 1
            self.image = self.anim_left[self.index_left % len(self.anim_left)]

        #update image if we are walking and mining right
        if self.is_mining:
            self.index_mining_right += 1
            self.image = self.anim_mining_right[self.index_mining_right % len(self.anim_mining_right)]

        #check we are not leaving the map
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            self.dy=0
            self.is_jump = False
        elif self.rect.top < 0: 
            self.rect.top = 0
            self.dy=0
        if (self.rect.x + self.rect.width) > screen_width:
            #generate fresh world. Respawn enemies
            global enemy_list
            for i in range(0,3-len(enemy_list)):
                new_enemy = Enemy(random.uniform(0,screen_height),random.uniform(0,screen_width))
                enemy_list.add(new_enemy)
            self.rect.x = 0
            self.level_count += 1
            world.scroll()
            self.dx = 0
        if (self.rect.x < 0):
            self.rect.x = 0
            self.dx = 0
           
        #draw sprite
        screen.blit(self.image,self.rect)
        #draw our level count (how many rooms we have cleared in this level) this should be next to our hearts 
        level_label = myfont.render("Level: {}".format(self.level_count), 1, (255,255,255))
        screen.blit(level_label, ((self.hearts+3) * tile_size,0))
        #scale heart image and draw 
        for i in range(0,self.hearts):
            screen.blit(heart_img, (i * tile_size, 0))


#define the world, i.e where we have platorms
class World():
    
    def __init__(self,level):
        #initialize our world
        self.iteration = 0
        #load from file
        self.level = level
        self.data = np.genfromtxt("./levels/level_{}.txt".format(self.level), delimiter=',')
        
        self.tile_list_base = []
        self.tile_list_random = []
        self.tile_list = []

        #load images

        [self.grid_height, self.grid_width] = np.shape(self.data)
        #load level
        self.load_level()

    def load_level(self):
        #load block images
        gravel_block = pygame.image.load('./images/gravel.jpg')
        dirt_block = pygame.image.load('./images/dirt.jpg')
        grass_block = pygame.image.load('./images/grass.jpg')
        #iterate over grid rows
        for i in range(self.grid_height):
            #iterate over grid cols
            for j in range(self.grid_width):
                if self.data[i][j] == 1:
                    #draw a gravel block to the screen
                    img = pygame.transform.scale(gravel_block, (tile_size,tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = j * tile_size
                    img_rect.y = i * tile_size
                    tile = (img, img_rect)
                    self.tile_list_base.append(tile)
                elif self.data[i][j] == 2:
                    #draw a dirt block to the screen
                    img = pygame.transform.scale(dirt_block, (tile_size,tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = j * tile_size
                    img_rect.y = i * tile_size
                    tile = (img, img_rect)
                    self.tile_list_base.append(tile)
                elif self.data[i][j] == 3:
                    #draw a grass block to the screen
                    img = pygame.transform.scale(grass_block, (tile_size,tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = j * tile_size
                    img_rect.y = i * tile_size
                    tile = (img, img_rect)
                    self.tile_list_base.append(tile)
                elif self.data[i][j] == 4:
                    #spawn an enemy
                    enemy1 = Enemy(j * tile_size, i * tile_size)
                    enemy_list.add(enemy1)
                    
        #generate blocks randomly
        #self.generate_random_blocks()
        #self.tile_list = np.concatenate([self.tile_list_base,self.tile_list_random])
        self.tile_list = self.tile_list_base

    def draw(self):
        #draw the loaded blocks to the screen
        for tile in self.tile_list:
            #format of tile is:
            #tile = [image, coordinates]
            screen.blit(tile[0],tile[1])

    def generate_random_blocks(self):
        #procedurally generate solo dirt blocks
        print("generate_random_blocks")
        block_img = pygame.image.load('./images/gravel.jpg')
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                if random.uniform(0,1) > 0.95:
                    #draw a gravel block to the screen
                    img = pygame.transform.scale(block_img, (tile_size,tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = ( j * tile_size ) % (screen_width - 100) 
                    img_rect.y = ( i * tile_size )
                    tile = (img, img_rect)
                    self.tile_list_random.append(tile)

    def scroll(self):
        #refresh random blocks
        if self.iteration < 10:
            #we are on the next sublevel
            self.tile_list_random = []
            self.generate_random_blocks()
            print("tile list is {}".format(self.tile_list))
            print("tile list shape is {}".format(np.shape(self.tile_list)))
            print("random blocks are {}".format(self.tile_list_random))
            print("random block shape is {}".format(np.shape(self.tile_list_random)))
            self.tile_list = np.concatenate([self.tile_list,self.tile_list_random]) 
            self.iteration += 1
            global enemy_list
            for enemy in enemy_list:
                enemy.scroll()
        else:
            #load new level
            self.__init__(self.level+1)

#enemy class, moves around and jumps randomly
class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        #initialize pygame sprite class to inherit
        pygame.sprite.Sprite.__init__(self)
        #initialize enemy sprite and coordinates
        img_ = pygame.image.load('./images/enemy.gif')
        self.index = 0
        self.counter = 0
        self.anim = []
        self.is_anim = False
        #load walking animation for walking right
        for img in enemy_gif:
            img = pygame.transform.scale(img,(player_width,player_height))
            #append image 3 times to slow down animation
            self.anim += [img] * 3
        self.image = self.anim[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jump_acceleration = int(0.5*tile_size)
        self.is_jump = False
        self.walk_speed = int(tile_size/(fps/4))
        self.is_moving_left = False
        self.is_moving_right = False
        self.dx = 0
        self.dy = 0

    def scroll(self):
        #we are going to the next level, appear in a random place again
        self.rect.x = random.uniform(10,screen_width-10)
        self.rect.y = random.uniform(10,screen_height-10)
   
    def update(self):     
    
        #we don't need to get keypress, instead we are moving randomly
        self.dx = 0
        self.dy = 0

        #check for horizontal movement. If so, animate.
        #default is NO animation
        self.is_anim = False        
        
        #check if we are moving, with probability p
        p = 0.5
        #if we are moving left, probably keep moving left
        p_left = False
        #if we are moving right, probably keep moving right

        #equal probability left and right UNLESS we are alreaself.dy moving
        #then we keep moving that direction (probably...)
        if self.is_moving_left:
            if random.uniform(0,1) < 0.90:
                #keep moving left
                self.is_anim = True
                self.dx -= self.walk_speed
            else:
                #stop moving
                self.is_moving_left = False
        elif self.is_moving_right:
            if random.uniform(0,1) < 0.90:
                #keep moving right
                self.is_anim = True
                self.dx += self.walk_speed
            else:
                #stop moving
                self.is_moving_right = False
        else:
            if random.uniform(0,1) > 0.5:
                #we are moving left 
                self.is_moving_left = True
                self.dx -= self.walk_speed
                self.is_anim = True
            else:
                #we are moving right
                self.is_moving_right = True
                self.dx += self.walk_speed
                self.is_anim = True
        
        #random jumping with probability p_j
        p_j = 0.01
        if random.uniform(0,1) < p_j:
            #no double jumping
            if self.is_jump == False:
                self.vel_y -= self.jump_acceleration
                self.is_jump = True
    
        #set terminal velocity equal to initial jump acceleration 
        if self.vel_y < (self.jump_acceleration):
            self.vel_y += int(self.jump_acceleration/10)
 
        #set downwards displacement from velocity
        self.dy = self.vel_y        

        #collision checking
        for tile in world.tile_list:
            #check for y-dir collision
            #tile has format tile(picture,rectangle object)
            #pass a rectangle object representing where the character wants to 
            #go to implement pre-emptive collision checking
            if tile[1].colliderect(self.rect.x, self.rect.y + self.dy, self.width, self.height):
                #check if jumping, i.e below block and hitting roof
                if self.vel_y < 0:
                    #touch top of sprite to roof
                    self.dy = tile[1].bottom - self.rect.top
                #else we are landing on a block
                elif self.vel_y >= 0:
                    self.dy = tile[1].top - self.rect.bottom
                    #we have landed back on a block, set is_jump to be false.
                    self.is_jump = False
                self.vel_y = 0
            elif tile[1].colliderect(self.rect.x + self.dx, self.rect.y, self.width, self.height):
                self.dx = 0


    def draw(self):
        #update co-ordinates
        self.rect.x += self.dx
        self.rect.y += self.dy
 
        #update animation if we are walking left
        if self.is_anim:
            self.index += 1
            self.image = self.anim[self.index % len(self.anim)]

        #check we are not leaving the map
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            self.dy=0
            self.is_jump = False
        elif self.rect.top < 0: 
            self.rect.top = 0
            self.dy=0
        if (self.rect.x + self.rect.width) > screen_width:
            self.rect.x = screen_width - self.rect.width
            self.dx = 0
        if (self.rect.x < 0):
            self.rect.x = 0
            self.dx = 0
           
        #draw sprite
        screen.blit(self.image,self.rect)

##############-CREATE GAME OBJECTS-##################################################################

#initialize enemies
enemy_list = pygame.sprite.Group()
#initialize world object
world = World(0)
#initialize player object
player = Player(100,5*tile_size-player_height)

################-COLLISION DETECTION-################################################################

def collision_detection(player,enemy_list):
    #see if player will collide with enemy after movement is applied
    proposed_player_x = pygame.Rect(player.rect.x + player.dx, player.rect.y, player.width, player.height)
    proposed_player_y = pygame.Rect(player.rect.x, player.rect.y + player.dy, player.width, player.height)
    for enemy in enemy_list:
        proposed_enemy_x = pygame.Rect(enemy.rect.x + enemy.dx, enemy.rect.y, enemy.rect.width, enemy.rect.height)
        proposed_enemy_y = pygame.Rect(enemy.rect.x, enemy.rect.y + enemy.dy, enemy.rect.width, enemy.rect.height)
        if proposed_player_x.colliderect(proposed_enemy_x):
            player.dx = 0
            enemy.dx = 0
            if player.hurt_cooldown <= 0:
                player.hearts -= 1
                player.hurt_cooldown = 120
        if proposed_player_y.colliderect(proposed_enemy_y):
            #check if we are jumping/falling onto enemy
            if player.dy > 0:
                #kill the enemy if we are
                enemy.kill()
                #make the player jump. This effect should not stack.
                if player.vel_y > 0:
                    player.vel_y -= player.jump_acceleration
                    player.is_jump = True
            else:
                player.dy = 0
                enemy.dy = 0
                if player.hurt_cooldown <= 0:
                    player.hearts -= 1    
                    player.hurt_cooldown = 320
  

#################-GAME LOGIC LOOP-###################################################################

#start game logic loop
run = True
while run == True:
    #set fps
    clock.tick(fps)

    #draw screen
    screen.blit(bg_img, (0,0))

    #draw blocks
    world.draw()

    #update player position
    player.update()

    #update enemy position
    for enemy in enemy_list:
        #update enemy movement
        enemy.update()

    #check if player is colliding with enemy
    collision_detection(player,enemy_list) 

    #draw grid
    #draw_grid()

    #draw player and enemies to screen
    player.draw()

    #draw enemies
    for enemy in enemy_list:
        enemy.draw()

    #process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

#exit game
pygame.quit()
