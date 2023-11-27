import pygame
from layout import tile_size

class tiles(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((tile_size, tile_size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def update(self, x_shift):
        self.rect.x += x_shift  # Update tile position based on x_shift
