import pygame
import sys
import math
from settings import *
from player_stats import player_stats
from font_manager import font_manager

class AchievementsScreen:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = font_manager.get('achievement')
        self.title_font = font_manager.get('title')
        self.small_font = font_manager.get('tiny')
        
        # Background
        self.background = pygame.image.load('../graphics/ui/home page.jpg').convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGTH))
        
        # Overlay for better text visibility
        self.overlay = pygame.Surface((WIDTH, HEIGTH), pygame.SRCALPHA)
        self.overlay.set_alpha(200)
        self.overlay.fill((0, 0, 0))
        
        # Colors
        self.text_color = (255, 255, 255)
        self.header_color = (255, 215, 0)  # Gold
        self.unlocked_color = (100, 255, 100)  # Light green
        self.locked_color = (120, 120, 120)  # Gray
        self.description_color = (200, 200, 200)
        
        # Layout
        self.start_x = 50
        self.start_y = 100
        self.column_width = (WIDTH - 100) // 2
        self.line_height = 80
        
        # Scroll variables
        self.scroll_offset = 0
        self.max_scroll = 0
        
        # Get all possible achievements with their requirements
        self.all_achievements = self.get_all_possible_achievements()
        self.unlocked_achievements = player_stats.check_achievements()
        
        # Calculate max scroll based on content
        rows_needed = (len(self.all_achievements) + 1) // 2  # Two columns
        total_height = rows_needed * self.line_height
        screen_available = HEIGTH - 200
        self.max_scroll = max(0, total_height - screen_available)
        
        # Animation
        self.glow_timer = 0
    
    def get_all_possible_achievements(self) -> list:
        """Retorna todas as conquistas possíveis com suas descrições"""
        return [
            ("🏁 Primeiro Passo", "Complete a primeira fase"),
            ("🚀 Em Movimento", "Complete duas fases"),
            ("💪 Quase Lá", "Complete três fases"),
            ("🏆 Campeão", "Complete todas as fases"),
            ("🛡️ Invencível", "Complete uma fase sem morrer"),
            ("💀 Imortal", "Complete o jogo sem morrer"),
            ("⚔️ Caçador", "Derrote 10 inimigos"),
            ("🗡️ Guerreiro", "Derrote 50 inimigos"),
            ("⚡ Devastador", "Derrote 100 inimigos"),
            ("🔥 Lenda", "Derrote 200 inimigos"),
            ("💎 Coletor", "Colete 10 orbs"),
            ("🔮 Colecionador", "Colete 25 orbs"),
            ("💰 Tesouro", "Colete 50 orbs"),
            ("👑 Rei dos Orbs", "Colete 100 orbs"),
            ("⏰ Dedicado", "Jogue por 30 minutos"),
            ("🕐 Persistente", "Jogue por 1 hora"),
            ("⌚ Veterano", "Jogue por 2 horas"),
            ("🚄 Velocista", "Complete uma fase em menos de 2 minutos"),
            ("💨 Relâmpago", "Complete uma fase em menos de 1 minuto"),
            ("💥 Destruidor", "Cause 1000 de dano"),
            ("🌪️ Tempestade", "Cause 5000 de dano"),
            ("🔮 Mago Novato", "Lance 20 magias"),
            ("✨ Feiticeiro", "Lance 50 magias"),
            ("🌟 Arcano", "Lance 100 magias"),
            ("🔄 Habitual", "Jogue 5 sessões"),
            ("📅 Frequente", "Jogue 10 sessões"),
            ("🐉 Caçador de Golus", "Derrote 20 Golus"),
            ("🖤 Sombras Vencidas", "Derrote 15 Blacks"),
            ("👹 Gigante Slayer", "Derrote 5 Bigbois"),
            ("❤️ Curandeiro", "Colete 20 Health Orbs"),
            ("💪 Berserker", "Colete 20 Attack Orbs"),
            ("💨 Corredor", "Colete 20 Speed Orbs")
        ]
    
    def handle_events(self, events):
        """Handle input events"""
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    return 'stats'
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.scroll_offset = max(0, self.scroll_offset - 20)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.scroll_offset = min(self.max_scroll, self.scroll_offset + 20)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    return 'stats'
                elif event.button == 4:  # Scroll up
                    self.scroll_offset = max(0, self.scroll_offset - 30)
                elif event.button == 5:  # Scroll down
                    self.scroll_offset = min(self.max_scroll, self.scroll_offset + 30)
        
        return 'achievements'
    
    def update(self, dt):
        """Update animations"""
        self.glow_timer += dt * 0.003
    
    def draw_achievement_item(self, achievement_name, description, x, y, is_unlocked):
        """Draw a single achievement item"""
        # Determine colors
        if is_unlocked:
            name_color = self.unlocked_color
            desc_color = self.description_color
            bg_alpha = 100
            # Add glow effect for unlocked achievements
            glow_intensity = int(30 + math.sin(self.glow_timer + hash(achievement_name) % 100) * 20)
            bg_color = (50, 100, 50, bg_alpha + glow_intensity)
        else:
            name_color = self.locked_color
            desc_color = (100, 100, 100)
            bg_alpha = 50
            bg_color = (30, 30, 30, bg_alpha)
        
        # Background box
        item_rect = pygame.Rect(x, y, self.column_width - 20, self.line_height - 10)
        bg_surface = pygame.Surface((item_rect.width, item_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surface, bg_color, (0, 0, item_rect.width, item_rect.height), border_radius=8)
        self.display_surface.blit(bg_surface, item_rect.topleft)
        
        # Border
        border_color = self.unlocked_color if is_unlocked else self.locked_color
        pygame.draw.rect(self.display_surface, border_color, item_rect, 2, border_radius=8)
        
        # Achievement name
        name_surface = self.font.render(achievement_name, True, name_color)
        name_rect = name_surface.get_rect(x=x + 10, y=y + 10)
        self.display_surface.blit(name_surface, name_rect)
        
        # Achievement description
        desc_surface = self.small_font.render(description, True, desc_color)
        desc_rect = desc_surface.get_rect(x=x + 10, y=y + 35)
        self.display_surface.blit(desc_surface, desc_rect)
        
        # Lock/unlock indicator
        if is_unlocked:
            indicator_surface = self.small_font.render("✓ DESBLOQUEADA", True, self.unlocked_color)
        else:
            indicator_surface = self.small_font.render("🔒 BLOQUEADA", True, self.locked_color)
        
        indicator_rect = indicator_surface.get_rect(x=x + 10, y=y + 55)
        self.display_surface.blit(indicator_surface, indicator_rect)
    
    def draw(self):
        """Draw the achievements screen"""
        # Draw background
        self.display_surface.blit(self.background, (0, 0))
        self.display_surface.blit(self.overlay, (0, 0))
        
        # Title
        title_text = "TODAS AS CONQUISTAS"
        title_surface = self.title_font.render(title_text, True, self.header_color)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, 50))
        self.display_surface.blit(title_surface, title_rect)
        
        # Progress summary
        unlocked_count = len(self.unlocked_achievements)
        total_count = len(self.all_achievements)
        progress_text = f"{unlocked_count}/{total_count} Conquistas Desbloqueadas ({int(unlocked_count/total_count*100)}%)"
        progress_surface = self.font.render(progress_text, True, self.text_color)
        progress_rect = progress_surface.get_rect(center=(WIDTH // 2, 80))
        self.display_surface.blit(progress_surface, progress_rect)
        
        # Draw achievements in two columns
        current_x = self.start_x
        current_y = self.start_y - self.scroll_offset
        column = 0
        
        for achievement_name, description in self.all_achievements:
            # Check if achievement is unlocked
            is_unlocked = achievement_name in self.unlocked_achievements
            
            # Only draw if visible on screen
            if current_y > -self.line_height and current_y < HEIGTH:
                self.draw_achievement_item(achievement_name, description, current_x, current_y, is_unlocked)
            
            # Move to next position
            column += 1
            if column >= 2:  # Two columns
                column = 0
                current_x = self.start_x
                current_y += self.line_height
            else:
                current_x = self.start_x + self.column_width
        
        # Scroll indicators
        if self.scroll_offset > 0:
            up_arrow = "▲ Mais conquistas acima"
            up_surface = self.small_font.render(up_arrow, True, self.text_color)
            up_rect = up_surface.get_rect(center=(WIDTH // 2, self.start_y - 20))
            self.display_surface.blit(up_surface, up_rect)
        
        if self.scroll_offset < self.max_scroll:
            down_arrow = "▼ Mais conquistas abaixo"
            down_surface = self.small_font.render(down_arrow, True, self.text_color)
            down_rect = down_surface.get_rect(center=(WIDTH // 2, HEIGTH - 60))
            self.display_surface.blit(down_surface, down_rect)
        
        # Instructions
        instructions = [
            "ESC/ENTER - Voltar | ↑↓ ou W/S - Rolar",
            "CLIQUE - Voltar | SCROLL - Rolar conquistas"
        ]
        
        instruction_y = HEIGTH - 40
        for instruction in instructions:
            inst_surface = self.small_font.render(instruction, True, (180, 180, 180))
            inst_rect = inst_surface.get_rect(center=(WIDTH // 2, instruction_y))
            self.display_surface.blit(inst_surface, inst_rect)
            instruction_y += 15
    
    def run(self):
        """Run the achievements screen"""
        clock = pygame.time.Clock()
        
        while True:
            dt = clock.tick(60)
            
            events = pygame.event.get()
            result = self.handle_events(events)
            
            if result != 'achievements':
                return result
            
            self.update(dt)
            self.draw()
            pygame.display.flip()