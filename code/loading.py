import pygame
import math
from support import import_folder
from settings import WIDTH, HEIGTH, TEXT_COLOR, UI_BG_COLOR, UI_BORDER_COLOR
from font_manager import font_manager
from professional_renderer import professional_renderer


class LoadingScreen():
    def __init__(self):
        # Use home page as background
        self.displaysurface = pygame.display.get_surface()
        
        # Load the home page image as background
        self.background = pygame.image.load('../graphics/ui/home page.jpg').convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGTH))
        
        # Create a semi-transparent overlay for better visibility of effects
        self.overlay = pygame.Surface((WIDTH, HEIGTH))
        self.overlay.set_alpha(180)  # Semi-transparent black overlay
        self.overlay.fill((0, 0, 0))
        
        self.rect = self.background.get_rect(topleft=(0, 0))
        self.music = pygame.mixer.Sound('../audio/Light Ambience 1.mp3')
        self.music.set_volume(0.5)
        
        # Loading animation variables
        self.time = 0
        self.particle_time = 0
        self.particles = []
        
        # Modern font system - no more hardcoded fonts needed
        
        # Create mystical particles (brighter for visibility)
        for _ in range(30):
            self.particles.append({
                'x': pygame.math.Vector2(WIDTH * 0.5, HEIGTH * 0.6).x + (pygame.math.Vector2(120, 0).rotate(360 * _ / 30)).x,
                'y': pygame.math.Vector2(WIDTH * 0.5, HEIGTH * 0.6).y + (pygame.math.Vector2(120, 0).rotate(360 * _ / 30)).y,
                'angle': 360 * _ / 30,
                'radius': 120,
                'size': pygame.math.Vector2(3, 8).length(),
                'color': (150 + (_ * 4) % 105, 255, 255 - (_ * 3) % 100)
            })

    def animate_background(self):
        # Reload the clean background to avoid accumulating effects
        self.background = pygame.image.load('../graphics/ui/home page.jpg').convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGTH))
        
        # Add subtle moving sparkles over the background
        for i in range(8):
            x = int((self.time * 40 + i * 160) % WIDTH)
            y = int((self.time * 25 + i * 100) % HEIGTH)
            size = int(2 + math.sin(self.time * 2 + i) * 1)
            alpha = int(100 + math.sin(self.time * 3 + i * 0.5) * 50)
            
            # Create sparkle effect
            sparkle_surface = pygame.Surface((size * 4, size * 4), pygame.SRCALPHA)
            pygame.draw.circle(sparkle_surface, (255, 255, 200, alpha), (size * 2, size * 2), size)
            pygame.draw.circle(sparkle_surface, (255, 255, 255, alpha // 2), (size * 2, size * 2), size // 2)
            
            self.background.blit(sparkle_surface, (x - size * 2, y - size * 2), special_flags=pygame.BLEND_ADD)

    def update_particles(self):
        self.time += 0.05
        self.particle_time += 1
        
        center_x = WIDTH * 0.5
        center_y = HEIGTH * 0.6
        
        for particle in self.particles:
            # Rotate particles around center
            particle['angle'] += 1
            new_radius = particle['radius'] + math.sin(self.time + particle['angle'] * 0.1) * 20
            
            particle['x'] = center_x + math.cos(math.radians(particle['angle'])) * new_radius
            particle['y'] = center_y + math.sin(math.radians(particle['angle'])) * new_radius
            
            # Pulsing effect
            particle['size'] = 2 + math.sin(self.time * 3 + particle['angle'] * 0.05) * 2

    def draw_loading_effects(self):
        # Draw mystical particles
        for particle in self.particles:
            pygame.draw.circle(
                self.displaysurface, 
                particle['color'], 
                (int(particle['x']), int(particle['y'])), 
                int(particle['size'])
            )
        
        # Draw central loading circle (brighter for visibility)
        center_x = WIDTH // 2
        center_y = HEIGTH * 0.6
        
        # Outer glowing ring (brighter colors)
        for i in range(4):
            pygame.draw.circle(
                self.displaysurface, 
                (100 + i * 40, 150 + i * 30, 255), 
                (int(center_x), int(center_y)), 
                int(90 - i * 15 + math.sin(self.time * 2) * 8), 
                4
            )
        
        # Loading text with glow effect
        loading_texts = [
            "Carregando...",
            "Preparando Aventura...", 
            "Invocando Magias...",
            "Carregando Relíquias..."
        ]
        
        current_text = loading_texts[int(self.time * 0.5) % len(loading_texts)]
        
        # Main text with modern rendering
        text_surface, text_rect = professional_renderer.render_text_professional(
            current_text, 'subtitle', TEXT_COLOR,
            shadow=True, glow=True, anti_alias=True
        )
        text_rect.center = (center_x, center_y + 100)
        self.displaysurface.blit(text_surface, text_rect)
        
        # Progress dots with modern rendering
        dots = "." * (int(self.time * 2) % 4)
        dots_surface, dots_rect = professional_renderer.render_text_professional(
            dots, 'text', TEXT_COLOR,
            shadow=True, anti_alias=True
        )
        dots_rect.center = (center_x + text_rect.width // 2 + 20, center_y + 100)
        self.displaysurface.blit(dots_surface, dots_rect)

    def update(self):
        self.animate_background()
        self.update_particles()
        self.music.play(-1)
        
        # Draw the background (home page with sparkles)
        self.displaysurface.blit(self.background, (0, 0))
        
        # Apply semi-transparent overlay for better contrast
        self.displaysurface.blit(self.overlay, (0, 0))
        
        # Draw loading effects on top
        self.draw_loading_effects()
