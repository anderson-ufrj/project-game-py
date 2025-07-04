import pygame
import math
import random
from settings import WIDTH, HEIGTH, TEXT_COLOR
from game_story import PHASE_STORIES
# CHEAT: Import cheat system for testing (remove for final version)
from cheat_system import cheat_system

class StoryScreen:
    def __init__(self, story_key="intro"):
        self.display_surface = pygame.display.get_surface()
        self.story_data = PHASE_STORIES.get(story_key, PHASE_STORIES["intro"])
        
        # Font setup - usar fontes arredondadas como nos créditos
        try:
            # Tentar carregar fonte especial primeiro
            self.title_font = pygame.font.Font('../graphics/font/PressStart2P.ttf', 28)
            self.subtitle_font = pygame.font.Font('../graphics/font/PressStart2P.ttf', 16)
            self.text_font = pygame.font.Font('../graphics/font/PressStart2P.ttf', 14)
        except:
            # Usar fontes arredondadas do sistema (como nos créditos)
            self.title_font = pygame.font.Font(None, 40)      # Maior e mais bonita
            self.subtitle_font = pygame.font.Font(None, 24)   # Fonte arredondada
            self.text_font = pygame.font.Font(None, 18)       # Fonte legível e arredondada
        
        # Animation variables
        self.scroll_y = HEIGTH
        self.scroll_speed = 0.15  # Velocidade MUITO mais lenta - quase parando!
        self.finished = False
        self.time = 0
        self.skip_requested = False
        
        # Carregar imagem de fundo
        try:
            self.background_image = pygame.image.load('../map new/map.png').convert()
            # Escalar para tela inteira com efeito escurecido
            self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGTH))
            # Criar uma sobreposição escura
            dark_overlay = pygame.Surface((WIDTH, HEIGTH))
            dark_overlay.set_alpha(180)  # Semi-transparente
            dark_overlay.fill((0, 0, 20))  # Azul escuro
            self.background_image.blit(dark_overlay, (0, 0))
        except:
            self.background_image = None
        
        # Create starfield background
        self.stars = []
        for _ in range(100):
            self.stars.append({
                'x': random.random() * WIDTH,
                'y': random.random() * HEIGTH,
                'speed': 0.5 + random.random() * 1.5,
                'brightness': 100 + int(random.random() * 155)
            })
    
    def create_story_surface(self):
        """Create the scrolling text surface"""
        # Calculate total height needed - mais espaçamento para leitura
        line_height = 35          # Mais espaçamento entre linhas
        title_height = 80         # Mais espaço para título
        subtitle_height = 50      # Mais espaço para subtítulo
        gap_height = 50           # Mais gap entre seções
        
        total_lines = len(self.story_data["text"])
        total_height = title_height + subtitle_height + gap_height + (total_lines * line_height) + 200
        
        # Create surface
        story_surface = pygame.Surface((WIDTH - 100, total_height), pygame.SRCALPHA)
        
        y_pos = 0
        
        # Title (centered)
        title_text = self.title_font.render(self.story_data["title"], True, (255, 255, 100))
        title_rect = title_text.get_rect(centerx=story_surface.get_width() // 2, y=y_pos)
        story_surface.blit(title_text, title_rect)
        y_pos += title_height
        
        # Subtitle (centered)
        subtitle_text = self.subtitle_font.render(self.story_data["subtitle"], True, (100, 200, 255))
        subtitle_rect = subtitle_text.get_rect(centerx=story_surface.get_width() // 2, y=y_pos)
        story_surface.blit(subtitle_text, subtitle_rect)
        y_pos += subtitle_height + gap_height
        
        # Story text (centered)
        for line in self.story_data["text"]:
            if line.strip():  # Non-empty line
                text_surface = self.text_font.render(line, True, TEXT_COLOR)
                text_rect = text_surface.get_rect(centerx=story_surface.get_width() // 2, y=y_pos)
                story_surface.blit(text_surface, text_rect)
            y_pos += line_height
        
        return story_surface
    
    def update_stars(self):
        """Update starfield animation"""
        for star in self.stars:
            star['y'] += star['speed']
            if star['y'] > HEIGTH:
                star['y'] = -5
                star['x'] = random.random() * WIDTH
    
    def draw_stars(self):
        """Draw animated starfield"""
        for star in self.stars:
            alpha = star['brightness']
            color = (alpha, alpha, alpha)
            pygame.draw.circle(self.display_surface, color, 
                             (int(star['x']), int(star['y'])), 1)
    
    def handle_input(self):
        """Handle input to skip story"""
        # Don't consume events here - let main.py handle cheats
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN] or keys[pygame.K_SPACE] or keys[pygame.K_ESCAPE]:
            self.skip_requested = True
    
    def update(self):
        """Update story screen"""
        self.time += 0.1
        self.handle_input()
        
        if not self.finished:
            # Update scroll position
            self.scroll_y -= self.scroll_speed
            
            # Update stars
            self.update_stars()
            
            # Check if story finished scrolling
            story_surface = self.create_story_surface()
            if self.scroll_y < -story_surface.get_height() - 200:
                self.finished = True
        
        # Clear screen and draw background
        if self.background_image:
            self.display_surface.blit(self.background_image, (0, 0))
        else:
            self.display_surface.fill((10, 10, 30))
        
        # Draw stars
        self.draw_stars()
        
        # Create and draw story text
        story_surface = self.create_story_surface()
        
        # Calculate position with perspective effect
        perspective_scale = max(0.8, 1.0 - abs(self.scroll_y) / (HEIGTH * 2))
        scaled_width = int(story_surface.get_width() * perspective_scale)
        scaled_height = int(story_surface.get_height() * perspective_scale)
        
        if scaled_width > 0 and scaled_height > 0:
            scaled_surface = pygame.transform.scale(story_surface, (scaled_width, scaled_height))
            
            # Position in center of screen
            x = (WIDTH - scaled_width) // 2
            y = int(self.scroll_y * perspective_scale)
            
            self.display_surface.blit(scaled_surface, (x, y))
        
        # Draw elegant skip instruction with translucent background
        skip_bg = pygame.Surface((520, 50), pygame.SRCALPHA)
        skip_bg.fill((20, 20, 40, 180))  # Semi-transparent background
        
        # Add inner glow for elegance
        inner_bg = pygame.Surface((500, 35), pygame.SRCALPHA)
        inner_bg.fill((60, 60, 80, 120))
        skip_bg.blit(inner_bg, (10, 7.5))
        
        skip_bg_rect = pygame.Rect((WIDTH // 2 - 260, HEIGTH - 60), (520, 50))
        self.display_surface.blit(skip_bg, skip_bg_rect)
        
        # Add elegant borders
        pygame.draw.rect(self.display_surface, (120, 120, 140), skip_bg_rect, 2)
        pygame.draw.rect(self.display_surface, (180, 180, 200), skip_bg_rect, 1)
        
        # Enhanced text with shadow
        skip_font = pygame.font.Font(None, 22)  # Fonte maior para instrução
        
        # Text shadow for better readability
        shadow_text = skip_font.render("Pressione ESPACO para pular a historia", True, (0, 0, 0))
        shadow_rect = shadow_text.get_rect(center=(WIDTH // 2 + 2, HEIGTH - 33))
        self.display_surface.blit(shadow_text, shadow_rect)
        
        # Main text
        skip_text = skip_font.render("Pressione ESPACO para pular a historia", True, (255, 255, 100))
        skip_rect = skip_text.get_rect(center=(WIDTH // 2, HEIGTH - 35))
        self.display_surface.blit(skip_text, skip_rect)
        
        # CHEAT: Display cheat information in story screen (remove for final version)
        cheat_system.display_cheat_info(self.display_surface)
        
        # Verificar se deve pular
        if self.skip_requested:
            self.finished = True
        
        pygame.display.update()
        
        return self.finished