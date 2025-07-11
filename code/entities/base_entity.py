"""
Entidade base refatorada para nova arquitetura
"""
import pygame
from math import sin
from typing import Optional, List

from utils.helpers import normalize_vector


class Entity(pygame.sprite.Sprite):
    """
    Classe base para todas as entidades (refatorada do entity.py original).
    Mantém compatibilidade com o código existente.
    """
    
    def __init__(self, groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()
        
        # Referência para sprites de obstáculos (será definida pelas subclasses)
        self.obstacle_sprites = None
    
    def move(self, speed: float) -> None:
        """
        Move a entidade com detecção de colisão.
        
        Args:
            speed (float): Velocidade de movimento
        """
        if self.direction.magnitude() != 0:
            self.direction = normalize_vector(self.direction)
        
        # Movimento horizontal
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        
        # Movimento vertical
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        
        # Atualiza posição do rect
        self.rect.center = self.hitbox.center
    
    def collision(self, direction: str) -> None:
        """
        Verifica e resolve colisões com obstáculos.
        
        Args:
            direction (str): Direção da colisão ('horizontal' ou 'vertical')
        """
        if not self.obstacle_sprites:
            return
        
        for sprite in self.obstacle_sprites:
            if hasattr(sprite, 'hitbox') and sprite.hitbox.colliderect(self.hitbox):
                if direction == 'horizontal':
                    if self.direction.x > 0:  # Moving right
                        self.hitbox.right = sprite.hitbox.left
                    elif self.direction.x < 0:  # Moving left
                        self.hitbox.left = sprite.hitbox.right
                        
                elif direction == 'vertical':
                    if self.direction.y > 0:  # Moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    elif self.direction.y < 0:  # Moving up
                        self.hitbox.top = sprite.hitbox.bottom
    
    def wave_value(self) -> int:
        """
        Retorna valor sinusoidal para efeitos visuais.
        
        Returns:
            int: Valor 0 ou 255 baseado em sine wave
        """
        value = sin(pygame.time.get_ticks() * 0.01)
        return 255 if value >= 0 else 0