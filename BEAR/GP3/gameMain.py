import pygame
import math
import random 
from random import randrange
import os
from pygame.locals import *

#General intializer functions

"""These are general initializer functions for the game, such as loading the screen width/height, the score, and the window title."""

pygame.init()
 #Settings
hitboxFlag = False #For debugging/hitboxes
scrnWidth = 594
scrnHeight = 337
screen = pygame.display.set_mode((scrnWidth, scrnHeight))
pygame.display.set_caption("BEAR-ly Captured")

#Background stuff
bg = pygame.image.load("img/forestBG.jpg")
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
        self.img = pygame.image.load('img/grumpyBee/1.png').convert_alpha()
        self.img = pygame.transform.scale(self.img,(50,50))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5   
        self.type = "grumpy"
    
            

    def draw(self, win):
        self.hitbox = (self.x + 10, self.y + 5, self.width - 20, self. height -5)
        self.hitboxRect = pygame.Rect(self.hitbox)
        if hitboxFlag:
            pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        win.blit(self.img, (self.x,self.y))
       
"""This is a secondary class for another enemy, which deducts more points than the standard enemy upon collision with the player."""
class weirdBee(object):
    def __init__(self,x,y,width,height):
        self.img = pygame.image.load('img/weirdBee/2.png').convert_alpha()
        self.img = pygame.transform.scale(self.img,(50,50))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 2   
        self.type = "weird"
            

    def draw(self, win):
        self.hitbox = (self.x + 10, self.y + 5, self.width - 20, self. height -5)
        self.hitboxRect = pygame.Rect(self.hitbox)
        if hitboxFlag:
            pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        win.blit(self.img, (self.x,self.y))


#class for honey jar
"""The honey jar rewards the player by increasing their score"""
class honeyJar(object):

    def __init__(self,x,y,width,height):
        self.img = pygame.image.load("img/honeyJar.png")
        self.img = pygame.transform.scale(self.img,(50,52))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 3

    def draw(self, win):
        self.hitbox = (self.x+10, self.y + 5, self.width - 20, self.height -5)
        self.hitboxRect = pygame.Rect(self.hitbox)
        if hitboxFlag:
            pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        win.blit(self.img, (self.x,self.y))

class hornedBee(object):
    def __init__(self,x,y,width,height):
        self.img = pygame.image.load('img/hornedBee/sprite2.png').convert_alpha()
        self.img = pygame.transform.scale(self.img,(50,50))
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 9  
        self.type = "horned"
            

    def draw(self, win):
        self.hitbox = (self.x + 10, self.y + 5, self.width - 20, self. height -5)
        self.hitboxRect = pygame.Rect(self.hitbox)
        if hitboxFlag:
            pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        win.blit(self.img, (self.x,self.y))


# Class for the ground object
"""The ground is generated infinitely and is where the player starts from."""
class ground(object):
    def __init__(self):
        self.ground = pygame.image.load("img/ground.png").convert_alpha()
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
            win.blit(self.ground, (ground_width*i + scroll,ground_height))
            
            #if i == repeat:
                #num1 = random.randrange(repeat)
                #num2 = random.randrange(repeat)   

     
    
"""This is the main player class, the bear character."""
class Player(object):
    #Load textures
    run = [pygame.image.load('img/stand.png')]
    jump = [pygame.image.load('img/jump.png')]
    slide = [pygame.image.load('img/crouch.png')]
    attack = [pygame.image.load('img/run1.png')]
    fall = [pygame.image.load('img/fall.png')]
    run[0] = pygame.transform.scale(run[0],(75,100))
    jump[0] = pygame.transform.scale(jump[0],(75,100))
    slide[0] = pygame.transform.scale(slide[0],(75,100))
    attack[0] = pygame.transform.scale(attack[0],(75,100))
    fall[0] = pygame.transform.scale(fall[0],(75,100))

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
            self.hitboxRect = pygame.Rect(self.hitbox)
        elif self.sliding or self.slideUp:
            if self.slideCount < 20:
                self.y += 1
                self.hitbox = (self.x+ 4,self.y+40,self.width-30,self.height-50) #Sliding hitbox
                self.hitboxRect = pygame.Rect(self.hitbox)
            elif self.slideCount == 80:
                self.y -= 19
                self.sliding = False
                self.slideUp = True
            elif self.slideCount > 20 and self.slideCount < 80: 
                self.hitbox = (self.x,self.y+40,self.width-8,self.height-50)
                self.hitboxRect = pygame.Rect(self.hitbox)
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
            self.hitboxRect = pygame.Rect(self.hitbox)
        if hitboxFlag:
            pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
          
"""This screen appears at the end of the game, after a minute has elapsed. Displays score."""

#end screen function
def endScreen(win):
    global score,bestScore,scrnWidth,scrnHeight
    #load image
    es = pygame.image.load("img/Bear-ly Captured.jpg")
    es = pygame.transform.scale(es,(scrnWidth,scrnHeight))
    mask = pygame.mask.from_surface(es)
    #image variables
    w = 670
    h = 500
    #reset variables 
    speed = 30

    #new game loop
    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                bear.falling = False
                bear.jumping = False
                bear.slideing = False
        win.blit(es, (0,0))
        largeFont = pygame.font.SysFont('Cascadia Mono Light', 60)
        currentScore = largeFont.render("Score: " + str(score),1,WHITE)
        win.blit(currentScore, (scrnWidth/2 - currentScore.get_width()/2,150))
        pygame.display.update()


speed = 30
ground = ground() #Instantiate ground and holes

bees = [] #Instantiate lists for enemy loops
jars = []


#score
"""This function is used for updating the game screen with new objects."""
score = 0
bestScore = 0
def redrawWindow():
    global score, bestScore
def redrawWindow(): #Drawing enemies/honey jars
    global score
    for bee in bees:
        bee.x = bee.x - bee.vel
        if bee.x < bee.width * -1:
            bees.pop(bees.index(bee))
        bee.draw(screen)
        collide = bee.hitboxRect.colliderect(bear.hitboxRect)
        if collide:
            if bee.type == "weird":
                score = score - 10
            elif bee.type == "grumpy":
                score = score - 5
            elif bee.type == "horned":
                score = score - 2
            bees.pop(bees.index(bee))

    for jar in jars:
        jar.x = jar.x - jar.vel
        if jar.x < jar.width*-1:
            jars.pop(jars.index(jar))
        jar.draw(screen)
        collide = jar.hitboxRect.colliderect(bear.hitboxRect)
        if collide:
            score = score + 15
            jars.pop(jars.index(jar))

    

    
bear = Player(150,175,90,100) #Starting position of player


pygame.time.set_timer(USEREVENT + 1, 500)
pygame.time.set_timer(USEREVENT+2,randrange(2000,3500))
pygame.time.set_timer(USEREVENT+3,randrange(1000,1750))

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
                bees.append(weirdBee(scrnWidth, fly_height, 50,50))
            elif r == 2:
                bees.append(hornedBee(scrnWidth, fly_height,35,35))
        if event.type == USEREVENT+3:
                jars.append(honeyJar(scrnWidth, fly_height, 50, 52))
            
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
