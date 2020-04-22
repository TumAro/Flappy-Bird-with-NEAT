import pygame
import neat
import time
import os
import random
pygame.font.init()

#----------ubuntu thing to run pygame------
# os.environ["SDL_VIDEODRIVER"] = "dummy"
#------------------------------------------

#-----------some variables--------------------

stat_font = pygame.font.SysFont("comicsans", 40)

#Assigning height and width of the window
screen_width = 500
screen_height = 700



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
        self.tick_count += 1

        displacement = self.vel*self.tick_count + 1.5*self.tick_count**2

        #so the bird cant go anywhere more than 16
        if displacement >= 16:
            displacement = 16

        #for the movement of jump, tweak for a better jump
        if displacement < 0:
            displacement -= 2

        self.y = self.y + displacement

        #for tiliting the bird
        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.max_rotation:
                self.tilt = self.max_rotation

            else:
                if self.tilt > -90:
                    self.tilt -= self.rot_vel

    def draw(self, win):

        #flapping the bird's wings animation
        self.img_count += 1

        if self.img_count < self.animation_time:
            self.img = self.imgs[0]
        elif self.img_count < self.animation_time*2:
            self.img = self.imgs[1]
        elif self.img_count < self.animation_time*3:
            self.img = self.imgs[2]
        elif self.img_count < self.animation_time*4:
            self.img = self.imgs[1]
        elif self.img_count == self.animation_time*4 + 1:
            self.img = self.imgs[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.imgs[1]
            self.img_count = self.animation_time*2      #to make sure the animation doesnt skip a frame

        #to make sure the bird rotates with a fixed axis in the center
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)

        win.blit(rotated_image, new_rect.topleft)

    #for getting the collisions
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    
    #setting up the class variables
    gap = 200
    vel = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        #initializing the pipes
        self.top = 0
        self.bottom = 0
        self.pipe_top = pygame.transform.flip(pipe_img, False, True)
        self.pipe_bottom  = pipe_img

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.pipe_top.get_height()
        self.bottom = self.height + self.gap

    def move(self):
        self.x -= self.vel

    def draw(self, win):
        win.blit(self.pipe_top, (self.x, self.top))
        win.blit(self.pipe_bottom, (self.x, self.bottom))

    #mechanism for pixel perfect collision
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.pipe_top)
        bottom_mask = pygame.mask.from_surface(self.pipe_bottom)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        t_point = bird_mask.overlap(top_mask,top_offset)
        b_point = bird_mask.overlap(bottom_mask,bottom_offset)

        if t_point or b_point:
            return True
        else:
            return False

class Base:
    vel = 5
    width = base_img.get_width()
    img = base_img

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.width

    def move(self):
        self.x1 -= self.vel
        self.x2 -= self.vel

        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width
        
        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def draw(self, win):
        win.blit(self.img, (self.x1,self.y))
        win.blit(self.img, (self.x2,self.y))



#------------functions for the game-----------

#drawing the game elements
def draw_window(win, bird, pipes, base, score):
    win.blit(bg_img, (0,-150))
    for pipe in pipes:
        pipe.draw(win)

    text = stat_font.render(f"Score: {score}", 1, (255,255,255))
    win.blit(text, (screen_width - 10 - text.get_width(), 10))

    base.draw(win)
    bird.draw(win)
    pygame.display.update()

#function for main loop
def main():
    bird = Bird(230,350)                                                #creating a bird object
    base = Base(620)
    pipes = [Pipe(700)]
    screen = pygame.display.set_mode((screen_width,screen_height))      #setting up the window
    clock = pygame.time.Clock()                                         #initializes the framerate control of the game
    run = True
    score = 0


    while run:
        clock.tick(30)                          #sets the framerate of the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        #bird.move()                             #move the bird
        add_pipe = False
        remove = []

        #for looping new pipes and pipe movement and collision and everything
        for pipe in pipes:
            if pipe.collide(bird):
                pass

            if pipe.x + pipe.pipe_top.get_width() < 0:
                remove.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            pipe.move()
        
        #for adding new pipes
        if add_pipe:
            score += 1
            pipes.append(Pipe(600))

        #for removing the last pipe if passed
        for r in remove:
            pipes.remove(r)

        #bird hitting the base
        if bird.y + bird.img.get_height() >= 620:
            pass

        base.move()                                     #moving the base
        draw_window(screen, bird, pipes, base, score)   #setup the bird in the screen

    pygame.quit()
    quit()



#-------------running the game-----------
if __name__ == '__main__':
    main()