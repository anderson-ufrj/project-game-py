"""
Tela inicial profissional do jogo Icarus
"""
import pygame
import math
from src.config import WIDTH, HEIGHT, COLORS, FONTS, CREDITS, GAME_STATES
from src.ui.button import AnimatedButton

class MainMenu:
    def __init__(self):
        self.buttons = []
        self.particles = []
        self.title_animation = 0
        self.setup_ui()
        self.setup_particles()
        
    def setup_ui(self):
        """Configura os botões da interface"""
        button_width = 280
        button_height = 60
        button_x = WIDTH // 2 - button_width // 2
        start_y = HEIGHT // 2 + 50
        
        # Botão Jogar
        self.btn_play = AnimatedButton(
            button_x, start_y, button_width, button_height,
            "JOGAR", FONTS['NORMAL'], 
            COLORS['GOLD'], COLORS['ORANGE'], COLORS['WHITE'], COLORS['DARK_BLUE']
        )
        
        # Botão Créditos
        self.btn_credits = AnimatedButton(
            button_x, start_y + 80, button_width, button_height,
            "CRÉDITOS", FONTS['NORMAL'],
            COLORS['LIGHT_BLUE'], COLORS['BLUE'], COLORS['WHITE'], COLORS['DARK_BLUE']
        )
        
        # Botão Sair
        self.btn_quit = AnimatedButton(
            button_x, start_y + 160, button_width, button_height,
            "SAIR", FONTS['NORMAL'],
            COLORS['GRAY'], COLORS['DARK_GRAY'], COLORS['WHITE'], COLORS['BLACK']
        )
        
        self.buttons = [self.btn_play, self.btn_credits, self.btn_quit]
    
    def setup_particles(self):
        """Cria partículas de fundo para efeito visual"""
        import random
        for _ in range(50):
            particle = {
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGHT),
                'speed_x': random.uniform(-0.5, 0.5),
                'speed_y': random.uniform(-0.5, 0.5),
                'size': random.randint(1, 3),
                'alpha': random.randint(50, 150)
            }
            self.particles.append(particle)
    
    def handle_event(self, event):
        """Processa eventos da tela"""
        # Eventos dos botões
        if self.btn_play.handle_event(event):
            return GAME_STATES['PLAYING']
        elif self.btn_credits.handle_event(event):
            return GAME_STATES['CREDITS']
        elif self.btn_quit.handle_event(event):
            return 'QUIT'
        
        return None
    
    def update(self, dt):
        """Atualiza animações"""
        self.title_animation += dt * 2
        
        # Atualiza botões
        for button in self.buttons:
            button.update()
        
        # Atualiza partículas
        for particle in self.particles:
            particle['x'] += particle['speed_x']
            particle['y'] += particle['speed_y']
            
            # Reposiciona partículas que saem da tela
            if particle['x'] < 0:
                particle['x'] = WIDTH
            elif particle['x'] > WIDTH:
                particle['x'] = 0
            if particle['y'] < 0:
                particle['y'] = HEIGHT
            elif particle['y'] > HEIGHT:
                particle['y'] = 0
    
    def draw(self, screen):
        """Desenha a tela inicial"""
        # Fundo gradiente
        self.draw_gradient_background(screen)
        
        # Partículas de fundo
        self.draw_particles(screen)
        
        # Título principal com animação
        self.draw_animated_title(screen)
        
        # Subtítulo
        self.draw_subtitle(screen)
        
        # Botões
        for button in self.buttons:
            button.draw(screen)
        
        # Versão
        self.draw_version_info(screen)
    
    def draw_gradient_background(self, screen):
        """Desenha um fundo degradê"""
        for y in range(HEIGHT):
            # Gradiente do azul escuro para azul claro
            ratio = y / HEIGHT
            r = int(25 + (135 * ratio))
            g = int(25 + (206 * ratio))
            b = int(112 + (118 * ratio))
            color = (min(255, r), min(255, g), min(255, b))
            pygame.draw.line(screen, color, (0, y), (WIDTH, y))
    
    def draw_particles(self, screen):
        """Desenha partículas flutuantes"""
        for particle in self.particles:
            # Criar superfície com alpha
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2))
            particle_surface.set_alpha(particle['alpha'])
            pygame.draw.circle(particle_surface, COLORS['WHITE'], 
                             (particle['size'], particle['size']), particle['size'])
            screen.blit(particle_surface, (particle['x'], particle['y']))
    
    def draw_animated_title(self, screen):
        """Desenha o título com animação"""
        # Efeito de flutuação
        offset_y = math.sin(self.title_animation) * 10
        
        # Título principal
        font = pygame.font.Font(None, FONTS['TITLE'] + 20)
        title_text = font.render("PROJETO ÍCARO", True, COLORS['GOLD'])
        title_rect = title_text.get_rect(center=(WIDTH // 2, 120 + offset_y))
        
        # Sombra do título
        shadow_text = font.render("PROJETO ÍCARO", True, COLORS['DARK_BLUE'])
        shadow_rect = shadow_text.get_rect(center=(WIDTH // 2 + 3, 123 + offset_y))
        screen.blit(shadow_text, shadow_rect)
        screen.blit(title_text, title_rect)
        
        # Linha decorativa
        line_y = int(title_rect.bottom + 20)
        pygame.draw.line(screen, COLORS['GOLD'], 
                        (WIDTH // 2 - 200, line_y), (WIDTH // 2 + 200, line_y), 3)
    
    def draw_subtitle(self, screen):
        """Desenha o subtítulo"""
        font = pygame.font.Font(None, FONTS['SUBTITLE'])
        subtitle = font.render("Um Jogo de Plataforma Mitológico", True, COLORS['WHITE'])
        subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, 200))
        screen.blit(subtitle, subtitle_rect)
    
    def draw_version_info(self, screen):
        """Desenha informações de versão"""
        font = pygame.font.Font(None, FONTS['TINY'])
        version_text = font.render("Versão 2.0 - Python + Pygame Zero", True, COLORS['LIGHT_BLUE'])
        screen.blit(version_text, (10, HEIGHT - 25))

class CreditsScreen:
    def __init__(self):
        self.scroll_y = HEIGHT
        self.setup_credits_text()
        
    def setup_credits_text(self):
        """Prepara o texto dos créditos"""
        self.credits_lines = [
            ("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", FONTS['NORMAL'], COLORS['GOLD']),
            ("", FONTS['SMALL'], COLORS['WHITE']),
            ("PROJETO ÍCARO", FONTS['TITLE'], COLORS['GOLD']),
            ("", FONTS['SMALL'], COLORS['WHITE']),
            ("Desenvolvido por:", FONTS['NORMAL'], COLORS['WHITE']),
            (CREDITS['DEVELOPER'], FONTS['SUBTITLE'], COLORS['LIGHT_BLUE']),
            (f"Estudante de {CREDITS['COURSE']}", FONTS['NORMAL'], COLORS['WHITE']),
            (CREDITS['INSTITUTION'], FONTS['NORMAL'], COLORS['WHITE']),
            ("", FONTS['SMALL'], COLORS['WHITE']),
            (f"Projeto acadêmico – {CREDITS['SUBJECT']}", FONTS['NORMAL'], COLORS['GOLD']),
            ("", FONTS['SMALL'], COLORS['WHITE']),
            (f"GitHub: {CREDITS['GITHUB']}", FONTS['SMALL'], COLORS['LIGHT_BLUE']),
            (f"LinkedIn: {CREDITS['LINKEDIN']}", FONTS['SMALL'], COLORS['LIGHT_BLUE']),
            ("", FONTS['SMALL'], COLORS['WHITE']),
            ("Programação & Design:", FONTS['NORMAL'], COLORS['WHITE']),
            (CREDITS['DEVELOPER'], FONTS['NORMAL'], COLORS['LIGHT_BLUE']),
            ("", FONTS['SMALL'], COLORS['WHITE']),
            ("Bibliotecas:", FONTS['NORMAL'], COLORS['WHITE']),
            ("Python + Pygame Zero", FONTS['NORMAL'], COLORS['LIGHT_BLUE']),
            ("", FONTS['SMALL'], COLORS['WHITE']),
            ("Sprites:", FONTS['NORMAL'], COLORS['WHITE']),
            ("[Créditos dos sprites serão adicionados]", FONTS['SMALL'], COLORS['GRAY']),
            ("", FONTS['NORMAL'], COLORS['WHITE']),
            ("", FONTS['NORMAL'], COLORS['WHITE']),
            ("Obrigado por jogar!", FONTS['SUBTITLE'], COLORS['GOLD']),
            ("", FONTS['NORMAL'], COLORS['WHITE']),
            ("Pressione ESC para voltar ao menu", FONTS['SMALL'], COLORS['WHITE']),
        ]
    
    def handle_event(self, event):
        """Processa eventos"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return GAME_STATES['MENU']
        return None
    
    def update(self, dt):
        """Atualiza o scroll dos créditos"""
        self.scroll_y -= 50 * dt  # Velocidade do scroll
        
        # Reinicia quando termina
        if self.scroll_y < -len(self.credits_lines) * 50 - HEIGHT:
            self.scroll_y = HEIGHT
    
    def draw(self, screen):
        """Desenha os créditos"""
        # Fundo escuro
        screen.fill(COLORS['BLACK'])
        
        # Desenha cada linha de crédito
        y_offset = self.scroll_y
        for line_text, font_size, color in self.credits_lines:
            if -50 <= y_offset <= HEIGHT + 50:  # Só desenha se estiver visível
                if line_text:  # Só desenha se não for linha vazia
                    font = pygame.font.Font(None, font_size)
                    text_surface = font.render(line_text, True, color)
                    text_rect = text_surface.get_rect(center=(WIDTH // 2, y_offset))
                    screen.blit(text_surface, text_rect)
            y_offset += 50