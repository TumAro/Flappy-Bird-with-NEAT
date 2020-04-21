import pygame
import neat
import time
import os
import random

#Assigning height and width of the window
screen_width = 600
screen_height = 800



#------------loading the images---------------
#the images for the flappy bird's flaps
bird_imgs = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))
]

pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))    #image of pipe
base_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))    #image of base
bg_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))        #image of background



#-----------defining the classes------------
class Bird:

    #things of birds that will be constant for every bird instances
    imgs = bird_imgs
    max_rotation = 25
    rot_vel = 20
    animation_time = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0           #Initial tilt angle of the bird
        self.tick_count = 0     #keeps track of when we last jumped
        self.vel = 0            #initial velocity of the bird
        self.height = y
        self.img_count = 0      #to keep track of which image is showing to animate
        self.img = self.imgs[0] #initial frame of the bird

    #the jump mechanism
    def jump(self):
        self.vel = -10.5        #the top left corner will be the origin (0,0) and the physics will be aplied as y coming down as +ve direction
        self.tick_count = 0
        self.height = self.y

    #the mechanism for moving
    def move(self):
        pass