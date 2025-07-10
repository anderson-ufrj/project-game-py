import pygame
import sys
import math
import random
from settings import *
from player_stats import player_stats
from font_manager import font_manager

class NameInputParticle:
    """Partícula mágica para a tela de entrada de nome"""
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

class NameInputButton:
    """Botão interativo estilizado"""
    def __init__(self, x, y, width, height, text, font, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.action = action
        self.hovered = False
        self.glow_intensity = 0
        
    def update(self, mouse_pos, mouse_click):
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        if self.hovered:
            self.glow_intensity = min(self.glow_intensity + 5, 255)
            if mouse_click:
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

class NameInputBox:
    """Caixa de entrada de texto estilizada"""
    def __init__(self, x, y, width, height, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text = ""
        self.active = True
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_blink_speed = 500
        self.max_length = 20
        self.glow_intensity = 0
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isprintable() and len(self.text) < self.max_length:
                self.text += event.unicode
                
    def update(self, dt):
        # Cursor blink
        self.cursor_timer += dt
        if self.cursor_timer >= self.cursor_blink_speed:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
            
        # Glow effect
        if self.active:
            self.glow_intensity = min(self.glow_intensity + 3, 255)
        else:
            self.glow_intensity = max(self.glow_intensity - 3, 0)
    
    def draw(self, surface):
        # Fundo da caixa de texto
        bg_alpha = 120 + int(self.glow_intensity * 0.2)
        bg_color = (30, 30, 40, bg_alpha)
        
        # Desenhar fundo
        s = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(s, bg_color, (0, 0, self.rect.width, self.rect.height), border_radius=8)
        surface.blit(s, self.rect.topleft)
        
        # Borda brilhante
        border_color = (100, 150, 255, self.glow_intensity) if self.active else (100, 100, 100, 100)
        border_s = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(border_s, border_color, (0, 0, self.rect.width, self.rect.height), 2, border_radius=8)
        surface.blit(border_s, self.rect.topleft)
        
        # Texto
        display_text = self.text
        if self.cursor_visible and self.active:
            display_text += "|"
            
        if display_text:
            text_surface = self.font.render(display_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(centery=self.rect.centery, left=self.rect.left + 15)
            surface.blit(text_surface, text_rect)
        else:
            # Placeholder
            placeholder_surface = self.font.render("Digite seu nome...", True, (120, 120, 120))
            placeholder_rect = placeholder_surface.get_rect(centery=self.rect.centery, left=self.rect.left + 15)
            surface.blit(placeholder_surface, placeholder_rect)

class NameInputScreenV2:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = font_manager.get('input')
        self.title_font = font_manager.get('title')
        self.subtitle_font = font_manager.get('subtitle')
        self.small_font = font_manager.get('small')
        
        # Background - same as main menu
        self.background = pygame.image.load('../graphics/ui/home page.jpg').convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGTH))
        
        # Partículas mágicas
        self.particles = []
        self.particle_spawn_timer = 0
        self.particle_spawn_rate = 10  # partículas por segundo
        
        # Input box
        self.input_box = NameInputBox(WIDTH // 2 - 200, HEIGTH // 2 - 25, 400, 60, self.font)
        
        # Buttons
        self.confirm_button = NameInputButton(WIDTH // 2 - 120, HEIGTH // 2 + 80, 120, 50, "CONFIRMAR", self.subtitle_font, "confirm")
        self.skip_button = NameInputButton(WIDTH // 2 + 20, HEIGTH // 2 + 80, 100, 50, "PULAR", self.subtitle_font, "skip")
        
        # Animation states
        self.title_pulse = 0
        self.subtitle_float = 0
        
        # Check if player already has a name
        self.player_has_name = bool(player_stats.stats["player_name"])
        
        # Welcome back state
        self.welcome_alpha = 0
        self.welcome_growing = True
        
    def spawn_particles(self, dt):
        """Spawn magical particles"""
        self.particle_spawn_timer += dt
        
        if self.particle_spawn_timer >= 1000 / self.particle_spawn_rate:
            # Spawn particles from random locations
            spawn_points = [
                (random.randint(0, WIDTH), HEIGTH + 10),  # Bottom
                (-10, random.randint(0, HEIGTH)),         # Left
                (WIDTH + 10, random.randint(0, HEIGTH)),  # Right
                (random.randint(0, WIDTH), -10)           # Top
            ]
            
            spawn_point = random.choice(spawn_points)
            self.particles.append(NameInputParticle(spawn_point[0], spawn_point[1]))
            self.particle_spawn_timer = 0
    
    def update_particles(self):
        """Update and remove dead particles"""
        self.particles = [particle for particle in self.particles if particle.update()]
        
        # Limit particle count
        if len(self.particles) > 50:
            self.particles = self.particles[-50:]
    
    def handle_events(self, events):
        """Handle input events"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click = True
            
            if event.type == pygame.KEYDOWN:
                if not self.player_has_name:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        return self.confirm_name()
                    elif event.key == pygame.K_ESCAPE:
                        return self.skip_name()
                    else:
                        self.input_box.handle_event(event)
                else:
                    # Welcome back - any key continues
                    return 'main_menu'
        
        # Handle button clicks
        if not self.player_has_name:
            confirm_result = self.confirm_button.update(mouse_pos, mouse_click)
            skip_result = self.skip_button.update(mouse_pos, mouse_click)
            
            if confirm_result == "confirm":
                return self.confirm_name()
            elif skip_result == "skip":
                return self.skip_name()
        elif mouse_click:
            return 'main_menu'
        
        return 'name_input'
    
    def confirm_name(self):
        """Confirm the entered name"""
        name = self.input_box.text.strip()
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
        """Update animations and effects"""
        # Update particles
        self.spawn_particles(dt)
        self.update_particles()
        
        # Update input box
        self.input_box.update(dt)
        
        # Title pulse animation
        self.title_pulse += dt * 0.003
        
        # Subtitle float animation
        self.subtitle_float += dt * 0.002
        
        # Welcome back alpha animation
        if self.player_has_name:
            if self.welcome_growing:
                self.welcome_alpha += dt * 0.3
                if self.welcome_alpha >= 255:
                    self.welcome_alpha = 255
                    self.welcome_growing = False
            else:
                self.welcome_alpha -= dt * 0.1
                if self.welcome_alpha <= 150:
                    self.welcome_alpha = 150
                    self.welcome_growing = True
    
    def draw_animated_title(self, text, y_pos, font, base_color):
        """Draw title with pulse animation"""
        pulse_scale = 1.0 + math.sin(self.title_pulse) * 0.05
        pulse_alpha = int(200 + math.sin(self.title_pulse * 2) * 55)
        
        # Create pulsing effect
        color = (*base_color, min(pulse_alpha, 255))
        
        # Render text
        text_surface = font.render(text, True, base_color)
        original_size = text_surface.get_size()
        
        # Scale text
        new_size = (int(original_size[0] * pulse_scale), int(original_size[1] * pulse_scale))
        scaled_surface = pygame.transform.scale(text_surface, new_size)
        
        # Center and draw
        text_rect = scaled_surface.get_rect(center=(WIDTH // 2, y_pos))
        self.display_surface.blit(scaled_surface, text_rect)
        
        # Add glow effect
        glow_surface = pygame.Surface(new_size, pygame.SRCALPHA)
        glow_color = (*base_color, int(pulse_alpha * 0.3))
        glow_surface.fill(glow_color)
        glow_rect = glow_surface.get_rect(center=(WIDTH // 2, y_pos))
        self.display_surface.blit(glow_surface, glow_rect, special_flags=pygame.BLEND_ADD)
    
    def draw(self):
        """Draw the name input screen"""
        # Draw background
        self.display_surface.blit(self.background, (0, 0))
        
        # Draw magical overlay
        overlay = pygame.Surface((WIDTH, HEIGTH), pygame.SRCALPHA)
        overlay.fill((0, 0, 20, 100))  # Dark blue tint
        self.display_surface.blit(overlay, (0, 0))
        
        # Draw particles
        for particle in self.particles:
            particle.draw(self.display_surface)
        
        if self.player_has_name:
            # Welcome back screen
            self.draw_welcome_back()
        else:
            # New player screen
            self.draw_new_player()
    
    def draw_new_player(self):
        """Draw new player input screen"""
        # Animated title
        self.draw_animated_title("CORRIDA PELA RELÍQUIA", HEIGTH // 2 - 180, self.title_font, (255, 215, 0))
        
        # Floating subtitle
        float_offset = math.sin(self.subtitle_float) * 3
        subtitle_text = "A BUSCA PELA GEMA ELDRITCH"
        subtitle_surface = self.subtitle_font.render(subtitle_text, True, (200, 200, 255))
        subtitle_rect = subtitle_surface.get_rect(center=(WIDTH // 2, HEIGTH // 2 - 130 + float_offset))
        self.display_surface.blit(subtitle_surface, subtitle_rect)
        
        # Instruction text
        instruction_text = "Digite seu nome para começar sua jornada:"
        instruction_surface = self.small_font.render(instruction_text, True, (180, 180, 180))
        instruction_rect = instruction_surface.get_rect(center=(WIDTH // 2, HEIGTH // 2 - 80))
        self.display_surface.blit(instruction_surface, instruction_rect)
        
        # Input box
        self.input_box.draw(self.display_surface)
        
        # Character count
        char_count = f"{len(self.input_box.text)}/20"
        count_surface = self.small_font.render(char_count, True, (150, 150, 150))
        count_rect = count_surface.get_rect(topright=(self.input_box.rect.right - 10, self.input_box.rect.bottom + 10))
        self.display_surface.blit(count_surface, count_rect)
        
        # Buttons
        self.confirm_button.draw(self.display_surface)
        self.skip_button.draw(self.display_surface)
        
        # Instructions
        instructions = [
            "ENTER - Confirmar nome | ESC - Usar nome padrão",
            "BACKSPACE - Apagar | CLIQUE - Usar botões"
        ]
        
        y_offset = HEIGTH // 2 + 160
        for instruction in instructions:
            inst_surface = self.small_font.render(instruction, True, (120, 120, 120))
            inst_rect = inst_surface.get_rect(center=(WIDTH // 2, y_offset))
            self.display_surface.blit(inst_surface, inst_rect)
            y_offset += 25
    
    def draw_welcome_back(self):
        """Draw welcome back screen"""
        # Animated welcome title
        alpha = int(self.welcome_alpha)
        welcome_color = (255, 215, 0)
        
        self.draw_animated_title("BEM-VINDO DE VOLTA!", HEIGTH // 2 - 120, self.title_font, welcome_color)
        
        # Player name with glow
        player_name = player_stats.stats['player_name'].upper()
        name_surface = self.font.render(f"Olá, {player_name}!", True, (100, 255, 100))
        name_rect = name_surface.get_rect(center=(WIDTH // 2, HEIGTH // 2 - 60))
        self.display_surface.blit(name_surface, name_rect)
        
        # Stats preview with floating animation
        float_offset = math.sin(self.subtitle_float) * 2
        stats_text = [
            f"Tempo Total: {player_stats.get_formatted_stats()['Tempo Total']}",
            f"Sessões: {player_stats.stats['game_sessions']}",
            f"Fases Completadas: {len(player_stats.stats['levels_completed'])}/4",
            f"Inimigos Derrotados: {player_stats.stats['combat_stats']['enemies_killed']}"
        ]
        
        y_offset = HEIGTH // 2 - 10
        for i, stat in enumerate(stats_text):
            individual_float = math.sin(self.subtitle_float + i * 0.5) * 1
            stat_surface = self.small_font.render(stat, True, (200, 200, 200))
            stat_rect = stat_surface.get_rect(center=(WIDTH // 2, y_offset + individual_float))
            self.display_surface.blit(stat_surface, stat_rect)
            y_offset += 30
        
        # Continue instruction with pulsing
        pulse_alpha = int(150 + math.sin(self.title_pulse * 3) * 50)
        continue_text = "Pressione qualquer tecla para continuar..."
        continue_surface = self.subtitle_font.render(continue_text, True, (255, 255, 255, pulse_alpha))
        continue_rect = continue_surface.get_rect(center=(WIDTH // 2, HEIGTH // 2 + 140))
        self.display_surface.blit(continue_surface, continue_rect)
    
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