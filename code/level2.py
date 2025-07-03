import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice
from weapon import Weapon, Weapon360Damage
from ui import UI
from enemy import Enemy
from collectables import*
from particles import CollectParticle, GemCollectAnimation, DeathParticle, EnemyDeathAnimation
from settings_manager import SettingsManager

class Level2:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()


        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.next_sprites = pygame.sprite.Group()
        self.health_orbs = pygame.sprite.Group()
        self.attack_orbs = pygame.sprite.Group()
        self.speed_orbs = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()
        self.ui.current_level = 2
        self.completed = False
        self.gameover = False
        
        # Settings manager for in-game menu
        self.settings = SettingsManager()
        # level music
        # collectable music
        self.collectable_music = pygame.mixer.Sound('../audio/heal.wav')
        self.collectable_music_channel = pygame.mixer.Channel(1)

    def reset(self):
        # Reset level-specific variables and clear sprites
        self.gameover = False
        self.completed = False
        self.visible_sprites.empty()
        self.obstacle_sprites.empty()
        self.next_sprites.empty()
        self.health_orbs.empty()
        self.attack_orbs.empty()
        self.speed_orbs.empty()
        self.create_map()

    def create_map(self):

        layouts = {
            'boundary': import_csv_layout('../map new/maze map_coklision.csv'),
            'next': import_csv_layout('../map new/maze map_Tile Layer end.csv'),
            'player': import_csv_layout('../map new/maze map_playerLevel2.csv'),
            'enemy': import_csv_layout('../map new/maze map_goluLevel2.csv'),
            'extra_enemies': import_csv_layout('../map new/maze map_test player.csv'),  # Mais inimigos
            'health': import_csv_layout('../map new/maze map_health(level2).csv'),
            'attack': import_csv_layout('../map new/maze map_attackLevel2.csv'),
            'speed': import_csv_layout('../map new/maze map_speed(level2).csv'),

        }
        graphics = {
            'grass': import_folder('../graphics/grass'),
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        if style == 'next':
                            Tile((x, y), [self.next_sprites], 'invisible')
                        if style == 'player':
                            self.player = Player(
                                    (x-80, y-5),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic)
                        if style == "enemy":
                            Enemy('golu',(x, y),[self.visible_sprites, self.attackable_sprites],self.obstacle_sprites,self.damage_player, visible_sprites=self.visible_sprites)
                        if style == "extra_enemies":
                            extra_enemy = Enemy('bigboi',(x, y),[self.visible_sprites, self.attackable_sprites],self.obstacle_sprites,self.damage_player,2, visible_sprites=self.visible_sprites)
                            extra_enemy.animation_speed = 0.05  # Mini-bosses no labirinto
                        if style =="health":
                            HealthOrbs((x, y), [self.health_orbs, self.visible_sprites])
                        if style == "attack":
                            AttackOrbs((x, y), [self.attack_orbs, self.visible_sprites])
                        if style =="speed":
                            SpeedOrbs((x, y), [self.speed_orbs, self.visible_sprites])
                        # if style =="particles":
                        #     Leaves((x,y), self.visible_sprites)


    def create_attack(self):
        # Create original visual weapon (shows in direction player is facing)
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])
        
        # Add invisible 360-degree damage area
        self.damage_area = Weapon360Damage(self.player, [self.attack_sprites])

    def create_magic(self, style, strength, cost):
        pass

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
        # spawn particles

    def run(self):
        # Handle settings events (only process settings-related events)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # Only handle settings keys, let player handle movement
                if event.key in [pygame.K_m, pygame.K_UP, pygame.K_DOWN, pygame.K_ESCAPE]:
                    self.settings.handle_keydown(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Handle settings mouse clicks
                consumed = self.settings.handle_mouse_click(pygame.mouse.get_pos())
                # If click wasn't consumed by settings, let game handle it
        
        # Only update game if settings menu is closed (pause when open)
        if not self.settings.is_menu_open():
            # update and draw the game
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()
        
        # Always draw (but don't update when paused)
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)
        
        # Draw settings button and menu
        self.settings.draw(pygame.display.get_surface())
        if pygame.sprite.spritecollide(self.player, self.next_sprites, False):
            self.completed = True
        if self.player.health <= 0:
            print('game over')
            self.gameover = True
        if pygame.sprite.spritecollide(self.player, self.health_orbs, True):
            self.player.inventory["healthOrbs"] += 1
            self.collectable_music_channel.play(self.collectable_music)
            self.ui.set_status_message('Vida Aumentada')
            if self.player.health < 450:
                self.player.health += 50
            else:
                self.player.health = 500

        if pygame.sprite.spritecollide(self.player, self.speed_orbs, True):
            self.player.inventory["speedOrbs"] += 1
            self.collectable_music_channel.play(self.collectable_music)
            self.ui.set_status_message('Velocidade Aumentada')
            self.player.speed += 0.4
            self.player.animation_speed += 0.04

        if pygame.sprite.spritecollide(self.player, self.attack_orbs, True):
            self.player.inventory["attackOrbs"] += 1
            self.collectable_music_channel.play(self.collectable_music)
            self.ui.set_status_message('Ataque Aumentado')
            self.player.attack += 10



class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surf = pygame.image.load('../map new/maze1.png').convert()
        self.floor_surf = pygame.transform.scale2x(self.floor_surf)
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))
        self.floor_surf2 = pygame.image.load('../map new/maze2.png').convert_alpha()
        self.floor_surf2 = pygame.transform.scale2x(self.floor_surf2)
        self.floor_rect2 = self.floor_surf2.get_rect(topleft=(0, 0))

    def custom_draw(self, player):

        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
            
            # Draw health bar for enemies with camera offset
            if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy':
                self.draw_enemy_health_bar(sprite)

        # drawing the floor
        floor_offset_pos2 = self.floor_rect2.topleft - self.offset
        self.display_surface.blit(self.floor_surf2, floor_offset_pos2)

    def draw_enemy_health_bar(self, enemy):
        """Draw health bar above enemy with camera offset"""
        if enemy.show_health_bar and enemy.health > 0:
            # Calculate health bar position with camera offset
            bar_x = enemy.rect.centerx - enemy.health_bar_width // 2 - self.offset.x
            bar_y = enemy.rect.top + enemy.health_bar_offset_y - self.offset.y
            
            # Calculate health percentage
            health_percentage = enemy.health / enemy.max_health
            current_width = int(enemy.health_bar_width * health_percentage)
            
            # Background (dark red)
            bg_rect = pygame.Rect(bar_x, bar_y, enemy.health_bar_width, enemy.health_bar_height)
            pygame.draw.rect(self.display_surface, (60, 20, 20), bg_rect)
            
            # Health bar (green to red based on health)
            if health_percentage > 0:
                # Color transitions from green to red
                if health_percentage > 0.6:
                    color = (0, 200, 0)  # Green
                elif health_percentage > 0.3:
                    color = (255, 200, 0)  # Yellow
                else:
                    color = (255, 50, 50)  # Red
                
                health_rect = pygame.Rect(bar_x, bar_y, current_width, enemy.health_bar_height)
                pygame.draw.rect(self.display_surface, color, health_rect)
            
            # Border
            pygame.draw.rect(self.display_surface, (200, 200, 200), bg_rect, 1)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if
                         hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
