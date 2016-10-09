import pygame, sys
from pygame.locals import *
import time

pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Sound Test')

'''
pygame.mixer.Sound(string path) : Load to memory a sound effect file with string path
                                  play(), stop()... other methodes access with returned 'Sound' instance
'''
soundObj = pygame.mixer.Sound('../SoundFiles/Sword.wav')
soundObj.play()
time.sleep(1)                   #time.sleep(seconds) is samed to 'C/C++ sleep in windows.h'
soundObj.stop()

'''
pygame.mixer.music : Is a background music controlled class
                     pygame is played only one bgm
                     load(string path) : Load to memory a bgm file with string path
                     play(int loop, float position) : Play a loaded bgm from position(seceond)
                                                      If loop is 0, or bigger then, non looping
'''
pygame.mixer.music.load('../SoundFiles/The Reluctant Heroes (acoustic arrange ver.).mp3')
pygame.mixer.music.play(-1, 135.0)
pygame.mixer.music.stop()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()