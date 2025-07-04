import pygame 
import math
from settings import weapon_data

class Weapon(pygame.sprite.Sprite):
	def __init__(self,player,groups):
		super().__init__(groups)
		self.sprite_type = 'weapon'
		self.player = player
		direction = player.status.split('_')[0]
		self.weapon_type = player.weapon
		
		# Animation properties
		self.animation_frames = 6
		self.current_frame = 0
		self.animation_speed = 0.8
		self.start_time = pygame.time.get_ticks()
		self.duration = 150  # Attack animation duration

		# Load weapon graphic based on type
		try:
			weapon_surf = pygame.image.load(weapon_data[self.weapon_type]['graphic']).convert_alpha()
			# Scale weapon based on type
			if self.weapon_type == 'sword':
				weapon_surf = pygame.transform.scale(weapon_surf, (60, 60))
			elif self.weapon_type == 'lance':
				weapon_surf = pygame.transform.scale(weapon_surf, (80, 20))
			elif self.weapon_type == 'axe':
				weapon_surf = pygame.transform.scale(weapon_surf, (70, 70))
			elif self.weapon_type == 'rapier':
				weapon_surf = pygame.transform.scale(weapon_surf, (50, 15))
			elif self.weapon_type == 'sai':
				weapon_surf = pygame.transform.scale(weapon_surf, (40, 60))
		except:
			# Fallback if image not found
			weapon_surf = pygame.Surface([64,64], pygame.SRCALPHA)
			pygame.draw.rect(weapon_surf, (200, 200, 200), (0, 0, 64, 64))

		self.base_weapon_surf = weapon_surf
		self.direction = direction
		
		# Initialize animation
		self.update_animation()

		weapon_offset_from_player = self.get_weapon_offset()
		# placement based on weapon type and direction
		if direction == 'right':
			self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0,16))
			self.rect.x-= weapon_offset_from_player
		elif direction == 'left': 
			self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0,16))
			self.rect.x+= weapon_offset_from_player
		elif direction == 'down':
			self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10,0))
			self.rect.y-= weapon_offset_from_player
		else:
			self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-10,0))
			self.rect.y+= weapon_offset_from_player
		
		# Add 360-degree damage area (invisible)
		self.attack_radius = 80  # Radius for 360-degree damage
		self.player_center = player.rect.center

	def get_weapon_offset(self):
		"""Get weapon offset based on weapon type"""
		offsets = {
			'sword': 20,
			'lance': 30,
			'axe': 25,
			'rapier': 15,
			'sai': 18
		}
		return offsets.get(self.weapon_type, 20)
	
	def update_animation(self):
		"""Update weapon animation frame"""
		elapsed_time = pygame.time.get_ticks() - self.start_time
		progress = min(elapsed_time / self.duration, 1.0)  # 0.0 to 1.0
		
		# Calculate current frame
		self.current_frame = progress * (self.animation_frames - 1)
		
		# Get animated rotation angle
		angle_offset = self.get_animation_angle_offset(progress)
		
		# Apply rotation with animation
		self.image = self.rotate_weapon_animated(self.base_weapon_surf, self.direction, angle_offset)
	
	def get_animation_angle_offset(self, progress):
		"""Get angle offset based on animation progress and weapon type"""
		if self.weapon_type == 'sword':
			# Sword: wide arc swing
			return math.sin(progress * math.pi) * 30  # 30 degree swing
		elif self.weapon_type == 'axe':
			# Axe: heavy overhead swing
			return math.sin(progress * math.pi) * 45  # 45 degree swing
		elif self.weapon_type == 'lance':
			# Lance: thrust forward and back
			thrust_distance = math.sin(progress * math.pi) * 10
			return thrust_distance
		elif self.weapon_type == 'rapier':
			# Rapier: quick precise stab
			return math.sin(progress * math.pi) * 15  # 15 degree precision
		elif self.weapon_type == 'sai':
			# Sai: defensive parry motion
			return math.sin(progress * math.pi) * 20  # 20 degree parry
		
		return 0
	
	def rotate_weapon_animated(self, weapon_surf, direction, angle_offset):
		"""Apply animated rotation to weapon"""
		base_angle = self.get_base_angle(direction)
		final_angle = base_angle + angle_offset
		
		return pygame.transform.rotate(weapon_surf, final_angle)
	
	def get_base_angle(self, direction):
		"""Get base rotation angle for direction"""
		if self.weapon_type == 'lance':
			# Lance: pointing directions
			if direction == 'right':
				return 0
			elif direction == 'left':
				return 180
			elif direction == 'up':
				return 90
			elif direction == 'down':
				return -90
		elif self.weapon_type == 'rapier':
			# Rapier: angled stabs
			if direction == 'right':
				return -15
			elif direction == 'left':
				return 165
			elif direction == 'up':
				return 75
			elif direction == 'down':
				return -105
		else:
			# Other weapons: diagonal swings
			if direction == 'right':
				return -45
			elif direction == 'left':
				return 45
			elif direction == 'up':
				return 135
			elif direction == 'down':
				return -135
		
		return 0
	
	def update(self):
		"""Update weapon animation"""
		self.update_animation()
		
		# Remove weapon when animation is complete
		elapsed_time = pygame.time.get_ticks() - self.start_time
		if elapsed_time >= self.duration:
			self.kill()


class Weapon360Damage(pygame.sprite.Sprite):
	"""Invisible sprite for 360-degree damage detection"""
	def __init__(self, player, groups):
		super().__init__(groups)
		self.sprite_type = 'weapon'
		self.player = player
		self.time_created = pygame.time.get_ticks()
		self.duration = 100  # Very short duration for damage detection
		
		# Adjust radius based on weapon type
		radius_map = {
			'sword': 80,
			'lance': 100,  # Longer reach
			'axe': 85,
			'rapier': 75,
			'sai': 70
		}
		radius = radius_map.get(player.weapon, 80)
		
		# Create invisible damage area
		self.image = pygame.Surface([radius*2, radius*2], pygame.SRCALPHA)
		# Make it completely transparent
		
		# Position at player center
		self.rect = self.image.get_rect(center=player.rect.center)
		self.hitbox = self.rect
	
	def update(self):
		# Remove after very short duration
		if pygame.time.get_ticks() - self.time_created > self.duration:
			self.kill()

class Magic(pygame.sprite.Sprite):
	"""Magic projectile that travels to target"""
	def __init__(self, player, groups, style, strength, cost, target_pos=None):
		super().__init__(groups)
		self.sprite_type = 'magic'
		self.player = player
		self.style = style
		self.strength = strength
		self.cost = cost
		self.frame_index = 0
		self.animation_speed = 0.2
		
		# Projectile movement
		self.pos = pygame.math.Vector2(player.rect.center)
		self.speed = 300  # pixels per second
		
		# Target direction
		if target_pos:
			self.direction = (pygame.math.Vector2(target_pos) - self.pos).normalize()
		else:
			# Default direction based on player facing
			direction_map = {
				'up': pygame.math.Vector2(0, -1),
				'down': pygame.math.Vector2(0, 1),
				'left': pygame.math.Vector2(-1, 0),
				'right': pygame.math.Vector2(1, 0)
			}
			player_direction = player.status.split('_')[0]
			self.direction = direction_map.get(player_direction, pygame.math.Vector2(1, 0))
		
		# Create animated magic effect
		self.frames = []
		if style == 'flame':
			self.frames = self.create_flame_projectile()
		elif style == 'heal':
			self.frames = self.create_water_projectile()  # Água/gelo para heal
		else:
			self.frames = self.create_default_projectile()
		
		self.image = self.frames[0]
		self.rect = self.image.get_rect(center=self.pos)
		
		self.time_created = pygame.time.get_ticks()
		self.max_distance = 400  # Maximum travel distance
		self.start_pos = pygame.math.Vector2(player.rect.center)
		
		# Don't apply heal immediately - let projectile travel first
		self.has_hit = False
		
	def create_flame_projectile(self):
		"""Create animated flame projectile"""
		frames = []
		for frame in range(8):
			surf = pygame.Surface((40, 40), pygame.SRCALPHA)
			
			# Compact flame projectile
			center = (20, 20)
			
			# Animated flame core
			for i in range(3):
				radius = 15 - i*4 + (frame % 2)
				if radius > 0:
					alpha = 255 - i*50
					if i == 0:
						color = (255, 255, 150)  # Hot center
					elif i == 1:
						color = (255, 150, 50)   # Orange
					else:
						color = (255, 100, 0)    # Red edges
					
					pygame.draw.circle(surf, color, center, radius)
			
			# Trailing sparks
			import random
			for _ in range(3):
				spark_x = 20 + random.randint(-15, 15)
				spark_y = 20 + random.randint(-15, 15)
				spark_color = (255, random.randint(100, 255), random.randint(0, 100))
				pygame.draw.circle(surf, spark_color, (spark_x, spark_y), 1)
			
			frames.append(surf)
		return frames
		
	def create_water_projectile(self):
		"""Create animated water/ice projectile"""
		frames = []
		for frame in range(8):
			surf = pygame.Surface((40, 40), pygame.SRCALPHA)
			
			# Water/ice projectile
			center = (20, 20)
			
			# Animated water core
			for i in range(3):
				radius = 15 - i*4 + (frame % 2)
				if radius > 0:
					if i == 0:
						color = (200, 255, 255)  # Ice blue center
					elif i == 1:
						color = (100, 200, 255)  # Water blue
					else:
						color = (50, 150, 255)   # Deep blue edges
					
					pygame.draw.circle(surf, color, center, radius)
			
			# Water droplets/ice crystals
			import random
			for _ in range(4):
				drop_x = 20 + random.randint(-15, 15)
				drop_y = 20 + random.randint(-15, 15)
				drop_color = (random.randint(100, 255), random.randint(200, 255), 255)
				pygame.draw.circle(surf, drop_color, (drop_x, drop_y), 1)
			
			frames.append(surf)
		return frames
	
	def create_default_projectile(self):
		"""Create default magic projectile"""
		frames = []
		for frame in range(6):
			surf = pygame.Surface((30, 30), pygame.SRCALPHA)
			center = (15, 15)
			radius = 12 + (frame % 3)
			color = (255, 255, 255)
			pygame.draw.circle(surf, color, center, radius)
			frames.append(surf)
		return frames
		
	def apply_effect_on_hit(self, target=None):
		"""Apply magic effect when projectile hits"""
		if self.has_hit:
			return
			
		self.has_hit = True
		
		if self.style == 'heal':
			# Heal player
			if self.player.health < self.player.stats['health']:
				self.player.health = min(self.player.stats['health'], self.player.health + self.strength)
				print(f"Curado! Vida: {self.player.health}/{self.player.stats['health']}")
		elif self.style == 'flame' and target:
			# Apply fire effect to enemy
			target.apply_fire_effect(self.strength)
		
		# Create impact effect
		self.create_impact_effect()
	
	def create_impact_effect(self):
		"""Create visual effect when projectile hits"""
		# This will be called when hitting enemies or reaching max distance
		from particles import MagicImpactEffect
		try:
			MagicImpactEffect(self.rect.center, [self.groups()[0]], self.style)
		except:
			pass  # Skip if particles module not available
	
	def update(self):
		# Animate projectile
		self.frame_index += self.animation_speed
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
		
		self.image = self.frames[int(self.frame_index)]
		
		# Move projectile
		dt = 1/60  # Assume 60 FPS
		self.pos += self.direction * self.speed * dt
		self.rect.center = self.pos
		
		# Check if traveled max distance
		distance_traveled = (self.pos - self.start_pos).length()
		if distance_traveled > self.max_distance:
			self.apply_effect_on_hit()  # Apply effect at max range for heal
			self.kill()

