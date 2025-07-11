"""
Constantes globais do jogo
"""

# Configurações de tela
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
FPS = 60
TILE_SIZE = 32

# Configurações de UI
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 300
ITEM_BOX_SIZE = 80
UI_FONT_PATH = '../graphics/font/PressStart2P.ttf'
UI_FONT_SIZE = 18

# Cores gerais
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# Cores da UI
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'blue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# Estados do jogo
GAME_STATES = {
    'NAME_INPUT': -1,
    'MAIN_MENU': 0,
    'LEVEL_1': 3,
    'LEVEL_2': 4,
    'LEVEL_3': 5,
    'LEVEL_4': 6,
    'GAME_OVER': 20,
    'STATS': 30,
    'ACHIEVEMENTS': 31,
    'DIFFICULTY': 40,
    'LOAD_GAME': 50,
    'SAVE_GAME': 51
}

# Dados de armas
WEAPON_DATA = {
    'sword': {
        'cooldown': 300,
        'damage': 15,
        'graphic': '../graphics/weapons/sword/full.png'
    },
    'lance': {
        'cooldown': 300,
        'damage': 30,
        'graphic': '../graphics/weapons/lance/full.png'
    },
    'axe': {
        'cooldown': 300,
        'damage': 20,
        'graphic': '../graphics/weapons/axe/full.png'
    },
    'rapier': {
        'cooldown': 300,
        'damage': 8,
        'graphic': '../graphics/weapons/rapier/full.png'
    },
    'sai': {
        'cooldown': 300,
        'damage': 10,
        'graphic': '../graphics/weapons/sai/full.png'
    }
}

# Dados de magia
MAGIC_DATA = {
    'flame': {
        'strength': 5,
        'cost': 20,
        'graphic': '../graphics/particles/flame/fire.png'
    },
    'heal': {
        'strength': 20,
        'cost': 10,
        'graphic': '../graphics/particles/heal/heal.png'
    }
}

# Dados de inimigos
MONSTER_DATA = {
    'bigboi': {
        'health': 450,
        'exp': 120,
        'damage': 180,
        'attack_type': 'leaf_attack',
        'attack_sound': '../audio/attack/slash.wav',
        'speed': 1.3,
        'resistance': 3,
        'attack_radius': 90,
        'notice_radius': 150
    },
    'black': {
        'health': 10,
        'exp': 120,
        'damage': 6,
        'attack_type': 'leaf_attack',
        'attack_sound': '../audio/attack/slash.wav',
        'speed': 4,
        'resistance': 3,
        'attack_radius': 80,
        'notice_radius': 1200
    },
    'golu': {
        'health': 200,
        'exp': 120,
        'damage': 60,
        'attack_type': 'leaf_attack',
        'attack_sound': '../audio/attack/slash.wav',
        'speed': 1.5,
        'resistance': 3,
        'attack_radius': 60,
        'notice_radius': 1000
    }
}

# Paths de recursos
PATHS = {
    'GRAPHICS': '../graphics',
    'AUDIO': '../audio',
    'FONTS': '../font',
    'MAPS': '../map new',
    'SAVES': '../saves'
}