"""
Funções auxiliares e utilitárias
"""
import pygame
import os
from typing import List, Dict, Any, Optional


def import_folder(path: str) -> List[pygame.Surface]:
    """
    Importa todos os arquivos de imagem de uma pasta e retorna uma lista de surfaces.
    
    Args:
        path (str): Caminho para a pasta
        
    Returns:
        List[pygame.Surface]: Lista de surfaces carregadas
    """
    surface_list = []
    
    if not os.path.exists(path):
        print(f"Aviso: Pasta não encontrada: {path}")
        return surface_list
    
    for _, __, img_files in os.walk(path):
        for image in sorted(img_files):
            if image.lower().endswith(('.png', '.jpg', '.jpeg')):
                full_path = os.path.join(path, image)
                try:
                    image_surf = pygame.image.load(full_path).convert_alpha()
                    surface_list.append(image_surf)
                except pygame.error as e:
                    print(f"Erro ao carregar {full_path}: {e}")
    
    return surface_list


def import_csv_layout(path: str) -> List[List[str]]:
    """
    Importa um arquivo CSV e retorna uma lista de listas.
    
    Args:
        path (str): Caminho para o arquivo CSV
        
    Returns:
        List[List[str]]: Dados do CSV como lista de listas
    """
    terrain_map = []
    
    if not os.path.exists(path):
        print(f"Aviso: Arquivo CSV não encontrado: {path}")
        return terrain_map
    
    try:
        with open(path) as level_map:
            layout = level_map.read().split('\n')
            for row in layout:
                terrain_map.append(row.split(','))
    except Exception as e:
        print(f"Erro ao importar CSV {path}: {e}")
    
    return terrain_map


def clamp(value: float, min_value: float, max_value: float) -> float:
    """
    Limita um valor entre min e max.
    
    Args:
        value (float): Valor a ser limitado
        min_value (float): Valor mínimo
        max_value (float): Valor máximo
        
    Returns:
        float: Valor limitado
    """
    return max(min_value, min(value, max_value))


def lerp(start: float, end: float, t: float) -> float:
    """
    Interpolação linear entre dois valores.
    
    Args:
        start (float): Valor inicial
        end (float): Valor final
        t (float): Fator de interpolação (0-1)
        
    Returns:
        float: Valor interpolado
    """
    return start + (end - start) * clamp(t, 0, 1)


def distance(pos1: tuple, pos2: tuple) -> float:
    """
    Calcula a distância entre dois pontos.
    
    Args:
        pos1 (tuple): Primeira posição (x, y)
        pos2 (tuple): Segunda posição (x, y)
        
    Returns:
        float: Distância entre os pontos
    """
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5


def normalize_vector(vector: pygame.math.Vector2) -> pygame.math.Vector2:
    """
    Normaliza um vetor 2D.
    
    Args:
        vector (pygame.math.Vector2): Vetor a ser normalizado
        
    Returns:
        pygame.math.Vector2: Vetor normalizado
    """
    if vector.magnitude() != 0:
        return vector.normalize()
    return vector


def load_image(path: str, convert_alpha: bool = True) -> Optional[pygame.Surface]:
    """
    Carrega uma imagem com tratamento de erro.
    
    Args:
        path (str): Caminho para a imagem
        convert_alpha (bool): Se deve converter com alpha
        
    Returns:
        Optional[pygame.Surface]: Surface carregada ou None se erro
    """
    try:
        if convert_alpha:
            return pygame.image.load(path).convert_alpha()
        else:
            return pygame.image.load(path).convert()
    except pygame.error as e:
        print(f"Erro ao carregar imagem {path}: {e}")
        return None


def load_sound(path: str) -> Optional[pygame.mixer.Sound]:
    """
    Carrega um som com tratamento de erro.
    
    Args:
        path (str): Caminho para o som
        
    Returns:
        Optional[pygame.mixer.Sound]: Som carregado ou None se erro
    """
    try:
        return pygame.mixer.Sound(path)
    except pygame.error as e:
        print(f"Erro ao carregar som {path}: {e}")
        return None


def create_gradient_surface(width: int, height: int, 
                          start_color: tuple, end_color: tuple, 
                          vertical: bool = True) -> pygame.Surface:
    """
    Cria uma surface com gradiente.
    
    Args:
        width (int): Largura da surface
        height (int): Altura da surface
        start_color (tuple): Cor inicial (R, G, B)
        end_color (tuple): Cor final (R, G, B)
        vertical (bool): Se o gradiente é vertical
        
    Returns:
        pygame.Surface: Surface com gradiente
    """
    surface = pygame.Surface((width, height))
    
    if vertical:
        for y in range(height):
            t = y / height
            color = (
                lerp(start_color[0], end_color[0], t),
                lerp(start_color[1], end_color[1], t),
                lerp(start_color[2], end_color[2], t)
            )
            pygame.draw.line(surface, color, (0, y), (width, y))
    else:
        for x in range(width):
            t = x / width
            color = (
                lerp(start_color[0], end_color[0], t),
                lerp(start_color[1], end_color[1], t),
                lerp(start_color[2], end_color[2], t)
            )
            pygame.draw.line(surface, color, (x, 0), (x, height))
    
    return surface


def format_time(seconds: float) -> str:
    """
    Formata tempo em segundos para string legível.
    
    Args:
        seconds (float): Tempo em segundos
        
    Returns:
        str: Tempo formatado (MM:SS)
    """
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"


def safe_divide(numerator: float, denominator: float, default: float = 0) -> float:
    """
    Divisão segura que evita divisão por zero.
    
    Args:
        numerator (float): Numerador
        denominator (float): Denominador
        default (float): Valor padrão se denominator for 0
        
    Returns:
        float: Resultado da divisão ou valor padrão
    """
    return numerator / denominator if denominator != 0 else default