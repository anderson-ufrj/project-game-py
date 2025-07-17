import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice
from weapon import Weapon, Weapon360Damage, Magic
from ui import UI
from enemy import Enemy
from collectables import*
from particles import CollectParticle, GemCollectAnimation, DeathParticle, EnemyDeathAnimation, FloatingText
# from settings_manager import SettingsManager  # REMOVED (using modern_audio_controls instead)
# CHEAT: Import cheat system for testing (remove for final version)
from cheat_system import cheat_system
# STATS: Import player statistics system
from player_stats import player_stats
from font_manager import font_manager
from professional_renderer import professional_renderer
from audio_manager import audio_manager

class Level3:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()


        # get the display surface
        self.display_surface = pygame.display.get_surface()
        
        # STATS: Initialize level statistics
        player_stats.start_level(3)

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
        
        # magic sprites
        self.magic_sprites = pygame.sprite.Group()
        
        # animation sprites
        self.floating_text_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()
        self.ui.current_level = 3
        self.gameover = False
        
        # settings manager - REMOVED (using modern_audio_controls instead)
        # self.settings = SettingsManager()
        
        # Minimap with modern font system
        self.show_minimap = False
        # Use font manager for consistent minimap text
        
        # Audio now handled by AudioManager - sounds removed
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
        self.magic_sprites.empty()
        self.floating_text_sprites.empty()
        self.create_map()
    def create_map(self):

        layouts = {
            'boundary': import_csv_layout('../map new/dungeon_collision.csv'),
            'player': import_csv_layout('../map new/dungeon_PLayer.csv'),
            'enemy': import_csv_layout('../map new/dungeon_dungeon bigboi.csv'),
            'black_enemy': import_csv_layout('../map new/dungeon_big boys .csv'),  # Inimigos black adicionais
            'health': import_csv_layout('../map new/dungeon_health.csv'),
            'speed': import_csv_layout('../map new/dungeon_spped.csv'),  # Corrigido o nome do arquivo
            'extra_speed': import_csv_layout('../map new/dungeon_spped.csv'),  # Duplicar speed orbs
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
                            enemy = Enemy('bigboi',(x, y),[self.visible_sprites, self.attackable_sprites],self.obstacle_sprites,self.damage_player,2, visible_sprites=self.visible_sprites)
                            enemy.animation_speed = 0.04
                        if style == "black_enemy":
                            black_enemy = Enemy('black',(x, y),[self.visible_sprites, self.attackable_sprites],self.obstacle_sprites,self.damage_player,1, visible_sprites=self.visible_sprites)
                            black_enemy.animation_speed = 0.06
                        if style =="health":
                            HealthOrbs((x, y), [self.health_orbs, self.visible_sprites])
                        if style == "attack":
                            AttackOrbs((x, y), [self.attack_orbs, self.visible_sprites])
                        if style =="speed":
                            SpeedOrbs((x, y), [self.speed_orbs, self.visible_sprites])
                        if style =="extra_speed":
                            # Adicionar speed orbs extras com pequeno offset
                            SpeedOrbs((x + 16, y + 16), [self.speed_orbs, self.visible_sprites])
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
        if self.player.energy >= cost:
            self.player.energy -= cost
            magic_sprite = Magic(self.player, [self.visible_sprites, self.magic_sprites, self.attack_sprites], style, strength, cost)
            print(f"Magia {style} usada! Energia restante: {self.player.energy}")

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                # Only process actual weapons and magic projectiles, not effects
                if hasattr(attack_sprite, 'sprite_type') and attack_sprite.sprite_type in ['weapon', 'magic']:
                    collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                    if collision_sprites:
                        for target_sprite in collision_sprites:
                            if target_sprite.sprite_type == 'grass':
                                target_sprite.kill()
                            elif attack_sprite.sprite_type == 'magic':
                                # Handle magic projectile collision
                                self.handle_magic_collision(attack_sprite, target_sprite)
                            else:
                                target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def handle_magic_collision(self, magic_projectile, target):
        """Handle collision between magic projectile and target"""
        if magic_projectile.style == 'flame':
            # Apply fire effect
            target.apply_fire_effect(magic_projectile.strength)
        elif magic_projectile.style == 'heal':
            # Water/ice magic slows enemies
            target.apply_water_effect(0.3)  # Slow to 30% speed
        
        # Apply projectile effect and remove it
        magic_projectile.apply_effect_on_hit(target)
        magic_projectile.kill()

    def damage_player(self, amount, attack_type):
        # CHEAT: Check god mode (remove for final version)
        if cheat_system.god_mode:
            return  # No damage in god mode
        
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
        # spawn particles

    def draw_minimap(self, surface):
        """Draw a helpful minimap showing keys and exit locations with modern rendering"""
        # Minimap background with modern panel
        map_width, map_height = 200, 150
        map_x, map_y = 20, 20
        
        # Create modern minimap panel
        minimap_panel = professional_renderer.create_modern_panel(
            map_width, map_height, 
            title="MAPA - FORTALEZA SOMBRIA",
            background_alpha=220
        )
        surface.blit(minimap_panel, (map_x, map_y))
        
        # Level 3 map info with modern rendering
        info_y = map_y + 50  # Account for title space
        
        # Player position indicator
        player_surface, player_rect = professional_renderer.render_text_professional(
            "🔴 Você está aqui", 'small', (255, 100, 100), 
            shadow=True, anti_alias=True
        )
        surface.blit(player_surface, (map_x + 5, info_y))
        info_y += 15
        
        # Keys info
        keys_collected = self.player.inventory.get('keys', 0)
        keys_surface, keys_rect = professional_renderer.render_text_professional(
            f"🔑 Chaves: {keys_collected}/4", 'small', (255, 255, 100),
            shadow=True, anti_alias=True
        )
        surface.blit(keys_surface, (map_x + 5, info_y))
        info_y += 15
        
        # Key locations hint with modern rendering
        if keys_collected < 4:
            hint1_surface, _ = professional_renderer.render_text_professional(
                "Locais das chaves:", 'small', (200, 200, 200),
                shadow=True, anti_alias=True
            )
            surface.blit(hint1_surface, (map_x + 5, info_y))
            info_y += 12
            
            for hint_text in [
                "• Norte: Sala dos Cristais",
                "• Sul: Calabouço Sombrio", 
                "• Leste: Torre do Bigboi",
                "• Oeste: Câmara Secreta"
            ]:
                hint_surface, _ = professional_renderer.render_text_professional(
                    hint_text, 'small', (150, 255, 150),
                    shadow=True, anti_alias=True
                )
                surface.blit(hint_surface, (map_x + 10, info_y))
                info_y += 12
            info_y += 3  # Extra spacing
        
        # Exit info with modern rendering
        if keys_collected >= 4:
            exit_surface, _ = professional_renderer.render_text_professional(
                "🚪 Saída desbloqueada!", 'small', (100, 255, 100),
                shadow=True, glow=True, anti_alias=True
            )
            surface.blit(exit_surface, (map_x + 5, info_y))
            info_y += 12
            
            hint_surface, _ = professional_renderer.render_text_professional(
                "Vá para o centro!", 'small', (100, 255, 100),
                shadow=True, anti_alias=True
            )
            surface.blit(hint_surface, (map_x + 5, info_y))
        else:
            exit_surface, _ = professional_renderer.render_text_professional(
                "🚪 Colete 4 chaves para sair", 'small', (255, 150, 150),
                shadow=True, anti_alias=True
            )
            surface.blit(exit_surface, (map_x + 5, info_y))
        
        # Controls with modern rendering
        controls_y = map_y + map_height - 25
        control_surface, _ = professional_renderer.render_text_professional(
            "TAB: Fechar mapa", 'small', (180, 180, 180),
            shadow=True, anti_alias=True
        )
        surface.blit(control_surface, (map_x + 5, controls_y))

    def run(self):
        # Handle settings events (only process settings-related events)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # Only handle settings keys, let player handle movement
                if event.key in [pygame.K_m, pygame.K_UP, pygame.K_DOWN, pygame.K_ESCAPE]:
                    # self.settings.handle_keydown(event)  # REMOVED
                    pass
                elif event.key == pygame.K_TAB:
                    # Toggle minimap
                    self.show_minimap = not self.show_minimap
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Handle settings mouse clicks
                # consumed = self.settings.handle_mouse_click(pygame.mouse.get_pos())  # REMOVED
                # If click wasn't consumed by settings, let game handle it
                pass
        
        # Only update game if settings menu is closed (pause when open)
        # if not self.settings.is_menu_open():  # REMOVED
        if True:  # Always run game update
            # CHEAT: Apply cheat effects (remove for final version)
            cheat_system.apply_god_mode(self.player)
            cheat_system.apply_max_energy(self.player)
            
            # update and draw the game
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()
            self.magic_sprites.update()  # Update magic sprites
            self.floating_text_sprites.update()  # Atualizar textos flutuantes
        
        # Always draw (but don't update when paused)
        self.visible_sprites.custom_draw(self.player)
        
        # Desenhar textos flutuantes por cima de tudo com offset da câmera
        for text in self.floating_text_sprites:
            # Aplicar offset da câmera
            screen_pos = text.rect.topleft - self.visible_sprites.offset
            pygame.display.get_surface().blit(text.image, screen_pos)
        
        self.ui.display(self.player)
        
        # CHEAT: Display cheat information (remove for final version)
        cheat_system.display_cheat_info(pygame.display.get_surface())
        
        # Draw settings button and menu
        # self.settings.draw(pygame.display.get_surface())  # REMOVED
        
        # Draw minimap if enabled
        if self.show_minimap:
            self.draw_minimap(pygame.display.get_surface())
        
        # Keep the rest of the original run() method logic after this point
        if pygame.sprite.spritecollide(self.player, self.next_sprites, False):
            self.completed = True
        if self.player.health <= 0:
            print('game over')
            # STATS: Record player death
            player_stats.record_death()
            self.gameover = True
        health_collisions = pygame.sprite.spritecollide(self.player, self.health_orbs, True)
        if health_collisions:
            for orb in health_collisions:
                # Create collection animation
                GemCollectAnimation(orb.rect.center, [self.visible_sprites])
                for _ in range(10):
                    CollectParticle(orb.rect.center, [self.visible_sprites], color=(255, 100, 100))
                
                # Animação de texto flutuante
                FloatingText(orb.rect.center, [self.floating_text_sprites], "+VIDA", color=(255, 100, 100), size=16)
                
                self.player.inventory["healthOrbs"] += 1
                audio_manager.play_sound('heal', 'collection')
                if self.player.health < 450:
                    self.player.health += 50
                else:
                    self.player.health = 500

        speed_collisions = pygame.sprite.spritecollide(self.player, self.speed_orbs, True)
        if speed_collisions:
            for orb in speed_collisions:
                # Create collection animation
                GemCollectAnimation(orb.rect.center, [self.visible_sprites])
                for _ in range(10):
                    CollectParticle(orb.rect.center, [self.visible_sprites], color=(100, 100, 255))
                
                # Animação de texto flutuante
                FloatingText(orb.rect.center, [self.floating_text_sprites], "+VELOCIDADE", color=(100, 255, 100), size=16)
                
                self.player.inventory["speedOrbs"] += 1
                audio_manager.play_sound('heal', 'collection')
                self.player.speed += 0.4
                self.player.animation_speed += 0.04

        gem_collisions = pygame.sprite.spritecollide(self.player, self.gem, True)
        if gem_collisions:
            for gem in gem_collisions:
                # Create collection animation
                GemCollectAnimation(gem.rect.center, [self.visible_sprites])
                for _ in range(20):
                    CollectParticle(gem.rect.center, [self.visible_sprites], color=(220, 180, 255))
                
                # Animação de texto flutuante especial para a pedra
                FloatingText(gem.rect.center, [self.floating_text_sprites], "PEDRA MÍSTICA!", color=(220, 180, 255), size=24)
                
                self.player.inventory['zappaguriStone'] = 1
                audio_manager.play_sound('heal', 'collection')

        attack_collisions = pygame.sprite.spritecollide(self.player, self.attack_orbs, True)
        if attack_collisions:
            for orb in attack_collisions:
                # Create collection animation
                GemCollectAnimation(orb.rect.center, [self.visible_sprites])
                for _ in range(10):
                    CollectParticle(orb.rect.center, [self.visible_sprites], color=(255, 200, 100))
                
                # Animação de texto flutuante
                FloatingText(orb.rect.center, [self.floating_text_sprites], "+ATAQUE", color=(255, 200, 100), size=16)
                
                self.player.inventory["attackOrbs"] += 1
                audio_manager.play_sound('heal', 'collection')
                self.player.attack += 10


        key_collisions = pygame.sprite.spritecollide(self.player, self.key, True)
        if key_collisions:
            for key in key_collisions:
                # Create collection animation
                GemCollectAnimation(key.rect.center, [self.visible_sprites])
                for _ in range(10):
                    CollectParticle(key.rect.center, [self.visible_sprites], color=(255, 215, 0))
                
                # Animação de texto flutuante
                FloatingText(key.rect.center, [self.floating_text_sprites], "+CHAVE", color=(255, 215, 0), size=18)
                
                self.player.inventory["keys"] += 1
                audio_manager.play_sound('heal', 'collection')
        if self.player.inventory['keys']<4:
            if pygame.sprite.spritecollide(self.player,self.door, False):
                self.ui.set_status_message('Você precisa de 4 chaves para abrir esta porta!')
        else:
            if pygame.sprite.spritecollide(self.player,self.door, True):
                self.ui.set_status_message('Porta Aberta!')

        if self.player.inventory['zappaguriStone']==1:
            print('Pedra Mística do Zappaguri coletada!')
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
