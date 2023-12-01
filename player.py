import pygame
from importer import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.import_player_animation()

        # animations
        self.frame_index = 0
        self.animation_speed = 0.15

        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))

        # player attributes
        self.x_speed = 8
        self.direction = pygame.math.Vector2(0, 0)
        self.y_speed = -16
        self.health = 1000
        # player physics
        self.gravity = 0.8

        # player state
        self.status = 'idle'
        self.facing_right = True
        self.onGround = False  # Start the player off the ground

        # slash animation attributes
        self.slash_animation = self.animations['slash']
        self.slash_frame_index = 0
        self.slash_animation_speed = 0.30
        self.is_slashing = False
        
    def import_player_animation(self):
        base_path = 'graphics\\Hero\\'
        self.animations = {
            'idle': [],
            'jump': [],
            'run': [],
            'slash': []
        }
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(base_path + animation)

    def animate(self):
        
        if self.onGround:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        
        if not self.is_slashing:
            
            animation = self.animations[self.status]
            self.frame_index += self.animation_speed
            
            if int(self.frame_index) >= len(animation):
                self.frame_index = 0
           
            image = animation[int(self.frame_index)]
            if self.direction.x < 0:
                self.image = pygame.transform.flip(image, True, False)
            else:
                self.image = image

    def attack_animate(self):
        if self.status != 'slash':
            self.is_slashing = True
            self.status = 'slash'

    def animate_slash(self):
        if self.is_slashing:
            self.image = self.slash_animation[int(self.slash_frame_index)]
            self.slash_frame_index += self.slash_animation_speed
            if self.slash_frame_index >= len(self.slash_animation):
                self.slash_frame_index = 0
                self.is_slashing = False
                self.status = 'idle'

    def animation_state(self):
        if self.direction.y == 0 and self.direction.x != 0:  # run
            self.status = 'run'
        elif self.direction.y != 0:  # jump
            self.status = 'run'
        elif self.direction.x == 0 and self.direction.y == 0:  # idle
            if not self.is_slashing:
                self.status = 'idle'

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_v]:
            self.attack_animate()
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.onGround and self.is_slashing == False:
            self.jump()
        

    def jump(self):
        self.direction.y = self.y_speed
        self.onGround = False

    def gravitation(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self):
        self.get_input()
        self.animate()
        self.animation_state()
        self.animate_slash()
