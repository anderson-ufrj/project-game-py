"""
Configurações globais do jogo Icarus
"""

# Resolução otimizada para PC
WIDTH = 1280
HEIGHT = 720

# Estados do jogo
GAME_STATES = {
    'MENU': 0,
    'PLAYING': 1,
    'PAUSED': 2,
    'GAME_OVER': 3,
    'CREDITS': 4,
    'SETTINGS': 5
}

# Cores (RGB)
COLORS = {
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'BLUE': (30, 144, 255),
    'GOLD': (255, 215, 0),
    'DARK_BLUE': (25, 25, 112),
    'LIGHT_BLUE': (173, 216, 230),
    'GRAY': (128, 128, 128),
    'DARK_GRAY': (64, 64, 64),
    'GREEN': (0, 255, 0),
    'RED': (255, 0, 0),
    'ORANGE': (255, 165, 0)
}

# Fontes
FONTS = {
    'TITLE': 72,
    'SUBTITLE': 48,
    'NORMAL': 32,
    'SMALL': 24,
    'TINY': 18
}

# Configurações do player
PLAYER_CONFIG = {
    'SPEED': 6,
    'JUMP_SPEED': 15,
    'GRAVITY': 0.8,
    'MAX_FALL_SPEED': 12
}

# FPS
FPS = 60

# Créditos
CREDITS = {
    'DEVELOPER': 'Anderson Henrique',
    'INSTITUTION': 'IFSULDEMINAS – Campus Muzambinho',
    'COURSE': 'Ciência da Computação',
    'SUBJECT': 'Tópicos Especiais I',
    'GITHUB': 'github.com/anderson-ufrj',
    'LINKEDIN': 'linkedin.com/in/anderson-h-silva95'
}