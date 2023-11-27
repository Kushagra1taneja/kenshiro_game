import pygame
import sys
 
from layout import *
from manager import level_setup  # Corrected import name "generate" to "generate" assuming it's the correct module name

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
setup = level_setup(stage1, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((50, 50 ,50))
    setup.run()
    pygame.display.update()
    clock.tick(60)