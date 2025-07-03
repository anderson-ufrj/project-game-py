import pygame
import math
from settings import WIDTH, HEIGTH, TEXT_COLOR
from game_story import PHASE_STORIES

class StoryScreen:
    def __init__(self, story_key="intro"):
        self.display_surface = pygame.display.get_surface()
        self.story_data = PHASE_STORIES.get(story_key, PHASE_STORIES["intro"])
        
        # Font setup
        try:
            self.title_font = pygame.font.Font('../graphics/font/PressStart2P.ttf', 28)
            self.subtitle_font = pygame.font.Font('../graphics/font/PressStart2P.ttf', 16)
            self.text_font = pygame.font.Font('../graphics/font/PressStart2P.ttf', 14)
        except:
            self.title_font = pygame.font.Font(None, 32)
            self.subtitle_font = pygame.font.Font(None, 20)
            self.text_font = pygame.font.Font(None, 16)
        
        # Animation variables
        self.scroll_y = HEIGTH
        self.scroll_speed = 1.5
        self.finished = False
        self.time = 0
        
        # Create starfield background
        self.stars = []
        for _ in range(100):
            self.stars.append({
                'x': pygame.math.Vector2.random() * WIDTH,
                'y': pygame.math.Vector2.random() * HEIGTH,
                'speed': 0.5 + pygame.math.Vector2.random() * 1.5,
                'brightness': 100 + int(pygame.math.Vector2.random() * 155)
            })
    
    def create_story_surface(self):
        """Create the scrolling text surface"""
        # Calculate total height needed
        line_height = 25
        title_height = 60
        subtitle_height = 40
        gap_height = 30
        
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
                star['x'] = pygame.math.Vector2.random() * WIDTH
    
    def draw_stars(self):
        """Draw animated starfield"""
        for star in self.stars:
            alpha = star['brightness']
            color = (alpha, alpha, alpha)
            pygame.draw.circle(self.display_surface, color, 
                             (int(star['x']), int(star['y'])), 1)
    
    def handle_input(self):
        """Handle input to skip story"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN] or keys[pygame.K_SPACE] or keys[pygame.K_ESCAPE]:
            self.finished = True
    
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
            if self.scroll_y < -story_surface.get_height():
                self.finished = True
        
        # Clear screen with space background
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
        
        # Draw skip instruction
        skip_text = self.text_font.render("Pressione ENTER para pular", True, (150, 150, 150))
        skip_rect = skip_text.get_rect(center=(WIDTH // 2, HEIGTH - 30))
        self.display_surface.blit(skip_text, skip_rect)
        
        pygame.display.update()
        
        return self.finished