import pygame
import math
import random 

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
        for i in range(repeat*2):
            if i != num1 and i != num2:
                win.blit(self.ground, (ground_width*i + scroll,ground_height))
            #if i == repeat:
                #num1 = random.randrange(repeat)
                #num2 = random.randrange(repeat)   


#Game main 
ground = ground()
run = True
while run:


    pygame.time.Clock().tick(60) #Set FPS

    scroll -=3
    
    if abs(scroll) > bgWidth:
        scroll = 0


    for i in range(0, tiles):
        screen.blit(bg,(i* bgWidth + scroll,0))
    ground.draw(screen, scroll)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()


pygame.QUIT
