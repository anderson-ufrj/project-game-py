import pygame 
import math

class Weapon(pygame.sprite.Sprite):
	def __init__(self,player,groups):
		super().__init__(groups)
		self.sprite_type = 'weapon'
		direction = player.status.split('_')[0]

		# graphic - restore original visual
		self.image = pygame.Surface([64,64], pygame.SRCALPHA)

		weapon_offset_from_player = 20
		# placement - restore original positioning
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

class Weapon360Damage(pygame.sprite.Sprite):
	"""Invisible sprite for 360-degree damage detection"""
	def __init__(self, player, groups):
		super().__init__(groups)
		self.sprite_type = 'weapon'
		self.player = player
		self.time_created = pygame.time.get_ticks()
		self.duration = 100  # Very short duration for damage detection
		
		# Create invisible damage area
		radius = 80
		self.image = pygame.Surface([radius*2, radius*2], pygame.SRCALPHA)
		# Make it completely transparent
		
		# Position at player center
		self.rect = self.image.get_rect(center=player.rect.center)
		self.hitbox = self.rect
	
	def update(self):
		# Remove after very short duration
		if pygame.time.get_ticks() - self.time_created > self.duration:
			self.kill()

