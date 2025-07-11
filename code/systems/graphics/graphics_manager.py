import pygame
import json
import os

class GraphicsManager:
    """Singleton para gerenciar configurações gráficas do jogo."""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GraphicsManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self.config_file = 'graphics_settings.json'
            self.default_settings = {
                'resolution': '1280x800',
                'fullscreen': False,
                'vsync': True,
                'quality': 'high',
                'fps_limit': 60
            }
            
            # Resoluções suportadas
            self.supported_resolutions = [
                '1280x720',
                '1280x800', 
                '1366x768',
                '1920x1080',
                '1920x1200',
                'custom'
            ]
            
            # Configurações de qualidade
            self.quality_settings = {
                'low': {
                    'particles_enabled': False,
                    'shadows_enabled': False,
                    'effects_quality': 0.5
                },
                'medium': {
                    'particles_enabled': True,
                    'shadows_enabled': False,
                    'effects_quality': 0.75
                },
                'high': {
                    'particles_enabled': True,
                    'shadows_enabled': True,
                    'effects_quality': 1.0
                }
            }
            
            self.settings = self.load_settings()
            self.screen = None
            GraphicsManager._initialized = True
    
    def load_settings(self):
        """Carrega configurações do arquivo ou usa padrões."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    # Merge com configurações padrão para garantir que todas as chaves existam
                    settings = self.default_settings.copy()
                    settings.update(loaded_settings)
                    return settings
        except Exception as e:
            print(f"Erro ao carregar configurações gráficas: {e}")
        
        return self.default_settings.copy()
    
    def save_settings(self):
        """Salva configurações no arquivo."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar configurações gráficas: {e}")
    
    def get_resolution(self):
        """Retorna a resolução atual como tupla (width, height)."""
        resolution_str = self.settings['resolution']
        if resolution_str == 'custom':
            return (1280, 800)  # Fallback para custom
        
        try:
            width, height = map(int, resolution_str.split('x'))
            return (width, height)
        except:
            return (1280, 800)  # Fallback em caso de erro
    
    def set_resolution(self, resolution_str):
        """Define nova resolução."""
        if resolution_str in self.supported_resolutions:
            self.settings['resolution'] = resolution_str
            self.save_settings()
            return True
        return False
    
    def toggle_fullscreen(self):
        """Alterna entre fullscreen e modo janela."""
        self.settings['fullscreen'] = not self.settings['fullscreen']
        self.save_settings()
        return self.settings['fullscreen']
    
    def set_fullscreen(self, fullscreen):
        """Define modo fullscreen."""
        self.settings['fullscreen'] = fullscreen
        self.save_settings()
    
    def is_fullscreen(self):
        """Retorna se está em modo fullscreen."""
        return self.settings['fullscreen']
    
    def toggle_vsync(self):
        """Alterna V-Sync."""
        self.settings['vsync'] = not self.settings['vsync']
        self.save_settings()
        return self.settings['vsync']
    
    def set_vsync(self, vsync):
        """Define V-Sync."""
        self.settings['vsync'] = vsync
        self.save_settings()
    
    def is_vsync_enabled(self):
        """Retorna se V-Sync está habilitado."""
        return self.settings['vsync']
    
    def set_quality(self, quality):
        """Define qualidade gráfica."""
        if quality in self.quality_settings:
            self.settings['quality'] = quality
            self.save_settings()
            return True
        return False
    
    def get_quality(self):
        """Retorna configuração de qualidade atual."""
        return self.settings['quality']
    
    def get_quality_settings(self):
        """Retorna configurações detalhadas da qualidade atual."""
        quality = self.get_quality()
        return self.quality_settings.get(quality, self.quality_settings['high'])
    
    def set_fps_limit(self, fps):
        """Define limite de FPS."""
        if fps in [30, 60, 120, 144, 0]:  # 0 = sem limite
            self.settings['fps_limit'] = fps
            self.save_settings()
            return True
        return False
    
    def get_fps_limit(self):
        """Retorna limite de FPS atual."""
        return self.settings['fps_limit']
    
    def apply_settings(self):
        """Aplica as configurações gráficas atuais ao pygame."""
        width, height = self.get_resolution()
        flags = 0
        
        if self.is_fullscreen():
            flags |= pygame.FULLSCREEN
        
        if self.is_vsync_enabled():
            flags |= pygame.DOUBLEBUF
        
        try:
            self.screen = pygame.display.set_mode((width, height), flags)
            return True
        except pygame.error as e:
            print(f"Erro ao aplicar configurações gráficas: {e}")
            # Fallback para configurações seguras
            self.screen = pygame.display.set_mode((1280, 800))
            return False
    
    def get_screen(self):
        """Retorna a surface da tela atual."""
        return self.screen
    
    def handle_alt_enter(self):
        """Manipula Alt+Enter para alternar fullscreen."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LALT] or keys[pygame.K_RALT]:
            if pygame.key.get_just_pressed()[pygame.K_RETURN]:
                self.toggle_fullscreen()
                self.apply_settings()
                return True
        return False
    
    def get_display_info(self):
        """Retorna informações sobre o display."""
        info = pygame.display.Info()
        return {
            'desktop_resolution': f"{info.current_w}x{info.current_h}",
            'current_resolution': f"{self.get_resolution()[0]}x{self.get_resolution()[1]}",
            'fullscreen': self.is_fullscreen(),
            'vsync': self.is_vsync_enabled(),
            'quality': self.get_quality(),
            'fps_limit': self.get_fps_limit()
        }