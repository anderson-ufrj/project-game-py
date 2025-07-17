import pygame
import math
import time
import random
from settings import *
from font_manager import font_manager
from graphics_screen import GraphicsScreen
from tutorial_system import tutorial_system

class GemSparkle:
    """Partícula de brilho para a pedra/gema"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.size = random.uniform(1, 3)
        self.life = random.uniform(60, 120)
        self.max_life = self.life
        self.color = random.choice([
            (186, 85, 211),   # Violeta médio
            (138, 43, 226),   # Violeta azul
            (147, 0, 211),    # Violeta escuro
            (221, 160, 221),  # Plum
            (218, 112, 214),  # Orquídea
        ])
        self.oscillation = random.uniform(0, math.pi * 2)
        self.float_speed = random.uniform(0.3, 0.8)
    
    def update(self):
        # Movimento flutuante sutil
        self.x += math.sin(pygame.time.get_ticks() * 0.003 + self.oscillation) * 0.2
        self.y -= self.float_speed
        self.life -= 1
        
        # Resetar quando morrer
        if self.life <= 0:
            return False
        return True
    
    def draw(self, surface):
        if self.life > 0:
            alpha = int(255 * (self.life / self.max_life))
            # Criar surface com alpha
            particle_surface = pygame.Surface((int(self.size * 4), int(self.size * 4)), pygame.SRCALPHA)
            
            # Core brilhante
            core_color = (*self.color, alpha)
            pygame.draw.circle(particle_surface, core_color, 
                             (int(self.size * 2), int(self.size * 2)), int(self.size))
            
            # Glow sutil
            if alpha > 50:
                glow_color = (*self.color, int(alpha * 0.3))
                pygame.draw.circle(particle_surface, glow_color,
                                 (int(self.size * 2), int(self.size * 2)), int(self.size * 2))
            
            surface.blit(particle_surface, (int(self.x - self.size * 2), int(self.y - self.size * 2)))

class CleanMenuButton:
    """Botão limpo e elegante"""
    
    def __init__(self, x, y, width, height, text, action, font=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.font = font or font_manager.get('button')
        
        # Estados
        self.hover = False
        self.click_animation = 0.0
        self.hover_animation = 0.0
        
        # Cores elegantes
        self.colors = {
            'normal': (45, 45, 55),
            'hover': (65, 65, 75),
            'click': (85, 85, 95),
            'border': (120, 120, 130),
            'border_hover': (180, 180, 190),
            'text': (255, 255, 255),
            'text_hover': (255, 255, 255)
        }
    
    def update(self, mouse_pos, mouse_click):
        """Atualiza estado do botão"""
        was_hover = self.hover
        self.hover = self.rect.collidepoint(mouse_pos)
        
        # Animações suaves
        if self.hover:
            self.hover_animation = min(1.0, self.hover_animation + 0.08)
        else:
            self.hover_animation = max(0.0, self.hover_animation - 0.08)
        
        # Clique
        if self.hover and mouse_click:
            self.click_animation = 1.0
            return self.action
        
        # Decay do clique
        if self.click_animation > 0:
            self.click_animation = max(0, self.click_animation - 0.15)
        
        return None
    
    def draw(self, surface):
        """Desenha o botão"""
        # Cor do fundo baseada no estado
        if self.click_animation > 0:
            bg_color = self.colors['click']
        elif self.hover_animation > 0:
            # Interpolação suave entre normal e hover
            factor = self.hover_animation
            normal = self.colors['normal']
            hover = self.colors['hover']
            bg_color = (
                int(normal[0] + (hover[0] - normal[0]) * factor),
                int(normal[1] + (hover[1] - normal[1]) * factor),
                int(normal[2] + (hover[2] - normal[2]) * factor)
            )
        else:
            bg_color = self.colors['normal']
        
        # Efeito de clique
        draw_rect = self.rect.copy()
        if self.click_animation > 0:
            offset = int(self.click_animation * 2)
            draw_rect.x += offset
            draw_rect.y += offset
        
        # Fundo
        pygame.draw.rect(surface, bg_color, draw_rect, border_radius=8)
        
        # Borda
        border_color = self.colors['border_hover'] if self.hover else self.colors['border']
        pygame.draw.rect(surface, border_color, draw_rect, width=2, border_radius=8)
        
        # Texto
        text_color = self.colors['text_hover'] if self.hover else self.colors['text']
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=draw_rect.center)
        surface.blit(text_surface, text_rect)

class CleanMainMenu:
    """Menu principal limpo e elegante"""
    
    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts = fonts
        
        # Carregar background
        try:
            self.background = pygame.image.load('../graphics/ui/home page.jpg').convert()
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGTH))
        except:
            print("Erro ao carregar background - usando cor sólida")
            self.background = self.create_simple_background()
        
        # Fontes
        self.title_font = font_manager.get('title')
        self.subtitle_font = font_manager.get('subtitle')
        self.button_font = font_manager.get('text')
        
        # Animações
        self.time = 0
        self.title_alpha = 255
        
        # Sistema de partículas da pedra/gema
        self.gem_sparkles = []
        self.sparkle_spawn_timer = 0
        
        # Criar botões
        self.create_clean_buttons()
        
        # Configurações gráficas
        self.graphics_screen = GraphicsScreen()
    
    def create_simple_background(self):
        """Cria fundo simples se não conseguir carregar"""
        surface = pygame.Surface((WIDTH, HEIGTH))
        surface.fill((25, 25, 35))  # Azul escuro
        return surface
    
    def create_clean_buttons(self):
        """Cria botões limpos e bem posicionados"""
        button_width = 200
        button_height = 40
        button_spacing = 10
        
        # Posicionar no lado direito, mas não muito colado na borda
        start_x = WIDTH - button_width - 100
        start_y = 300
        
        self.buttons = [
            CleanMenuButton(start_x, start_y, button_width, button_height, 
                          "INICIAR JOGO", "start_game", self.button_font),
            CleanMenuButton(start_x, start_y + (button_height + button_spacing), button_width, button_height, 
                          "TUTORIAL", "show_tutorial", self.button_font),
            CleanMenuButton(start_x, start_y + (button_height + button_spacing) * 2, button_width, button_height, 
                          "CONFIGURAÇÕES", "show_graphics", self.button_font),
            CleanMenuButton(start_x, start_y + (button_height + button_spacing) * 3, button_width, button_height, 
                          "ESTATÍSTICAS", "show_stats", self.button_font),
            CleanMenuButton(start_x, start_y + (button_height + button_spacing) * 4, button_width, button_height, 
                          "SAIR", "quit_game", self.button_font)
        ]
    
    def draw_clean_title(self):
        """Desenha título limpo"""
        # Título principal com sombra sutil
        title_text = "CORRIDA PELA RELÍQUIA"
        
        # Sombra
        shadow_surface = self.title_font.render(title_text, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect(center=(WIDTH // 2 + 2, 102))
        self.screen.blit(shadow_surface, shadow_rect)
        
        # Título
        title_surface = self.title_font.render(title_text, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(WIDTH // 2, 100))
        self.screen.blit(title_surface, title_rect)
        
        # Subtítulo simples
        subtitle_text = "A Busca pela Pedra Mística de Zappaguri"
        subtitle_surface = self.subtitle_font.render(subtitle_text, True, (200, 200, 220))
        subtitle_rect = subtitle_surface.get_rect(center=(WIDTH // 2, 130))
        
        # Sombra do subtítulo
        subtitle_shadow = self.subtitle_font.render(subtitle_text, True, (0, 0, 0))
        shadow_rect = subtitle_shadow.get_rect(center=(WIDTH // 2 + 1, 131))
        self.screen.blit(subtitle_shadow, shadow_rect)
        self.screen.blit(subtitle_surface, subtitle_rect)
    
    def draw_footer_info(self):
        """Desenha informações simples no rodapé"""
        footer_font = font_manager.get('small')
        
        # Informações essenciais
        info_text = "Enter: Iniciar Jogo • Alt+Enter: Tela Cheia • ESC: Sair"
        info_surface = footer_font.render(info_text, True, (150, 150, 170))
        info_rect = info_surface.get_rect(center=(WIDTH // 2, HEIGTH - 30))
        
        # Sombra
        shadow_surface = footer_font.render(info_text, True, (0, 0, 0))
        shadow_rect = shadow_surface.get_rect(center=(WIDTH // 2 + 1, HEIGTH - 29))
        self.screen.blit(shadow_surface, shadow_rect)
        self.screen.blit(info_surface, info_rect)
    
    def handle_event(self, event):
        """Manipula eventos"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return "start_game"
            elif event.key == pygame.K_ESCAPE:
                return "quit_game"
            elif event.key == pygame.K_t:
                tutorial_system.open_tutorial()
                return "show_tutorial"
            elif event.key == pygame.K_g:
                self.graphics_screen.open_screen()
                return "show_graphics"
        
        # Eventos da tela de gráficos
        if self.graphics_screen.is_open():
            if event.type == pygame.KEYDOWN:
                self.graphics_screen.handle_keydown(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.graphics_screen.handle_mouse_click(event.pos)
            return None
        
        return None
    
    def update_gem_sparkles(self):
        """Atualiza partículas de brilho da pedra"""
        # Atualizar partículas existentes
        self.gem_sparkles = [sparkle for sparkle in self.gem_sparkles if sparkle.update()]
        
        # Spawn novas partículas (assumindo que a pedra está no centro-esquerda da tela)
        self.sparkle_spawn_timer += 1
        if self.sparkle_spawn_timer > 15:  # Spawn a cada 15 frames
            # Área aproximada onde a pedra/gema deve estar na imagem de fundo
            gem_center_x = WIDTH // 2 - 100  # Mais central
            gem_center_y = HEIGTH // 2 + 50   # Ligeiramente abaixo do centro
            
            # Spawn em uma área circular ao redor da pedra
            angle = random.uniform(0, math.pi * 2)
            radius = random.uniform(10, 80)
            spawn_x = gem_center_x + math.cos(angle) * radius
            spawn_y = gem_center_y + math.sin(angle) * radius
            
            self.gem_sparkles.append(GemSparkle(spawn_x, spawn_y))
            self.sparkle_spawn_timer = 0
        
        # Manter máximo de partículas
        if len(self.gem_sparkles) > 25:
            self.gem_sparkles = self.gem_sparkles[-25:]
    
    def draw_gem_sparkles(self):
        """Desenha as partículas de brilho da pedra"""
        for sparkle in self.gem_sparkles:
            sparkle.draw(self.screen)
    
    def update_and_draw(self, mouse_pos, mouse_click):
        """Atualiza e desenha o menu"""
        self.time = pygame.time.get_ticks()
        
        # Background
        self.screen.blit(self.background, (0, 0))
        
        # Efeitos de brilho da pedra (atrás do overlay)
        self.update_gem_sparkles()
        self.draw_gem_sparkles()
        
        # Overlay sutil para melhor contraste
        overlay = pygame.Surface((WIDTH, HEIGTH), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 60))
        self.screen.blit(overlay, (0, 0))
        
        # Título
        self.draw_clean_title()
        
        # Botões
        action = None
        if not self.graphics_screen.is_open():
            for button in self.buttons:
                button_action = button.update(mouse_pos, mouse_click)
                if button_action:
                    action = button_action
                button.draw(self.screen)
        
        # Informações do rodapé
        self.draw_footer_info()
        
        # Tela de gráficos
        self.graphics_screen.draw(self.screen)
        
        return action

# Função para obter o menu limpo
def get_clean_menu(screen, fonts):
    return CleanMainMenu(screen, fonts)