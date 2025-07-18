import pygame
import math
import json
import os
from settings import *
from font_manager import font_manager
from audio_manager import audio_manager
from graphics_manager import GraphicsManager

class SettingsTab:
    """Classe para representar uma aba de configurações"""
    def __init__(self, name, icon, sections):
        self.name = name
        self.icon = icon
        self.sections = sections
        self.active = False

class SettingsSection:
    """Classe para uma seção dentro de uma aba"""
    def __init__(self, title, settings):
        self.title = title
        self.settings = settings

class SettingSetting:
    """Classe para uma configuração individual"""
    def __init__(self, key, display_name, setting_type, value, options=None, min_val=0, max_val=100):
        self.key = key
        self.display_name = display_name
        self.type = setting_type  # 'slider', 'toggle', 'dropdown', 'button'
        self.value = value
        self.options = options or []
        self.min_val = min_val
        self.max_val = max_val
        self.rect = None
        self.hovered = False

class ModernSettingsScreen:
    """Tela de configurações moderna e abrangente"""
    
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.graphics_manager = GraphicsManager()
        
        # Fonts
        self.title_font = font_manager.get('title')
        self.subtitle_font = font_manager.get('subtitle')
        self.text_font = font_manager.get('text')
        self.small_font = font_manager.get('small')
        
        # Colors
        self.colors = {
            'bg': (15, 15, 25),
            'panel': (25, 25, 35, 240),
            'tab_inactive': (40, 40, 50, 200),
            'tab_active': (138, 43, 226, 240),
            'text': (255, 255, 255),
            'text_secondary': (200, 200, 220),
            'text_disabled': (120, 120, 120),
            'accent': (138, 43, 226),
            'accent_hover': (186, 85, 211),
            'button_bg': (60, 60, 70),
            'button_hover': (80, 80, 90),
            'slider_bg': (50, 50, 60),
            'slider_fill': (138, 43, 226),
            'slider_handle': (255, 255, 255),
            'toggle_on': (34, 139, 34),
            'toggle_off': (139, 34, 34),
            'border': (100, 100, 120)
        }
        
        # Configurações persistentes
        self.settings_file = "user_settings.json"
        self.user_settings = self.load_user_settings()
        
        # Layout
        self.tab_height = 60
        self.sidebar_width = 200
        self.content_padding = 20
        
        # Estados
        self.current_tab = 0
        self.scroll_offset = 0
        self.max_scroll = 0
        self.hover_item = None
        self.dragging_slider = None
        
        # Animações
        self.time = 0
        self.tab_transition_progress = 0
        
        # Criar abas
        self.tabs = self.create_tabs()
        
        # Background particles
        self.particles = []
        self.particle_timer = 0
        
    def load_user_settings(self):
        """Carrega configurações do usuário"""
        default_settings = {
            'audio': {
                'master_volume': audio_manager.get_music_volume_percentage(),
                'music_volume': audio_manager.get_music_volume_percentage(),
                'sfx_volume': audio_manager.get_sfx_volume_percentage(),
                'mute': audio_manager.is_muted()
            },
            'graphics': {
                'resolution': '1280x720',
                'fullscreen': False,
                'vsync': True,
                'quality': 'medium',
                'fps_limit': 60,
                'particles': True
            },
            'gameplay': {
                'difficulty': 'normal',
                'auto_save': True,
                'show_fps': False,
                'tutorial_completed': False
            },
            'controls': {
                'movement_keys': 'wasd',
                'attack_key': 'space',
                'run_key': 'shift',
                'menu_key': 'escape'
            }
        }
        
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    loaded = json.load(f)
                    # Merge with defaults
                    for category in default_settings:
                        if category in loaded:
                            default_settings[category].update(loaded[category])
                return default_settings
            except:
                pass
        
        return default_settings
    
    def save_user_settings(self):
        """Salva configurações do usuário"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.user_settings, f, indent=2)
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")
    
    def create_tabs(self):
        """Cria as abas de configurações"""
        return [
            SettingsTab("🎵 ÁUDIO", "🎵", [
                SettingsSection("Volume", [
                    SettingSetting('master_volume', 'Volume Geral', 'slider', 
                                 self.user_settings['audio']['master_volume'], min_val=0, max_val=100),
                    SettingSetting('music_volume', 'Volume da Música', 'slider', 
                                 self.user_settings['audio']['music_volume'], min_val=0, max_val=100),
                    SettingSetting('sfx_volume', 'Volume dos Efeitos', 'slider', 
                                 self.user_settings['audio']['sfx_volume'], min_val=0, max_val=100),
                    SettingSetting('mute', 'Silenciar', 'toggle', 
                                 self.user_settings['audio']['mute'])
                ])
            ]),
            
            SettingsTab("🖥️ GRÁFICOS", "🖥️", [
                SettingsSection("Exibição", [
                    SettingSetting('resolution', 'Resolução', 'dropdown', 
                                 self.user_settings['graphics']['resolution'], 
                                 ['1280x720', '1280x800', '1366x768', '1920x1080', '1920x1200']),
                    SettingSetting('fullscreen', 'Tela Cheia', 'toggle', 
                                 self.user_settings['graphics']['fullscreen']),
                    SettingSetting('vsync', 'VSync', 'toggle', 
                                 self.user_settings['graphics']['vsync'])
                ]),
                SettingsSection("Performance", [
                    SettingSetting('quality', 'Qualidade Gráfica', 'dropdown', 
                                 self.user_settings['graphics']['quality'], 
                                 ['baixa', 'média', 'alta']),
                    SettingSetting('fps_limit', 'Limite de FPS', 'dropdown', 
                                 self.user_settings['graphics']['fps_limit'], 
                                 [30, 60, 120, 144, 'sem limite']),
                    SettingSetting('particles', 'Efeitos de Partículas', 'toggle', 
                                 self.user_settings['graphics']['particles'])
                ])
            ]),
            
            SettingsTab("🎮 GAMEPLAY", "🎮", [
                SettingsSection("Dificuldade", [
                    SettingSetting('difficulty', 'Nível de Dificuldade', 'dropdown', 
                                 self.user_settings['gameplay']['difficulty'], 
                                 ['fácil', 'normal', 'difícil']),
                    SettingSetting('auto_save', 'Salvamento Automático', 'toggle', 
                                 self.user_settings['gameplay']['auto_save'])
                ]),
                SettingsSection("Interface", [
                    SettingSetting('show_fps', 'Mostrar FPS', 'toggle', 
                                 self.user_settings['gameplay']['show_fps']),
                    SettingSetting('tutorial_reset', 'Reiniciar Tutorial', 'button', None)
                ])
            ]),
            
            SettingsTab("⌨️ CONTROLES", "⌨️", [
                SettingsSection("Movimento", [
                    SettingSetting('movement_keys', 'Teclas de Movimento', 'dropdown', 
                                 self.user_settings['controls']['movement_keys'], 
                                 ['wasd', 'setas']),
                    SettingSetting('run_key', 'Tecla de Corrida', 'dropdown', 
                                 self.user_settings['controls']['run_key'], 
                                 ['shift', 'ctrl', 'alt'])
                ]),
                SettingsSection("Ações", [
                    SettingSetting('attack_key', 'Tecla de Ataque', 'dropdown', 
                                 self.user_settings['controls']['attack_key'], 
                                 ['space', 'enter', 'z', 'x']),
                    SettingSetting('menu_key', 'Tecla de Menu', 'dropdown', 
                                 self.user_settings['controls']['menu_key'], 
                                 ['escape', 'tab', 'm'])
                ])
            ])
        ]
    
    def handle_events(self, events):
        """Manipula eventos da tela de configurações"""
        mouse_pos = pygame.mouse.get_pos()
        
        for event in events:
            if event.type == pygame.QUIT:
                return 'quit'
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.save_user_settings()
                    return 'main_menu'
                elif event.key == pygame.K_LEFT and self.current_tab > 0:
                    self.current_tab -= 1
                elif event.key == pygame.K_RIGHT and self.current_tab < len(self.tabs) - 1:
                    self.current_tab += 1
                elif event.key == pygame.K_UP:
                    self.scroll_offset = max(0, self.scroll_offset - 30)
                elif event.key == pygame.K_DOWN:
                    self.scroll_offset = min(self.max_scroll, self.scroll_offset + 30)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    # Check tab clicks
                    if self.handle_tab_click(mouse_pos):
                        continue
                    
                    # Check setting interactions
                    if self.handle_setting_click(mouse_pos):
                        continue
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging_slider = None
            
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging_slider:
                    self.handle_slider_drag(mouse_pos)
                
                # Update hover states
                self.update_hover_states(mouse_pos)
            
            elif event.type == pygame.MOUSEWHEEL:
                # Scroll content
                scroll_speed = 30
                self.scroll_offset -= event.y * scroll_speed
                self.scroll_offset = max(0, min(self.max_scroll, self.scroll_offset))
        
        return 'settings'
    
    def handle_tab_click(self, mouse_pos):
        """Manipula cliques nas abas"""
        tab_y = 100
        for i, tab in enumerate(self.tabs):
            tab_rect = pygame.Rect(50, tab_y + i * (self.tab_height + 10), self.sidebar_width - 20, self.tab_height)
            if tab_rect.collidepoint(mouse_pos):
                self.current_tab = i
                return True
        return False
    
    def handle_setting_click(self, mouse_pos):
        """Manipula cliques em configurações"""
        current_tab = self.tabs[self.current_tab]
        y_offset = 150 - self.scroll_offset
        
        for section in current_tab.sections:
            y_offset += 50  # Section header
            
            for setting in section.settings:
                setting_rect = pygame.Rect(self.sidebar_width + 50, y_offset, 600, 40)
                
                if setting_rect.collidepoint(mouse_pos):
                    return self.handle_setting_interaction(setting, mouse_pos, setting_rect)
                
                y_offset += 60
        
        return False
    
    def handle_setting_interaction(self, setting, mouse_pos, setting_rect):
        """Manipula interação com uma configuração específica"""
        if setting.type == 'toggle':
            setting.value = not setting.value
            self.apply_setting_change(setting)
            return True
        
        elif setting.type == 'slider':
            # Check if clicking on slider
            slider_rect = pygame.Rect(setting_rect.x + 200, setting_rect.y + 15, 200, 10)
            if slider_rect.collidepoint(mouse_pos):
                self.dragging_slider = setting
                self.handle_slider_drag(mouse_pos)
                return True
        
        elif setting.type == 'dropdown':
            # Cycle through options
            if setting.options:
                current_index = 0
                try:
                    current_index = setting.options.index(setting.value)
                except ValueError:
                    pass
                
                next_index = (current_index + 1) % len(setting.options)
                setting.value = setting.options[next_index]
                self.apply_setting_change(setting)
                return True
        
        elif setting.type == 'button':
            self.handle_button_click(setting)
            return True
        
        return False
    
    def handle_slider_drag(self, mouse_pos):
        """Manipula arrastar de slider"""
        if not self.dragging_slider:
            return
        
        setting = self.dragging_slider
        slider_x = self.sidebar_width + 250
        slider_width = 200
        
        # Calculate value based on mouse position
        relative_x = mouse_pos[0] - slider_x
        percentage = max(0, min(1, relative_x / slider_width))
        setting.value = int(setting.min_val + percentage * (setting.max_val - setting.min_val))
        
        self.apply_setting_change(setting)
    
    def apply_setting_change(self, setting):
        """Aplica mudança de configuração"""
        # Update user settings
        category = None
        for tab in self.tabs:
            for section in tab.sections:
                if setting in section.settings:
                    if "ÁUDIO" in tab.name:
                        category = 'audio'
                    elif "GRÁFICOS" in tab.name:
                        category = 'graphics'
                    elif "GAMEPLAY" in tab.name:
                        category = 'gameplay'
                    elif "CONTROLES" in tab.name:
                        category = 'controls'
                    break
        
        if category:
            self.user_settings[category][setting.key] = setting.value
        
        # Apply changes immediately
        if setting.key == 'master_volume' or setting.key == 'music_volume':
            audio_manager.set_music_volume(setting.value / 100.0)
        elif setting.key == 'sfx_volume':
            audio_manager.set_sfx_volume(setting.value / 100.0)
        elif setting.key == 'mute':
            if setting.value:
                audio_manager.toggle_mute()  # Mute
            else:
                # Unmute - toggle only if currently muted
                if audio_manager.is_muted():
                    audio_manager.toggle_mute()
        elif setting.key == 'fullscreen':
            self.graphics_manager.set_fullscreen(setting.value)
        elif setting.key == 'resolution':
            width, height = map(int, setting.value.split('x'))
            self.graphics_manager.set_resolution(width, height)
    
    def handle_button_click(self, setting):
        """Manipula clique em botão"""
        if setting.key == 'tutorial_reset':
            # Reset tutorial
            print("Tutorial reiniciado!")
    
    def update_hover_states(self, mouse_pos):
        """Atualiza estados de hover"""
        self.hover_item = None
        
        # Check tabs
        tab_y = 100
        for i, tab in enumerate(self.tabs):
            tab_rect = pygame.Rect(50, tab_y + i * (self.tab_height + 10), self.sidebar_width - 20, self.tab_height)
            if tab_rect.collidepoint(mouse_pos):
                self.hover_item = f"tab_{i}"
        
        # Check settings
        current_tab = self.tabs[self.current_tab]
        y_offset = 150 - self.scroll_offset
        
        for section in current_tab.sections:
            y_offset += 50
            for setting in section.settings:
                setting_rect = pygame.Rect(self.sidebar_width + 50, y_offset, 600, 40)
                if setting_rect.collidepoint(mouse_pos):
                    self.hover_item = f"setting_{setting.key}"
                y_offset += 60
    
    def update(self, dt):
        """Atualiza animações"""
        self.time += dt
        
        # Update particles
        self.particle_timer += dt
        if self.particle_timer > 100:
            self.add_particle()
            self.particle_timer = 0
        
        # Update particles
        updated_particles = []
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['life'] -= 1
            if p['life'] > 0:
                updated_particles.append(p)
        self.particles = updated_particles
        
        # Calculate max scroll
        current_tab = self.tabs[self.current_tab]
        content_height = sum(50 + len(section.settings) * 60 for section in current_tab.sections)
        visible_height = HEIGTH - 200
        self.max_scroll = max(0, content_height - visible_height)
    
    def add_particle(self):
        """Adiciona partícula de fundo"""
        if len(self.particles) < 20:
            self.particles.append({
                'x': random.randint(0, WIDTH),
                'y': HEIGTH + 10,
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(-1, -0.5),
                'size': random.uniform(1, 3),
                'life': 200,
                'color': random.choice([(138, 43, 226), (186, 85, 211), (255, 215, 0)])
            })
    
    def draw(self):
        """Desenha a tela de configurações"""
        # Background
        self.display_surface.fill(self.colors['bg'])
        
        # Draw particles
        for particle in self.particles:
            alpha = int(255 * (particle['life'] / 200))
            color = (*particle['color'], alpha)
            s = pygame.Surface((int(particle['size'] * 2), int(particle['size'] * 2)), pygame.SRCALPHA)
            pygame.draw.circle(s, color, (int(particle['size']), int(particle['size'])), int(particle['size']))
            self.display_surface.blit(s, (int(particle['x']), int(particle['y'])))
        
        # Title
        title_text = "⚙️ CONFIGURAÇÕES"
        title_surface = self.title_font.render(title_text, True, self.colors['text'])
        title_rect = title_surface.get_rect(center=(WIDTH // 2, 50))
        self.display_surface.blit(title_surface, title_rect)
        
        # Draw tabs (sidebar)
        self.draw_tabs()
        
        # Draw content
        self.draw_content()
        
        # Instructions
        instructions = [
            "ESC - Voltar ao Menu | ←→ - Trocar Abas | ↑↓ - Rolar",
            "CLIQUE - Interagir | ARRASTE - Sliders"
        ]
        
        y_offset = HEIGTH - 60
        for instruction in instructions:
            inst_surface = self.small_font.render(instruction, True, self.colors['text_secondary'])
            inst_rect = inst_surface.get_rect(center=(WIDTH // 2, y_offset))
            self.display_surface.blit(inst_surface, inst_rect)
            y_offset += 25
    
    def draw_tabs(self):
        """Desenha as abas laterais"""
        tab_y = 100
        
        for i, tab in enumerate(self.tabs):
            is_active = i == self.current_tab
            is_hovered = self.hover_item == f"tab_{i}"
            
            # Tab background
            tab_rect = pygame.Rect(50, tab_y, self.sidebar_width - 20, self.tab_height)
            
            if is_active:
                color = self.colors['tab_active']
            elif is_hovered:
                color = (*self.colors['accent_hover'][:3], 200)
            else:
                color = self.colors['tab_inactive']
            
            # Draw tab
            tab_surface = pygame.Surface((tab_rect.width, tab_rect.height), pygame.SRCALPHA)
            tab_surface.fill(color)
            pygame.draw.rect(tab_surface, self.colors['border'], (0, 0, tab_rect.width, tab_rect.height), 2, border_radius=10)
            self.display_surface.blit(tab_surface, tab_rect.topleft)
            
            # Tab text
            text_color = self.colors['text'] if is_active else self.colors['text_secondary']
            tab_surface = self.text_font.render(tab.name, True, text_color)
            text_rect = tab_surface.get_rect(center=tab_rect.center)
            self.display_surface.blit(tab_surface, text_rect)
            
            tab_y += self.tab_height + 10
    
    def draw_content(self):
        """Desenha o conteúdo da aba atual"""
        current_tab = self.tabs[self.current_tab]
        
        # Content area
        content_rect = pygame.Rect(self.sidebar_width + 20, 120, WIDTH - self.sidebar_width - 40, HEIGTH - 200)
        content_surface = pygame.Surface((content_rect.width, content_rect.height), pygame.SRCALPHA)
        content_surface.fill(self.colors['panel'])
        pygame.draw.rect(content_surface, self.colors['border'], (0, 0, content_rect.width, content_rect.height), 2, border_radius=15)
        self.display_surface.blit(content_surface, content_rect.topleft)
        
        # Draw sections
        y_offset = 150 - self.scroll_offset
        
        for section in current_tab.sections:
            # Section header
            section_surface = self.subtitle_font.render(section.title, True, self.colors['accent'])
            self.display_surface.blit(section_surface, (self.sidebar_width + 50, y_offset))
            y_offset += 50
            
            # Section settings
            for setting in section.settings:
                if y_offset > 100 and y_offset < HEIGTH - 100:  # Only draw visible items
                    self.draw_setting(setting, self.sidebar_width + 50, y_offset)
                y_offset += 60
    
    def draw_setting(self, setting, x, y):
        """Desenha uma configuração individual"""
        is_hovered = self.hover_item == f"setting_{setting.key}"
        
        # Setting background
        if is_hovered:
            bg_surface = pygame.Surface((600, 40), pygame.SRCALPHA)
            bg_surface.fill((*self.colors['accent'], 50))
            self.display_surface.blit(bg_surface, (x, y))
        
        # Setting name
        name_surface = self.text_font.render(setting.display_name, True, self.colors['text'])
        self.display_surface.blit(name_surface, (x + 10, y + 10))
        
        # Setting control
        if setting.type == 'slider':
            self.draw_slider(setting, x + 200, y + 15)
        elif setting.type == 'toggle':
            self.draw_toggle(setting, x + 500, y + 10)
        elif setting.type == 'dropdown':
            self.draw_dropdown(setting, x + 300, y + 5)
        elif setting.type == 'button':
            self.draw_button(setting, x + 400, y + 5)
    
    def draw_slider(self, setting, x, y):
        """Desenha um slider"""
        slider_width = 200
        slider_height = 10
        
        # Background
        pygame.draw.rect(self.display_surface, self.colors['slider_bg'], 
                        (x, y, slider_width, slider_height), border_radius=5)
        
        # Fill
        fill_width = int((setting.value - setting.min_val) / (setting.max_val - setting.min_val) * slider_width)
        pygame.draw.rect(self.display_surface, self.colors['slider_fill'], 
                        (x, y, fill_width, slider_height), border_radius=5)
        
        # Handle
        handle_x = x + fill_width - 5
        pygame.draw.circle(self.display_surface, self.colors['slider_handle'], 
                          (handle_x, y + slider_height // 2), 8)
        
        # Value text
        value_text = f"{setting.value}"
        value_surface = self.small_font.render(value_text, True, self.colors['text'])
        self.display_surface.blit(value_surface, (x + slider_width + 10, y - 3))
    
    def draw_toggle(self, setting, x, y):
        """Desenha um toggle"""
        toggle_width = 50
        toggle_height = 20
        
        # Background
        bg_color = self.colors['toggle_on'] if setting.value else self.colors['toggle_off']
        pygame.draw.rect(self.display_surface, bg_color, 
                        (x, y, toggle_width, toggle_height), border_radius=10)
        
        # Handle
        handle_x = x + toggle_width - 15 if setting.value else x + 5
        pygame.draw.circle(self.display_surface, self.colors['slider_handle'], 
                          (handle_x, y + toggle_height // 2), 8)
    
    def draw_dropdown(self, setting, x, y):
        """Desenha um dropdown"""
        dropdown_width = 150
        dropdown_height = 30
        
        # Background
        pygame.draw.rect(self.display_surface, self.colors['button_bg'], 
                        (x, y, dropdown_width, dropdown_height), border_radius=5)
        pygame.draw.rect(self.display_surface, self.colors['border'], 
                        (x, y, dropdown_width, dropdown_height), 2, border_radius=5)
        
        # Text
        value_text = str(setting.value)
        text_surface = self.small_font.render(value_text, True, self.colors['text'])
        text_rect = text_surface.get_rect(center=(x + dropdown_width // 2, y + dropdown_height // 2))
        self.display_surface.blit(text_surface, text_rect)
        
        # Arrow
        arrow_text = "▼"
        arrow_surface = self.small_font.render(arrow_text, True, self.colors['text'])
        self.display_surface.blit(arrow_surface, (x + dropdown_width - 20, y + 8))
    
    def draw_button(self, setting, x, y):
        """Desenha um botão"""
        button_width = 120
        button_height = 30
        
        # Background
        is_hovered = self.hover_item == f"setting_{setting.key}"
        bg_color = self.colors['button_hover'] if is_hovered else self.colors['button_bg']
        
        pygame.draw.rect(self.display_surface, bg_color, 
                        (x, y, button_width, button_height), border_radius=5)
        pygame.draw.rect(self.display_surface, self.colors['border'], 
                        (x, y, button_width, button_height), 2, border_radius=5)
        
        # Text
        button_text = "EXECUTAR"
        text_surface = self.small_font.render(button_text, True, self.colors['text'])
        text_rect = text_surface.get_rect(center=(x + button_width // 2, y + button_height // 2))
        self.display_surface.blit(text_surface, text_rect)

# Instância global
settings_screen = None

def get_settings_screen():
    global settings_screen
    if settings_screen is None:
        settings_screen = ModernSettingsScreen()
    return settings_screen