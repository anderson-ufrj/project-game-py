"""
Sistema de Design Moderno para Projeto Ícaro
Inspirado em Material Design 3, Glassmorphism e Design Systems modernos
"""
import pygame
import math
from typing import Tuple, List

class ModernColors:
    """Paleta de cores moderna e harmoniosa"""
    
    # Cores primárias - Inspirado em gradientes modernos
    PRIMARY_DARK = (10, 10, 20)
    PRIMARY_BLUE = (59, 130, 246)      # Blue-500
    PRIMARY_PURPLE = (139, 92, 246)    # Purple-500
    PRIMARY_CYAN = (6, 182, 212)       # Cyan-500
    
    # Cores secundárias
    SECONDARY_GOLD = (245, 158, 11)    # Amber-500
    SECONDARY_PINK = (236, 72, 153)    # Pink-500
    SECONDARY_GREEN = (34, 197, 94)    # Green-500
    
    # Cores neutras modernas
    NEUTRAL_50 = (249, 250, 251)
    NEUTRAL_100 = (243, 244, 246)
    NEUTRAL_200 = (229, 231, 235)
    NEUTRAL_300 = (209, 213, 219)
    NEUTRAL_400 = (156, 163, 175)
    NEUTRAL_500 = (107, 114, 128)
    NEUTRAL_600 = (75, 85, 99)
    NEUTRAL_700 = (55, 65, 81)
    NEUTRAL_800 = (31, 41, 55)
    NEUTRAL_900 = (17, 24, 39)
    
    # Cores especiais para glassmorphism
    GLASS_WHITE = (255, 255, 255, 30)
    GLASS_BLUE = (59, 130, 246, 50)
    GLASS_PURPLE = (139, 92, 246, 40)
    GLASS_BORDER = (255, 255, 255, 60)
    
    # Gradientes
    GRADIENT_HERO = [(139, 92, 246), (59, 130, 246)]      # Purple to Blue
    GRADIENT_ACCENT = [(245, 158, 11), (236, 72, 153)]    # Gold to Pink
    GRADIENT_DARK = [(17, 24, 39), (31, 41, 55)]          # Dark gradient

class ModernTypography:
    """Sistema de tipografia moderno"""
    
    # Tamanhos de fonte modernos (escala 1.25)
    DISPLAY_XL = 96    # Títulos principais
    DISPLAY_LG = 72    # Títulos grandes
    DISPLAY_MD = 54    # Títulos médios
    DISPLAY_SM = 42    # Títulos pequenos
    
    TEXT_XL = 32       # Texto extra grande
    TEXT_LG = 24       # Texto grande
    TEXT_MD = 18       # Texto médio
    TEXT_SM = 16       # Texto pequeno
    TEXT_XS = 14       # Texto muito pequeno

class ModernSpacing:
    """Sistema de espaçamento moderno (múltiplos de 4px)"""
    
    XS = 4
    SM = 8
    MD = 16
    LG = 24
    XL = 32
    XXL = 48
    XXXL = 64

class GlassmorphismEffect:
    """Sistema de efeitos glassmorphism"""
    
    @staticmethod
    def create_glass_surface(width: int, height: int, 
                           base_color: Tuple[int, int, int, int] = (255, 255, 255, 30),
                           border_radius: int = 16) -> pygame.Surface:
        """Cria uma superfície com efeito glassmorphism"""
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Fundo semi-transparente
        glass_rect = pygame.Rect(0, 0, width, height)
        pygame.draw.rect(surface, base_color, glass_rect, border_radius=border_radius)
        
        # Borda brilhante
        border_color = (255, 255, 255, 80)
        pygame.draw.rect(surface, border_color, glass_rect, 2, border_radius=border_radius)
        
        # Highlight no topo
        highlight_rect = pygame.Rect(2, 2, width - 4, height // 3)
        highlight_color = (255, 255, 255, 20)
        pygame.draw.rect(surface, highlight_color, highlight_rect, 
                        border_radius=border_radius//2)
        
        return surface
    
    @staticmethod
    def create_gradient_surface(width: int, height: int, 
                              colors: List[Tuple[int, int, int]],
                              direction: str = 'vertical') -> pygame.Surface:
        """Cria uma superfície com gradiente suave"""
        surface = pygame.Surface((width, height))
        
        if direction == 'vertical':
            for y in range(height):
                ratio = y / height
                color = GlassmorphismEffect._interpolate_color(colors[0], colors[1], ratio)
                pygame.draw.line(surface, color, (0, y), (width, y))
        else:  # horizontal
            for x in range(width):
                ratio = x / width
                color = GlassmorphismEffect._interpolate_color(colors[0], colors[1], ratio)
                pygame.draw.line(surface, color, (x, 0), (x, height))
        
        return surface
    
    @staticmethod
    def _interpolate_color(color1: Tuple[int, int, int], 
                          color2: Tuple[int, int, int], 
                          ratio: float) -> Tuple[int, int, int]:
        """Interpola entre duas cores"""
        r = int(color1[0] + (color2[0] - color1[0]) * ratio)
        g = int(color1[1] + (color2[1] - color1[1]) * ratio)
        b = int(color1[2] + (color2[2] - color1[2]) * ratio)
        return (r, g, b)

class ModernAnimations:
    """Sistema de animações modernas"""
    
    @staticmethod
    def ease_out_cubic(t: float) -> float:
        """Função de easing suave"""
        return 1 - pow(1 - t, 3)
    
    @staticmethod
    def ease_in_out_cubic(t: float) -> float:
        """Função de easing suave bidirecional"""
        return 4 * t * t * t if t < 0.5 else 1 - pow(-2 * t + 2, 3) / 2
    
    @staticmethod
    def bounce_ease(t: float) -> float:
        """Efeito de bounce suave"""
        if t < 1/2.75:
            return 7.5625 * t * t
        elif t < 2/2.75:
            return 7.5625 * (t - 1.5/2.75) * (t - 1.5/2.75) + 0.75
        elif t < 2.5/2.75:
            return 7.5625 * (t - 2.25/2.75) * (t - 2.25/2.75) + 0.9375
        else:
            return 7.5625 * (t - 2.625/2.75) * (t - 2.625/2.75) + 0.984375

class ParticleSystem:
    """Sistema de partículas avançado"""
    
    def __init__(self):
        self.particles = []
    
    def add_particle(self, x: float, y: float, vel_x: float, vel_y: float,
                    color: Tuple[int, int, int], life: float, size: float):
        """Adiciona uma nova partícula"""
        particle = {
            'x': x,
            'y': y,
            'vel_x': vel_x,
            'vel_y': vel_y,
            'color': color,
            'life': life,
            'max_life': life,
            'size': size,
            'alpha': 255
        }
        self.particles.append(particle)
    
    def update(self, dt: float):
        """Atualiza todas as partículas"""
        for particle in self.particles[:]:
            # Atualiza posição
            particle['x'] += particle['vel_x'] * dt
            particle['y'] += particle['vel_y'] * dt
            
            # Atualiza vida e alpha
            particle['life'] -= dt
            if particle['life'] <= 0:
                self.particles.remove(particle)
                continue
            
            # Fade out
            life_ratio = particle['life'] / particle['max_life']
            particle['alpha'] = int(255 * life_ratio)
    
    def draw(self, surface: pygame.Surface):
        """Desenha todas as partículas"""
        for particle in self.particles:
            if particle['alpha'] > 0:
                # Cria superfície com alpha
                particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), 
                                                pygame.SRCALPHA)
                color_with_alpha = (*particle['color'], particle['alpha'])
                pygame.draw.circle(particle_surface, color_with_alpha,
                                 (particle['size'], particle['size']), particle['size'])
                
                # Blur effect (simplified)
                surface.blit(particle_surface, 
                           (particle['x'] - particle['size'], 
                            particle['y'] - particle['size']),
                           special_flags=pygame.BLEND_ALPHA_SDL2)

class ModernIcons:
    """Sistema de ícones modernos (usando formas geométricas)"""
    
    @staticmethod
    def create_play_icon(size: int, color: Tuple[int, int, int]) -> pygame.Surface:
        """Cria ícone de play moderno"""
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        # Triângulo play
        points = [
            (size * 0.3, size * 0.2),
            (size * 0.3, size * 0.8),
            (size * 0.8, size * 0.5)
        ]
        pygame.draw.polygon(surface, color, points)
        return surface
    
    @staticmethod
    def create_fullscreen_icon(size: int, color: Tuple[int, int, int]) -> pygame.Surface:
        """Cria ícone de tela cheia moderno"""
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Cantos para expand
        corner_size = size // 4
        thickness = max(2, size // 12)
        
        # Canto superior esquerdo
        pygame.draw.rect(surface, color, (2, 2, corner_size, thickness))
        pygame.draw.rect(surface, color, (2, 2, thickness, corner_size))
        
        # Canto superior direito
        pygame.draw.rect(surface, color, (size - corner_size - 2, 2, corner_size, thickness))
        pygame.draw.rect(surface, color, (size - thickness - 2, 2, thickness, corner_size))
        
        # Canto inferior esquerdo
        pygame.draw.rect(surface, color, (2, size - thickness - 2, corner_size, thickness))
        pygame.draw.rect(surface, color, (2, size - corner_size - 2, thickness, corner_size))
        
        # Canto inferior direito
        pygame.draw.rect(surface, color, (size - corner_size - 2, size - thickness - 2, corner_size, thickness))
        pygame.draw.rect(surface, color, (size - thickness - 2, size - corner_size - 2, thickness, corner_size))
        
        return surface
    
    @staticmethod
    def create_credits_icon(size: int, color: Tuple[int, int, int]) -> pygame.Surface:
        """Cria ícone de créditos moderno"""
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Círculo com 'i'
        pygame.draw.circle(surface, color, (size // 2, size // 2), size // 2 - 2, 2)
        
        # Ponto do 'i'
        pygame.draw.circle(surface, color, (size // 2, size // 3), size // 8)
        
        # Linha do 'i'
        pygame.draw.rect(surface, color, 
                        (size // 2 - size // 16, size // 2, size // 8, size // 3))
        
        return surface