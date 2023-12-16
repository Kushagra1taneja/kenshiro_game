import pygame
import sys
from settings import *
from level import Level

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(screen)
background = pygame.image.load('graphics//District//Backgound//clouds-with-background.png')
background = pygame.transform.rotozoom(background, 0, 3)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.blit(background, (0,-10))
    level.run()
    pygame.display.update()
    clock.tick(60)