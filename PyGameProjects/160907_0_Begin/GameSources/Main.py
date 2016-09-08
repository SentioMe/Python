import pygame, sys
from pygame.locals import *

#Required import 'pygame' and 'sys',
#And pygame in all classes, functions... to import by key(*)

pygame.init()                                           #start pygame lib
DISPLAYSURF = pygame.display.set_mode((400, 300))       #set pygame display (resolution, flags, depth)
pygame.display.set_caption('Hello World')               #set display title

while True:                                           #game loop
    for event in pygame.event.get():                   #check a frame, appeared all events
        if event.type  == QUIT:                        #If event equals to QUIT(pygame constant value) then, pygame and system end
            pygame.quit()
            sys.exit()
    pygame.display.update()                            #game frame update


# it this mean, C++ Console methode
# pygame is same C++ WinAPI Framework
# 'print', 'input' is CLI methode

