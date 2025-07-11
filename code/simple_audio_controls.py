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
        
        # Cores
        self.colors = {
            'background': (20, 20, 30, 200),
            'border': (100, 100, 120),
            'slider_track': (60, 60, 80),
            'slider_fill': (80, 150, 255),
            'slider_handle': (120, 180, 255),
            'text': (255, 255, 255),
            'muted': (255, 100, 100),
            'active': (100, 255, 100)
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
    
    def _draw_toggle_button(self, surface):
        """Desenha o ícone de som estático"""
        rect = self.toggle_button_rect
        
        # Fundo do botão
        button_color = self.colors['active'] if self.controls_visible else self.colors['border']
        pygame.draw.rect(surface, button_color, rect, border_radius=5)
        pygame.draw.rect(surface, self.colors['text'], rect, 2, border_radius=5)
        
        # Ícone de som simples (alto-falante)
        center_x = rect.centerx
        center_y = rect.centery
        
        # Base do alto-falante
        speaker_rect = pygame.Rect(center_x - 8, center_y - 4, 6, 8)
        pygame.draw.rect(surface, self.colors['text'], speaker_rect)
        
        # Cone do alto-falante
        cone_points = [
            (center_x - 2, center_y - 6),
            (center_x + 4, center_y - 8),
            (center_x + 4, center_y + 8),
            (center_x - 2, center_y + 6)
        ]
        pygame.draw.polygon(surface, self.colors['text'], cone_points)
        
        # Ondas sonoras (se não estiver mudo)
        if not audio_manager.is_music_muted() or not audio_manager.is_sfx_muted():
            for i, radius in enumerate([6, 9, 12]):
                pygame.draw.arc(surface, self.colors['text'], 
                              (center_x, center_y - radius, radius * 2, radius * 2),
                              -math.pi/3, math.pi/3, 2)
    
    def _draw_audio_panel(self, surface):
        """Desenha o painel completo de controles de áudio"""
        # Fundo do painel
        panel_surface = pygame.Surface((self.background_rect.width, self.background_rect.height), pygame.SRCALPHA)
        panel_surface.fill(self.colors['background'])
        surface.blit(panel_surface, self.background_rect)
        
        # Borda do painel
        pygame.draw.rect(surface, self.colors['border'], self.background_rect, 2, border_radius=8)
        
        # Título
        font = font_manager.get('text')
        title_text = font.render("Controles de Áudio", True, self.colors['text'])
        title_x = self.background_rect.x + (self.background_rect.width - title_text.get_width()) // 2
        surface.blit(title_text, (title_x, self.background_rect.y + 5))
        
        # Controle de música
        self._draw_audio_line(surface, "🎵", "Música", 
                            self.music_icon_rect, self.music_slider_rect, self.music_mute_rect,
                            audio_manager.music_volume, audio_manager.is_music_muted())
        
        # Controle de efeitos
        self._draw_audio_line(surface, "🔊", "Efeitos", 
                            self.sfx_icon_rect, self.sfx_slider_rect, self.sfx_mute_rect,
                            audio_manager.sfx_volume, audio_manager.is_sfx_muted())
        
        # Instruções
        font_small = font_manager.get('small')
        instructions = [
            "M: Mute música | N: Mute efeitos",
            "↑↓: Volume música | Shift+↑↓: Volume efeitos"
        ]
        
        for i, instruction in enumerate(instructions):
            text = font_small.render(instruction, True, self.colors['text'])
            surface.blit(text, (self.background_rect.x + 10, self.background_rect.bottom - 35 + i * 15))
    
    def _draw_audio_line(self, surface, icon, label, icon_rect, slider_rect, mute_rect, volume, is_muted):
        """Desenha uma linha de controle (música ou efeitos)"""
        font = font_manager.get('small')
        
        # Ícone
        icon_text = font.render(icon, True, self.colors['muted'] if is_muted else self.colors['text'])
        surface.blit(icon_text, icon_rect)
        
        # Slider track
        pygame.draw.rect(surface, self.colors['slider_track'], slider_rect, border_radius=8)
        
        # Slider fill
        if not is_muted and volume > 0:
            fill_width = int(slider_rect.width * volume)
            fill_rect = pygame.Rect(slider_rect.x, slider_rect.y, fill_width, slider_rect.height)
            pygame.draw.rect(surface, self.colors['slider_fill'], fill_rect, border_radius=8)
        
        # Slider handle
        if not is_muted:
            handle_x = slider_rect.x + int(slider_rect.width * volume) - 4
            handle_rect = pygame.Rect(handle_x, slider_rect.y - 2, 8, slider_rect.height + 4)
            pygame.draw.rect(surface, self.colors['slider_handle'], handle_rect, border_radius=4)
        
        # Botão mute
        mute_color = self.colors['muted'] if is_muted else self.colors['border']
        pygame.draw.rect(surface, mute_color, mute_rect, border_radius=4)
        
        mute_text = "MUDO" if is_muted else f"{int(volume * 100)}%"
        mute_surface = font.render(mute_text, True, self.colors['text'])
        mute_x = mute_rect.x + (mute_rect.width - mute_surface.get_width()) // 2
        mute_y = mute_rect.y + (mute_rect.height - mute_surface.get_height()) // 2
        surface.blit(mute_surface, (mute_x, mute_y))

# Instância global
simple_audio_controls = SimpleAudioControls()