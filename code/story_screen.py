import pygame
import math
import random
from settings import WIDTH, HEIGTH, TEXT_COLOR
from game_story import PHASE_STORIES
from professional_renderer import professional_renderer
# from enhanced_font_system import enhanced_font_renderer  # Comentado - módulo não existe
from font_manager import font_manager
# CHEAT: Import cheat system for testing (remove for final version)
from cheat_system import cheat_system

class StoryScreen:
    def __init__(self, story_key="intro", custom_background=None):
        self.display_surface = pygame.display.get_surface()
        self.story_data = PHASE_STORIES.get(story_key, PHASE_STORIES["intro"])
        
        # Usar sistema moderno de fontes - sem mais hardcoded!
        # Todas as fontes agora vem do font_manager
        
        # Animation variables
        self.scroll_y = HEIGTH
        self.scroll_speed = 1.2  # Velocidade otimizada para melhor experiência
        self.finished = False
        self.time = 0
        self.skip_requested = False
        
        # Carregar imagem de fundo (personalizada ou padrão)
        self.background_image = None
        background_path = custom_background or '../map new/map.png'
        
        try:
            self.background_image = pygame.image.load(background_path).convert()
            # Escalar para tela inteira com efeito escurecido
            self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGTH))
            # Criar uma sobreposição escura para legibilidade
            dark_overlay = pygame.Surface((WIDTH, HEIGTH))
            dark_overlay.set_alpha(200)  # Mais escuro para melhor contraste
            dark_overlay.fill((0, 0, 20))  # Azul escuro
            self.background_image.blit(dark_overlay, (0, 0))
            print(f"🖼️ Background da história carregado: {background_path}")
        except Exception as e:
            print(f"⚠️ Erro ao carregar background {background_path}: {e}")
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
        """Create the scrolling text surface with modern rendering"""
        # Calculate total height needed with better spacing
        line_height = 40          # Espaçamento otimizado entre linhas
        title_height = 120        # Mais espaço para título com efeitos
        subtitle_height = 80      # Mais espaço para subtítulo
        gap_height = 60           # Gap entre seções
        
        total_lines = len(self.story_data["text"])
        total_height = title_height + subtitle_height + gap_height + (total_lines * line_height) + 200
        
        # Create surface with modern background
        story_surface = pygame.Surface((WIDTH - 100, total_height), pygame.SRCALPHA)
        
        # Add subtle background panel
        panel_surface = professional_renderer.create_modern_panel(
            WIDTH - 100, total_height, background_alpha=120
        )
        story_surface.blit(panel_surface, (0, 0))
        
        y_pos = 30  # Padding from top
        
        # Title with modern effects
        title_surface, title_rect = professional_renderer.render_text_professional(
            self.story_data["title"], 
            'title', 
            (255, 215, 0),  # Dourado elegante
            shadow=True, 
            glow=True, 
            anti_alias=True
        )
        title_x = (story_surface.get_width() - title_rect.width) // 2
        story_surface.blit(title_surface, (title_x, y_pos))
        y_pos += title_height
        
        # Subtitle with professional rendering
        subtitle_surface, subtitle_rect = professional_renderer.render_text_professional(
            self.story_data["subtitle"], 
            'subtitle', 
            (100, 200, 255),  # Azul elegante
            shadow=True, 
            anti_alias=True
        )
        subtitle_x = (story_surface.get_width() - subtitle_rect.width) // 2
        story_surface.blit(subtitle_surface, (subtitle_x, y_pos))
        y_pos += subtitle_height + gap_height
        
        # Story text with enhanced rendering
        for line in self.story_data["text"]:
            if line.strip():  # Non-empty line
                text_surface, text_rect = professional_renderer.render_text_professional(
                    line, 
                    'text', 
                    (230, 230, 250),  # Branco suave
                    shadow=True, 
                    anti_alias=True
                )
                text_x = (story_surface.get_width() - text_rect.width) // 2
                story_surface.blit(text_surface, (text_x, y_pos))
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
        
        # Modern skip instruction with professional rendering
        skip_surface, skip_rect = professional_renderer.render_text_professional(
            "Pressione ESPACO para pular a historia", 
            'text',  # Use text size from font manager
            (255, 255, 100),  # Amarelo elegante
            shadow=True, 
            glow=True,
            anti_alias=True
        )
        skip_x = (WIDTH - skip_rect.width) // 2
        skip_y = HEIGTH - 35
        self.display_surface.blit(skip_surface, (skip_x, skip_y))
        
        # CHEAT: Display cheat information in story screen (remove for final version)
        cheat_system.display_cheat_info(self.display_surface)
        
        # Verificar se deve pular
        if self.skip_requested:
            self.finished = True
        
        pygame.display.update()
        
        return self.finished