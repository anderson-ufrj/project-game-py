# ===================================================================================
# SISTEMA DE CHEAT CODES - VERSÃO DE TESTES
# ===================================================================================
# IMPORTANTE: Este arquivo contém códigos de cheat para facilitar os testes.
# Para remover os cheats da versão final:
# 1. Deletar este arquivo (cheat_system.py)
# 2. Remover import "from cheat_system import CheatSystem" dos levels
# 3. Remover chamadas para self.cheat_system nos levels
# 4. Remover os cheats do main.py (linhas comentadas com "# CHEAT:")
# ===================================================================================

import pygame
from font_manager import font_manager
from professional_renderer import professional_renderer

class CheatSystem:
    """Sistema de cheat codes para facilitar testes"""
    
    def __init__(self):
        self.cheats_enabled = True  # Set to False to disable all cheats
        self.cheat_keys = {
            # Normal number keys
            pygame.K_1: "level1",
            pygame.K_2: "level2", 
            pygame.K_3: "level3",
            pygame.K_4: "level4",
            # Keypad number keys (for compatibility)
            pygame.K_KP1: "level1",
            pygame.K_KP2: "level2",
            pygame.K_KP3: "level3",
            pygame.K_KP4: "level4",
            # Other keys
            pygame.K_h: "home",
            pygame.K_F1: "god_mode",
            pygame.K_F2: "max_energy",
        }
        
        # God mode variables
        self.god_mode = False
        self.max_energy_cheat = False
        
    def handle_cheat_input(self, event):
        """Handle cheat key inputs"""
        if not self.cheats_enabled:
            return None
            
        if event.type == pygame.KEYDOWN:
            # Check by key code first
            if event.key in self.cheat_keys:
                cheat_action = self.cheat_keys[event.key]
                return self._execute_cheat(cheat_action)
            
            # Also check by unicode for compatibility
            elif hasattr(event, 'unicode') and event.unicode:
                unicode_key = event.unicode.lower()
                if unicode_key == '1':
                    return self._execute_cheat("level1")
                elif unicode_key == '2':
                    return self._execute_cheat("level2")
                elif unicode_key == '3':
                    return self._execute_cheat("level3")
                elif unicode_key == '4':
                    return self._execute_cheat("level4")
                elif unicode_key == 'h':
                    return self._execute_cheat("home")
        
        return None
    
    def _execute_cheat(self, cheat_action):
        """Execute a cheat action"""
        # Handle special cheats
        if cheat_action == "god_mode":
            self.god_mode = not self.god_mode
            print(f"🎮 CHEAT: God Mode {'ATIVADO' if self.god_mode else 'DESATIVADO'}")
            return None
        elif cheat_action == "max_energy":
            self.max_energy_cheat = not self.max_energy_cheat
            print(f"🎮 CHEAT: Energia Infinita {'ATIVADA' if self.max_energy_cheat else 'DESATIVADA'}")
            return None
        else:
            print(f"🎮 CHEAT: Mudando para {cheat_action}")
            return cheat_action
    
    def apply_god_mode(self, player):
        """Apply god mode effects to player"""
        if self.god_mode:
            player.health = player.stats['health']  # Full health
            player.vulnerable = True  # Reset vulnerability (prevent damage immunity)
            
    def apply_max_energy(self, player):
        """Apply infinite energy cheat"""
        if self.max_energy_cheat:
            player.energy = player.stats['energy']  # Always full energy
    
    def display_cheat_info(self, screen):
        """Display cheat information on screen with modern rendering"""
        if not self.cheats_enabled:
            return
            
        y_offset = 10
        
        # Display active cheats with modern rendering
        if self.god_mode:
            text_surf, text_rect = professional_renderer.render_text_professional(
                "CHEAT: God Mode ATIVO", 'text', (255, 255, 0),
                background=(0, 0, 0), shadow=True, anti_alias=True
            )
            screen.blit(text_surf, (10, y_offset))
            y_offset += 25
            
        if self.max_energy_cheat:
            text_surf, text_rect = professional_renderer.render_text_professional(
                "CHEAT: Energia Infinita ATIVA", 'text', (0, 255, 255),
                background=(0, 0, 0), shadow=True, anti_alias=True
            )
            screen.blit(text_surf, (10, y_offset))
            y_offset += 25
            
        # Display cheat help with modern rendering
        cheat_help = [
            "✅ CHEATS ATIVOS: 1-4 (Fases), H (Home), F1 (God), F2 (Energia)"
        ]
        
        for i, help_text in enumerate(cheat_help):
            text_surf, text_rect = professional_renderer.render_text_professional(
                help_text, 'small', (0, 255, 0),
                background=(0, 0, 0), shadow=True, anti_alias=True
            )
            screen.blit(text_surf, (10, screen.get_height() - 30 + i * 15))

# Global cheat system instance
cheat_system = CheatSystem()