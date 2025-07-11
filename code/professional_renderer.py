import pygame
import numpy as np
import math
import time
from typing import Tuple, Optional, List, Dict, Any
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from font_manager import font_manager

class AdvancedRenderer:
    """Sistema de renderização profissional com efeitos avançados"""
    
    def __init__(self):
        # Cache para otimização
        self.surface_cache = {}
        self.font_cache = {}
        
        # Configurações de qualidade
        self.anti_aliasing = True
        self.high_quality = True
        self.blur_radius = 2
        
        # Cores profissionais
        self.theme = {
            'primary': (74, 144, 226),
            'secondary': (108, 92, 231),
            'success': (56, 178, 172),
            'warning': (255, 193, 7),
            'danger': (220, 53, 69),
            'dark': (33, 37, 41),
            'light': (248, 249, 250),
            'text_primary': (33, 37, 41),
            'text_secondary': (108, 117, 125),
            'text_muted': (173, 181, 189)
        }
    
    def create_rounded_surface(self, width: int, height: int, radius: int, 
                             color: Tuple[int, int, int], alpha: int = 255) -> pygame.Surface:
        """Cria surface com cantos arredondados usando anti-aliasing"""
        cache_key = f"rounded_{width}_{height}_{radius}_{color}_{alpha}"
        
        if cache_key in self.surface_cache:
            return self.surface_cache[cache_key].copy()
        
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Simplificar - sempre usar pygame nativo para compatibilidade
        if radius > 0:
            # Desenhar retângulo com cantos arredondados
            pygame.draw.rect(surface, (*color, alpha), (radius, 0, width-2*radius, height))
            pygame.draw.rect(surface, (*color, alpha), (0, radius, width, height-2*radius))
            
            # Cantos arredondados
            pygame.draw.circle(surface, (*color, alpha), (radius, radius), radius)
            pygame.draw.circle(surface, (*color, alpha), (width-radius, radius), radius)
            pygame.draw.circle(surface, (*color, alpha), (radius, height-radius), radius)
            pygame.draw.circle(surface, (*color, alpha), (width-radius, height-radius), radius)
        else:
            # Retângulo simples se radius for 0
            pygame.draw.rect(surface, (*color, alpha), (0, 0, width, height))
        
        self.surface_cache[cache_key] = surface.copy()
        return surface
    
    def render_text_professional(self, text: str, font_size: str, color: Tuple[int, int, int],
                                background: Optional[Tuple[int, int, int]] = None,
                                shadow: bool = True, glow: bool = False,
                                anti_alias: bool = True) -> Tuple[pygame.Surface, pygame.Rect]:
        """Renderiza texto com qualidade profissional"""
        
        cache_key = f"text_{text}_{font_size}_{color}_{background}_{shadow}_{glow}_{anti_alias}"
        
        if cache_key in self.surface_cache:
            cached_surface = self.surface_cache[cache_key]
            return cached_surface.copy(), cached_surface.get_rect()
        
        font = font_manager.get(font_size)
        
        # Renderizar texto base com anti-aliasing
        base_surface = font.render(text, anti_alias, color)
        width, height = base_surface.get_size()
        
        # Criar surface expandida para efeitos
        padding = 10 if (shadow or glow) else 0
        final_width = width + padding * 2
        final_height = height + padding * 2
        
        final_surface = pygame.Surface((final_width, final_height), pygame.SRCALPHA)
        
        # Background se especificado
        if background:
            bg_surface = self.create_rounded_surface(
                final_width, final_height, 8, background, 200
            )
            final_surface.blit(bg_surface, (0, 0))
        
        # Sombra
        if shadow:
            shadow_surface = font.render(text, anti_alias, (0, 0, 0))
            shadow_surface.set_alpha(100)
            final_surface.blit(shadow_surface, (padding + 2, padding + 2))
        
        # Glow effect
        if glow:
            glow_color = tuple(min(255, c + 100) for c in color)
            for offset in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
                glow_surface = font.render(text, anti_alias, glow_color)
                glow_surface.set_alpha(50)
                final_surface.blit(glow_surface, (padding + offset[0], padding + offset[1]))
        
        # Texto principal
        final_surface.blit(base_surface, (padding, padding))
        
        # Cache do resultado
        self.surface_cache[cache_key] = final_surface.copy()
        
        return final_surface, final_surface.get_rect()
    
    def create_gradient_surface(self, width: int, height: int, 
                              color_start: Tuple[int, int, int],
                              color_end: Tuple[int, int, int],
                              direction: str = 'vertical') -> pygame.Surface:
        """Cria surface com gradiente profissional"""
        
        cache_key = f"gradient_{width}_{height}_{color_start}_{color_end}_{direction}"
        
        if cache_key in self.surface_cache:
            return self.surface_cache[cache_key].copy()
        
        surface = pygame.Surface((width, height))
        
        if direction == 'vertical':
            for y in range(height):
                ratio = y / height
                r = int(color_start[0] + (color_end[0] - color_start[0]) * ratio)
                g = int(color_start[1] + (color_end[1] - color_start[1]) * ratio)
                b = int(color_start[2] + (color_end[2] - color_start[2]) * ratio)
                pygame.draw.line(surface, (r, g, b), (0, y), (width, y))
        else:  # horizontal
            for x in range(width):
                ratio = x / width
                r = int(color_start[0] + (color_end[0] - color_start[0]) * ratio)
                g = int(color_start[1] + (color_end[1] - color_start[1]) * ratio)
                b = int(color_start[2] + (color_end[2] - color_start[2]) * ratio)
                pygame.draw.line(surface, (r, g, b), (x, 0), (x, height))
        
        self.surface_cache[cache_key] = surface.copy()
        return surface
    
    def apply_blur_effect(self, surface: pygame.Surface, radius: int = 2) -> pygame.Surface:
        """Aplica efeito de blur usando PIL"""
        if not self.high_quality or radius <= 0:
            return surface
        
        # Converter para PIL
        w, h = surface.get_size()
        raw = pygame.surfarray.array3d(surface)
        pil_image = Image.fromarray(raw.swapaxes(0, 1))
        
        # Aplicar blur
        blurred = pil_image.filter(ImageFilter.GaussianBlur(radius=radius))
        
        # Converter de volta
        blurred_array = np.array(blurred)
        blurred_surface = pygame.surfarray.make_surface(blurred_array.swapaxes(0, 1))
        
        return blurred_surface
    
    def create_professional_button(self, width: int, height: int, text: str,
                                 font_size: str = 'button',
                                 style: str = 'primary',
                                 state: str = 'normal') -> pygame.Surface:
        """Cria botão com visual profissional"""
        
        # Cores baseadas no estilo
        if style == 'primary':
            base_color = self.theme['primary']
        elif style == 'success':
            base_color = self.theme['success']
        elif style == 'warning':
            base_color = self.theme['warning']
        elif style == 'danger':
            base_color = self.theme['danger']
        else:
            base_color = self.theme['secondary']
        
        # Modificar cor baseado no estado
        if state == 'hover':
            base_color = tuple(min(255, c + 30) for c in base_color)
        elif state == 'pressed':
            base_color = tuple(max(0, c - 30) for c in base_color)
        
        # Criar fundo com gradiente
        gradient_start = tuple(min(255, c + 20) for c in base_color)
        gradient_end = tuple(max(0, c - 20) for c in base_color)
        
        button_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Fundo com gradiente
        gradient = self.create_gradient_surface(width, height, gradient_start, gradient_end)
        
        # Máscara para cantos arredondados
        rounded_mask = self.create_rounded_surface(width, height, 12, (255, 255, 255))
        
        # Aplicar máscara ao gradiente
        gradient.blit(rounded_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        button_surface.blit(gradient, (0, 0))
        
        # Borda
        border_surface = self.create_rounded_surface(width, height, 12, base_color, 0)
        pygame.draw.rect(border_surface, base_color, (0, 0, width, height), 2, border_radius=12)
        button_surface.blit(border_surface, (0, 0))
        
        # Texto
        text_color = (255, 255, 255) if sum(base_color) < 400 else (0, 0, 0)
        text_surface, text_rect = self.render_text_professional(
            text, font_size, text_color, shadow=True, anti_alias=True
        )
        
        # Centralizar texto
        text_x = (width - text_rect.width) // 2
        text_y = (height - text_rect.height) // 2
        button_surface.blit(text_surface, (text_x, text_y))
        
        return button_surface
    
    def create_modern_panel(self, width: int, height: int, title: str = "",
                           background_alpha: int = 200) -> pygame.Surface:
        """Cria painel moderno com visual profissional"""
        
        panel_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Fundo com gradiente sutil
        bg_gradient = self.create_gradient_surface(
            width, height,
            (45, 45, 55), (35, 35, 45)
        )
        
        # Aplicar transparência e cantos arredondados
        bg_rounded = self.create_rounded_surface(width, height, 15, (255, 255, 255))
        bg_gradient.blit(bg_rounded, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        bg_gradient.set_alpha(background_alpha)
        panel_surface.blit(bg_gradient, (0, 0))
        
        # Borda com brilho sutil
        border_color = self.theme['primary']
        border_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(border_surface, border_color, (0, 0, width, height), 3, border_radius=15)
        border_surface.set_alpha(150)
        panel_surface.blit(border_surface, (0, 0))
        
        # Título se especificado
        if title:
            title_surface, title_rect = self.render_text_professional(
                title, 'subtitle', (255, 255, 255), glow=True, anti_alias=True
            )
            title_x = (width - title_rect.width) // 2
            panel_surface.blit(title_surface, (title_x, 20))
        
        return panel_surface
    
    def create_health_bar(self, width: int, height: int, current: float, maximum: float,
                         bar_color: Tuple[int, int, int] = None) -> pygame.Surface:
        """Cria barra de vida moderna"""
        
        if bar_color is None:
            # Cor baseada na porcentagem
            percentage = current / maximum
            if percentage > 0.6:
                bar_color = self.theme['success']
            elif percentage > 0.3:
                bar_color = self.theme['warning']
            else:
                bar_color = self.theme['danger']
        
        bar_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Fundo da barra
        bg_surface = self.create_rounded_surface(width, height, height//2, (60, 60, 60))
        bar_surface.blit(bg_surface, (0, 0))
        
        # Preenchimento
        fill_width = int((current / maximum) * width)
        if fill_width > 0:
            # Gradiente no preenchimento
            fill_gradient = self.create_gradient_surface(
                fill_width, height,
                tuple(min(255, c + 40) for c in bar_color),
                tuple(max(0, c - 20) for c in bar_color)
            )
            
            fill_rounded = self.create_rounded_surface(fill_width, height, height//2, (255, 255, 255))
            fill_gradient.blit(fill_rounded, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            bar_surface.blit(fill_gradient, (0, 0))
        
        # Borda brilhante
        border_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(border_surface, (255, 255, 255), (0, 0, width, height), 2, border_radius=height//2)
        border_surface.set_alpha(100)
        bar_surface.blit(border_surface, (0, 0))
        
        return bar_surface
    
    def clear_cache(self):
        """Limpa cache para liberar memória"""
        self.surface_cache.clear()
        self.font_cache.clear()

# Instância global do renderizador profissional
professional_renderer = AdvancedRenderer()