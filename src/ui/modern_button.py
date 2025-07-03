"""
Sistema de botões modernos com glassmorphism e animações avançadas
"""
import pygame
import math
from typing import Tuple, Optional, Callable
from src.design_system import (ModernColors, ModernTypography, ModernSpacing, 
                              GlassmorphismEffect, ModernAnimations, ModernIcons)

class ModernButton:
    """Botão moderno com efeitos glassmorphism"""
    
    def __init__(self, x: int, y: int, width: int, height: int, text: str,
                 font_size: int = ModernTypography.TEXT_LG,
                 style: str = 'primary', icon: Optional[str] = None,
                 on_click: Optional[Callable] = None):
        
        self.rect = pygame.Rect(x, y, width, height)
        self.original_rect = self.rect.copy()
        self.text = text
        self.font_size = font_size
        self.style = style
        self.icon = icon
        self.on_click = on_click
        
        # Estados de animação
        self.is_hovered = False
        self.is_pressed = False
        self.is_focused = False
        
        # Propriedades de animação
        self.hover_progress = 0.0
        self.press_progress = 0.0
        self.scale = 1.0
        self.glow_intensity = 0.0
        self.ripple_effects = []
        
        # Cache de superfícies
        self._cached_surfaces = {}
        self._setup_style()
    
    def _setup_style(self):
        """Configura o estilo do botão"""
        styles = {
            'primary': {
                'base_color': ModernColors.GLASS_BLUE,
                'border_color': ModernColors.PRIMARY_BLUE,
                'text_color': ModernColors.NEUTRAL_50,
                'glow_color': ModernColors.PRIMARY_BLUE,
                'gradient': ModernColors.GRADIENT_HERO
            },
            'secondary': {
                'base_color': ModernColors.GLASS_WHITE,
                'border_color': ModernColors.NEUTRAL_300,
                'text_color': ModernColors.NEUTRAL_700,
                'glow_color': ModernColors.NEUTRAL_400,
                'gradient': [ModernColors.NEUTRAL_100, ModernColors.NEUTRAL_200]
            },
            'accent': {
                'base_color': ModernColors.GLASS_PURPLE,
                'border_color': ModernColors.PRIMARY_PURPLE,
                'text_color': ModernColors.NEUTRAL_50,
                'glow_color': ModernColors.PRIMARY_PURPLE,
                'gradient': ModernColors.GRADIENT_ACCENT
            },
            'danger': {
                'base_color': (239, 68, 68, 50),  # Red glass
                'border_color': (239, 68, 68),
                'text_color': ModernColors.NEUTRAL_50,
                'glow_color': (239, 68, 68),
                'gradient': [(239, 68, 68), (220, 38, 127)]
            }
        }
        
        self.button_style = styles.get(self.style, styles['primary'])
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Processa eventos do botão"""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.is_pressed = True
                self._add_ripple_effect(event.pos)
                return False
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.is_pressed:
                self.is_pressed = False
                if self.rect.collidepoint(event.pos):
                    if self.on_click:
                        self.on_click()
                    return True
        
        return False
    
    def _add_ripple_effect(self, click_pos: Tuple[int, int]):
        """Adiciona efeito ripple no clique"""
        local_x = click_pos[0] - self.rect.x
        local_y = click_pos[1] - self.rect.y
        
        ripple = {
            'x': local_x,
            'y': local_y,
            'radius': 0,
            'max_radius': max(self.rect.width, self.rect.height),
            'alpha': 100,
            'time': 0
        }
        self.ripple_effects.append(ripple)
    
    def update(self, dt: float):
        """Atualiza animações do botão"""
        # Animação de hover
        target_hover = 1.0 if self.is_hovered else 0.0
        self.hover_progress += (target_hover - self.hover_progress) * 8 * dt
        
        # Animação de press
        target_press = 1.0 if self.is_pressed else 0.0
        self.press_progress += (target_press - self.press_progress) * 15 * dt
        
        # Escala do botão
        hover_scale = 1.0 + (0.02 * self.hover_progress)
        press_scale = 1.0 - (0.02 * self.press_progress)
        self.scale = hover_scale * press_scale
        
        # Intensidade do glow
        self.glow_intensity = self.hover_progress * 0.5 + self.press_progress * 0.3
        
        # Atualiza posição com escala
        center = self.original_rect.center
        new_width = int(self.original_rect.width * self.scale)
        new_height = int(self.original_rect.height * self.scale)
        self.rect = pygame.Rect(0, 0, new_width, new_height)
        self.rect.center = center
        
        # Atualiza ripples
        for ripple in self.ripple_effects[:]:
            ripple['time'] += dt
            progress = min(ripple['time'] / 0.6, 1.0)  # 600ms duration
            
            ripple['radius'] = ripple['max_radius'] * ModernAnimations.ease_out_cubic(progress)
            ripple['alpha'] = int(100 * (1.0 - progress))
            
            if progress >= 1.0:
                self.ripple_effects.remove(ripple)
    
    def draw(self, surface: pygame.Surface):
        """Desenha o botão com todos os efeitos"""
        # Desenha glow se hover/pressed
        if self.glow_intensity > 0:
            self._draw_glow(surface)
        
        # Desenha o fundo do botão
        self._draw_background(surface)
        
        # Desenha ripples
        self._draw_ripples(surface)
        
        # Desenha ícone e texto
        self._draw_content(surface)
    
    def _draw_glow(self, surface: pygame.Surface):
        """Desenha o efeito glow"""
        glow_size = 20
        glow_rect = self.rect.inflate(glow_size * 2, glow_size * 2)
        
        # Cria superfície para o glow
        glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
        
        # Desenha círculos concêntricos para simular glow
        glow_color = (*self.button_style['glow_color'], int(30 * self.glow_intensity))
        for i in range(glow_size):
            alpha = int((glow_size - i) * 2 * self.glow_intensity)
            if alpha > 0:
                color = (*self.button_style['glow_color'], min(alpha, 255))
                pygame.draw.rect(glow_surface, color, 
                               pygame.Rect(i, i, glow_rect.width - i*2, glow_rect.height - i*2),
                               border_radius=20)
        
        surface.blit(glow_surface, glow_rect.topleft, special_flags=pygame.BLEND_ALPHA_SDL2)
    
    def _draw_background(self, surface: pygame.Surface):
        """Desenha o fundo glassmorphism"""
        # Cria superfície do botão
        button_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        
        # Gradiente de fundo
        gradient_surface = GlassmorphismEffect.create_gradient_surface(
            self.rect.width, self.rect.height, self.button_style['gradient']
        )
        
        # Aplica transparência baseada no hover
        alpha = 30 + int(20 * self.hover_progress)
        gradient_surface.set_alpha(alpha)
        
        # Desenha gradiente
        button_surface.blit(gradient_surface, (0, 0))
        
        # Efeito glassmorphism
        glass_surface = GlassmorphismEffect.create_glass_surface(
            self.rect.width, self.rect.height, self.button_style['base_color']
        )
        button_surface.blit(glass_surface, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
        
        # Borda
        border_alpha = 100 + int(55 * self.hover_progress)
        border_color = (*self.button_style['border_color'], border_alpha)
        pygame.draw.rect(button_surface, border_color, 
                        pygame.Rect(0, 0, self.rect.width, self.rect.height), 
                        2, border_radius=12)
        
        surface.blit(button_surface, self.rect.topleft)
    
    def _draw_ripples(self, surface: pygame.Surface):
        """Desenha efeitos ripple"""
        if not self.ripple_effects:
            return
            
        # Cria clip para o botão
        clip_rect = surface.get_clip()
        surface.set_clip(self.rect)
        
        for ripple in self.ripple_effects:
            if ripple['alpha'] > 0:
                ripple_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
                
                ripple_color = (*ModernColors.NEUTRAL_50, ripple['alpha'])
                pygame.draw.circle(ripple_surface, ripple_color,
                                 (ripple['x'], ripple['y']), int(ripple['radius']))
                
                surface.blit(ripple_surface, self.rect.topleft, 
                           special_flags=pygame.BLEND_ALPHA_SDL2)
        
        surface.set_clip(clip_rect)
    
    def _draw_content(self, surface: pygame.Surface):
        """Desenha ícone e texto"""
        content_rect = self.rect.copy()
        
        # Desenha ícone se existir
        if self.icon:
            icon_size = min(24, self.rect.height // 2)
            icon_surface = self._get_icon_surface(self.icon, icon_size)
            
            if self.text:  # Ícone + texto
                icon_x = content_rect.x + ModernSpacing.MD
                icon_y = content_rect.centery - icon_size // 2
                surface.blit(icon_surface, (icon_x, icon_y))
                content_rect.x += icon_size + ModernSpacing.SM
                content_rect.width -= icon_size + ModernSpacing.SM + ModernSpacing.MD
            else:  # Só ícone
                icon_rect = icon_surface.get_rect(center=content_rect.center)
                surface.blit(icon_surface, icon_rect)
                return
        
        # Desenha texto
        if self.text:
            font = pygame.font.Font(None, self.font_size)
            
            # Sombra do texto
            shadow_color = (0, 0, 0, 100)
            shadow_text = font.render(self.text, True, shadow_color)
            shadow_rect = shadow_text.get_rect(center=(content_rect.centerx + 1, content_rect.centery + 1))
            surface.blit(shadow_text, shadow_rect)
            
            # Texto principal
            text_surface = font.render(self.text, True, self.button_style['text_color'])
            text_rect = text_surface.get_rect(center=content_rect.center)
            surface.blit(text_surface, text_rect)
    
    def _get_icon_surface(self, icon_name: str, size: int) -> pygame.Surface:
        """Obtém superfície do ícone (cacheable)"""
        cache_key = f"{icon_name}_{size}_{self.button_style['text_color']}"
        
        if cache_key not in self._cached_surfaces:
            if icon_name == 'play':
                icon_surface = ModernIcons.create_play_icon(size, self.button_style['text_color'])
            elif icon_name == 'fullscreen':
                icon_surface = ModernIcons.create_fullscreen_icon(size, self.button_style['text_color'])
            elif icon_name == 'credits':
                icon_surface = ModernIcons.create_credits_icon(size, self.button_style['text_color'])
            else:
                # Ícone padrão
                icon_surface = pygame.Surface((size, size), pygame.SRCALPHA)
                pygame.draw.circle(icon_surface, self.button_style['text_color'], 
                                 (size//2, size//2), size//2)
            
            self._cached_surfaces[cache_key] = icon_surface
        
        return self._cached_surfaces[cache_key]

class FloatingActionButton(ModernButton):
    """Botão de ação flutuante (FAB) moderno"""
    
    def __init__(self, x: int, y: int, size: int = 56, icon: str = 'play'):
        super().__init__(x, y, size, size, '', 
                        icon=icon, style='primary')
        self.floating_offset = 0
        self.floating_time = 0
    
    def update(self, dt: float):
        super().update(dt)
        
        # Animação de flutuação
        self.floating_time += dt * 2
        self.floating_offset = math.sin(self.floating_time) * 2
        
        # Atualiza posição
        center = self.original_rect.center
        self.rect.center = (center[0], center[1] + self.floating_offset)
    
    def _draw_background(self, surface: pygame.Surface):
        """FAB tem sombra mais pronunciada"""
        # Desenha sombra
        shadow_offset = 4 + int(2 * self.hover_progress)
        shadow_rect = self.rect.move(shadow_offset, shadow_offset)
        shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        
        # Sombra com blur
        for i in range(8):
            alpha = max(0, 30 - i * 4)
            shadow_color = (0, 0, 0, alpha)
            pygame.draw.ellipse(shadow_surface, shadow_color, 
                              pygame.Rect(i, i, shadow_rect.width - i*2, shadow_rect.height - i*2))
        
        surface.blit(shadow_surface, shadow_rect.topleft, special_flags=pygame.BLEND_ALPHA_SDL2)
        
        # Desenha fundo normal
        super()._draw_background(surface)