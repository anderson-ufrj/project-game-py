import pygame
import math
import random
from settings import *

class MenuParticle:
    """Partícula mágica para o menu principal"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-1, -0.2)
        self.size = random.uniform(1, 3)
        self.life = random.uniform(100, 200)
        self.max_life = self.life
        self.color = random.choice([
            (255, 215, 0),    # Dourado
            (138, 43, 226),   # Roxo
            (0, 191, 255),    # Azul
            (255, 20, 147),   # Rosa
            (50, 205, 50)     # Verde
        ])
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        
        # Movimento flutuante
        self.y += math.sin(pygame.time.get_ticks() * 0.001 + self.x * 0.01) * 0.1
        
        return self.life > 0
    
    def draw(self, surface):
        if self.life > 0:
            alpha = int(255 * (self.life / self.max_life))
            color = (*self.color, alpha)
            
            # Desenhar com transparência
            s = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
            pygame.draw.circle(s, color, (int(self.size), int(self.size)), int(self.size))
            surface.blit(s, (int(self.x - self.size), int(self.y - self.size)))

class MenuButton:
    """Botão interativo do menu"""
    def __init__(self, x, y, width, height, text, font, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.action = action
        self.hovered = False
        self.clicked = False
        self.glow_intensity = 0
        
    def update(self, mouse_pos, mouse_click):
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        if self.hovered:
            self.glow_intensity = min(self.glow_intensity + 5, 255)
            if mouse_click:
                self.clicked = True
                return self.action
        else:
            self.glow_intensity = max(self.glow_intensity - 5, 0)
            
        return None
    
    def draw(self, surface):
        # Fundo do botão com transparência
        bg_alpha = 100 + int(self.glow_intensity * 0.3)
        if self.hovered:
            bg_color = (100, 50, 150, bg_alpha)
        else:
            bg_color = (50, 50, 80, bg_alpha)
            
        # Desenhar fundo
        s = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(s, bg_color, (0, 0, self.rect.width, self.rect.height), border_radius=10)
        surface.blit(s, self.rect.topleft)
        
        # Borda brilhante quando hover
        if self.hovered:
            border_color = (255, 215, 0, self.glow_intensity)
            border_s = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            pygame.draw.rect(border_s, border_color, (0, 0, self.rect.width, self.rect.height), 3, border_radius=10)
            surface.blit(border_s, self.rect.topleft)
        
        # Texto do botão
        text_color = (255, 255, 255) if not self.hovered else (255, 215, 0)
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

class AdvancedMainMenu:
    """Menu principal avançado com animações e efeitos"""
    
    def __init__(self, screen, fonts):
        self.screen = screen
        self.title_font = fonts['title']
        self.subtitle_font = fonts['subtitle'] 
        self.info_font = fonts['info']
        self.button_font = fonts['button'] if 'button' in fonts else fonts['info']
        
        # Carregar imagens
        try:
            self.background = pygame.image.load('../graphics/ui/home page.jpg').convert()
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGTH))
            
            self.logo_if = pygame.image.load('../graphics/logoif.png').convert_alpha()
            self.logo_if = pygame.transform.scale(self.logo_if, (80, 80))
            
            self.author_photo = pygame.image.load('../graphics/author.jpeg').convert()
            self.author_photo = pygame.transform.scale(self.author_photo, (60, 60))
            # Criar máscara circular para a foto
            self.author_photo = self.make_circular_image(self.author_photo)
            
        except:
            print("Erro ao carregar imagens do menu")
        
        # Carregar fontes mais arredondadas
        try:
            # Usar fonte padrão do sistema mais arredondada
            self.custom_title_font = pygame.font.Font(None, 48)  # Fonte maior para título
            self.custom_subtitle_font = pygame.font.Font(None, 24)  # Fonte média para subtítulo
            self.custom_button_font = pygame.font.Font(None, 20)  # Fonte para botões
            self.custom_info_font = pygame.font.Font(None, 16)  # Fonte para informações
        except:
            # Fallback para fontes originais se houver erro
            self.custom_title_font = self.title_font
            self.custom_subtitle_font = self.subtitle_font
            self.custom_button_font = self.button_font
            self.custom_info_font = self.info_font
        
        # Sistema de partículas
        self.particles = []
        self.particle_spawn_timer = 0
        
        # Animações
        self.time = 0
        self.title_glow = 0
        self.title_glow_direction = 1
        
        # Estado do menu
        self.current_section = "main"  # main, credits, stats
        
        # Estatísticas do jogo (placeholder)
        self.game_stats = {
            'levels_completed': 0,
            'total_time': 0,
            'gems_collected': 0,
            'deaths': 0
        }
        
        # Criar botões do menu principal
        self.main_buttons = self.create_main_buttons()
        self.credits_buttons = self.create_credits_buttons()
        self.stats_buttons = self.create_stats_buttons()
        
    def make_circular_image(self, image):
        """Converte uma imagem para formato circular"""
        size = image.get_size()
        mask = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.circle(mask, (255, 255, 255), (size[0]//2, size[1]//2), min(size)//2)
        
        result = pygame.Surface(size, pygame.SRCALPHA)
        for x in range(size[0]):
            for y in range(size[1]):
                if mask.get_at((x, y))[3] > 0:  # Se o alpha da máscara > 0
                    result.set_at((x, y), image.get_at((x, y)))
        return result
    
    def create_main_buttons(self):
        """Criar botões do menu principal"""
        buttons = []
        button_width = 280
        button_height = 45
        start_y = HEIGTH // 2 + 30  # Começar mais cedo para não sobrepor instruções
        spacing = 60
        
        button_data = [
            ("► INICIAR JOGO", "start_game"),
            ("📊 ESTATÍSTICAS", "show_stats"),
            ("👥 CRÉDITOS", "show_credits"),
            ("❌ SAIR", "quit_game")
        ]
        
        for i, (text, action) in enumerate(button_data):
            x = WIDTH // 2 - button_width // 2
            y = start_y + i * spacing
            buttons.append(MenuButton(x, y, button_width, button_height, text, self.custom_button_font, action))
            
        return buttons
    
    def create_credits_buttons(self):
        """Criar botões da tela de créditos"""
        return [MenuButton(50, HEIGTH - 100, 150, 40, "← VOLTAR", self.custom_button_font, "back_to_main")]
    
    def create_stats_buttons(self):
        """Criar botões da tela de estatísticas"""
        return [MenuButton(50, HEIGTH - 100, 150, 40, "← VOLTAR", self.custom_button_font, "back_to_main")]
    
    def update_particles(self):
        """Atualizar sistema de partículas"""
        # Spawnar novas partículas
        self.particle_spawn_timer += 1
        if self.particle_spawn_timer > 20:  # Spawnar a cada 20 frames
            # Spawnar próximo ao portal (centro da tela)
            x = WIDTH // 2 + random.randint(-100, 100)
            y = HEIGTH // 2 + random.randint(-50, 50)
            self.particles.append(MenuParticle(x, y))
            self.particle_spawn_timer = 0
        
        # Atualizar partículas existentes
        self.particles = [p for p in self.particles if p.update()]
        
        # Limitar número de partículas
        if len(self.particles) > 50:
            self.particles = self.particles[-50:]
    
    def update_animations(self):
        """Atualizar animações"""
        self.time += 1
        
        # Animação do brilho do título
        self.title_glow += self.title_glow_direction * 3
        if self.title_glow >= 50:
            self.title_glow_direction = -1
        elif self.title_glow <= 0:
            self.title_glow_direction = 1
    
    def draw_title_with_glow(self):
        """Desenhar título com efeito glow e fontes melhoradas"""
        title_text = "CORRIDA PELA RELÍQUIA"
        
        # Calcular posição do título
        title_surface = self.custom_title_font.render(title_text, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(WIDTH//2, 110))
        
        # Desenhar sombra simples para melhor contraste
        shadow_surface = self.custom_title_font.render(title_text, True, (0, 0, 0))
        self.screen.blit(shadow_surface, (title_rect.x + 3, title_rect.y + 3))
        
        # Desenhar título principal com gradiente suave
        gradient_colors = [
            (255, 215, 0),   # Dourado
            (255, 255, 255)  # Branco
        ]
        
        # Efeito gradiente simples
        for i, color in enumerate(gradient_colors):
            offset = i + 1
            title_glow = self.custom_title_font.render(title_text, True, color)
            title_glow.set_alpha(200 - i * 50)
            self.screen.blit(title_glow, (title_rect.x - offset, title_rect.y - offset))
        
        # Desenhar título principal
        self.screen.blit(title_surface, title_rect)
        
        # Subtitle com animação mais sutil
        subtitle_y = 150 + math.sin(self.time * 0.03) * 2
        subtitle_text = self.custom_subtitle_font.render("A Busca pela Pedra Mística do Zappaguri", True, (220, 220, 255))
        subtitle_rect = subtitle_text.get_rect(center=(WIDTH//2, subtitle_y))
        
        # Sombra do subtitle
        subtitle_shadow = self.custom_subtitle_font.render("A Busca pela Pedra Mística do Zappaguri", True, (0, 0, 0))
        self.screen.blit(subtitle_shadow, (subtitle_rect.x + 2, subtitle_rect.y + 2))
        self.screen.blit(subtitle_text, subtitle_rect)
    
    def draw_main_menu(self, mouse_pos, mouse_click):
        """Desenhar menu principal"""
        # Título animado
        self.draw_title_with_glow()
        
        # Desenhar e atualizar botões
        action = None
        for button in self.main_buttons:
            button_action = button.update(mouse_pos, mouse_click)
            if button_action:
                action = button_action
            button.draw(self.screen)
        
        # Instruções de controle - movidas para baixo para não sobrepor botões
        controls_y = HEIGTH - 140
        controls = [
            "⌨️ WASD/Setas: Movimento | Shift: Correr | Espaço: Ataque 360°",
            "♪ M: Mudo | ↑↓: Volume | ⚙: Configurações | S: Estatísticas | D: Dificuldade",
            "💾 L: Carregar Jogo | F5: Quick Save | F9: Quick Load | F6: Salvar",
            "🗺️ TAB: Minimapa (Fase 3) | ♦ Teclas 1-4: Ir direto para fase"
        ]
        
        for i, control in enumerate(controls):
            text = self.custom_info_font.render(control, True, (200, 200, 200))
            rect = text.get_rect(center=(WIDTH//2, controls_y + i * 18))
            # Sombra
            shadow = self.custom_info_font.render(control, True, (0, 0, 0))
            self.screen.blit(shadow, (rect.x + 1, rect.y + 1))
            self.screen.blit(text, rect)
        
        return action
    
    def draw_credits_screen(self, mouse_pos, mouse_click):
        """Desenhar tela de créditos"""
        # Fundo semi-transparente
        overlay = pygame.Surface((WIDTH, HEIGTH), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Título da seção
        title = self.custom_title_font.render("CRÉDITOS", True, (255, 215, 0))
        title_rect = title.get_rect(center=(WIDTH//2, 80))
        self.screen.blit(title, title_rect)
        
        # Seção do desenvolvedor
        dev_y = 150
        
        # Foto do autor
        self.screen.blit(self.author_photo, (WIDTH//2 - 150, dev_y))
        
        # Informações do desenvolvedor
        dev_info = [
            "DESENVOLVEDOR",
            "Anderson Henrique da Silva",
            "Estudante de Ciência da Computação",
            "IFSULDEMINAS Campus Muzambinho"
        ]
        
        for i, info in enumerate(dev_info):
            color = (255, 215, 0) if i == 0 else (255, 255, 255)
            font = self.custom_subtitle_font if i == 0 else self.custom_info_font
            text = font.render(info, True, color)
            self.screen.blit(text, (WIDTH//2 - 80, dev_y + i * 25))
        
        # Seção acadêmica
        academic_y = dev_y + 150
        
        # Logo do IF
        self.screen.blit(self.logo_if, (WIDTH//2 - 150, academic_y))
        
        academic_info = [
            "PROJETO ACADÊMICO",
            "Disciplina: Tópicos Especiais I",
            "Orientador: Prof. Ricardo Martins",
            "IFSULDEMINAS Campus Muzambinho"
        ]
        
        for i, info in enumerate(academic_info):
            color = (255, 215, 0) if i == 0 else (255, 255, 255)
            font = self.custom_subtitle_font if i == 0 else self.custom_info_font
            text = font.render(info, True, color)
            self.screen.blit(text, (WIDTH//2 - 80, academic_y + i * 25))
        
        # Tecnologias utilizadas
        tech_y = academic_y + 150
        tech_title = self.custom_subtitle_font.render("TECNOLOGIAS", True, (255, 215, 0))
        self.screen.blit(tech_title, (WIDTH//2 - 100, tech_y))
        
        technologies = [
            "🐍 Python 3.8+ & Pygame 2.6+",
            "🎨 PIL/Pillow para processamento de imagens",
            "🎵 Sistema de áudio centralizado com Threading",
            "🗺️ Mapas criados com Tiled & CSV",
            "✨ Assets do OpenGameArt.org"
        ]
        
        for i, tech in enumerate(technologies):
            text = self.custom_info_font.render(tech, True, (200, 200, 255))
            self.screen.blit(text, (WIDTH//2 - 200, tech_y + 30 + i * 20))
        
        # Botão voltar
        action = None
        for button in self.credits_buttons:
            button_action = button.update(mouse_pos, mouse_click)
            if button_action:
                action = button_action
            button.draw(self.screen)
        
        return action
    
    def draw_stats_screen(self, mouse_pos, mouse_click):
        """Desenhar tela de estatísticas"""
        # Fundo semi-transparente
        overlay = pygame.Surface((WIDTH, HEIGTH), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Título
        title = self.custom_title_font.render("ESTATÍSTICAS", True, (255, 215, 0))
        title_rect = title.get_rect(center=(WIDTH//2, 80))
        self.screen.blit(title, title_rect)
        
        # Estatísticas do jogo
        stats_y = 150
        stats_data = [
            ("🏆 Níveis Completados", f"{self.game_stats['levels_completed']}/4"),
            ("⏱️ Tempo Total de Jogo", f"{self.game_stats['total_time']//60}min {self.game_stats['total_time']%60}s"),
            ("💎 Gemas Coletadas", str(self.game_stats['gems_collected'])),
            ("💀 Mortes", str(self.game_stats['deaths'])),
        ]
        
        for i, (label, value) in enumerate(stats_data):
            # Label
            label_text = self.custom_subtitle_font.render(label, True, (255, 215, 0))
            self.screen.blit(label_text, (WIDTH//2 - 200, stats_y + i * 60))
            
            # Valor
            value_text = self.custom_title_font.render(value, True, (255, 255, 255))
            value_rect = value_text.get_rect(right=WIDTH//2 + 200, y=stats_y + i * 60)
            self.screen.blit(value_text, value_rect)
        
        # Progresso visual
        progress_y = stats_y + 300
        progress_title = self.custom_subtitle_font.render("PROGRESSO DOS NÍVEIS", True, (255, 215, 0))
        self.screen.blit(progress_title, (WIDTH//2 - 150, progress_y))
        
        # Barras de progresso por nível
        level_names = ["🌲 Floresta", "🌀 Labirinto", "🏰 Fortaleza", "⚡ Final"]
        for i, level_name in enumerate(level_names):
            y = progress_y + 40 + i * 30
            completed = i < self.game_stats['levels_completed']
            
            # Nome do nível
            color = (100, 255, 100) if completed else (100, 100, 100)
            text = self.custom_info_font.render(level_name, True, color)
            self.screen.blit(text, (WIDTH//2 - 200, y))
            
            # Status
            status = "✅ COMPLETO" if completed else "⏳ PENDENTE"
            status_text = self.custom_info_font.render(status, True, color)
            self.screen.blit(status_text, (WIDTH//2 + 50, y))
        
        # Botão voltar
        action = None
        for button in self.stats_buttons:
            button_action = button.update(mouse_pos, mouse_click)
            if button_action:
                action = button_action
            button.draw(self.screen)
        
        return action
    
    def update_and_draw(self, mouse_pos, mouse_click):
        """Atualizar e desenhar o menu principal"""
        # Desenhar background
        self.screen.blit(self.background, (0, 0))
        
        # Atualizar sistemas
        self.update_particles()
        self.update_animations()
        
        # Desenhar partículas
        for particle in self.particles:
            particle.draw(self.screen)
        
        # Desenhar seção atual
        action = None
        if self.current_section == "main":
            action = self.draw_main_menu(mouse_pos, mouse_click)
        elif self.current_section == "credits":
            action = self.draw_credits_screen(mouse_pos, mouse_click)
        elif self.current_section == "stats":
            action = self.draw_stats_screen(mouse_pos, mouse_click)
        
        # Processar ações
        if action == "start_game":
            return "start_game"
        elif action == "show_credits":
            self.current_section = "credits"
        elif action == "show_stats":
            self.current_section = "stats"
        elif action == "back_to_main":
            self.current_section = "main"
        elif action == "quit_game":
            return "quit_game"
        
        return None