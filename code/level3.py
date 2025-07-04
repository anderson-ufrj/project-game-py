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
from settings_manager import SettingsManager
# CHEAT: Import cheat system for testing (remove for final version)
from cheat_system import cheat_system

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
        keys_info = self.minimap_font.render(f"🔑 Chaves: {keys_collected}/4", True, (255, 255, 100))
        surface.blit(keys_info, (map_x + 5, info_y))
        info_y += 15
        
        # Key locations hint
        if keys_collected < 4:
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
            info_y += 12
            
            hint5 = self.minimap_font.render("• Oeste: Câmara Secreta", True, (150, 255, 150))
            surface.blit(hint5, (map_x + 10, info_y))
            info_y += 15
        
        # Exit info
        if keys_collected >= 4:
            exit_info = self.minimap_font.render("🚪 Saída desbloqueada!", True, (100, 255, 100))
            surface.blit(exit_info, (map_x + 5, info_y))
            info_y += 12
            exit_hint = self.minimap_font.render("Vá para o centro!", True, (100, 255, 100))
            surface.blit(exit_hint, (map_x + 5, info_y))
        else:
            exit_info = self.minimap_font.render("🚪 Colete 4 chaves para sair", True, (255, 150, 150))
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
                self.collectable_music_channel.play(self.collectable_music)
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
                self.collectable_music_channel.play(self.collectable_music)
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
                self.collectable_music_channel.play(self.collectable_music)

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
                self.collectable_music_channel.play(self.collectable_music)
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
                self.collectable_music_channel.play(self.collectable_music)
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
