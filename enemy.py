import pygame
from projectile import Projectile

projectiles = pygame.sprite.Group();
# all_sprites = pygame.sprite.Group();
class BaseEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, health, speed, projectile_frequency):
        super().__init__()

        self.toreverse= False;
        self.image = pygame.Surface((30, 30)) 
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y-2)
        self.projectile_frequency = projectile_frequency  # Fire every 120 frames
        self.projectile_timer = 0
        self.distance=0;
       
        self.speed = speed 
        self.direction = 1  
        self.health = health
    def shoot_projectile(self):
        # Create a new projectile instance
        projectile = Projectile(self.rect.centerx, self.rect.centery, self.direction)
        projectiles.add(projectile)

        

    def update(self):

        self.projectile_timer += 1;
        self.distance += abs(self.speed)
        if self.health<=0:
            self.kill()


        if self.projectile_timer >= self.projectile_frequency:
            self.shoot_projectile()
            self.projectile_timer = 0
        else :
            self.rect.x += self.speed * self.direction
        

    def reverse_direction(self):
        self.direction *= -1
    
class Knight(BaseEnemy):
    def __init__(self, x, y):
        super().__init__(x, y, health=100 , speed=2, projectile_frequency=120)
        self.image.fill((255, 0, 0))  

class Pawn(BaseEnemy):
    def __init__(self, x, y):
        super().__init__(x, y, health=5000 , speed=1, projectile_frequency=240)
        self.image.fill((0, 255, 0))  

class Queen(BaseEnemy):
    def __init__(self, x, y):
        super().__init__(x, y, health=200 , speed=1)
        self.image.fill((0, 0, 255))  




