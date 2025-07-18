import pygame
import math
import random
from settings import *
from font_manager import font_manager
from player_stats import player_stats

class NamePopupParticle:
    """Partícula decorativa para o pop-up"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-0.3, 0.3)
        self.vy = random.uniform(-0.5, -0.1)
        self.size = random.uniform(1, 2)
        self.life = random.uniform(80, 120)
        self.max_life = self.life
        self.color = random.choice([
            (138, 43, 226),   # Roxo mágico
            (186, 85, 211),   # Orquídea
            (255, 215, 0),    # Dourado
            (147, 0, 211),    # Violeta
            (255, 182, 193),  # Rosa claro
        ])
        self.oscillation = random.uniform(0, math.pi * 2)
    
    def update(self):
        self.x += self.vx + math.sin(pygame.time.get_ticks() * 0.003 + self.oscillation) * 0.1
        self.y += self.vy
        self.life -= 1
        return self.life > 0
    
    def draw(self, surface):
        if self.life > 0:
            alpha = int(255 * (self.life / self.max_life))
            particle_surface = pygame.Surface((int(self.size * 4), int(self.size * 4)), pygame.SRCALPHA)
            color = (*self.color, alpha)
            pygame.draw.circle(particle_surface, color, 
                             (int(self.size * 2), int(self.size * 2)), int(self.size))
            surface.blit(particle_surface, (int(self.x - self.size * 2), int(self.y - self.size * 2)))

class NamePopup:
    """Pop-up moderno para capturar o nome do jogador"""
    
    def __init__(self, screen):
        self.screen = screen
        self.active = False
        self.name_text = ""
        self.cursor_visible = True
        self.cursor_timer = 0
        self.animation_offset = 0
        self.time = 0
        
        # Partículas decorativas
        self.particles = []
        self.particle_spawn_timer = 0
        
        # Fonts
        self.title_font = font_manager.get('title')
        self.text_font = font_manager.get('text')
        self.button_font = font_manager.get('subtitle')
        
        # Cores modernas e vibrantes
        self.colors = {
            'overlay': (0, 0, 0, 200),
            'popup_bg': (15, 15, 25, 250),
            'popup_border': (138, 43, 226),
            'popup_glow': (186, 85, 211, 80),
            'input_bg': (35, 35, 45, 240),
            'input_border': (100, 100, 120),
            'input_active': (138, 43, 226),
            'input_glow': (186, 85, 211, 100),
            'text': (255, 255, 255),
            'title': (255, 215, 0),
            'subtitle': (200, 200, 220),
            'button_confirm_bg': (34, 139, 34, 240),
            'button_confirm_hover': (50, 205, 50, 240),
            'button_cancel_bg': (220, 20, 60, 240),
            'button_cancel_hover': (255, 69, 0, 240),
            'button_text': (255, 255, 255),
            'accent': (255, 215, 0),
            'particle_colors': [
                (138, 43, 226),   # Roxo mágico
                (186, 85, 211),   # Orquídea
                (255, 215, 0),    # Dourado
                (147, 0, 211),    # Violeta
                (255, 182, 193),  # Rosa claro
            ]
        }
        
        # Dimensões maiores e mais modernas
        self.popup_width = 500
        self.popup_height = 320
        self.popup_x = (WIDTH - self.popup_width) // 2
        self.popup_y = (HEIGTH - self.popup_height) // 2
        
        # Input field maior e mais elegante
        self.input_rect = pygame.Rect(
            self.popup_x + 60, 
            self.popup_y + 160, 
            self.popup_width - 120, 
            50
        )
        
        # Buttons maiores e mais espaçados
        self.confirm_button = pygame.Rect(
            self.popup_x + 80, 
            self.popup_y + 240, 
            140, 
            45
        )
        
        self.cancel_button = pygame.Rect(
            self.popup_x + 280, 
            self.popup_y + 240, 
            140, 
            45
        )
        
        self.hover_button = None
        
    def show(self):
        """Mostra o pop-up"""
        self.active = True
        self.name_text = ""
        self.animation_offset = 50  # Começa fora da tela
        
    def hide(self):
        """Esconde o pop-up"""
        self.active = False
        
    def update_particles(self):
        """Atualiza partículas decorativas melhoradas"""
        # Spawn novas partículas de múltiplas direções
        self.particle_spawn_timer += 1
        if self.particle_spawn_timer > 15:
            # Spawn ao redor das bordas do popup
            spawn_positions = [
                # Bottom
                (random.randint(self.popup_x, self.popup_x + self.popup_width), self.popup_y + self.popup_height + 10),
                # Top
                (random.randint(self.popup_x, self.popup_x + self.popup_width), self.popup_y - 10),
                # Left
                (self.popup_x - 10, random.randint(self.popup_y, self.popup_y + self.popup_height)),
                # Right
                (self.popup_x + self.popup_width + 10, random.randint(self.popup_y, self.popup_y + self.popup_height))
            ]
            
            # Spawn 3-4 partículas por vez para mais densidade
            for _ in range(random.randint(3, 4)):
                x, y = random.choice(spawn_positions)
                self.particles.append(NamePopupParticle(x, y))
            self.particle_spawn_timer = 0
        
        # Atualizar partículas existentes
        self.particles = [p for p in self.particles if p.update()]
        
        # Limitar número de partículas para performance
        if len(self.particles) > 50:
            self.particles = self.particles[-50:]
    
    def handle_event(self, event):
        """Manipula eventos do pop-up"""
        if not self.active:
            return None
            
        mouse_pos = pygame.mouse.get_pos()
        
        # Hover nos botões
        self.hover_button = None
        if self.confirm_button.collidepoint(mouse_pos):
            self.hover_button = 'confirm'
        elif self.cancel_button.collidepoint(mouse_pos):
            self.hover_button = 'cancel'
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                # Confirmar com Enter
                if len(self.name_text.strip()) >= 2:
                    player_stats.stats["player_name"] = self.name_text.strip()
                    player_stats.save_stats()
                    self.hide()
                    return "confirmed"
                    
            elif event.key == pygame.K_ESCAPE:
                # Cancelar com ESC
                self.hide()
                return "cancelled"
                
            elif event.key == pygame.K_BACKSPACE:
                # Apagar caractere
                self.name_text = self.name_text[:-1]
                
            else:
                # Adicionar caractere (apenas letras, números, espaços)
                if event.unicode.isprintable() and len(self.name_text) < 20:
                    self.name_text += event.unicode
                    
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.confirm_button.collidepoint(mouse_pos):
                # Botão confirmar
                if len(self.name_text.strip()) >= 2:
                    player_stats.stats["player_name"] = self.name_text.strip()
                    player_stats.save_stats()
                    self.hide()
                    return "confirmed"
                    
            elif self.cancel_button.collidepoint(mouse_pos):
                # Botão cancelar
                self.hide()
                return "cancelled"
        
        return None
    
    def update(self, dt):
        """Atualiza animações"""
        if not self.active:
            return
            
        self.time += dt
        
        # Animação de entrada
        if self.animation_offset > 0:
            self.animation_offset = max(0, self.animation_offset - dt * 200)
        
        # Cursor piscando
        self.cursor_timer += dt * 1000
        if self.cursor_timer > 500:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
            
        # Partículas
        self.update_particles()
    
    def draw(self):
        """Desenha o pop-up com design moderno"""
        if not self.active:
            return
        
        # Overlay escuro mais suave
        overlay = pygame.Surface((WIDTH, HEIGTH), pygame.SRCALPHA)
        overlay.fill(self.colors['overlay'])
        self.screen.blit(overlay, (0, 0))
        
        # Desenhar partículas atrás do popup
        for particle in self.particles:
            particle.draw(self.screen)
        
        # Posição do popup com animação
        popup_y = self.popup_y - self.animation_offset
        
        # Efeito de glow ao redor do popup
        for i in range(5, 0, -1):
            glow_surface = pygame.Surface((self.popup_width + i*8, self.popup_height + i*8), pygame.SRCALPHA)
            glow_alpha = int(20 * (6-i))
            glow_color = (*self.colors['popup_glow'][:3], glow_alpha)
            pygame.draw.rect(glow_surface, glow_color, 
                           (0, 0, self.popup_width + i*8, self.popup_height + i*8), 
                           border_radius=20+i*2)
            self.screen.blit(glow_surface, (self.popup_x - i*4, popup_y - i*4))
        
        # Fundo do popup com gradiente simulado
        popup_surface = pygame.Surface((self.popup_width, self.popup_height), pygame.SRCALPHA)
        popup_surface.fill(self.colors['popup_bg'])
        
        # Borda principal mais grossa
        pygame.draw.rect(popup_surface, self.colors['popup_border'], 
                        (0, 0, self.popup_width, self.popup_height), 
                        width=3, border_radius=20)
        
        # Borda interna para efeito de profundidade
        pygame.draw.rect(popup_surface, (*self.colors['accent'], 120), 
                        (2, 2, self.popup_width-4, self.popup_height-4), 
                        width=1, border_radius=18)
        
        self.screen.blit(popup_surface, (self.popup_x, popup_y))
        
        # Ícone decorativo (estrela mágica)
        star_center = (self.popup_x + self.popup_width // 2, popup_y + 35)
        self.draw_magic_star(star_center)
        
        # Título com efeito
        title_text = "✨ BEM-VINDO, AVENTUREIRO! ✨"
        title_surface = self.title_font.render(title_text, True, self.colors['title'])
        title_rect = title_surface.get_rect(center=(self.popup_x + self.popup_width // 2, popup_y + 70))
        
        # Sombra do título
        shadow_surface = self.title_font.render(title_text, True, (0, 0, 0, 100))
        shadow_rect = shadow_surface.get_rect(center=(title_rect.centerx + 2, title_rect.centery + 2))
        self.screen.blit(shadow_surface, shadow_rect)
        self.screen.blit(title_surface, title_rect)
        
        # Subtítulo elegante
        subtitle_text = "Digite seu nome para começar a jornada épica:"
        subtitle_surface = self.text_font.render(subtitle_text, True, self.colors['subtitle'])
        subtitle_rect = subtitle_surface.get_rect(center=(self.popup_x + self.popup_width // 2, popup_y + 110))
        self.screen.blit(subtitle_surface, subtitle_rect)
        
        # Campo de input moderno
        input_rect_adjusted = pygame.Rect(
            self.input_rect.x, 
            self.input_rect.y - self.animation_offset, 
            self.input_rect.width, 
            self.input_rect.height
        )
        
        # Efeito de glow no input quando ativo
        if len(self.name_text) > 0:
            for i in range(3, 0, -1):
                glow_rect = pygame.Rect(
                    input_rect_adjusted.x - i*2, 
                    input_rect_adjusted.y - i*2, 
                    input_rect_adjusted.width + i*4, 
                    input_rect_adjusted.height + i*4
                )
                glow_alpha = int(40 * (4-i))
                glow_color = (*self.colors['input_glow'][:3], glow_alpha)
                glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
                pygame.draw.rect(glow_surface, glow_color, (0, 0, glow_rect.width, glow_rect.height), border_radius=12+i)
                self.screen.blit(glow_surface, glow_rect.topleft)
        
        # Fundo do input com gradiente
        input_surface = pygame.Surface((input_rect_adjusted.width, input_rect_adjusted.height), pygame.SRCALPHA)
        input_surface.fill(self.colors['input_bg'])
        self.screen.blit(input_surface, input_rect_adjusted.topleft)
        
        # Borda do input mais elegante
        border_color = self.colors['input_active'] if len(self.name_text) > 0 else self.colors['input_border']
        pygame.draw.rect(self.screen, border_color, input_rect_adjusted, width=3, border_radius=12)
        
        # Texto do input
        if self.name_text:
            text_surface = self.text_font.render(self.name_text, True, self.colors['text'])
            text_x = input_rect_adjusted.x + 10
            text_y = input_rect_adjusted.y + (input_rect_adjusted.height - text_surface.get_height()) // 2
            self.screen.blit(text_surface, (text_x, text_y))
            
            # Cursor
            if self.cursor_visible:
                cursor_x = text_x + text_surface.get_width() + 2
                cursor_y = text_y
                pygame.draw.line(self.screen, self.colors['text'], 
                               (cursor_x, cursor_y), 
                               (cursor_x, cursor_y + text_surface.get_height()), 2)
        else:
            # Placeholder
            placeholder_surface = self.text_font.render("Nome do jogador...", True, (150, 150, 150))
            placeholder_x = input_rect_adjusted.x + 10
            placeholder_y = input_rect_adjusted.y + (input_rect_adjusted.height - placeholder_surface.get_height()) // 2
            self.screen.blit(placeholder_surface, (placeholder_x, placeholder_y))
            
            # Cursor no placeholder
            if self.cursor_visible:
                cursor_x = placeholder_x
                cursor_y = placeholder_y
                pygame.draw.line(self.screen, (150, 150, 150), 
                               (cursor_x, cursor_y), 
                               (cursor_x, cursor_y + placeholder_surface.get_height()), 2)
        
        # Botões
        self.draw_button("CONFIRMAR", self.confirm_button, popup_y, 'confirm')
        self.draw_button("CANCELAR", self.cancel_button, popup_y, 'cancel')
        
        # Dica
        hint_text = f"Mínimo 2 caracteres ({len(self.name_text.strip())}/20)"
        hint_color = self.colors['text'] if len(self.name_text.strip()) >= 2 else (180, 180, 180)
        hint_surface = font_manager.get('small').render(hint_text, True, hint_color)
        hint_rect = hint_surface.get_rect(center=(self.popup_x + self.popup_width // 2, popup_y + self.popup_height - 20))
        self.screen.blit(hint_surface, hint_rect)
    
    def draw_button(self, text, rect, popup_y, button_type):
        """Desenha um botão moderno com efeitos"""
        button_rect = pygame.Rect(rect.x, rect.y - self.animation_offset, rect.width, rect.height)
        
        # Determinar cores baseadas no tipo de botão
        if button_type == 'confirm':
            if len(self.name_text.strip()) >= 2:
                bg_color = self.colors['button_confirm_hover'] if self.hover_button == button_type else self.colors['button_confirm_bg']
                text_color = self.colors['button_text']
                border_color = (50, 205, 50) if self.hover_button == button_type else (34, 139, 34)
                icon = "✓"
            else:
                bg_color = (40, 40, 40, 150)
                text_color = (100, 100, 100)
                border_color = (60, 60, 60)
                icon = "✓"
        else:  # cancel
            bg_color = self.colors['button_cancel_hover'] if self.hover_button == button_type else self.colors['button_cancel_bg']
            text_color = self.colors['button_text']
            border_color = (255, 69, 0) if self.hover_button == button_type else (220, 20, 60)
            icon = "✗"
        
        # Efeito de glow quando hover
        if self.hover_button == button_type and (button_type != 'confirm' or len(self.name_text.strip()) >= 2):
            for i in range(3, 0, -1):
                glow_rect = pygame.Rect(
                    button_rect.x - i*2, 
                    button_rect.y - i*2, 
                    button_rect.width + i*4, 
                    button_rect.height + i*4
                )
                glow_alpha = int(30 * (4-i))
                glow_color = (*border_color[:3], glow_alpha)
                glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
                pygame.draw.rect(glow_surface, glow_color, (0, 0, glow_rect.width, glow_rect.height), border_radius=15+i)
                self.screen.blit(glow_surface, glow_rect.topleft)
        
        # Fundo do botão
        button_surface = pygame.Surface((button_rect.width, button_rect.height), pygame.SRCALPHA)
        button_surface.fill(bg_color)
        self.screen.blit(button_surface, button_rect.topleft)
        
        # Borda do botão mais grossa
        pygame.draw.rect(self.screen, border_color, button_rect, width=3, border_radius=15)
        
        # Borda interna para profundidade
        if self.hover_button == button_type and (button_type != 'confirm' or len(self.name_text.strip()) >= 2):
            pygame.draw.rect(self.screen, (*self.colors['accent'], 80), 
                           (button_rect.x + 2, button_rect.y + 2, button_rect.width - 4, button_rect.height - 4), 
                           width=1, border_radius=13)
        
        # Texto do botão com ícone
        full_text = f"{icon} {text}"
        text_surface = self.button_font.render(full_text, True, text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        
        # Sombra do texto
        if button_type != 'confirm' or len(self.name_text.strip()) >= 2:
            shadow_surface = self.button_font.render(full_text, True, (0, 0, 0, 150))
            shadow_rect = shadow_surface.get_rect(center=(text_rect.centerx + 1, text_rect.centery + 1))
            self.screen.blit(shadow_surface, shadow_rect)
        
        self.screen.blit(text_surface, text_rect)
    
    def draw_magic_star(self, center):
        """Desenha uma estrela mágica decorativa"""
        x, y = center
        size = 8 + math.sin(self.time * 3) * 2  # Pulsante
        
        # Estrela principal (dourada)
        star_points = []
        for i in range(10):
            angle = i * math.pi / 5
            if i % 2 == 0:
                radius = size
            else:
                radius = size * 0.4
            px = x + math.cos(angle) * radius
            py = y + math.sin(angle) * radius
            star_points.append((px, py))
        
        # Sombra da estrela
        shadow_points = [(px + 2, py + 2) for px, py in star_points]
        pygame.draw.polygon(self.screen, (0, 0, 0, 100), shadow_points)
        
        # Estrela principal
        pygame.draw.polygon(self.screen, self.colors['accent'], star_points)
        
        # Brilho central
        pygame.draw.circle(self.screen, (255, 255, 255, 180), (int(x), int(y)), int(size * 0.3))
        
        # Raios de luz
        for i in range(4):
            angle = i * math.pi / 2 + self.time
            end_x = x + math.cos(angle) * (size * 1.5)
            end_y = y + math.sin(angle) * (size * 1.5)
            pygame.draw.line(self.screen, (*self.colors['accent'], 120), (x, y), (end_x, end_y), 2)

# Instância global
name_popup = None

def get_name_popup(screen):
    global name_popup
    if name_popup is None:
        name_popup = NamePopup(screen)
    return name_popup