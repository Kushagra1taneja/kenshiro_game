import pygame
from player import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)

    def update(self,shift):
        self.rect.x += shift

# class Player_tile(Tile):
#     def __init__(self,pos,x,y, surf, groups):
#         super().__init__(pos,surf, groups)
#         self.player_module = Player(x,y)