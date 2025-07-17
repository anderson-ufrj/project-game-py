"""
UI Melhorada - Mantém funcionalidade mas adiciona visual moderno
"""
import pygame
import math
from settings import * 
from player import Player
from font_manager import font_manager

class EnhancedUI:
    """UI melhorada com efeitos visuais modernos mas mantendo simplicidade"""
    
    def __init__(self):
        # General
        self.display_surface = pygame.display.get_surface()
        self.font = font_manager.get('ui')
        
        # Cores do tema moderno
        self.colors = {
            'health_high': (100, 255, 100),    # Verde
            'health_med': (255, 255, 100),     # Amarelo  
            'health_low': (255, 100, 100),     # Vermelho
            'energy': (100, 200, 255),         # Azul
            'background': (20, 20, 30, 180),   # Fundo escuro
            'border': (120, 120, 140),         # Borda padrão
            'border_active': (255, 215, 0),    # Borda ativa (dourado)
            'text': (255, 255, 255),           # Texto branco
            'text_shadow': (0, 0, 0),          # Sombra do texto
        }
        
        # Bar setup com posições melhoradas
        self.health_bar_rect = pygame.Rect(15, 15, HEALTH_BAR_WIDTH*3, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(15, 45, ENERGY_BAR_WIDTH, BAR_HEIGHT)
        
        # Convert weapon dictionary
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

        # Convert magic dictionary
        self.magic_graphics = []
        for magic in magic_data.values():
            magic = pygame.image.load(magic['graphic']).convert_alpha()
            self.magic_graphics.append(magic)

        self.pixelated_font = font_manager.get('text')

        # Status message variables
        self.status_message = ""
        self.status_message_duration = 2000
        self.status_message_start_time = 0
        self.current_level = 1
        
        # Cache para superfícies
        self.surface_cache = {}
        
        # Timer para animações
        self.animation_time = 0

    def create_gradient_bar(self, width, height, color1, color2):
        """Cria uma barra com gradiente"""
        cache_key = f"gradient_{width}_{height}_{color1}_{color2}"
        if cache_key in self.surface_cache:
            return self.surface_cache[cache_key]
        
        surface = pygame.Surface((width, height))
        for x in range(width):
            ratio = x / width
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            pygame.draw.line(surface, (r, g, b), (x, 0), (x, height))
        
        self.surface_cache[cache_key] = surface
        return surface

    def create_glowing_border(self, rect, color, intensity=1.0):
        """Cria um efeito de borda brilhante"""
        glow_surface = pygame.Surface((rect.width + 20, rect.height + 20), pygame.SRCALPHA)
        
        # Múltiplas camadas para efeito glow
        for i in range(5, 0, -1):
            alpha = int(50 * intensity * (i / 5))
            glow_color = (*color[:3], alpha)
            glow_rect = pygame.Rect(10 - i, 10 - i, rect.width + i*2, rect.height + i*2)
            pygame.draw.rect(glow_surface, glow_color, glow_rect, width=2)
        
        return glow_surface

    def show_modern_bar(self, current, max_amount, bg_rect, base_color, label=""):
        """Desenha uma barra moderna com gradiente e efeitos"""
        # Background com transparência
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        bg_surface.fill(self.colors['background'])
        self.display_surface.blit(bg_surface, bg_rect)
        
        # Calcular progresso
        ratio = max(0, current / max_amount) if max_amount > 0 else 0
        current_width = int(bg_rect.width * ratio)
        
        if current_width > 0:
            # Determinar cores baseadas no progresso
            if label == "health":
                if ratio > 0.6:
                    color1, color2 = self.colors['health_high'], (50, 200, 50)
                elif ratio > 0.3:
                    color1, color2 = self.colors['health_med'], (200, 200, 50)
                else:
                    color1, color2 = self.colors['health_low'], (200, 50, 50)
            else:
                color1, color2 = base_color, tuple(max(0, c - 50) for c in base_color)
            
            # Criar gradiente da barra
            if current_width > 0:
                gradient_bar = self.create_gradient_bar(current_width, bg_rect.height, color1, color2)
                self.display_surface.blit(gradient_bar, bg_rect)
        
        # Efeito pulse para vida baixa
        if label == "health" and ratio < 0.2:
            pulse = 0.5 + 0.5 * math.sin(self.animation_time * 0.1)
            glow = self.create_glowing_border(bg_rect, self.colors['health_low'], pulse)
            self.display_surface.blit(glow, (bg_rect.x - 10, bg_rect.y - 10))
        
        # Borda principal
        pygame.draw.rect(self.display_surface, self.colors['border'], bg_rect, 2)
        
        # Borda interna sutil
        inner_rect = pygame.Rect(bg_rect.x + 2, bg_rect.y + 2, bg_rect.width - 4, bg_rect.height - 4)
        pygame.draw.rect(self.display_surface, (60, 60, 80), inner_rect, 1)
        
        # Texto de valor se houver espaço
        if bg_rect.width > 100:
            text = f"{int(current)}/{int(max_amount)}"
            text_surface = self.font.render(text, True, self.colors['text'])
            text_rect = text_surface.get_rect(center=bg_rect.center)
            
            # Sombra do texto
            shadow_surface = self.font.render(text, True, self.colors['text_shadow'])
            shadow_rect = text_rect.copy()
            shadow_rect.x += 1
            shadow_rect.y += 1
            
            self.display_surface.blit(shadow_surface, shadow_rect)
            self.display_surface.blit(text_surface, text_rect)

    def show_enhanced_instructions(self, player):
        """Mostra instruções com visual melhorado"""
        instructions = {
            1: "Espaço: Atacar | Q: Trocar arma | E: Trocar magia | Ctrl: Usar magia",
            2: "Encontre uma saída do labirinto! | Q: Trocar arma | E: Magia", 
            3: f"Você tem {player.inventory['keys']} chaves | Q: Trocar arma",
            4: "Fuja! | Q: Trocar arma | E: Magia"
        }
        
        text = instructions.get(self.current_level, "")
        if not text:
            return
        
        text_surf = self.font.render(text, False, self.colors['text'])
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(x, y))

        # Background com gradiente sutil
        bg_rect = text_rect.inflate(25, 15)
        bg_surface = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
        
        # Gradiente de fundo
        for i in range(bg_rect.height):
            alpha = int(200 - (i / bg_rect.height) * 50)
            color = (*self.colors['background'][:3], alpha)
            pygame.draw.line(bg_surface, color, (0, i), (bg_rect.width, i))
        
        # Borda externa com glow sutil
        glow = self.create_glowing_border(bg_rect, self.colors['border'], 0.3)
        self.display_surface.blit(glow, (bg_rect.x - 10, bg_rect.y - 10))
        
        self.display_surface.blit(bg_surface, bg_rect)
        
        # Sombra do texto
        shadow_surf = self.font.render(text, False, self.colors['text_shadow'])
        shadow_rect = text_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        self.display_surface.blit(shadow_surf, shadow_rect)
        
        # Texto principal
        self.display_surface.blit(text_surf, text_rect)
        
        # Bordas elegantes
        pygame.draw.rect(self.display_surface, self.colors['border'], bg_rect, 2)
        pygame.draw.rect(self.display_surface, (180, 180, 200), bg_rect, 1)

    def enhanced_selection_box(self, left, top, has_switched):
        """Caixa de seleção com efeitos visuais melhorados"""
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        
        # Background com gradiente
        bg_surface = pygame.Surface((ITEM_BOX_SIZE, ITEM_BOX_SIZE), pygame.SRCALPHA)
        
        # Gradiente de fundo
        for y in range(ITEM_BOX_SIZE):
            ratio = y / ITEM_BOX_SIZE
            alpha = int(160 + 40 * (1 - ratio))
            color = (*self.colors['background'][:3], alpha)
            pygame.draw.line(bg_surface, color, (0, y), (ITEM_BOX_SIZE, y))
        
        self.display_surface.blit(bg_surface, bg_rect)
        
        # Efeito de estado ativo
        if has_switched:
            # Glow dourado para item ativo
            glow = self.create_glowing_border(bg_rect, self.colors['border_active'], 0.8)
            self.display_surface.blit(glow, (bg_rect.x - 10, bg_rect.y - 10))
            
            # Borda dourada
            pygame.draw.rect(self.display_surface, self.colors['border_active'], bg_rect, 3)
            pygame.draw.rect(self.display_surface, (255, 255, 200), bg_rect, 1)
            
            # Highlight interno
            inner_rect = pygame.Rect(bg_rect.x + 4, bg_rect.y + 4, bg_rect.width - 8, bg_rect.height - 8)
            pygame.draw.rect(self.display_surface, (255, 255, 150, 50), inner_rect)
        else:
            # Estado normal
            pygame.draw.rect(self.display_surface, self.colors['border'], bg_rect, 2)
            pygame.draw.rect(self.display_surface, (160, 160, 180), bg_rect, 1)
        
        return bg_rect

    def weapon_overlay(self, weapon_index, has_switched):
        """Overlay de arma melhorado"""
        bg_rect = self.enhanced_selection_box(15, 630, has_switched)
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(weapon_surf, weapon_rect)

    def magic_overlay(self, magic_index, has_switched):
        """Overlay de magia melhorado"""
        bg_rect = self.enhanced_selection_box(85, 630, has_switched)
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(magic_surf, magic_rect)

    def show_enhanced_status_message(self):
        """Mensagem de status com visual melhorado"""
        if not self.status_message:
            return
        
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.status_message_start_time

        if elapsed_time < self.status_message_duration:
            # Efeito fade in/out
            progress = elapsed_time / self.status_message_duration
            if progress < 0.1:
                alpha_mult = progress / 0.1
            elif progress > 0.9:
                alpha_mult = (1 - progress) / 0.1
            else:
                alpha_mult = 1.0
            
            text_surface = self.pixelated_font.render(self.status_message, True, self.colors['text'])
            x = self.display_surface.get_size()[0] // 2 - text_surface.get_width() // 2
            y = self.display_surface.get_size()[1] - 100
            text_rect = text_surface.get_rect(topleft=(x, y))

            # Background elegante com fade
            bg_rect = text_rect.inflate(40, 20)
            bg_surface = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
            
            # Gradiente com alpha dinâmico
            for i in range(bg_rect.height):
                base_alpha = int(200 * alpha_mult)
                alpha = int(base_alpha - (i / bg_rect.height) * 60)
                color = (*self.colors['background'][:3], alpha)
                pygame.draw.line(bg_surface, color, (0, i), (bg_rect.width, i))
            
            # Glow baseado no fade
            if alpha_mult > 0.5:
                glow = self.create_glowing_border(bg_rect, self.colors['border'], alpha_mult * 0.5)
                self.display_surface.blit(glow, (bg_rect.x - 10, bg_rect.y - 10))
            
            self.display_surface.blit(bg_surface, bg_rect)
            
            # Sombra com alpha
            shadow_surface = self.pixelated_font.render(self.status_message, True, self.colors['text_shadow'])
            shadow_surface.set_alpha(int(255 * alpha_mult))
            shadow_rect = text_rect.copy()
            shadow_rect.x += 2
            shadow_rect.y += 2
            self.display_surface.blit(shadow_surface, shadow_rect)
            
            # Texto principal com alpha
            text_surface.set_alpha(int(255 * alpha_mult))
            self.display_surface.blit(text_surface, text_rect)
            
            # Bordas com alpha
            border_color = (*self.colors['border'], int(255 * alpha_mult))
            pygame.draw.rect(self.display_surface, border_color, bg_rect, 2)
        else:
            self.status_message = ""

    def display(self, player):
        """Display principal da UI melhorada"""
        # Atualizar timer de animação
        self.animation_time += 0.1
        
        # Barras modernas
        self.show_modern_bar(
            player.health, 
            player.stats['health'], 
            self.health_bar_rect, 
            self.colors['health_high'],
            "health"
        )
        
        self.show_modern_bar(
            player.energy, 
            player.stats['energy'], 
            self.energy_bar_rect, 
            self.colors['energy']
        )
        
        # Elementos de UI melhorados
        self.show_enhanced_instructions(player)
        self.show_enhanced_status_message()
        
        # Overlays de arma e magia
        self.weapon_overlay(player.weapon_index, not player.can_switch_weapon)
        self.magic_overlay(player.magic_index, not player.can_switch_magic)

    def set_status_message(self, message):
        """Define mensagem de status"""
        self.status_message = message
        self.status_message_start_time = pygame.time.get_ticks()

# Rename class to maintain compatibility
UI = EnhancedUI

# Remove global instance that causes initialization issues