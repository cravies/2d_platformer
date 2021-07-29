import pygame
from pygame.locals import *

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

#start game logic loop
run = True
while run == True:

    screen.blit(bg_img, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

#exit game
pygame.quit()
