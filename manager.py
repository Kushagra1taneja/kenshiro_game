import pygame
from enviroment import tiles
from layout import tile_size
from player import Player
from enemy import BaseEnemy,Pawn,Knight,projectiles

class level_setup:
    def __init__(self, layout, surface):
        self.display = surface
        self.tiles_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()
        self.enemy_group = pygame.sprite.Group()
        self.projectile_group = pygame.sprite.Group()
        self.world_shift = 0

        self.onGround = True
        self.level_setup(layout)
        
    def level_setup(self, layout):
        for rows_index, rows in enumerate(layout):
            for cols_index, cols in enumerate(rows):
                x = cols_index * tile_size
                y = rows_index * tile_size
                if cols == 'x':
                    tile = tiles(x, y)
                    self.tiles_group.add(tile)
                if cols == 'p':
                    player_sprite = Player(x, y)
                    self.player_group.add(player_sprite)
                if cols == 'w':
                    enemy_sprite = Pawn(x, y)
                    self.enemy_group.add(enemy_sprite)
                if cols == 'k':
                    enemy_sprite = Knight(x, y)
                    self.enemy_group.add(enemy_sprite)

    def scroll_x(self):
        player = self.player_group.sprite
        player_x = player.rect.centerx
        direction = player.direction.x
        speed = player.x_speed

        if player_x >= 650 and direction > 0:
            self.world_shift = -8
            player.x_speed = 0
            
        elif player_x <= 10 and direction < 0:
            self.world_shift = 8
            player.x_speed = 0
        else:
            self.world_shift = 0
            player.x_speed = 8
    
    def collision_x(self):
        player = self.player_group.sprite

        player.rect.x += player.x_speed * player.direction.x
        for tile in self.tiles_group.sprites():
            if tile.rect.colliderect(player.rect):
                if player.direction.x < 0:                #detection if collision is on right or left    
                    player.rect.left = tile.rect.right    #left of the player will placed on right side of the tile
                elif player.direction.x > 0:
                    player.rect.right = tile.rect.left
                
    def collision_y(self):
        player = self.player_group.sprite

        player.gravitation()

        for tile in self.tiles_group.sprites():
            if tile.rect.colliderect(player.rect):
                if player.direction.y < 0:  # Collision from above
                    player.rect.top = tile.rect.bottom
                    
                elif player.direction.y > 0:  # Collision from below
                    player.rect.bottom = tile.rect.top
                    player.direction.y = 0  # Stop vertical movement
                    player.onGround = True
            if player.onGround and player.direction.y < 0 and player.direction.y > 1:
                player.onGround = False
    def update_tiles_position(self):
        for tile in self.tiles_group:
            tile.rect.x += self.world_shift  # Update tile positions based on shift direction
        for enemy in self.enemy_group:
            enemy.rect.x += self.world_shift  # Update tile positions based on shift direction
        for proj in self.projectile_group:
            proj.rect.x += self.world_shift  # Update tile positions based on shift direction
    
    def collision_projectiles(self):
        for projectile in self.projectile_group.sprites():
           
            if pygame.sprite.spritecollideany(projectile, self.tiles_group):
                projectile.kill()  

            # Check collision with player
            player_hit = pygame.sprite.spritecollideany(projectile, self.player_group)
            if player_hit:
                # player_hit.onHit()  
                projectile.kill()  


    def enemy_to_reverse(self):
        for enemy in self.enemy_group.sprites():
            for tile in self.tiles_group.sprites():

                if tile.rect.colliderect(enemy.rect):
                    if enemy.direction < 0:                #detection if collision is on right or left    
                        enemy.rect.left = tile.rect.right    #left of the player will placed on right side of the tile
                        enemy.reverse_direction()
                    elif enemy.direction > 0:
                        enemy.rect.right = tile.rect.left
                        enemy.reverse_direction()
   
    def run(self):
        self.update_tiles_position()  # Update tile positions
        self.tiles_group.draw(self.display)
        self.player_group.draw(self.display)
        self.enemy_group.draw(self.display)
        
        self.player_group.update()
        self.enemy_group.update()
        self.enemy_to_reverse()

        for proj in projectiles:
            self.projectile_group.add(proj)

        self.projectile_group.draw(self.display)
        self.projectile_group.update()
        self.collision_projectiles()
        self.collision_x()
        self.collision_y()
        self.scroll_x()
