import pygame
import math
import random 
from random import randrange
import os
from pygame.locals import *

#General intializer functions

pygame.init()

scrnWidth = 594
scrnHeight = 337
screen = pygame.display.set_mode((scrnWidth, scrnHeight))
pygame.display.set_caption("BEAR GP3")

#Background stuff
bg = pygame.image.load("forestBG.jpg")
bgX = 0
bgX2 = bg.get_width()
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
            

    def draw(self, win, scroll, fly_height):
        #grumpyBee
        w, h = pygame.display.get_surface().get_size()
        win.blit(self.img, (w + scroll*1.5,fly_height))

grumpyBee = grumpyBee()

#class for honey jar
class honeyJar(object):

    def __init__(self):
        self.honeyJar = pygame.image.load("honeyJar.png")
        self.honeyJar = pygame.transform.scale(self.honeyJar,(50,52))

    def draw(self, win, scroll, fly_height):
        #honey jar
        w, h = pygame.display.get_surface().get_size()
        win.blit(self.honeyJar, (w + scroll,fly_height))


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

class Player(object):

    run = [pygame.image.load('stand.png')]
    jump = [pygame.image.load('jump.png')]
    slide = [pygame.image.load('crouch.png')]
    attack = [pygame.image.load('run1.png')]
    fall = [pygame.image.load('fall.png')]
    jumpList = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.sliding = False
        self.attacking = False
        self.falling = False
        self.slideCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.attackCount = 0
        self.slideUp = False

    def draw(self, win):

        if self.falling:
            win.blit(self.fall, (self.x, self.y + 30))
        elif self.jumping:
            self.y -= self.jumpList[self.jumpCount] * 1.2
            win.blit(self.jump[self.jumpCount//128], (self.x,self.y)) #may need to increase
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0
            self.hitbox = (self.x+ 4,self.y,self.width-24,self.height-10) #Default hitbox
        elif self.sliding or self.slideUp:
            if self.slideCount < 20:
                self.y += 1
                self.hitbox = (self.x+ 4,self.y,self.width-24,self.height-10) #Sliding hitbox
            elif self.slideCount == 80:
                self.y -= 19
                self.sliding = False
                self.slideUp = True
            elif self.slideCount > 20 and self.slideCount < 80: # NEW
                self.hitbox = (self.x,self.y+3,self.width-8,self.height-35) # NEW
            if self.slideCount >= 110:
                self.slideCount = 0
                self.slideUp = False
                self.runCount = 0
            win.blit(self.slide[self.slideCount//150], (self.x,self.y)) #may need to increase
            self.slideCount += 1
            
        elif self.attacking:
            win.blit(self.attack[self.attackCount//128], (self.x,self.y)) #may need to increase
            self.attackCount += 1
            if self.attackCount > 108:
                self.attackCount = 0
                self.attacking = False
                

        else:
            if self.runCount > 42:
                self.runCount = 0
            win.blit(self.run[self.runCount//50], (self.x,self.y)) #may need to increase
            self.runCount += 1
            self.hitbox = (self.x+ 4,self.y,self.width-24,self.height-13)

#Game main 
speed = 30
ground = ground()
platform = platform()
hole = hole()
honeyJar = honeyJar()



def redrawWindow():
    screen.blit(bg,(bgX,0))
    screen.blit(bg,(bgX2,0))
    
    pygame.display.update()
    
    
bear = Player(200,65,98,131)

#Game main loop
pygame.time.set_timer(USEREVENT + 1, 500)

run = True
while run:

    bear.draw(screen)
    if scroll ==0:
        honeyJar_y_pos = randrange(0,200)
        fly_height = randrange(0,200)
    pygame.display.update()
    pygame.time.Clock().tick(30) #Set FPS


    scroll -=3
    
    if abs(scroll) > bgWidth:
        scroll = 0


    for i in range(0, tiles):
        screen.blit(bg,(i* bgWidth + scroll,0))
    
    ground.draw(screen, scroll)
    platform.draw(screen, scroll)
    hole.draw(screen,scroll)
    grumpyBee.draw(screen,scroll, fly_height)
    honeyJar.draw(screen,scroll, honeyJar_y_pos)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == USEREVENT + 1:
            speed += 1
            
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] or keys[pygame.K_UP]: # If user hits space or up arrow key
        if not(bear.jumping):  # If we are not already jumping
            bear.jumping = True

    if keys[pygame.K_DOWN]:  # If user hits down arrow key
        if not(bear.sliding):  # If we are not already sliding
            bear.sliding = True

    if keys[pygame.K_r]:
        if not(bear.attacking):
            bear.attacking = True
    
    pygame.display.update()


pygame.QUIT
