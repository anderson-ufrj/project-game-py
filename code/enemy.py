import pygame
from settings import *
from entity import Entity
from support import *
from particles import DeathParticle, EnemyDeathAnimation
# STATS: Import player statistics system
from player_stats import player_stats
from difficulty_manager import difficulty_manager


class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player, level=1, visible_sprites=None):
        self.movestatus = False

        # general setup
        super().__init__(groups)
        self.visible_sprites = visible_sprites  # For death animation
        # self.animations = None
        self.sprite_type = 'enemy'
        self.monster_level = level
        # graphics setup
        self.import_graphics(monster_name)
        self.status = 'down_idle'
        # self.image = self.animations[self.status][self.frame_index]
        self.image = self.animations[self.status][self.frame_index]

        # stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        # movement
        self.image = pygame.transform.scale2x(self.image)
        if self.monster_level == 2:
            self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-100, -52)
        self.obstacle_sprites = obstacle_sprites

        # stats (apply difficulty modifiers)
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        
        # Base stats
        base_health = monster_info['health']
        base_damage = monster_info['damage']
        base_speed = monster_info['speed']
        
        # Apply difficulty modifiers
        modified_health, modified_damage, modified_speed = difficulty_manager.apply_to_enemy_stats(
            base_health, base_damage, base_speed
        )
        
        self.health = modified_health
        self.max_health = modified_health  # Store max health for health bar calculation
        self.exp = monster_info['exp']
        self.speed = modified_speed
        self.attack_damage = modified_damage
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player
        self.monsta = pygame.mixer.Sound('../audio/heal.wav')
        self.monsta_channel = pygame.mixer.Channel(1)

        # invincibility timer
        self.vulnerable = True
        self.hit_time = 200
        self.invincibility_duration = 300
        
        # Health bar properties
        self.health_bar_width = 60
        self.health_bar_height = 8
        self.health_bar_offset_y = -20  # Above the monster
        self.show_health_bar = True
        
        # Magic effects
        self.fire_effect = False
        self.fire_effect_time = 0
        self.fire_effect_duration = 3000  # 3 seconds
        self.fire_damage_interval = 500   # Damage every 0.5 seconds
        self.last_fire_damage = 0
        
        self.water_effect = False
        self.water_effect_time = 0  
        self.water_effect_duration = 2000  # 2 seconds
        self.original_speed = self.speed

    def import_graphics(self, name):
        character_path = f'../graphics/monsters/{name}/'
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)


    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]
        direcshun = self.get_player_distance_direction(player)[1]

        if distance >= self.notice_radius:
            self.movestatus = False
        else:
            self.movestatus = True
        if self.movestatus:
            if direcshun.x > 0 and abs(direcshun.y) < abs(direcshun.x):
                self.status = 'right'
            elif direcshun.x < 0 and abs(direcshun.y) < abs(direcshun.x):
                self.status = 'left'
            elif direcshun.y > 0 and abs(direcshun.x) < abs(direcshun.y):
                self.status = 'down'
            elif direcshun.y < 0 and abs(direcshun.x) < abs(direcshun.y):
                self.status = 'up'
            if distance <= self.attack_radius and self.can_attack:
                if 'attack' not in self.status:
                    if 'idle' in self.status:
                        self.status = self.status.replace('_idle', '_attack')
                    else:
                        self.status = self.status + '_attack'
                        # self.frame_index = 0
                elif 'attack' in self.status:
                    self.status = self.status.replace('_attack', '')
            # elif distance <= self.notice_radius:
            #   self.status = 'move'
            else:

                if direcshun.x > 0 and abs(direcshun.y) < abs(direcshun.x):
                    self.status = 'right'
                elif direcshun.x < 0 and abs(direcshun.y) < abs(direcshun.x):
                    self.status = 'left'
                elif direcshun.y > 0 and abs(direcshun.x) < abs(direcshun.y):
                    self.status = 'down'
                elif direcshun.y < 0 and abs(direcshun.x) < abs(direcshun.y):
                    self.status = 'up'
                elif 'idle' not in self.status and 'attack' not in self.status:
                    self.status = self.status + '_idle'
        else:
            self.status = 'down_idle'

    def actions(self, player):
        if 'attack' in self.status:
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage, self.attack_type)
        elif 'idle' not in self.status and self.movestatus:
            self.get_status(player)
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()


    def animate(self):
        if self.monster_name == "black":
            self.animation_speed = 0.1
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if 'attack' in self.status:
                self.can_attack = True
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        if self.monster_name == "golu":
            self.image = pygame.transform.scale2x(self.image)
        elif self.monster_name == 'black':
            self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect(center=self.hitbox.center)


        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
            else:
                self.vulnerable = False

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True
            else:
                self.vulnerable = False

    def get_damage(self, player, attack_type):
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == 'weapon':
                damage = player.get_full_weapon_damage()
                self.health -= damage
                # STATS: Record damage dealt
                player_stats.record_damage_dealt(damage)
            else:
                pass
            # magic damage
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def draw_health_bar(self, surface):
        """Draw health bar above the monster"""
        if self.show_health_bar and self.health > 0:
            # Calculate health bar position
            bar_x = self.rect.centerx - self.health_bar_width // 2
            bar_y = self.rect.top + self.health_bar_offset_y
            
            # Calculate health percentage
            health_percentage = self.health / self.max_health
            current_width = int(self.health_bar_width * health_percentage)
            
            # Background (dark red)
            bg_rect = pygame.Rect(bar_x, bar_y, self.health_bar_width, self.health_bar_height)
            pygame.draw.rect(surface, (60, 20, 20), bg_rect)
            
            # Health bar (green to red based on health)
            if health_percentage > 0:
                # Color transitions from green to red
                if health_percentage > 0.6:
                    color = (0, 200, 0)  # Green
                elif health_percentage > 0.3:
                    color = (255, 200, 0)  # Yellow
                else:
                    color = (255, 50, 50)  # Red
                
                health_rect = pygame.Rect(bar_x, bar_y, current_width, self.health_bar_height)
                pygame.draw.rect(surface, color, health_rect)
            
            # Border
            pygame.draw.rect(surface, (200, 200, 200), bg_rect, 1)

    def check_death(self):
        if self.health <= 0:
            # STATS: Record enemy kill
            player_stats.record_enemy_kill(self.monster_name)
            
            # Create death animation if visible_sprites is available
            if self.visible_sprites:
                # Create explosion effect
                EnemyDeathAnimation(self.rect.center, [self.visible_sprites], self.rect.width)
                
                # Create multiple death particles
                for _ in range(20):
                    DeathParticle(self.rect.center, [self.visible_sprites])
            
            self.kill()

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance
            #self.vulnerable = False

    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.cooldowns()
        self.check_death()
        if self.movestatus:
            self.animate()
    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.update_magic_effects()  # Update magic effects
        self.check_death()
    
    
    def apply_fire_effect(self, damage):
        """Apply fire effect to enemy"""
        print(f"🔥 {self.monster_name} pegou fogo!")
        self.fire_effect = True
        self.fire_effect_time = pygame.time.get_ticks()
        self.fire_damage = damage // 3  # Fire does damage over time
        self.last_fire_damage = pygame.time.get_ticks()
    
    def apply_water_effect(self, slow_amount=0.5):
        """Apply water/ice effect to enemy (slows down)"""
        print(f"❄️ {self.monster_name} foi congelado!")
        self.water_effect = True
        self.water_effect_time = pygame.time.get_ticks()
        self.speed = self.original_speed * slow_amount  # Slow down
    
    def update_magic_effects(self):
        """Update ongoing magic effects"""
        current_time = pygame.time.get_ticks()
        
        # Fire effect - continuous damage
        if self.fire_effect:
            if current_time - self.fire_effect_time > self.fire_effect_duration:
                self.fire_effect = False
                print(f"🔥 {self.monster_name} parou de queimar")
            else:
                # Apply fire damage periodically
                if current_time - self.last_fire_damage > self.fire_damage_interval:
                    self.health -= self.fire_damage
                    self.last_fire_damage = current_time
                    print(f"🔥 {self.monster_name} queimando! Vida: {self.health}")
                    
                    # Create fire particles
                    if self.visible_sprites:
                        from particles import FireParticle
                        try:
                            FireParticle(self.rect.center, [self.visible_sprites])
                        except:
                            pass
        
        # Water/ice effect - slow movement
        if self.water_effect:
            if current_time - self.water_effect_time > self.water_effect_duration:
                self.water_effect = False
                self.speed = self.original_speed  # Restore original speed
                print(f"❄️ {self.monster_name} saiu do gelo")
            else:
                # Create ice particles
                if self.visible_sprites:
                    from particles import IceParticle
                    try:
                        IceParticle(self.rect.center, [self.visible_sprites])
                    except:
                        pass
    
    def draw_magic_effects(self, surface, offset):
        """Draw visual indicators for magic effects"""
        if self.fire_effect:
            # Draw fire effect overlay
            fire_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            fire_surface.fill((255, 100, 0, 100))  # Semi-transparent red
            screen_pos = self.rect.topleft - offset
            surface.blit(fire_surface, screen_pos)
            
        if self.water_effect:
            # Draw ice effect overlay
            ice_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            ice_surface.fill((100, 200, 255, 100))  # Semi-transparent blue
            screen_pos = self.rect.topleft - offset
            surface.blit(ice_surface, screen_pos)
