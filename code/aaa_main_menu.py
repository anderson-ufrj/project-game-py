import pygame
import math
import random
import time
from settings import *
from font_manager import font_manager
from graphics_screen import GraphicsScreen
from tutorial_system import tutorial_system

class AAA_Particle:
    """Partícula cinematográfica de alta qualidade"""
    def __init__(self, x, y, particle_type="magic"):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.particle_type = particle_type
        
        if particle_type == "magic":
            self.vx = random.uniform(-0.3, 0.3)
            self.vy = random.uniform(-0.8, -0.2)
            self.size = random.uniform(2, 4)
            self.life = random.uniform(120, 200)
            self.color = random.choice([
                (138, 43, 226),   # Roxo mágico
                (75, 0, 130),     # Índigo
                (147, 0, 211),    # Violeta
                (216, 191, 216),  # Thistle
            ])
        elif particle_type == "ember":
            self.vx = random.uniform(-0.2, 0.2)
            self.vy = random.uniform(-0.5, -0.1)
            self.size = random.uniform(1, 2)
            self.life = random.uniform(80, 150)
            self.color = random.choice([
                (255, 140, 0),    # Laranja
                (255, 69, 0),     # Vermelho laranja
                (255, 215, 0),    # Dourado
            ])
        
        self.max_life = self.life
        self.oscillation = random.uniform(0, math.pi * 2)
    
    def update(self):
        # Movimento flutuante senoidal
        self.x += self.vx + math.sin(pygame.time.get_ticks() * 0.002 + self.oscillation) * 0.1
        self.y += self.vy
        self.life -= 1
        
        # Resetar quando sair da tela
        if self.y < -20:
            self.y = HEIGTH + 20
            self.x = random.randint(0, WIDTH)
            self.life = self.max_life
        
        return self.life > 0
    
    def draw(self, surface):
        if self.life > 0:
            alpha = int(255 * (self.life / self.max_life))
            color = (*self.color, alpha)
            
            # Criar surface com alpha
            particle_surface = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
            
            # Desenhar core brilhante
            pygame.draw.circle(particle_surface, color, 
                             (int(self.size), int(self.size)), int(self.size))
            
            # Desenhar glow externo
            if alpha > 50:
                glow_size = int(self.size * 1.5)
                glow_color = (*self.color, int(alpha * 0.3))
                pygame.draw.circle(particle_surface, glow_color,
                                 (int(self.size), int(self.size)), glow_size)
            
            surface.blit(particle_surface, (int(self.x - self.size), int(self.y - self.size)))

class AAA_MenuButton:
    """Botão de menu com qualidade AAA"""
    
    def __init__(self, x, y, width, height, text, action, icon=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.icon = icon
        
        # Estados de animação
        self.hover = False
        self.click_animation = 0.0
        self.hover_animation = 0.0
        self.glow_intensity = 0.0
        self.particle_spawn_timer = 0
        
        # Cores temáticas
        self.colors = {
            'background': (20, 25, 35, 180),
            'border': (138, 43, 226, 200),
            'hover': (147, 0, 211, 220),
            'text': (255, 255, 255),
            'glow': (138, 43, 226),
            'accent': (216, 191, 216)
        }
        
        # Partículas do botão
        self.particles = []
        
        # Fontes
        self.font = font_manager.get('button')
        self.icon_font = font_manager.get('title')
    
    def update(self, mouse_pos, mouse_click):
        """Atualiza animações e estados do botão"""
        was_hover = self.hover
        self.hover = self.rect.collidepoint(mouse_pos)
        
        # Animações de hover
        if self.hover:
            self.hover_animation = min(1.0, self.hover_animation + 0.05)
            self.glow_intensity = 0.7 + 0.3 * math.sin(time.time() * 4)
            
            # Spawn partículas no hover
            self.particle_spawn_timer += 1
            if self.particle_spawn_timer > 8:
                self.spawn_hover_particle()
                self.particle_spawn_timer = 0
        else:
            self.hover_animation = max(0.0, self.hover_animation - 0.03)
            self.glow_intensity = 0.0
        
        # Animação de clique
        if self.hover and mouse_click:
            self.click_animation = 1.0
            self.spawn_click_effect()
            return self.action
        
        # Decay da animação de clique
        if self.click_animation > 0:
            self.click_animation = max(0, self.click_animation - 0.1)
        
        # Atualizar partículas
        self.particles = [p for p in self.particles if p.update()]
        
        return None
    
    def spawn_hover_particle(self):
        """Cria partícula no hover"""
        if len(self.particles) < 5:
            x = random.randint(self.rect.left, self.rect.right)
            y = random.randint(self.rect.top, self.rect.bottom)
            particle = AAA_Particle(x, y, "magic")
            particle.size *= 0.5  # Partículas menores
            particle.life *= 0.3  # Vida mais curta
            self.particles.append(particle)
    
    def spawn_click_effect(self):
        """Efeito visual de clique"""
        for _ in range(3):
            x = random.randint(self.rect.left, self.rect.right)
            y = random.randint(self.rect.top, self.rect.bottom)
            particle = AAA_Particle(x, y, "ember")
            self.particles.append(particle)
    
    def draw(self, surface):
        """Desenha o botão com efeitos AAA"""
        # Calcular efeitos baseados na animação
        animation_offset = int(self.click_animation * 2)
        glow_size = int(self.hover_animation * 8)
        
        # Posição ajustada para click
        draw_rect = self.rect.copy()
        draw_rect.x += animation_offset
        draw_rect.y += animation_offset
        
        # Desenhar glow externo
        if self.hover_animation > 0:
            glow_surface = pygame.Surface((draw_rect.width + glow_size * 2, 
                                         draw_rect.height + glow_size * 2), pygame.SRCALPHA)
            
            glow_color = (*self.colors['glow'], int(self.glow_intensity * 100))
            
            # Múltiplas camadas de glow
            for i in range(3, 0, -1):
                size_mult = i * 0.7
                alpha_mult = (4 - i) * 0.4
                glow_rect = pygame.Rect(glow_size * size_mult, glow_size * size_mult,
                                      draw_rect.width - glow_size * size_mult * 2,
                                      draw_rect.height - glow_size * size_mult * 2)
                
                if glow_rect.width > 0 and glow_rect.height > 0:
                    current_color = (*self.colors['glow'], int(self.glow_intensity * 100 * alpha_mult))
                    pygame.draw.rect(glow_surface, current_color, glow_rect, border_radius=15)
            
            surface.blit(glow_surface, (draw_rect.x - glow_size, draw_rect.y - glow_size))
        
        # Fundo do botão com gradiente
        button_surface = pygame.Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
        
        # Cor de fundo baseada no estado
        if self.hover:
            bg_color = self.colors['hover']
        else:
            bg_color = self.colors['background']
        
        pygame.draw.rect(button_surface, bg_color, (0, 0, draw_rect.width, draw_rect.height), 
                        border_radius=12)
        
        # Borda brilhante
        border_base = self.colors['border'][:3]  # RGB only
        border_alpha = max(0, min(255, int(self.colors['border'][3] * (1 + self.hover_animation * 0.5))))
        border_color = (*border_base, border_alpha)
        
        # Create border surface with alpha
        border_surface = pygame.Surface((draw_rect.width, draw_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(border_surface, border_color, (0, 0, draw_rect.width, draw_rect.height), 
                        width=2, border_radius=12)
        button_surface.blit(border_surface, (0, 0))
        
        # Gradiente sutil no topo
        gradient_height = draw_rect.height // 3
        for y in range(gradient_height):
            alpha = int(40 * (1 - y / gradient_height) * (1 + self.hover_animation))
            color = (255, 255, 255, alpha)
            pygame.draw.line(button_surface, color, (8, y + 5), (draw_rect.width - 8, y + 5))
        
        surface.blit(button_surface, draw_rect)
        
        # Desenhar ícone e texto
        if self.icon:
            icon_surface = self.icon_font.render(self.icon, True, self.colors['accent'])
            icon_rect = icon_surface.get_rect(center=(draw_rect.x + 40, draw_rect.centery))
            surface.blit(icon_surface, icon_rect)
            text_x = draw_rect.x + 80
        else:
            text_x = draw_rect.centerx
        
        # Texto principal com sombra
        shadow_surface = self.font.render(self.text, True, (0, 0, 0))
        text_surface = self.font.render(self.text, True, self.colors['text'])
        
        text_rect = text_surface.get_rect(center=(text_x, draw_rect.centery))
        shadow_rect = text_rect.copy()
        shadow_rect.x += 1
        shadow_rect.y += 1
        
        surface.blit(shadow_surface, shadow_rect)
        surface.blit(text_surface, text_rect)
        
        # Desenhar partículas do botão
        for particle in self.particles:
            particle.draw(surface)

class AAA_AdvancedMainMenu:
    """Menu principal com qualidade AAA (EA Games, Blizzard, etc.)"""
    
    def __init__(self, screen, fonts):
        self.screen = screen
        self.fonts = fonts
        
        # Carregar background
        try:
            self.background = pygame.image.load('../graphics/ui/home page.jpg').convert()
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGTH))
        except:
            print("Erro ao carregar background - usando gradiente")
            self.background = self.create_epic_background()
        
        # Sistema de partículas cinematográfico
        self.particles = []
        self.create_particle_system()
        
        # Fontes
        self.title_font = font_manager.get('title')
        self.subtitle_font = font_manager.get('subtitle')
        
        # Animações cinematográficas
        self.time = 0
        self.title_pulse = 0
        self.crystal_glow = 0
        
        # Criar botões AAA
        self.create_aaa_buttons()
        
        # Estado do menu
        self.current_section = "main"
        
        # Configurações gráficas
        self.graphics_screen = GraphicsScreen()
    
    def create_epic_background(self):
        """Cria fundo épico se não conseguir carregar imagem"""
        surface = pygame.Surface((WIDTH, HEIGTH))
        
        # Gradiente épico
        for y in range(HEIGTH):
            progress = y / HEIGTH
            r = int(10 + 20 * progress)
            g = int(5 + 15 * progress)
            b = int(30 + 40 * progress)
            pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))
        
        return surface
    
    def create_particle_system(self):
        """Sistema de partículas cinematográfico"""
        # Partículas mágicas ambiente
        for _ in range(40):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGTH)
            self.particles.append(AAA_Particle(x, y, "magic"))
        
        # Partículas ember menores
        for _ in range(20):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGTH)
            self.particles.append(AAA_Particle(x, y, "ember"))
    
    def create_aaa_buttons(self):
        """Cria botões com design AAA"""
        # Posicionamento estratégico que não cobre o cristal
        button_width = 280
        button_height = 45
        button_spacing = 15
        
        # Posicionar à direita para não cobrir o cristal central
        start_x = WIDTH - button_width - 80
        start_y = 320
        
        self.buttons = [
            AAA_MenuButton(start_x, start_y, button_width, button_height, 
                          "INICIAR JOGO", "start_game", "▶"),
            AAA_MenuButton(start_x, start_y + (button_height + button_spacing), button_width, button_height, 
                          "TUTORIAL", "show_tutorial", "🎓"),
            AAA_MenuButton(start_x, start_y + (button_height + button_spacing) * 2, button_width, button_height, 
                          "GRÁFICOS", "show_graphics", "🖥️"),
            AAA_MenuButton(start_x, start_y + (button_height + button_spacing) * 3, button_width, button_height, 
                          "ESTATÍSTICAS", "show_stats", "📊"),
            AAA_MenuButton(start_x, start_y + (button_height + button_spacing) * 4, button_width, button_height, 
                          "CRÉDITOS", "show_credits", "👥"),
            AAA_MenuButton(start_x, start_y + (button_height + button_spacing) * 5, button_width, button_height, 
                          "SAIR", "quit_game", "✕")
        ]
    
    def update_particles(self):
        """Atualiza sistema de partículas"""
        self.particles = [p for p in self.particles if p.update()]
        
        # Manter número constante de partículas
        while len([p for p in self.particles if p.particle_type == "magic"]) < 40:
            x = random.randint(0, WIDTH)
            y = HEIGTH + 20
            self.particles.append(AAA_Particle(x, y, "magic"))
        
        while len([p for p in self.particles if p.particle_type == "ember"]) < 20:
            x = random.randint(0, WIDTH)
            y = HEIGTH + 20
            self.particles.append(AAA_Particle(x, y, "ember"))
    
    def update_animations(self):
        """Atualiza animações cinematográficas"""
        self.time = pygame.time.get_ticks()
        self.title_pulse = 0.5 + 0.5 * math.sin(self.time * 0.002)
        self.crystal_glow = 0.6 + 0.4 * math.sin(self.time * 0.003)
    
    def draw_epic_title(self):
        """Desenha título épico com efeitos"""
        # Título principal
        title_text = "CORRIDA PELA RELÍQUIA"
        
        # Múltiplas camadas de sombra para profundidade
        for offset in [(3, 3), (2, 2), (1, 1)]:
            shadow_color = (0, 0, 0, 100 - offset[0] * 20)
            shadow_surface = self.title_font.render(title_text, True, shadow_color[:3])
            shadow_rect = shadow_surface.get_rect(center=(WIDTH // 2 + offset[0], 100 + offset[1]))
            self.screen.blit(shadow_surface, shadow_rect)
        
        # Título com glow
        title_surface = self.title_font.render(title_text, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(WIDTH // 2, 100))
        
        # Glow effect
        glow_surface = self.title_font.render(title_text, True, (138, 43, 226))
        for offset in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            glow_rect = title_rect.copy()
            glow_rect.x += offset[0]
            glow_rect.y += offset[1]
            self.screen.blit(glow_surface, glow_rect)
        
        self.screen.blit(title_surface, title_rect)
        
        # Subtítulo elegante
        subtitle_text = "A Busca pela Pedra Mística de Zappaguri"
        subtitle_surface = self.subtitle_font.render(subtitle_text, True, (216, 191, 216))
        subtitle_rect = subtitle_surface.get_rect(center=(WIDTH // 2, 140))
        
        # Sombra do subtítulo
        subtitle_shadow = self.subtitle_font.render(subtitle_text, True, (0, 0, 0))
        shadow_rect = subtitle_shadow.get_rect(center=(WIDTH // 2 + 1, 141))
        self.screen.blit(subtitle_shadow, shadow_rect)
        self.screen.blit(subtitle_surface, subtitle_rect)
    
    def draw_footer_info(self):
        """Desenha informações no rodapé"""
        footer_font = font_manager.get('small')
        
        info_lines = [
            "💡 Pressione Alt+Enter para alternar tela cheia",
            "🎮 Use WASD para movimento • Espaço para atacar • TAB para minimapa (Nível 3)"
        ]
        
        for i, line in enumerate(info_lines):
            info_surface = footer_font.render(line, True, (180, 180, 200))
            info_rect = info_surface.get_rect(center=(WIDTH // 2, HEIGTH - 60 + i * 20))
            
            # Sombra
            shadow_surface = footer_font.render(line, True, (0, 0, 0))
            shadow_rect = shadow_surface.get_rect(center=(WIDTH // 2 + 1, HEIGTH - 59 + i * 20))
            self.screen.blit(shadow_surface, shadow_rect)
            self.screen.blit(info_surface, info_rect)
    
    def handle_event(self, event):
        """Manipula eventos"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                tutorial_system.open_tutorial()
                return "show_tutorial"
            elif event.key == pygame.K_RETURN:
                return "start_game"
            elif event.key == pygame.K_ESCAPE:
                return "quit_game"
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
    
    def update_and_draw(self, mouse_pos, mouse_click):
        """Atualiza e desenha o menu AAA"""
        # Atualizar sistemas
        self.update_animations()
        self.update_particles()
        
        # Desenhar background
        self.screen.blit(self.background, (0, 0))
        
        # Overlay escuro sutil para contraste
        overlay = pygame.Surface((WIDTH, HEIGTH), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 40))
        self.screen.blit(overlay, (0, 0))
        
        # Desenhar partículas de fundo
        for particle in self.particles:
            particle.draw(self.screen)
        
        # Desenhar título épico
        self.draw_epic_title()
        
        # Desenhar botões AAA
        action = None
        if not self.graphics_screen.is_open():
            for button in self.buttons:
                button_action = button.update(mouse_pos, mouse_click)
                if button_action:
                    action = button_action
                button.draw(self.screen)
        
        # Desenhar informações do rodapé
        self.draw_footer_info()
        
        # Desenhar tela de gráficos se aberta
        self.graphics_screen.draw(self.screen)
        
        return action

# Função para obter o menu AAA
def get_aaa_menu(screen, fonts):
    return AAA_AdvancedMainMenu(screen, fonts)