"""
Menu Principal Moderno com Animações e Efeitos
"""
import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UILabel, UIImage
import math
import random
from typing import List, Tuple, Optional
from modern_ui_system import modern_ui, UITheme
from enum import Enum
from dataclasses import dataclass

class MenuState(Enum):
    MAIN = "main"
    SETTINGS = "settings"
    CREDITS = "credits"
    LOADING = "loading"

@dataclass
class ParticleEffect:
    """Partícula para efeitos visuais"""
    x: float
    y: float
    vx: float
    vy: float
    size: float
    color: Tuple[int, int, int]
    lifetime: float
    max_lifetime: float
    glow: bool = False

class ModernMainMenu:
    """Menu principal com visual moderno e animações"""
    
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.width, self.height = self.screen.get_size()
        
        # Estado do menu
        self.state = MenuState.MAIN
        self.transition_alpha = 0
        self.transitioning = False
        
        # Animações
        self.animation_time = 0
        self.particles: List[ParticleEffect] = []
        self.background_offset = 0
        
        # Elementos UI
        self.ui_elements = {}
        self.create_ui_elements()
        
        # Efeitos
        self.logo_scale = 1.0
        self.logo_glow = 0
        self.button_hover_states = {}
        
        # Background
        self.create_animated_background()
        
        # Sons (usar AudioManager quando disponível)
        self.hover_sound = None
        self.click_sound = None
        
        print("🎮 Menu Principal Moderno inicializado!")
    
    def create_animated_background(self):
        """Cria background animado com gradientes"""
        self.bg_surface = pygame.Surface((self.width * 2, self.height * 2))
        
        # Criar padrão de gradiente complexo
        colors = modern_ui.get_current_colors()
        
        # Gradiente base
        for y in range(self.height * 2):
            ratio = y / (self.height * 2)
            # Interpolar entre background e surface color
            r = int(colors.background[0] * (1 - ratio) + colors.surface[0] * ratio)
            g = int(colors.background[1] * (1 - ratio) + colors.surface[1] * ratio)
            b = int(colors.background[2] * (1 - ratio) + colors.surface[2] * ratio)
            
            # Adicionar variação sinusoidal
            variation = int(20 * math.sin(y * 0.01))
            r = max(0, min(255, r + variation))
            
            pygame.draw.line(self.bg_surface, (r, g, b), (0, y), (self.width * 2, y))
        
        # Adicionar padrões geométricos
        for i in range(20):
            x = random.randint(0, self.width * 2)
            y = random.randint(0, self.height * 2)
            size = random.randint(50, 200)
            alpha = random.randint(5, 20)
            
            # Círculos com gradiente
            for radius in range(size, 0, -5):
                circle_alpha = int(alpha * (radius / size))
                color = (*colors.primary, circle_alpha)
                pygame.draw.circle(self.bg_surface, color, (x, y), radius)
    
    def create_ui_elements(self):
        """Cria elementos modernos da UI"""
        colors = modern_ui.get_current_colors()
        
        # Container principal
        self.main_container = pygame.Rect(0, 0, self.width, self.height)
        
        # Logo/Título com efeitos
        self.title_text = "CORRIDA PELA RELÍQUIA"
        self.title_font = pygame.font.Font(None, 72)
        self.subtitle_text = "A Busca pela Pedra Mística"
        self.subtitle_font = pygame.font.Font(None, 36)
        
        # Botões principais com Pygame GUI
        button_width = 300
        button_height = 60
        button_spacing = 80
        start_y = self.height // 2
        
        # Botão Novo Jogo
        self.new_game_button = UIButton(
            relative_rect=pygame.Rect(
                (self.width - button_width) // 2,
                start_y,
                button_width,
                button_height
            ),
            text='NOVO JOGO',
            manager=modern_ui.manager,
            object_id='#new_game_button'
        )
        
        # Botão Continuar
        self.continue_button = UIButton(
            relative_rect=pygame.Rect(
                (self.width - button_width) // 2,
                start_y + button_spacing,
                button_width,
                button_height
            ),
            text='CONTINUAR',
            manager=modern_ui.manager,
            object_id='#continue_button'
        )
        
        # Botão Configurações
        self.settings_button = UIButton(
            relative_rect=pygame.Rect(
                (self.width - button_width) // 2,
                start_y + button_spacing * 2,
                button_width,
                button_height
            ),
            text='CONFIGURAÇÕES',
            manager=modern_ui.manager,
            object_id='#settings_button'
        )
        
        # Botão Sair
        self.quit_button = UIButton(
            relative_rect=pygame.Rect(
                (self.width - button_width) // 2,
                start_y + button_spacing * 3,
                button_width,
                button_height
            ),
            text='SAIR',
            manager=modern_ui.manager,
            object_id='#quit_button'
        )
        
        # Registrar callbacks
        modern_ui.callbacks['#new_game_button'] = self.on_new_game
        modern_ui.callbacks['#continue_button'] = self.on_continue
        modern_ui.callbacks['#settings_button'] = self.on_settings
        modern_ui.callbacks['#quit_button'] = self.on_quit
        
        # Criar partículas iniciais
        self.spawn_particles(50)
    
    def spawn_particles(self, count: int):
        """Cria partículas para efeitos visuais"""
        colors = modern_ui.get_current_colors()
        
        for _ in range(count):
            # Posição aleatória
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            
            # Velocidade aleatória
            vx = random.uniform(-0.5, 0.5)
            vy = random.uniform(-1.0, -0.2)
            
            # Propriedades
            size = random.uniform(1, 4)
            lifetime = random.uniform(3, 6)
            
            # Cor aleatória do tema
            color_choices = [
                colors.primary,
                colors.secondary,
                colors.accent
            ]
            color = random.choice(color_choices)
            
            # Algumas partículas com glow
            glow = random.random() < 0.3
            
            particle = ParticleEffect(
                x, y, vx, vy, size, color, lifetime, lifetime, glow
            )
            
            self.particles.append(particle)
    
    def update_particles(self, dt: float):
        """Atualiza sistema de partículas"""
        for particle in self.particles[:]:
            # Movimento
            particle.x += particle.vx * dt * 60
            particle.y += particle.vy * dt * 60
            
            # Gravidade suave
            particle.vy += 0.02 * dt * 60
            
            # Reduzir lifetime
            particle.lifetime -= dt
            
            # Remover partículas mortas
            if particle.lifetime <= 0:
                self.particles.remove(particle)
            
            # Reposicionar partículas que saem da tela
            if particle.y < -10:
                particle.y = self.height + 10
                particle.x = random.randint(0, self.width)
        
        # Manter número mínimo de partículas
        if len(self.particles) < 30:
            self.spawn_particles(5)
    
    def draw_particles(self, surface: pygame.Surface):
        """Desenha as partículas com efeitos"""
        for particle in self.particles:
            # Calcular alpha baseado no lifetime
            alpha = int(255 * (particle.lifetime / particle.max_lifetime))
            
            # Desenhar glow se ativado
            if particle.glow:
                glow_size = int(particle.size * 4)
                glow_surface = modern_ui.create_glow_surface(
                    (glow_size * 2, glow_size * 2),
                    particle.color,
                    0.3 * (particle.lifetime / particle.max_lifetime)
                )
                surface.blit(
                    glow_surface,
                    (particle.x - glow_size, particle.y - glow_size)
                )
            
            # Desenhar partícula principal
            particle_surface = pygame.Surface(
                (int(particle.size * 2), int(particle.size * 2)),
                pygame.SRCALPHA
            )
            pygame.draw.circle(
                particle_surface,
                (*particle.color, alpha),
                (int(particle.size), int(particle.size)),
                int(particle.size)
            )
            surface.blit(
                particle_surface,
                (particle.x - particle.size, particle.y - particle.size)
            )
    
    def draw_animated_title(self, surface: pygame.Surface):
        """Desenha título com animações e efeitos"""
        colors = modern_ui.get_current_colors()
        
        # Animação de escala
        scale = 1.0 + 0.02 * math.sin(self.animation_time * 2)
        
        # Título principal com glow
        title_surface = self.title_font.render(self.title_text, True, colors.text_primary)
        title_rect = title_surface.get_rect(center=(self.width // 2, 150))
        
        # Efeito glow pulsante
        glow_intensity = 0.5 + 0.3 * math.sin(self.animation_time * 3)
        glow_surface = modern_ui.create_glow_surface(
            (title_rect.width + 100, title_rect.height + 50),
            colors.accent,
            glow_intensity
        )
        glow_rect = glow_surface.get_rect(center=title_rect.center)
        surface.blit(glow_surface, glow_rect)
        
        # Título com escala
        scaled_width = int(title_rect.width * scale)
        scaled_height = int(title_rect.height * scale)
        scaled_title = pygame.transform.scale(
            title_surface,
            (scaled_width, scaled_height)
        )
        scaled_rect = scaled_title.get_rect(center=title_rect.center)
        surface.blit(scaled_title, scaled_rect)
        
        # Subtítulo com fade
        subtitle_alpha = int(200 + 55 * math.sin(self.animation_time * 1.5))
        subtitle_surface = self.subtitle_font.render(
            self.subtitle_text,
            True,
            colors.text_secondary
        )
        subtitle_surface.set_alpha(subtitle_alpha)
        subtitle_rect = subtitle_surface.get_rect(center=(self.width // 2, 220))
        surface.blit(subtitle_surface, subtitle_rect)
        
        # Linha decorativa animada
        line_width = 300 + 50 * math.sin(self.animation_time * 2)
        line_rect = pygame.Rect(
            (self.width - line_width) // 2,
            250,
            line_width,
            3
        )
        gradient = modern_ui.create_gradient_surface(
            (int(line_width), 3),
            colors.primary,
            colors.secondary,
            vertical=False
        )
        surface.blit(gradient, line_rect)
    
    def draw_animated_background(self, surface: pygame.Surface):
        """Desenha background animado"""
        # Movimento do background
        offset_x = int(self.background_offset % self.width)
        offset_y = int((self.background_offset * 0.5) % self.height)
        
        # Desenhar background com parallax
        surface.blit(self.bg_surface, (-offset_x, -offset_y))
        surface.blit(self.bg_surface, (-offset_x + self.width * 2, -offset_y))
        surface.blit(self.bg_surface, (-offset_x, -offset_y + self.height * 2))
        
        # Overlay com gradiente
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        for y in range(self.height):
            alpha = int(50 * (1 - y / self.height))
            pygame.draw.line(
                overlay,
                (0, 0, 0, alpha),
                (0, y),
                (self.width, y)
            )
        surface.blit(overlay, (0, 0))
    
    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """Processa eventos do menu"""
        # Deixar o sistema de UI processar primeiro
        if modern_ui.process_event(event):
            return None
        
        # Eventos customizados
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.state == MenuState.SETTINGS:
                    self.state = MenuState.MAIN
                    return None
                else:
                    return "quit"
            elif event.key == pygame.K_F1:
                # Alternar tema
                themes = list(UITheme)
                current_index = themes.index(modern_ui.current_theme)
                next_theme = themes[(current_index + 1) % len(themes)]
                modern_ui.set_theme(next_theme)
                self.create_animated_background()
                modern_ui.create_notification(
                    f"Tema alterado para: {next_theme.value}",
                    "info"
                )
        
        return None
    
    def update(self, dt: float):
        """Atualiza o menu"""
        # Atualizar tempo de animação
        self.animation_time += dt
        
        # Atualizar background
        self.background_offset += 20 * dt
        
        # Atualizar partículas
        self.update_particles(dt)
        
        # Atualizar sistema de UI
        modern_ui.update(dt)
        
        # Animações de hover para botões
        for element in modern_ui.manager.get_sprite_group():
            if isinstance(element, UIButton):
                if element.hovered:
                    if element not in self.button_hover_states:
                        self.button_hover_states[element] = 0
                    self.button_hover_states[element] = min(
                        1.0,
                        self.button_hover_states[element] + dt * 5
                    )
                else:
                    if element in self.button_hover_states:
                        self.button_hover_states[element] = max(
                            0,
                            self.button_hover_states[element] - dt * 5
                        )
    
    def draw(self, surface: pygame.Surface):
        """Desenha o menu"""
        # Background animado
        self.draw_animated_background(surface)
        
        # Partículas de fundo
        self.draw_particles(surface)
        
        # Título animado
        self.draw_animated_title(surface)
        
        # UI moderna
        modern_ui.draw(surface)
        
        # Informações adicionais
        self.draw_info(surface)
    
    def draw_info(self, surface: pygame.Surface):
        """Desenha informações adicionais"""
        colors = modern_ui.get_current_colors()
        font = pygame.font.Font(None, 20)
        
        # Versão
        version_text = font.render("v1.0.0", True, colors.text_secondary)
        version_rect = version_text.get_rect(bottomright=(self.width - 10, self.height - 10))
        surface.blit(version_text, version_rect)
        
        # Dica de tema
        theme_text = font.render(
            f"F1: Alternar Tema ({modern_ui.current_theme.value})",
            True,
            colors.text_secondary
        )
        theme_rect = theme_text.get_rect(bottomleft=(10, self.height - 10))
        surface.blit(theme_text, theme_rect)
    
    # Callbacks
    def on_new_game(self):
        """Callback para novo jogo"""
        modern_ui.create_notification("Iniciando novo jogo...", "success")
        self.state = MenuState.LOADING
        return "new_game"
    
    def on_continue(self):
        """Callback para continuar"""
        modern_ui.create_notification("Carregando save...", "info")
        return "continue"
    
    def on_settings(self):
        """Callback para configurações"""
        self.state = MenuState.SETTINGS
        modern_ui.create_notification("Abrindo configurações", "info")
    
    def on_quit(self):
        """Callback para sair"""
        return "quit"