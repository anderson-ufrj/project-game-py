import pygame
from settings import * 
from player import Player
class UI:
	def __init__(self):
		
		# general 
		self.display_surface = pygame.display.get_surface()
		self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)

		# bar setup 
		self.health_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH*3,BAR_HEIGHT)
		self.energy_bar_rect = pygame.Rect(10,34,ENERGY_BAR_WIDTH,BAR_HEIGHT)

		# convert weapon dictionary
		self.weapon_graphics = []
		for weapon in weapon_data.values():
			path = weapon['graphic']
			weapon = pygame.image.load(path).convert_alpha()
			self.weapon_graphics.append(weapon)

		# convert magic dictionary
		self.magic_graphics = []
		for magic in magic_data.values():
			magic = pygame.image.load(magic['graphic']).convert_alpha()
			self.magic_graphics.append(magic)

		self.pixelated_font = pygame.font.Font('../graphics/font/PressStart2P.ttf', 24)

		# Status message variables
		self.status_message = ""
		self.status_message_duration = 2000  # Duration in milliseconds
		self.status_message_start_time = 0
		self.current_level = 1

	def show_bar(self,current,max_amount,bg_rect,color):
		# draw bg 
		pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)

		# converting stat to pixel
		ratio = current / max_amount
		current_width = bg_rect.width * ratio
		current_rect = bg_rect.copy()
		current_rect.width = current_width

		# drawing the bar
		pygame.draw.rect(self.display_surface,color,current_rect)
		pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)

	def show_exp(self,player):
		if self.current_level == 1:
			text_surf = self.font.render(f"Espaço: Atacar | Q: Trocar arma | E: Trocar magia | Ctrl: Usar magia",False,TEXT_COLOR)
		elif self.current_level == 2:
			text_surf = self.font.render(f"Encontre uma saída do labirinto! | Q: Trocar arma | E: Magia",False,TEXT_COLOR)
		elif self.current_level == 3:
			text_surf = self.font.render(f"Você tem {player.inventory['keys']} chaves | Q: Trocar arma",False,TEXT_COLOR)
		elif self.current_level == 4:
			text_surf = self.font.render(f"Fuja! | Q: Trocar arma | E: Magia",False,TEXT_COLOR)
		x = self.display_surface.get_size()[0] - 20
		y = self.display_surface.get_size()[1] - 20
		text_rect = text_surf.get_rect(bottomright = (x,y))

		# Create translucent background with elegant design
		bg_surface = pygame.Surface(text_rect.inflate(20,20).size, pygame.SRCALPHA)
		bg_surface.fill((10, 10, 10, 180))  # Semi-transparent dark background
		
		# Add subtle gradient effect
		gradient_surface = pygame.Surface(text_rect.inflate(20,20).size, pygame.SRCALPHA)
		gradient_surface.fill((40, 40, 40, 120))
		bg_surface.blit(gradient_surface, (0, 0))
		
		self.display_surface.blit(bg_surface, text_rect.inflate(20,20).topleft)
		self.display_surface.blit(text_surf,text_rect)
		
		# Elegant double border
		pygame.draw.rect(self.display_surface,(100, 100, 100, 200),text_rect.inflate(20,20),2)
		pygame.draw.rect(self.display_surface,(150, 150, 150, 150),text_rect.inflate(20,20),1)

	def selection_box(self,left,top, has_switched):
		bg_rect = pygame.Rect(left,top,ITEM_BOX_SIZE,ITEM_BOX_SIZE)
		
		# Create translucent selection box background
		bg_surface = pygame.Surface((ITEM_BOX_SIZE, ITEM_BOX_SIZE), pygame.SRCALPHA)
		bg_surface.fill((30, 30, 40, 160))  # Semi-transparent background
		
		# Add inner highlight for depth
		inner_surface = pygame.Surface((ITEM_BOX_SIZE-8, ITEM_BOX_SIZE-8), pygame.SRCALPHA)
		inner_surface.fill((50, 50, 60, 100))
		bg_surface.blit(inner_surface, (4, 4))
		
		self.display_surface.blit(bg_surface, bg_rect.topleft)
		
		if has_switched:
			# Active state with golden glow
			pygame.draw.rect(self.display_surface,(255, 215, 0),bg_rect,3)  # Gold border
			pygame.draw.rect(self.display_surface,(255, 255, 150),bg_rect,1)  # Inner glow
		else:
			# Normal state with silver border
			pygame.draw.rect(self.display_surface,(120, 120, 140),bg_rect,2)
			pygame.draw.rect(self.display_surface,(160, 160, 180),bg_rect,1)
		return bg_rect

	def weapon_overlay(self,weapon_index,has_switched):
		bg_rect = self.selection_box(10,630,has_switched)
		weapon_surf = self.weapon_graphics[weapon_index]
		weapon_rect = weapon_surf.get_rect(center = bg_rect.center)

		self.display_surface.blit(weapon_surf,weapon_rect)

	def blit_pixelated_text(self, text, position):
		text_surface = self.pixelated_font.render(text, True, TEXT_COLOR)
		self.display_surface.blit(text_surface, position)

	def magic_overlay(self,magic_index,has_switched):
		bg_rect = self.selection_box(80,635,has_switched)
		magic_surf = self.magic_graphics[magic_index]
		magic_rect = magic_surf.get_rect(center = bg_rect.center)

		self.display_surface.blit(magic_surf,magic_rect)

	def show_status_message(self):
		if self.status_message:
			current_time = pygame.time.get_ticks()
			elapsed_time = current_time - self.status_message_start_time

			if elapsed_time < self.status_message_duration:
				text_surface = self.pixelated_font.render(self.status_message, True, (255, 255, 255))
				x = self.display_surface.get_size()[0] // 2 - text_surface.get_width() // 2
				y = self.display_surface.get_size()[1] - 80
				text_rect = text_surface.get_rect(topleft=(x, y))

				# Create elegant translucent message box
				bg_surface = pygame.Surface(text_rect.inflate(30, 15).size, pygame.SRCALPHA)
				
				# Multi-layer background for depth
				bg_surface.fill((20, 20, 30, 200))  # Dark blue-tinted base
				
				# Add inner glow effect
				inner_surface = pygame.Surface(text_rect.inflate(20, 10).size, pygame.SRCALPHA)
				inner_surface.fill((60, 60, 80, 100))
				bg_surface.blit(inner_surface, (5, 2.5))
				
				# Add text shadow for better readability
				shadow_surface = self.pixelated_font.render(self.status_message, True, (0, 0, 0))
				shadow_rect = shadow_surface.get_rect(topleft=(text_rect.left + 2, text_rect.top + 2))
				
				self.display_surface.blit(bg_surface, text_rect.inflate(30, 15).topleft)
				self.display_surface.blit(shadow_surface, shadow_rect)  # Shadow
				self.display_surface.blit(text_surface, text_rect)  # Main text
				
				# Stylish rounded-corner effect with multiple borders
				pygame.draw.rect(self.display_surface, (120, 120, 140), text_rect.inflate(30, 15), 2)
				pygame.draw.rect(self.display_surface, (180, 180, 200), text_rect.inflate(30, 15), 1)
			else:
				self.status_message = ""  # Clear the status message when its duration is over

	def display(self,player):
		self.show_bar(player.health,player.stats['health'],self.health_bar_rect,HEALTH_COLOR)
		self.show_bar(player.energy,player.stats['energy'],self.energy_bar_rect,ENERGY_COLOR)
		self.show_exp(player)
		self.show_status_message()

		self.weapon_overlay(player.weapon_index,not player.can_switch_weapon)
		self.magic_overlay(player.magic_index,not player.can_switch_magic)

	def set_status_message(self, message):
		self.status_message = message
		self.status_message_start_time = pygame.time.get_ticks()
