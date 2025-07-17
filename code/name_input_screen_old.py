import pygame
import sys
from settings import *
from player_stats import player_stats

class NameInputScreen:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../graphics/font/PressStart2P.ttf', 24)
        self.title_font = pygame.font.Font('../graphics/font/PressStart2P.ttf', 36)
        self.small_font = pygame.font.Font('../graphics/font/PressStart2P.ttf', 16)
        
        # Input state
        self.input_text = ""
        self.max_length = 20
        self.active = True
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_blink_speed = 500  # milliseconds
        
        # Background
        self.background = pygame.image.load('../graphics/ui/home page.jpg').convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGTH))
        
        # Overlay for better text visibility
        self.overlay = pygame.Surface((WIDTH, HEIGTH))
        self.overlay.set_alpha(180)
        self.overlay.fill((0, 0, 0))
        
        # Colors
        self.text_color = (255, 255, 255)
        self.input_bg_color = (30, 30, 30)
        self.input_border_color = (100, 100, 100)
        self.input_active_color = (0, 150, 255)
        
        # Input box
        self.input_box = pygame.Rect(WIDTH // 2 - 200, HEIGTH // 2 - 25, 400, 50)
        
        # Buttons
        self.confirm_button = pygame.Rect(WIDTH // 2 - 100, HEIGTH // 2 + 80, 200, 40)
        self.skip_button = pygame.Rect(WIDTH // 2 - 100, HEIGTH // 2 + 140, 200, 40)
        
        # Check if player already has a name
        self.player_has_name = bool(player_stats.stats["player_name"])
        
    def handle_events(self, events):
        """Handle input events"""
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    return self.confirm_name()
                elif event.key == pygame.K_ESCAPE:
                    return self.skip_name()
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    # Add character if it's printable and within limit
                    if event.unicode.isprintable() and len(self.input_text) < self.max_length:
                        self.input_text += event.unicode
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if self.confirm_button.collidepoint(event.pos):
                        return self.confirm_name()
                    elif self.skip_button.collidepoint(event.pos):
                        return self.skip_name()
        
        return 'name_input'
    
    def confirm_name(self):
        """Confirm the entered name"""
        name = self.input_text.strip()
        if name:
            player_stats.set_player_name(name)
            print(f"👤 Nome definido: {name}")
            return 'main_menu'
        return 'name_input'
    
    def skip_name(self):
        """Skip name input and use default"""
        if not self.player_has_name:
            player_stats.set_player_name("Jogador")
            print("👤 Nome padrão definido: Jogador")
        return 'main_menu'
    
    def update(self, dt):
        """Update cursor blink"""
        self.cursor_timer += dt
        if self.cursor_timer >= self.cursor_blink_speed:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
    
    def draw_button(self, rect, text, color=(60, 60, 60), border_color=(150, 150, 150)):
        """Draw a button"""
        pygame.draw.rect(self.display_surface, color, rect)
        pygame.draw.rect(self.display_surface, border_color, rect, 2)
        
        text_surface = self.font.render(text, True, self.text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.display_surface.blit(text_surface, text_rect)
    
    def draw(self):
        """Draw the name input screen"""
        # Draw background
        self.display_surface.blit(self.background, (0, 0))
        self.display_surface.blit(self.overlay, (0, 0))
        
        # Title
        if self.player_has_name:
            title_text = "BEM-VINDO DE VOLTA!"
            subtitle_text = f"Olá, {player_stats.stats['player_name']}"
        else:
            title_text = "CORRIDA PELA RELÍQUIA"
            subtitle_text = "Digite seu nome para começar"
        
        title_surface = self.title_font.render(title_text, True, self.text_color)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGTH // 2 - 150))
        self.display_surface.blit(title_surface, title_rect)
        
        subtitle_surface = self.small_font.render(subtitle_text, True, self.text_color)
        subtitle_rect = subtitle_surface.get_rect(center=(WIDTH // 2, HEIGTH // 2 - 100))
        self.display_surface.blit(subtitle_surface, subtitle_rect)
        
        if not self.player_has_name:
            # Input box
            input_color = self.input_active_color if self.active else self.input_border_color
            pygame.draw.rect(self.display_surface, self.input_bg_color, self.input_box)
            pygame.draw.rect(self.display_surface, input_color, self.input_box, 2)
            
            # Input text
            display_text = self.input_text
            if self.cursor_visible and self.active:
                display_text += "|"
            
            if display_text:
                text_surface = self.font.render(display_text, True, self.text_color)
                text_rect = text_surface.get_rect(centery=self.input_box.centery, left=self.input_box.left + 10)
                self.display_surface.blit(text_surface, text_rect)
            
            # Placeholder text
            if not self.input_text:
                placeholder_surface = self.small_font.render("Seu nome aqui...", True, (120, 120, 120))
                placeholder_rect = placeholder_surface.get_rect(centery=self.input_box.centery, left=self.input_box.left + 10)
                self.display_surface.blit(placeholder_surface, placeholder_rect)
            
            # Character limit
            limit_text = f"{len(self.input_text)}/{self.max_length}"
            limit_surface = self.small_font.render(limit_text, True, (150, 150, 150))
            limit_rect = limit_surface.get_rect(topleft=(self.input_box.right - 80, self.input_box.bottom + 5))
            self.display_surface.blit(limit_surface, limit_rect)
            
            # Confirm button
            confirm_color = (0, 120, 0) if self.input_text.strip() else (60, 60, 60)
            self.draw_button(self.confirm_button, "CONFIRMAR", confirm_color)
            
            # Skip button
            self.draw_button(self.skip_button, "PULAR", (80, 80, 80))
            
            # Instructions
            instructions = [
                "ENTER - Confirmar",
                "ESC - Pular",
                "BACKSPACE - Apagar"
            ]
            
            y_offset = HEIGTH // 2 + 200
            for instruction in instructions:
                inst_surface = self.small_font.render(instruction, True, (180, 180, 180))
                inst_rect = inst_surface.get_rect(center=(WIDTH // 2, y_offset))
                self.display_surface.blit(inst_surface, inst_rect)
                y_offset += 25
        
        else:
            # Welcome back message
            welcome_text = "Pressione qualquer tecla para continuar"
            welcome_surface = self.small_font.render(welcome_text, True, self.text_color)
            welcome_rect = welcome_surface.get_rect(center=(WIDTH // 2, HEIGTH // 2 + 50))
            self.display_surface.blit(welcome_surface, welcome_rect)
            
            # Show some basic stats
            stats_text = [
                f"Tempo Total: {player_stats.get_formatted_stats()['Tempo Total']}",
                f"Sessões: {player_stats.stats['game_sessions']}",
                f"Fases Completadas: {len(player_stats.stats['levels_completed'])}/4"
            ]
            
            y_offset = HEIGTH // 2 + 100
            for stat in stats_text:
                stat_surface = self.small_font.render(stat, True, (200, 200, 200))
                stat_rect = stat_surface.get_rect(center=(WIDTH // 2, y_offset))
                self.display_surface.blit(stat_surface, stat_rect)
                y_offset += 25
    
    def run(self):
        """Run the name input screen"""
        clock = pygame.time.Clock()
        
        while True:
            dt = clock.tick(60)
            
            events = pygame.event.get()
            result = self.handle_events(events)
            
            if result != 'name_input':
                return result
            
            self.update(dt)
            self.draw()
            pygame.display.flip()