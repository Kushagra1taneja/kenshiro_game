import pygame
from settings import screen_height
from settings import screen_width

from projectile import Projectile
import os
pygame.init()


clock = pygame.time.Clock()

screen = pygame.display.set_mode((screen_width,screen_height))

projectiles = pygame.sprite.Group()
# all_sprites = pygame.sprite.Group();
class BaseEnemy(pygame.sprite.Sprite):

    def __init__(self,char_type,x, y, health, speed, projectile_frequency):
        super().__init__()

        self.toreverse= False
        # self.image = pygame.Surface((30, 30)) #not required
        # self.rect = self.image.get_rect()#not required
        # self.rect.topleft = (x-10, y-2)#not required
        self.projectile_frequency = projectile_frequency  # Fire every 120 frames
        self.projectile_timer = 0

        self.speed = speed 
        self.direction = 1  
        self.health = health
       
       #gopi start
       
       
        # self.char_type = char_type
        # self.flip = False
        # self.animation_list =[]#main list of list of images
        # self.frame_index = 0
        # self.action = 0
        # self.update_time = pygame.time.get_ticks()
        
        
        self.char_type = char_type
        self.jump =False
        self.in_air = True
        self.flip = False
        self.animation_list =[]
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        
        
        animation_types = ['run_attack','deth']
        for animation in animation_types:
            temp_list = []
            
            num_of_frames = len(os.listdir(f'graphics/{self.char_type}/{animation}'))
            
            for i in range(num_of_frames):
                img = pygame.image.load(f'graphics/{self.char_type}/{animation}/{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width() ), int(img.get_height())))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        if self.flip :
            oringnalimage = self.animation_list[self.action][self.frame_index]    
            self.image = pygame.transform.flip(oringnalimage, True, False)
            
        else :
            self.image = self.animation_list[self.action][self.frame_index] 
        
        self.rect = self.image.get_rect()
        self.rect.center = (x,y+3)
    
    def draw(self):
        screen.blit(self.image,self.rect)
    
    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        current_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.action][self.frame_index]
        if ((current_time - self.update_time) > ANIMATION_COOLDOWN):
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        
        if (self.frame_index >= len(self.animation_list[self.action])):
            self.frame_index = 0
            
    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
        
    def update_1(self):
        if(self.direction < 0):
            self.flip = True
        elif(self.direction > 0):
            self.flip = False
        # gopi end
        
                       
    def shoot_projectile(self):
        # Create a new projectile instance
        projectile = Projectile(self.rect.centerx+(self.image.get_width())*self.direction*0.6, self.rect.centery, self.direction)
        projectiles.add(projectile)

    def reverse_direction(self):
        self.direction *= -1    
        if(self.direction < 0):
            self.flip = True
        elif(self.direction > 0):
            self.flip = False

    def update(self):
        self.rect.x += self.speed * self.direction
        self.projectile_timer += 1
        self.update_animation()
        

        if self.toreverse :
            self.reverse_direction()
            self.toreverse=False

        if self.projectile_timer >= self.projectile_frequency:
            self.shoot_projectile()
            self.projectile_timer = 0
        if self.flip :
            oringnalimage = self.animation_list[self.action][self.frame_index]    
            self.image = pygame.transform.flip(oringnalimage, True, False)
            
        else :
            self.image = self.animation_list[self.action][self.frame_index] 
               


    

class Knight(BaseEnemy):
    def __init__(self, x, y):
        super().__init__('Knight',x, y+10, health=100 , speed=3, projectile_frequency=60)

        self.update_animation()
        self.draw()
        if(self.health > 0):
            self.update_action(0)
        else:
            self.update_action(1)

class Pawn(BaseEnemy):
    def __init__(self, x, y):
        super().__init__('Pawn',x,  y+10, health=40 , speed=1, projectile_frequency=120)

        self.update_animation()
        self.draw()
        if(self.health > 0):
            self.update_action(0)
        else:
            self.update_action(1) 

class Queen(BaseEnemy):
    def __init__(self, x, y):
        super().__init__('Queen',x, y+10, health=200 , speed=1,projectile_frequency=120)

        self.update_animation()
        self.draw()
        if(self.health > 0):
            self.update_action(0)
        else:
            self.update_action(1)


pygame.display.update()    



