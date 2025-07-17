import pygame 
import math
from settings import weapon_data

class Weapon(pygame.sprite.Sprite):
	def __init__(self,player,groups):
		super().__init__(groups)
		self.sprite_type = 'weapon'
		self.player = player
		self.direction = player.status.split('_')[0]
		self.weapon_type = player.weapon
		
		# Animation properties
		self.start_time = pygame.time.get_ticks()
		self.duration = 200  # Attack animation duration
		self.animation_progress = 0.0

		# Load weapon graphic with proper scaling
		self.original_weapon_surf = self.load_weapon_graphic()
		
		# Calculate proper positioning
		self.base_position = self.calculate_base_position()
		
		# Initialize with first frame
		self.update_animation()

	def load_weapon_graphic(self):
		"""Load directional weapon graphic (the correct approach!)"""
		try:
			# Use directional files instead of full.png - this is the key!
			direction_file = f"../graphics/weapons/{self.weapon_type}/{self.direction}.png"
			print(f"🔧 Carregando: {direction_file}")
			
			weapon_surf = pygame.image.load(direction_file).convert_alpha()
			original_size = weapon_surf.get_size()
			print(f"📏 Tamanho original: {original_size}")
			
			# Scale 2x to make it visible but preserve aspect ratio
			new_width = original_size[0] * 2
			new_height = original_size[1] * 2
			weapon_surf = pygame.transform.scale(weapon_surf, (new_width, new_height))
			
			print(f"✅ {self.weapon_type} {self.direction}: {original_size} -> {weapon_surf.get_size()}")
			return weapon_surf
			
		except Exception as e:
			print(f"⚠️ Erro ao carregar {self.weapon_type}/{self.direction}.png: {e}")
			print(f"🔄 Tentando fallback para full.png...")
			
			# Fallback to full.png if directional file doesn't exist
			try:
				weapon_surf = pygame.image.load(weapon_data[self.weapon_type]['graphic']).convert_alpha()
				# Scale 3x for full.png since they're smaller
				original_size = weapon_surf.get_size()
				weapon_surf = pygame.transform.scale(weapon_surf, (original_size[0] * 3, original_size[1] * 3))
				print(f"🔄 Fallback {self.weapon_type}: {original_size} -> {weapon_surf.get_size()}")
				return weapon_surf
			except Exception as e2:
				print(f"❌ Fallback também falhou: {e2}")
				return self.create_fallback_weapon()
	
	def create_fallback_weapon(self):
		"""Create enhanced fallback weapon graphics"""
		if self.weapon_type == 'sword':
			surf = pygame.Surface([48, 48], pygame.SRCALPHA)
			# Draw sword shape
			pygame.draw.rect(surf, (192, 192, 192), (20, 8, 8, 32))  # Blade
			pygame.draw.rect(surf, (139, 69, 19), (18, 36, 12, 8))   # Handle
			pygame.draw.circle(surf, (255, 215, 0), (24, 42), 3)     # Pommel
			
		elif self.weapon_type == 'lance':
			surf = pygame.Surface([64, 16], pygame.SRCALPHA)
			# Draw lance shape
			pygame.draw.rect(surf, (139, 69, 19), (8, 6, 48, 4))     # Shaft
			pygame.draw.polygon(surf, (192, 192, 192), [(56, 2), (62, 8), (56, 14)])  # Tip
			
		elif self.weapon_type == 'axe':
			surf = pygame.Surface([52, 52], pygame.SRCALPHA)
			# Draw axe shape
			pygame.draw.rect(surf, (139, 69, 19), (22, 16, 8, 28))   # Handle
			pygame.draw.polygon(surf, (105, 105, 105), [(22, 16), (8, 12), (8, 28), (22, 24)])  # Blade
			
		elif self.weapon_type == 'rapier':
			surf = pygame.Surface([56, 12], pygame.SRCALPHA)
			# Draw rapier shape
			pygame.draw.rect(surf, (255, 215, 0), (8, 4, 40, 4))     # Thin blade
			pygame.draw.rect(surf, (139, 69, 19), (44, 2, 8, 8))     # Handle
			pygame.draw.circle(surf, (192, 192, 192), (50, 6), 2)    # Guard
			
		elif self.weapon_type == 'sai':
			surf = pygame.Surface([32, 48], pygame.SRCALPHA)
			# Draw sai shape
			pygame.draw.rect(surf, (70, 130, 180), (14, 8, 4, 32))   # Main prong
			pygame.draw.rect(surf, (70, 130, 180), (10, 12, 2, 16))  # Left prong
			pygame.draw.rect(surf, (70, 130, 180), (20, 12, 2, 16))  # Right prong
			pygame.draw.rect(surf, (139, 69, 19), (12, 36, 8, 8))    # Handle
			
		else:
			# Generic weapon
			surf = pygame.Surface([48, 48], pygame.SRCALPHA)
			pygame.draw.rect(surf, (200, 200, 200), (20, 12, 8, 24))
		
		return surf

	def calculate_base_position(self):
		"""Calculate weapon base position relative to player"""
		offset = self.get_weapon_offset()
		
		if self.direction == 'right':
			return self.player.rect.midright + pygame.math.Vector2(-offset, 16)
		elif self.direction == 'left':
			return self.player.rect.midleft + pygame.math.Vector2(offset, 16)
		elif self.direction == 'down':
			return self.player.rect.midbottom + pygame.math.Vector2(-10, -offset)
		else:  # up
			return self.player.rect.midtop + pygame.math.Vector2(-10, offset)

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
		"""Update weapon animation with smooth movement"""
		elapsed_time = pygame.time.get_ticks() - self.start_time
		self.animation_progress = min(elapsed_time / self.duration, 1.0)
		
		# Create smooth animation based on weapon type
		self.apply_weapon_animation()
		
		# Update position
		self.update_position()
	
	def apply_weapon_animation(self):
		"""Apply weapon-specific animation - simplified since we use directional images"""
		# Since we're using directional images, we don't need rotation!
		# Just apply subtle animation effects
		
		# Get animation offset for subtle movement
		animation_offset = self.get_animation_offset()
		
		# Apply minimal rotation for animation effect only
		if abs(animation_offset) > 0:
			self.image = pygame.transform.rotate(self.original_weapon_surf, animation_offset)
		else:
			self.image = self.original_weapon_surf.copy()
	
	def get_base_rotation_angle(self):
		"""Get base rotation angle for each weapon type and direction"""
		angle_map = {
			'sword': {
				'right': -45, 'left': 135, 'up': 45, 'down': -135
			},
			'lance': {
				'right': 0, 'left': 180, 'up': 90, 'down': -90
			},
			'axe': {
				'right': -30, 'left': 150, 'up': 60, 'down': -120
			},
			'rapier': {
				'right': -10, 'left': 170, 'up': 80, 'down': -100
			},
			'sai': {
				'right': -45, 'left': 135, 'up': 45, 'down': -135
			}
		}
		
		return angle_map.get(self.weapon_type, {}).get(self.direction, 0)
	
	def get_animation_offset(self):
		"""Get subtle animation offset - much smaller since images are pre-oriented"""
		# Use smooth sine wave for natural movement
		sin_progress = math.sin(self.animation_progress * math.pi)
		
		# Much smaller angles since we're not doing full rotation
		if self.weapon_type == 'sword':
			# Sword: subtle swing
			return sin_progress * 8
		elif self.weapon_type == 'axe':
			# Axe: small heavy movement
			return sin_progress * 10
		elif self.weapon_type == 'lance':
			# Lance: minimal rotation (more thrust-based)
			return sin_progress * 3
		elif self.weapon_type == 'rapier':
			# Rapier: precise tiny movement
			return sin_progress * 5
		elif self.weapon_type == 'sai':
			# Sai: small defensive movement
			return sin_progress * 6
		
		return 0
	
	def update_position(self):
		"""Update weapon position during animation"""
		# Base position
		pos = pygame.math.Vector2(self.base_position)
		
		# Add animation-based position offset
		position_offset = self.get_position_offset()
		pos += position_offset
		
		# Set rect position
		self.rect = self.image.get_rect(center=pos)
	
	def get_position_offset(self):
		"""Get position offset during animation"""
		# Use animation progress for smooth movement
		thrust_amount = math.sin(self.animation_progress * math.pi) * 15
		
		if self.weapon_type == 'lance':
			# Lance thrusts forward more
			thrust_amount *= 2
		
		# Direction-based thrust
		if self.direction == 'right':
			return pygame.math.Vector2(thrust_amount, 0)
		elif self.direction == 'left':
			return pygame.math.Vector2(-thrust_amount, 0)
		elif self.direction == 'up':
			return pygame.math.Vector2(0, -thrust_amount)
		elif self.direction == 'down':
			return pygame.math.Vector2(0, thrust_amount)
		
		return pygame.math.Vector2(0, 0)
	
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

