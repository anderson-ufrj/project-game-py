"""
Sistema Unificado de UI Moderna
Centraliza todos os elementos de interface com visual moderno e animações
"""
import pygame
import pygame_gui
from typing import Dict, List, Tuple, Optional, Callable
import json
import os
from enum import Enum
from dataclasses import dataclass
import math

class UITheme(Enum):
    DARK = "dark"
    LIGHT = "light"
    CYBERPUNK = "cyberpunk"
    FANTASY = "fantasy"

@dataclass
class UIColors:
    """Cores padronizadas para o tema"""
    primary: Tuple[int, int, int]
    secondary: Tuple[int, int, int]
    accent: Tuple[int, int, int]
    background: Tuple[int, int, int]
    surface: Tuple[int, int, int]
    text_primary: Tuple[int, int, int]
    text_secondary: Tuple[int, int, int]
    success: Tuple[int, int, int]
    warning: Tuple[int, int, int]
    error: Tuple[int, int, int]

class ModernUISystem:
    """Sistema principal de UI moderna"""
    
    # Singleton
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
            
        self._initialized = True
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        
        # Configurações
        self.current_theme = UITheme.DARK
        self.animations_enabled = True
        self.transition_speed = 0.3
        
        # Cores dos temas
        self.themes = {
            UITheme.DARK: UIColors(
                primary=(52, 152, 219),      # Azul vibrante
                secondary=(46, 204, 113),    # Verde esmeralda
                accent=(155, 89, 182),       # Roxo
                background=(30, 30, 40),     # Fundo escuro
                surface=(45, 45, 60),        # Superfície
                text_primary=(255, 255, 255),
                text_secondary=(180, 180, 190),
                success=(46, 204, 113),
                warning=(241, 196, 15),
                error=(231, 76, 60)
            ),
            UITheme.LIGHT: UIColors(
                primary=(41, 128, 185),
                secondary=(39, 174, 96),
                accent=(142, 68, 173),
                background=(245, 245, 250),
                surface=(255, 255, 255),
                text_primary=(30, 30, 40),
                text_secondary=(100, 100, 110),
                success=(39, 174, 96),
                warning=(243, 156, 18),
                error=(192, 57, 43)
            ),
            UITheme.CYBERPUNK: UIColors(
                primary=(0, 255, 255),       # Cyan neon
                secondary=(255, 0, 255),     # Magenta neon
                accent=(255, 255, 0),        # Amarelo neon
                background=(10, 10, 20),
                surface=(20, 20, 35),
                text_primary=(255, 255, 255),
                text_secondary=(150, 150, 170),
                success=(0, 255, 128),
                warning=(255, 128, 0),
                error=(255, 0, 128)
            ),
            UITheme.FANTASY: UIColors(
                primary=(212, 175, 55),      # Dourado
                secondary=(143, 45, 86),     # Vinho
                accent=(64, 130, 109),       # Verde musgo
                background=(25, 20, 30),
                surface=(40, 35, 45),
                text_primary=(255, 248, 220),
                text_secondary=(200, 190, 170),
                success=(64, 130, 109),
                warning=(212, 175, 55),
                error=(143, 45, 86)
            )
        }
        
        # Manager do Pygame GUI
        self.manager = None
        self.setup_pygame_gui()
        
        # Cache de superfícies
        self.surface_cache = {}
        
        # Animações ativas
        self.active_animations = []
        
        # Callbacks
        self.callbacks = {}
        
        print("🎨 Sistema de UI Moderna inicializado!")
    
    def setup_pygame_gui(self):
        """Configura o Pygame GUI com tema customizado"""
        # Criar tema base
        theme_dict = self.create_theme_dict()
        
        # Salvar tema temporariamente
        theme_path = 'temp_theme.json'
        with open(theme_path, 'w') as f:
            json.dump(theme_dict, f, indent=2)
        
        # Inicializar manager
        if self.screen:
            self.manager = pygame_gui.UIManager(
                self.screen.get_size(),
                theme_path
            )
        
        # Remover arquivo temporário
        if os.path.exists(theme_path):
            os.remove(theme_path)
    
    def create_theme_dict(self) -> dict:
        """Cria dicionário de tema para Pygame GUI"""
        colors = self.get_current_colors()
        
        return {
            "defaults": {
                "colours": {
                    "normal_bg": f"#{colors.surface[0]:02x}{colors.surface[1]:02x}{colors.surface[2]:02x}",
                    "hovered_bg": f"#{colors.primary[0]:02x}{colors.primary[1]:02x}{colors.primary[2]:02x}",
                    "disabled_bg": f"#{colors.background[0]:02x}{colors.background[1]:02x}{colors.background[2]:02x}",
                    "selected_bg": f"#{colors.accent[0]:02x}{colors.accent[1]:02x}{colors.accent[2]:02x}",
                    "normal_text": f"#{colors.text_primary[0]:02x}{colors.text_primary[1]:02x}{colors.text_primary[2]:02x}",
                    "hovered_text": f"#{colors.text_primary[0]:02x}{colors.text_primary[1]:02x}{colors.text_primary[2]:02x}",
                    "selected_text": f"#{colors.text_primary[0]:02x}{colors.text_primary[1]:02x}{colors.text_primary[2]:02x}",
                    "disabled_text": f"#{colors.text_secondary[0]:02x}{colors.text_secondary[1]:02x}{colors.text_secondary[2]:02x}",
                },
                "misc": {
                    "shape": "rounded_rectangle",
                    "shape_corner_radius": "10",
                    "border_width": "2",
                    "shadow_width": "2",
                    "text_horiz_alignment": "center",
                    "text_vert_alignment": "center"
                }
            },
            "button": {
                "colours": {
                    "normal_border": f"#{colors.primary[0]:02x}{colors.primary[1]:02x}{colors.primary[2]:02x}",
                    "hovered_border": f"#{colors.accent[0]:02x}{colors.accent[1]:02x}{colors.accent[2]:02x}",
                },
                "misc": {
                    "border_width": "2",
                    "shadow_width": "3",
                    "shape_corner_radius": "8"
                }
            },
            "horizontal_slider": {
                "colours": {
                    "normal_bg": f"#{colors.background[0]:02x}{colors.background[1]:02x}{colors.background[2]:02x}",
                    "sliding_button": f"#{colors.primary[0]:02x}{colors.primary[1]:02x}{colors.primary[2]:02x}",
                    "filled_bar": f"#{colors.secondary[0]:02x}{colors.secondary[1]:02x}{colors.secondary[2]:02x}"
                },
                "misc": {
                    "sliding_button_width": "20",
                    "border_width": "1",
                    "shadow_width": "0"
                }
            }
        }
    
    def get_current_colors(self) -> UIColors:
        """Retorna as cores do tema atual"""
        return self.themes[self.current_theme]
    
    def set_theme(self, theme: UITheme):
        """Muda o tema da UI"""
        self.current_theme = theme
        self.setup_pygame_gui()
        print(f"🎨 Tema alterado para: {theme.value}")
    
    def create_gradient_surface(self, size: Tuple[int, int], 
                              color1: Tuple[int, int, int], 
                              color2: Tuple[int, int, int],
                              vertical: bool = True) -> pygame.Surface:
        """Cria uma superfície com gradiente"""
        cache_key = f"gradient_{size}_{color1}_{color2}_{vertical}"
        
        if cache_key in self.surface_cache:
            return self.surface_cache[cache_key]
        
        surface = pygame.Surface(size, pygame.SRCALPHA)
        
        if vertical:
            for y in range(size[1]):
                ratio = y / size[1]
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                pygame.draw.line(surface, (r, g, b), (0, y), (size[0], y))
        else:
            for x in range(size[0]):
                ratio = x / size[0]
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                pygame.draw.line(surface, (r, g, b), (x, 0), (x, size[1]))
        
        self.surface_cache[cache_key] = surface
        return surface
    
    def create_glow_surface(self, size: Tuple[int, int], 
                          color: Tuple[int, int, int], 
                          intensity: float = 1.0) -> pygame.Surface:
        """Cria superfície com efeito glow"""
        surface = pygame.Surface(size, pygame.SRCALPHA)
        center = (size[0] // 2, size[1] // 2)
        max_radius = max(size) // 2
        
        for radius in range(max_radius, 0, -2):
            alpha = int(255 * intensity * (1 - radius / max_radius))
            color_with_alpha = (*color, alpha)
            pygame.draw.circle(surface, color_with_alpha, center, radius)
        
        return surface
    
    def draw_modern_button(self, surface: pygame.Surface, 
                         rect: pygame.Rect, 
                         text: str, 
                         hovered: bool = False,
                         clicked: bool = False,
                         disabled: bool = False) -> pygame.Rect:
        """Desenha um botão moderno com efeitos"""
        colors = self.get_current_colors()
        
        # Determinar cores baseadas no estado
        if disabled:
            bg_color = colors.background
            text_color = colors.text_secondary
            border_color = colors.surface
        elif clicked:
            bg_color = colors.accent
            text_color = colors.text_primary
            border_color = colors.accent
        elif hovered:
            bg_color = colors.primary
            text_color = colors.text_primary
            border_color = colors.primary
        else:
            bg_color = colors.surface
            text_color = colors.text_primary
            border_color = colors.primary
        
        # Criar gradiente de fundo
        gradient = self.create_gradient_surface(
            (rect.width, rect.height),
            bg_color,
            tuple(max(0, c - 30) for c in bg_color)
        )
        
        # Aplicar sombra
        if not disabled:
            shadow_rect = rect.copy()
            shadow_rect.x += 2
            shadow_rect.y += 2
            pygame.draw.rect(surface, (0, 0, 0, 50), shadow_rect, border_radius=10)
        
        # Desenhar botão
        button_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        button_surface.blit(gradient, (0, 0))
        
        # Borda
        pygame.draw.rect(button_surface, border_color, 
                        pygame.Rect(0, 0, rect.width, rect.height), 
                        width=2, border_radius=10)
        
        # Efeito glow se hover
        if hovered and not disabled:
            glow = self.create_glow_surface((rect.width + 20, rect.height + 20), border_color, 0.3)
            surface.blit(glow, (rect.x - 10, rect.y - 10))
        
        surface.blit(button_surface, rect)
        
        # Texto
        font = pygame.font.Font(None, 24)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)
        
        return rect
    
    def draw_modern_slider(self, surface: pygame.Surface,
                         rect: pygame.Rect,
                         value: float,
                         min_val: float = 0,
                         max_val: float = 100,
                         label: str = "") -> float:
        """Desenha um slider moderno"""
        colors = self.get_current_colors()
        
        # Background do slider
        bg_rect = pygame.Rect(rect.x, rect.y + rect.height//2 - 4, rect.width, 8)
        pygame.draw.rect(surface, colors.background, bg_rect, border_radius=4)
        
        # Barra preenchida
        fill_width = int((value - min_val) / (max_val - min_val) * rect.width)
        if fill_width > 0:
            fill_rect = pygame.Rect(rect.x, rect.y + rect.height//2 - 4, fill_width, 8)
            gradient = self.create_gradient_surface(
                (fill_width, 8),
                colors.secondary,
                colors.primary,
                vertical=False
            )
            surface.blit(gradient, fill_rect)
        
        # Handle do slider
        handle_x = rect.x + fill_width
        handle_rect = pygame.Rect(handle_x - 10, rect.y, 20, rect.height)
        
        # Sombra do handle
        shadow_rect = handle_rect.copy()
        shadow_rect.x += 1
        shadow_rect.y += 1
        pygame.draw.circle(surface, (0, 0, 0, 30), shadow_rect.center, 12)
        
        # Handle com gradiente
        pygame.draw.circle(surface, colors.primary, handle_rect.center, 10)
        pygame.draw.circle(surface, colors.accent, handle_rect.center, 8)
        
        # Label e valor
        if label:
            font = pygame.font.Font(None, 20)
            label_text = font.render(f"{label}: {int(value)}", True, colors.text_primary)
            surface.blit(label_text, (rect.x, rect.y - 25))
        
        return value
    
    def create_notification(self, message: str, 
                          notification_type: str = "info",
                          duration: float = 3.0) -> Dict:
        """Cria uma notificação toast moderna"""
        colors = self.get_current_colors()
        
        # Determinar cor baseada no tipo
        type_colors = {
            "success": colors.success,
            "warning": colors.warning,
            "error": colors.error,
            "info": colors.primary
        }
        
        notification = {
            "message": message,
            "type": notification_type,
            "color": type_colors.get(notification_type, colors.primary),
            "duration": duration,
            "start_time": pygame.time.get_ticks(),
            "y_offset": 0,
            "alpha": 0
        }
        
        self.active_animations.append(notification)
        return notification
    
    def update_animations(self, dt: float):
        """Atualiza todas as animações ativas"""
        current_time = pygame.time.get_ticks()
        
        # Atualizar notificações
        for i, notif in enumerate(self.active_animations[:]):
            elapsed = (current_time - notif["start_time"]) / 1000.0
            
            # Fade in
            if elapsed < 0.3:
                notif["alpha"] = min(255, int(255 * (elapsed / 0.3)))
                notif["y_offset"] = 20 * (1 - elapsed / 0.3)
            # Visível
            elif elapsed < notif["duration"] - 0.3:
                notif["alpha"] = 255
                notif["y_offset"] = 0
            # Fade out
            elif elapsed < notif["duration"]:
                remaining = notif["duration"] - elapsed
                notif["alpha"] = int(255 * (remaining / 0.3))
                notif["y_offset"] = -20 * (1 - remaining / 0.3)
            else:
                self.active_animations.remove(notif)
    
    def draw_notifications(self, surface: pygame.Surface):
        """Desenha todas as notificações ativas"""
        y_start = 50
        
        for notif in self.active_animations:
            # Criar superfície da notificação
            font = pygame.font.Font(None, 24)
            text = font.render(notif["message"], True, (255, 255, 255))
            
            # Background com transparência
            padding = 20
            notif_width = text.get_width() + padding * 2
            notif_height = text.get_height() + padding
            
            notif_surface = pygame.Surface((notif_width, notif_height), pygame.SRCALPHA)
            
            # Gradiente de fundo
            gradient = self.create_gradient_surface(
                (notif_width, notif_height),
                notif["color"],
                tuple(max(0, c - 50) for c in notif["color"])
            )
            gradient.set_alpha(notif["alpha"])
            notif_surface.blit(gradient, (0, 0))
            
            # Borda
            border_color = (*notif["color"], notif["alpha"])
            pygame.draw.rect(notif_surface, border_color, 
                           pygame.Rect(0, 0, notif_width, notif_height),
                           width=2, border_radius=8)
            
            # Texto
            text.set_alpha(notif["alpha"])
            notif_surface.blit(text, (padding, padding // 2))
            
            # Posição centralizada
            x = (surface.get_width() - notif_width) // 2
            y = y_start + notif["y_offset"]
            
            surface.blit(notif_surface, (x, y))
            y_start += notif_height + 10
    
    def process_event(self, event: pygame.event.Event) -> bool:
        """Processa eventos para o sistema de UI"""
        if self.manager:
            self.manager.process_events(event)
        
        # Processar callbacks customizados
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                button_id = event.ui_element.get_object_id()
                if button_id in self.callbacks:
                    self.callbacks[button_id]()
                    return True
        
        return False
    
    def update(self, dt: float):
        """Atualiza o sistema de UI"""
        if self.manager:
            self.manager.update(dt)
        
        self.update_animations(dt)
    
    def draw(self, surface: pygame.Surface):
        """Desenha todos os elementos de UI"""
        if self.manager:
            self.manager.draw_ui(surface)
        
        self.draw_notifications(surface)

# Singleton global
modern_ui = ModernUISystem()