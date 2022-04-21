import pygame
import math
import random 
from random import randrange
import os
from pygame.locals import *

#General intializer functions

"""These are general initializer functions for the game, such as loading the screen width/height, the score, and the window title."""

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
tiles = math.ceil((scrnWidth / bgWidth)) + 1
scroll = 0
myfont = pygame.font.SysFont("Cascadia Mono Light", 40)
WHITE = (255,255,255)




"""General notes: Each object on the screen usually consists of a constructor, a draw function (sets hitbox/size/texture), and a collision
function to handle interactions with other objects on the screen."""


"""This is the main class for the enemy. Deducts points upon collision with the player."""
# Class for the grumpy bee
class grumpyBee(object):
    def __init__(self,x,y,width,height):
        self.img = pygame.image.load('grumpyBee/1.png').convert_alpha()
        self.img = pygame.transform.scale(self.img,(50,50))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5   
        self.type = "grumpy"
    
            

    def draw(self, win):
        self.hitbox = (self.x + 10, self.y + 5, self.width - 20, self. height -5)
        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        win.blit(self.img, (self.x,self.y))

   
    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
        return False
       
"""This is a secondary class for another enemy, which deducts more points than the standard enemy upon collision with the player."""
class weirdBee(object):
    def __init__(self,x,y,width,height):
        self.img = pygame.image.load('weirdBee/2.png').convert_alpha()
        self.img = pygame.transform.scale(self.img,(50,50))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 2   
        self.type = "weird"
            

    def draw(self, win):
        self.hitbox = (self.x + 10, self.y + 5, self.width - 20, self. height -5)
        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        win.blit(self.img, (self.x,self.y))

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
        return False



#class for honey jar
"""The honey jar rewards the player by increasing their score"""
class honeyJar(object):

    def __init__(self,x,y,width,height):
        self.img = pygame.image.load("honeyJar.png")
        self.img = pygame.transform.scale(self.img,(50,52))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 3

    def draw(self, win):
        self.hitbox = (self.x+10, self.y + 5, self.width - 20, self.height -5)
        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        win.blit(self.img, (self.x,self.y))

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]: #Hitbox for collisions
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
        return False
        


# Class for the ground object
"""The ground is generated infinitely and is where the player starts from."""
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

     

class hole(object):
    def __init__(self):
        self.hole = pygame.image.load("hole.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.hole)

    def draw(self, win, scroll):
       
        hole_height = 290
        hole_width =  10
        w, h = pygame.display.get_surface().get_size()

        repeat = math.ceil(w*2 / hole_width)+1
        num1 = 3
        num2 = 8
        for i in range(repeat):
            if i != num1 and i != num2 :
                win.blit(self.hole, (600*i + scroll + 350,hole_height))

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
        return False

    
"""This is the main player class, the bear character."""
class Player(object):
    #Load textures
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

    def draw(self, win): #Handle cases for various states

        #These if/else statements handle texture and hitbox changes, based on what position/state the player is in.
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
                self.hitbox = (self.x+ 4,self.y,self.width-24,self.height-50) #Sliding hitbox
            elif self.slideCount == 80:
                self.y -= 19
                self.sliding = False
                self.slideUp = True
            elif self.slideCount > 20 and self.slideCount < 80: 
                self.hitbox = (self.x,self.y+3,self.width-8,self.height-50) 
            if self.slideCount >= 110:
                self.slideCount = 0
                self.slideUp = False
                self.runCount = 0
            win.blit(self.slide[self.slideCount//150], (self.x,self.y)) 
            self.slideCount += 1
            
        elif self.attacking:
            win.blit(self.attack[self.attackCount//128], (self.x,self.y))
            self.attackCount += 1
            if self.attackCount > 108:
                self.attackCount = 0
                self.attacking = False
                

        else:
            if self.runCount > 42:
                self.runCount = 0
            win.blit(self.run[self.runCount//50], (self.x,self.y)) 
            self.runCount += 1
            self.hitbox = (self.x+ 4,self.y,self.width-24,self.height-13)
        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)


speed = 30
ground = ground() #Instantiate ground and holes
hole = hole()

bees = [] #Instantiate lists for enemy loops
jars = []


#score
"""This function is used for updating the game screen with new objects."""
score = 0
def redrawWindow(): #Drawing enemies/honey jars
    global score
    for bee in bees:
        bee.x = bee.x - bee.vel
        if bee.x < bee.width * -1:
            bees.pop(bees.index(bee))
        bee.draw(screen)
        if bee.collide(bear.hitbox):
            if bee.type == "weird":
                score = score - 10
            elif bee.type == "grumpy":
                score = score - 5

    for jar in jars:
        jar.x = jar.x - jar.vel
        if jar.x < jar.width*-1:
            jars.pop(jars.index(jar))
        jar.draw(screen)
        if jar.collide(bear.hitbox):
            score = score + 15

    

    
bear = Player(200,155,98,131) #Starting position of player


pygame.time.set_timer(USEREVENT + 1, 500)
pygame.time.set_timer(USEREVENT+2,1000)

run = True

#Game main loop
"""This is the main game loop - this insantiates everything on the screen, the FPS, the pictures, the scrolling background, etc."""
while run:
    redrawWindow()
    bear.draw(screen) #Draw player on screen

    honeyJar_y_pos = randrange(0,scrnHeight - 119)
    fly_height = randrange(0,scrnHeight - 119)
    pygame.display.update()
    pygame.time.Clock().tick(30) #Set FPS


    scroll -=3
    
    if abs(scroll) > bgWidth:
        scroll = 0

    #Draw ground tiles
    for i in range(0, tiles):
        screen.blit(bg,(i* bgWidth + scroll,0))
    
    ground.draw(screen, scroll)
   
    hole.draw(screen,scroll)
    #grumpyBee.draw(screen,scroll, fly_height)
    #honeyJar.draw(screen,scroll, scrnHeight//2)
    
    
    #Deals with user events, such as key presses 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == USEREVENT + 1:
            speed += 1
        if event.type == USEREVENT+2:
            r = random.randrange(0,3)
            if r == 0:
                bees.append(grumpyBee(scrnWidth, fly_height, 50, 50))
            elif r == 1:
                jars.append(honeyJar(scrnWidth, fly_height, 50, 52))
            elif r == 2:
                bees.append(weirdBee(scrnWidth, fly_height, 50,50))
            
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] or keys[pygame.K_UP]: # If user hits space or up arrow key
        if not(bear.jumping):  # If we are not already jumping
            bear.jumping = True

    if keys[pygame.K_DOWN]:  # If user hits down arrow key
        if not(bear.sliding):  # If we are not already sliding
            bear.sliding = True

    if keys[pygame.K_r]: #Attack state (not used)
        if not(bear.attacking):
            bear.attacking = True

    text = myfont.render("Score {0}".format(score), 1, WHITE)
    screen.blit(text, (240,10))
    
    pygame.display.update()


pygame.QUIT #Game over