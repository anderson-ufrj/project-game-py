import pygame
import math
import time
from typing import Tuple, List, Optional, Callable
from font_manager import font_manager

class UITheme:
    """Sistema de temas para interface moderna"""
    
    # Cores principais
    PRIMARY = (64, 128, 255)      # Azul principal
    SECONDARY = (128, 64, 255)    # Roxo secundário
    SUCCESS = (64, 255, 128)      # Verde sucesso
    WARNING = (255, 192, 64)      # Amarelo aviso
    DANGER = (255, 64, 64)        # Vermelho perigo
    
    # Cores de fundo
    BG_DARK = (20, 20, 25)        # Fundo escuro
    BG_MEDIUM = (35, 35, 40)      # Fundo médio
    BG_LIGHT = (50, 50, 60)       # Fundo claro
    
    # Cores de texto
    TEXT_PRIMARY = (255, 255, 255)    # Texto principal
    TEXT_SECONDARY = (200, 200, 220)  # Texto secundário
    TEXT_MUTED = (150, 150, 170)      # Texto desabilitado
    
    # Efeitos
    GLOW_COLOR = (255, 255, 255, 100)
    SHADOW_COLOR = (0, 0, 0, 150)
    
    # Gradientes
    @staticmethod
    def get_gradient_colors(color_start: Tuple[int, int, int], 
                          color_end: Tuple[int, int, int], 
                          steps: int) -> List[Tuple[int, int, int]]:
        """Gera gradiente entre duas cores"""
        colors = []
        for i in range(steps):
            ratio = i / (steps - 1)
            r = int(color_start[0] + (color_end[0] - color_start[0]) * ratio)
            g = int(color_start[1] + (color_end[1] - color_start[1]) * ratio)
            b = int(color_start[2] + (color_end[2] - color_start[2]) * ratio)
            colors.append((r, g, b))
        return colors

class UIComponent:
    """Classe base para todos os componentes UI"""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True
        self.enabled = True
        self.hover = False
        self.animations = {}
        
    def update(self, mouse_pos: Tuple[int, int]) -> None:
        """Atualiza o componente"""
        self.hover = self.rect.collidepoint(mouse_pos) if self.enabled else False
        self._update_animations()
        
    def _update_animations(self) -> None:
        """Atualiza animações do componente"""
        current_time = time.time()
        for anim_name, anim_data in list(self.animations.items()):
            elapsed = current_time - anim_data['start_time']
            if elapsed >= anim_data['duration']:
                self.animations.pop(anim_name)
            else:
                progress = elapsed / anim_data['duration']
                anim_data['current_value'] = self._ease_animation(
                    anim_data['start_value'], 
                    anim_data['end_value'], 
                    progress, 
                    anim_data['easing']
                )
    
    def _ease_animation(self, start: float, end: float, progress: float, easing: str) -> float:
        """Aplica easing a animação"""
        if easing == 'ease_out':
            progress = 1 - (1 - progress) ** 2
        elif easing == 'ease_in':
            progress = progress ** 2
        elif easing == 'ease_in_out':
            progress = 3 * progress ** 2 - 2 * progress ** 3
        elif easing == 'bounce':
            if progress < 0.5:
                progress = 2 * progress ** 2
            else:
                progress = 1 - 2 * (1 - progress) ** 2
        
        return start + (end - start) * progress
    
    def animate(self, property_name: str, end_value: float, duration: float = 0.3, easing: str = 'ease_out') -> None:
        """Inicia uma animação"""
        current_value = getattr(self, property_name, 0)
        self.animations[property_name] = {
            'start_value': current_value,
            'end_value': end_value,
            'current_value': current_value,
            'duration': duration,
            'start_time': time.time(),
            'easing': easing
        }
    
    def draw(self, surface: pygame.Surface) -> None:
        """Desenha o componente (deve ser implementado pelas subclasses)"""
        pass

class ModernButton(UIComponent):
    """Botão moderno com efeitos visuais avançados"""
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 text: str, font_size: str = 'button', 
                 color: Tuple[int, int, int] = UITheme.PRIMARY,
                 text_color: Tuple[int, int, int] = UITheme.TEXT_PRIMARY,
                 on_click: Optional[Callable] = None):
        super().__init__(x, y, width, height)
        self.text = text
        self.font = font_manager.get(font_size)
        self.color = color
        self.text_color = text_color
        self.on_click = on_click
        
        # Estados visuais
        self.glow_intensity = 0
        self.scale = 1.0
        self.pressed = False
        
    def handle_click(self, mouse_pos: Tuple[int, int]) -> bool:
        """Manipula clique do mouse"""
        if self.rect.collidepoint(mouse_pos) and self.enabled:
            self.pressed = True
            self.animate('scale', 0.95, 0.1, 'ease_in')
            if self.on_click:
                self.on_click()
            return True
        return False
    
    def update(self, mouse_pos: Tuple[int, int]) -> None:
        super().update(mouse_pos)
        
        # Animações baseadas no estado
        target_glow = 50 if self.hover else 0
        target_scale = 1.05 if self.hover and not self.pressed else 1.0
        
        if abs(self.glow_intensity - target_glow) > 1:
            self.glow_intensity += (target_glow - self.glow_intensity) * 0.1
        
        if 'scale' not in self.animations:
            if abs(self.scale - target_scale) > 0.01:
                self.scale += (target_scale - self.scale) * 0.1
        else:
            self.scale = self.animations['scale']['current_value']
        
        self.pressed = False
    
    def draw(self, surface: pygame.Surface) -> None:
        if not self.visible:
            return
        
        # Calcular posição e tamanho com escala
        scaled_width = int(self.rect.width * self.scale)
        scaled_height = int(self.rect.height * self.scale)
        scaled_x = self.rect.centerx - scaled_width // 2
        scaled_y = self.rect.centery - scaled_height // 2
        scaled_rect = pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)
        
        # Sombra
        shadow_offset = 4
        shadow_rect = pygame.Rect(scaled_x + shadow_offset, scaled_y + shadow_offset, 
                                scaled_width, scaled_height)
        shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, UITheme.SHADOW_COLOR, 
                        (0, 0, shadow_rect.width, shadow_rect.height), border_radius=8)
        surface.blit(shadow_surface, shadow_rect.topleft)
        
        # Brilho (glow)
        if self.glow_intensity > 0:
            glow_size = 6
            glow_rect = pygame.Rect(scaled_x - glow_size, scaled_y - glow_size,
                                  scaled_width + 2 * glow_size, scaled_height + 2 * glow_size)
            glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            glow_color = (*self.color, int(self.glow_intensity))
            pygame.draw.rect(glow_surface, glow_color,
                           (0, 0, glow_rect.width, glow_rect.height), border_radius=12)
            surface.blit(glow_surface, glow_rect.topleft)
        
        # Fundo do botão com gradiente
        button_surface = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
        
        # Gradiente de cima para baixo
        gradient_colors = UITheme.get_gradient_colors(
            tuple(min(255, c + 30) for c in self.color),
            tuple(max(0, c - 30) for c in self.color),
            scaled_height
        )
        
        for i, color in enumerate(gradient_colors):
            pygame.draw.rect(button_surface, color, (0, i, scaled_width, 1))
        
        # Borda
        pygame.draw.rect(button_surface, tuple(min(255, c + 50) for c in self.color),
                        (0, 0, scaled_width, scaled_height), 2, border_radius=8)
        
        surface.blit(button_surface, scaled_rect.topleft)
        
        # Texto
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=scaled_rect.center)
        
        # Sombra do texto
        text_shadow = self.font.render(self.text, True, (0, 0, 0))
        surface.blit(text_shadow, (text_rect.x + 1, text_rect.y + 1))
        surface.blit(text_surface, text_rect)

class ModernSlider(UIComponent):
    """Slider moderno com efeitos visuais"""
    
    def __init__(self, x: int, y: int, width: int, height: int,
                 min_value: float = 0.0, max_value: float = 1.0, 
                 initial_value: float = 0.5,
                 color: Tuple[int, int, int] = UITheme.PRIMARY,
                 on_change: Optional[Callable] = None):
        super().__init__(x, y, width, height)
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.color = color
        self.on_change = on_change
        
        # Estados visuais
        self.handle_glow = 0
        self.track_glow = 0
        self.dragging = False
        
    def handle_click(self, mouse_pos: Tuple[int, int]) -> bool:
        """Manipula clique do mouse"""
        if self.rect.collidepoint(mouse_pos) and self.enabled:
            # Calcular novo valor baseado na posição do mouse
            relative_x = mouse_pos[0] - self.rect.x
            self.value = self.min_value + (relative_x / self.rect.width) * (self.max_value - self.min_value)
            self.value = max(self.min_value, min(self.max_value, self.value))
            
            if self.on_change:
                self.on_change(self.value)
            
            self.dragging = True
            return True
        return False
    
    def handle_drag(self, mouse_pos: Tuple[int, int]) -> None:
        """Manipula arraste do mouse"""
        if self.dragging and self.enabled:
            relative_x = mouse_pos[0] - self.rect.x
            self.value = self.min_value + (relative_x / self.rect.width) * (self.max_value - self.min_value)
            self.value = max(self.min_value, min(self.max_value, self.value))
            
            if self.on_change:
                self.on_change(self.value)
    
    def handle_release(self) -> None:
        """Manipula soltar o mouse"""
        self.dragging = False
    
    def update(self, mouse_pos: Tuple[int, int]) -> None:
        super().update(mouse_pos)
        
        # Verificar se o mouse está sobre o handle
        handle_x = self.rect.x + int((self.value - self.min_value) / (self.max_value - self.min_value) * self.rect.width)
        handle_rect = pygame.Rect(handle_x - 12, self.rect.centery - 12, 24, 24)
        handle_hover = handle_rect.collidepoint(mouse_pos)
        
        # Animações
        target_handle_glow = 60 if (handle_hover or self.dragging) else 0
        target_track_glow = 30 if self.hover else 0
        
        self.handle_glow += (target_handle_glow - self.handle_glow) * 0.1
        self.track_glow += (target_track_glow - self.track_glow) * 0.1
    
    def draw(self, surface: pygame.Surface) -> None:
        if not self.visible:
            return
        
        # Track (trilha)
        track_rect = pygame.Rect(self.rect.x, self.rect.centery - 4, self.rect.width, 8)
        
        # Fundo do track
        pygame.draw.rect(surface, UITheme.BG_DARK, track_rect, border_radius=4)
        
        # Brilho do track
        if self.track_glow > 0:
            glow_rect = pygame.Rect(track_rect.x - 2, track_rect.y - 2, 
                                  track_rect.width + 4, track_rect.height + 4)
            glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            glow_color = (*self.color, int(self.track_glow))
            pygame.draw.rect(glow_surface, glow_color, 
                           (0, 0, glow_rect.width, glow_rect.height), border_radius=6)
            surface.blit(glow_surface, glow_rect.topleft)
        
        # Preenchimento do track
        fill_width = int((self.value - self.min_value) / (self.max_value - self.min_value) * self.rect.width)
        if fill_width > 0:
            fill_rect = pygame.Rect(self.rect.x, self.rect.centery - 4, fill_width, 8)
            
            # Gradiente no preenchimento
            gradient_colors = UITheme.get_gradient_colors(
                self.color,
                tuple(max(0, c - 40) for c in self.color),
                8
            )
            
            for i, color in enumerate(gradient_colors):
                line_rect = pygame.Rect(fill_rect.x, fill_rect.y + i, fill_rect.width, 1)
                pygame.draw.rect(surface, color, line_rect)
        
        # Handle (alça)
        handle_x = self.rect.x + int((self.value - self.min_value) / (self.max_value - self.min_value) * self.rect.width)
        handle_center = (handle_x, self.rect.centery)
        
        # Brilho do handle
        if self.handle_glow > 0:
            glow_radius = 18
            glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            glow_color = (*UITheme.TEXT_PRIMARY, int(self.handle_glow))
            pygame.draw.circle(glow_surface, glow_color, (glow_radius, glow_radius), glow_radius)
            surface.blit(glow_surface, (handle_x - glow_radius, self.rect.centery - glow_radius))
        
        # Handle principal
        pygame.draw.circle(surface, UITheme.BG_LIGHT, handle_center, 10)
        pygame.draw.circle(surface, UITheme.TEXT_PRIMARY, handle_center, 8)
        pygame.draw.circle(surface, self.color, handle_center, 6)
        
        # Valor no handle
        if self.dragging or self.hover:
            value_text = font_manager.get('small').render(f"{int(self.value * 100)}", True, UITheme.TEXT_PRIMARY)
            value_rect = value_text.get_rect(center=(handle_x, self.rect.centery - 25))
            
            # Background do valor
            bg_rect = pygame.Rect(value_rect.x - 5, value_rect.y - 2, value_rect.width + 10, value_rect.height + 4)
            pygame.draw.rect(surface, UITheme.BG_DARK, bg_rect, border_radius=4)
            surface.blit(value_text, value_rect)

class ModernPanel(UIComponent):
    """Painel moderno com efeitos visuais"""
    
    def __init__(self, x: int, y: int, width: int, height: int,
                 title: str = "", 
                 background_color: Tuple[int, int, int] = UITheme.BG_MEDIUM,
                 border_color: Tuple[int, int, int] = UITheme.PRIMARY):
        super().__init__(x, y, width, height)
        self.title = title
        self.background_color = background_color
        self.border_color = border_color
        self.border_glow = 0
        
    def update(self, mouse_pos: Tuple[int, int]) -> None:
        super().update(mouse_pos)
        
        # Animação da borda
        target_glow = 50 if self.hover else 20
        self.border_glow += (target_glow - self.border_glow) * 0.05
    
    def draw(self, surface: pygame.Surface) -> None:
        if not self.visible:
            return
        
        # Sombra
        shadow_offset = 6
        shadow_rect = pygame.Rect(self.rect.x + shadow_offset, self.rect.y + shadow_offset,
                                self.rect.width, self.rect.height)
        shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, UITheme.SHADOW_COLOR,
                        (0, 0, shadow_rect.width, shadow_rect.height), border_radius=12)
        surface.blit(shadow_surface, shadow_rect.topleft)
        
        # Brilho da borda
        if self.border_glow > 0:
            glow_rect = pygame.Rect(self.rect.x - 3, self.rect.y - 3,
                                  self.rect.width + 6, self.rect.height + 6)
            glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            glow_color = (*self.border_color, int(self.border_glow))
            pygame.draw.rect(glow_surface, glow_color,
                           (0, 0, glow_rect.width, glow_rect.height), border_radius=15)
            surface.blit(glow_surface, glow_rect.topleft)
        
        # Fundo do painel
        pygame.draw.rect(surface, self.background_color, self.rect, border_radius=12)
        
        # Borda
        pygame.draw.rect(surface, self.border_color, self.rect, 3, border_radius=12)
        
        # Título
        if self.title:
            title_font = font_manager.get('subtitle')
            title_surface = title_font.render(self.title, True, UITheme.TEXT_PRIMARY)
            title_rect = title_surface.get_rect(centerx=self.rect.centerx, y=self.rect.y + 15)
            
            # Sombra do título
            title_shadow = title_font.render(self.title, True, (0, 0, 0))
            surface.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))
            surface.blit(title_surface, title_rect)

# Sistema de gerenciamento de UI
class UIManager:
    """Gerenciador central para todos os componentes UI"""
    
    def __init__(self):
        self.components = []
        self.mouse_pos = (0, 0)
        self.mouse_pressed = False
        self.last_mouse_pressed = False
        
    def add_component(self, component: UIComponent) -> None:
        """Adiciona um componente à lista"""
        self.components.append(component)
    
    def remove_component(self, component: UIComponent) -> None:
        """Remove um componente da lista"""
        if component in self.components:
            self.components.remove(component)
    
    def clear_components(self) -> None:
        """Remove todos os componentes"""
        self.components.clear()
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Manipula eventos para todos os componentes"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_pressed = True
            # Processar cliques em ordem reversa (componentes de cima primeiro)
            for component in reversed(self.components):
                if isinstance(component, (ModernButton, ModernSlider)):
                    if component.handle_click(self.mouse_pos):
                        return True
                        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_pressed = False
            # Soltar sliders
            for component in self.components:
                if isinstance(component, ModernSlider):
                    component.handle_release()
                    
        elif event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
            # Arrastar sliders APENAS se estiverem sendo arrastados
            for component in self.components:
                if isinstance(component, ModernSlider) and component.dragging:
                    component.handle_drag(self.mouse_pos)
        
        self.last_mouse_pressed = self.mouse_pressed
        return False
    
    def update(self) -> None:
        """Atualiza todos os componentes"""
        for component in self.components:
            component.update(self.mouse_pos)
    
    def draw(self, surface: pygame.Surface) -> None:
        """Desenha todos os componentes"""
        for component in self.components:
            component.draw(surface)

# Instância global do gerenciador UI
ui_manager = UIManager()