import pygame, sys
from pygame.locals import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Font Test')

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)

fontObj = pygame.font.Font('freesansbold.ttf', 32)                  #Create a instance of font object(font name, font size)
textSurfaceObj = fontObj.render('Hello World!', True, GREEN, BLUE) #Create a instance font surface
textRectObj = textSurfaceObj.get_rect()                             #Returned a rect by font surface
textRectObj.center = (200, 150)                                     #Move a rect(font) position

while True:
    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(textSurfaceObj, textRectObj)                   #Copied font surface with rect
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()