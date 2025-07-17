"""
Sistema moderno e unificado de controles de áudio + fullscreen
Interface centralizada que substitui simple_audio_controls e settings_manager
"""
import pygame
import math
from typing import Tuple, Optional
from audio_manager import audio_manager
from graphics_manager import GraphicsManager
from icon_manager import icon_manager


class ModernAudioControls:
    """
    Interface moderna unificada para controles de áudio e fullscreen.
    Posicionada no canto superior direito, consistente em todas as fases.
    """
    
    def __init__(self):
        # Managers
        self.graphics_manager = GraphicsManager()
        
        # Estados
        self.audio_panel_open = False
        self.last_toggle_time = 0
        self.hover_button = None
        self.dragging_slider = None
        
        # Posições e tamanhos (serão atualizados dinamicamente)
        self.screen_width = 1280
        self.screen_height = 800
        self.update_positions()
        
        # Cores e estilo (inspirado no menu principal)
        self.colors = {
            'primary': (64, 224, 208),      # Turquesa
            'secondary': (255, 107, 107),    # Coral
            'background': (25, 25, 35),      # Cinza escuro
            'surface': (35, 35, 45),         # Cinza médio
            'text': (255, 255, 255),         # Branco
            'text_secondary': (180, 180, 180), # Cinza claro
            'hover': (80, 240, 220),         # Turquesa claro
            'active': (48, 208, 192),        # Turquesa escuro
            'success': (46, 213, 115),       # Verde
            'warning': (255, 193, 7),        # Amarelo
            'error': (255, 71, 87),          # Vermelho
        }
        
        # Animações
        self.animations = {
            'panel_slide': 0.0,
            'button_glow': 0.0,
            'equalizer_bars': [0.0] * 10,
            'gear_rotation': 0.0,
        }
        
        # Fontes
        self._load_fonts()
        
        # Cache de surfaces - agora usando IconManager
        self._create_button_surfaces()
    
    def _load_fonts(self) -> None:
        """Carrega fontes para a interface."""
        try:
            self.font_small = pygame.font.Font(None, 18)
            self.font_medium = pygame.font.Font(None, 24)
            self.font_large = pygame.font.Font(None, 32)
        except pygame.error:
            # Fallback para fonte do sistema
            self.font_small = pygame.font.SysFont('Arial', 14)
            self.font_medium = pygame.font.SysFont('Arial', 18)
            self.font_large = pygame.font.SysFont('Arial', 24)
    
    def update_positions(self) -> None:
        """Atualiza posições baseado no tamanho da tela."""
        # Botões no canto superior direito
        button_size = 40
        button_margin = 10
        top_margin = 10
        
        # Botão de áudio
        self.audio_button_rect = pygame.Rect(
            self.screen_width - (button_size + button_margin) * 2 - button_margin,
            top_margin,
            button_size,
            button_size
        )
        
        # Botão de fullscreen
        self.fullscreen_button_rect = pygame.Rect(
            self.screen_width - button_size - button_margin,
            top_margin,
            button_size,
            button_size
        )
        
        # Painel de áudio (quando aberto)
        panel_width = 320
        panel_height = 200
        self.audio_panel_rect = pygame.Rect(
            self.screen_width - panel_width - button_margin,
            self.audio_button_rect.bottom + 5,
            panel_width,
            panel_height
        )
        
        # Sliders dentro do painel
        slider_width = 200
        slider_height = 20
        slider_x = self.audio_panel_rect.x + 60
        
        self.music_slider_rect = pygame.Rect(
            slider_x,
            self.audio_panel_rect.y + 60,
            slider_width,
            slider_height
        )
        
        self.sfx_slider_rect = pygame.Rect(
            slider_x,
            self.audio_panel_rect.y + 120,
            slider_width,
            slider_height
        )
        
        # Botões de mute
        mute_size = 24
        self.music_mute_rect = pygame.Rect(
            self.audio_panel_rect.x + 20,
            self.music_slider_rect.y + (slider_height - mute_size) // 2,
            mute_size,
            mute_size
        )
        
        self.sfx_mute_rect = pygame.Rect(
            self.audio_panel_rect.x + 20,
            self.sfx_slider_rect.y + (slider_height - mute_size) // 2,
            mute_size,
            mute_size
        )
    
    def _create_button_surfaces(self) -> None:
        """Cria surfaces para os botões com ícones profissionais."""
        button_size = 40
        
        # Botão de áudio - usando IconManager
        volume_level = audio_manager.volume
        is_muted = audio_manager.is_muted()
        icon_name = icon_manager.get_volume_icon_by_level(volume_level, is_muted)
        
        self.audio_icon_surface = icon_manager.get_icon(icon_name, button_size-8, self.colors['text'])
        
        # Botão de fullscreen - usando IconManager
        fullscreen_icon = 'windowed' if self.graphics_manager.is_fullscreen() else 'fullscreen'
        self.fullscreen_icon_surface = icon_manager.get_icon(fullscreen_icon, button_size-8, self.colors['text'])
    
    def _update_button_icons(self) -> None:
        """Atualiza ícones dos botões baseado no estado atual."""
        button_size = 40
        
        # Atualizar ícone de áudio baseado no volume/mute
        volume_level = audio_manager.volume
        is_muted = audio_manager.is_muted()
        icon_name = icon_manager.get_volume_icon_by_level(volume_level, is_muted)
        
        self.audio_icon_surface = icon_manager.get_icon(icon_name, button_size-8, self.colors['text'])
        
        # Atualizar ícone de fullscreen baseado no estado
        fullscreen_icon = 'windowed' if self.graphics_manager.is_fullscreen() else 'fullscreen'
        self.fullscreen_icon_surface = icon_manager.get_icon(fullscreen_icon, button_size-8, self.colors['text'])
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Processa eventos da interface.
        
        Args:
            event: Evento do pygame
            
        Returns:
            bool: True se o evento foi consumido
        """
        mouse_pos = pygame.mouse.get_pos()
        current_time = pygame.time.get_ticks()
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Clique no botão de áudio
            if self.audio_button_rect.collidepoint(mouse_pos):
                if current_time - self.last_toggle_time > 200:  # Debounce
                    self.audio_panel_open = not self.audio_panel_open
                    self.last_toggle_time = current_time
                return True
            
            # Clique no botão de fullscreen
            if self.fullscreen_button_rect.collidepoint(mouse_pos):
                self.graphics_manager.toggle_fullscreen()
                self.graphics_manager.apply_settings()
                # Atualiza tamanho da tela
                screen = self.graphics_manager.get_screen()
                if screen:
                    self.screen_width = screen.get_width()
                    self.screen_height = screen.get_height()
                    self.update_positions()
                    self._create_button_surfaces()
                return True
            
            # Cliques no painel de áudio
            if self.audio_panel_open and self.audio_panel_rect.collidepoint(mouse_pos):
                # Botão mute música
                if self.music_mute_rect.collidepoint(mouse_pos):
                    audio_manager.toggle_mute()
                    return True
                
                # Botão mute SFX
                if self.sfx_mute_rect.collidepoint(mouse_pos):
                    audio_manager.toggle_mute()
                    return True
                
                # Slider música
                if self.music_slider_rect.collidepoint(mouse_pos):
                    self.dragging_slider = 'music'
                    self._update_slider_value(mouse_pos, 'music')
                    return True
                
                # Slider SFX
                if self.sfx_slider_rect.collidepoint(mouse_pos):
                    self.dragging_slider = 'sfx'
                    self._update_slider_value(mouse_pos, 'sfx')
                    return True
                
                return True  # Consome clique no painel
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging_slider = None
        
        elif event.type == pygame.MOUSEMOTION:
            # Atualiza hover
            self.hover_button = None
            if self.audio_button_rect.collidepoint(mouse_pos):
                self.hover_button = 'audio'
            elif self.fullscreen_button_rect.collidepoint(mouse_pos):
                self.hover_button = 'fullscreen'
            
            # Arrasta slider
            if self.dragging_slider:
                self._update_slider_value(mouse_pos, self.dragging_slider)
                return True
        
        elif event.type == pygame.KEYDOWN:
            # Controles por teclado
            if event.key == pygame.K_m:
                audio_manager.toggle_mute()
                return True
            elif event.key == pygame.K_n:
                audio_manager.toggle_mute()
                return True
            elif event.key == pygame.K_UP or event.key == pygame.K_PLUS:
                current_vol = audio_manager.volume
                audio_manager.set_volume(min(1.0, current_vol + 0.1))
                return True
            elif event.key == pygame.K_DOWN or event.key == pygame.K_MINUS:
                current_vol = audio_manager.volume
                audio_manager.set_volume(max(0.0, current_vol - 0.1))
                return True
            elif event.key == pygame.K_F11:
                self.graphics_manager.toggle_fullscreen()
                self.graphics_manager.apply_settings()
                return True
        
        # Clique fora fecha o painel
        if event.type == pygame.MOUSEBUTTONDOWN and self.audio_panel_open:
            if not self.audio_panel_rect.collidepoint(mouse_pos) and \
               not self.audio_button_rect.collidepoint(mouse_pos):
                self.audio_panel_open = False
                return False
        
        return False
    
    def handle_keydown(self, event: pygame.event.Event) -> bool:
        """
        Compatibilidade com API do settings_manager.
        
        Args:
            event: Evento de teclado
            
        Returns:
            bool: True se o evento foi processado
        """
        return self.handle_event(event)
    
    def handle_mouse_click(self, mouse_pos: Tuple[int, int]) -> bool:
        """
        Compatibilidade com API do settings_manager.
        
        Args:
            mouse_pos: Posição do mouse
            
        Returns:
            bool: True se o clique foi processado
        """
        # Simula evento de clique para compatibilidade
        fake_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, 
                                       {'button': 1, 'pos': mouse_pos})
        return self.handle_event(fake_event)
    
    def is_menu_open(self) -> bool:
        """
        Compatibilidade com API do settings_manager.
        
        Returns:
            bool: True se o menu está aberto
        """
        return self.audio_panel_open
    
    def _update_slider_value(self, mouse_pos: Tuple[int, int], slider_type: str) -> None:
        """Atualiza valor do slider baseado na posição do mouse."""
        if slider_type == 'music':
            slider_rect = self.music_slider_rect
        else:
            slider_rect = self.sfx_slider_rect
        
        # Calcula valor baseado na posição X
        relative_x = mouse_pos[0] - slider_rect.x
        value = max(0.0, min(1.0, relative_x / slider_rect.width))
        
        if slider_type == 'music':
            audio_manager.set_volume(value)
        else:
            audio_manager.set_volume(value)
    
    def update(self, dt: float) -> None:
        """Atualiza animações."""
        # Animação do painel
        target_slide = 1.0 if self.audio_panel_open else 0.0
        self.animations['panel_slide'] += (target_slide - self.animations['panel_slide']) * dt * 8
        
        # Animação de glow dos botões
        target_glow = 1.0 if self.hover_button else 0.0
        self.animations['button_glow'] += (target_glow - self.animations['button_glow']) * dt * 10
        
        # Animação do equalizador (baseado no volume)
        music_vol = audio_manager.volume
        for i in range(len(self.animations['equalizer_bars'])):
            target_height = music_vol * (0.5 + 0.5 * math.sin(pygame.time.get_ticks() * 0.01 + i * 0.5))
            self.animations['equalizer_bars'][i] += (target_height - self.animations['equalizer_bars'][i]) * dt * 5
        
        # Rotação da engrenagem
        self.animations['gear_rotation'] += dt * 90  # 90 graus por segundo
    
    def draw(self, screen: pygame.Surface) -> None:
        """Desenha a interface."""
        # Atualiza tamanho da tela se mudou
        current_size = screen.get_size()
        if (current_size[0], current_size[1]) != (self.screen_width, self.screen_height):
            self.screen_width, self.screen_height = current_size
            self.update_positions()
            self._create_button_surfaces()
        
        # Desenha botões
        self._draw_buttons(screen)
        
        # Desenha painel de áudio se aberto
        if self.animations['panel_slide'] > 0.01:
            self._draw_audio_panel(screen)
    
    def _draw_buttons(self, screen: pygame.Surface) -> None:
        """Desenha os botões principais."""
        # Efeito de glow
        if self.animations['button_glow'] > 0.01:
            glow_size = int(50 * self.animations['button_glow'])
            glow_surface = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
            alpha = int(50 * self.animations['button_glow'])
            glow_color = (*self.colors['primary'], alpha)
            
            # Usar círculo com alpha por preenchimento
            for radius in range(glow_size//2, 0, -2):
                circle_alpha = int(alpha * (1 - radius / (glow_size//2)))
                if circle_alpha > 0:
                    circle_surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
                    color_with_alpha = (*self.colors['primary'], max(0, min(255, int(circle_alpha))))
                    pygame.draw.circle(circle_surface, color_with_alpha, 
                                     (radius, radius), radius)
                    glow_surface.blit(circle_surface, (glow_size//2 - radius, glow_size//2 - radius))
            
            if self.hover_button == 'audio':
                screen.blit(glow_surface, (self.audio_button_rect.centerx - glow_size//2, 
                                         self.audio_button_rect.centery - glow_size//2))
            elif self.hover_button == 'fullscreen':
                screen.blit(glow_surface, (self.fullscreen_button_rect.centerx - glow_size//2, 
                                         self.fullscreen_button_rect.centery - glow_size//2))
        
        # Background dos botões
        self._draw_button_background(screen, self.audio_button_rect, self.hover_button == 'audio')
        self._draw_button_background(screen, self.fullscreen_button_rect, self.hover_button == 'fullscreen')
        
        # Ícones profissionais - atualizar se necessário
        self._update_button_icons()
        
        # Centralizar ícones nos botões
        audio_icon_rect = self.audio_icon_surface.get_rect(center=self.audio_button_rect.center)
        fullscreen_icon_rect = self.fullscreen_icon_surface.get_rect(center=self.fullscreen_button_rect.center)
        
        screen.blit(self.audio_icon_surface, audio_icon_rect)
        screen.blit(self.fullscreen_icon_surface, fullscreen_icon_rect)
    
    def _draw_button_background(self, screen: pygame.Surface, rect: pygame.Rect, is_hovered: bool) -> None:
        """Desenha fundo do botão com gradiente."""
        # Gradiente
        for i in range(rect.height):
            ratio = i / rect.height
            if is_hovered:
                color = self._lerp_color(self.colors['surface'], self.colors['hover'], ratio * 0.3)
            else:
                color = self._lerp_color(self.colors['background'], self.colors['surface'], ratio * 0.5)
            pygame.draw.line(screen, color, (rect.x, rect.y + i), (rect.right, rect.y + i))
        
        # Borda
        border_color = self.colors['primary'] if is_hovered else self.colors['text_secondary']
        pygame.draw.rect(screen, border_color, rect, 2, border_radius=8)
    
    def _draw_audio_panel(self, screen: pygame.Surface) -> None:
        """Desenha o painel de controles de áudio."""
        # Animação de slide
        slide_offset = int((1.0 - self.animations['panel_slide']) * self.audio_panel_rect.width)
        panel_rect = self.audio_panel_rect.copy()
        panel_rect.x += slide_offset
        
        # Background do painel com transparência
        panel_surface = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
        
        # Gradiente de fundo
        for i in range(panel_rect.height):
            ratio = i / panel_rect.height
            color = self._lerp_color(self.colors['background'], self.colors['surface'], ratio * 0.7)
            alpha_color = (*color, int(240 * self.animations['panel_slide']))
            pygame.draw.line(panel_surface, alpha_color, (0, i), (panel_rect.width, i))
        
        # Borda do painel
        pygame.draw.rect(panel_surface, self.colors['primary'], 
                        (0, 0, panel_rect.width, panel_rect.height), 2, border_radius=12)
        
        screen.blit(panel_surface, panel_rect)
        
        # Conteúdo do painel
        alpha = int(255 * self.animations['panel_slide'])
        
        # Título
        title_surface = self.font_medium.render("Controles de Áudio", True, self.colors['text'])
        screen.blit(title_surface, (panel_rect.x + 20, panel_rect.y + 15))
        
        # Música
        music_label = self.font_small.render("Música:", True, self.colors['text_secondary'])
        screen.blit(music_label, (panel_rect.x + 60, panel_rect.y + 45))
        
        # SFX
        sfx_label = self.font_small.render("Efeitos:", True, self.colors['text_secondary'])
        screen.blit(sfx_label, (panel_rect.x + 60, panel_rect.y + 105))
        
        # Desenha controles
        self._draw_audio_control(screen, panel_rect, 'music', alpha)
        self._draw_audio_control(screen, panel_rect, 'sfx', alpha)
        
        # Equalizador decorativo
        self._draw_equalizer(screen, panel_rect, alpha)
        
        # Teclas de atalho
        shortcuts = self.font_small.render("M: Mute Música | N: Mute SFX | ↑↓: Volume | F11: Fullscreen", 
                                         True, self.colors['text_secondary'])
        screen.blit(shortcuts, (panel_rect.x + 10, panel_rect.y + panel_rect.height - 20))
    
    def _draw_audio_control(self, screen: pygame.Surface, panel_rect: pygame.Rect, 
                           control_type: str, alpha: int) -> None:
        """Desenha controle individual (música ou SFX)."""
        if control_type == 'music':
            mute_rect = self.music_mute_rect.copy()
            slider_rect = self.music_slider_rect.copy()
            volume = audio_manager.volume
            is_muted = audio_manager.is_muted()
        else:
            mute_rect = self.sfx_mute_rect.copy()
            slider_rect = self.sfx_slider_rect.copy()
            volume = audio_manager.volume
            is_muted = audio_manager.is_muted()
        
        # Ajusta posições para o slide
        slide_offset = int((1.0 - self.animations['panel_slide']) * self.audio_panel_rect.width)
        mute_rect.x += slide_offset
        slider_rect.x += slide_offset
        
        # Botão de mute
        mute_color = self.colors['error'] if is_muted else self.colors['success']
        pygame.draw.rect(screen, mute_color, mute_rect, border_radius=4)
        
        # Ícone do botão mute usando IconManager
        icon_name = 'volume_mute' if is_muted else 'volume_high'
        mute_icon = icon_manager.get_icon(icon_name, mute_rect.width-4, self.colors['text'])
        mute_icon_rect = mute_icon.get_rect(center=mute_rect.center)
        screen.blit(mute_icon, mute_icon_rect)
        
        # Slider track
        pygame.draw.rect(screen, self.colors['background'], slider_rect, border_radius=10)
        
        # Slider fill
        fill_width = int(slider_rect.width * volume)
        if fill_width > 0:
            fill_rect = pygame.Rect(slider_rect.x, slider_rect.y, fill_width, slider_rect.height)
            color = self.colors['primary'] if not is_muted else self.colors['text_secondary']
            pygame.draw.rect(screen, color, fill_rect, border_radius=10)
        
        # Slider handle
        handle_x = slider_rect.x + int(slider_rect.width * volume) - 8
        handle_rect = pygame.Rect(handle_x, slider_rect.y - 2, 16, slider_rect.height + 4)
        pygame.draw.rect(screen, self.colors['text'], handle_rect, border_radius=8)
        
        # Valor numérico
        value_text = f"{int(volume * 100)}%"
        value_surface = self.font_small.render(value_text, True, self.colors['text'])
        screen.blit(value_surface, (slider_rect.right + 10, slider_rect.y + 2))
    
    def _draw_equalizer(self, screen: pygame.Surface, panel_rect: pygame.Rect, alpha: int) -> None:
        """Desenha equalizador decorativo."""
        eq_x = panel_rect.x + 10
        eq_y = panel_rect.y + 45
        bar_width = 3
        bar_spacing = 4
        max_height = 30
        
        for i, height_ratio in enumerate(self.animations['equalizer_bars']):
            bar_height = int(max_height * height_ratio)
            bar_rect = pygame.Rect(
                eq_x + i * (bar_width + bar_spacing),
                eq_y + max_height - bar_height,
                bar_width,
                bar_height
            )
            
            # Cor baseada na altura
            if height_ratio > 0.7:
                color = self.colors['error']
            elif height_ratio > 0.4:
                color = self.colors['warning']
            else:
                color = self.colors['success']
            
            pygame.draw.rect(screen, color, bar_rect)
    
    def _lerp_color(self, color1: Tuple[int, int, int], color2: Tuple[int, int, int], t: float) -> Tuple[int, int, int]:
        """Interpola entre duas cores."""
        return (
            int(color1[0] + (color2[0] - color1[0]) * t),
            int(color1[1] + (color2[1] - color1[1]) * t),
            int(color1[2] + (color2[2] - color1[2]) * t)
        )


# Instância global
modern_audio_controls = ModernAudioControls()