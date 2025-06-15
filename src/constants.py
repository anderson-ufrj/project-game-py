"""
Constantes e configurações globais do jogo Wizarding Duel 2.0
"""

import pygame
from enum import Enum

# Configurações da janela
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60
TITLE = "Wizarding Duel 2.0"

# Cores principais
class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    PURPLE = (128, 0, 128)
    CYAN = (0, 255, 255)
    ORANGE = (255, 165, 0)
    DARK_BLUE = (0, 0, 64)
    DARK_PURPLE = (64, 0, 64)
    GOLD = (255, 215, 0)
    SILVER = (192, 192, 192)
    
    # Cores de UI
    MENU_BG = (20, 0, 40)
    MENU_TEXT = (255, 215, 0)
    MENU_HOVER = (255, 255, 100)
    HUD_BG = (0, 0, 0, 128)  # Com transparência
    
    # Cores de efeitos
    SPELL_BLUE = (100, 200, 255)
    SPELL_RED = (255, 100, 100)
    SPELL_GREEN = (100, 255, 100)
    SPELL_PURPLE = (200, 100, 255)
    SPELL_YELLOW = (255, 255, 100)

# Estados do jogo
class GameState(Enum):
    MENU = "menu"
    CHARACTER_SELECT = "character_select"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    VICTORY = "victory"

# Configurações de gameplay
class GameSettings:
    # Player
    PLAYER_SPEED = 5
    PLAYER_HEALTH = 100
    PLAYER_INVULNERABILITY_TIME = 2000  # milliseconds
    PLAYER_SIZE = (64, 64)
    
    # Spells
    SPELL_SPEED = 8
    SPELL_DAMAGE = 20
    SPELL_COOLDOWN = 250  # milliseconds
    SPELL_SIZE = (32, 32)
    MAX_PLAYER_SPELLS = 10
    
    # Enemies
    PIXIE_BASE_HEALTH = 40
    PIXIE_BASE_SPEED = 2
    PIXIE_SIZE = (48, 48)
    PIXIE_SPELL_SPEED = 4
    PIXIE_SPELL_DAMAGE = 10
    PIXIE_POINTS = 10
    MAX_PIXIES = 20
    
    # Spawn rates (milliseconds)
    INITIAL_SPAWN_RATE = 2000
    MIN_SPAWN_RATE = 500
    SPAWN_RATE_DECREASE = 50
    
    # Difficulty
    LEVEL_UP_TIME = 30000  # 30 seconds
    HEALTH_SCALE_PER_LEVEL = 1.2
    SPEED_SCALE_PER_LEVEL = 1.1
    POINTS_SCALE_PER_LEVEL = 1.5

# Tipos de comportamento dos inimigos
class PixieBehavior(Enum):
    STRAIGHT = "straight"
    ZIGZAG = "zigzag"
    CIRCULAR = "circular"
    HOMING = "homing"
    RANDOM = "random"

# Tipos de feitiços
class SpellType(Enum):
    BASIC = "basic"
    FIRE = "fire"
    ICE = "ice"
    LIGHTNING = "lightning"
    ARCANE = "arcane"
    DARK = "dark"

# Configurações de personagens
class CharacterStats:
    WIZARD_BLUE = {
        "name": "Azure Wizard",
        "health": 100,
        "speed": 5,
        "spell_type": SpellType.ICE,
        "spell_damage": 20,
        "spell_cooldown": 250,
        "color": Colors.SPELL_BLUE,
        "sprite": "wizard1.png"
    }
    
    WIZARD_RED = {
        "name": "Crimson Mage",
        "health": 80,
        "speed": 6,
        "spell_type": SpellType.FIRE,
        "spell_damage": 25,
        "spell_cooldown": 300,
        "color": Colors.SPELL_RED,
        "sprite": "wizard2.png"
    }
    
    WIZARD_GREEN = {
        "name": "Nature Druid",
        "health": 120,
        "speed": 4,
        "spell_type": SpellType.ARCANE,
        "spell_damage": 15,
        "spell_cooldown": 200,
        "color": Colors.SPELL_GREEN,
        "sprite": "wizard3.png"
    }

# Configurações de partículas
class ParticleSettings:
    MAX_PARTICLES = 1000
    STAR_COUNT = 100
    EXPLOSION_PARTICLES = 50
    MAGIC_TRAIL_PARTICLES = 20
    
    # Tempo de vida (milliseconds)
    EXPLOSION_LIFETIME = 1000
    TRAIL_LIFETIME = 500
    IMPACT_LIFETIME = 300

# Configurações de UI
class UISettings:
    FONT_SIZE_TITLE = 72
    FONT_SIZE_MENU = 48
    FONT_SIZE_HUD = 24
    FONT_SIZE_SMALL = 16
    
    MENU_ITEM_SPACING = 80
    HUD_PADDING = 20
    
    # Animações
    FADE_SPEED = 5
    GLOW_SPEED = 2
    PULSE_SPEED = 0.05

# Teclas de controle
class Controls:
    # Movimento
    MOVE_UP = [pygame.K_w, pygame.K_UP]
    MOVE_DOWN = [pygame.K_s, pygame.K_DOWN]
    MOVE_LEFT = [pygame.K_a, pygame.K_LEFT]
    MOVE_RIGHT = [pygame.K_d, pygame.K_RIGHT]
    
    # Ações
    SHOOT = [pygame.K_SPACE, pygame.K_RETURN]
    PAUSE = [pygame.K_ESCAPE, pygame.K_p]
    CONFIRM = [pygame.K_RETURN, pygame.K_SPACE]
    BACK = [pygame.K_ESCAPE, pygame.K_BACKSPACE]
    
    # Especiais
    SPECIAL_ATTACK = [pygame.K_q]
    ULTIMATE = [pygame.K_e]
    DASH = [pygame.K_LSHIFT]

# Caminhos de assets
class AssetPaths:
    # Diretórios base
    ASSETS_DIR = "assets"
    IMAGES_DIR = "assets/images"
    SOUNDS_DIR = "assets/sounds"
    
    # Subdiretórios de imagens
    CHARACTERS_DIR = "assets/images/characters"
    SPELLS_DIR = "assets/images/spells"
    UI_DIR = "assets/images/ui"
    BACKGROUNDS_DIR = "assets/images/backgrounds"
    
    # Sons específicos
    SOUNDS = {
        "shoot": "shoot.wav",
        "hit": "hit.wav",
        "explosion": "explosion.wav",
        "powerup": "powerup.wav",
        "menu_select": "menu_select.wav",
        "menu_hover": "menu_hover.wav",
        "game_over": "game_over.wav",
        "victory": "victory.wav"
    }
    
    # Músicas
    MUSIC = {
        "menu": "menu_theme.mp3",
        "game": "battle_theme.mp3",
        "boss": "boss_theme.mp3",
        "victory": "victory_theme.mp3"
    }

# Configurações de debug
DEBUG = False
SHOW_FPS = True
SHOW_HITBOXES = False
INVINCIBLE_MODE = False