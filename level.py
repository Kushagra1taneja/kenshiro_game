import pygame
from pytmx.util_pygame import load_pygame
from tiles import*
from settings import tile_size
from player import*
# from support import import_csv_layout,import_cut_graphics
# from layout import load_tiles

class Level:
    def __init__(self,surface):
        # universal setup
        self.display_surface = surface
        self.world_shift = 0

        #tiles that should be ignored by collision detection 
        self.background_layer_sprites = self.load_tiles('background_layer')
        self.cosmetics_sprites = self.load_tiles('cosmetics')
        self.fakes_sprites = self.load_tiles('fakes')
        #tiles that are going to collide
        self.enemy_sprites = self.load_tiles('enemy')
        self.player_sprites = self.load_character_tiles('player')
        #tiles with special purpose
        self.destination_sprites = self.load_tiles('start/end')
        self.crates_sprites = self.load_tiles('power_ups')
        #tiles that should not ignored by collision detection
        self.ground_sprites = self.load_tiles('ground')
        self.float_sprites = self.load_tiles('float')
        self.catacomb_sprites = self.load_tiles('catacomb')
        self.steps_sprites = self.load_tiles('steps')

    def load_tiles(self,layer_name):
        tmx_data = load_pygame('graphics/Environment/Tiled_tsx/level_0.tmx')
        sprite_group = pygame.sprite.Group()

            # for layer in tmx_data.layers:
            #     if hasattr(layer, 'data'):
        layer = tmx_data.get_layer_by_name(layer_name)
        for x, y, surf in layer.tiles():
            pos = (x * tile_size, y * tile_size)
            Tile(pos=pos, surf=surf, groups=sprite_group)

        return sprite_group
    
    def load_character_tiles(self,layer_name):
        tmx_data = load_pygame('graphics/Environment/Tiled_tsx/level_0.tmx')
        sprite_group = pygame.sprite.GroupSingle()

            # for layer in tmx_data.layers:
            #     if hasattr(layer, 'data'):
        layer = tmx_data.get_layer_by_name(layer_name)
        for x, y, surf in layer.tiles():
            # pos = (x * tile_size, y * tile_size)
            # Tile(pos=pos, x=x, y=y, surf=surf, groups=sprite_group)
            player_sprite = Player(x*tile_size,y*tile_size)
            sprite_group.add(player_sprite)

        return sprite_group
    
    def scroll_x(self):
        player = self.player_sprites.sprite
        if player:
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
        player = self.player_sprites.sprite
        if player:
            player.rect.x += player.x_speed * player.direction.x
            for tile in self.ground_sprites.sprites():
                if tile.rect.colliderect(player.rect):
                    if player.direction.x < 0:                #detection if collision is on right or left    
                        player.rect.left = tile.rect.right    #left of the player will placed on right side of the tile
                    elif player.direction.x > 0:
                        player.rect.right = tile.rect.left

            for tile in self.catacomb_sprites.sprites():
                if tile.rect.colliderect(player.rect):
                    if player.direction.x < 0:                #detection if collision is on right or left    
                        player.rect.left = tile.rect.right    #left of the player will placed on right side of the tile
                    elif player.direction.x > 0:
                        player.rect.right = tile.rect.left
                
    def collision_y(self):
        player = self.player_sprites.sprite
        if player:
            player.gravitation()

            for tile in self.ground_sprites.sprites():
                if tile.rect.colliderect(player.rect):
                    if player.direction.y < 0:  # Collision from above
                        player.rect.top = tile.rect.bottom
                        
                    elif player.direction.y > 0:  # Collision from below
                        player.rect.bottom = tile.rect.top
                        player.direction.y = 0  # Stop vertical movement
                        player.onGround = True
                if player.onGround and player.direction.y < 0 and player.direction.y > 1:
                    player.onGround = False

            for tile in self.catacomb_sprites.sprites():
                if tile.rect.colliderect(player.rect):
                    if player.direction.y < 0:  # Collision from above
                        player.rect.top = tile.rect.bottom
                        
                    elif player.direction.y > 0:  # Collision from below
                        player.rect.bottom = tile.rect.top
                        player.direction.y = 0  # Stop vertical movement
                        player.onGround = True
                if player.onGround and player.direction.y < 0 and player.direction.y > 1:
                    player.onGround = False
    
    
    def collision_player_enemy(self):
        player = self.player_sprites.sprite
        if player:
            enemy_hit_list = pygame.sprite.spritecollide(player, self.enemy_sprites, False)
            
            if player.is_slashing :
                
                for enemy in enemy_hit_list:
                    enemy.kill()
            
            
    def update_tiles_position(self):
        for tile in self.ground_sprites:
            tile.rect.x += self.world_shift  # Update tile positions based on shift direction
        for enemy in self.enemy_sprites:
            enemy.rect.x += self.world_shift  # Update tile positions based on shift direction
        # for proj in self.projectile_group:
        #     proj.rect.x += self.world_shift  # Update tile positions based on shift direction
    
    # def collision_projectiles(self):
    #     player = self.player_group.sprite
    #     if player:
    #         for projectile in self.projectile_group.sprites():
            
    #             if pygame.sprite.spritecollideany(projectile, self.tiles_group):
    #                 projectile.kill()  

    #             # Check collision with player
    #             player_hit = pygame.sprite.spritecollideany(projectile, self.player_group)
    #             if player_hit:
    #                 player.health -= 1  
    #                 projectile.kill()  
    #             if player.health <= 0:
    #                 player.kill()
    #                 break


    def enemy_to_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            for tile in self.ground_sprites.sprites():

                if tile.rect.colliderect(enemy.rect):
                    if enemy.direction < 0:                #detection if collision is on right or left    
                        enemy.rect.left = tile.rect.right    #left of the player will placed on right side of the tile
                        enemy.reverse_direction()
                    elif enemy.direction > 0:
                        enemy.rect.right = tile.rect.left
                        enemy.reverse_direction()
   
    # def run(self):
    #     self.update_tiles_position()  # Update tile positions
    #     self.level.ground_sprites.draw(self.display)
    #     self.level.player_sprites.draw(self.display)
    #     self.level.enemy_sprites.draw(self.display)
        
    #     self.level.player_sprites.update(self.world_shift)
    #     self.level.enemy_sprites.update(self.world_shift)
    #     self.enemy_to_reverse()
    #     # self.collision_player_enemy()
    #     # for proj in projectiles:
    #     #     self.projectile_group.add(proj)

    #     # self.projectile_group.draw(self.display)
    #     # self.projectile_group.update()
    #     # self.collision_projectiles()
    #     self.collision_x()
    #     self.collision_y()
    #     self.scroll_x()


    def run(self):
        #run the level for entire game
        self.background_layer_sprites.update(self.world_shift)
        self.background_layer_sprites.draw(self.display_surface)

        self.cosmetics_sprites.update(self.world_shift)
        self.cosmetics_sprites.draw(self.display_surface)

        self.fakes_sprites.update(self.world_shift)
        self.fakes_sprites.draw(self.display_surface)

        self.enemy_sprites.update(self.world_shift)
        self.enemy_sprites.draw(self.display_surface)

        self.player_sprites.update()
        self.player_sprites.draw(self.display_surface)

        self.destination_sprites.update(self.world_shift)
        self.destination_sprites.draw(self.display_surface)

        self.crates_sprites.update(self.world_shift)
        self.crates_sprites.draw(self.display_surface)

        self.ground_sprites.update(self.world_shift)
        self.ground_sprites.draw(self.display_surface)

        self.float_sprites.update(self.world_shift)
        self.float_sprites.draw(self.display_surface)

        self.catacomb_sprites.update(self.world_shift)
        self.catacomb_sprites.draw(self.display_surface)

        self.steps_sprites.update(self.world_shift)
        self.steps_sprites.draw(self.display_surface)

        self.enemy_to_reverse()
        # self.collision_player_enemy()
        # for proj in projectiles:
        #     self.projectile_group.add(proj)

        # self.projectile_group.draw(self.display)
        # self.projectile_group.update()
        # self.collision_projectiles()
        self.collision_x()
        self.collision_y()
        self.scroll_x()
