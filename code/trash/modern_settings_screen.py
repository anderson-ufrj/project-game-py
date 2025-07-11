"""
Tela de Configurações Moderna com Tabs e Controles Avançados
"""
import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UIHorizontalSlider, UILabel, UIDropDownMenu, UITextEntryLine
from pygame_gui.elements import UISelectionList, UIPanel
from typing import Dict, List, Tuple, Optional
from modern_ui_system import modern_ui, UITheme
from audio_manager import audio_manager
from enum import Enum
import json

class SettingsTab(Enum):
    AUDIO = "Áudio"
    GRAPHICS = "Gráficos"
    CONTROLS = "Controles"
    GAME = "Jogo"

class ModernSettingsScreen:
    """Tela de configurações com visual moderno e tabs"""
    
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.width, self.height = self.screen.get_size()
        
        # Estado
        self.active_tab = SettingsTab.AUDIO
        self.is_open = False
        self.changes_made = False
        
        # Container principal
        panel_width = 800
        panel_height = 600
        self.panel_rect = pygame.Rect(
            (self.width - panel_width) // 2,
            (self.height - panel_height) // 2,
            panel_width,
            panel_height
        )
        
        # Criar elementos UI
        self.create_ui_elements()
        
        # Configurações temporárias
        self.temp_settings = self.load_current_settings()
        
        print("⚙️ Tela de Configurações Moderna inicializada!")
    
    def load_current_settings(self) -> Dict:
        """Carrega configurações atuais"""
        return {
            # Áudio
            "music_volume": audio_manager.music_volume * 100,
            "sfx_volume": audio_manager.sfx_volume * 100,
            "music_muted": audio_manager.music_muted,
            "sfx_muted": audio_manager.sfx_muted,
            
            # Gráficos
            "resolution": "1280x720",
            "fullscreen": False,
            "vsync": True,
            "quality": "Alta",
            "particles": True,
            "shadows": True,
            
            # Controles
            "move_up": "W",
            "move_down": "S",
            "move_left": "A",
            "move_right": "D",
            "attack": "Espaço",
            "dash": "Shift",
            
            # Jogo
            "difficulty": "Normal",
            "show_fps": False,
            "auto_save": True,
            "language": "Português"
        }
    
    def create_ui_elements(self):
        """Cria todos os elementos da UI"""
        colors = modern_ui.get_current_colors()
        
        # Panel principal com transparência
        self.main_panel = UIPanel(
            relative_rect=self.panel_rect,
            starting_layer_height=1,
            manager=modern_ui.manager
        )
        
        # Título
        title_rect = pygame.Rect(0, 10, self.panel_rect.width, 40)
        self.title_label = UILabel(
            relative_rect=title_rect,
            text="CONFIGURAÇÕES",
            manager=modern_ui.manager,
            container=self.main_panel
        )
        
        # Criar tabs
        self.create_tabs()
        
        # Container para conteúdo das tabs
        content_rect = pygame.Rect(
            20, 100,
            self.panel_rect.width - 40,
            self.panel_rect.height - 180
        )
        self.content_panel = UIPanel(
            relative_rect=content_rect,
            starting_layer_height=2,
            manager=modern_ui.manager,
            container=self.main_panel
        )
        
        # Botões de ação
        self.create_action_buttons()
        
        # Criar conteúdo inicial
        self.update_tab_content()
    
    def create_tabs(self):
        """Cria os botões de tabs"""
        tab_width = 150
        tab_height = 40
        tab_y = 50
        tab_spacing = 10
        
        self.tab_buttons = {}
        
        for i, tab in enumerate(SettingsTab):
            x = 20 + i * (tab_width + tab_spacing)
            
            button = UIButton(
                relative_rect=pygame.Rect(x, tab_y, tab_width, tab_height),
                text=tab.value,
                manager=modern_ui.manager,
                container=self.main_panel,
                object_id=f'#tab_{tab.name.lower()}'
            )
            
            self.tab_buttons[tab] = button
            
            # Registrar callback
            modern_ui.callbacks[f'#tab_{tab.name.lower()}'] = lambda t=tab: self.switch_tab(t)
    
    def create_action_buttons(self):
        """Cria botões de aplicar/cancelar"""
        button_width = 120
        button_height = 40
        button_y = self.panel_rect.height - 60
        
        # Botão Aplicar
        self.apply_button = UIButton(
            relative_rect=pygame.Rect(
                self.panel_rect.width - 260,
                button_y,
                button_width,
                button_height
            ),
            text="Aplicar",
            manager=modern_ui.manager,
            container=self.main_panel,
            object_id='#apply_settings'
        )
        
        # Botão Cancelar
        self.cancel_button = UIButton(
            relative_rect=pygame.Rect(
                self.panel_rect.width - 130,
                button_y,
                button_width,
                button_height
            ),
            text="Cancelar",
            manager=modern_ui.manager,
            container=self.main_panel,
            object_id='#cancel_settings'
        )
        
        # Registrar callbacks
        modern_ui.callbacks['#apply_settings'] = self.apply_settings
        modern_ui.callbacks['#cancel_settings'] = self.close
    
    def switch_tab(self, tab: SettingsTab):
        """Muda para outra tab"""
        if tab != self.active_tab:
            self.active_tab = tab
            self.update_tab_content()
            
            # Atualizar visual das tabs
            for t, button in self.tab_buttons.items():
                if t == tab:
                    button.set_text(f"[{t.value}]")
                else:
                    button.set_text(t.value)
    
    def update_tab_content(self):
        """Atualiza o conteúdo baseado na tab ativa"""
        # Limpar conteúdo anterior
        self.content_panel.kill()
        
        # Recriar panel
        content_rect = pygame.Rect(
            20, 100,
            self.panel_rect.width - 40,
            self.panel_rect.height - 180
        )
        self.content_panel = UIPanel(
            relative_rect=content_rect,
            starting_layer_height=2,
            manager=modern_ui.manager,
            container=self.main_panel
        )
        
        # Criar conteúdo baseado na tab
        if self.active_tab == SettingsTab.AUDIO:
            self.create_audio_settings()
        elif self.active_tab == SettingsTab.GRAPHICS:
            self.create_graphics_settings()
        elif self.active_tab == SettingsTab.CONTROLS:
            self.create_controls_settings()
        elif self.active_tab == SettingsTab.GAME:
            self.create_game_settings()
    
    def create_audio_settings(self):
        """Cria configurações de áudio"""
        y_offset = 20
        
        # Volume da Música
        UILabel(
            relative_rect=pygame.Rect(20, y_offset, 200, 30),
            text="Volume da Música:",
            manager=modern_ui.manager,
            container=self.content_panel
        )
        
        self.music_slider = UIHorizontalSlider(
            relative_rect=pygame.Rect(220, y_offset, 300, 30),
            start_value=self.temp_settings["music_volume"],
            value_range=(0, 100),
            manager=modern_ui.manager,
            container=self.content_panel
        )
        
        self.music_value_label = UILabel(
            relative_rect=pygame.Rect(530, y_offset, 60, 30),
            text=f"{int(self.temp_settings['music_volume'])}%",
            manager=modern_ui.manager,
            container=self.content_panel
        )
        
        y_offset += 50
        
        # Volume dos Efeitos
        UILabel(
            relative_rect=pygame.Rect(20, y_offset, 200, 30),
            text="Volume dos Efeitos:",
            manager=modern_ui.manager,
            container=self.content_panel
        )
        
        self.sfx_slider = UIHorizontalSlider(
            relative_rect=pygame.Rect(220, y_offset, 300, 30),
            start_value=self.temp_settings["sfx_volume"],
            value_range=(0, 100),
            manager=modern_ui.manager,
            container=self.content_panel
        )
        
        self.sfx_value_label = UILabel(
            relative_rect=pygame.Rect(530, y_offset, 60, 30),
            text=f"{int(self.temp_settings['sfx_volume'])}%",
            manager=modern_ui.manager,
            container=self.content_panel
        )
        
        y_offset += 60
        
        # Botões Mute
        self.music_mute_button = UIButton(
            relative_rect=pygame.Rect(20, y_offset, 250, 40),
            text="🔇 Mutar Música" if not self.temp_settings["music_muted"] else "🔊 Desmutar Música",
            manager=modern_ui.manager,
            container=self.content_panel,
            object_id='#music_mute'
        )
        
        self.sfx_mute_button = UIButton(
            relative_rect=pygame.Rect(290, y_offset, 250, 40),
            text="🔇 Mutar Efeitos" if not self.temp_settings["sfx_muted"] else "🔊 Desmutar Efeitos",
            manager=modern_ui.manager,
            container=self.content_panel,
            object_id='#sfx_mute'
        )
        
        # Callbacks
        modern_ui.callbacks['#music_mute'] = self.toggle_music_mute
        modern_ui.callbacks['#sfx_mute'] = self.toggle_sfx_mute
        
        y_offset += 60
        
        # Teste de som
        UILabel(
            relative_rect=pygame.Rect(20, y_offset, 200, 30),
            text="Testar Sons:",
            manager=modern_ui.manager,
            container=self.content_panel
        )
        
        self.test_sound_button = UIButton(
            relative_rect=pygame.Rect(220, y_offset, 150, 40),
            text="🔊 Testar",
            manager=modern_ui.manager,
            container=self.content_panel,
            object_id='#test_sound'
        )
        
        modern_ui.callbacks['#test_sound'] = self.test_sound
    
    def create_graphics_settings(self):
        """Cria configurações gráficas"""
        y_offset = 20
        
        # Resolução
        UILabel(
            relative_rect=pygame.Rect(20, y_offset, 200, 30),
            text="Resolução:",
            manager=modern_ui.manager,
            container=self.content_panel
        )
        
        resolutions = ["1280x720", "1366x768", "1920x1080", "2560x1440"]
        self.resolution_dropdown = UIDropDownMenu(
            options_list=resolutions,
            starting_option=self.temp_settings["resolution"],
            relative_rect=pygame.Rect(220, y_offset, 200, 30),
            manager=modern_ui.manager,
            container=self.content_panel
        )
        
        y_offset += 50
        
        # Fullscreen
        self.fullscreen_button = UIButton(
            relative_rect=pygame.Rect(20, y_offset, 250, 40),
            text="✓ Tela Cheia" if self.temp_settings["fullscreen"] else "□ Tela Cheia",
            manager=modern_ui.manager,
            container=self.content_panel,
            object_id='#fullscreen_toggle'
        )
        
        # VSync
        self.vsync_button = UIButton(
            relative_rect=pygame.Rect(290, y_offset, 250, 40),
            text="✓ VSync" if self.temp_settings["vsync"] else "□ VSync",
            manager=modern_ui.manager,
            container=self.content_panel,
            object_id='#vsync_toggle'
        )
        
        y_offset += 60
        
        # Qualidade
        UILabel(
            relative_rect=pygame.Rect(20, y_offset, 200, 30),
            text="Qualidade Gráfica:",
            manager=modern_ui.manager,
            container=self.content_panel
        )
        
        qualities = ["Baixa", "Média", "Alta", "Ultra"]
        self.quality_dropdown = UIDropDownMenu(
            options_list=qualities,
            starting_option=self.temp_settings["quality"],
            relative_rect=pygame.Rect(220, y_offset, 200, 30),
            manager=modern_ui.manager,
            container=self.content_panel
        )
        
        y_offset += 60
        
        # Efeitos
        UILabel(
            relative_rect=pygame.Rect(20, y_offset, 200, 30),
            text="Efeitos Visuais:",
            manager=modern_ui.manager,
            container=self.content_panel
        )
        
        self.particles_button = UIButton(
            relative_rect=pygame.Rect(20, y_offset + 40, 250, 40),
            text="✓ Partículas" if self.temp_settings["particles"] else "□ Partículas",
            manager=modern_ui.manager,
            container=self.content_panel,
            object_id='#particles_toggle'
        )
        
        self.shadows_button = UIButton(
            relative_rect=pygame.Rect(290, y_offset + 40, 250, 40),
            text="✓ Sombras" if self.temp_settings["shadows"] else "□ Sombras",
            manager=modern_ui.manager,
            container=self.content_panel,
            object_id='#shadows_toggle'
        )
        
        # Callbacks
        modern_ui.callbacks['#fullscreen_toggle'] = self.toggle_fullscreen
        modern_ui.callbacks['#vsync_toggle'] = self.toggle_vsync
        modern_ui.callbacks['#particles_toggle'] = self.toggle_particles
        modern_ui.callbacks['#shadows_toggle'] = self.toggle_shadows
    
    def create_controls_settings(self):
        """Cria configurações de controles"""
        y_offset = 20
        
        controls = [
            ("Mover para Cima:", "move_up"),
            ("Mover para Baixo:", "move_down"),
            ("Mover para Esquerda:", "move_left"),
            ("Mover para Direita:", "move_right"),
            ("Atacar:", "attack"),
            ("Correr:", "dash")
        ]
        
        self.control_entries = {}
        
        for label, key in controls:
            UILabel(
                relative_rect=pygame.Rect(20, y_offset, 200, 30),
                text=label,
                manager=modern_ui.manager,
                container=self.content_panel
            )
            
            entry = UITextEntryLine(
                relative_rect=pygame.Rect(220, y_offset, 100, 30),
                initial_text=self.temp_settings[key],
                manager=modern_ui.manager,
                container=self.content_panel
            )
            entry.set_allowed_characters('ABCDEFGHIJKLMNOPQRSTUVWXYZ ')
            entry.set_text_length_limit(10)
            
            self.control_entries[key] = entry
            
            y_offset += 40
        
        # Botão reset
        self.reset_controls_button = UIButton(
            relative_rect=pygame.Rect(20, y_offset + 20, 200, 40),
            text="🔄 Resetar Controles",
            manager=modern_ui.manager,
            container=self.content_panel,
            object_id='#reset_controls'
        )
        
        modern_ui.callbacks['#reset_controls'] = self.reset_controls
    
    def create_game_settings(self):
        """Cria configurações do jogo"""
        y_offset = 20
        
        # Dificuldade
        UILabel(
            relative_rect=pygame.Rect(20, y_offset, 200, 30),
            text="Dificuldade:",
            manager=modern_ui.manager,
            container=self.content_panel
        )
        
        difficulties = ["Fácil", "Normal", "Difícil", "Extremo"]
        self.difficulty_dropdown = UIDropDownMenu(
            options_list=difficulties,
            starting_option=self.temp_settings["difficulty"],
            relative_rect=pygame.Rect(220, y_offset, 200, 30),
            manager=modern_ui.manager,
            container=self.content_panel
        )
        
        y_offset += 60
        
        # Opções
        self.show_fps_button = UIButton(
            relative_rect=pygame.Rect(20, y_offset, 250, 40),
            text="✓ Mostrar FPS" if self.temp_settings["show_fps"] else "□ Mostrar FPS",
            manager=modern_ui.manager,
            container=self.content_panel,
            object_id='#show_fps_toggle'
        )
        
        self.auto_save_button = UIButton(
            relative_rect=pygame.Rect(290, y_offset, 250, 40),
            text="✓ Auto-Save" if self.temp_settings["auto_save"] else "□ Auto-Save",
            manager=modern_ui.manager,
            container=self.content_panel,
            object_id='#auto_save_toggle'
        )
        
        y_offset += 60
        
        # Idioma
        UILabel(
            relative_rect=pygame.Rect(20, y_offset, 200, 30),
            text="Idioma:",
            manager=modern_ui.manager,
            container=self.content_panel
        )
        
        languages = ["Português", "English", "Español"]
        self.language_dropdown = UIDropDownMenu(
            options_list=languages,
            starting_option=self.temp_settings["language"],
            relative_rect=pygame.Rect(220, y_offset, 200, 30),
            manager=modern_ui.manager,
            container=self.content_panel
        )
        
        # Callbacks
        modern_ui.callbacks['#show_fps_toggle'] = self.toggle_show_fps
        modern_ui.callbacks['#auto_save_toggle'] = self.toggle_auto_save
    
    def update(self, dt: float):
        """Atualiza a tela de configurações"""
        if not self.is_open:
            return
        
        # Atualizar valores dos sliders
        if hasattr(self, 'music_slider'):
            music_vol = self.music_slider.get_current_value()
            self.music_value_label.set_text(f"{int(music_vol)}%")
            self.temp_settings["music_volume"] = music_vol
        
        if hasattr(self, 'sfx_slider'):
            sfx_vol = self.sfx_slider.get_current_value()
            self.sfx_value_label.set_text(f"{int(sfx_vol)}%")
            self.temp_settings["sfx_volume"] = sfx_vol
    
    def draw(self, surface: pygame.Surface):
        """Desenha a tela de configurações"""
        if not self.is_open:
            return
        
        # Overlay escuro
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))
        
        # Efeito de glow no panel
        colors = modern_ui.get_current_colors()
        glow = modern_ui.create_glow_surface(
            (self.panel_rect.width + 40, self.panel_rect.height + 40),
            colors.primary,
            0.3
        )
        glow_rect = glow.get_rect(center=self.panel_rect.center)
        surface.blit(glow, glow_rect)
    
    def open(self):
        """Abre a tela de configurações"""
        self.is_open = True
        self.temp_settings = self.load_current_settings()
        self.update_tab_content()
    
    def close(self):
        """Fecha a tela de configurações"""
        self.is_open = False
        if self.changes_made:
            modern_ui.create_notification("Alterações descartadas", "warning")
        self.changes_made = False
    
    def apply_settings(self):
        """Aplica as configurações"""
        # Aplicar áudio
        audio_manager.set_music_volume(self.temp_settings["music_volume"] / 100)
        audio_manager.set_sfx_volume(self.temp_settings["sfx_volume"] / 100)
        audio_manager.music_muted = self.temp_settings["music_muted"]
        audio_manager.sfx_muted = self.temp_settings["sfx_muted"]
        
        # TODO: Aplicar outras configurações
        
        modern_ui.create_notification("Configurações aplicadas!", "success")
        self.changes_made = False
        self.close()
    
    # Callbacks de toggle
    def toggle_music_mute(self):
        self.temp_settings["music_muted"] = not self.temp_settings["music_muted"]
        self.music_mute_button.set_text(
            "🔊 Desmutar Música" if self.temp_settings["music_muted"] else "🔇 Mutar Música"
        )
        self.changes_made = True
    
    def toggle_sfx_mute(self):
        self.temp_settings["sfx_muted"] = not self.temp_settings["sfx_muted"]
        self.sfx_mute_button.set_text(
            "🔊 Desmutar Efeitos" if self.temp_settings["sfx_muted"] else "🔇 Mutar Efeitos"
        )
        self.changes_made = True
    
    def toggle_fullscreen(self):
        self.temp_settings["fullscreen"] = not self.temp_settings["fullscreen"]
        self.fullscreen_button.set_text(
            "✓ Tela Cheia" if self.temp_settings["fullscreen"] else "□ Tela Cheia"
        )
        self.changes_made = True
    
    def toggle_vsync(self):
        self.temp_settings["vsync"] = not self.temp_settings["vsync"]
        self.vsync_button.set_text(
            "✓ VSync" if self.temp_settings["vsync"] else "□ VSync"
        )
        self.changes_made = True
    
    def toggle_particles(self):
        self.temp_settings["particles"] = not self.temp_settings["particles"]
        self.particles_button.set_text(
            "✓ Partículas" if self.temp_settings["particles"] else "□ Partículas"
        )
        self.changes_made = True
    
    def toggle_shadows(self):
        self.temp_settings["shadows"] = not self.temp_settings["shadows"]
        self.shadows_button.set_text(
            "✓ Sombras" if self.temp_settings["shadows"] else "□ Sombras"
        )
        self.changes_made = True
    
    def toggle_show_fps(self):
        self.temp_settings["show_fps"] = not self.temp_settings["show_fps"]
        self.show_fps_button.set_text(
            "✓ Mostrar FPS" if self.temp_settings["show_fps"] else "□ Mostrar FPS"
        )
        self.changes_made = True
    
    def toggle_auto_save(self):
        self.temp_settings["auto_save"] = not self.temp_settings["auto_save"]
        self.auto_save_button.set_text(
            "✓ Auto-Save" if self.temp_settings["auto_save"] else "□ Auto-Save"
        )
        self.changes_made = True
    
    def test_sound(self):
        """Testa o som"""
        audio_manager.play_sound('heal', 'ui')
        modern_ui.create_notification("Som de teste reproduzido!", "info")
    
    def reset_controls(self):
        """Reseta os controles para padrão"""
        defaults = {
            "move_up": "W",
            "move_down": "S",
            "move_left": "A",
            "move_right": "D",
            "attack": "Espaço",
            "dash": "Shift"
        }
        
        for key, value in defaults.items():
            if key in self.control_entries:
                self.control_entries[key].set_text(value)
                self.temp_settings[key] = value
        
        modern_ui.create_notification("Controles resetados!", "info")
        self.changes_made = True