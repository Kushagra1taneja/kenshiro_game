import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()

      
        self.image = pygame.Surface((8, 8))  
        self.image.fill((0, 200, 0)) 
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.counter = 0
      
        self.speed = 5  
        self.direction = direction  

    def update(self):
        self.rect.x += self.speed * self.direction
        self.counter += 1
        if self.counter>=570:
            self.kill()