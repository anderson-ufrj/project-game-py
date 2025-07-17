import pygame
import sys
from settings import *
from player_stats import player_stats
from datetime import timedelta
from font_manager import font_manager

class StatsScreen:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = font_manager.get('stats')
        self.title_font = font_manager.get('title')
        self.small_font = font_manager.get('small')
        
        # Background
        self.background = pygame.image.load('../graphics/ui/home page.jpg').convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGTH))
        
        # Overlay for better text visibility
        self.overlay = pygame.Surface((WIDTH, HEIGTH))
        self.overlay.set_alpha(200)
        self.overlay.fill((0, 0, 0))
        
        # Colors
        self.text_color = (255, 255, 255)
        self.header_color = (255, 215, 0)  # Gold
        self.value_color = (100, 255, 100)  # Light green
        self.label_color = (200, 200, 200)  # Light gray
        
        # Layout
        self.left_column_x = 100
        self.right_column_x = WIDTH // 2 + 50
        self.start_y = 120
        self.line_height = 30
        
        # Get formatted stats
        self.stats_data = self.get_detailed_stats()
        
    def get_detailed_stats(self):
        """Get detailed statistics for display"""
        stats = player_stats.stats
        
        # Calculate additional stats
        total_orbs = sum(stats["collection_stats"].values())
        total_enemies = sum(stats["combat_stats"]["enemies_by_type"].values())
        total_magic = sum(stats["combat_stats"]["magic_by_type"].values())
        
        # Calculate favorite weapon
        weapon_usage = stats["equipment_stats"]["weapon_usage"]
        favorite_weapon = max(weapon_usage.items(), key=lambda x: x[1])[0] if any(weapon_usage.values()) else "N/A"
        
        # Calculate playtime
        playtime = str(timedelta(seconds=stats["total_playtime"]))
        
        # Best times
        best_times = stats["performance"]["best_times"]
        best_time_str = "N/A"
        if any(t for t in best_times.values() if t is not None):
            best_time = min(t for t in best_times.values() if t is not None)
            best_time_str = f"{int(best_time)}s"
        
        # Completion percentage
        completion = len(stats["levels_completed"]) / 4 * 100
        
        return {
            "basic": {
                "Nome": stats["player_name"],
                "Criado em": stats["created_at"][:10],
                "Última sessão": stats["last_played"][:10],
                "Tempo total": playtime,
                "Sessões": stats["game_sessions"],
                "Progresso": f"{completion:.1f}%"
            },
            "combat": {
                "Inimigos derrotados": total_enemies,
                "Golu derrotados": stats["combat_stats"]["enemies_by_type"]["golu"],
                "Black derrotados": stats["combat_stats"]["enemies_by_type"]["black"],
                "Bigboi derrotados": stats["combat_stats"]["enemies_by_type"]["bigboi"],
                "Dano causado": stats["combat_stats"]["damage_dealt"],
                "Dano recebido": stats["combat_stats"]["damage_taken"],
                "Mortes": stats["combat_stats"]["deaths"],
                "Ataques realizados": stats["combat_stats"]["attacks_made"],
                "Magias lançadas": total_magic
            },
            "collection": {
                "Orbs coletados": total_orbs,
                "Health Orbs": stats["collection_stats"]["health_orbs"],
                "Attack Orbs": stats["collection_stats"]["attack_orbs"],
                "Speed Orbs": stats["collection_stats"]["speed_orbs"],
                "Chaves encontradas": stats["collection_stats"]["keys_found"],
                "Gemas Eldritch": stats["collection_stats"]["eldritch_gems"]
            },
            "performance": {
                "Melhor tempo": best_time_str,
                "Fases completadas": len(stats["levels_completed"]),
                "Tentativas Fase 1": stats["performance"]["attempts_per_level"]["level1"],
                "Tentativas Fase 2": stats["performance"]["attempts_per_level"]["level2"],
                "Tentativas Fase 3": stats["performance"]["attempts_per_level"]["level3"],
                "Tentativas Fase 4": stats["performance"]["attempts_per_level"]["level4"],
                "Arma favorita": favorite_weapon.title()
            }
        }
    
    def draw_section(self, title, data, x, y):
        """Draw a section of statistics"""
        # Draw section title
        title_surface = self.title_font.render(title, True, self.header_color)
        title_rect = title_surface.get_rect(x=x, y=y)
        self.display_surface.blit(title_surface, title_rect)
        
        current_y = y + 40
        
        # Draw each stat in the section
        for label, value in data.items():
            # Draw label
            label_surface = self.small_font.render(f"{label}:", True, self.label_color)
            label_rect = label_surface.get_rect(x=x, y=current_y)
            self.display_surface.blit(label_surface, label_rect)
            
            # Draw value
            value_surface = self.small_font.render(str(value), True, self.value_color)
            value_rect = value_surface.get_rect(x=x + 180, y=current_y)
            self.display_surface.blit(value_surface, value_rect)
            
            current_y += 22
        
        return current_y + 10  # Return next available Y position
    
    def draw_achievements(self, x, y):
        """Draw achievements section"""
        title_surface = self.title_font.render("CONQUISTAS", True, self.header_color)
        title_rect = title_surface.get_rect(x=x, y=y)
        self.display_surface.blit(title_surface, title_rect)
        
        current_y = y + 40
        
        # Get all achievements
        achievements = player_stats.check_achievements()
        
        # Show achievement count
        count_text = f"({len(achievements)}/32 desbloqueadas)"
        count_surface = self.small_font.render(count_text, True, self.label_color)
        count_rect = count_surface.get_rect(x=x + 180, y=y + 5)
        self.display_surface.blit(count_surface, count_rect)
        
        # Draw achievements (limit to 10 for space)
        displayed_achievements = achievements[:10]
        for achievement in displayed_achievements:
            achievement_surface = self.small_font.render(achievement, True, self.value_color)
            achievement_rect = achievement_surface.get_rect(x=x, y=current_y)
            self.display_surface.blit(achievement_surface, achievement_rect)
            current_y += 20
        
        # Show "and more..." if there are more achievements
        if len(achievements) > 10:
            more_text = f"... e mais {len(achievements) - 10} conquistas"
            more_surface = self.small_font.render(more_text, True, self.label_color)
            more_rect = more_surface.get_rect(x=x, y=current_y)
            self.display_surface.blit(more_surface, more_rect)
        
        if not achievements:
            no_achievements_surface = self.small_font.render("Nenhuma conquista ainda", True, self.label_color)
            no_achievements_rect = no_achievements_surface.get_rect(x=x, y=current_y)
            self.display_surface.blit(no_achievements_surface, no_achievements_rect)
    
    def handle_events(self, events):
        """Handle input events"""
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    return 'main_menu'
                elif event.key == pygame.K_r:
                    # Refresh stats
                    self.stats_data = self.get_detailed_stats()
                elif event.key == pygame.K_a:
                    # Go to achievements screen
                    return 'achievements'
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    return 'main_menu'
        
        return 'stats'
    
    def draw(self):
        """Draw the stats screen"""
        # Draw background
        self.display_surface.blit(self.background, (0, 0))
        self.display_surface.blit(self.overlay, (0, 0))
        
        # Title
        title_text = f"ESTATÍSTICAS - {player_stats.stats['player_name'].upper()}"
        title_surface = self.title_font.render(title_text, True, self.text_color)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, 50))
        self.display_surface.blit(title_surface, title_rect)
        
        # Draw sections
        current_y = self.start_y
        
        # Left column
        current_y = self.draw_section("PERFIL", self.stats_data["basic"], self.left_column_x, current_y)
        current_y = self.draw_section("COMBATE", self.stats_data["combat"], self.left_column_x, current_y)
        
        # Right column
        current_y = self.start_y
        current_y = self.draw_section("COLETA", self.stats_data["collection"], self.right_column_x, current_y)
        current_y = self.draw_section("PERFORMANCE", self.stats_data["performance"], self.right_column_x, current_y)
        
        # Achievements at the bottom
        self.draw_achievements(self.left_column_x, current_y + 20)
        
        # Instructions
        instructions = [
            "ESC/ENTER - Voltar ao menu | A - Ver todas as conquistas",
            "R - Atualizar estatísticas | CLIQUE - Voltar ao menu"
        ]
        
        instruction_y = HEIGTH - 80
        for instruction in instructions:
            inst_surface = self.small_font.render(instruction, True, self.label_color)
            inst_rect = inst_surface.get_rect(center=(WIDTH // 2, instruction_y))
            self.display_surface.blit(inst_surface, inst_rect)
            instruction_y += 20
    
    def run(self):
        """Run the stats screen"""
        clock = pygame.time.Clock()
        
        while True:
            dt = clock.tick(60)
            
            events = pygame.event.get()
            result = self.handle_events(events)
            
            if result != 'stats':
                return result
            
            self.draw()
            pygame.display.flip()