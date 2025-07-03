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

		# Rotate weapon based on direction and weapon type
		self.image = self.rotate_weapon(weapon_surf, direction)

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

	def rotate_weapon(self, weapon_surf, direction):
		"""Rotate weapon sprite based on direction and weapon type"""
		if self.weapon_type == 'lance':
			# Lance has specific rotations
			if direction == 'right':
				return weapon_surf  # No rotation
			elif direction == 'left':
				return pygame.transform.flip(weapon_surf, True, False)
			elif direction == 'up':
				return pygame.transform.rotate(weapon_surf, 90)
			elif direction == 'down':
				return pygame.transform.rotate(weapon_surf, -90)
		elif self.weapon_type == 'rapier':
			# Rapier similar to lance but thinner
			if direction == 'right':
				return weapon_surf
			elif direction == 'left':
				return pygame.transform.flip(weapon_surf, True, False)
			elif direction == 'up':
				return pygame.transform.rotate(weapon_surf, 90)
			elif direction == 'down':
				return pygame.transform.rotate(weapon_surf, -90)
		else:
			# Other weapons (sword, axe, sai) rotate normally
			if direction == 'right':
				return pygame.transform.rotate(weapon_surf, -45)
			elif direction == 'left':
				return pygame.transform.rotate(weapon_surf, 45)
			elif direction == 'up':
				return pygame.transform.rotate(weapon_surf, 135)
			elif direction == 'down':
				return pygame.transform.rotate(weapon_surf, -135)
		
		return weapon_surf

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
	"""Magic spell sprite"""
	def __init__(self, player, groups, style, strength, cost):
		super().__init__(groups)
		self.sprite_type = 'magic'
		self.player = player
		self.style = style
		self.strength = strength
		self.cost = cost
		self.frame_index = 0
		self.animation_speed = 0.15
		
		# Create animated magic effect
		self.frames = []
		if style == 'flame':
			self.frames = self.create_flame_animation()
		elif style == 'heal':
			self.frames = self.create_heal_animation()
		else:
			# Default magic effect
			self.frames = [pygame.Surface((64, 64), pygame.SRCALPHA)]
			pygame.draw.circle(self.frames[0], (255, 255, 255), (32, 32), 30)
		
		self.image = self.frames[0]
		
		# Position at player center
		self.rect = self.image.get_rect(center=player.rect.center)
		self.time_created = pygame.time.get_ticks()
		self.duration = 800  # Magic lasts longer for better visibility
		
		# Apply magic effect immediately
		if style == 'heal':
			self.apply_heal()
		
	def create_flame_animation(self):
		"""Create animated flame magic effect"""
		frames = []
		for frame in range(6):
			surf = pygame.Surface((80, 80), pygame.SRCALPHA)
			# Animated flame with pulsing effect
			for i in range(3):
				alpha = 255 - frame * 20
				color = (255, 200 - i*40, 0, alpha)
				radius = 25 - i*6 + (frame % 3) * 2
				center = (40, 40)
				pygame.draw.circle(surf, color[:3], center, radius)
			frames.append(surf)
		return frames
		
	def create_heal_animation(self):
		"""Create animated heal magic effect"""
		frames = []
		for frame in range(8):
			surf = pygame.Surface((80, 80), pygame.SRCALPHA)
			# Pulsing cross effect
			pulse = 1.0 + 0.3 * (frame / 8)
			width = int(6 * pulse)
			height = int(24 * pulse)
			
			# Cross
			pygame.draw.rect(surf, (0, 255, 100), (40 - width//2, 40 - height//2, width, height))
			pygame.draw.rect(surf, (0, 255, 100), (40 - height//2, 40 - width//2, height, width))
			
			# Glow effect
			glow_radius = int(20 * pulse)
			glow_color = (100, 255, 150, 150 - frame * 15)
			pygame.draw.circle(surf, glow_color[:3], (40, 40), glow_radius)
			frames.append(surf)
		return frames
		
	def apply_heal(self):
		"""Apply healing to player"""
		if self.player.health < self.player.stats['health']:
			self.player.health = min(self.player.stats['health'], self.player.health + self.strength)
			print(f"Curado! Vida: {self.player.health}/{self.player.stats['health']}")
			
	def update(self):
		# Animate magic effect
		self.frame_index += self.animation_speed
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
		
		self.image = self.frames[int(self.frame_index)]
		
		# Keep magic effect centered on player
		self.rect.center = self.player.rect.center
		
		# Remove after duration
		if pygame.time.get_ticks() - self.time_created > self.duration:
			self.kill()

