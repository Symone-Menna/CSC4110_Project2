import pygame
import math

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


#Game main loop
run = True
while run:


    pygame.time.Clock().tick(60) #Set FPS

    scroll -=5
    
    if abs(scroll) > bgWidth:
        scroll = 0


    for i in range(0, tiles):
        screen.blit(bg,(i* bgWidth + scroll,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()


pygame.QUIT
