"""
Menu principal moderno com design system avançado
"""
import pygame
import math
import random
from typing import List, Tuple
from src.design_system import (ModernColors, ModernTypography, ModernSpacing, 
                              GlassmorphismEffect, ModernAnimations, ParticleSystem)
from src.ui.modern_button import ModernButton, FloatingActionButton
from src.config import WIDTH, HEIGHT, GAME_STATES, CREDITS

class ModernMainMenu:
    """Menu principal com design moderno e efeitos avançados"""
    
    def __init__(self):
        self.buttons: List[ModernButton] = []
        self.particle_system = ParticleSystem()
        self.floating_elements = []
        
        # Animações
        self.title_animation_time = 0
        self.background_animation_time = 0
        self.intro_animation_progress = 0
        self.is_intro_complete = False
        
        # Elementos visuais
        self.background_particles = []
        self.gradient_offset = 0
        
        self.setup_ui()
        self.setup_background_effects()
        
        # Som (placeholder para futuro)
        self.sound_enabled = True
    
    def setup_ui(self):
        """Configura interface moderna"""
        button_width = 320
        button_height = 64
        button_x = WIDTH // 2 - button_width // 2
        start_y = HEIGHT // 2 + 40
        spacing = ModernSpacing.XL + ModernSpacing.MD
        
        # Botão principal - JOGAR
        play_btn = ModernButton(
            button_x, start_y, button_width, button_height,
            "INICIAR JORNADA", ModernTypography.TEXT_LG,
            style='primary', icon='play',
            on_click=lambda: self._on_play_click()
        )
        
        # Botão Créditos
        credits_btn = ModernButton(
            button_x, start_y + spacing, button_width, button_height,
            "CRÉDITOS", ModernTypography.TEXT_LG,
            style='secondary', icon='credits',
            on_click=lambda: self._on_credits_click()
        )
        
        # Botão Sair
        quit_btn = ModernButton(
            button_x, start_y + spacing * 2, button_width, button_height,
            "SAIR", ModernTypography.TEXT_LG,
            style='danger',
            on_click=lambda: self._on_quit_click()
        )
        
        # Botão flutuante - Tela cheia
        fullscreen_fab = FloatingActionButton(
            WIDTH - 80, HEIGHT - 80, 56, 'fullscreen'
        )
        fullscreen_fab.on_click = lambda: self._on_fullscreen_click()
        
        self.buttons = [play_btn, credits_btn, quit_btn, fullscreen_fab]
        
        # Armazenar referências para callbacks
        self.result = None
    
    def setup_background_effects(self):
        """Configura efeitos de fundo"""
        # Partículas de fundo
        for _ in range(100):
            self.background_particles.append({
                'x': random.uniform(0, WIDTH),
                'y': random.uniform(0, HEIGHT),
                'size': random.uniform(1, 4),
                'speed_x': random.uniform(-20, 20),
                'speed_y': random.uniform(-30, -10),
                'alpha': random.uniform(30, 120),
                'color': random.choice([
                    ModernColors.PRIMARY_BLUE,
                    ModernColors.PRIMARY_PURPLE,
                    ModernColors.PRIMARY_CYAN,
                    ModernColors.NEUTRAL_400
                ]),
                'pulse_phase': random.uniform(0, math.pi * 2)
            })
        
        # Elementos flutuantes (formas geométricas)
        for _ in range(15):
            self.floating_elements.append({
                'x': random.uniform(0, WIDTH),
                'y': random.uniform(0, HEIGHT),
                'size': random.uniform(20, 80),
                'rotation': random.uniform(0, 360),
                'rotation_speed': random.uniform(-30, 30),
                'float_speed': random.uniform(5, 15),
                'alpha': random.uniform(10, 40),
                'shape': random.choice(['circle', 'triangle', 'square']),
                'color': random.choice([
                    ModernColors.PRIMARY_BLUE,
                    ModernColors.PRIMARY_PURPLE,
                    ModernColors.SECONDARY_GOLD
                ])
            })
    
    def handle_event(self, event: pygame.event.Event):
        """Processa eventos"""
        # Eventos dos botões
        for button in self.buttons:
            if button.handle_event(event):
                if hasattr(button, 'on_click') and button.on_click:
                    button.on_click()
        
        return self.result
    
    def update(self, dt: float):
        """Atualiza animações e lógica"""
        # Animação de introdução
        if not self.is_intro_complete:
            self.intro_animation_progress += dt * 2
            if self.intro_animation_progress >= 1.0:
                self.intro_animation_progress = 1.0
                self.is_intro_complete = True
        
        # Animações principais
        self.title_animation_time += dt
        self.background_animation_time += dt * 0.5
        self.gradient_offset += dt * 10
        
        # Atualiza botões
        for button in self.buttons:
            button.update(dt)
        
        # Atualiza partículas de fundo
        self._update_background_particles(dt)
        
        # Atualiza elementos flutuantes
        self._update_floating_elements(dt)
        
        # Sistema de partículas
        self.particle_system.update(dt)
        
        # Adiciona partículas ocasionais
        if random.random() < 0.1:  # 10% chance por frame
            self._spawn_magic_particle()
    
    def _update_background_particles(self, dt: float):
        """Atualiza partículas de fundo"""
        for particle in self.background_particles:
            # Movimento
            particle['x'] += particle['speed_x'] * dt
            particle['y'] += particle['speed_y'] * dt
            
            # Efeito pulsante
            particle['pulse_phase'] += dt * 3
            pulse_factor = (math.sin(particle['pulse_phase']) + 1) / 2
            particle['current_alpha'] = particle['alpha'] * pulse_factor
            
            # Reposiciona se sair da tela
            if particle['x'] < -10:
                particle['x'] = WIDTH + 10
            elif particle['x'] > WIDTH + 10:
                particle['x'] = -10
            
            if particle['y'] < -10:
                particle['y'] = HEIGHT + 10
            elif particle['y'] > HEIGHT + 10:
                particle['y'] = -10
    
    def _update_floating_elements(self, dt: float):
        """Atualiza elementos geométricos flutuantes"""
        for element in self.floating_elements:
            # Rotação
            element['rotation'] += element['rotation_speed'] * dt
            
            # Movimento flutuante
            element['y'] -= element['float_speed'] * dt
            
            # Reposiciona quando sai da tela
            if element['y'] < -element['size']:
                element['y'] = HEIGHT + element['size']
                element['x'] = random.uniform(0, WIDTH)
    
    def _spawn_magic_particle(self):
        """Cria partícula mágica"""
        x = random.uniform(0, WIDTH)
        y = HEIGHT + 10
        
        vel_x = random.uniform(-50, 50)
        vel_y = random.uniform(-100, -50)
        
        color = random.choice([
            ModernColors.SECONDARY_GOLD,
            ModernColors.PRIMARY_CYAN,
            ModernColors.SECONDARY_PINK
        ])
        
        self.particle_system.add_particle(x, y, vel_x, vel_y, color, 3.0, 3)
    
    def draw(self, surface: pygame.Surface):
        """Desenha menu com todos os efeitos"""
        # Fundo gradiente animado
        self._draw_animated_background(surface)
        
        # Elementos flutuantes
        self._draw_floating_elements(surface)
        
        # Partículas de fundo
        self._draw_background_particles(surface)
        
        # Título principal
        self._draw_hero_section(surface)
        
        # Sistema de partículas mágicas
        self.particle_system.draw(surface)
        
        # Botões (com animação de entrada)
        if self.is_intro_complete:
            for i, button in enumerate(self.buttons):
                # Animação escalonada de entrada
                delay = i * 0.1
                animation_progress = max(0, min(1, (self.intro_animation_progress - delay) * 3))
                
                if animation_progress > 0:
                    # Salva posição original
                    original_y = button.rect.y
                    
                    # Aplicar animação de entrada
                    offset_y = (1 - ModernAnimations.ease_out_cubic(animation_progress)) * 50
                    button.rect.y = original_y + offset_y
                    
                    # Transparência
                    alpha = int(255 * animation_progress)
                    
                    # Desenha botão
                    button.draw(surface)
                    
                    # Restaura posição
                    button.rect.y = original_y
        
        # Overlay de introdução
        if not self.is_intro_complete:
            self._draw_intro_overlay(surface)
    
    def _draw_animated_background(self, surface: pygame.Surface):
        """Desenha fundo com gradiente animado"""
        # Gradiente base
        for y in range(HEIGHT):
            progress = y / HEIGHT
            
            # Cores que mudam ao longo do tempo
            time_factor = math.sin(self.background_animation_time) * 0.1 + 0.9
            
            # Interpolação entre cores
            r = int(10 + (60 * progress * time_factor))
            g = int(10 + (40 * progress * time_factor))
            b = int(20 + (80 * progress))
            
            color = (min(255, r), min(255, g), min(255, b))
            pygame.draw.line(surface, color, (0, y), (WIDTH, y))
        
        # Overlay com efeito de movimento
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        
        # Desenha ondas sutis
        for x in range(0, WIDTH, 10):
            wave_y = math.sin((x + self.gradient_offset) * 0.01) * 20 + HEIGHT // 2
            wave_alpha = int(10 + 5 * math.sin(self.background_animation_time * 2))
            
            pygame.draw.line(overlay, (*ModernColors.PRIMARY_BLUE, wave_alpha),
                           (x, wave_y - 100), (x, wave_y + 100))
        
        surface.blit(overlay, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
    
    def _draw_floating_elements(self, surface: pygame.Surface):
        """Desenha elementos geométricos flutuantes"""
        for element in self.floating_elements:
            element_surface = pygame.Surface((element['size'] * 2, element['size'] * 2), pygame.SRCALPHA)
            
            center = (element['size'], element['size'])
            color_with_alpha = (*element['color'], int(element['alpha']))
            
            if element['shape'] == 'circle':
                pygame.draw.circle(element_surface, color_with_alpha, center, element['size'] // 2)
            
            elif element['shape'] == 'triangle':
                points = [
                    (center[0], center[1] - element['size'] // 2),
                    (center[0] - element['size'] // 2, center[1] + element['size'] // 2),
                    (center[0] + element['size'] // 2, center[1] + element['size'] // 2)
                ]
                pygame.draw.polygon(element_surface, color_with_alpha, points)
            
            elif element['shape'] == 'square':
                rect = pygame.Rect(center[0] - element['size'] // 4, center[1] - element['size'] // 4,
                                 element['size'] // 2, element['size'] // 2)
                pygame.draw.rect(element_surface, color_with_alpha, rect)
            
            # Rotaciona elemento
            rotated_surface = pygame.transform.rotate(element_surface, element['rotation'])
            
            # Desenha na posição
            rect = rotated_surface.get_rect(center=(element['x'], element['y']))
            surface.blit(rotated_surface, rect, special_flags=pygame.BLEND_ALPHA_SDL2)
    
    def _draw_background_particles(self, surface: pygame.Surface):
        """Desenha partículas de fundo"""
        for particle in self.background_particles:
            if particle.get('current_alpha', 0) > 0:
                particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
                
                color_with_alpha = (*particle['color'], int(particle['current_alpha']))
                pygame.draw.circle(particle_surface, color_with_alpha,
                                 (particle['size'], particle['size']), particle['size'])
                
                surface.blit(particle_surface, 
                           (particle['x'] - particle['size'], particle['y'] - particle['size']),
                           special_flags=pygame.BLEND_ALPHA_SDL2)
    
    def _draw_hero_section(self, surface: pygame.Surface):
        """Desenha seção principal com título"""
        # Efeito de flutuação
        float_offset = math.sin(self.title_animation_time * 2) * 8
        
        # Painel glassmorphism para o título
        panel_width = 800
        panel_height = 220
        panel_x = WIDTH // 2 - panel_width // 2
        panel_y = 80 + float_offset
        
        # Cria painel com glassmorphism
        panel_surface = GlassmorphismEffect.create_glass_surface(
            panel_width, panel_height, ModernColors.GLASS_WHITE
        )
        
        # Adiciona gradiente sutil
        gradient_surface = GlassmorphismEffect.create_gradient_surface(
            panel_width, panel_height, 
            [ModernColors.PRIMARY_PURPLE, ModernColors.PRIMARY_BLUE],
            'horizontal'
        )
        gradient_surface.set_alpha(20)
        panel_surface.blit(gradient_surface, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)
        
        surface.blit(panel_surface, (panel_x, panel_y), special_flags=pygame.BLEND_ALPHA_SDL2)
        
        # Título principal
        title_font = pygame.font.Font(None, ModernTypography.DISPLAY_LG)
        title_text = title_font.render("PROJETO ÍCARO", True, ModernColors.NEUTRAL_50)
        
        # Sombra do título
        shadow_text = title_font.render("PROJETO ÍCARO", True, (0, 0, 0, 100))
        shadow_rect = shadow_text.get_rect(center=(WIDTH // 2 + 2, panel_y + 60 + 2))
        surface.blit(shadow_text, shadow_rect)
        
        # Título principal
        title_rect = title_text.get_rect(center=(WIDTH // 2, panel_y + 60))
        surface.blit(title_text, title_rect)
        
        # Subtítulo
        subtitle_font = pygame.font.Font(None, ModernTypography.TEXT_XL)
        subtitle_text = subtitle_font.render("Uma Jornada Mitológica Épica", True, ModernColors.NEUTRAL_300)
        subtitle_rect = subtitle_text.get_rect(center=(WIDTH // 2, panel_y + 110))
        surface.blit(subtitle_text, subtitle_rect)
        
        # Linha decorativa
        line_y = panel_y + 140
        line_start = WIDTH // 2 - 150
        line_end = WIDTH // 2 + 150
        
        # Gradiente na linha
        for x in range(line_start, line_end):
            progress = (x - line_start) / (line_end - line_start)
            alpha = int(255 * (1 - abs(progress - 0.5) * 2))
            color = (*ModernColors.SECONDARY_GOLD, alpha)
            
            line_surface = pygame.Surface((1, 3), pygame.SRCALPHA)
            line_surface.fill(color)
            surface.blit(line_surface, (x, line_y))
        
        # Versão info
        version_font = pygame.font.Font(None, ModernTypography.TEXT_SM)
        version_text = version_font.render("v2.0 Modern Edition", True, ModernColors.NEUTRAL_400)
        version_rect = version_text.get_rect(center=(WIDTH // 2, panel_y + 180))
        surface.blit(version_text, version_rect)
    
    def _draw_intro_overlay(self, surface: pygame.Surface):
        """Desenha overlay de introdução"""
        alpha = int(255 * (1 - self.intro_animation_progress))
        if alpha > 0:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.fill(ModernColors.PRIMARY_DARK)
            overlay.set_alpha(alpha)
            surface.blit(overlay, (0, 0))
    
    # Callbacks dos botões
    def _on_play_click(self):
        """Callback do botão jogar"""
        self.result = GAME_STATES['PLAYING']
    
    def _on_credits_click(self):
        """Callback do botão créditos"""
        self.result = GAME_STATES['CREDITS']
    
    def _on_quit_click(self):
        """Callback do botão sair"""
        self.result = 'QUIT'
    
    def _on_fullscreen_click(self):
        """Callback do botão tela cheia"""
        self.result = 'FULLSCREEN'