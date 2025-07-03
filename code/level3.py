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

class Level3:
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
        self.gem = pygame.sprite.Group()
        self.door = pygame.sprite.Group()
        self.key = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()
        self.ui.current_level = 3
        self.gameover = False
        
        # settings manager
        self.settings = SettingsManager()
        
        # Minimap
        self.show_minimap = False
        try:
            self.minimap_font = pygame.font.Font('../graphics/font/PressStart2P.ttf', 8)
        except:
            self.minimap_font = pygame.font.Font(None, 12)
        
        # level music
        # collectable music
        self.collectable_music = pygame.mixer.Sound('../audio/heal.wav')
        self.collectable_music_channel = pygame.mixer.Channel(1)
        self.completed = False

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
            'boundary': import_csv_layout('../map new/dungeon_collision.csv'),
            'player': import_csv_layout('../map new/dungeon_PLayer.csv'),
            'enemy': import_csv_layout('../map new/dungeon_dungeon bigboi.csv'),
            'health': import_csv_layout('../map new/dungeon_health.csv'),
            'speed': import_csv_layout('../map new/dungeon_health.csv'),
            'gem': import_csv_layout('../map new/dungeon_eldritchGem.csv'),
            'door': import_csv_layout('../map new/dungeon_door message.csv'),
            'keys': import_csv_layout('../map new/dungeon_key.csv')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        if style == 'player':
                            self.player = Player(
                                    (x-80, y-5),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic)
                        if style == "enemy":
                            self.enemy = Enemy('bigboi',(x, y),[self.visible_sprites, self.attackable_sprites],self.obstacle_sprites,self.damage_player,2, visible_sprites=self.visible_sprites)
                            self.enemy.animation_speed = 0.04
                        if style =="health":
                            HealthOrbs((x, y), [self.health_orbs, self.visible_sprites])
                        if style == "attack":
                            AttackOrbs((x, y), [self.attack_orbs, self.visible_sprites])
                        if style =="speed":
                            SpeedOrbs((x, y), [self.speed_orbs, self.visible_sprites])
                        if style == "gem":
                            EldritchGem((x,y),[self.gem,self.visible_sprites])
                        if style == 'door':
                            Tile((x, y),[self.door, self.obstacle_sprites],'invisible')
                        if style == 'keys':
                            Key((x, y), [self.key, self.visible_sprites])


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

    def draw_minimap(self, surface):
        """Draw a helpful minimap showing keys and exit locations"""
        # Minimap background
        map_width, map_height = 200, 150
        map_x, map_y = 20, 20
        
        # Semi-transparent background
        minimap_surface = pygame.Surface((map_width, map_height))
        minimap_surface.set_alpha(220)
        minimap_surface.fill((30, 30, 30))
        surface.blit(minimap_surface, (map_x, map_y))
        
        # Border
        pygame.draw.rect(surface, (150, 150, 150), (map_x, map_y, map_width, map_height), 2)
        
        # Title
        title = self.minimap_font.render("MAPA - FORTALEZA SOMBRIA", True, (255, 255, 100))
        surface.blit(title, (map_x + 5, map_y + 5))
        
        # Level 3 map info (approximate layout)
        info_y = map_y + 25
        
        # Player position indicator
        player_info = self.minimap_font.render("🔴 Você está aqui", True, (255, 100, 100))
        surface.blit(player_info, (map_x + 5, info_y))
        info_y += 15
        
        # Keys info
        keys_collected = self.player.inventory.get('keys', 0)
        keys_info = self.minimap_font.render(f"🔑 Chaves: {keys_collected}/3", True, (255, 255, 100))
        surface.blit(keys_info, (map_x + 5, info_y))
        info_y += 15
        
        # Key locations hint
        if keys_collected < 3:
            hint1 = self.minimap_font.render("Locais das chaves:", True, (200, 200, 200))
            surface.blit(hint1, (map_x + 5, info_y))
            info_y += 12
            
            hint2 = self.minimap_font.render("• Norte: Sala dos Cristais", True, (150, 255, 150))
            surface.blit(hint2, (map_x + 10, info_y))
            info_y += 12
            
            hint3 = self.minimap_font.render("• Sul: Calabouço Sombrio", True, (150, 255, 150))
            surface.blit(hint3, (map_x + 10, info_y))
            info_y += 12
            
            hint4 = self.minimap_font.render("• Leste: Torre do Bigboi", True, (150, 255, 150))
            surface.blit(hint4, (map_x + 10, info_y))
            info_y += 15
        
        # Exit info
        if keys_collected >= 3:
            exit_info = self.minimap_font.render("🚪 Saída desbloqueada!", True, (100, 255, 100))
            surface.blit(exit_info, (map_x + 5, info_y))
            info_y += 12
            exit_hint = self.minimap_font.render("Vá para o centro!", True, (100, 255, 100))
            surface.blit(exit_hint, (map_x + 5, info_y))
        else:
            exit_info = self.minimap_font.render("🚪 Colete 3 chaves para sair", True, (255, 150, 150))
            surface.blit(exit_info, (map_x + 5, info_y))
        
        # Controls
        controls_y = map_y + map_height - 25
        control_text = self.minimap_font.render("TAB: Fechar mapa", True, (180, 180, 180))
        surface.blit(control_text, (map_x + 5, controls_y))

    def run(self):
        # Handle settings events (only process settings-related events)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # Only handle settings keys, let player handle movement
                if event.key in [pygame.K_m, pygame.K_UP, pygame.K_DOWN, pygame.K_ESCAPE]:
                    self.settings.handle_keydown(event)
                elif event.key == pygame.K_TAB:
                    # Toggle minimap
                    self.show_minimap = not self.show_minimap
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
        
        # Draw minimap if enabled
        if self.show_minimap:
            self.draw_minimap(pygame.display.get_surface())
        
        # Keep the rest of the original run() method logic after this point
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

        if pygame.sprite.spritecollide(self.player, self.gem, True):

            self.player.inventory['megaGem'] = 1

        if pygame.sprite.spritecollide(self.player, self.attack_orbs, True):
            self.player.inventory["attackOrbs"] += 1
            self.collectable_music_channel.play(self.collectable_music)
            self.ui.set_status_message('Ataque Aumentado')
            self.player.attack += 10


        if pygame.sprite.spritecollide(self.player, self.key, True):
            self.player.inventory["keys"] += 1
            self.collectable_music_channel.play(self.collectable_music)
            self.ui.set_status_message('Chave Obtida!')
        if self.player.inventory['keys']<3:
            if pygame.sprite.spritecollide(self.player,self.door, False):
                self.ui.set_status_message('Você precisa de 3 chaves para abrir esta porta!')
        else:
            if pygame.sprite.spritecollide(self.player,self.door, True):
                self.ui.set_status_message('Porta Aberta!')

        if self.player.inventory['megaGem']==1:
            print('level completed')
            self.completed = True


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surf = pygame.image.load('../map new/dungeon ground.png').convert()
        self.floor_surf = pygame.transform.scale2x(self.floor_surf)
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))
        self.floor_surf2 = pygame.image.load('../map new/ala.png').convert_alpha()
        self.floor_surf2 = pygame.transform.scale2x(self.floor_surf2)
        self.floor_rect2 = self.floor_surf2.get_rect(topleft=(0, 0))
        self.vignette_radius = 1000

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

        # drawing the floor
        floor_offset_pos2 = self.floor_rect2.topleft - self.offset
        self.display_surface.blit(self.floor_surf2, floor_offset_pos2)
        self.draw_vignette()


    def draw_vignette(self):
        vignette_surface = pygame.Surface((self.half_width * 2, self.half_height * 2), pygame.SRCALPHA)
        pygame.draw.circle(vignette_surface, (0, 0, 0, 230), (self.half_width, self.half_height), self.vignette_radius)
        pygame.draw.circle(vignette_surface, (0, 0, 0, 200), (self.half_width, self.half_height),self.vignette_radius * 0.2 + 25)
        pygame.draw.circle(vignette_surface, (0, 0, 0, 170), (self.half_width, self.half_height),self.vignette_radius * 0.2 + 20)
        pygame.draw.circle(vignette_surface, (0, 0, 0, 140), (self.half_width, self.half_height),self.vignette_radius * 0.2 + 15)
        pygame.draw.circle(vignette_surface, (0, 0, 0, 110), (self.half_width, self.half_height),self.vignette_radius * 0.2 + 10)
        pygame.draw.circle(vignette_surface, (0, 0, 0, 60), (self.half_width, self.half_height),self.vignette_radius * 0.2 + 5)
        pygame.draw.circle(vignette_surface, (0, 0, 0, 0), (self.half_width, self.half_height),int(self.vignette_radius * 0.2))

        # Blit the vignette surface onto the display surface
        self.display_surface.blit(vignette_surface, (0, 0))
    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if
                         hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
