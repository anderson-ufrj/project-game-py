"""
Sistema de botões interativos para o jogo Icarus
"""
import pygame
from src.config import COLORS, FONTS

class Button:
    def __init__(self, x, y, width, height, text, font_size=FONTS['NORMAL'], 
                 color=COLORS['WHITE'], hover_color=COLORS['LIGHT_BLUE'], 
                 text_color=COLORS['BLACK'], border_color=COLORS['DARK_BLUE']):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font_size = font_size
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_color = border_color
        self.is_hovered = False
        self.is_pressed = False
        
    def handle_event(self, event):
        """Processa eventos do mouse"""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos) and self.is_pressed:
                self.is_pressed = False
                return True  # Botão foi clicado
            self.is_pressed = False
        return False
    
    def draw(self, screen):
        """Desenha o botão na tela"""
        # Cor do fundo baseada no estado
        current_color = self.hover_color if self.is_hovered else self.color
        
        # Desenha o botão com efeito de pressionado
        button_rect = self.rect.copy()
        if self.is_pressed:
            button_rect.x += 2
            button_rect.y += 2
        
        # Desenha o fundo do botão
        pygame.draw.rect(screen, current_color, button_rect)
        pygame.draw.rect(screen, self.border_color, button_rect, 3)
        
        # Desenha o texto centralizado
        font = pygame.font.Font(None, self.font_size)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

class AnimatedButton(Button):
    """Botão com animações suaves"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scale = 1.0
        self.target_scale = 1.0
        
    def handle_event(self, event):
        clicked = super().handle_event(event)
        
        # Animação de hover
        if self.is_hovered:
            self.target_scale = 1.05
        else:
            self.target_scale = 1.0
            
        return clicked
    
    def update(self):
        """Atualiza animações"""
        # Suaviza a transição da escala
        self.scale += (self.target_scale - self.scale) * 0.2
    
    def draw(self, screen):
        """Desenha o botão com animações"""
        # Salva o tamanho original
        original_rect = self.rect.copy()
        
        # Aplica a escala
        center = self.rect.center
        scaled_width = int(self.rect.width * self.scale)
        scaled_height = int(self.rect.height * self.scale)
        self.rect = pygame.Rect(0, 0, scaled_width, scaled_height)
        self.rect.center = center
        
        # Desenha o botão
        super().draw(screen)
        
        # Restaura o tamanho original
        self.rect = original_rect