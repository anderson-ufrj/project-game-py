# game setup
WIDTH    = 1280
HEIGTH   = 800
FPS      = 60
TILESIZE = 32

# ui 
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 300  # Metade da largura da barra de vida (600/2)
ITEM_BOX_SIZE = 80
UI_FONT = '../graphics/font/PressStart2P.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# weapons 
weapon_data = {
	'sword': {'cooldown': 300, 'damage': 15,'graphic':'../graphics/weapons/sword/full.png'},
	'lance': {'cooldown': 300, 'damage': 30,'graphic':'../graphics/weapons/lance/full.png'},
	'axe': {'cooldown': 300, 'damage': 20, 'graphic':'../graphics/weapons/axe/full.png'},
	'rapier':{'cooldown': 300, 'damage': 8, 'graphic':'../graphics/weapons/rapier/full.png'},
	'sai':{'cooldown': 300, 'damage': 10, 'graphic':'../graphics/weapons/sai/full.png'}}

# magic
magic_data = {
	'flame': {'strength': 5,'cost': 20,'graphic':'../graphics/particles/flame/fire.png'},
	'heal' : {'strength': 20,'cost': 10,'graphic':'../graphics/particles/heal/heal.png'}}

# enemy
monster_data = {
	'bigboi': {'health': 450, 'exp': 120, 'damage': 180, 'attack_type': 'leaf_attack', 'attack_sound': '../audio/attack/slash.wav', 'speed': 1.3, 'resistance': 3, 'attack_radius': 90,'notice_radius': 150},
	'black': {'health': 10, 'exp': 120, 'damage': 6, 'attack_type': 'leaf_attack','attack_sound': '../audio/attack/slash.wav', 'speed': 4, 'resistance': 3, 'attack_radius': 80,'notice_radius': 1200},
	'golu': {'health': 200, 'exp': 120, 'damage': 60, 'attack_type': 'leaf_attack', 'attack_sound': '../audio/attack/slash.wav', 'speed': 1.5, 'resistance': 3, 'attack_radius': 60,'notice_radius': 1000}}
