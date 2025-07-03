"""
Sistema de entidades do jogo Wizarding Duel 2.0
"""

from .base import GameObject, AnimatedGameObject
from .magic_caster import MagicCaster
from .player import Player

__all__ = [
    'GameObject',
    'AnimatedGameObject',
    'MagicCaster',
    'Player'
]