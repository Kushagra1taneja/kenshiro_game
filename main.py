import pygame
import sys
from settings import *
from level import Level

pygame.init()

game_state = False
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(screen)
background = pygame.image.load('graphics//District//Backgound//clouds-with-background.png')
background = pygame.transform.rotozoom(background, 0, 3)
pixelfont = pygame.font.Font("Font//vermin_vibes_1989.ttf", 78)
pixelfont_small = pygame.font.Font("Font//vermin_vibes_1989.ttf", 40)

overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
overlay.fill((0, 0, 0, 100))  

music = pygame.mixer.Sound("Audio\cyber.mp3")
music.set_volume(0.2)
music.play(loops = -1)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_state = True

    if game_state:
        screen.blit(background, (0, -10))
        level.run()
    else:
        screen.blit(background, (0, -10)) 
        screen.blit(overlay, (0, 0))  
        
        text = pixelfont.render("Kenshiro : Memories Echo", False, "Yellow")
        start_text = pixelfont_small.render("Press Space to Start", False, "Yellow")
        
        text_rect = text.get_rect(center = (screen_width // 2, screen_height // 2 - 50))
        start_text_rect = start_text.get_rect(center = (screen_width // 2, screen_height // 2 + 100))
        
        screen.blit(text, text_rect)  
        screen.blit(start_text, start_text_rect)
    pygame.display.update()
    clock.tick(60)
