import pygame
import math
import random 
import os

#General intializer functions

pygame.init()

scrnWidth = 594
scrnHeight = 337
screen = pygame.display.set_mode((scrnWidth, scrnHeight))
pygame.display.set_caption("BEAR GP3")

#Background stuff
bg = pygame.image.load("forestBG.jpg")
bgWidth = bg.get_width()
bgHeight = bg.get_height()
scroll = 0
tiles = math.ceil((scrnWidth / bgWidth)) + 1

# Class for the grumpy bee
class grumpyBee(object):
    def __init__(self):
        self.img = []
        for i in range(1,6):
            self.img = pygame.image.load('grumpyBee/'+ str(i) + '.png').convert_alpha()
            self.img = pygame.transform.scale(self.img,(50,50))
            self.mask = pygame.mask.from_surface(self.img)
            

    def draw(self, win, scroll):
        #grumpyBee
        fly_height = 175
        w, h = pygame.display.get_surface().get_size()
        win.blit(self.img, (w + scroll*1.5,fly_height))

grumpyBee = grumpyBee()


# Class for the ground object

class ground(object):
    def __init__(self):
        self.ground = pygame.image.load("ground.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.ground)

    def draw(self, win, scroll):
        #ground
        ground_height = 250
        ground_width =  119
        w, h = pygame.display.get_surface().get_size()

        repeat = math.ceil(w*2 / ground_width)+1
        num1 = 3
        num2 = 8
        for i in range(repeat):
            if i != num1 and i != num2 :
                win.blit(self.ground, (ground_width*i + scroll,ground_height))
            
            #if i == repeat:
                #num1 = random.randrange(repeat)
                #num2 = random.randrange(repeat)   

#Works more like a hill then a platform
class platform(object):
    def __init__(self):
        self.platform = pygame.image.load("ground.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.platform)

    def draw(self, win, scroll):
        #ground
        platform_height = 200
        platform_width =  10
        w, h = pygame.display.get_surface().get_size()

        repeat = math.ceil(w*2 / platform_width)+1
        num1 = 3
        num2 = 8
        for i in range(repeat):
            if i != num1 and i != num2 :
                win.blit(self.platform, (600*i + scroll,platform_height))
                
           

class hole(object):
    def __init__(self):
        self.hole = pygame.image.load("hole.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.hole)

    def draw(self, win, scroll):
       
        hole_height = 250
        hole_width =  10
        w, h = pygame.display.get_surface().get_size()

        repeat = math.ceil(w*2 / hole_width)+1
        num1 = 3
        num2 = 8
        for i in range(repeat):
            if i != num1 and i != num2 :
                win.blit(self.hole, (600*i + scroll + 350,hole_height))



#Game main 
ground = ground()
platform = platform()
hole = hole()
run = True
while run:


    pygame.time.Clock().tick(60) #Set FPS

    scroll -=3
    
    if abs(scroll) > bgWidth:
        scroll = 0


    for i in range(0, tiles):
        screen.blit(bg,(i* bgWidth + scroll,0))
    ground.draw(screen, scroll)
    platform.draw(screen, scroll)
    hole.draw(screen,scroll)
    grumpyBee.draw(screen,scroll)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()


pygame.QUIT
