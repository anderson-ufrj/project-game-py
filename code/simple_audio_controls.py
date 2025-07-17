import pygame
import math
from audio_manager import audio_manager
from font_manager import font_manager

class SimpleAudioControls:
    """Controles de áudio simples e estáticos para música e efeitos separados"""
    
    def __init__(self):
        # Posicionamento dos controles
        self.controls_visible = False
        self.background_rect = None
        
        # Posições dos elementos (serão calculadas na primeira renderização)
        self.music_icon_rect = None
        self.sfx_icon_rect = None
        self.music_slider_rect = None
        self.sfx_slider_rect = None
        self.music_mute_rect = None
        self.sfx_mute_rect = None
        self.toggle_button_rect = None
        
        # Estado de interação
        self.dragging_music = False
        self.dragging_sfx = False
        
        # Cores modernizadas
        self.colors = {
            'background': (25, 25, 35, 220),
            'background_gradient': (35, 35, 45, 180),
            'border': (120, 140, 160),
            'border_active': (180, 200, 220),
            'slider_track': (50, 50, 70),
            'slider_fill': (70, 130, 200),
            'slider_fill_bright': (100, 160, 255),
            'slider_handle': (140, 180, 240),
            'slider_handle_hover': (160, 200, 255),
            'text': (255, 255, 255),
            'text_shadow': (0, 0, 0),
            'muted': (255, 120, 120),
            'active': (120, 255, 120),
            'icon_normal': (200, 200, 220),
            'icon_muted': (255, 100, 100),
            'glow': (100, 150, 255)
        }
        
        # Estado de hover para efeitos visuais
        self.hover_states = {
            'music_slider': False,
            'sfx_slider': False,
            'music_mute': False,
            'sfx_mute': False,
            'toggle': False
        }
    
    def toggle_visibility(self):
        """Alterna a visibilidade dos controles"""
        self.controls_visible = not self.controls_visible
    
    def _calculate_positions(self, screen_width, screen_height):
        """Calcula as posições dos elementos na tela"""
        if self.background_rect is not None:
            return  # Já calculado
        
        # Painel principal (canto superior direito)
        panel_width = 280
        panel_height = 140
        panel_x = screen_width - panel_width - 20
        panel_y = 20
        
        self.background_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        
        # Botão de toggle (ícone de som estático)
        toggle_size = 30
        self.toggle_button_rect = pygame.Rect(
            screen_width - toggle_size - 10, 10, toggle_size, toggle_size
        )
        
        # Linha 1: Música
        music_y = panel_y + 20
        self.music_icon_rect = pygame.Rect(panel_x + 10, music_y, 20, 20)
        self.music_slider_rect = pygame.Rect(panel_x + 40, music_y + 2, 150, 16)
        self.music_mute_rect = pygame.Rect(panel_x + 200, music_y, 60, 20)
        
        # Linha 2: Efeitos
        sfx_y = music_y + 40
        self.sfx_icon_rect = pygame.Rect(panel_x + 10, sfx_y, 20, 20)
        self.sfx_slider_rect = pygame.Rect(panel_x + 40, sfx_y + 2, 150, 16)
        self.sfx_mute_rect = pygame.Rect(panel_x + 200, sfx_y, 60, 20)
    
    def handle_event(self, event, screen_width, screen_height):
        """Processa eventos de mouse e teclado"""
        self._calculate_positions(screen_width, screen_height)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clique esquerdo
                mouse_pos = event.pos
                
                # Toggle do painel
                if self.toggle_button_rect.collidepoint(mouse_pos):
                    self.toggle_visibility()
                    return True
                
                if not self.controls_visible:
                    return False
                
                # Botões mute
                if self.music_mute_rect.collidepoint(mouse_pos):
                    audio_manager.toggle_music_mute()
                    return True
                elif self.sfx_mute_rect.collidepoint(mouse_pos):
                    audio_manager.toggle_sfx_mute()
                    return True
                
                # Sliders
                elif self.music_slider_rect.collidepoint(mouse_pos):
                    self._handle_slider_click(mouse_pos, 'music')
                    self.dragging_music = True
                    return True
                elif self.sfx_slider_rect.collidepoint(mouse_pos):
                    self._handle_slider_click(mouse_pos, 'sfx')
                    self.dragging_sfx = True
                    return True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging_music = False
                self.dragging_sfx = False
        
        elif event.type == pygame.MOUSEMOTION:
            if self.controls_visible:
                mouse_pos = event.pos
                if self.dragging_music:
                    self._handle_slider_click(mouse_pos, 'music')
                    return True
                elif self.dragging_sfx:
                    self._handle_slider_click(mouse_pos, 'sfx')
                    return True
        
        elif event.type == pygame.KEYDOWN:
            # Atalhos de teclado
            if event.key == pygame.K_m:
                audio_manager.toggle_music_mute()
                return True
            elif event.key == pygame.K_n:  # N para efeitos sonoros
                audio_manager.toggle_sfx_mute()
                return True
            elif event.key == pygame.K_UP:
                if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                    # Shift + Up = aumentar efeitos
                    new_volume = min(1.0, audio_manager.sfx_volume + 0.1)
                    audio_manager.set_sfx_volume(new_volume)
                else:
                    # Up = aumentar música
                    new_volume = min(1.0, audio_manager.music_volume + 0.1)
                    audio_manager.set_music_volume(new_volume)
                return True
            elif event.key == pygame.K_DOWN:
                if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                    # Shift + Down = diminuir efeitos
                    new_volume = max(0.0, audio_manager.sfx_volume - 0.1)
                    audio_manager.set_sfx_volume(new_volume)
                else:
                    # Down = diminuir música
                    new_volume = max(0.0, audio_manager.music_volume - 0.1)
                    audio_manager.set_music_volume(new_volume)
                return True
        
        return False
    
    def _handle_slider_click(self, mouse_pos, slider_type):
        """Processa clique nos sliders"""
        if slider_type == 'music':
            slider_rect = self.music_slider_rect
        else:
            slider_rect = self.sfx_slider_rect
        
        # Calcular novo valor baseado na posição do mouse
        relative_x = mouse_pos[0] - slider_rect.x
        relative_x = max(0, min(slider_rect.width, relative_x))
        new_value = relative_x / slider_rect.width
        
        # Aplicar novo volume
        if slider_type == 'music':
            audio_manager.set_music_volume(new_value)
        else:
            audio_manager.set_sfx_volume(new_value)
    
    def draw(self, surface):
        """Desenha os controles na tela"""
        screen_width = surface.get_width()
        screen_height = surface.get_height()
        self._calculate_positions(screen_width, screen_height)
        
        # Desenhar botão de toggle (sempre visível)
        self._draw_toggle_button(surface)
        
        # Desenhar painel se visível
        if self.controls_visible:
            self._draw_audio_panel(surface)
    
    def _create_gradient_surface(self, width, height, color1, color2, vertical=True):
        """Cria uma superfície com gradiente"""
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        
        if vertical:
            for y in range(height):
                ratio = y / height
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                a = int(color1[3] * (1 - ratio) + color2[3] * ratio) if len(color1) > 3 else 255
                pygame.draw.line(surface, (r, g, b, a), (0, y), (width, y))
        else:
            for x in range(width):
                ratio = x / width
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                a = int(color1[3] * (1 - ratio) + color2[3] * ratio) if len(color1) > 3 else 255
                pygame.draw.line(surface, (r, g, b, a), (x, 0), (x, height))
        
        return surface
    
    def _draw_glow_effect(self, surface, rect, color, intensity=0.5):
        """Desenha efeito glow ao redor de um retângulo"""
        glow_surface = pygame.Surface((rect.width + 20, rect.height + 20), pygame.SRCALPHA)
        
        for i in range(5, 0, -1):
            alpha = int(50 * intensity * (i / 5))
            glow_color = (*color[:3], alpha)
            glow_rect = pygame.Rect(10 - i, 10 - i, rect.width + i*2, rect.height + i*2)
            pygame.draw.rect(glow_surface, glow_color, glow_rect, border_radius=8)
        
        surface.blit(glow_surface, (rect.x - 10, rect.y - 10))

    def _draw_toggle_button(self, surface):
        """Desenha o ícone de som estático com efeitos modernos"""
        rect = self.toggle_button_rect
        
        # Efeito glow se ativo
        if self.controls_visible:
            self._draw_glow_effect(surface, rect, self.colors['glow'], 0.6)
        
        # Fundo com gradiente
        gradient_color1 = self.colors['background']
        gradient_color2 = self.colors['background_gradient']
        
        if self.controls_visible:
            gradient_color1 = self.colors['active']
            gradient_color2 = (80, 200, 80, 200)
        
        gradient_bg = self._create_gradient_surface(rect.width, rect.height, gradient_color1, gradient_color2)
        surface.blit(gradient_bg, rect)
        
        # Borda moderna
        border_color = self.colors['border_active'] if self.controls_visible else self.colors['border']
        pygame.draw.rect(surface, border_color, rect, 2, border_radius=6)
        
        # Ícone de som melhorado
        center_x = rect.centerx
        center_y = rect.centery
        
        # Base do alto-falante com sombra
        speaker_rect = pygame.Rect(center_x - 7, center_y - 3, 5, 6)
        pygame.draw.rect(surface, (50, 50, 50), pygame.Rect(center_x - 6, center_y - 2, 5, 6))  # Sombra
        pygame.draw.rect(surface, self.colors['text'], speaker_rect)
        
        # Cone do alto-falante
        cone_points = [
            (center_x - 2, center_y - 5),
            (center_x + 3, center_y - 7),
            (center_x + 3, center_y + 7),
            (center_x - 2, center_y + 5)
        ]
        pygame.draw.polygon(surface, self.colors['text'], cone_points)
        
        # Ondas sonoras animadas (se não estiver mudo)
        if not audio_manager.is_music_muted() or not audio_manager.is_sfx_muted():
            import time
            pulse = 0.7 + 0.3 * math.sin(time.time() * 3)
            
            for i, radius in enumerate([5, 8, 11]):
                alpha = int(255 * pulse * (1 - i * 0.2))
                wave_color = (*self.colors['text'][:3], alpha)
                pygame.draw.arc(surface, wave_color, 
                              (center_x - 2, center_y - radius, radius * 2, radius * 2),
                              -math.pi/4, math.pi/4, max(1, int(2 * pulse)))
    
    def _draw_audio_panel(self, surface):
        """Desenha o painel completo de controles de áudio com visual moderno"""
        # Efeito glow no painel
        self._draw_glow_effect(surface, self.background_rect, self.colors['glow'], 0.4)
        
        # Fundo do painel com gradiente
        gradient_bg = self._create_gradient_surface(
            self.background_rect.width, 
            self.background_rect.height,
            self.colors['background'],
            self.colors['background_gradient']
        )
        surface.blit(gradient_bg, self.background_rect)
        
        # Borda do painel com dupla linha
        pygame.draw.rect(surface, self.colors['border_active'], self.background_rect, 2, border_radius=8)
        pygame.draw.rect(surface, self.colors['border'], self.background_rect, 1, border_radius=8)
        
        # Título com sombra
        font = font_manager.get('text')
        title_text = "Controles de Áudio"
        
        # Sombra do título
        shadow_surf = font.render(title_text, True, self.colors['text_shadow'])
        title_surf = font.render(title_text, True, self.colors['text'])
        
        title_x = self.background_rect.x + (self.background_rect.width - title_surf.get_width()) // 2
        title_y = self.background_rect.y + 8
        
        surface.blit(shadow_surf, (title_x + 1, title_y + 1))
        surface.blit(title_surf, (title_x, title_y))
        
        # Linha separadora elegante
        line_y = self.background_rect.y + 28
        line_start_x = self.background_rect.x + 20
        line_end_x = self.background_rect.x + self.background_rect.width - 20
        
        # Gradiente da linha
        line_gradient = self._create_gradient_surface(
            line_end_x - line_start_x, 2,
            (120, 140, 160, 100), 
            (180, 200, 220, 200),
            vertical=False
        )
        surface.blit(line_gradient, (line_start_x, line_y))
        
        # Desenhar controles de música
        self._draw_audio_control_line(surface, "music", "🎵 Música", 
                                     self.music_slider_rect, self.music_mute_rect)
        
        # Desenhar controles de efeitos
        self._draw_audio_control_line(surface, "sfx", "🔊 Efeitos", 
                                     self.sfx_slider_rect, self.sfx_mute_rect)
    
    def _draw_audio_control_line(self, surface, control_type, label, slider_rect, mute_rect):
        """Desenha uma linha de controle (música ou efeitos)"""
        font = font_manager.get('small')
        
        # Label com sombra
        label_surf = font.render(label, True, self.colors['text'])
        label_shadow = font.render(label, True, self.colors['text_shadow'])
        
        label_x = slider_rect.x - 5
        label_y = slider_rect.y - 18
        
        surface.blit(label_shadow, (label_x + 1, label_y + 1))
        surface.blit(label_surf, (label_x, label_y))
        
        # Desenhar slider moderno
        self._draw_modern_slider(surface, control_type, slider_rect)
        
        # Desenhar botão mute moderno
        self._draw_modern_mute_button(surface, control_type, mute_rect)
    
    def _draw_modern_slider(self, surface, control_type, rect):
        """Desenha um slider moderno com gradiente"""
        # Obter volume atual
        if control_type == "music":
            volume = audio_manager.music_volume
            is_muted = audio_manager.is_music_muted()
        else:
            volume = audio_manager.sfx_volume
            is_muted = audio_manager.is_sfx_muted()
        
        # Track do slider (fundo)
        track_rect = pygame.Rect(rect.x, rect.y + 6, rect.width, 4)
        pygame.draw.rect(surface, self.colors['slider_track'], track_rect, border_radius=2)
        
        # Barra preenchida
        if not is_muted and volume > 0:
            fill_width = int(rect.width * volume)
            fill_rect = pygame.Rect(rect.x, rect.y + 6, fill_width, 4)
            
            # Gradiente da barra preenchida
            if fill_width > 0:
                fill_gradient = self._create_gradient_surface(
                    fill_width, 4,
                    self.colors['slider_fill'],
                    self.colors['slider_fill_bright'],
                    vertical=False
                )
                surface.blit(fill_gradient, fill_rect)
        
        # Handle do slider
        handle_x = rect.x + int(rect.width * volume) - 6
        handle_y = rect.y + 2
        handle_rect = pygame.Rect(handle_x, handle_y, 12, 12)
        
        # Sombra do handle
        shadow_rect = pygame.Rect(handle_x + 1, handle_y + 1, 12, 12)
        pygame.draw.ellipse(surface, (0, 0, 0, 100), shadow_rect)
        
        # Handle com gradiente
        handle_color1 = self.colors['slider_handle_hover'] if control_type in self.hover_states else self.colors['slider_handle']
        handle_color2 = tuple(max(0, c - 40) for c in handle_color1)
        
        handle_gradient = self._create_gradient_surface(12, 12, handle_color1, handle_color2)
        surface.blit(handle_gradient, handle_rect)
        
        # Borda do handle
        pygame.draw.ellipse(surface, self.colors['border_active'], handle_rect, 2)
        
        # Texto do volume
        volume_text = f"{int(volume * 100)}%"
        volume_surf = font_manager.get('small').render(volume_text, True, self.colors['text'])
        volume_x = rect.x + rect.width + 10
        volume_y = rect.y
        surface.blit(volume_surf, (volume_x, volume_y))
    
    def _draw_modern_mute_button(self, surface, control_type, rect):
        """Desenha botão mute moderno"""
        # Verificar se está mudo
        if control_type == "music":
            is_muted = audio_manager.is_music_muted()
        else:
            is_muted = audio_manager.is_sfx_muted()
        
        # Cor do botão baseada no estado
        if is_muted:
            button_color1 = self.colors['muted']
            button_color2 = (200, 80, 80, 200)
            text_color = (255, 255, 255)
        else:
            button_color1 = self.colors['active']
            button_color2 = (80, 200, 80, 200)
            text_color = (255, 255, 255)
        
        # Fundo do botão com gradiente
        button_gradient = self._create_gradient_surface(rect.width, rect.height, button_color1, button_color2)
        surface.blit(button_gradient, rect)
        
        # Borda do botão
        border_color = self.colors['border_active'] if is_muted else self.colors['border']
        pygame.draw.rect(surface, border_color, rect, 2, border_radius=4)
        
        # Texto do botão
        text = "MUDO" if is_muted else "SOM"
        text_surf = font_manager.get('small').render(text, True, text_color)
        text_rect = text_surf.get_rect(center=rect.center)
        
        # Sombra do texto
        shadow_surf = font_manager.get('small').render(text, True, self.colors['text_shadow'])
        shadow_rect = text_rect.copy()
        shadow_rect.x += 1
        shadow_rect.y += 1
        
        surface.blit(shadow_surf, shadow_rect)
        surface.blit(text_surf, text_rect)

# Instância global
simple_audio_controls = SimpleAudioControls()