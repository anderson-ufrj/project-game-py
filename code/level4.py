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

class Level4:
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

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.bosssprites = pygame.sprite.Group()
        
        # magic sprites
        self.magic_sprites = pygame.sprite.Group()
        
        # animation sprites
        self.floating_text_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()
        self.ui.current_level = 4
        self.completed = False
        self.gameover = False
        
        # settings manager
        self.settings = SettingsManager()
        # level music
        # collectable music
        self.collectable_music = pygame.mixer.Sound('../audio/heal.wav')
        self.collectable_music_channel = pygame.mixer.Channel(1)
        self.stomp_music = pygame.mixer.Sound('../audio/stomp.wav')
        self.stomp_music_channel = pygame.mixer.Channel(3)

    def create_map(self):

        layouts = {
            'boundary': import_csv_layout('../map new/last level_collision last level.csv'),
            'player': import_csv_layout('../map new/last level_player spwan.csv'),
            'health': import_csv_layout('../map new/last level_health.csv'),
            'speed': import_csv_layout('../map new/last level_speed.csv'),
            'extra_speed': import_csv_layout('../map new/latest_final_speed.csv'),  # Mais speed orbs
            'attack':import_csv_layout('../map new/last level_attac.csv'),
            'enemy':import_csv_layout('../map new/last level_golu.csv'),
            'big_enemies': import_csv_layout('../map new/latest_final_big boys.csv'),  # Inimigos bigboi extras
            'monster_spawn': import_csv_layout('../map new/latest_final_main monster spwam.csv'),  # Mais monstros
            'next' : import_csv_layout('../map new/last level_end.csv')
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
                            self.boss = Boss((x+500, y-30),[self.bosssprites, self.visible_sprites])
                        if style == "enemy":
                            enemy = Enemy('golu',(x, y),[self.visible_sprites, self.attackable_sprites],self.obstacle_sprites,self.damage_player, visible_sprites=self.visible_sprites)
                        if style == "big_enemies":
                            big_enemy = Enemy('bigboi',(x, y),[self.visible_sprites, self.attackable_sprites],self.obstacle_sprites,self.damage_player,3, visible_sprites=self.visible_sprites)
                            big_enemy.animation_speed = 0.03
                        if style == "monster_spawn":
                            monster = Enemy('black',(x, y),[self.visible_sprites, self.attackable_sprites],self.obstacle_sprites,self.damage_player,1, visible_sprites=self.visible_sprites)
                            monster.animation_speed = 0.08
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
                        if style == 'next':
                            Tile((x, y), [self.next_sprites],"invisible")





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
        
        # Keep the rest of the original run() method logic after this point
        if pygame.sprite.spritecollide(self.player, self.next_sprites, False):
            self.completed = True
            self.ui.set_status_message('VOCÊ VENCEU')
        if self.player.health <= 0:
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
        if self.player.rect.colliderect(self.boss.hitbox):
            self.player.health = -10







class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surf = pygame.image.load('../map new/last level.png').convert()
        self.floor_surf = pygame.transform.scale2x(self.floor_surf)
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))
        self.vignette_radius = 1000

        self.floor_surf2 = pygame.image.load('../map new/last level1.png').convert_alpha()
        self.floor_surf2 = pygame.transform.scale2x(self.floor_surf2)
        self.floor_rect2 = self.floor_surf2.get_rect(topleft=(0, 0))

    def custom_draw(self, player):

        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)


        floor_offset_pos2 = self.floor_rect2.topleft - self.offset
        self.display_surface.blit(self.floor_surf2, floor_offset_pos2)

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)





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

class Boss(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        self.frames = import_folder('../graphics/monsters/black/left')
        self.frame_index = 0
        self.animation_speed = 0.09

        self.image = self.frames[self.frame_index]
        self.image = pygame.transform.scale2x(self.image)  # Apenas um scale2x
        self.rect = self.image.get_rect(center=pos)

        self.hitbox = self.rect.inflate(-self.rect.width + 50,-self.rect.height + 50)  # Hitbox ajustado para o novo tamanho
        #self.rect = self.rect.inflate(-60, -500)


    def animate(self):
        animation = self.frames

            # Loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

            # Set the image
        self.image = animation[int(self.frame_index)]
        self.image = pygame.transform.scale2x(self.image)  # Apenas um scale2x
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def move(self, speed):
        self.rect.x -= speed
        self.hitbox.center = self.rect.center

    def update(self):
        self.animate()
        self.move(3)

