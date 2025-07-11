"""
Gerenciador de Transições e Efeitos Visuais
"""
import pygame
import math
from typing import Callable, Optional, Dict, Any
from enum import Enum
from modern_ui_system import modern_ui

class TransitionType(Enum):
    FADE = "fade"
    SLIDE_LEFT = "slide_left"
    SLIDE_RIGHT = "slide_right"
    SLIDE_UP = "slide_up"
    SLIDE_DOWN = "slide_down"
    ZOOM_IN = "zoom_in"
    ZOOM_OUT = "zoom_out"
    CIRCLE_EXPAND = "circle_expand"
    CIRCLE_CONTRACT = "circle_contract"
    PIXELATE = "pixelate"
    BLUR = "blur"

class TransitionState(Enum):
    IDLE = "idle"
    OUT = "out"  # Saindo da tela atual
    IN = "in"    # Entrando na nova tela

class TransitionManager:
    """Gerencia transições suaves entre telas"""
    
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.width, self.height = self.screen.get_size()
        
        # Estado da transição
        self.state = TransitionState.IDLE
        self.transition_type = TransitionType.FADE
        self.duration = 1.0
        self.progress = 0.0
        
        # Superfícies para transição
        self.old_surface = None
        self.new_surface = None
        
        # Callback para quando a transição termina
        self.on_complete: Optional[Callable] = None
        
        # Cache de efeitos
        self.effect_cache = {}
        
        print("🎬 Gerenciador de Transições inicializado!")
    
    def start_transition(self, transition_type: TransitionType, 
                        duration: float = 1.0,
                        on_complete: Optional[Callable] = None):
        """Inicia uma transição"""
        if self.state != TransitionState.IDLE:
            return  # Já está em transição
        
        self.transition_type = transition_type
        self.duration = duration
        self.progress = 0.0
        self.state = TransitionState.OUT
        self.on_complete = on_complete
        
        # Capturar tela atual
        self.old_surface = self.screen.copy()
        
        print(f"🎬 Iniciando transição: {transition_type.value} ({duration}s)")
    
    def set_new_surface(self, surface: pygame.Surface):
        """Define a nova superfície para transição"""
        self.new_surface = surface.copy()
        self.state = TransitionState.IN
    
    def update(self, dt: float) -> bool:
        """Atualiza a transição. Retorna True se ainda está ativa"""
        if self.state == TransitionState.IDLE:
            return False
        
        self.progress += dt / self.duration
        
        if self.progress >= 1.0:
            self.progress = 1.0
            self.complete_transition()
            return False
        
        return True
    
    def complete_transition(self):
        """Completa a transição"""
        self.state = TransitionState.IDLE
        self.progress = 0.0
        self.old_surface = None
        self.new_surface = None
        
        if self.on_complete:
            self.on_complete()
            self.on_complete = None
        
        print("🎬 Transição completa!")
    
    def draw(self, surface: pygame.Surface):
        """Desenha a transição"""
        if self.state == TransitionState.IDLE:
            return
        
        if self.transition_type == TransitionType.FADE:
            self.draw_fade(surface)
        elif self.transition_type == TransitionType.SLIDE_LEFT:
            self.draw_slide(surface, (-1, 0))
        elif self.transition_type == TransitionType.SLIDE_RIGHT:
            self.draw_slide(surface, (1, 0))
        elif self.transition_type == TransitionType.SLIDE_UP:
            self.draw_slide(surface, (0, -1))
        elif self.transition_type == TransitionType.SLIDE_DOWN:
            self.draw_slide(surface, (0, 1))
        elif self.transition_type == TransitionType.ZOOM_IN:
            self.draw_zoom(surface, True)
        elif self.transition_type == TransitionType.ZOOM_OUT:
            self.draw_zoom(surface, False)
        elif self.transition_type == TransitionType.CIRCLE_EXPAND:
            self.draw_circle(surface, True)
        elif self.transition_type == TransitionType.CIRCLE_CONTRACT:
            self.draw_circle(surface, False)
        elif self.transition_type == TransitionType.PIXELATE:
            self.draw_pixelate(surface)
        elif self.transition_type == TransitionType.BLUR:
            self.draw_blur(surface)
    
    def draw_fade(self, surface: pygame.Surface):
        """Desenha transição de fade"""
        if self.state == TransitionState.OUT:
            # Fade out da tela antiga
            if self.old_surface:
                alpha = int(255 * (1 - self.progress))
                self.old_surface.set_alpha(alpha)
                surface.blit(self.old_surface, (0, 0))
        
        elif self.state == TransitionState.IN:
            # Fade in da tela nova
            if self.new_surface:
                alpha = int(255 * self.progress)
                self.new_surface.set_alpha(alpha)
                surface.blit(self.new_surface, (0, 0))
    
    def draw_slide(self, surface: pygame.Surface, direction: tuple):
        """Desenha transição de slide"""
        dx, dy = direction
        
        if self.state == TransitionState.OUT:
            # Slide out da tela antiga
            if self.old_surface:
                offset_x = int(dx * self.width * self.progress)
                offset_y = int(dy * self.height * self.progress)
                surface.blit(self.old_surface, (offset_x, offset_y))
        
        elif self.state == TransitionState.IN:
            # Slide in da tela nova
            if self.new_surface:
                offset_x = int(dx * self.width * (1 - self.progress))
                offset_y = int(dy * self.height * (1 - self.progress))
                surface.blit(self.new_surface, (-offset_x, -offset_y))
    
    def draw_zoom(self, surface: pygame.Surface, zoom_in: bool):
        """Desenha transição de zoom"""
        if self.state == TransitionState.OUT:
            if self.old_surface:
                if zoom_in:
                    # Zoom in: tela fica maior
                    scale = 1 + self.progress * 2
                else:
                    # Zoom out: tela fica menor
                    scale = 1 - self.progress * 0.5
                
                # Redimensionar superfície
                new_width = int(self.width * scale)
                new_height = int(self.height * scale)
                
                if new_width > 0 and new_height > 0:
                    scaled_surface = pygame.transform.scale(
                        self.old_surface, 
                        (new_width, new_height)
                    )
                    
                    # Centralizar
                    x = (self.width - new_width) // 2
                    y = (self.height - new_height) // 2
                    
                    surface.blit(scaled_surface, (x, y))
        
        elif self.state == TransitionState.IN:
            if self.new_surface:
                if zoom_in:
                    scale = 0.5 + self.progress * 0.5
                else:
                    scale = 2 - self.progress * 1
                
                new_width = int(self.width * scale)
                new_height = int(self.height * scale)
                
                if new_width > 0 and new_height > 0:
                    scaled_surface = pygame.transform.scale(
                        self.new_surface,
                        (new_width, new_height)
                    )
                    
                    x = (self.width - new_width) // 2
                    y = (self.height - new_height) // 2
                    
                    surface.blit(scaled_surface, (x, y))
    
    def draw_circle(self, surface: pygame.Surface, expand: bool):
        """Desenha transição circular"""
        center = (self.width // 2, self.height // 2)
        max_radius = int(math.sqrt(self.width**2 + self.height**2) / 2)
        
        if self.state == TransitionState.OUT:
            if self.old_surface:
                surface.blit(self.old_surface, (0, 0))
                
                # Máscara circular
                if expand:
                    radius = int(max_radius * self.progress)
                else:
                    radius = int(max_radius * (1 - self.progress))
                
                # Criar máscara
                mask = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                mask.fill((0, 0, 0, 255))
                pygame.draw.circle(mask, (0, 0, 0, 0), center, radius)
                surface.blit(mask, (0, 0))
        
        elif self.state == TransitionState.IN:
            if self.new_surface:
                # Desenhar nova superfície com máscara circular
                if expand:
                    radius = int(max_radius * self.progress)
                else:
                    radius = int(max_radius * (1 - self.progress))
                
                # Criar superfície com máscara
                masked_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                masked_surface.blit(self.new_surface, (0, 0))
                
                # Aplicar máscara
                mask = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                mask.fill((0, 0, 0, 0))
                pygame.draw.circle(mask, (255, 255, 255, 255), center, radius)
                
                masked_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                surface.blit(masked_surface, (0, 0))
    
    def draw_pixelate(self, surface: pygame.Surface):
        """Desenha transição de pixelização"""
        if self.state == TransitionState.OUT:
            if self.old_surface:
                # Aumentar pixelização
                pixel_size = int(1 + self.progress * 20)
                
                # Reduzir resolução
                small_width = max(1, self.width // pixel_size)
                small_height = max(1, self.height // pixel_size)
                
                # Redimensionar para baixo e depois para cima
                small_surface = pygame.transform.scale(
                    self.old_surface,
                    (small_width, small_height)
                )
                pixelated_surface = pygame.transform.scale(
                    small_surface,
                    (self.width, self.height)
                )
                
                surface.blit(pixelated_surface, (0, 0))
        
        elif self.state == TransitionState.IN:
            if self.new_surface:
                # Diminuir pixelização
                pixel_size = int(20 - self.progress * 19)
                pixel_size = max(1, pixel_size)
                
                small_width = max(1, self.width // pixel_size)
                small_height = max(1, self.height // pixel_size)
                
                small_surface = pygame.transform.scale(
                    self.new_surface,
                    (small_width, small_height)
                )
                pixelated_surface = pygame.transform.scale(
                    small_surface,
                    (self.width, self.height)
                )
                
                surface.blit(pixelated_surface, (0, 0))
    
    def draw_blur(self, surface: pygame.Surface):
        """Desenha transição com blur (simplificado)"""
        if self.state == TransitionState.OUT:
            if self.old_surface:
                # Simular blur com scaling
                blur_amount = int(self.progress * 10)
                if blur_amount > 0:
                    # Criar efeito de blur simples
                    blur_surface = self.old_surface.copy()
                    
                    for i in range(blur_amount):
                        # Reduzir e aumentar várias vezes
                        small_surface = pygame.transform.scale(
                            blur_surface,
                            (max(1, self.width - i * 20), max(1, self.height - i * 20))
                        )
                        blur_surface = pygame.transform.scale(
                            small_surface,
                            (self.width, self.height)
                        )
                    
                    surface.blit(blur_surface, (0, 0))
                else:
                    surface.blit(self.old_surface, (0, 0))
        
        elif self.state == TransitionState.IN:
            if self.new_surface:
                blur_amount = int((1 - self.progress) * 10)
                if blur_amount > 0:
                    blur_surface = self.new_surface.copy()
                    
                    for i in range(blur_amount):
                        small_surface = pygame.transform.scale(
                            blur_surface,
                            (max(1, self.width - i * 20), max(1, self.height - i * 20))
                        )
                        blur_surface = pygame.transform.scale(
                            small_surface,
                            (self.width, self.height)
                        )
                    
                    surface.blit(blur_surface, (0, 0))
                else:
                    surface.blit(self.new_surface, (0, 0))
    
    def create_loading_animation(self, surface: pygame.Surface):
        """Cria animação de loading"""
        colors = modern_ui.get_current_colors()
        center = (self.width // 2, self.height // 2)
        
        # Spinner girando
        angle = pygame.time.get_ticks() * 0.01
        radius = 50
        
        for i in range(8):
            point_angle = angle + i * (math.pi / 4)
            alpha = int(255 * (1 - i / 8))
            
            x = center[0] + int(math.cos(point_angle) * radius)
            y = center[1] + int(math.sin(point_angle) * radius)
            
            color = (*colors.primary, alpha)
            pygame.draw.circle(surface, color, (x, y), 8)
        
        # Texto de loading
        font = pygame.font.Font(None, 36)
        loading_text = font.render("Carregando...", True, colors.text_primary)
        text_rect = loading_text.get_rect(center=(center[0], center[1] + 100))
        surface.blit(loading_text, text_rect)
    
    def is_active(self) -> bool:
        """Verifica se há uma transição ativa"""
        return self.state != TransitionState.IDLE

# Singleton global
transition_manager = TransitionManager()