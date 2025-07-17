"""
Sistema avançado de ícones SVG-style para interface moderna
Cria ícones vetoriais de alta qualidade usando pygame
"""
import pygame
import math
from typing import Tuple, List, Dict, Optional

class AdvancedIconRenderer:
    """Renderizador de ícones vetoriais avançados"""
    
    def __init__(self):
        self.icon_cache = {}
    
    def create_volume_icon(self, size: int, color: Tuple[int, int, int], 
                          level: str = 'high', glow: bool = False) -> pygame.Surface:
        """
        Cria ícone de volume vetorial profissional
        
        Args:
            size: Tamanho do ícone
            color: Cor principal
            level: 'mute', 'low', 'medium', 'high'
            glow: Adicionar efeito de brilho
        """
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        center = size // 2
        
        # Configurações do alto-falante
        speaker_width = size // 5
        speaker_height = int(size // 2.5)
        speaker_x = size // 4
        speaker_y = center - speaker_height // 2
        
        # Corpo do alto-falante com gradiente
        self._draw_gradient_rect(surface, color, 
                               (speaker_x, speaker_y, speaker_width, speaker_height))
        
        # Cone do alto-falante
        cone_points = [
            (speaker_x + speaker_width, speaker_y),
            (speaker_x + speaker_width + size//6, speaker_y - size//8),
            (speaker_x + speaker_width + size//6, speaker_y + speaker_height + size//8),
            (speaker_x + speaker_width, speaker_y + speaker_height)
        ]
        
        # Cone com sombra
        shadow_points = [(p[0]+1, p[1]+1) for p in cone_points]
        pygame.draw.polygon(surface, self._darken_color(color, 0.3), shadow_points)
        pygame.draw.polygon(surface, color, cone_points)
        pygame.draw.polygon(surface, self._lighten_color(color, 0.2), cone_points, 2)
        
        # Ondas sonoras baseadas no nível
        if level != 'mute':
            wave_start_x = speaker_x + speaker_width + size//6 + size//10
            wave_count = {'low': 1, 'medium': 2, 'high': 3}.get(level, 3)
            
            for i in range(wave_count):
                wave_radius = size//6 + i * size//10
                wave_thickness = max(2, size//20)
                
                # Onda com gradiente
                for thickness in range(wave_thickness, 0, -1):
                    alpha = int(255 * (thickness / wave_thickness))
                    wave_color = (*color, alpha)
                    
                    # Arco da onda
                    self._draw_arc_smooth(surface, wave_color, 
                                        (wave_start_x - wave_radius//2, 
                                         center - wave_radius//2, 
                                         wave_radius, wave_radius),
                                        -math.pi/3, math.pi/3, thickness)
                
                # Efeito de brilho nas ondas
                if glow:
                    glow_color = (*color, 50)
                    self._draw_arc_smooth(surface, glow_color,
                                        (wave_start_x - wave_radius//2 - 2, 
                                         center - wave_radius//2 - 2, 
                                         wave_radius + 4, wave_radius + 4),
                                        -math.pi/3, math.pi/3, 1)
        else:
            # X para mute com estilo
            x_size = size // 3
            x_center_x = speaker_x + speaker_width + size//6 + size//10
            x_center_y = center
            
            # Sombra do X
            self._draw_x_mark(surface, self._darken_color(color, 0.5), 
                            (x_center_x+1, x_center_y+1), x_size, size//15)
            
            # X principal
            self._draw_x_mark(surface, color, (x_center_x, x_center_y), x_size, size//15)
            
            # Destaque do X
            self._draw_x_mark(surface, self._lighten_color(color, 0.3), 
                            (x_center_x, x_center_y), x_size, size//20)
        
        return surface
    
    def create_fullscreen_icon(self, size: int, color: Tuple[int, int, int], 
                             is_fullscreen: bool = False, style: str = 'arrows') -> pygame.Surface:
        """
        Cria ícone de fullscreen profissional
        
        Args:
            size: Tamanho do ícone
            color: Cor principal
            is_fullscreen: True para modo windowed, False para fullscreen
            style: 'arrows', 'squares', 'expand'
        """
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        center = size // 2
        
        if style == 'arrows':
            arrow_size = size // 6
            arrow_thickness = max(2, size // 20)
            
            # Posições dos cantos
            corners = [
                (size//4, size//4),           # Superior esquerdo
                (size*3//4, size//4),         # Superior direito
                (size//4, size*3//4),         # Inferior esquerdo
                (size*3//4, size*3//4)        # Inferior direito
            ]
            
            # Direções das setas
            if is_fullscreen:
                # Setas para dentro (windowed)
                directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
            else:
                # Setas para fora (fullscreen)
                directions = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
            
            for (x, y), (dx, dy) in zip(corners, directions):
                # Sombra da seta
                self._draw_arrow(surface, self._darken_color(color, 0.3), 
                               (x+1, y+1), (dx, dy), arrow_size, arrow_thickness)
                
                # Seta principal
                self._draw_arrow(surface, color, (x, y), (dx, dy), arrow_size, arrow_thickness)
                
                # Destaque da seta
                self._draw_arrow(surface, self._lighten_color(color, 0.2), 
                               (x, y), (dx, dy), arrow_size, arrow_thickness//2)
        
        elif style == 'squares':
            # Estilo com quadrados nos cantos
            square_size = size // 8
            gap = size // 6
            
            positions = [
                (gap, gap),                    # Superior esquerdo
                (size - gap - square_size, gap),  # Superior direito
                (gap, size - gap - square_size),  # Inferior esquerdo
                (size - gap - square_size, size - gap - square_size)  # Inferior direito
            ]
            
            for x, y in positions:
                # Sombra
                pygame.draw.rect(surface, self._darken_color(color, 0.3), 
                               (x+1, y+1, square_size, square_size))
                
                # Quadrado principal
                pygame.draw.rect(surface, color, (x, y, square_size, square_size))
                
                # Borda brilhante
                pygame.draw.rect(surface, self._lighten_color(color, 0.3), 
                               (x, y, square_size, square_size), 1)
        
        return surface
    
    def create_settings_icon(self, size: int, color: Tuple[int, int, int], 
                           rotation: float = 0, style: str = 'gear') -> pygame.Surface:
        """
        Cria ícone de configurações profissional
        
        Args:
            size: Tamanho do ícone
            color: Cor principal
            rotation: Rotação em graus
            style: 'gear', 'sliders', 'dots'
        """
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        center = size // 2
        
        if style == 'gear':
            # Engrenagem detalhada
            outer_radius = int(size // 2.5)
            inner_radius = size // 6
            teeth_count = 8
            tooth_height = size // 8
            
            # Pontos da engrenagem
            points = []
            for i in range(teeth_count * 2):
                angle = (2 * math.pi * i / (teeth_count * 2)) + math.radians(rotation)
                
                if i % 2 == 0:
                    # Ponto do dente
                    radius = outer_radius + tooth_height
                else:
                    # Ponto entre dentes
                    radius = outer_radius
                
                x = center + radius * math.cos(angle)
                y = center + radius * math.sin(angle)
                points.append((x, y))
            
            # Sombra da engrenagem
            shadow_points = [(p[0]+2, p[1]+2) for p in points]
            pygame.draw.polygon(surface, self._darken_color(color, 0.5), shadow_points)
            
            # Engrenagem principal
            pygame.draw.polygon(surface, color, points)
            
            # Gradiente interno
            inner_color = self._darken_color(color, 0.2)
            pygame.draw.polygon(surface, inner_color, points, 2)
            
            # Círculo interno (furo)
            pygame.draw.circle(surface, (0, 0, 0, 0), (center, center), inner_radius)
            pygame.draw.circle(surface, self._lighten_color(color, 0.3), 
                             (center, center), inner_radius, 2)
            
            # Parafusos decorativos
            for i in range(4):
                angle = math.pi/2 * i + math.radians(rotation)
                screw_x = center + (outer_radius * 0.7) * math.cos(angle)
                screw_y = center + (outer_radius * 0.7) * math.sin(angle)
                
                pygame.draw.circle(surface, self._darken_color(color, 0.3), 
                                 (int(screw_x), int(screw_y)), size//20)
                pygame.draw.circle(surface, self._lighten_color(color, 0.2), 
                                 (int(screw_x), int(screw_y)), size//20, 1)
        
        elif style == 'sliders':
            # Estilo sliders/equalizador
            slider_count = 3
            slider_width = size // 8
            slider_height = int(size // 1.5)
            spacing = size // 4
            
            for i in range(slider_count):
                x = center - (slider_count-1) * spacing // 2 + i * spacing - slider_width // 2
                y = center - slider_height // 2
                
                # Track do slider
                pygame.draw.rect(surface, self._darken_color(color, 0.3), 
                               (x, y, slider_width, slider_height), border_radius=slider_width//2)
                
                # Handle do slider (posição variável)
                handle_y = y + slider_height // 3 + i * slider_height // 6
                handle_size = int(slider_width * 1.5)
                
                # Sombra do handle
                pygame.draw.circle(surface, self._darken_color(color, 0.5), 
                                 (int(x + slider_width//2 + 1), int(handle_y + 1)), 
                                 int(handle_size//2))
                
                # Handle principal
                pygame.draw.circle(surface, color, 
                                 (int(x + slider_width//2), int(handle_y)), 
                                 int(handle_size//2))
                
                # Destaque do handle
                pygame.draw.circle(surface, self._lighten_color(color, 0.3), 
                                 (int(x + slider_width//2), int(handle_y)), 
                                 int(handle_size//2), 2)
        
        return surface
    
    def _draw_gradient_rect(self, surface: pygame.Surface, color: Tuple[int, int, int], 
                           rect: Tuple[int, int, int, int]):
        """Desenha retângulo com gradiente"""
        x, y, width, height = rect
        
        for i in range(height):
            ratio = i / height
            gradient_color = self._lerp_color(
                self._lighten_color(color, 0.2), 
                self._darken_color(color, 0.2), 
                ratio
            )
            pygame.draw.line(surface, gradient_color, (x, y + i), (x + width, y + i))
    
    def _draw_arc_smooth(self, surface: pygame.Surface, color: Tuple[int, int, int], 
                        rect: Tuple[int, int, int, int], start_angle: float, 
                        end_angle: float, thickness: int):
        """Desenha arco suave"""
        x, y, width, height = rect
        center_x = x + width // 2
        center_y = y + height // 2
        radius = min(width, height) // 2
        
        # Desenhar arco como série de linhas
        angle_step = 0.1
        angle = start_angle
        
        while angle < end_angle:
            next_angle = min(angle + angle_step, end_angle)
            
            start_x = center_x + radius * math.cos(angle)
            start_y = center_y + radius * math.sin(angle)
            end_x = center_x + radius * math.cos(next_angle)
            end_y = center_y + radius * math.sin(next_angle)
            
            pygame.draw.line(surface, color, 
                           (int(start_x), int(start_y)), 
                           (int(end_x), int(end_y)), thickness)
            
            angle = next_angle
    
    def _draw_x_mark(self, surface: pygame.Surface, color: Tuple[int, int, int], 
                    center: Tuple[int, int], size: int, thickness: int):
        """Desenha marca X estilizada"""
        x, y = center
        half_size = size // 2
        
        # Primeira linha do X
        pygame.draw.line(surface, color, 
                        (x - half_size, y - half_size), 
                        (x + half_size, y + half_size), thickness)
        
        # Segunda linha do X
        pygame.draw.line(surface, color, 
                        (x - half_size, y + half_size), 
                        (x + half_size, y - half_size), thickness)
    
    def _draw_arrow(self, surface: pygame.Surface, color: Tuple[int, int, int], 
                   pos: Tuple[int, int], direction: Tuple[int, int], 
                   size: int, thickness: int):
        """Desenha seta estilizada"""
        x, y = pos
        dx, dy = direction
        
        # Linhas da seta
        pygame.draw.line(surface, color, 
                        (x, y), (x + dx * size, y), thickness)
        pygame.draw.line(surface, color, 
                        (x, y), (x, y + dy * size), thickness)
    
    def _lighten_color(self, color: Tuple[int, int, int], factor: float) -> Tuple[int, int, int]:
        """Clareia uma cor"""
        return tuple(min(255, int(c + (255 - c) * factor)) for c in color)
    
    def _darken_color(self, color: Tuple[int, int, int], factor: float) -> Tuple[int, int, int]:
        """Escurece uma cor"""
        return tuple(max(0, int(c * (1 - factor))) for c in color)
    
    def _lerp_color(self, color1: Tuple[int, int, int], color2: Tuple[int, int, int], 
                   t: float) -> Tuple[int, int, int]:
        """Interpola entre duas cores"""
        return tuple(int(c1 + (c2 - c1) * t) for c1, c2 in zip(color1, color2))

# Instância global
advanced_icon_renderer = AdvancedIconRenderer()