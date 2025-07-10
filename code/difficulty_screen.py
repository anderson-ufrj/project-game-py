import pygame
import sys
import math
from settings import *
from difficulty_manager import difficulty_manager
from font_manager import font_manager

class DifficultyButton:
    """Botão de seleção de dificuldade"""
    def __init__(self, x, y, width, height, difficulty_key, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.difficulty_key = difficulty_key
        self.font = font
        self.hovered = False
        self.selected = False
        self.glow_intensity = 0
        self.pulse_timer = 0
        
        # Obter dados da dificuldade
        self.difficulty_data = difficulty_manager.get_all_difficulties()[difficulty_key]
        
    def update(self, mouse_pos, mouse_click, current_difficulty):
        self.hovered = self.rect.collidepoint(mouse_pos)
        self.selected = (self.difficulty_key == current_difficulty)
        self.pulse_timer += 0.05
        
        if self.hovered:
            self.glow_intensity = min(self.glow_intensity + 5, 255)
            if mouse_click:
                return self.difficulty_key
        else:
            self.glow_intensity = max(self.glow_intensity - 5, 0)
            
        return None
    
    def draw(self, surface):
        # Base color da dificuldade
        base_color = self.difficulty_data["color"]
        
        # Efeito de seleção
        if self.selected:
            pulse_intensity = int(50 + math.sin(self.pulse_timer) * 30)
            border_color = (255, 255, 255, pulse_intensity)
            border_width = 4
        else:
            border_color = base_color
            border_width = 2
        
        # Fundo do botão
        bg_alpha = 120 + int(self.glow_intensity * 0.3)
        if self.hovered:
            bg_color = (*base_color, bg_alpha + 50)
        elif self.selected:
            bg_color = (*base_color, bg_alpha + 30)
        else:
            bg_color = (50, 50, 80, bg_alpha)
            
        # Desenhar fundo
        bg_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surface, bg_color, (0, 0, self.rect.width, self.rect.height), border_radius=15)
        surface.blit(bg_surface, self.rect.topleft)
        
        # Borda
        border_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(border_surface, border_color, (0, 0, self.rect.width, self.rect.height), 
                        border_width, border_radius=15)
        surface.blit(border_surface, self.rect.topleft)
        
        # Título da dificuldade
        title_color = (255, 255, 255) if not self.hovered else (255, 255, 255)
        title_surface = self.font.render(self.difficulty_data["name"], True, title_color)
        title_rect = title_surface.get_rect(center=(self.rect.centerx, self.rect.y + 25))
        surface.blit(title_surface, title_rect)
        
        # Descrição
        desc_font = pygame.font.Font('../graphics/font/PressStart2P.ttf', 10)
        desc_surface = desc_font.render(self.difficulty_data["description"], True, (200, 200, 200))
        desc_rect = desc_surface.get_rect(center=(self.rect.centerx, self.rect.y + 50))
        surface.blit(desc_surface, desc_rect)
        
        # Indicador de seleção
        if self.selected:
            indicator_text = "SELECIONADO"
            indicator_surface = desc_font.render(indicator_text, True, (100, 255, 100))
            indicator_rect = indicator_surface.get_rect(center=(self.rect.centerx, self.rect.bottom - 20))
            surface.blit(indicator_surface, indicator_rect)

class DifficultyScreen:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = font_manager.get('button')
        self.title_font = font_manager.get('title')
        self.small_font = font_manager.get('small')
        
        # Background
        self.background = pygame.image.load('../graphics/ui/home page.jpg').convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGTH))
        
        # Overlay
        self.overlay = pygame.Surface((WIDTH, HEIGTH), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 40, 160))
        
        # Botões de dificuldade
        self.buttons = []
        button_width = 200
        button_height = 100
        start_x = WIDTH // 2 - (len(difficulty_manager.get_all_difficulties()) * button_width + 
                              (len(difficulty_manager.get_all_difficulties()) - 1) * 50) // 2
        
        difficulties = list(difficulty_manager.get_all_difficulties().keys())
        for i, difficulty in enumerate(difficulties):
            x = start_x + i * (button_width + 50)
            y = HEIGTH // 2 - 50
            self.buttons.append(DifficultyButton(x, y, button_width, button_height, difficulty, self.font))
        
        # Botão confirmar
        self.confirm_button = pygame.Rect(WIDTH // 2 - 100, HEIGTH // 2 + 120, 200, 50)
        self.confirm_hovered = False
        self.confirm_glow = 0
        
        # Área de estatísticas
        self.stats_area = pygame.Rect(50, HEIGTH // 2 + 200, WIDTH - 100, 150)
        
    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 'main_menu'
                elif event.key == pygame.K_RETURN:
                    return 'confirm'
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.cycle_difficulty(-1)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.cycle_difficulty(1)
        
        # Update buttons
        current_difficulty = difficulty_manager.get_current_difficulty()
        for button in self.buttons:
            result = button.update(mouse_pos, mouse_click, current_difficulty)
            if result:
                difficulty_manager.set_difficulty(result)
        
        # Update confirm button
        self.confirm_hovered = self.confirm_button.collidepoint(mouse_pos)
        if self.confirm_hovered:
            self.confirm_glow = min(self.confirm_glow + 5, 255)
            if mouse_click:
                return 'confirm'
        else:
            self.confirm_glow = max(self.confirm_glow - 5, 0)
        
        return 'difficulty'
    
    def cycle_difficulty(self, direction):
        """Alterna dificuldade com teclado"""
        difficulties = list(difficulty_manager.get_all_difficulties().keys())
        current_index = difficulties.index(difficulty_manager.get_current_difficulty())
        new_index = (current_index + direction) % len(difficulties)
        difficulty_manager.set_difficulty(difficulties[new_index])
    
    def draw_confirm_button(self):
        """Desenha o botão de confirmação"""
        # Fundo
        bg_alpha = 120 + int(self.confirm_glow * 0.3)
        if self.confirm_hovered:
            bg_color = (100, 150, 100, bg_alpha)
            border_color = (150, 255, 150)
        else:
            bg_color = (50, 80, 50, bg_alpha)
            border_color = (100, 150, 100)
        
        # Desenhar fundo
        bg_surface = pygame.Surface((self.confirm_button.width, self.confirm_button.height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surface, bg_color, (0, 0, self.confirm_button.width, self.confirm_button.height), 
                        border_radius=10)
        self.display_surface.blit(bg_surface, self.confirm_button.topleft)
        
        # Borda
        pygame.draw.rect(self.display_surface, border_color, self.confirm_button, 2, border_radius=10)
        
        # Texto
        text_color = (255, 255, 255) if not self.confirm_hovered else (200, 255, 200)
        text_surface = self.font.render("CONFIRMAR", True, text_color)
        text_rect = text_surface.get_rect(center=self.confirm_button.center)
        self.display_surface.blit(text_surface, text_rect)
    
    def draw_stats_panel(self):
        """Desenha o painel de estatísticas da dificuldade"""
        # Fundo do painel
        panel_surface = pygame.Surface((self.stats_area.width, self.stats_area.height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surface, (0, 0, 0, 150), (0, 0, self.stats_area.width, self.stats_area.height), 
                        border_radius=10)
        self.display_surface.blit(panel_surface, self.stats_area.topleft)
        
        # Borda
        pygame.draw.rect(self.display_surface, (100, 100, 100), self.stats_area, 2, border_radius=10)
        
        # Título
        title_text = "MODIFICAÇÕES DA DIFICULDADE:"
        title_surface = self.small_font.render(title_text, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.stats_area.centerx, self.stats_area.y + 20))
        self.display_surface.blit(title_surface, title_rect)
        
        # Estatísticas
        stats = difficulty_manager.get_stats_summary()
        y_offset = self.stats_area.y + 50
        
        # Dividir em duas colunas
        items = list(stats.items())
        left_column = items[:len(items)//2]
        right_column = items[len(items)//2:]
        
        # Coluna esquerda
        for stat_name, stat_value in left_column:
            stat_text = f"{stat_name}: {stat_value}"
            color = (200, 255, 200) if "+" in stat_value else (255, 200, 200) if "-" in stat_value else (255, 255, 255)
            stat_surface = self.small_font.render(stat_text, True, color)
            self.display_surface.blit(stat_surface, (self.stats_area.x + 20, y_offset))
            y_offset += 20
        
        # Coluna direita
        y_offset = self.stats_area.y + 50
        for stat_name, stat_value in right_column:
            stat_text = f"{stat_name}: {stat_value}"
            color = (200, 255, 200) if "+" in stat_value else (255, 200, 200) if "-" in stat_value else (255, 255, 255)
            stat_surface = self.small_font.render(stat_text, True, color)
            self.display_surface.blit(stat_surface, (self.stats_area.centerx + 20, y_offset))
            y_offset += 20
    
    def draw(self):
        """Desenha a tela de dificuldade"""
        # Background
        self.display_surface.blit(self.background, (0, 0))
        self.display_surface.blit(self.overlay, (0, 0))
        
        # Título
        title_text = "SELECIONAR DIFICULDADE"
        title_surface = self.title_font.render(title_text, True, (255, 215, 0))
        title_rect = title_surface.get_rect(center=(WIDTH // 2, 100))
        self.display_surface.blit(title_surface, title_rect)
        
        # Subtítulo
        subtitle_text = f"Atual: {difficulty_manager.get_current_name()}"
        subtitle_surface = self.font.render(subtitle_text, True, difficulty_manager.get_current_color())
        subtitle_rect = subtitle_surface.get_rect(center=(WIDTH // 2, 140))
        self.display_surface.blit(subtitle_surface, subtitle_rect)
        
        # Botões de dificuldade
        for button in self.buttons:
            button.draw(self.display_surface)
        
        # Botão confirmar
        self.draw_confirm_button()
        
        # Painel de estatísticas
        self.draw_stats_panel()
        
        # Instruções
        instructions = [
            "CLIQUE - Selecionar dificuldade",
            "A/D ou ←/→ - Navegar",
            "ENTER - Confirmar | ESC - Voltar"
        ]
        
        y_offset = HEIGTH - 80
        for instruction in instructions:
            inst_surface = self.small_font.render(instruction, True, (180, 180, 180))
            inst_rect = inst_surface.get_rect(center=(WIDTH // 2, y_offset))
            self.display_surface.blit(inst_surface, inst_rect)
            y_offset += 20
    
    def run(self):
        """Executa a tela de dificuldade"""
        clock = pygame.time.Clock()
        
        while True:
            events = pygame.event.get()
            result = self.handle_events(events)
            
            if result != 'difficulty':
                return result
            
            self.draw()
            pygame.display.flip()
            clock.tick(60)