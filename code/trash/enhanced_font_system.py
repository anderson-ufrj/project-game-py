import pygame
import math
import time
from typing import Tuple, Optional, List
from font_manager import font_manager

class TextEffect:
    """Sistema de efeitos visuais para texto"""
    
    @staticmethod
    def render_with_shadow(font: pygame.font.Font, text: str, color: Tuple[int, int, int],
                          shadow_color: Tuple[int, int, int] = (0, 0, 0),
                          shadow_offset: Tuple[int, int] = (2, 2)) -> Tuple[pygame.Surface, pygame.Rect]:
        """Renderiza texto com sombra"""
        # Renderizar sombra
        shadow_surface = font.render(text, True, shadow_color)
        
        # Renderizar texto principal
        text_surface = font.render(text, True, color)
        
        # Criar surface combinada
        combined_width = text_surface.get_width() + abs(shadow_offset[0])
        combined_height = text_surface.get_height() + abs(shadow_offset[1])
        combined_surface = pygame.Surface((combined_width, combined_height), pygame.SRCALPHA)
        
        # Posicionar sombra
        shadow_x = max(0, shadow_offset[0])
        shadow_y = max(0, shadow_offset[1])
        combined_surface.blit(shadow_surface, (shadow_x, shadow_y))
        
        # Posicionar texto principal
        text_x = max(0, -shadow_offset[0])
        text_y = max(0, -shadow_offset[1])
        combined_surface.blit(text_surface, (text_x, text_y))
        
        # Criar rect para posicionamento
        rect = combined_surface.get_rect()
        
        return combined_surface, rect
    
    @staticmethod
    def render_with_glow(font: pygame.font.Font, text: str, color: Tuple[int, int, int],
                        glow_color: Tuple[int, int, int] = (255, 255, 255),
                        glow_radius: int = 3) -> Tuple[pygame.Surface, pygame.Rect]:
        """Renderiza texto com efeito de brilho"""
        # Renderizar texto principal
        text_surface = font.render(text, True, color)
        
        # Criar surface para o brilho
        glow_size = glow_radius * 2
        combined_width = text_surface.get_width() + glow_size
        combined_height = text_surface.get_height() + glow_size
        combined_surface = pygame.Surface((combined_width, combined_height), pygame.SRCALPHA)
        
        # Criar múltiplas camadas de brilho
        for i in range(glow_radius, 0, -1):
            alpha = int(50 * (1 - i / glow_radius))
            glow_surface = font.render(text, True, (*glow_color, alpha))
            
            # Desenhar brilho em múltiplas posições
            for x_offset in range(-i, i + 1):
                for y_offset in range(-i, i + 1):
                    if x_offset == 0 and y_offset == 0:
                        continue
                    combined_surface.blit(glow_surface, 
                                        (glow_radius + x_offset, glow_radius + y_offset))
        
        # Desenhar texto principal no centro
        combined_surface.blit(text_surface, (glow_radius, glow_radius))
        
        rect = combined_surface.get_rect()
        return combined_surface, rect
    
    @staticmethod
    def render_with_outline(font: pygame.font.Font, text: str, color: Tuple[int, int, int],
                           outline_color: Tuple[int, int, int] = (0, 0, 0),
                           outline_width: int = 2) -> Tuple[pygame.Surface, pygame.Rect]:
        """Renderiza texto com contorno"""
        # Renderizar texto principal
        text_surface = font.render(text, True, color)
        
        # Criar surface para o contorno
        outline_size = outline_width * 2
        combined_width = text_surface.get_width() + outline_size
        combined_height = text_surface.get_height() + outline_size
        combined_surface = pygame.Surface((combined_width, combined_height), pygame.SRCALPHA)
        
        # Renderizar contorno
        outline_surface = font.render(text, True, outline_color)
        
        # Desenhar contorno em múltiplas posições
        for x_offset in range(-outline_width, outline_width + 1):
            for y_offset in range(-outline_width, outline_width + 1):
                if x_offset == 0 and y_offset == 0:
                    continue
                combined_surface.blit(outline_surface, 
                                    (outline_width + x_offset, outline_width + y_offset))
        
        # Desenhar texto principal no centro
        combined_surface.blit(text_surface, (outline_width, outline_width))
        
        rect = combined_surface.get_rect()
        return combined_surface, rect
    
    @staticmethod
    def render_gradient_text(font: pygame.font.Font, text: str, 
                           color_start: Tuple[int, int, int],
                           color_end: Tuple[int, int, int]) -> Tuple[pygame.Surface, pygame.Rect]:
        """Renderiza texto com gradiente vertical"""
        # Renderizar texto base
        text_surface = font.render(text, True, (255, 255, 255))
        width, height = text_surface.get_size()
        
        # Criar surface para gradiente
        gradient_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Criar gradiente linha por linha
        for y in range(height):
            ratio = y / height
            r = int(color_start[0] + (color_end[0] - color_start[0]) * ratio)
            g = int(color_start[1] + (color_end[1] - color_start[1]) * ratio)
            b = int(color_start[2] + (color_end[2] - color_start[2]) * ratio)
            
            # Criar linha colorida
            line_surface = pygame.Surface((width, 1), pygame.SRCALPHA)
            line_surface.fill((r, g, b, 255))
            
            # Aplicar máscara do texto
            line_surface.blit(text_surface.subsurface(0, y, width, 1), (0, 0), 
                            special_flags=pygame.BLEND_RGBA_MULT)
            
            gradient_surface.blit(line_surface, (0, y))
        
        rect = gradient_surface.get_rect()
        return gradient_surface, rect

class AnimatedText:
    """Classe para texto animado"""
    
    def __init__(self, text: str, font_size: str, color: Tuple[int, int, int],
                 x: int, y: int, effect_type: str = "none"):
        self.text = text
        self.font = font_manager.get(font_size)
        self.color = color
        self.x = x
        self.y = y
        self.effect_type = effect_type
        self.start_time = time.time()
        
        # Propriedades de animação
        self.alpha = 255
        self.scale = 1.0
        self.rotation = 0
        self.wave_offset = 0
        
    def update(self) -> None:
        """Atualiza a animação do texto"""
        current_time = time.time()
        elapsed = current_time - self.start_time
        
        if self.effect_type == "fade_in":
            self.alpha = min(255, int(elapsed * 255))
        elif self.effect_type == "pulse":
            self.scale = 1.0 + 0.1 * math.sin(elapsed * 4)
        elif self.effect_type == "wave":
            self.wave_offset = elapsed * 2
        elif self.effect_type == "rotate":
            self.rotation = elapsed * 90  # 90 graus por segundo
    
    def draw(self, surface: pygame.Surface) -> None:
        """Desenha o texto animado"""
        if self.effect_type == "wave":
            self._draw_wave_text(surface)
        else:
            self._draw_normal_text(surface)
    
    def _draw_normal_text(self, surface: pygame.Surface) -> None:
        """Desenha texto normal com transformações"""
        text_surface = self.font.render(self.text, True, self.color)
        
        # Aplicar alpha
        if self.alpha < 255:
            text_surface.set_alpha(self.alpha)
        
        # Aplicar escala
        if self.scale != 1.0:
            scaled_width = int(text_surface.get_width() * self.scale)
            scaled_height = int(text_surface.get_height() * self.scale)
            text_surface = pygame.transform.scale(text_surface, (scaled_width, scaled_height))
        
        # Aplicar rotação
        if self.rotation != 0:
            text_surface = pygame.transform.rotate(text_surface, self.rotation)
        
        # Posicionar e desenhar
        rect = text_surface.get_rect(center=(self.x, self.y))
        surface.blit(text_surface, rect)
    
    def _draw_wave_text(self, surface: pygame.Surface) -> None:
        """Desenha texto com efeito de onda"""
        for i, char in enumerate(self.text):
            if char == ' ':
                continue
            
            char_surface = self.font.render(char, True, self.color)
            
            # Calcular posição da onda
            char_x = self.x + i * 20  # Espaçamento entre caracteres
            char_y = self.y + math.sin(self.wave_offset + i * 0.5) * 10
            
            # Aplicar alpha
            if self.alpha < 255:
                char_surface.set_alpha(self.alpha)
            
            surface.blit(char_surface, (char_x, char_y))

class EnhancedFontRenderer:
    """Sistema avançado de renderização de fontes"""
    
    def __init__(self):
        self.cached_surfaces = {}
        self.animated_texts = []
    
    def render_title(self, text: str, x: int, y: int, surface: pygame.Surface,
                    color: Tuple[int, int, int] = (255, 255, 255),
                    effect: str = "glow") -> pygame.Rect:
        """Renderiza título com efeitos especiais"""
        font = font_manager.get('title')
        
        if effect == "glow":
            text_surface, rect = TextEffect.render_with_glow(
                font, text, color, (255, 215, 0), 4
            )
        elif effect == "outline":
            text_surface, rect = TextEffect.render_with_outline(
                font, text, color, (0, 0, 0), 3
            )
        elif effect == "gradient":
            text_surface, rect = TextEffect.render_gradient_text(
                font, text, (255, 215, 0), (255, 165, 0)
            )
        else:
            text_surface, rect = TextEffect.render_with_shadow(font, text, color)
        
        rect.center = (x, y)
        surface.blit(text_surface, rect)
        return rect
    
    def render_subtitle(self, text: str, x: int, y: int, surface: pygame.Surface,
                       color: Tuple[int, int, int] = (200, 200, 255)) -> pygame.Rect:
        """Renderiza subtítulo com sombra suave"""
        font = font_manager.get('subtitle')
        text_surface, rect = TextEffect.render_with_shadow(
            font, text, color, (0, 0, 0), (2, 2)
        )
        rect.center = (x, y)
        surface.blit(text_surface, rect)
        return rect
    
    def render_body_text(self, text: str, x: int, y: int, surface: pygame.Surface,
                        color: Tuple[int, int, int] = (220, 220, 220),
                        max_width: Optional[int] = None) -> List[pygame.Rect]:
        """Renderiza texto do corpo com quebra de linha automática"""
        font = font_manager.get('text')
        
        if max_width is None:
            # Texto simples sem quebra
            text_surface, rect = TextEffect.render_with_shadow(font, text, color)
            rect.topleft = (x, y)
            surface.blit(text_surface, rect)
            return [rect]
        
        # Quebra de linha automática
        words = text.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
        
        # Renderizar cada linha
        rects = []
        line_height = font.get_height() + 5
        
        for i, line in enumerate(lines):
            text_surface, rect = TextEffect.render_with_shadow(font, line, color)
            rect.topleft = (x, y + i * line_height)
            surface.blit(text_surface, rect)
            rects.append(rect)
        
        return rects
    
    def render_instruction(self, text: str, x: int, y: int, surface: pygame.Surface,
                          color: Tuple[int, int, int] = (160, 180, 200)) -> pygame.Rect:
        """Renderiza texto de instrução com efeito sutil"""
        font = font_manager.get('small')
        text_surface, rect = TextEffect.render_with_outline(
            font, text, color, (0, 0, 0), 1
        )
        rect.center = (x, y)
        surface.blit(text_surface, rect)
        return rect
    
    def add_animated_text(self, text: str, font_size: str, color: Tuple[int, int, int],
                         x: int, y: int, effect_type: str = "fade_in") -> None:
        """Adiciona texto animado à lista"""
        animated_text = AnimatedText(text, font_size, color, x, y, effect_type)
        self.animated_texts.append(animated_text)
    
    def update_animations(self) -> None:
        """Atualiza todas as animações de texto"""
        for animated_text in self.animated_texts:
            animated_text.update()
    
    def draw_animations(self, surface: pygame.Surface) -> None:
        """Desenha todos os textos animados"""
        for animated_text in self.animated_texts:
            animated_text.draw(surface)
    
    def clear_animations(self) -> None:
        """Remove todas as animações"""
        self.animated_texts.clear()
    
    def render_ui_panel_text(self, title: str, content: List[str], 
                           x: int, y: int, width: int, surface: pygame.Surface) -> pygame.Rect:
        """Renderiza um painel de texto formatado"""
        panel_height = 60  # Header
        line_height = font_manager.get('text').get_height() + 3
        panel_height += len(content) * line_height + 20  # Content + padding
        
        # Fundo do painel
        panel_rect = pygame.Rect(x, y, width, panel_height)
        
        # Gradiente de fundo
        for i in range(panel_height):
            alpha = int(150 * (1 - i / panel_height))
            color = (20, 20, 30, alpha)
            line_surface = pygame.Surface((width, 1), pygame.SRCALPHA)
            line_surface.fill(color)
            surface.blit(line_surface, (x, y + i))
        
        # Borda
        pygame.draw.rect(surface, (100, 120, 150), panel_rect, 2, border_radius=8)
        
        # Título
        self.render_subtitle(title, x + width // 2, y + 25, surface)
        
        # Conteúdo
        content_y = y + 50
        for line in content:
            self.render_body_text(line, x + 15, content_y, surface, max_width=width - 30)
            content_y += line_height
        
        return panel_rect

# Instância global do renderizador avançado
enhanced_font_renderer = EnhancedFontRenderer()