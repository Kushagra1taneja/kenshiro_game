import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()

      
        self.image = pygame.Surface((4, 4))  
        image= pygame.image.load(f'graphics\\bullet\\bullet.png') 
        self.image=pygame.transform.scale_by(image,0.5)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.counter = 0
      
        self.speed = 5  
        self.direction = direction  

    def update(self):
        self.rect.x += self.speed * self.direction
        self.counter += 1
        if self.counter>=50:
            self.kill()