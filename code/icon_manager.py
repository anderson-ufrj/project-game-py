"""
Sistema de gerenciamento de ícones profissionais para a interface
Suporta emojis, ícones PNG, fontes de ícones e renderização vetorial avançada
"""
import pygame
import os
from typing import Dict, Tuple, Optional
from PIL import Image, ImageDraw, ImageFont
import io

# Importar sistema avançado de ícones
try:
    from advanced_icons import advanced_icon_renderer
    ADVANCED_ICONS_AVAILABLE = True
except ImportError:
    ADVANCED_ICONS_AVAILABLE = False
    print("⚠️ Sistema avançado de ícones não disponível")

class IconManager:
    """Gerenciador de ícones profissionais para interface"""
    
    def __init__(self):
        self.icons_cache = {}
        self.emoji_font = None
        self.icon_font = None
        self._load_fonts()
        
        # Emojis Unicode para diferentes controles
        self.emoji_map = {
            'volume_high': '🔊',
            'volume_medium': '🔉', 
            'volume_low': '🔈',
            'volume_mute': '🔇',
            'fullscreen': '⛶',
            'windowed': '🗖',
            'settings': '⚙️',
            'music': '🎵',
            'sound': '🔊',
            'play': '▶️',
            'pause': '⏸️',
            'stop': '⏹️',
            'close': '❌',
            'minimize': '➖',
            'maximize': '🗖',
            'speaker': '🎤',
            'headphones': '🎧',
            'equalizer': '🎛️'
        }
        
        # Códigos de ícones estilo Font Awesome
        self.icon_codes = {
            'volume_high': '\uf028',
            'volume_medium': '\uf027',
            'volume_low': '\uf026', 
            'volume_mute': '\uf6a9',
            'fullscreen': '\uf065',
            'windowed': '\uf066',
            'settings': '\uf013',
            'music': '\uf001',
            'sound': '\uf028',
            'play': '\uf04b',
            'pause': '\uf04c',
            'stop': '\uf04d'
        }
        
    def _load_fonts(self):
        """Carrega fontes para emojis e ícones"""
        # Tentar carregar fonte de emojis do sistema
        emoji_fonts = [
            '/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf',
            '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
            '/System/Library/Fonts/Apple Color Emoji.ttc',
            'C:\\Windows\\Fonts\\seguiemj.ttf'
        ]
        
        for font_path in emoji_fonts:
            if os.path.exists(font_path):
                try:
                    self.emoji_font = pygame.font.Font(font_path, 24)
                    print(f"✅ Fonte de emojis carregada: {font_path}")
                    break
                except pygame.error:
                    continue
        
        # Fallback para fonte do sistema
        if not self.emoji_font:
            self.emoji_font = pygame.font.SysFont('Arial', 24)
            print("⚠️ Usando fonte do sistema para emojis")
    
    def get_icon(self, icon_name: str, size: int = 24, color: Tuple[int, int, int] = (255, 255, 255)) -> pygame.Surface:
        """
        Obtém ícone com tamanho e cor especificados
        
        Args:
            icon_name: Nome do ícone (ex: 'volume_high', 'fullscreen')
            size: Tamanho em pixels
            color: Cor do ícone (R, G, B)
            
        Returns:
            pygame.Surface: Surface com o ícone
        """
        cache_key = f"{icon_name}_{size}_{color}"
        
        if cache_key in self.icons_cache:
            return self.icons_cache[cache_key]
        
        # Tentar diferentes métodos de criação (ordem de preferência)
        icon_surface = None
        
        # Método 1: Renderizador avançado (preferido)
        if ADVANCED_ICONS_AVAILABLE:
            icon_surface = self._create_advanced_icon(icon_name, size, color)
        
        # Método 2: Emoji Unicode
        if not icon_surface and icon_name in self.emoji_map:
            icon_surface = self._create_emoji_icon(icon_name, size, color)
        
        # Método 3: Ícone vetorial customizado
        if not icon_surface:
            icon_surface = self._create_vector_icon(icon_name, size, color)
        
        # Método 4: Fallback para ícone básico melhorado
        if not icon_surface:
            icon_surface = self._create_basic_icon(icon_name, size, color)
        
        # Cache o resultado
        self.icons_cache[cache_key] = icon_surface
        return icon_surface
    
    def _create_advanced_icon(self, icon_name: str, size: int, color: Tuple[int, int, int]) -> Optional[pygame.Surface]:
        """Cria ícone usando renderizador avançado"""
        if not ADVANCED_ICONS_AVAILABLE:
            return None
        
        try:
            if icon_name.startswith('volume_'):
                level = icon_name.split('_')[1]  # high, medium, low, mute
                return advanced_icon_renderer.create_volume_icon(size, color, level, glow=True)
            
            elif icon_name == 'fullscreen':
                return advanced_icon_renderer.create_fullscreen_icon(size, color, False, 'arrows')
            
            elif icon_name == 'windowed':
                return advanced_icon_renderer.create_fullscreen_icon(size, color, True, 'arrows')
            
            elif icon_name == 'settings':
                return advanced_icon_renderer.create_settings_icon(size, color, 0, 'gear')
            
            return None
            
        except Exception as e:
            print(f"❌ Erro ao criar ícone avançado {icon_name}: {e}")
            return None
    
    def _create_emoji_icon(self, icon_name: str, size: int, color: Tuple[int, int, int]) -> Optional[pygame.Surface]:
        """Cria ícone usando emoji Unicode"""
        if icon_name not in self.emoji_map:
            return None
            
        try:
            # Ajustar fonte para o tamanho desejado
            font = pygame.font.Font(None, int(size * 1.2))
            
            # Renderizar emoji
            emoji = self.emoji_map[icon_name]
            text_surface = font.render(emoji, True, color)
            
            # Centralizar em surface do tamanho correto
            icon_surface = pygame.Surface((size, size), pygame.SRCALPHA)
            text_rect = text_surface.get_rect(center=(size//2, size//2))
            icon_surface.blit(text_surface, text_rect)
            
            return icon_surface
            
        except Exception as e:
            print(f"❌ Erro ao criar emoji icon {icon_name}: {e}")
            return None
    
    def _create_vector_icon(self, icon_name: str, size: int, color: Tuple[int, int, int]) -> Optional[pygame.Surface]:
        """Cria ícone vetorial usando PIL"""
        try:
            # Criar imagem PIL
            img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Desenhar ícones vetoriais melhorados
            if icon_name == 'volume_high':
                self._draw_volume_icon(draw, size, color, 'high')
            elif icon_name == 'volume_medium':
                self._draw_volume_icon(draw, size, color, 'medium')
            elif icon_name == 'volume_low':
                self._draw_volume_icon(draw, size, color, 'low')
            elif icon_name == 'volume_mute':
                self._draw_volume_icon(draw, size, color, 'mute')
            elif icon_name == 'fullscreen':
                self._draw_fullscreen_icon(draw, size, color, True)
            elif icon_name == 'windowed':
                self._draw_fullscreen_icon(draw, size, color, False)
            elif icon_name == 'settings':
                self._draw_settings_icon(draw, size, color)
            else:
                return None
            
            # Converter PIL para pygame
            img_str = img.tobytes()
            icon_surface = pygame.image.fromstring(img_str, (size, size), 'RGBA')
            
            return icon_surface
            
        except Exception as e:
            print(f"❌ Erro ao criar vector icon {icon_name}: {e}")
            return None
    
    def _draw_volume_icon(self, draw, size: int, color: Tuple[int, int, int], level: str):
        """Desenha ícone de volume vetorial"""
        center = size // 2
        
        # Alto-falante base
        speaker_width = size // 6
        speaker_height = size // 3
        speaker_x = center - size // 3
        speaker_y = center - speaker_height // 2
        
        # Corpo do alto-falante
        draw.rectangle([speaker_x, speaker_y, speaker_x + speaker_width, speaker_y + speaker_height], 
                      fill=color)
        
        # Cone do alto-falante
        cone_points = [
            (speaker_x + speaker_width, speaker_y),
            (speaker_x + speaker_width + size//4, speaker_y - size//6),
            (speaker_x + speaker_width + size//4, speaker_y + speaker_height + size//6),
            (speaker_x + speaker_width, speaker_y + speaker_height)
        ]
        draw.polygon(cone_points, fill=color)
        
        # Ondas sonoras baseadas no nível
        if level != 'mute':
            wave_x = speaker_x + speaker_width + size//4 + size//8
            
            if level in ['low', 'medium', 'high']:
                # Primeira onda
                draw.arc([wave_x, center - size//6, wave_x + size//6, center + size//6], 
                        -45, 45, fill=color, width=2)
            
            if level in ['medium', 'high']:
                # Segunda onda
                draw.arc([wave_x + size//12, center - size//4, wave_x + size//4, center + size//4], 
                        -45, 45, fill=color, width=2)
            
            if level == 'high':
                # Terceira onda
                draw.arc([wave_x + size//6, center - size//3, wave_x + size//3, center + size//3], 
                        -45, 45, fill=color, width=2)
        else:
            # X para mute
            x_size = size // 4
            x_center = speaker_x + speaker_width + size//4 + size//8
            draw.line([x_center - x_size//2, center - x_size//2, 
                      x_center + x_size//2, center + x_size//2], fill=color, width=3)
            draw.line([x_center - x_size//2, center + x_size//2, 
                      x_center + x_size//2, center - x_size//2], fill=color, width=3)
    
    def _draw_fullscreen_icon(self, draw, size: int, color: Tuple[int, int, int], is_fullscreen: bool):
        """Desenha ícone de fullscreen/windowed"""
        center = size // 2
        arrow_size = size // 6
        margin = size // 4
        
        if is_fullscreen:
            # Setas para fora (fullscreen)
            positions = [
                (margin, margin),  # Canto superior esquerdo
                (size - margin, margin),  # Canto superior direito
                (margin, size - margin),  # Canto inferior esquerdo
                (size - margin, size - margin)  # Canto inferior direito
            ]
            
            directions = [
                [(-1, -1), (-1, 0), (0, -1)],  # Seta para cima-esquerda
                [(1, -1), (1, 0), (0, -1)],   # Seta para cima-direita
                [(-1, 1), (-1, 0), (0, 1)],   # Seta para baixo-esquerda
                [(1, 1), (1, 0), (0, 1)]      # Seta para baixo-direita
            ]
        else:
            # Setas para dentro (windowed)
            positions = [
                (center - arrow_size, center - arrow_size),
                (center + arrow_size, center - arrow_size),
                (center - arrow_size, center + arrow_size),
                (center + arrow_size, center + arrow_size)
            ]
            
            directions = [
                [(1, 1), (1, 0), (0, 1)],     # Seta para baixo-direita
                [(-1, 1), (-1, 0), (0, 1)],   # Seta para baixo-esquerda
                [(1, -1), (1, 0), (0, -1)],   # Seta para cima-direita
                [(-1, -1), (-1, 0), (0, -1)]  # Seta para cima-esquerda
            ]
        
        # Desenhar setas
        for pos, dirs in zip(positions, directions):
            x, y = pos
            for dx, dy in dirs:
                end_x = x + dx * arrow_size
                end_y = y + dy * arrow_size
                draw.line([x, y, end_x, end_y], fill=color, width=2)
    
    def _draw_settings_icon(self, draw, size: int, color: Tuple[int, int, int]):
        """Desenha ícone de configurações (engrenagem)"""
        center = size // 2
        outer_radius = size // 2 - 2
        inner_radius = size // 4
        teeth_count = 8
        
        import math
        
        # Pontos da engrenagem
        points = []
        for i in range(teeth_count * 2):
            angle = 2 * math.pi * i / (teeth_count * 2)
            if i % 2 == 0:
                # Ponto externo
                x = center + outer_radius * math.cos(angle)
                y = center + outer_radius * math.sin(angle)
            else:
                # Ponto interno
                x = center + (outer_radius * 0.8) * math.cos(angle)
                y = center + (outer_radius * 0.8) * math.sin(angle)
            points.append((x, y))
        
        # Desenhar engrenagem
        draw.polygon(points, fill=color)
        
        # Furo central
        draw.ellipse([center - inner_radius, center - inner_radius, 
                     center + inner_radius, center + inner_radius], 
                    fill=(0, 0, 0, 0))
    
    def _create_basic_icon(self, icon_name: str, size: int, color: Tuple[int, int, int]) -> pygame.Surface:
        """Cria ícone básico melhorado como fallback"""
        icon_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        center = size // 2
        
        if icon_name.startswith('volume'):
            # Ícone de volume melhorado
            # Alto-falante
            pygame.draw.rect(icon_surface, color, (center-size//3, center-size//6, size//6, size//3))
            pygame.draw.polygon(icon_surface, color, [
                (center-size//6, center-size//6),
                (center, center-size//3),
                (center, center+size//3),
                (center-size//6, center+size//6)
            ])
            
            # Ondas baseadas no tipo
            if icon_name != 'volume_mute':
                wave_count = 1 if 'low' in icon_name else 2 if 'medium' in icon_name else 3
                for i in range(wave_count):
                    radius = size//4 + i * size//8
                    pygame.draw.arc(icon_surface, color, 
                                  (center-radius//2, center-radius//2, radius, radius),
                                  -45, 45, 2)
            else:
                # X para mute
                pygame.draw.line(icon_surface, color, 
                               (center+size//8, center-size//8), (center+size//4, center), 3)
                pygame.draw.line(icon_surface, color, 
                               (center+size//8, center), (center+size//4, center-size//8), 3)
        
        elif icon_name == 'fullscreen':
            # Setas para os cantos
            arrow_size = size//6
            for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
                x, y = center + dx * size//4, center + dy * size//4
                pygame.draw.lines(icon_surface, color, False, [
                    (x, y + dy * arrow_size),
                    (x, y),
                    (x + dx * arrow_size, y)
                ], 2)
        
        elif icon_name == 'windowed':
            # Setas para dentro
            arrow_size = size//6
            for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
                x, y = center + dx * size//6, center + dy * size//6
                pygame.draw.lines(icon_surface, color, False, [
                    (x - dx * arrow_size, y),
                    (x, y),
                    (x, y - dy * arrow_size)
                ], 2)
        
        elif icon_name == 'settings':
            # Engrenagem simples
            pygame.draw.circle(icon_surface, color, (center, center), size//3, 2)
            pygame.draw.circle(icon_surface, color, (center, center), size//6, 2)
            
            # Dentes da engrenagem
            for i in range(8):
                angle = i * 45
                import math
                x = center + (size//2.5) * math.cos(math.radians(angle))
                y = center + (size//2.5) * math.sin(math.radians(angle))
                pygame.draw.circle(icon_surface, color, (int(x), int(y)), 2)
        
        return icon_surface
    
    def get_volume_icon_by_level(self, volume: float, is_muted: bool = False) -> str:
        """Retorna nome do ícone baseado no nível de volume"""
        if is_muted:
            return 'volume_mute'
        elif volume > 0.66:
            return 'volume_high'
        elif volume > 0.33:
            return 'volume_medium'
        else:
            return 'volume_low'

# Instância global
icon_manager = IconManager()