import pygame
import os
from typing import Dict, Optional

class FontManager:
    """Gerenciador de fontes do jogo com fallback para fontes mais legíveis"""
    
    def __init__(self):
        self.fonts = {}
        self.font_paths = {
            'pixel': '../graphics/font/PressStart2P.ttf',
            'joystix': '../graphics/font/joystix.ttf'
        }
        
        # Fontes do sistema mais legíveis (em ordem de preferência)
        self.system_fonts = [
            'DejaVu Sans',
            'Arial',
            'Helvetica',
            'Liberation Sans',
            'Ubuntu',
            'Segoe UI',
            'Tahoma',
            'Verdana',
            'sans-serif'
        ]
        
        # Inicializar pygame fonts
        pygame.font.init()
        
        # Configurar fontes padrão
        self.setup_default_fonts()
    
    def setup_default_fonts(self):
        """Configura as fontes padrão do jogo"""
        # Encontrar a melhor fonte do sistema
        best_system_font = self.find_best_system_font()
        
        # Configurar diferentes tamanhos e estilos
        self.fonts = {
            'title': self.get_font(best_system_font, 32, bold=True),
            'subtitle': self.get_font(best_system_font, 20, bold=True),
            'button': self.get_font(best_system_font, 16, bold=True),
            'text': self.get_font(best_system_font, 14),
            'small': self.get_font(best_system_font, 12),
            'tiny': self.get_font(best_system_font, 10),
            'ui': self.get_font(best_system_font, 16, bold=True),
            'menu': self.get_font(best_system_font, 18, bold=True),
            'stats': self.get_font(best_system_font, 14),
            'input': self.get_font(best_system_font, 16),
            'achievement': self.get_font(best_system_font, 12, bold=True),
            'pixel_title': self.get_font_from_file('pixel', 24),  # Mantém pixel para título se quiser
            'pixel_small': self.get_font_from_file('pixel', 10)   # Pixel pequeno para detalhes
        }
        
        print(f"✅ Fontes configuradas usando: {best_system_font}")
    
    def find_best_system_font(self) -> str:
        """Encontra a melhor fonte do sistema disponível"""
        available_fonts = pygame.font.get_fonts()
        
        for font_name in self.system_fonts:
            # Normalizar nome da fonte
            normalized_name = font_name.lower().replace(' ', '')
            
            # Procurar fonte similar
            for available_font in available_fonts:
                if normalized_name in available_font.lower():
                    return available_font
        
        # Se não encontrar nenhuma, usar a fonte padrão do sistema
        return pygame.font.get_default_font()
    
    def get_font(self, font_name: str, size: int, bold: bool = False) -> pygame.font.Font:
        """Cria uma fonte do sistema"""
        try:
            font = pygame.font.SysFont(font_name, size, bold=bold)
            return font
        except:
            # Fallback para fonte padrão
            return pygame.font.Font(None, size)
    
    def get_font_from_file(self, font_key: str, size: int) -> pygame.font.Font:
        """Carrega fonte de arquivo"""
        try:
            if font_key in self.font_paths:
                font_path = self.font_paths[font_key]
                if os.path.exists(font_path):
                    return pygame.font.Font(font_path, size)
            # Fallback para fonte padrão
            return pygame.font.Font(None, size)
        except:
            return pygame.font.Font(None, size)
    
    def get(self, font_type: str) -> pygame.font.Font:
        """Retorna uma fonte configurada"""
        return self.fonts.get(font_type, self.fonts['text'])
    
    def create_custom_font(self, font_name: str, size: int, bold: bool = False) -> pygame.font.Font:
        """Cria uma fonte personalizada"""
        return self.get_font(font_name, size, bold)
    
    def get_available_fonts(self) -> list:
        """Retorna lista de fontes disponíveis no sistema"""
        return pygame.font.get_fonts()
    
    def print_available_fonts(self):
        """Imprime todas as fontes disponíveis (para debug)"""
        fonts = self.get_available_fonts()
        print("🔤 Fontes disponíveis no sistema:")
        for i, font in enumerate(fonts[:20]):  # Mostrar apenas as primeiras 20
            print(f"  {i+1}. {font}")
        if len(fonts) > 20:
            print(f"  ... e mais {len(fonts) - 20} fontes")

# Instância singleton
font_manager = FontManager()