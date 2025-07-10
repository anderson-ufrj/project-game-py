import pygame
import sys
import os
from datetime import datetime
from settings import *
from save_manager import save_manager

class SaveScreen:
    def __init__(self, mode="load"):
        """
        Tela de Save/Load
        mode: 'save' ou 'load'
        """
        self.display_surface = pygame.display.get_surface()
        self.mode = mode
        self.font = pygame.font.Font('../graphics/font/PressStart2P.ttf', 16)
        self.title_font = pygame.font.Font('../graphics/font/PressStart2P.ttf', 24)
        self.small_font = pygame.font.Font('../graphics/font/PressStart2P.ttf', 12)
        
        # Background
        self.background = pygame.image.load('../graphics/ui/home page.jpg').convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGTH))
        
        # Overlay
        self.overlay = pygame.Surface((WIDTH, HEIGTH))
        self.overlay.set_alpha(200)
        self.overlay.fill((0, 0, 0))
        
        # Colors
        self.text_color = (255, 255, 255)
        self.header_color = (255, 215, 0)  # Gold
        self.selected_color = (100, 255, 100)  # Light green
        self.empty_color = (120, 120, 120)  # Gray
        self.filled_color = (200, 200, 200)  # Light gray
        
        # Layout
        self.selected_slot = 1
        self.save_slots = 5
        self.slot_height = 80
        self.start_y = 150
        
        # Get all saves info
        self.saves_info = save_manager.get_all_saves_info()
        
        # Input handling for save name
        self.input_mode = False
        self.save_name = ""
        self.cursor_visible = True
        self.cursor_timer = 0
        
    def handle_events(self, events):
        """Handle input events"""
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if self.input_mode:
                    # Handle save name input
                    if event.key == pygame.K_RETURN:
                        if self.save_name.strip():
                            return ('save_confirm', self.selected_slot, self.save_name.strip())
                        else:
                            return ('save_confirm', self.selected_slot, None)
                    elif event.key == pygame.K_ESCAPE:
                        self.input_mode = False
                        self.save_name = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.save_name = self.save_name[:-1]
                    else:
                        if len(self.save_name) < 20 and event.unicode.isprintable():
                            self.save_name += event.unicode
                else:
                    # Handle menu navigation
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.selected_slot = max(1, self.selected_slot - 1)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.selected_slot = min(self.save_slots, self.selected_slot + 1)
                    elif event.key == pygame.K_RETURN:
                        if self.mode == "save":
                            # Enter save name input mode
                            self.input_mode = True
                            self.save_name = ""
                        else:
                            # Load selected save
                            save_info = self.saves_info[self.selected_slot - 1]
                            if not save_info.get('is_empty', False):
                                return ('load_confirm', self.selected_slot)
                    elif event.key == pygame.K_DELETE and self.mode == "save":
                        # Delete save
                        save_info = self.saves_info[self.selected_slot - 1]
                        if not save_info.get('is_empty', False):
                            return ('delete_confirm', self.selected_slot)
                    elif event.key == pygame.K_ESCAPE:
                        return 'cancel'
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if not self.input_mode:
                        # Calculate clicked slot
                        mouse_y = event.pos[1]
                        for i in range(self.save_slots):
                            slot_y = self.start_y + i * self.slot_height
                            if slot_y <= mouse_y <= slot_y + self.slot_height - 10:
                                self.selected_slot = i + 1
                                # Double click to confirm
                                if self.mode == "load":
                                    save_info = self.saves_info[self.selected_slot - 1]
                                    if not save_info.get('is_empty', False):
                                        return ('load_confirm', self.selected_slot)
                                else:
                                    self.input_mode = True
                                    self.save_name = ""
                                break
        
        return 'save_screen'
    
    def update(self, dt):
        """Update animations"""
        self.cursor_timer += dt
        if self.cursor_timer >= 500:  # 500ms cursor blink
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
    
    def draw_save_slot(self, slot_num, save_info, y_pos):
        """Draw a single save slot"""
        is_selected = slot_num == self.selected_slot
        is_empty = save_info.get('is_empty', False)
        
        # Slot background
        slot_rect = pygame.Rect(100, y_pos, WIDTH - 200, self.slot_height - 10)
        if is_selected:
            pygame.draw.rect(self.display_surface, (50, 100, 50), slot_rect, border_radius=8)
            pygame.draw.rect(self.display_surface, self.selected_color, slot_rect, 3, border_radius=8)
        else:
            pygame.draw.rect(self.display_surface, (30, 30, 30), slot_rect, border_radius=8)
            pygame.draw.rect(self.display_surface, self.filled_color if not is_empty else self.empty_color, slot_rect, 2, border_radius=8)
        
        # Slot number
        slot_text = f"SLOT {slot_num}"
        slot_surface = self.font.render(slot_text, True, self.header_color)
        slot_rect_text = slot_surface.get_rect(x=slot_rect.x + 20, y=slot_rect.y + 10)
        self.display_surface.blit(slot_surface, slot_rect_text)
        
        if is_empty:
            # Empty slot
            empty_text = "- SLOT VAZIO -"
            empty_surface = self.small_font.render(empty_text, True, self.empty_color)
            empty_rect = empty_surface.get_rect(x=slot_rect.x + 20, y=slot_rect.y + 35)
            self.display_surface.blit(empty_surface, empty_rect)
        else:
            # Filled slot information
            save_name = save_info['save_name']
            save_time = save_info['save_time']
            player_name = save_info['player_name']
            difficulty = save_info['difficulty'].title()
            levels_completed = save_info['levels_completed']
            
            # Save name
            name_surface = self.small_font.render(f"Nome: {save_name}", True, self.text_color)
            name_rect = name_surface.get_rect(x=slot_rect.x + 20, y=slot_rect.y + 35)
            self.display_surface.blit(name_surface, name_rect)
            
            # Player and time info
            info_text = f"Jogador: {player_name} | {save_time} | {difficulty}"
            info_surface = self.small_font.render(info_text, True, self.filled_color)
            info_rect = info_surface.get_rect(x=slot_rect.x + 20, y=slot_rect.y + 50)
            self.display_surface.blit(info_surface, info_rect)
            
            # Progress info
            progress_text = f"Progresso: {levels_completed}/4 fases"
            progress_surface = self.small_font.render(progress_text, True, self.filled_color)
            progress_rect = progress_surface.get_rect(x=slot_rect.x + 400, y=slot_rect.y + 35)
            self.display_surface.blit(progress_surface, progress_rect)
    
    def draw_input_overlay(self):
        """Draw save name input overlay"""
        if not self.input_mode:
            return
        
        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGTH), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.display_surface.blit(overlay, (0, 0))
        
        # Input box
        input_rect = pygame.Rect(WIDTH // 2 - 250, HEIGTH // 2 - 100, 500, 200)
        pygame.draw.rect(self.display_surface, (40, 40, 40), input_rect, border_radius=10)
        pygame.draw.rect(self.display_surface, self.header_color, input_rect, 3, border_radius=10)
        
        # Title
        title_text = "NOME DO SAVE"
        title_surface = self.title_font.render(title_text, True, self.header_color)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGTH // 2 - 60))
        self.display_surface.blit(title_surface, title_rect)
        
        # Input field
        input_field_rect = pygame.Rect(WIDTH // 2 - 200, HEIGTH // 2 - 20, 400, 40)
        pygame.draw.rect(self.display_surface, (60, 60, 60), input_field_rect, border_radius=5)
        pygame.draw.rect(self.display_surface, self.text_color, input_field_rect, 2, border_radius=5)
        
        # Input text
        display_text = self.save_name
        if self.cursor_visible:
            display_text += "|"
        
        if not display_text.replace("|", ""):
            display_text = "Digite o nome do save..."
            text_color = self.empty_color
        else:
            text_color = self.text_color
        
        text_surface = self.font.render(display_text, True, text_color)
        text_rect = text_surface.get_rect(x=input_field_rect.x + 10, y=input_field_rect.y + 10)
        self.display_surface.blit(text_surface, text_rect)
        
        # Instructions
        instructions = [
            "ENTER - Confirmar | ESC - Cancelar",
            "Deixe vazio para nome automático"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_surface = self.small_font.render(instruction, True, self.filled_color)
            inst_rect = inst_surface.get_rect(center=(WIDTH // 2, HEIGTH // 2 + 40 + i * 20))
            self.display_surface.blit(inst_surface, inst_rect)
    
    def draw(self):
        """Draw the save/load screen"""
        # Draw background
        self.display_surface.blit(self.background, (0, 0))
        self.display_surface.blit(self.overlay, (0, 0))
        
        # Title
        title_text = "SALVAR JOGO" if self.mode == "save" else "CARREGAR JOGO"
        title_surface = self.title_font.render(title_text, True, self.header_color)
        title_rect = title_surface.get_rect(center=(WIDTH // 2, 50))
        self.display_surface.blit(title_surface, title_rect)
        
        # Instructions
        if self.mode == "save":
            instructions = [
                "↑↓ - Navegar | ENTER - Salvar | DEL - Deletar",
                "ESC - Cancelar | CLIQUE - Selecionar slot"
            ]
        else:
            instructions = [
                "↑↓ - Navegar | ENTER - Carregar",
                "ESC - Cancelar | CLIQUE - Selecionar slot"
            ]
        
        for i, instruction in enumerate(instructions):
            inst_surface = self.small_font.render(instruction, True, self.filled_color)
            inst_rect = inst_surface.get_rect(center=(WIDTH // 2, 100 + i * 20))
            self.display_surface.blit(inst_surface, inst_rect)
        
        # Draw save slots
        for i in range(self.save_slots):
            slot_num = i + 1
            save_info = self.saves_info[i]
            y_pos = self.start_y + i * self.slot_height
            self.draw_save_slot(slot_num, save_info, y_pos)
        
        # Draw input overlay if in input mode
        self.draw_input_overlay()