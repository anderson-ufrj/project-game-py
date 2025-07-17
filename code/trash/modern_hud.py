"""
HUD Moderno para o Jogo com Barras Animadas e Efeitos
"""
import pygame
import math
from typing import Dict, List, Tuple, Optional
from modern_ui_system import modern_ui
from dataclasses import dataclass
from enum import Enum

class AnimationType(Enum):
    SLIDE_IN = "slide_in"
    FADE_IN = "fade_in" 
    BOUNCE = "bounce"
    PULSE = "pulse"

@dataclass
class HUDAnimation:
    """Animação para elementos do HUD"""
    element_id: str
    animation_type: AnimationType
    duration: float
    progress: float = 0.0
    start_value: float = 0.0
    end_value: float = 1.0
    delay: float = 0.0

class ModernHUD:
    """HUD moderno com animações e efeitos visuais"""
    
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.width, self.height = self.screen.get_size()
        
        # Cache de superfícies
        self.surface_cache = {}
        
        # Animações ativas
        self.animations: List[HUDAnimation] = []
        
        # Estado dos elementos
        self.element_states = {
            "health_visible": True,
            "energy_visible": True,
            "minimap_visible": False,
            "inventory_visible": False
        }
        
        # Posições dos elementos
        self.setup_positions()
        
        # Cores e estilo
        self.colors = modern_ui.get_current_colors()
        
        # Fonts
        self.fonts = {
            "large": pygame.font.Font(None, 36),
            "medium": pygame.font.Font(None, 24),
            "small": pygame.font.Font(None, 18)
        }
        
        print("🎮 HUD Moderno inicializado!")
    
    def setup_positions(self):
        """Define posições dos elementos do HUD"""
        # Margem das bordas
        margin = 20
        
        # Barra de vida (canto superior esquerdo)
        self.health_bar_rect = pygame.Rect(
            margin, margin, 300, 40
        )
        
        # Barra de energia (abaixo da vida)
        self.energy_bar_rect = pygame.Rect(
            margin, margin + 50, 250, 30
        )
        
        # Inventário (canto superior direito)
        self.inventory_rect = pygame.Rect(
            self.width - 250 - margin, margin, 250, 100
        )
        
        # Minimap (canto inferior direito)
        self.minimap_rect = pygame.Rect(
            self.width - 220 - margin, self.height - 170 - margin, 220, 170
        )
        
        # Status messages (centro superior)
        self.status_rect = pygame.Rect(
            (self.width - 400) // 2, margin, 400, 50
        )
        
        # FPS Counter (canto superior direito)
        self.fps_rect = pygame.Rect(
            self.width - 100 - margin, margin, 100, 30
        )
    
    def create_gradient_bar(self, size: Tuple[int, int], 
                          color1: Tuple[int, int, int], 
                          color2: Tuple[int, int, int],
                          vertical: bool = False) -> pygame.Surface:
        """Cria uma barra com gradiente"""
        cache_key = f"gradient_bar_{size}_{color1}_{color2}_{vertical}"
        
        if cache_key in self.surface_cache:
            return self.surface_cache[cache_key]
        
        surface = pygame.Surface(size, pygame.SRCALPHA)
        
        if vertical:
            for y in range(size[1]):
                ratio = y / size[1]
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                pygame.draw.line(surface, (r, g, b), (0, y), (size[0], y))
        else:
            for x in range(size[0]):
                ratio = x / size[0]
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                pygame.draw.line(surface, (r, g, b), (x, 0), (x, size[1]))
        
        self.surface_cache[cache_key] = surface
        return surface
    
    def draw_modern_health_bar(self, surface: pygame.Surface, 
                             current_health: int, 
                             max_health: int):
        """Desenha barra de vida moderna"""
        rect = self.health_bar_rect
        
        # Background com transparência
        bg_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        bg_surface.fill((*self.colors.background, 180))
        pygame.draw.rect(bg_surface, self.colors.surface, 
                        pygame.Rect(0, 0, rect.width, rect.height), 
                        border_radius=10)
        surface.blit(bg_surface, rect)
        
        # Borda externa
        pygame.draw.rect(surface, self.colors.primary, rect, width=2, border_radius=10)
        
        # Calcular porcentagem de vida
        health_percentage = current_health / max_health if max_health > 0 else 0
        
        # Barra de vida com gradiente
        if health_percentage > 0:
            bar_width = int((rect.width - 10) * health_percentage)
            bar_rect = pygame.Rect(rect.x + 5, rect.y + 5, bar_width, rect.height - 10)
            
            # Determinar cores baseadas na vida
            if health_percentage > 0.6:
                color1 = (100, 255, 100)  # Verde claro
                color2 = (50, 200, 50)    # Verde escuro
            elif health_percentage > 0.3:
                color1 = (255, 255, 100)  # Amarelo claro
                color2 = (200, 200, 50)   # Amarelo escuro
            else:
                color1 = (255, 100, 100)  # Vermelho claro
                color2 = (200, 50, 50)    # Vermelho escuro
            
            # Criar gradiente
            gradient = self.create_gradient_bar((bar_width, rect.height - 10), color1, color2)
            surface.blit(gradient, bar_rect)
            
            # Efeito pulsante quando vida baixa
            if health_percentage < 0.2:
                pulse = 0.8 + 0.2 * math.sin(pygame.time.get_ticks() * 0.01)
                glow_surface = modern_ui.create_glow_surface(
                    (bar_width + 20, rect.height + 10),
                    (255, 0, 0),
                    pulse * 0.5
                )
                surface.blit(glow_surface, (bar_rect.x - 10, bar_rect.y - 5))
        
        # Ícone de vida
        heart_color = self.colors.error if health_percentage < 0.3 else self.colors.success
        heart_rect = pygame.Rect(rect.x + 10, rect.y + 8, 24, 24)
        pygame.draw.circle(surface, heart_color, (heart_rect.x + 6, heart_rect.y + 8), 6)
        pygame.draw.circle(surface, heart_color, (heart_rect.x + 18, heart_rect.y + 8), 6)
        
        # Texto de vida
        health_text = f"{current_health}/{max_health}"
        text_surface = self.fonts["medium"].render(health_text, True, self.colors.text_primary)
        text_rect = text_surface.get_rect(center=(rect.centerx + 20, rect.centery))
        surface.blit(text_surface, text_rect)
    
    def draw_modern_energy_bar(self, surface: pygame.Surface, 
                             current_energy: float, 
                             max_energy: float):
        """Desenha barra de energia moderna"""
        rect = self.energy_bar_rect
        
        # Background
        bg_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        bg_surface.fill((*self.colors.background, 160))
        pygame.draw.rect(bg_surface, self.colors.surface, 
                        pygame.Rect(0, 0, rect.width, rect.height), 
                        border_radius=8)
        surface.blit(bg_surface, rect)
        
        # Borda
        pygame.draw.rect(surface, self.colors.secondary, rect, width=2, border_radius=8)
        
        # Calcular porcentagem de energia
        energy_percentage = current_energy / max_energy if max_energy > 0 else 0
        
        # Barra de energia
        if energy_percentage > 0:
            bar_width = int((rect.width - 8) * energy_percentage)
            bar_rect = pygame.Rect(rect.x + 4, rect.y + 4, bar_width, rect.height - 8)
            
            # Gradiente azul
            gradient = self.create_gradient_bar(
                (bar_width, rect.height - 8),
                (100, 200, 255),  # Azul claro
                (50, 100, 200)    # Azul escuro
            )
            surface.blit(gradient, bar_rect)
            
            # Efeito cintilante
            if energy_percentage > 0.8:
                shimmer = 0.3 + 0.2 * math.sin(pygame.time.get_ticks() * 0.02)
                shimmer_surface = pygame.Surface((bar_width, rect.height - 8), pygame.SRCALPHA)
                shimmer_surface.fill((255, 255, 255, int(shimmer * 100)))
                surface.blit(shimmer_surface, bar_rect)
        
        # Ícone de energia (raio)
        lightning_color = self.colors.secondary
        bolt_points = [
            (rect.x + 8, rect.y + 6),
            (rect.x + 12, rect.y + 6),
            (rect.x + 10, rect.y + 12),
            (rect.x + 16, rect.y + 12),
            (rect.x + 12, rect.y + 24),
            (rect.x + 8, rect.y + 18),
            (rect.x + 10, rect.y + 12)
        ]
        pygame.draw.polygon(surface, lightning_color, bolt_points)
        
        # Texto de energia
        energy_text = f"{int(current_energy)}/{int(max_energy)}"
        text_surface = self.fonts["small"].render(energy_text, True, self.colors.text_primary)
        text_rect = text_surface.get_rect(center=(rect.centerx + 15, rect.centery))
        surface.blit(text_surface, text_rect)
    
    def draw_modern_inventory(self, surface: pygame.Surface, inventory: Dict):
        """Desenha inventário moderno"""
        if not self.element_states["inventory_visible"]:
            return
        
        rect = self.inventory_rect
        
        # Background com transparência
        bg_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        bg_surface.fill((*self.colors.background, 200))
        pygame.draw.rect(bg_surface, self.colors.surface, 
                        pygame.Rect(0, 0, rect.width, rect.height), 
                        border_radius=12)
        surface.blit(bg_surface, rect)
        
        # Borda com glow
        glow = modern_ui.create_glow_surface((rect.width + 10, rect.height + 10), 
                                           self.colors.accent, 0.2)
        surface.blit(glow, (rect.x - 5, rect.y - 5))
        pygame.draw.rect(surface, self.colors.accent, rect, width=2, border_radius=12)
        
        # Título
        title_text = self.fonts["medium"].render("INVENTÁRIO", True, self.colors.text_primary)
        surface.blit(title_text, (rect.x + 10, rect.y + 8))
        
        # Items
        y_offset = 35
        item_height = 15
        
        items = [
            ("🔮 Pedras Místicas", inventory.get("zappaguriStone", 0)),
            ("🔑 Chaves", inventory.get("keys", 0)),
            ("❤️ Orbs de Vida", inventory.get("healthOrbs", 0)),
            ("⚡ Orbs de Energia", inventory.get("attackOrbs", 0)),
            ("💨 Orbs de Velocidade", inventory.get("speedOrbs", 0))
        ]
        
        for item_name, count in items:
            # Item background se houver itens
            if count > 0:
                item_bg = pygame.Rect(rect.x + 5, rect.y + y_offset - 2, 
                                    rect.width - 10, item_height + 2)
                pygame.draw.rect(surface, (*self.colors.primary, 50), item_bg, border_radius=4)
            
            # Texto do item
            color = self.colors.text_primary if count > 0 else self.colors.text_secondary
            item_text = f"{item_name}: {count}"
            text_surface = self.fonts["small"].render(item_text, True, color)
            surface.blit(text_surface, (rect.x + 10, rect.y + y_offset))
            
            y_offset += item_height + 2
    
    def draw_modern_minimap(self, surface: pygame.Surface, level: int, player_pos: Tuple[int, int]):
        """Desenha minimapa moderno"""
        if not self.element_states["minimap_visible"]:
            return
        
        rect = self.minimap_rect
        
        # Background
        bg_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        bg_surface.fill((*self.colors.background, 220))
        pygame.draw.rect(bg_surface, self.colors.surface, 
                        pygame.Rect(0, 0, rect.width, rect.height), 
                        border_radius=15)
        surface.blit(bg_surface, rect)
        
        # Borda
        pygame.draw.rect(surface, self.colors.primary, rect, width=3, border_radius=15)
        
        # Título
        title_text = f"MAPA - NÍVEL {level}"
        title_surface = self.fonts["small"].render(title_text, True, self.colors.text_primary)
        surface.blit(title_surface, (rect.x + 10, rect.y + 5))
        
        # Área do mapa
        map_rect = pygame.Rect(rect.x + 10, rect.y + 25, rect.width - 20, rect.height - 35)
        pygame.draw.rect(surface, self.colors.background, map_rect, border_radius=8)
        
        # Grid do mapa
        grid_size = 20
        for x in range(0, map_rect.width, grid_size):
            for y in range(0, map_rect.height, grid_size):
                grid_rect = pygame.Rect(map_rect.x + x, map_rect.y + y, grid_size, grid_size)
                pygame.draw.rect(surface, (*self.colors.surface, 100), grid_rect, width=1)
        
        # Posição do player
        player_x = map_rect.x + (player_pos[0] % map_rect.width)
        player_y = map_rect.y + (player_pos[1] % map_rect.height)
        
        # Efeito pulsante no player
        pulse = 0.8 + 0.4 * math.sin(pygame.time.get_ticks() * 0.01)
        player_radius = int(8 * pulse)
        
        pygame.draw.circle(surface, self.colors.accent, (player_x, player_y), player_radius + 2)
        pygame.draw.circle(surface, self.colors.text_primary, (player_x, player_y), player_radius)
    
    def draw_status_message(self, surface: pygame.Surface, message: str, duration: float = 3.0):
        """Desenha mensagem de status moderna"""
        if not message:
            return
        
        rect = self.status_rect
        
        # Background com transparência
        bg_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        bg_surface.fill((*self.colors.accent, 200))
        pygame.draw.rect(bg_surface, (*self.colors.primary, 150), 
                        pygame.Rect(0, 0, rect.width, rect.height), 
                        border_radius=25)
        surface.blit(bg_surface, rect)
        
        # Glow effect
        glow = modern_ui.create_glow_surface((rect.width + 20, rect.height + 20), 
                                           self.colors.accent, 0.4)
        surface.blit(glow, (rect.x - 10, rect.y - 10))
        
        # Texto centralizado
        text_surface = self.fonts["large"].render(message, True, self.colors.text_primary)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)
    
    def draw_fps_counter(self, surface: pygame.Surface, fps: float):
        """Desenha contador de FPS"""
        if not self.element_states.get("show_fps", False):
            return
        
        rect = self.fps_rect
        
        # Background
        bg_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        bg_surface.fill((*self.colors.background, 150))
        surface.blit(bg_surface, rect)
        
        # Cor baseada no FPS
        if fps >= 50:
            color = self.colors.success
        elif fps >= 30:
            color = self.colors.warning
        else:
            color = self.colors.error
        
        # Texto FPS
        fps_text = f"FPS: {int(fps)}"
        text_surface = self.fonts["small"].render(fps_text, True, color)
        surface.blit(text_surface, (rect.x + 5, rect.y + 5))
    
    def add_animation(self, element_id: str, animation_type: AnimationType, 
                     duration: float, start_value: float = 0.0, 
                     end_value: float = 1.0, delay: float = 0.0):
        """Adiciona uma animação"""
        animation = HUDAnimation(
            element_id=element_id,
            animation_type=animation_type,
            duration=duration,
            start_value=start_value,
            end_value=end_value,
            delay=delay
        )
        self.animations.append(animation)
    
    def update_animations(self, dt: float):
        """Atualiza todas as animações"""
        for animation in self.animations[:]:
            if animation.delay > 0:
                animation.delay -= dt
                continue
            
            animation.progress += dt / animation.duration
            
            if animation.progress >= 1.0:
                animation.progress = 1.0
                self.animations.remove(animation)
    
    def toggle_element(self, element: str):
        """Alterna visibilidade de um elemento"""
        if element in self.element_states:
            self.element_states[element] = not self.element_states[element]
            
            # Adicionar animação
            if self.element_states[element]:
                self.add_animation(element, AnimationType.FADE_IN, 0.3)
            else:
                self.add_animation(element, AnimationType.FADE_IN, 0.3, 1.0, 0.0)
    
    def update(self, dt: float):
        """Atualiza o HUD"""
        self.update_animations(dt)
    
    def draw_complete_hud(self, surface: pygame.Surface, 
                         player_health: int, player_max_health: int,
                         player_energy: float, player_max_energy: float,
                         inventory: Dict, level: int, 
                         player_pos: Tuple[int, int],
                         status_message: str = "",
                         fps: float = 60.0):
        """Desenha o HUD completo"""
        # Barras principais
        self.draw_modern_health_bar(surface, player_health, player_max_health)
        self.draw_modern_energy_bar(surface, player_energy, player_max_energy)
        
        # Elementos opcionais
        self.draw_modern_inventory(surface, inventory)
        self.draw_modern_minimap(surface, level, player_pos)
        self.draw_fps_counter(surface, fps)
        
        # Mensagens
        if status_message:
            self.draw_status_message(surface, status_message)

# Singleton global
modern_hud = ModernHUD()