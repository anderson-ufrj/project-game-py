#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Wizarding Duel: Varinha vs Diabretes (Versão Local)
=====================================================

Um jogo mágico inspirado no mundo de Harry Potter:
- Controle uma varinha mágica voadora
- Lance feitiços para repelir os diabretes da Cornualha
- Fundo de galáxia mágica em movimento
- Sistema de pontuação e níveis
- Tela de seleção de personagem para escolher diferentes varinhas e diabretes
- Imagens geradas localmente (sem necessidade de download)
- Tela de Game Over com opção de sair
"""

import os
import sys
import math
import random
import pygame
from pygame.locals import *
from enum import Enum

# Constantes globais
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
MAGIC_BLUE = (65, 105, 225)
CORNISH_BLUE = (0, 150, 255)

# Variáveis globais para tela cheia
fullscreen = False
current_screen = None

# Corrigindo o caminho para as imagens - usando o diretório correto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")  # Diretório de imagens local

# Criar o diretório de imagens se não existir
if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)

# Dicionário para armazenar sprites carregados
loaded_sprites = {}

# Estados do jogo
class GameState(Enum):
    MENU = 0
    CHARACTER_SELECT = 1
    PLAYING = 2
    GAME_OVER = 3
    PAUSED = 4

# Comportamentos dos diabretes
class PixieBehavior(Enum):
    STRAIGHT_DOWN = 0
    LEFT_TO_RIGHT = 1
    RIGHT_TO_LEFT = 2
    ZIGZAG = 3
    CIRCULAR = 4

# Funções para carregar sprites externos
def load_sprite_sheet(filename):
    """Carrega uma sprite sheet e retorna a superfície"""
    try:
        filepath = os.path.join(IMAGES_DIR, filename)
        if os.path.exists(filepath):
            return pygame.image.load(filepath).convert_alpha()
    except Exception as e:
        print(f"Aviso: Não foi possível carregar {filename}: {e}")
    return None

def extract_sprite(sheet, x, y, width, height, scale=1.0):
    """Extrai um sprite de uma sprite sheet"""
    sprite = pygame.Surface((width, height), pygame.SRCALPHA)
    sprite.blit(sheet, (0, 0), (x, y, width, height))
    if scale != 1.0:
        new_width = int(width * scale)
        new_height = int(height * scale)
        sprite = pygame.transform.scale(sprite, (new_width, new_height))
    return sprite

def load_all_sprites():
    """Carrega todos os sprites externos disponíveis"""
    global loaded_sprites
    
    print("Tentando carregar sprites externos...")
    print(f"Diretório de imagens: {IMAGES_DIR}")
    
    # Lista de arquivos de sprite para tentar carregar
    sprite_files = [
        "Designer_sprite_0.png",
        "Designer (1)_sprite_0.png", 
        "Designer (2)_sprite_0.png"
    ]
    
    for filename in sprite_files:
        sheet = load_sprite_sheet(filename)
        if sheet:
            loaded_sprites[filename] = sheet
            print(f"Carregado com sucesso: {filename}")
        else:
            print(f"Não foi possível carregar: {filename}")
    
    # Extrair sprites específicos se as sheets foram carregadas
    if "Designer_sprite_0.png" in loaded_sprites:
        sheet = loaded_sprites["Designer_sprite_0.png"]
        print("Extraindo sprites de Designer_sprite_0.png...")
        # Assumindo que os sprites estão organizados em grid
        # Wizards no topo (64x64 cada)
        for i in range(8):
            loaded_sprites[f"wizard_{i}"] = extract_sprite(sheet, i*64, 0, 64, 64, 0.8)
        # Varinhas no meio (32x32 cada)
        for i in range(8):
            loaded_sprites[f"wand_{i}"] = extract_sprite(sheet, i*64, 128, 64, 64, 0.5)
    
    if "Designer (2)_sprite_0.png" in loaded_sprites:
        sheet = loaded_sprites["Designer (2)_sprite_0.png"]
        print("Extraindo sprites de Designer (2)_sprite_0.png...")
        # Criaturas fofas como inimigos (64x64 cada)
        for i in range(8):
            loaded_sprites[f"pixie_{i}"] = extract_sprite(sheet, i*64, 128, 64, 64, 0.7)
        # Orbs como projéteis (32x32 cada)
        for i in range(4):
            loaded_sprites[f"spell_{i}"] = extract_sprite(sheet, i*64, 256, 64, 64, 0.3)
    
    print(f"Total de sprites carregados: {len(loaded_sprites)}")

# Funções para criar sprites e imagens
def create_wand_image(width=30, height=160, style="classic"):
    """Cria uma imagem de varinha mágica com estilos diferentes"""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Cores para diferentes estilos de varinha
    wand_styles = {
        "classic": [  # Varinha clássica marrom
            (79, 53, 31),  # Marrom escuro
            (101, 67, 33),  # Marrom médio
            (120, 81, 45),  # Marrom claro
            (88, 57, 33)    # Marrom avermelhado
        ],
        "elder": [  # Varinha de Sabugueiro (The Elder Wand)
            (30, 30, 30),  # Quase preto
            (50, 50, 50),  # Cinza escuro
            (70, 70, 70),  # Cinza
            (40, 40, 40)   # Cinza escuro
        ],
        "holly": [  # Varinha de Azevinho (varinha do Harry)
            (60, 40, 20),  # Marrom escuro
            (90, 60, 30),  # Marrom avermelhado
            (110, 70, 40),  # Marrom médio
            (80, 50, 25)    # Marrom
        ],
        "crystal": [  # Varinha de cristal
            (200, 220, 255),  # Azul claro cristalino
            (180, 200, 255),  # Azul cristalino
            (220, 240, 255),  # Branco azulado
            (190, 210, 255)   # Azul cristalino
        ]
    }
    
    # Obtém o esquema de cores para o estilo selecionado
    wand_colors = wand_styles.get(style, wand_styles["classic"])
    
    # Forma da varinha - mais fina e realista
    # Corpo principal (mais fino no topo, gradualmente mais largo para baixo)
    wand_width_top = width // 4
    wand_width_bottom = width // 2
    
    # Desenha o corpo da varinha com gradiente de cor
    for y in range(0, height):
        # Calcula a largura em cada ponto (mais fina no topo)
        progress = y / height
        current_width = wand_width_top + (wand_width_bottom - wand_width_top) * progress
        
        # Adiciona uma leve curva natural à varinha
        curve_offset = math.sin(progress * math.pi) * 4
        
        # Varia a cor ligeiramente ao longo do comprimento
        color_index = int(progress * len(wand_colors))
        if color_index >= len(wand_colors):
            color_index = len(wand_colors) - 1
        
        color = wand_colors[color_index]
        
        # Desenha uma linha horizontal em cada ponto y
        pygame.draw.line(
            surface, 
            color, 
            (width//2 - current_width//2 + curve_offset, y), 
            (width//2 + current_width//2 + curve_offset, y), 
            1
        )
    
    # Adiciona detalhes à varinha
    
    # Ponta mais afilada no topo
    pygame.draw.ellipse(
        surface, 
        wand_colors[0], 
        (width//2 - wand_width_top//2 - 1, 0, wand_width_top + 2, 10)
    )
    
    # Cabo/empunhadura na parte inferior
    handle_top = height - 30
    pygame.draw.rect(
        surface, 
        wand_colors[2], 
        (width//2 - wand_width_bottom//2 - 2, handle_top, wand_width_bottom + 4, 30)
    )
    
    # Detalhes entalhados na empunhadura
    for i in range(5):
        y_pos = handle_top + i * 6
        detail_color = wand_colors[i % 2]  # Alterna cores
        pygame.draw.line(
            surface, 
            detail_color, 
            (width//2 - wand_width_bottom//2 - 2, y_pos), 
            (width//2 + wand_width_bottom//2 + 2, y_pos), 
            1
        )
    
    # Adiciona brilho na ponta da varinha
    glow_radius = 15
    glow_color = (255, 255, 150)  # Padrão amarelo
    
    # Cores de brilho diferentes por estilo
    if style == "elder":
        glow_color = (255, 255, 255)  # Branco para Elder Wand
    elif style == "holly":
        glow_color = (255, 200, 100)  # Dourado suave para Holly
    elif style == "crystal":
        glow_color = (150, 230, 255)  # Azul claro para Crystal
    
    for r in range(glow_radius, 0, -1):
        alpha = 150 - r * 10
        if alpha < 0:
            alpha = 0
        color = (*glow_color, alpha)
        pygame.draw.circle(surface, color, (width // 2, 5), r)
        
    # Adiciona decorações específicas para cada estilo
    if style == "crystal":
        # Adiciona um cristal na ponta
        pygame.draw.polygon(
            surface,
            (220, 240, 255, 200),
            [
                (width//2, 0),
                (width//2 - 7, 15),
                (width//2 + 7, 15)
            ]
        )
    elif style == "holly":
        # Adiciona um pequeno emblema na empunhadura
        circle_y = handle_top + 15
        pygame.draw.circle(surface, (180, 150, 50), (width//2, circle_y), 4)
        pygame.draw.circle(surface, (210, 180, 60), (width//2, circle_y), 2)
    
    return surface

def create_pixie_image(width=60, height=70, style="blue"):
    """Cria uma imagem de diabrete com estilos diferentes"""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Cores para diferentes estilos de diabrete
    pixie_styles = {
        "blue": {
            "body": (0, 150, 255),      # Azul vivo para o corpo
            "dark": (0, 100, 200),      # Azul mais escuro para sombreamento
            "wing": (180, 230, 255, 180)  # Azul claro translúcido para as asas
        },
        "green": {
            "body": (50, 180, 50),      # Verde vivo
            "dark": (30, 130, 30),      # Verde escuro
            "wing": (200, 255, 200, 180)  # Verde claro translúcido
        },
        "fairy": {
            "body": (230, 180, 255),    # Lilás/roxo claro
            "dark": (180, 120, 200),    # Lilás escuro
            "wing": (255, 220, 255, 180)  # Rosa translúcido
        },
        "shadow": {
            "body": (100, 30, 150),     # Roxo escuro
            "dark": (60, 10, 90),       # Roxo muito escuro
            "wing": (150, 100, 200, 180)  # Roxo médio translúcido
        }
    }
    
    # Obtém as cores para o estilo selecionado
    style_colors = pixie_styles.get(style, pixie_styles["blue"])
    pixie_color = style_colors["body"]
    darker_color = style_colors["dark"]
    wing_color = style_colors["wing"]
    
    # Desenha o corpo - mais humanoide com forma corporal clara
    
    # Torso
    torso_rect = pygame.Rect(width//2 - 10, height//3, 20, height//3)
    pygame.draw.ellipse(surface, pixie_color, torso_rect)
    pygame.draw.ellipse(surface, darker_color, torso_rect, 1)  # Contorno
    
    # Cabeça (mais oval, como um diabrete)
    head_width, head_height = 20, 25
    head_rect = pygame.Rect(width//2 - head_width//2, height//6, head_width, head_height)
    pygame.draw.ellipse(surface, pixie_color, head_rect)
    pygame.draw.ellipse(surface, darker_color, head_rect, 1)  # Contorno
    
    # Rosto mais definido
    
    # Olhos grandes e negros (característicos dos diabretes)
    eye_size = 6
    eye_color = BLACK
    
    # Olhos especiais para tipos específicos
    if style == "shadow":
        eye_color = RED  # Olhos vermelhos para diabretes sombrios
    
    pygame.draw.ellipse(surface, eye_color, (width//2 - 9, height//6 + 8, eye_size, eye_size))
    pygame.draw.ellipse(surface, eye_color, (width//2 + 3, height//6 + 8, eye_size, eye_size))
    
    # Reflexos nos olhos
    pygame.draw.ellipse(surface, WHITE, (width//2 - 8, height//6 + 9, 2, 2))
    pygame.draw.ellipse(surface, WHITE, (width//2 + 4, height//6 + 9, 2, 2))
    
    # Sorriso travesso
    smile_color = RED
    if style == "green":
        smile_color = (130, 30, 30)  # Marrom avermelhado
    elif style == "fairy":
        smile_color = (255, 100, 200)  # Rosa
    
    smile_rect = pygame.Rect(width//2 - 7, height//6 + 15, 14, 6)
    pygame.draw.arc(surface, smile_color, smile_rect, 0, math.pi, 2)
    
    # Dentes afiados (característica dos diabretes)
    tooth_color = (240, 240, 240)
    pygame.draw.rect(surface, tooth_color, (width//2 - 5, height//6 + 15, 2, 2))
    pygame.draw.rect(surface, tooth_color, (width//2 + 3, height//6 + 15, 2, 2))
    
    # Orelhas pontudas
    pygame.draw.polygon(surface, pixie_color, [
        (width//2 - head_width//2, height//6 + 10),  # Base esquerda
        (width//2 - head_width//2 - 8, height//6 + 7),  # Ponta
        (width//2 - head_width//2, height//6 + 5)    # Topo
    ])
    pygame.draw.polygon(surface, pixie_color, [
        (width//2 + head_width//2, height//6 + 10),  # Base direita
        (width//2 + head_width//2 + 8, height//6 + 7),  # Ponta
        (width//2 + head_width//2, height//6 + 5)    # Topo
    ])
    
    # Asas grandes e semi-transparentes (característica marcante)
    
    # Asa esquerda
    wing_left_points = [
        (width//2 - 5, height//3 + 5),  # Ponto de conexão
        (width//2 - 35, height//4),     # Ponta superior
        (width//2 - 40, height//3 + 10), # Ponta externa
        (width//2 - 30, height//2),     # Ponta inferior
        (width//2 - 10, height//3 + 15)  # Base inferior
    ]
    pygame.draw.polygon(surface, wing_color, wing_left_points)
    pygame.draw.lines(surface, darker_color, False, wing_left_points, 1)
    
    # Detalhes da asa esquerda (nervuras)
    for x in range(3):
        start_point = wing_left_points[0]
        end_point = (
            (wing_left_points[1][0] + wing_left_points[3][0]) // 2,
            (wing_left_points[1][1] + wing_left_points[3][1]) // 2
        )
        mid_point = (
            start_point[0] + (end_point[0] - start_point[0]) * (x+1)/4,
            start_point[1] + (end_point[1] - start_point[1]) * (x+1)/4
        )
        pygame.draw.line(surface, darker_color, start_point, mid_point, 1)
    
    # Asa direita
    wing_right_points = [
        (width//2 + 5, height//3 + 5),  # Ponto de conexão
        (width//2 + 35, height//4),     # Ponta superior
        (width//2 + 40, height//3 + 10), # Ponta externa
        (width//2 + 30, height//2),     # Ponta inferior
        (width//2 + 10, height//3 + 15)  # Base inferior
    ]
    pygame.draw.polygon(surface, wing_color, wing_right_points)
    pygame.draw.lines(surface, darker_color, False, wing_right_points, 1)
    
    # Detalhes da asa direita (nervuras)
    for x in range(3):
        start_point = wing_right_points[0]
        end_point = (
            (wing_right_points[1][0] + wing_right_points[3][0]) // 2,
            (wing_right_points[1][1] + wing_right_points[3][1]) // 2
        )
        mid_point = (
            start_point[0] + (end_point[0] - start_point[0]) * (x+1)/4,
            start_point[1] + (end_point[1] - start_point[1]) * (x+1)/4
        )
        pygame.draw.line(surface, darker_color, start_point, mid_point, 1)
    
    # Braços e pernas
    pygame.draw.line(surface, pixie_color, (width//2 - 8, height//3 + 8), (width//2 - 18, height//2 + 5), 3)
    pygame.draw.line(surface, pixie_color, (width//2 + 8, height//3 + 8), (width//2 + 18, height//2 + 5), 3)
    pygame.draw.line(surface, pixie_color, (width//2 - 5, height//3 + height//3 - 2), (width//2 - 10, height - 10), 3)
    pygame.draw.line(surface, pixie_color, (width//2 + 5, height//3 + height//3 - 2), (width//2 + 10, height - 10), 3)
    
    # Adições específicas para cada estilo
    if style == "shadow":
        # Adiciona pequenos chifres/antenas para diabretes sombrios
        horn_left_start = (width//2 - 8, height//6)
        horn_left_end = (width//2 - 10, height//6 - 10)
        pygame.draw.line(surface, darker_color, horn_left_start, horn_left_end, 2)
        
        horn_right_start = (width//2 + 8, height//6)
        horn_right_end = (width//2 + 10, height//6 - 10)
        pygame.draw.line(surface, darker_color, horn_right_start, horn_right_end, 2)
    elif style == "fairy":
        # Adiciona uma pequena coroa para a fada
        pygame.draw.polygon(
            surface,
            (255, 215, 0, 220),  # Dourado
            [
                (width//2 - 10, height//6 - 2),  # Esquerda
                (width//2 - 6, height//6 - 6),   # Ponta esquerda
                (width//2, height//6 - 8),       # Meio
                (width//2 + 6, height//6 - 6),   # Ponta direita
                (width//2 + 10, height//6 - 2)   # Direita
            ]
        )
    
    return surface

def create_spell_image(color=(150, 230, 255), width=15, height=30):
    """Cria uma imagem de feitiço mágico"""
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Cria um brilho de feitiço
    for r in range(width // 2, 0, -1):
        alpha = 200 if r == width // 2 else 150 - r * 15
        if alpha < 0:
            alpha = 0
        current_color = (*color, alpha)
        pygame.draw.ellipse(surface, current_color, (width // 2 - r, height // 2 - r * 2, r * 2, r * 4))
        
    # Adiciona alguns "brilhos" aleatórios
    for _ in range(5):
        x = random.randint(0, width - 4)
        y = random.randint(0, height - 4)
        size = random.randint(2, 4)
        pygame.draw.circle(surface, (*color, 255), (x + size // 2, y + size // 2), size // 2)
        
    return surface

def create_pixie_spell_image(width=15, height=20):
    """Cria uma imagem de feitiço de diabrete"""
    return create_spell_image((255, 100, 100), width, height)

def create_game_images():
    """Cria todas as imagens para o jogo"""
    global loaded_sprites
    
    print(f"\nCriando imagens do jogo. Sprites carregados: {len(loaded_sprites)}")
    
    # Tenta usar sprites carregados primeiro
    wand_images = []
    pixie_images = []
    spell_images = []
    
    # Varinhas - usa sprites carregados se disponíveis
    if "wand_0" in loaded_sprites:
        print("Usando sprites de varinha carregados...")
        for i in range(4):
            if f"wand_{i}" in loaded_sprites:
                wand_images.append({"name": f"Varinha Mágica {i+1}", "image": loaded_sprites[f"wand_{i}"]})
    
    # Se não houver sprites carregados, usa os procedurais
    if not wand_images:
        print("Usando sprites de varinha procedurais...")
        wand_images = [
            {"name": "Varinha Clássica", "image": create_wand_image(style="classic")},
            {"name": "Varinha de Sabugueiro", "image": create_wand_image(style="elder")},
            {"name": "Varinha de Azevinho", "image": create_wand_image(style="holly")},
            {"name": "Varinha de Cristal", "image": create_wand_image(style="crystal")}
        ]
    
    # Inimigos - usa sprites carregados se disponíveis
    if "pixie_0" in loaded_sprites:
        print("Usando sprites de inimigos carregados...")
        for i in range(4):
            if f"pixie_{i}" in loaded_sprites:
                pixie_images.append({"name": f"Criatura Mágica {i+1}", "image": loaded_sprites[f"pixie_{i}"]})
    
    # Se não houver sprites carregados, usa os procedurais
    if not pixie_images:
        print("Usando sprites de inimigos procedurais...")
        pixie_images = [
            {"name": "Diabrete Azul", "image": create_pixie_image(style="blue")},
            {"name": "Duende Verde", "image": create_pixie_image(style="green")},
            {"name": "Fada da Floresta", "image": create_pixie_image(style="fairy")},
            {"name": "Diabrete Sombrio", "image": create_pixie_image(style="shadow")}
        ]
    
    # Feitiços - usa sprites carregados se disponíveis
    if "spell_0" in loaded_sprites:
        for i in range(2):
            if f"spell_{i}" in loaded_sprites:
                spell_images.append({"name": f"Feitiço Mágico {i+1}", "image": loaded_sprites[f"spell_{i}"]})
    
    # Se não houver sprites carregados, usa os procedurais
    if not spell_images:
        spell_images = [{"name": "Feitiço Azul", "image": create_spell_image((150, 230, 255))}]
    
    return {
        "wand": wand_images,
        "pixie": pixie_images,
        "spell": spell_images,
        "pixie_spell": spell_images  # Usa os mesmos feitiços para inimigos
    }

class Selector:
    """Classe para criar um seletor de imagens"""
    
    def __init__(self, items, title, position, item_size=(150, 150), spacing=30):
        self.items = items  # Lista de dicionários com 'name' e 'image'
        self.title = title
        self.position = position
        self.item_size = item_size
        self.spacing = spacing
        self.selected_index = 0
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 36)
        
    def draw(self, surface):
        """Desenha o seletor na tela"""
        # Desenha o título
        title_text = self.title_font.render(self.title, True, YELLOW)
        title_rect = title_text.get_rect(center=(self.position[0], self.position[1] - 50))
        surface.blit(title_text, title_rect)
        
        # Calcula a posição inicial para centralizar os itens
        total_width = len(self.items) * (self.item_size[0] + self.spacing) - self.spacing
        start_x = self.position[0] - total_width // 2
        
        # Desenha cada item
        for i, item in enumerate(self.items):
            # Calcula a posição
            x = start_x + i * (self.item_size[0] + self.spacing)
            y = self.position[1]
            
            # Cria um retângulo para o item
            item_rect = pygame.Rect(x, y, self.item_size[0], self.item_size[1])
            
            # Desenha um destaque para o item selecionado
            if i == self.selected_index:
                highlight_rect = item_rect.inflate(20, 20)  # Aumenta o retângulo
                pygame.draw.rect(surface, YELLOW, highlight_rect, 3, border_radius=10)
            
            # Desenha o item
            image = item["image"]
            if image:
                # Redimensiona a imagem para caber no retângulo mantendo as proporções
                img_rect = image.get_rect()
                scale = min(self.item_size[0] / img_rect.width, self.item_size[1] / img_rect.height)
                new_width = int(img_rect.width * scale)
                new_height = int(img_rect.height * scale)
                scaled_image = pygame.transform.scale(image, (new_width, new_height))
                
                # Centraliza a imagem no retângulo
                image_rect = scaled_image.get_rect(center=item_rect.center)
                surface.blit(scaled_image, image_rect)
            else:
                # Desenha um placeholder se a imagem não existir
                pygame.draw.rect(surface, MAGIC_BLUE, item_rect, 0, border_radius=10)
                
            # Desenha o nome do item
            name_text = self.font.render(item["name"], True, WHITE)
            name_rect = name_text.get_rect(center=(x + self.item_size[0] // 2, y + self.item_size[1] + 20))
            surface.blit(name_text, name_rect)
            
    def move_selection(self, direction):
        """Move a seleção para a esquerda ou direita"""
        if direction == "left":
            self.selected_index = (self.selected_index - 1) % len(self.items)
        elif direction == "right":
            self.selected_index = (self.selected_index + 1) % len(self.items)
            
    def get_selected_item(self):
        """Retorna o item selecionado"""
        return self.items[self.selected_index]

class MagicExplosion(pygame.sprite.Sprite):
    """Classe para animação de explosão mágica"""
    
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.frame = 0
        self.frames = 9  # Número de frames na animação
        self.animation_speed = 50  # ms entre frames
        self.last_update = pygame.time.get_ticks()
        
        # Cria frames da explosão mágica
        self.explosion_images = []
        for i in range(self.frames):
            # Cria uma versão mágica da explosão
            size = 30 + i * 5  # Tamanho aumenta gradualmente
            img = pygame.Surface((size, size), pygame.SRCALPHA)
            
            # Desenha círculos com cores mágicas
            for j in range(3):  # Camadas de cores
                alpha = 255 - (i * 25)
                if alpha < 0:
                    alpha = 0
                
                # Cores diferentes para cada camada
                if j == 0:
                    color = (100, 200, 255, alpha)  # Azul claro
                elif j == 1:
                    color = (150, 100, 255, alpha)  # Púrpura
                else:
                    color = (200, 255, 100, alpha)  # Verde claro
                    
                # Desenha o círculo com um pequeno deslocamento para cada camada
                offset = j * 3
                pygame.draw.circle(img, color, (size//2 + offset, size//2 - offset), size//2 - j * 5)
            
            # Adiciona alguns pequenos brilhos
            for _ in range(5):
                x = random.randint(0, size - 1)
                y = random.randint(0, size - 1)
                spark_size = random.randint(2, 5)
                spark_color = (255, 255, 255, 200 - i * 20)
                pygame.draw.circle(img, spark_color, (x, y), spark_size)
                
            self.explosion_images.append(img)
            
        # Começa com o primeiro frame
        self.image = self.explosion_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        
    def update(self, dt):
        # Atualiza o frame da animação
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.last_update = now
            self.frame += 1
            if self.frame >= len(self.explosion_images):
                self.kill()  # Remove quando a animação acaba
            else:
                center = self.rect.center
                self.image = self.explosion_images[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class GameObject(pygame.sprite.Sprite):
    """Classe base para todos os objetos do jogo"""
    
    def __init__(self, image, position, speed=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        
        # Carrega a imagem
        if isinstance(image, str):
            try:
                image_path = os.path.join(IMAGES_DIR, image)
                if os.path.exists(image_path):
                    self.image = pygame.image.load(image_path).convert_alpha()
                else:
                    # Usa imagem padrão se o arquivo não existir
                    print(f"Aviso: Imagem '{image}' não encontrada em: {image_path}")
                    if image == "varinha.png" or image == "wand.png" or image == "nave.png":
                        self.image = game_images["wand"][0]["image"]
                    elif image == "diabrete.png" or image == "pixie.png" or image == "inimigo.png":
                        self.image = game_images["pixie"][0]["image"]
                    elif image == "feitico.png" or image == "spell.png" or image == "tiro.png":
                        self.image = game_images["spell"][0]["image"]
                    elif image == "feitico_diabrete.png" or image == "pixie_spell.png" or image == "tiro_inimigo.png":
                        self.image = game_images["pixie_spell"][0]["image"]
                    else:
                        # Imagem placeholder genérica se nenhuma das acima
                        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
                        self.image.fill(PURPLE)
            except pygame.error as e:
                print(f"Erro ao carregar imagem: {e}")
                self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
                self.image.fill(PURPLE)
        else:
            self.image = image
            
        # Configura o retângulo e a área da tela
        self.rect = self.image.get_rect()
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()
        
        # Configura posição e velocidade
        self.set_pos(position)
        self.set_speed(speed)
        
    def update(self, dt):
        """Atualiza a posição do objeto baseado na velocidade"""
        # Calcula o movimento baseado no delta time
        move_speed = (self.speed[0] * dt / 16, self.speed[1] * dt / 16)
        self.rect = self.rect.move(move_speed)
        
        # Remove o objeto se sair da tela
        if (self.rect.left > self.area.right or
            self.rect.top > self.area.bottom or
            self.rect.right < 0 or
            self.rect.bottom < -40):
            self.kill()
            
    def get_speed(self):
        return self.speed
        
    def set_speed(self, speed):
        self.speed = speed
        
    def get_pos(self):
        return (self.rect.center[0], self.rect.bottom)
        
    def set_pos(self, pos):
        self.rect.center = (pos[0], pos[1])
        
    def get_size(self):
        return self.image.get_size()
        
class Spell(GameObject):
    """Classe para os feitiços lançados"""
    
    def __init__(self, position, speed=(0, -10), image=None, damage=1, owner=None):
        # Se a imagem for None, use a imagem padrão de feitiço
        if image is None:
            image = game_images["spell"][0]["image"]
            
        GameObject.__init__(self, image, position, speed)
        self.damage = damage
        self.owner = owner  # Referência a quem lançou o feitiço
        
        # Adiciona efeito de rotação para o feitiço parecer mais mágico
        self.rotation = 0
        self.rotation_speed = random.randint(-5, 5)
        self.original_image = self.image
        
    def update(self, dt):
        """Atualiza o feitiço com efeito de rotação"""
        GameObject.update(self, dt)
        
        # Rotaciona o feitiço
        self.rotation = (self.rotation + self.rotation_speed) % 360
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
        
    def hit(self, target):
        """Aplica dano ao alvo atingido"""
        if hasattr(target, 'take_damage'):
            target.take_damage(self.damage)
        self.kill()

class MagicCaster(GameObject):
    """Classe base para todos os lançadores de magia"""
    
    def __init__(self, position, health=3, speed=(0, 0), image=None):
        if image is None:
            image = game_images["wand"][0]["image"]
            
        GameObject.__init__(self, image, position, speed)
        self.health = health
        self.max_health = health
        self.spell_cooldown = 0
        self.spell_rate = 250  # Tempo em ms entre feitiços
        self.spell_speed = 10
        self.spell_damage = 1
        self.spell_image = None  # Será definido pelas subclasses
        
    def update(self, dt):
        GameObject.update(self, dt)
        
        # Atualiza o cooldown de lançamento de feitiços
        if self.spell_cooldown > 0:
            self.spell_cooldown -= dt
            
    def cast_spell(self, spell_group):
        """Lança um feitiço"""
        if self.spell_cooldown <= 0:
            # Configura a velocidade do feitiço (invertida para diabretes)
            spell_speed = (0, -self.spell_speed)
            if isinstance(self, Pixie):
                spell_speed = (0, self.spell_speed)
                
            # Cria o feitiço
            spell = Spell(
                self.get_pos(), 
                spell_speed,
                self.spell_image,
                self.spell_damage,
                self
            )
            
            # Adiciona ao grupo
            spell_group.add(spell)
            all_sprites.add(spell)
            
            # Reseta o cooldown
            self.spell_cooldown = self.spell_rate
            
            # Reproduz o som de lançamento (sem usar o gerenciador para evitar erros)
            try:
                if sound_enabled:
                    spell_sound.play()
            except:
                pass
                
            return True
        return False
        
    def take_damage(self, amount):
        """Recebe dano"""
        self.health -= amount
        if self.health <= 0:
            self.explode()
            self.kill()
            return True
        return False
        
    def explode(self):
        """Cria uma explosão mágica na posição"""
        explosion = MagicExplosion(self.rect.center)
        all_sprites.add(explosion)
        try:
            if sound_enabled:
                explosion_sound.play()
        except:
            pass
        
    def is_dead(self):
        return self.health <= 0
        
class Wand(MagicCaster):
    """Classe para a varinha mágica controlada pelo jogador"""
    
    def __init__(self, position, health=5, image=None):
        MagicCaster.__init__(self, position, health, (0, 0), image)
        self.acceleration = 0.2  # Aceleração baixa para movimento suave
        self.max_speed = 4.0     # Velocidade máxima reduzida
        self.score = 0
        self.lives = 3
        self.is_invulnerable = False
        self.invulnerable_timer = 0
        self.spell_rate = 200  # Lança feitiços mais rápido que os diabretes
        self.spell_damage = 1
        self.spell_image = game_images["spell"][0]["image"]
        
        # Efeito de brilho da varinha
        self.glow_surface = None
        self.glow_alpha = 0
        self.glow_direction = 1
        self.create_glow_effect()
        
    def create_glow_effect(self):
        """Cria o efeito de brilho da ponta da varinha"""
        size = max(self.rect.width, self.rect.height) + 20
        self.glow_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
    def update(self, dt):
        # Adiciona um fator de desaceleração para tornar o controle mais suave
        friction = 0.95
        self.speed = (self.speed[0] * friction, self.speed[1] * friction)
        
        # Atualiza a posição sem remover o objeto se ele sair da tela
        move_speed = (self.speed[0] * dt / 16, self.speed[1] * dt / 16)
        self.rect = self.rect.move(move_speed)
        
        # Mantém a varinha dentro da tela
        if self.rect.right > self.area.right:
            self.rect.right = self.area.right
            self.speed = (0, self.speed[1])
        elif self.rect.left < 0:
            self.rect.left = 0
            self.speed = (0, self.speed[1])
            
        if self.rect.bottom > self.area.bottom:
            self.rect.bottom = self.area.bottom
            self.speed = (self.speed[0], 0)
        elif self.rect.top < 0:
            self.rect.top = 0
            self.speed = (self.speed[0], 0)
            
        # Atualiza o cooldown de lançamento de feitiços
        if self.spell_cooldown > 0:
            self.spell_cooldown -= dt
            
        # Processa a invulnerabilidade
        if self.is_invulnerable:
            self.invulnerable_timer -= dt
            if self.invulnerable_timer <= 0:
                self.is_invulnerable = False
                # Restaura a opacidade normal
                self.image.set_alpha(255)
            else:
                # Pisca a varinha para indicar invulnerabilidade
                alpha = 128 + 127 * math.sin(pygame.time.get_ticks() / 100)
                self.image.set_alpha(int(alpha))
                
        # Atualiza o brilho
        self.glow_alpha += self.glow_direction * 2
        if self.glow_alpha > 100:
            self.glow_alpha = 100
            self.glow_direction = -1
        elif self.glow_alpha < 30:
            self.glow_alpha = 30
            self.glow_direction = 1
                
    def draw(self, surface):
        """Desenha a varinha com efeito de brilho"""
        # Primeiro desenha o brilho
        self.glow_surface.fill((0, 0, 0, 0))
        
        # Cria um brilho na ponta da varinha
        glow_radius = 15
        glow_pos = (self.glow_surface.get_width() // 2, 20)  # Posição na ponta da varinha
        
        for r in range(glow_radius, 0, -1):
            alpha = min(self.glow_alpha, 150 - r * 10)
            if alpha < 0:
                alpha = 0
            color = (200, 220, 255, alpha)
            pygame.draw.circle(self.glow_surface, color, glow_pos, r)
            
        # Posição do brilho
        glow_rect = self.glow_surface.get_rect()
        glow_rect.center = self.rect.center
        glow_rect.bottom = self.rect.top + 10  # Ajuste para o brilho ficar na ponta
        
        # Desenha o brilho e depois a varinha
        surface.blit(self.glow_surface, glow_rect)
        surface.blit(self.image, self.rect)
                
    def get_pos(self):
        # A posição de lançamento é na ponta da varinha
        return (self.rect.center[0], self.rect.top)
        
    def move(self, direction):
        """Aplica aceleração na direção especificada"""
        dx, dy = 0, 0
        
        if direction == 'left':
            dx = -self.acceleration
        elif direction == 'right':
            dx = self.acceleration
        elif direction == 'up':
            dy = -self.acceleration
        elif direction == 'down':
            dy = self.acceleration
            
        # Aplica a aceleração
        self.speed = (self.speed[0] + dx, self.speed[1] + dy)
        
        # Limita à velocidade máxima
        speed_x, speed_y = self.speed
        if abs(speed_x) > self.max_speed:
            speed_x = self.max_speed if speed_x > 0 else -self.max_speed
        if abs(speed_y) > self.max_speed:
            speed_y = self.max_speed if speed_y > 0 else -self.max_speed
            
        self.speed = (speed_x, speed_y)
        
    def stop(self, axis):
        """Para o movimento em um eixo"""
        if axis == 'horizontal':
            self.speed = (0, self.speed[1])
        elif axis == 'vertical':
            self.speed = (self.speed[0], 0)
        elif axis == 'both':
            self.speed = (0, 0)
            
    def take_damage(self, amount):
        """Sobrescreve o método para implementar invulnerabilidade"""
        if not self.is_invulnerable:
            self.health -= amount
            if self.health <= 0:
                self.lives -= 1
                if self.lives > 0:
                    # Reinicia a saúde e torna invulnerável
                    self.health = self.max_health
                    self.make_invulnerable(3000)  # 3 segundos
                    # Centraliza a varinha
                    center_x = self.area.width // 2
                    bottom_y = self.area.height - 50
                    self.set_pos((center_x, bottom_y))
                    self.stop('both')
                    return False
                else:
                    # Sem vidas, game over
                    self.explode()
                    self.kill()
                    return True
            else:
                # Torna invulnerável por um período mais curto ao ser atingido
                self.make_invulnerable(1500)  # 1.5 segundos
                
        return False
        
    def make_invulnerable(self, duration):
        """Torna a varinha invulnerável por um tempo"""
        self.is_invulnerable = True
        self.invulnerable_timer = duration

class Pixie(MagicCaster):
    """Classe para os diabretes da Cornualha"""
    
    def __init__(self, position, health=1, behavior=PixieBehavior.STRAIGHT_DOWN, 
                 image=None, points=100):
        # Se image for None, usa a imagem de diabrete padrão
        if image is None:
            image = game_images["pixie"][0]["image"]
            
        MagicCaster.__init__(self, position, health, (0, 0), image)
        self.behavior = behavior
        self.points = points
        self.timer = 0
        self.spell_rate = random.randint(1000, 3000)  # Tempo aleatório entre feitiços
        self.spell_image = game_images["pixie_spell"][0]["image"]
        
        # Wings flapping animation state
        self.wing_frame = 0
        self.wing_frame_timer = 0
        self.wing_frame_rate = 100  # ms entre frames
        
        # Define a velocidade inicial com base no comportamento
        if behavior == PixieBehavior.STRAIGHT_DOWN:
            self.set_speed((0, 3))
        elif behavior == PixieBehavior.LEFT_TO_RIGHT:
            self.set_speed((2, 2))
        elif behavior == PixieBehavior.RIGHT_TO_LEFT:
            self.set_speed((-2, 2))
        elif behavior == PixieBehavior.ZIGZAG:
            self.set_speed((math.sin(0) * 3, 2))
        elif behavior == PixieBehavior.CIRCULAR:
            self.set_speed((0, 2))
            self.circle_center_x = position[0]
            self.circle_radius = random.randint(50, 100)
            self.angle = 0
            
    def update(self, dt):
        MagicCaster.update(self, dt)
        
        # Atualiza o movimento baseado no comportamento
        self.timer += dt
        
        if self.behavior == PixieBehavior.ZIGZAG:
            # Movimento em zig-zag
            speed_x = math.sin(self.timer / 500) * 3
            self.set_speed((speed_x, self.speed[1]))
        elif self.behavior == PixieBehavior.CIRCULAR:
            # Movimento circular enquanto desce
            self.angle = (self.angle + 0.05) % (2 * math.pi)
            x = self.circle_center_x + math.sin(self.angle) * self.circle_radius
            
            # Mantém a posição vertical original (descendo)
            original_y = self.rect.centery
            self.rect.centerx = x
            self.rect.centery = original_y
            
        # Animação das asas
        self.wing_frame_timer += dt
        if self.wing_frame_timer > self.wing_frame_rate:
            self.wing_frame_timer = 0
            self.wing_frame = (self.wing_frame + 1) % 4  # 4 frames de animação
            
    def take_damage(self, amount):
        """Sobrescreve para adicionar pontuação quando destruído"""
        destroyed = super().take_damage(amount)
        if destroyed and hasattr(self, 'owner') and self.owner:
            # Aumenta a pontuação do jogador
            self.owner.score += self.points
        return destroyed

class Star:
    """Classe para estrelas do fundo"""
    
    def __init__(self, surface):
        self.surface = surface
        self.width, self.height = surface.get_size()
        self.reset()
        
    def reset(self):
        """Reinicia a estrela em uma posição aleatória"""
        self.x = random.randint(0, self.width)
        self.y = random.randint(0, self.height)
        self.speed = random.randint(1, 3)
        brightness = random.randint(100, 255)
        
        # Adiciona chance de estrelas coloridas para o efeito mágico
        if random.random() < 0.3:  # 30% de chance de ser uma estrela mágica colorida
            r = random.randint(180, 255)
            g = random.randint(180, 255)
            b = random.randint(180, 255)
            self.color = (r, g, b)
        else:
            self.color = (brightness, brightness, brightness)
            
        self.size = random.choice([1, 1, 1, 2, 2, 3])  # Probabilidade para tamanhos diferentes
        
    def update(self, dt):
        """Atualiza a posição da estrela"""
        self.y += self.speed * dt / 16
        
        # Reinicia a estrela se sair da tela
        if self.y > self.height:
            self.reset()
            self.y = 0
            
    def draw(self):
        """Desenha a estrela na superfície"""
        pygame.draw.circle(self.surface, self.color, (int(self.x), int(self.y)), self.size)

class MagicalBackground:
    """Classe para o fundo mágico em movimento"""
    
    def __init__(self, surface, star_count=80):
        self.surface = surface
        self.width, self.height = surface.get_size()
        self.stars = [Star(surface) for _ in range(star_count)]  # Menos estrelas
        
        # Cria uma nebulosa mágica para o fundo
        self.nebula = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.create_magical_nebula()
        self.offset_y = 0
        
        # Efeitos mágicos adicionais
        self.magic_particles = []
        self.create_magic_particles(15)  # Menos partículas mágicas
        
    def create_magical_nebula(self):
        """Cria uma nebulosa mágica usando gradientes e transparência"""
        # Adiciona alguns pontos coloridos de nebulosa mágica
        for _ in range(8):  # Menos nebulosas
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            radius = random.randint(80, 200)
            
            # Cores aleatórias mais suaves para as nebulosas mágicas
            r = random.randint(30, 80)
            g = random.randint(30, 100)
            b = random.randint(100, 180)  # Predominantemente azul/púrpura
            a = random.randint(5, 20)    # Mais transparente
            
            color = (r, g, b, a)
            
            # Desenha círculos gradientes
            for i in range(radius, 0, -1):
                alpha = a * (i / radius)  # Diminui a opacidade para criar gradiente
                c = (r, g, b, int(alpha))
                pygame.draw.circle(self.nebula, c, (x, y), i)
                
    def create_magic_particles(self, count):
        """Cria partículas de magia flutuantes pelo fundo"""
        for _ in range(count):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            size = random.randint(3, 8)
            speed = random.uniform(0.2, 0.8)
            alpha = random.randint(40, 150)
            
            # Cores mágicas vibrantes
            hue = random.random()
            if hue < 0.33:
                color = (random.randint(180, 255), random.randint(100, 180), random.randint(200, 255))  # Tons de roxo/azul
            elif hue < 0.66:
                color = (random.randint(100, 180), random.randint(180, 255), random.randint(200, 255))  # Tons de verde/azul
            else:
                color = (random.randint(200, 255), random.randint(180, 255), random.randint(100, 180))  # Tons de amarelo/verde
                
            # Adiciona a partícula
            self.magic_particles.append({
                'x': x, 
                'y': y, 
                'size': size,
                'speed': speed,
                'color': (*color, alpha),
                'angle': random.uniform(0, 2 * math.pi),
                'orbit_radius': random.uniform(0, 2),
                'orbit_speed': random.uniform(0.01, 0.05)
            })
                
    def update(self, dt):
        """Atualiza o fundo mágico"""
        # Atualiza as estrelas
        for star in self.stars:
            star.update(dt)
            
        # Move a nebulosa muito lentamente
        self.offset_y += 0.1 * dt / 16
        if self.offset_y >= self.height:
            self.offset_y = 0
            
        # Atualiza as partículas mágicas
        for particle in self.magic_particles:
            # Movimento em espiral suave
            particle['angle'] += particle['orbit_speed']
            particle['x'] += math.sin(particle['angle']) * particle['orbit_radius']
            particle['y'] -= particle['speed']
            
            # Se a partícula sair do topo, volta para o fundo
            if particle['y'] < -particle['size']:
                particle['y'] = self.height + particle['size']
                particle['x'] = random.randint(0, self.width)
            
    def draw(self):
        """Desenha o fundo mágico"""
        # Fundo com gradiente escuro
        # Cria um gradiente vertical do topo escuro para o fundo um pouco mais claro
        for y in range(0, self.height, 4):
            darkness = 1 - (y / self.height) * 0.3
            color = (int(10 * darkness), int(10 * darkness), int(35 * darkness))
            pygame.draw.rect(self.surface, color, (0, y, self.width, 4))
        
        # Desenha a nebulosa (duas vezes para efeito de rolagem)
        self.surface.blit(self.nebula, (0, int(self.offset_y)))
        self.surface.blit(self.nebula, (0, int(self.offset_y - self.height)))
        
        # Desenha as partículas mágicas
        for particle in self.magic_particles:
            # Desenha um pequeno brilho em vez de apenas um círculo
            radius = particle['size']
            pygame.draw.circle(self.surface, particle['color'], 
                              (int(particle['x']), int(particle['y'])), radius)
            
            # Adiciona um pequeno brilho interno
            if radius > 3:
                inner_color = (255, 255, 255, int(particle['color'][3] * 0.7))
                pygame.draw.circle(self.surface, inner_color, 
                                  (int(particle['x']), int(particle['y'])), radius // 2)
        
        # Desenha as estrelas
        for star in self.stars:
            star.draw()

class Game:
    """Classe principal do jogo"""
    
    def __init__(self):
        # Inicializa o pygame
        pygame.init()
        pygame.display.set_caption("Wizarding Duel: Varinha vs Diabretes")
        
        # Configurações de tela
        global current_screen, fullscreen
        self.screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.fullscreen = False
        self.screen = pygame.display.set_mode(self.screen_size, DOUBLEBUF)
        current_screen = self.screen
        self.clock = pygame.time.Clock()
        
        # Carrega sprites externos agora que a tela foi inicializada
        load_all_sprites()
        
        # Recria as imagens do jogo após carregar os sprites
        global game_images
        game_images = create_game_images()
        
        # Carrega fonte com suporte a caracteres especiais para idiomas
        try:
            self.title_font = pygame.font.Font(None, 64)
            self.menu_font = pygame.font.Font(None, 36)
            self.hud_font = pygame.font.Font(None, 24)
        except:
            # Fallback para fonte padrão se não conseguir carregar
            print("Aviso: Usando fonte padrão")
            self.title_font = pygame.font.SysFont("Arial", 64)
            self.menu_font = pygame.font.SysFont("Arial", 36)
            self.hud_font = pygame.font.SysFont("Arial", 24)
        
        # Estado do jogo
        self.state = GameState.MENU
        self.running = True
        
        # Fundo mágico
        self.background = MagicalBackground(self.screen, 80)  # Menos estrelas
        
        # Inicializa grupos de sprites
        global all_sprites, player_spells, pixie_spells, pixies
        all_sprites = pygame.sprite.Group()
        player_spells = pygame.sprite.Group()
        pixie_spells = pygame.sprite.Group()
        pixies = pygame.sprite.Group()
        
        # Estado de teclas
        self.keys_pressed = {}
        
        # Rastreamento de tempo
        self.pixie_spawn_timer = 0
        self.level_timer = 0
        self.game_time = 0
        
        # Dificuldade
        self.difficulty = 1
        self.level = 1
        self.pixie_spawn_rate = 2000  # ms entre diabretes
        
        # Seletores de personagem
        self.wand_selector = None
        self.pixie_selector = None
        self.selected_wand = None
        self.selected_pixie = None
        self.active_selector = "wand"  # Começa com o seletor de varinha ativo
        self.setup_character_selection()
        
    def toggle_fullscreen(self):
        """Alterna entre tela cheia e modo janela"""
        global current_screen, fullscreen
        self.fullscreen = not self.fullscreen
        fullscreen = self.fullscreen
        
        if self.fullscreen:
            # Pega as dimensões da tela
            info = pygame.display.Info()
            self.screen = pygame.display.set_mode((info.current_w, info.current_h), 
                                                pygame.FULLSCREEN | pygame.DOUBLEBUF)
        else:
            self.screen = pygame.display.set_mode(self.screen_size, pygame.DOUBLEBUF)
        
        current_screen = self.screen
        # Recria o fundo com o novo tamanho de tela
        self.background = MagicalBackground(self.screen, 80)
        
    def setup_character_selection(self):
        """Configura os seletores de personagem"""
        # Configura o seletor de varinhas
        self.wand_selector = Selector(
            game_images["wand"], 
            "Escolha sua Varinha Mágica",
            (self.screen_size[0] // 2, self.screen_size[1] // 3),
            (120, 120)
        )
        
        # Configura o seletor de diabretes
        self.pixie_selector = Selector(
            game_images["pixie"],
            "Escolha seus Inimigos",
            (self.screen_size[0] // 2, self.screen_size[1] * 2 // 3),
            (120, 120)
        )
        
    def create_player(self):
        """Cria a varinha do jogador com a imagem selecionada"""
        if self.selected_wand is None:
            self.selected_wand = game_images["wand"][0]
            
        self.player = Wand((self.screen_size[0] // 2, self.screen_size[1] - 50), 
                          image=self.selected_wand["image"])
        all_sprites.add(self.player)
        
    def reset_game(self):
        """Reinicia o jogo para um novo início"""
        # Limpa todos os sprites
        all_sprites.empty()
        player_spells.empty()
        pixie_spells.empty()
        pixies.empty()
        
        # Reinicia o jogador
        self.create_player()
        
        # Reinicia contadores
        self.pixie_spawn_timer = 0
        self.level_timer = 0
        self.game_time = 0
        self.difficulty = 1
        self.level = 1
        self.pixie_spawn_rate = 2000
        
        # Reinicia o estado
        self.state = GameState.PLAYING
        
        # Inicia a música
        try:
            if sound_enabled:
                pygame.mixer.music.play(-1)
        except:
            pass
        
    def spawn_pixie(self):
        """Cria um diabrete da Cornualha aleatório"""
        # Escolhe um comportamento aleatório
        behavior = random.choice(list(PixieBehavior))
        
        # Escolhe uma posição inicial aleatória no topo da tela
        x = random.randint(50, self.screen_size[0] - 50)
        y = -20
        
        # Aumenta a dificuldade com o tempo
        health = 1
        if self.difficulty > 3:
            health = 2
        if self.difficulty > 6:
            health = 3
        
        # Usa a imagem selecionada pelo jogador
        pixie_image = self.selected_pixie["image"] if self.selected_pixie else game_images["pixie"][0]["image"]
            
        # Cria o diabrete
        pixie = Pixie((x, y), health, behavior, pixie_image, points=100*self.difficulty)
        pixie.owner = self.player  # Para rastrear pontuação
        
        # Adiciona aos grupos
        pixies.add(pixie)
        all_sprites.add(pixie)
        
    def handle_events(self):
        """Processa os eventos do pygame"""
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
                
            elif event.type == KEYDOWN:
                self.keys_pressed[event.key] = True
                
                # Teclas específicas
                if event.key == K_ESCAPE:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
                        
                elif event.key == K_RETURN:
                    if self.state == GameState.MENU:
                        self.state = GameState.CHARACTER_SELECT
                    elif self.state == GameState.CHARACTER_SELECT:
                        self.selected_wand = self.wand_selector.get_selected_item()
                        self.selected_pixie = self.pixie_selector.get_selected_item()
                        self.reset_game()
                    elif self.state == GameState.GAME_OVER:
                        self.state = GameState.MENU
                        
                elif event.key == K_SPACE:
                    if self.state == GameState.PLAYING:
                        self.player.cast_spell(player_spells)
                        
                # Tecla F11 para alternar tela cheia
                elif event.key == K_F11:
                    self.toggle_fullscreen()
                
                # Controles de seleção de personagem
                elif self.state == GameState.CHARACTER_SELECT:
                    if event.key == K_LEFT:
                        if self.active_selector == "wand":
                            self.wand_selector.move_selection("left")
                        else:
                            self.pixie_selector.move_selection("left")
                    elif event.key == K_RIGHT:
                        if self.active_selector == "wand":
                            self.wand_selector.move_selection("right")
                        else:
                            self.pixie_selector.move_selection("right")
                    elif event.key == K_UP:
                        # Alterna para o seletor de varinha
                        self.active_selector = "wand"
                    elif event.key == K_DOWN:
                        # Alterna para o seletor de diabrete
                        self.active_selector = "pixie"
                    elif event.key == K_a:
                        if self.active_selector == "wand":
                            self.wand_selector.move_selection("left")
                        else:
                            self.pixie_selector.move_selection("left")
                    elif event.key == K_d:
                        if self.active_selector == "wand":
                            self.wand_selector.move_selection("right")
                        else:
                            self.pixie_selector.move_selection("right") 
                        
            elif event.type == KEYUP:
                self.keys_pressed[event.key] = False
                
    def process_input(self):
        """Processa teclas pressionadas continuamente"""
        if self.state != GameState.PLAYING:
            return
            
        # Movimento do jogador
        if self.keys_pressed.get(K_LEFT) or self.keys_pressed.get(K_a):
            self.player.move('left')
        if self.keys_pressed.get(K_RIGHT) or self.keys_pressed.get(K_d):
            self.player.move('right')
        if self.keys_pressed.get(K_UP) or self.keys_pressed.get(K_w):
            self.player.move('up')
        if self.keys_pressed.get(K_DOWN) or self.keys_pressed.get(K_s):
            self.player.move('down')
        
        # Lançamento contínuo de feitiços com a barra de espaço
        if self.keys_pressed.get(K_SPACE):
            self.player.cast_spell(player_spells)
            
    def update(self, dt):
        """Atualiza o estado do jogo"""
        # Atualiza o fundo em todos os estados
        self.background.update(dt)
        
        if self.state == GameState.PLAYING:
            # Atualiza o tempo de jogo
            self.game_time += dt
            
            # Aumenta a dificuldade com o tempo
            self.level_timer += dt
            if self.level_timer > 30000:  # A cada 30 segundos
                self.level_timer = 0
                self.level += 1
                self.difficulty = min(10, self.level)
                self.pixie_spawn_rate = max(500, 2000 - self.level * 150)
                
            # Spawn de diabretes
            self.pixie_spawn_timer += dt
            if self.pixie_spawn_timer > self.pixie_spawn_rate:
                self.pixie_spawn_timer = 0
                self.spawn_pixie()
                
            # Alguns diabretes lançam feitiços aleatoriamente
            for pixie in pixies:
                if random.random() < 0.005:  # 0.5% de chance por frame
                    pixie.cast_spell(pixie_spells)
                    
            # Atualiza todos os sprites
            all_sprites.update(dt)
            
            # Verifica colisões
            self.check_collisions()
            
            # Verifica game over
            if self.player.is_dead() and self.state != GameState.GAME_OVER:
                self.state = GameState.GAME_OVER
                try:
                    if sound_enabled:
                        pygame.mixer.music.stop()
                except:
                    pass
                
    def check_collisions(self):
        """Verifica todas as colisões do jogo"""
        # Feitiços do jogador vs diabretes
        hits = pygame.sprite.groupcollide(pixies, player_spells, False, True)
        for pixie, spells in hits.items():
            for spell in spells:
                pixie.take_damage(spell.damage)
                
        # Feitiços dos diabretes vs jogador
        if not self.player.is_invulnerable:
            hits = pygame.sprite.spritecollide(self.player, pixie_spells, True)
            if hits:
                self.player.take_damage(len(hits))
                
        # Colisão direta jogador vs diabretes
        if not self.player.is_invulnerable:
            hits = pygame.sprite.spritecollide(self.player, pixies, False)
            if hits:
                # Destrói o diabrete e causa dano ao jogador
                for pixie in hits:
                    pixie.take_damage(pixie.health)
                    self.player.take_damage(1)
                    
    def draw_menu(self):
        """Desenha a tela de menu"""
        # Desenha o fundo mágico
        self.background.draw()
        
        # Título do jogo
        title_text = self.title_font.render("Wizarding Duel", True, YELLOW)
        title_rect = title_text.get_rect(center=(self.screen_size[0]//2, self.screen_size[1]//4))
        self.screen.blit(title_text, title_rect)
        
        subtitle_text = self.menu_font.render("Varinha vs Diabretes da Cornualha", True, MAGIC_BLUE)
        subtitle_rect = subtitle_text.get_rect(center=(self.screen_size[0]//2, self.screen_size[1]//4 + 50))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Instruções
        start_text = self.menu_font.render("Pressione ENTER para iniciar", True, WHITE)
        start_rect = start_text.get_rect(center=(self.screen_size[0]//2, self.screen_size[1]//2))
        self.screen.blit(start_text, start_rect)
        
        controls_text = self.menu_font.render("Setas/WASD para mover, ESPAÇO para lançar feitiços", True, WHITE)
        controls_rect = controls_text.get_rect(center=(self.screen_size[0]//2, self.screen_size[1]//2 + 50))
        self.screen.blit(controls_text, controls_rect)
        
        # Informação sobre imagens
        image_text = self.menu_font.render("Escolha sua varinha e diabretes na próxima tela!", True, GREEN)
        image_rect = image_text.get_rect(center=(self.screen_size[0]//2, self.screen_size[1]//2 + 100))
        self.screen.blit(image_text, image_rect)
        
        # Instrução sobre tela cheia
        fullscreen_text = self.hud_font.render("F11 para alternar tela cheia", True, WHITE)
        fullscreen_rect = fullscreen_text.get_rect(center=(self.screen_size[0]//2, self.screen_size[1] - 50))
        self.screen.blit(fullscreen_text, fullscreen_rect)
        
    def draw_character_select(self):
        """Desenha a tela de seleção de personagem"""
        # Desenha o fundo mágico
        self.background.draw()
        
        # Título da tela
        title_text = self.title_font.render("Seleção de Personagem", True, YELLOW)
        title_rect = title_text.get_rect(center=(self.screen_size[0]//2, 50))
        self.screen.blit(title_text, title_rect)
        
        # Desenha os seletores
        self.wand_selector.draw(self.screen)
        self.pixie_selector.draw(self.screen)
        
        # Destaca o seletor ativo
        highlight_text = self.menu_font.render("▼ Seleção Atual ▼", True, GREEN)
        if self.active_selector == "wand":
            highlight_rect = highlight_text.get_rect(center=(self.screen_size[0]//2, self.screen_size[1]//3 - 100))
        else:
            highlight_rect = highlight_text.get_rect(center=(self.screen_size[0]//2, self.screen_size[1]*2//3 - 100))
        self.screen.blit(highlight_text, highlight_rect)
        
        # Instruções
        instructions_text = self.menu_font.render("Use as SETAS para navegar, CIMA/BAIXO para alternar, ENTER para confirmar", True, WHITE)
        instructions_rect = instructions_text.get_rect(center=(self.screen_size[0]//2, self.screen_size[1] - 50))
        self.screen.blit(instructions_text, instructions_rect)
        
    def draw_game(self):
        """Desenha o jogo"""
        # Desenha o fundo mágico
        self.background.draw()
        
        # Desenha todos os sprites
        for sprite in all_sprites:
            if hasattr(sprite, 'draw') and callable(sprite.draw):
                sprite.draw(self.screen)
            else:
                self.screen.blit(sprite.image, sprite.rect)
        
        # HUD - Informações do jogador
        score_text = self.hud_font.render(f"Pontuação: {self.player.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        lives_text = self.hud_font.render(f"Vidas: {self.player.lives}", True, WHITE)
        self.screen.blit(lives_text, (10, 40))
        
        health_text = self.hud_font.render(f"Saúde: {self.player.health}/{self.player.max_health}", True, WHITE)
        self.screen.blit(health_text, (10, 70))
        
        level_text = self.hud_font.render(f"Nível: {self.level}", True, WHITE)
        self.screen.blit(level_text, (self.screen_size[0] - 100, 10))
        
        # Mostra qual varinha está sendo usada
        wand_name = self.selected_wand["name"] if self.selected_wand else "Varinha Padrão"
        wand_text = self.hud_font.render(f"Varinha: {wand_name}", True, WHITE)
        self.screen.blit(wand_text, (self.screen_size[0] - 300, 40))
        
    def draw_pause(self):
        """Desenha a tela de pause"""
        # Primeira desenha o jogo normalmente
        self.draw_game()
        
        # Adiciona um overlay semi-transparente
        overlay = pygame.Surface(self.screen_size, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Preto com 50% de transparência
        self.screen.blit(overlay, (0, 0))
        
        # Texto de pausa
        pause_text = self.title_font.render("PAUSADO", True, WHITE)
        pause_rect = pause_text.get_rect(center=(self.screen_size[0]//2, self.screen_size[1]//2))
        self.screen.blit(pause_text, pause_rect)
        
        # Instruções
        resume_text = self.menu_font.render("Pressione ESC para continuar", True, WHITE)
        resume_rect = resume_text.get_rect(center=(self.screen_size[0]//2, self.screen_size[1]//2 + 60))
        self.screen.blit(resume_text, resume_rect)
        
    def draw_game_over(self):
        """Desenha a tela de game over"""
        # Desenha o fundo mágico
        self.background.draw()
        
        # Texto de Game Over
        over_text = self.title_font.render("GAME OVER", True, RED)
        over_rect = over_text.get_rect(center=(self.screen_size[0]//2, self.screen_size[1]//3))
        self.screen.blit(over_text, over_rect)
        
        # Pontuação final
        score_text = self.menu_font.render(f"Pontuação Final: {self.player.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(self.screen_size[0]//2, self.screen_size[1]//2))
        self.screen.blit(score_text, score_rect)
        
        # Instruções
        menu_text = self.menu_font.render("Pressione ENTER para voltar ao menu", True, WHITE)
        menu_rect = menu_text.get_rect(center=(self.screen_size[0]//2, self.screen_size[1]//2 + 60))
        self.screen.blit(menu_text, menu_rect)
        
    def draw(self):
        """Desenha o estado atual do jogo"""
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.CHARACTER_SELECT:
            self.draw_character_select()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.PAUSED:
            self.draw_pause()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
            
        # Atualiza a tela
        pygame.display.flip()
        
    def run(self):
        """Loop principal do jogo"""
        try:
            # Loop principal
            while self.running:
                # Limita a taxa de quadros
                dt = self.clock.tick(FPS)
                
                # Processa eventos
                self.handle_events()
                
                # Processa input contínuo
                self.process_input()
                
                # Atualiza o jogo
                self.update(dt)
                
                # Desenha tudo
                self.draw()
                
        except Exception as e:
            print(f"Erro no jogo: {e}")
            import traceback
            traceback.print_exc()
            
        finally:
            # Limpeza final
            pygame.quit()

def main():
    """Função principal do jogo"""
    print("Inicializando Wizarding Duel: Varinha vs Diabretes (Versão Local)...")
    
    # Carrega as imagens geradas localmente
    global game_images, sound_enabled, spell_sound, explosion_sound
    
    try:
        game_images = create_game_images()
        print("Imagens geradas com sucesso!")
    except Exception as e:
        print(f"Erro ao gerar imagens: {e}")
        return
    
    # Configuração de som
    sound_enabled = False
    try:
        pygame.mixer.init()
        
        # Cria sons básicos usando PyGame diretamente (sem arquivos externos)
        spell_sound_buffer = bytearray([128] * 1000 + [180, 128, 80, 128] * 500)
        explosion_sound_buffer = bytearray([128] * 100 + [random.randint(64, 192) for _ in range(3000)])
        
        spell_sound = pygame.mixer.Sound(spell_sound_buffer)
        explosion_sound = pygame.mixer.Sound(explosion_sound_buffer)
        sound_enabled = True
        print("Sons gerados com sucesso!")
        
    except Exception as e:
        print(f"Aviso: Sons desabilitados - {e}")
        sound_enabled = False
    
    print("Inicializando o jogo...")
    # Inicializa e executa o jogo
    game = Game()
    game.run()
    
    print("Obrigado por jogar Wizarding Duel!")
    
if __name__ == "__main__":
    main()