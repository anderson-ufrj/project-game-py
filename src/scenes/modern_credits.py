"""
Tela de créditos moderna com design avançado
"""
import pygame
import math
from typing import List, Tuple
from src.design_system import (ModernColors, ModernTypography, ModernSpacing, 
                              GlassmorphismEffect, ModernAnimations)
from src.ui.modern_button import ModernButton
from src.config import WIDTH, HEIGHT, GAME_STATES, CREDITS

class ModernCreditsScreen:
    """Tela de créditos com design moderno e animações"""
    
    def __init__(self):
        self.scroll_y = HEIGHT
        self.target_scroll_y = HEIGHT
        self.credits_content = []
        self.particles = []
        self.animation_time = 0
        self.is_auto_scrolling = True
        
        # Botão de voltar
        self.back_button = ModernButton(
            50, HEIGHT - 100, 200, 50,
            "← VOLTAR", ModernTypography.TEXT_MD,
            style='secondary',
            on_click=lambda: self._on_back_click()
        )
        
        self.result = None
        self.setup_credits_content()
        self.setup_particles()
    
    def setup_credits_content(self):
        """Prepara o conteúdo dos créditos com formatação moderna"""
        self.credits_content = [
            # Header
            {
                'type': 'header',
                'text': 'PROJETO ÍCARO',
                'font_size': ModernTypography.DISPLAY_MD,
                'color': ModernColors.SECONDARY_GOLD,
                'spacing': 80
            },
            {
                'type': 'line',
                'color': ModernColors.SECONDARY_GOLD,
                'spacing': 40
            },
            {
                'type': 'subtitle',
                'text': 'Uma Jornada Mitológica Épica',
                'font_size': ModernTypography.TEXT_XL,
                'color': ModernColors.NEUTRAL_300,
                'spacing': 60
            },
            
            # Desenvolvedor
            {
                'type': 'section_title',
                'text': 'DESENVOLVIDO POR',
                'font_size': ModernTypography.TEXT_LG,
                'color': ModernColors.PRIMARY_BLUE,
                'spacing': 50
            },
            {
                'type': 'highlight',
                'text': CREDITS['DEVELOPER'],
                'font_size': ModernTypography.DISPLAY_SM,
                'color': ModernColors.NEUTRAL_50,
                'spacing': 30
            },
            {
                'type': 'info',
                'text': f"Estudante de {CREDITS['COURSE']}",
                'font_size': ModernTypography.TEXT_MD,
                'color': ModernColors.NEUTRAL_400,
                'spacing': 20
            },
            {
                'type': 'info',
                'text': CREDITS['INSTITUTION'],
                'font_size': ModernTypography.TEXT_MD,
                'color': ModernColors.NEUTRAL_400,
                'spacing': 50
            },
            
            # Projeto acadêmico
            {
                'type': 'section_title',
                'text': 'PROJETO ACADÊMICO',
                'font_size': ModernTypography.TEXT_LG,
                'color': ModernColors.PRIMARY_PURPLE,
                'spacing': 30
            },
            {
                'type': 'highlight',
                'text': CREDITS['SUBJECT'],
                'font_size': ModernTypography.TEXT_XL,
                'color': ModernColors.SECONDARY_GOLD,
                'spacing': 60
            },
            
            # Contatos
            {
                'type': 'section_title',
                'text': 'CONTATOS',
                'font_size': ModernTypography.TEXT_LG,
                'color': ModernColors.PRIMARY_CYAN,
                'spacing': 30
            },
            {
                'type': 'link',
                'text': f"GitHub: {CREDITS['GITHUB']}",
                'font_size': ModernTypography.TEXT_MD,
                'color': ModernColors.PRIMARY_BLUE,
                'spacing': 25
            },
            {
                'type': 'link',
                'text': f"LinkedIn: {CREDITS['LINKEDIN']}",
                'font_size': ModernTypography.TEXT_MD,
                'color': ModernColors.PRIMARY_BLUE,
                'spacing': 50
            },
            
            # Tecnologias
            {
                'type': 'section_title',
                'text': 'TECNOLOGIAS UTILIZADAS',
                'font_size': ModernTypography.TEXT_LG,
                'color': ModernColors.SECONDARY_GREEN,
                'spacing': 30
            },
            {
                'type': 'tech',
                'text': 'Python 3.x',
                'description': 'Linguagem de programação principal',
                'spacing': 25
            },
            {
                'type': 'tech',
                'text': 'Pygame',
                'description': 'Engine de desenvolvimento de jogos',
                'spacing': 25
            },
            {
                'type': 'tech',
                'text': 'Pygame Zero',
                'description': 'Framework simplificado para jogos',
                'spacing': 25
            },
            {
                'type': 'tech',
                'text': 'Modern Design System',
                'description': 'Interface inspirada em Material Design 3',
                'spacing': 60
            },
            
            # Arte e Assets
            {
                'type': 'section_title',
                'text': 'ARTE E RECURSOS VISUAIS',
                'font_size': ModernTypography.TEXT_LG,
                'color': ModernColors.SECONDARY_PINK,
                'spacing': 30
            },
            {
                'type': 'info',
                'text': 'Sprites customizados para temática mitológica',
                'font_size': ModernTypography.TEXT_MD,
                'color': ModernColors.NEUTRAL_400,
                'spacing': 25
            },
            {
                'type': 'info',
                'text': 'Sistema de partículas procedural',
                'font_size': ModernTypography.TEXT_MD,
                'color': ModernColors.NEUTRAL_400,
                'spacing': 25
            },
            {
                'type': 'info',
                'text': 'Efeitos glassmorphism modernos',
                'font_size': ModernTypography.TEXT_MD,
                'color': ModernColors.NEUTRAL_400,
                'spacing': 80
            },
            
            # Agradecimentos
            {
                'type': 'section_title',
                'text': 'AGRADECIMENTOS ESPECIAIS',
                'font_size': ModernTypography.TEXT_LG,
                'color': ModernColors.SECONDARY_GOLD,
                'spacing': 30
            },
            {
                'type': 'info',
                'text': 'Professores do IFSULDEMINAS',
                'font_size': ModernTypography.TEXT_MD,
                'color': ModernColors.NEUTRAL_400,
                'spacing': 25
            },
            {
                'type': 'info',
                'text': 'Comunidade Python e Pygame',
                'font_size': ModernTypography.TEXT_MD,
                'color': ModernColors.NEUTRAL_400,
                'spacing': 25
            },
            {
                'type': 'info',
                'text': 'Desenvolvedores indie brasileiros',
                'font_size': ModernTypography.TEXT_MD,
                'color': ModernColors.NEUTRAL_400,
                'spacing': 100
            },
            
            # Final
            {
                'type': 'header',
                'text': 'OBRIGADO POR JOGAR!',
                'font_size': ModernTypography.DISPLAY_SM,
                'color': ModernColors.SECONDARY_GOLD,
                'spacing': 60
            },
            {
                'type': 'subtitle',
                'text': 'Que sua jornada seja épica como a de Ícaro',
                'font_size': ModernTypography.TEXT_LG,
                'color': ModernColors.NEUTRAL_300,
                'spacing': 100
            },
            {
                'type': 'info',
                'text': 'Pressione ESC ou clique em VOLTAR para retornar',
                'font_size': ModernTypography.TEXT_SM,
                'color': ModernColors.NEUTRAL_500,
                'spacing': 200
            }
        ]
    
    def setup_particles(self):
        """Configura partículas de fundo"""
        import random
        for _ in range(30):
            self.particles.append({
                'x': random.uniform(0, WIDTH),
                'y': random.uniform(0, HEIGHT * 3),  # Espalha por toda área de scroll
                'size': random.uniform(2, 6),
                'speed': random.uniform(10, 30),
                'color': random.choice([
                    ModernColors.SECONDARY_GOLD,
                    ModernColors.PRIMARY_BLUE,
                    ModernColors.PRIMARY_PURPLE,
                    ModernColors.PRIMARY_CYAN
                ]),
                'alpha': random.uniform(30, 100),
                'pulse_phase': random.uniform(0, math.pi * 2)
            })
    
    def handle_event(self, event: pygame.event.Event):
        """Processa eventos"""
        # Botão de voltar
        if self.back_button.handle_event(event):
            return self.result
        
        # Teclado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.result = GAME_STATES['MENU']
                return self.result
            elif event.key == pygame.K_SPACE:
                self.is_auto_scrolling = not self.is_auto_scrolling
        
        # Mouse scroll
        elif event.type == pygame.MOUSEWHEEL:
            self.is_auto_scrolling = False
            self.target_scroll_y += event.y * 50
            
            # Limites do scroll
            max_scroll = sum(item.get('spacing', 40) for item in self.credits_content) + HEIGHT
            self.target_scroll_y = max(-max_scroll, min(HEIGHT, self.target_scroll_y))
        
        return None
    
    def update(self, dt: float):
        """Atualiza animações"""
        self.animation_time += dt
        
        # Auto scroll
        if self.is_auto_scrolling:
            self.target_scroll_y -= 30 * dt  # Velocidade do scroll
            
            # Reinicia quando termina
            total_height = sum(item.get('spacing', 40) for item in self.credits_content)
            if self.target_scroll_y < -total_height - HEIGHT:
                self.target_scroll_y = HEIGHT
        
        # Suaviza movimento do scroll
        self.scroll_y += (self.target_scroll_y - self.scroll_y) * 8 * dt
        
        # Atualiza botão
        self.back_button.update(dt)
        
        # Atualiza partículas
        for particle in self.particles:
            particle['y'] -= particle['speed'] * dt
            particle['pulse_phase'] += dt * 3
            
            # Reposiciona se sair da área
            if particle['y'] < -particle['size']:
                particle['y'] = HEIGHT + particle['size']
                particle['x'] = random.uniform(0, WIDTH)
    
    def draw(self, surface: pygame.Surface):
        """Desenha tela de créditos"""
        # Fundo escuro com gradiente
        self._draw_background(surface)
        
        # Partículas
        self._draw_particles(surface)
        
        # Conteúdo dos créditos
        self._draw_credits_content(surface)
        
        # Overlay gradiente nas bordas
        self._draw_edge_gradients(surface)
        
        # Botão de voltar
        self.back_button.draw(surface)
        
        # Indicador de scroll
        self._draw_scroll_indicator(surface)
    
    def _draw_background(self, surface: pygame.Surface):
        """Desenha fundo com gradiente animado"""
        # Gradiente base
        for y in range(HEIGHT):
            progress = y / HEIGHT
            time_factor = math.sin(self.animation_time * 0.5) * 0.1 + 0.9
            
            r = int(5 + (15 * progress * time_factor))
            g = int(5 + (20 * progress * time_factor))
            b = int(15 + (35 * progress))
            
            color = (r, g, b)
            pygame.draw.line(surface, color, (0, y), (WIDTH, y))
    
    def _draw_particles(self, surface: pygame.Surface):
        """Desenha partículas de fundo"""
        for particle in self.particles:
            # Posição relativa ao scroll
            display_y = particle['y'] + self.scroll_y
            
            # Só desenha se estiver visível
            if -particle['size'] <= display_y <= HEIGHT + particle['size']:
                # Efeito pulsante
                pulse_factor = (math.sin(particle['pulse_phase']) + 1) / 2
                current_alpha = int(particle['alpha'] * pulse_factor)
                
                if current_alpha > 0:
                    particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
                    color_with_alpha = (*particle['color'], current_alpha)
                    
                    pygame.draw.circle(particle_surface, color_with_alpha,
                                     (particle['size'], particle['size']), particle['size'])
                    
                    surface.blit(particle_surface, 
                               (particle['x'] - particle['size'], display_y - particle['size']),
                               special_flags=pygame.BLEND_ALPHA_SDL2)
    
    def _draw_credits_content(self, surface: pygame.Surface):
        """Desenha conteúdo dos créditos"""
        current_y = self.scroll_y
        
        for item in self.credits_content:
            # Só processa se estiver próximo da área visível
            if current_y > HEIGHT + 100 or current_y < -200:
                current_y += item.get('spacing', 40)
                continue
            
            item_type = item['type']
            
            if item_type == 'header':
                self._draw_header(surface, item, current_y)
            
            elif item_type == 'subtitle':
                self._draw_subtitle(surface, item, current_y)
            
            elif item_type == 'section_title':
                self._draw_section_title(surface, item, current_y)
            
            elif item_type == 'highlight':
                self._draw_highlight(surface, item, current_y)
            
            elif item_type == 'info':
                self._draw_info(surface, item, current_y)
            
            elif item_type == 'link':
                self._draw_link(surface, item, current_y)
            
            elif item_type == 'tech':
                self._draw_tech_item(surface, item, current_y)
            
            elif item_type == 'line':
                self._draw_decorative_line(surface, item, current_y)
            
            current_y += item.get('spacing', 40)
    
    def _draw_header(self, surface: pygame.Surface, item: dict, y: float):
        """Desenha cabeçalho"""
        if not (-100 <= y <= HEIGHT + 100):
            return
            
        font = pygame.font.Font(None, item['font_size'])
        
        # Efeito brilhante
        glow_surface = pygame.Surface((WIDTH, 100), pygame.SRCALPHA)
        
        # Múltiplas camadas para glow
        for i in range(5):
            glow_text = font.render(item['text'], True, (*item['color'], 20 - i * 3))
            glow_rect = glow_text.get_rect(center=(WIDTH // 2 + i, 50 + i))
            glow_surface.blit(glow_text, glow_rect)
        
        surface.blit(glow_surface, (0, y - 25), special_flags=pygame.BLEND_ALPHA_SDL2)
        
        # Texto principal
        text_surface = font.render(item['text'], True, item['color'])
        text_rect = text_surface.get_rect(center=(WIDTH // 2, y))
        surface.blit(text_surface, text_rect)
    
    def _draw_subtitle(self, surface: pygame.Surface, item: dict, y: float):
        """Desenha subtítulo"""
        if not (-50 <= y <= HEIGHT + 50):
            return
            
        font = pygame.font.Font(None, item['font_size'])
        text_surface = font.render(item['text'], True, item['color'])
        text_rect = text_surface.get_rect(center=(WIDTH // 2, y))
        surface.blit(text_surface, text_rect)
    
    def _draw_section_title(self, surface: pygame.Surface, item: dict, y: float):
        """Desenha título de seção"""
        if not (-50 <= y <= HEIGHT + 50):
            return
            
        # Painel de fundo
        panel_width = 400
        panel_height = 40
        panel_rect = pygame.Rect(WIDTH // 2 - panel_width // 2, y - 15, panel_width, panel_height)
        
        panel_surface = GlassmorphismEffect.create_glass_surface(
            panel_width, panel_height, (*item['color'], 30)
        )
        surface.blit(panel_surface, panel_rect.topleft, special_flags=pygame.BLEND_ALPHA_SDL2)
        
        # Texto
        font = pygame.font.Font(None, item['font_size'])
        text_surface = font.render(item['text'], True, item['color'])
        text_rect = text_surface.get_rect(center=(WIDTH // 2, y))
        surface.blit(text_surface, text_rect)
    
    def _draw_highlight(self, surface: pygame.Surface, item: dict, y: float):
        """Desenha texto destacado"""
        if not (-50 <= y <= HEIGHT + 50):
            return
            
        font = pygame.font.Font(None, item['font_size'])
        
        # Sombra
        shadow_text = font.render(item['text'], True, (0, 0, 0, 150))
        shadow_rect = shadow_text.get_rect(center=(WIDTH // 2 + 2, y + 2))
        surface.blit(shadow_text, shadow_rect)
        
        # Texto principal
        text_surface = font.render(item['text'], True, item['color'])
        text_rect = text_surface.get_rect(center=(WIDTH // 2, y))
        surface.blit(text_surface, text_rect)
    
    def _draw_info(self, surface: pygame.Surface, item: dict, y: float):
        """Desenha texto informativo"""
        if not (-30 <= y <= HEIGHT + 30):
            return
            
        font = pygame.font.Font(None, item['font_size'])
        text_surface = font.render(item['text'], True, item['color'])
        text_rect = text_surface.get_rect(center=(WIDTH // 2, y))
        surface.blit(text_surface, text_rect)
    
    def _draw_link(self, surface: pygame.Surface, item: dict, y: float):
        """Desenha link"""
        if not (-30 <= y <= HEIGHT + 30):
            return
            
        font = pygame.font.Font(None, item['font_size'])
        
        # Sublinhado
        text_width = font.size(item['text'])[0]
        line_start = WIDTH // 2 - text_width // 2
        line_end = WIDTH // 2 + text_width // 2
        pygame.draw.line(surface, item['color'], (line_start, y + 15), (line_end, y + 15), 1)
        
        # Texto
        text_surface = font.render(item['text'], True, item['color'])
        text_rect = text_surface.get_rect(center=(WIDTH // 2, y))
        surface.blit(text_surface, text_rect)
    
    def _draw_tech_item(self, surface: pygame.Surface, item: dict, y: float):
        """Desenha item de tecnologia"""
        if not (-40 <= y <= HEIGHT + 40):
            return
            
        # Título da tecnologia
        title_font = pygame.font.Font(None, ModernTypography.TEXT_LG)
        title_surface = title_font.render(item['text'], True, ModernColors.SECONDARY_CYAN)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, y - 10))
        surface.blit(title_surface, title_rect)
        
        # Descrição
        desc_font = pygame.font.Font(None, ModernTypography.TEXT_SM)
        desc_surface = desc_font.render(item['description'], True, ModernColors.NEUTRAL_500)
        desc_rect = desc_surface.get_rect(center=(WIDTH // 2, y + 10))
        surface.blit(desc_surface, desc_rect)
    
    def _draw_decorative_line(self, surface: pygame.Surface, item: dict, y: float):
        """Desenha linha decorativa"""
        if not (-10 <= y <= HEIGHT + 10):
            return
            
        line_width = 300
        start_x = WIDTH // 2 - line_width // 2
        end_x = WIDTH // 2 + line_width // 2
        
        # Gradiente na linha
        for x in range(start_x, end_x):
            progress = (x - start_x) / line_width
            alpha = int(255 * (1 - abs(progress - 0.5) * 2))
            color = (*item['color'], alpha)
            
            line_surface = pygame.Surface((1, 2), pygame.SRCALPHA)
            line_surface.fill(color)
            surface.blit(line_surface, (x, y))
    
    def _draw_edge_gradients(self, surface: pygame.Surface):
        """Desenha gradientes nas bordas para fade"""
        gradient_height = 100
        
        # Gradiente superior
        for y in range(gradient_height):
            alpha = int(255 * (1 - y / gradient_height))
            line_surface = pygame.Surface((WIDTH, 1))
            line_surface.fill(ModernColors.PRIMARY_DARK)
            line_surface.set_alpha(alpha)
            surface.blit(line_surface, (0, y))
        
        # Gradiente inferior
        for y in range(gradient_height):
            alpha = int(255 * (y / gradient_height))
            line_surface = pygame.Surface((WIDTH, 1))
            line_surface.fill(ModernColors.PRIMARY_DARK)
            line_surface.set_alpha(alpha)
            surface.blit(line_surface, (0, HEIGHT - gradient_height + y))
    
    def _draw_scroll_indicator(self, surface: pygame.Surface):
        """Desenha indicador de posição do scroll"""
        # Barra de scroll
        total_height = sum(item.get('spacing', 40) for item in self.credits_content)
        if total_height > HEIGHT:
            scroll_bar_height = HEIGHT * 0.8
            scroll_bar_width = 4
            scroll_bar_x = WIDTH - 20
            scroll_bar_y = HEIGHT * 0.1
            
            # Fundo da barra
            pygame.draw.rect(surface, ModernColors.NEUTRAL_800,
                           (scroll_bar_x, scroll_bar_y, scroll_bar_width, scroll_bar_height))
            
            # Indicador atual
            progress = max(0, min(1, -self.scroll_y / total_height))
            indicator_height = max(20, scroll_bar_height * (HEIGHT / total_height))
            indicator_y = scroll_bar_y + (scroll_bar_height - indicator_height) * progress
            
            pygame.draw.rect(surface, ModernColors.PRIMARY_BLUE,
                           (scroll_bar_x, indicator_y, scroll_bar_width, indicator_height),
                           border_radius=2)
    
    def _on_back_click(self):
        """Callback do botão voltar"""
        self.result = GAME_STATES['MENU']