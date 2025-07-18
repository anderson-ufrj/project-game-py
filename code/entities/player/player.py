import pygame 
from utils.constants import *
from utils.helpers import import_folder
from entities.base_entity import Entity
from systems.difficulty.difficulty_manager import difficulty_manager
from systems.audio.audio_manager import audio_manager

class Player(Entity):
	def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack,create_magic):
		super().__init__(groups)
		self.image = pygame.image.load('../graphics/player/down_idle/tile000.png').convert_alpha()
		self.image = pygame.transform.scale2x(self.image)
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(-100,-52)

		# graphics setup
		self.import_player_assets()
		self.status = 'down'
		self.inventory = {'healthOrbs':0, "attackOrbs":0 , 'speedOrbs': 0, "keys":0, "zappaguriStone":0 }

		# movement 
		self.attacking = False
		self.attack_cooldown = 200
		self.attack_time = 25
		self.obstacle_sprites = obstacle_sprites
		# Audio now handled by AudioManager - removed walking_sound
		# weapon
		self.create_attack = create_attack
		self.destroy_attack = destroy_attack
		self.weapon_index = 0
		self.weapon = list(weapon_data.keys())[self.weapon_index]
		self.can_switch_weapon = True
		self.weapon_switch_time = None
		self.switch_duration_cooldown = 200

		# magic 
		self.create_magic = create_magic
		self.magic_index = 0
		self.magic = list(magic_data.keys())[self.magic_index]
		self.can_switch_magic = True
		self.magic_switch_time = None

		# stats (base values)
		base_health = 500
		base_attack = 10
		
		# Apply difficulty modifiers
		modified_health, modified_attack = difficulty_manager.apply_to_player_stats(base_health, base_attack)
		
		self.stats = {'health': modified_health,'energy':120,'attack': modified_attack,'magic': 4,'speed': 3}
		self.health = self.stats['health']
		self.energy = self.stats['energy'] * 0.8
		self.exp = 123
		self.speed = self.stats['speed']
		self.attack = self.stats['attack']

		# damage timer
		self.vulnerable = True
		self.hurt_time = None
		self.invulnerability_duration = 500

	def import_player_assets(self):
		character_path = '../graphics/player/'
		self.animations = {'up': [],'down': [],'left': [],'right': [],
			'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
			'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[]}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	def input(self):
		self.speedmod = 0
		keys = pygame.key.get_pressed()
		if not self.attacking:
			self.speedmod = 0

			# movement input
			if keys[pygame.K_LSHIFT]:
				self.energy -= 0.2  # Reduzido de 0.3 para 0.2

				if self.energy < 0:
					self.energy = 0

				if self.energy < 1:
					self.speedmod = 0
				else:
					self.speedmod = 3
			else:
				if 0 <= self.energy <= self.stats['energy']:
					self.energy += 0.15  # Aumentado de 0.1 para 0.15 (recuperação mais rápida)
					self.speedmod = 0

			if keys[pygame.K_UP]:
				self.direction.y = -1
				self.status = 'up'
			elif keys[pygame.K_DOWN]:
				self.direction.y = 1
				self.status = 'down'
			else:
				self.direction.y = 0

			if keys[pygame.K_RIGHT]:
				self.direction.x = 1
				self.status = 'right'
			elif keys[pygame.K_LEFT]:
				self.direction.x = -1
				self.status = 'left'
			else:
				self.direction.x = 0

			# attack input - prevent overlapping animations
			if keys[pygame.K_SPACE] and not self.attacking:
				print('SPACE UP')
				self.attacking = True
				self.attack_time = pygame.time.get_ticks()
				self.create_attack()

			# magic input - prevent overlapping with attacks
			if keys[pygame.K_LCTRL] and not self.attacking:
				self.attacking = True
				self.attack_time = pygame.time.get_ticks()
				style = list(magic_data.keys())[self.magic_index]
				strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
				cost = list(magic_data.values())[self.magic_index]['cost']
				self.create_magic(style, strength, cost)

			if keys[pygame.K_q] and self.can_switch_weapon:
				self.can_switch_weapon = False
				self.weapon_switch_time = pygame.time.get_ticks()

				if self.weapon_index < len(list(weapon_data.keys())) - 1:
					self.weapon_index += 1
				else:
					self.weapon_index = 0

				self.weapon = list(weapon_data.keys())[self.weapon_index]
				# Mostrar nome da arma
				weapon_names = {'sword': 'Espada', 'lance': 'Lança', 'axe': 'Machado', 'rapier': 'Florete', 'sai': 'Sai'}
				print(f"Arma trocada para: {weapon_names.get(self.weapon, self.weapon)}")
			#
			if keys[pygame.K_e] and self.can_switch_magic:
				self.can_switch_magic = False
				self.magic_switch_time = pygame.time.get_ticks()

				if self.magic_index < len(list(magic_data.keys())) - 1:
					self.magic_index += 1
				else:
					self.magic_index = 0

				self.magic = list(magic_data.keys())[self.magic_index]
				# Mostrar nome da magia
				magic_names = {'flame': 'Chama', 'heal': 'Cura'}
				print(f"Magia trocada para: {magic_names.get(self.magic, self.magic)}")

	def get_status(self):

		# idle status
		if self.direction.x == 0 and self.direction.y == 0:
			if not 'idle' in self.status and not 'attack' in self.status:
				self.status = self.status + '_idle'

		if self.attacking:
			self.direction.x = 0
			self.direction.y = 0
			if not 'attack' in self.status:
				if 'idle' in self.status:
					self.status = self.status.replace('_idle','_attack')
				else:
					self.status = self.status + '_attack'
		else:
			if 'attack' in self.status:
				self.status = self.status.replace('_attack','')

	def cooldowns(self):
		current_time = pygame.time.get_ticks()

		if self.attacking:
			if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
				self.attacking = False
				self.destroy_attack()

		if not self.can_switch_weapon:
			if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
				self.can_switch_weapon = True
		#
		if not self.can_switch_magic:
			if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
				self.can_switch_magic = True

		if not self.vulnerable:
			if current_time - self.hurt_time >= self.invulnerability_duration:
				self.vulnerable = True

	def animate(self):
		animation = self.animations[self.status]

		# loop over the frame index 
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		# set the image
		self.image = animation[int(self.frame_index)]
		self.image = pygame.transform.scale2x(self.image)
		self.rect = self.image.get_rect(center = self.hitbox.center)

		# flicker 
		if not self.vulnerable:
			alpha = self.wave_value()
			self.image.set_alpha(alpha)
		else:
			self.image.set_alpha(255)

	def get_full_weapon_damage(self):
		base_damage = self.stats['attack']
		weapon_damage = weapon_data[self.weapon]['damage']
		return base_damage + weapon_damage

	def update(self):
		self.input()
		self.cooldowns()
		self.get_status()
		self.animate()
		self.move(self.speed+self.speedmod)