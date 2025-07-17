import pygame
import math
import time
import random
from settings import WIDTH, HEIGTH
from font_manager import font_manager
from tutorial_system import tutorial_system

class ModernMenuButton:
    """Botão moderno com animações e efeitos"""
    
    def __init__(self, x, y, width, height, text, action, icon=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.icon = icon
        
        # Estados de animação
        self.hover = False
        self.click_time = 0
        self.hover_animation = 0.0
        self.glow_intensity = 0.0
        
        # Cores
        self.base_color = (40, 45, 60)
        self.hover_color = (60, 70, 90)
        self.accent_color = (120, 150, 255)
        self.text_color = (220, 225, 235)
        
        # Fontes
        self.font = font_manager.get('button')
        self.icon_font = font_manager.get('title')
    
    def update(self, mouse_pos, mouse_click):
        """Atualiza estado do botão"""
        # Verificar hover
        was_hover = self.hover
        self.hover = self.rect.collidepoint(mouse_pos)
        
        # Animação de hover
        if self.hover:
            self.hover_animation = min(1.0, self.hover_animation + 0.1)
            self.glow_intensity = 0.5 + 0.3 * math.sin(time.time() * 4)
        else:
            self.hover_animation = max(0.0, self.hover_animation - 0.1)
            self.glow_intensity = 0.0
        
        # Verificar clique
        if self.hover and mouse_click:
            self.click_time = time.time()
            return self.action
        
        return None
    
    def draw(self, surface):
        """Desenha o botão com efeitos modernos"""
        # Calcular cor atual baseada na animação
        current_color = self.interpolate_color(
            self.base_color, self.hover_color, self.hover_animation
        )
        
        # Desenhar sombra suave
        shadow_offset = 3
        shadow_rect = self.rect.copy()
        shadow_rect.x += shadow_offset
        shadow_rect.y += shadow_offset
        shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, (0, 0, 0, 40), (0, 0, shadow_rect.width, shadow_rect.height), border_radius=8)
        surface.blit(shadow_surface, shadow_rect)
        
        # Desenhar borda brilhante se hover
        if self.hover_animation > 0:
            border_rect = self.rect.copy()
            border_rect.inflate_ip(4, 4)
            glow_color = (*self.accent_color, int(self.glow_intensity * 255))
            glow_surface = pygame.Surface((border_rect.width, border_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, glow_color, (0, 0, border_rect.width, border_rect.height), border_radius=10)
            surface.blit(glow_surface, (border_rect.x, border_rect.y))
        
        # Desenhar fundo do botão
        pygame.draw.rect(surface, current_color, self.rect, border_radius=8)
        
        # Desenhar gradiente sutil
        gradient_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        for y in range(self.rect.height):
            alpha = int(30 * (1 - y / self.rect.height))
            color = (255, 255, 255, alpha)
            pygame.draw.line(gradient_surface, color, (0, y), (self.rect.width, y))
        surface.blit(gradient_surface, self.rect)
        
        # Desenhar ícone e texto
        text_x = self.rect.centerx
        if self.icon:
            # Desenhar ícone
            icon_surface = self.icon_font.render(self.icon, True, self.accent_color)
            icon_rect = icon_surface.get_rect(center=(self.rect.x + 40, self.rect.centery))
            surface.blit(icon_surface, icon_rect)
            text_x = self.rect.x + 80
        
        # Desenhar texto principal
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(text_x, self.rect.centery))
        surface.blit(text_surface, text_rect)
        
        # Efeito de clique
        if time.time() - self.click_time < 0.2:
            click_overlay = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            click_overlay.fill((255, 255, 255, 50))
            surface.blit(click_overlay, self.rect)
    
    def interpolate_color(self, color1, color2, t):
        """Interpola entre duas cores"""
        return tuple(int(c1 + (c2 - c1) * t) for c1, c2 in zip(color1, color2))

class ProfessionalMainMenu:
    """Menu principal profissional com design moderno"""
    
    def __init__(self, screen):
        self.screen = screen
        
        # Carregar background
        try:
            self.background = pygame.image.load('../graphics/ui/home page.jpg').convert()
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGTH))
        except Exception as e:
            print(f"Aviso: Não foi possível carregar background: {e}")
            # Fallback para fundo gradiente
            self.background = self.create_gradient_background()
        
        # Criar overlay escuro para melhor contraste
        self.overlay = pygame.Surface((WIDTH, HEIGTH), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 120))
        
        # Partículas de fundo
        self.particles = []
        self.create_particles()
        
        # Fontes
        self.title_font = font_manager.get('title')
        self.subtitle_font = font_manager.get('subtitle')
        
        # Animações
        self.time = 0
        self.title_offset = 0
        self.subtitle_alpha = 255
        
        # Criar botões modernos
        self.create_modern_buttons()
    
    def create_gradient_background(self):
        """Cria um fundo gradiente caso não tenha imagem"""
        surface = pygame.Surface((WIDTH, HEIGTH))
        for y in range(HEIGTH):
            # Gradiente do azul escuro para preto
            r = int(20 * (1 - y / HEIGTH))
            g = int(30 * (1 - y / HEIGTH))
            b = int(50 * (1 - y / HEIGTH))
            pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))
        return surface
    
    def create_particles(self):
        """Cria partículas flutuantes de fundo"""
        for _ in range(30):
            particle = {
                'x': random.randint(0, WIDTH),
                'y': random.randint(0, HEIGTH),
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(-0.8, -0.2),
                'size': random.uniform(1, 3),
                'color': random.choice([
                    (120, 150, 255, 80),
                    (255, 215, 0, 60),
                    (255, 255, 255, 40)
                ])
            }
            self.particles.append(particle)
    
    def create_modern_buttons(self):
        """Cria botões com design moderno"""
        button_width = 320
        button_height = 55
        button_spacing = 70
        start_x = (WIDTH - button_width) // 2
        start_y = 280
        
        self.buttons = [
            ModernMenuButton(start_x, start_y, button_width, button_height, 
                           "INICIAR JOGO", "start_game", "▶"),
            ModernMenuButton(start_x, start_y + button_spacing, button_width, button_height, 
                           "TUTORIAL", "show_tutorial", "🎓"),
            ModernMenuButton(start_x, start_y + button_spacing * 2, button_width, button_height, 
                           "CONFIGURAÇÕES", "show_settings", "⚙"),
            ModernMenuButton(start_x, start_y + button_spacing * 3, button_width, button_height, 
                           "ESTATÍSTICAS", "show_stats", "📊"),
            ModernMenuButton(start_x, start_y + button_spacing * 4, button_width, button_height, 
                           "SAIR", "quit_game", "✕")
        ]
    
    def update_particles(self):
        """Atualiza partículas de fundo"""
        for particle in self.particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            
            # Reset da posição quando sair da tela
            if particle['y'] < -10:
                particle['y'] = HEIGTH + 10
                particle['x'] = random.randint(0, WIDTH)
            
            if particle['x'] < -10:
                particle['x'] = WIDTH + 10
            elif particle['x'] > WIDTH + 10:
                particle['x'] = -10
    
    def draw_particles(self):
        """Desenha partículas de fundo"""
        for particle in self.particles:
            # Criar surface com alpha para transparência
            particle_surface = pygame.Surface((int(particle['size'] * 2), int(particle['size'] * 2)), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, particle['color'], 
                             (int(particle['size']), int(particle['size'])), int(particle['size']))
            self.screen.blit(particle_surface, (int(particle['x']), int(particle['y'])))
    
    def draw_title(self):
        """Desenha título com efeitos profissionais"""
        # Animação sutil do título
        self.title_offset = math.sin(self.time * 0.002) * 3
        
        # Título principal
        title_text = "CORRIDA PELA RELÍQUIA"
        title_surface = self.title_font.render(title_text, True, (255, 255, 255))
        
        # Sombra do título
        shadow_surface = self.title_font.render(title_text, True, (0, 0, 0))
        
        # Posicionamento
        title_rect = title_surface.get_rect(center=(WIDTH // 2, 120 + self.title_offset))
        shadow_rect = shadow_surface.get_rect(center=(WIDTH // 2 + 3, 123 + self.title_offset))
        
        # Desenhar sombra e título
        self.screen.blit(shadow_surface, shadow_rect)
        self.screen.blit(title_surface, title_rect)
        
        # Subtítulo
        subtitle_text = "A Busca pela Pedra Mística do Zappaguri"
        subtitle_surface = self.subtitle_font.render(subtitle_text, True, (200, 215, 255))
        subtitle_rect = subtitle_surface.get_rect(center=(WIDTH // 2, 170))
        
        # Sombra do subtítulo
        subtitle_shadow = self.subtitle_font.render(subtitle_text, True, (0, 0, 0))
        shadow_rect = subtitle_shadow.get_rect(center=(WIDTH // 2 + 2, 172))
        
        self.screen.blit(subtitle_shadow, shadow_rect)
        self.screen.blit(subtitle_surface, subtitle_rect)
    
    def draw_footer(self):
        """Desenha informações no rodapé"""
        footer_y = HEIGTH - 60
        
        # Informações úteis
        info_font = font_manager.get('small')
        
        info_lines = [
            "💡 Pressione Alt+Enter para alternar tela cheia",
            "🎮 Use WASD para movimento • Espaço para atacar"
        ]
        
        for i, line in enumerate(info_lines):
            info_surface = info_font.render(line, True, (160, 170, 180))
            info_rect = info_surface.get_rect(center=(WIDTH // 2, footer_y + i * 20))
            self.screen.blit(info_surface, info_rect)
    
    def handle_event(self, event):
        """Manipula eventos do menu"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                tutorial_system.open_tutorial()
                return "show_tutorial"
            elif event.key == pygame.K_RETURN:
                return "start_game"
            elif event.key == pygame.K_ESCAPE:
                return "quit_game"
        
        return None
    
    def update_and_draw(self, mouse_pos, mouse_click):
        """Atualiza e desenha o menu completo"""
        # Atualizar tempo
        self.time = pygame.time.get_ticks()
        
        # Desenhar background
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.overlay, (0, 0))
        
        # Atualizar e desenhar partículas
        self.update_particles()
        self.draw_particles()
        
        # Desenhar título
        self.draw_title()
        
        # Atualizar e desenhar botões
        action = None
        for button in self.buttons:
            button_action = button.update(mouse_pos, mouse_click)
            if button_action:
                action = button_action
            button.draw(self.screen)
        
        # Desenhar rodapé
        self.draw_footer()
        
        return action

# Instância global
professional_menu = None

def get_professional_menu(screen):
    """Retorna instância do menu profissional"""
    global professional_menu
    if professional_menu is None:
        professional_menu = ProfessionalMainMenu(screen)
    return professional_menu