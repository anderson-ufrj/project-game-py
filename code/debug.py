import pygame
from font_manager import font_manager
from professional_renderer import professional_renderer

def debug(info, y=10, x=10):
	"""Debug function with modern rendering and better visibility"""
	display_surface = pygame.display.get_surface()
	
	# Use professional renderer for debug text
	debug_surf, debug_rect = professional_renderer.render_text_professional(
		str(info),
		'debug',  # Use debug font size
		(255, 255, 255),  # White text
		background=(0, 0, 0),  # Black background for contrast
		shadow=True,
		anti_alias=True
	)
	
	# Position the debug text
	debug_rect.topleft = (x, y)
	display_surface.blit(debug_surf, debug_rect)
