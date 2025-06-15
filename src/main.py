"""
Arquivo principal do jogo Wizarding Duel 2.0 - Versão de teste
"""

import pygame
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.constants import *
from src.entities import Player

class TestGame:
    """Versão básica do jogo para testar a nova estrutura"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Cria jogador de teste
        test_character = CharacterStats.WIZARD_BLUE
        self.player = Player(test_character)
        
        # Grupos de sprites
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        
        print("Jogo inicializado com nova estrutura!")
        print(f"Personagem: {self.player.character_name}")
        print("Controles:")
        print("- WASD/Setas: Movimentar")
        print("- Mouse/Espaço: Atirar")
        print("- Shift: Dash")
        print("- ESC: Sair")
    
    def handle_events(self):
        """Processa eventos"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self, dt):
        """Atualiza o jogo"""
        # Input do jogador
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        current_time = pygame.time.get_ticks()
        
        # Processa input do jogador
        spell_data = self.player.handle_input(keys, mouse_pos, mouse_buttons, current_time)
        
        if spell_data:
            print(f"Feitiço lançado: {spell_data['type']} em direção a {mouse_pos}")
        
        # Atualiza sprites
        self.all_sprites.update(dt)
    
    def render(self):
        """Renderiza o jogo"""
        # Fundo estrelado simples
        self.screen.fill(Colors.DARK_BLUE)
        
        # Desenha algumas estrelas
        for i in range(50):
            x = (i * 47) % SCREEN_WIDTH
            y = (i * 73) % SCREEN_HEIGHT
            intensity = 100 + (i * 13) % 155
            color = (intensity, intensity, intensity)
            pygame.draw.circle(self.screen, color, (x, y), 1)
        
        # Renderiza player
        self.player.render(self.screen)
        
        # HUD básico
        self.render_hud()
        
        pygame.display.flip()
    
    def render_hud(self):
        """Renderiza interface básica"""
        font = pygame.font.Font(None, 36)
        
        # Info do personagem
        text = font.render(f"{self.player.character_name}", True, Colors.GOLD)
        self.screen.blit(text, (20, 20))
        
        # Vida
        health_text = f"Vida: {self.player.current_health}/{self.player.max_health}"
        health_surface = font.render(health_text, True, Colors.WHITE)
        self.screen.blit(health_surface, (20, 60))
        
        # Mana
        mana_text = f"Mana: {int(self.player.mana)}/{self.player.max_mana}"
        mana_surface = font.render(mana_text, True, Colors.CYAN)
        self.screen.blit(mana_surface, (20, 100))
        
        # Combo
        if self.player.combo_counter > 0:
            combo_text = f"Combo: {self.player.combo_counter}x"
            combo_surface = font.render(combo_text, True, Colors.YELLOW)
            self.screen.blit(combo_surface, (20, 140))
        
        # Status de dash
        if self.player.is_dashing:
            dash_surface = font.render("DASH!", True, Colors.ORANGE)
            self.screen.blit(dash_surface, (SCREEN_WIDTH - 150, 20))
        
        # Invulnerabilidade
        if self.player.is_invulnerable:
            inv_surface = font.render("INVULNERÁVEL", True, Colors.GREEN)
            self.screen.blit(inv_surface, (SCREEN_WIDTH - 250, 60))
        
        # Instruções
        instruction_font = pygame.font.Font(None, 24)
        instructions = [
            "WASD/Setas: Mover",
            "Mouse/Espaço: Atirar",
            "Shift: Dash",
            "ESC: Sair"
        ]
        
        for i, instruction in enumerate(instructions):
            inst_surface = instruction_font.render(instruction, True, Colors.WHITE)
            self.screen.blit(inst_surface, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 100 + i * 25))
    
    def run(self):
        """Loop principal do jogo"""
        while self.running:
            dt = self.clock.tick(FPS)
            
            self.handle_events()
            self.update(dt)
            self.render()
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    try:
        game = TestGame()
        game.run()
    except Exception as e:
        print(f"Erro ao executar o jogo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)