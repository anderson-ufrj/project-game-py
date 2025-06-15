"""
Classes base para todas as entidades do jogo
"""

import pygame
from abc import ABC, abstractmethod
from typing import Tuple, Optional, List
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.constants import *


class GameObject(pygame.sprite.Sprite, ABC):
    """Classe base para todos os objetos do jogo"""
    
    def __init__(self, x: float, y: float, width: int, height: int):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        self._create_image()
    
    @abstractmethod
    def _create_image(self):
        """Cria a imagem do objeto"""
        pass
    
    @abstractmethod
    def update(self, dt: float):
        """Atualiza o objeto"""
        pass
    
    def move(self, dt: float):
        """Move o objeto baseado na velocidade e aceleração"""
        self.velocity += self.acceleration * dt
        self.rect.x += self.velocity.x * dt
        self.rect.y += self.velocity.y * dt
    
    def check_bounds(self, screen_rect: pygame.Rect) -> bool:
        """Verifica se o objeto está dentro dos limites da tela"""
        return screen_rect.contains(self.rect)
    
    def get_center(self) -> Tuple[float, float]:
        """Retorna o centro do objeto"""
        return self.rect.center
    
    def set_center(self, x: float, y: float):
        """Define o centro do objeto"""
        self.rect.center = (x, y)
    
    def collides_with(self, other: 'GameObject') -> bool:
        """Verifica colisão com outro objeto"""
        return self.rect.colliderect(other.rect)
    
    def distance_to(self, other: 'GameObject') -> float:
        """Calcula a distância até outro objeto"""
        dx = self.rect.centerx - other.rect.centerx
        dy = self.rect.centery - other.rect.centery
        return (dx**2 + dy**2)**0.5


class AnimatedGameObject(GameObject):
    """Classe base para objetos animados"""
    
    def __init__(self, x: float, y: float, width: int, height: int, 
                 sprite_paths: Optional[List[str]] = None):
        self.sprites = []
        self.current_sprite_index = 0
        self.animation_speed = 10  # FPS da animação
        self.animation_timer = 0
        self.sprite_paths = sprite_paths or []
        
        super().__init__(x, y, width, height)
        
        if self.sprite_paths:
            self._load_sprites()
    
    def _load_sprites(self):
        """Carrega os sprites da animação"""
        for path in self.sprite_paths:
            try:
                sprite = pygame.image.load(path).convert_alpha()
                sprite = pygame.transform.scale(sprite, (self.rect.width, self.rect.height))
                self.sprites.append(sprite)
            except:
                # Se não conseguir carregar, cria um sprite placeholder
                placeholder = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
                pygame.draw.rect(placeholder, Colors.WHITE, placeholder.get_rect(), 2)
                self.sprites.append(placeholder)
        
        if self.sprites:
            self.image = self.sprites[0]
    
    def _create_image(self):
        """Cria imagem padrão se não houver sprites"""
        if not self.sprites:
            self.image.fill((255, 255, 255, 128))
    
    def update_animation(self, dt: float):
        """Atualiza a animação"""
        if len(self.sprites) <= 1:
            return
        
        self.animation_timer += dt
        
        if self.animation_timer >= 1000 / self.animation_speed:
            self.animation_timer = 0
            self.current_sprite_index = (self.current_sprite_index + 1) % len(self.sprites)
            self.image = self.sprites[self.current_sprite_index]
    
    def set_animation_speed(self, fps: float):
        """Define a velocidade da animação em FPS"""
        self.animation_speed = fps
    
    def reset_animation(self):
        """Reseta a animação para o primeiro frame"""
        self.current_sprite_index = 0
        self.animation_timer = 0
        if self.sprites:
            self.image = self.sprites[0]


class HealthBar:
    """Barra de vida para entidades"""
    
    def __init__(self, width: int, height: int, max_health: int):
        self.width = width
        self.height = height
        self.max_health = max_health
        self.current_health = max_health
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.border_color = Colors.WHITE
        self.bg_color = Colors.RED
        self.health_color = Colors.GREEN
        self.warning_color = Colors.YELLOW
        self.critical_color = Colors.ORANGE
    
    def update(self, current_health: int):
        """Atualiza a barra de vida"""
        self.current_health = max(0, min(current_health, self.max_health))
        self._draw()
    
    def _draw(self):
        """Desenha a barra de vida"""
        self.surface.fill((0, 0, 0, 0))
        
        # Borda
        pygame.draw.rect(self.surface, self.border_color, 
                        (0, 0, self.width, self.height), 2)
        
        # Fundo
        pygame.draw.rect(self.surface, self.bg_color,
                        (2, 2, self.width - 4, self.height - 4))
        
        # Vida
        if self.current_health > 0:
            health_percentage = self.current_health / self.max_health
            health_width = int((self.width - 4) * health_percentage)
            
            # Escolhe cor baseada na porcentagem de vida
            if health_percentage > 0.5:
                color = self.health_color
            elif health_percentage > 0.25:
                color = self.warning_color
            else:
                color = self.critical_color
            
            pygame.draw.rect(self.surface, color,
                           (2, 2, health_width, self.height - 4))
    
    def render(self, screen: pygame.Surface, x: int, y: int):
        """Renderiza a barra de vida na tela"""
        screen.blit(self.surface, (x, y))


class DamageNumber:
    """Números de dano flutuantes"""
    
    def __init__(self, x: float, y: float, damage: int, color: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.damage = damage
        self.color = color
        self.alpha = 255
        self.velocity_y = -2
        self.lifetime = 1000  # milliseconds
        self.timer = 0
        self.font = pygame.font.Font(None, 24)
        self.text = self.font.render(str(damage), True, color)
    
    def update(self, dt: float):
        """Atualiza o número de dano"""
        self.timer += dt
        
        # Move para cima
        self.y += self.velocity_y * dt * 0.05
        
        # Fade out
        progress = self.timer / self.lifetime
        self.alpha = int(255 * (1 - progress))
        
        return self.timer < self.lifetime
    
    def render(self, screen: pygame.Surface):
        """Renderiza o número de dano"""
        if self.alpha > 0:
            text_surface = self.text.copy()
            text_surface.set_alpha(self.alpha)
            rect = text_surface.get_rect(center=(self.x, self.y))
            screen.blit(text_surface, rect)