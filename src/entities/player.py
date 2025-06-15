"""
Classe do jogador
"""

import pygame
from typing import Dict, Any, Optional
from .magic_caster import MagicCaster
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.constants import *


class Player(MagicCaster):
    """Classe do personagem controlado pelo jogador"""
    
    def __init__(self, character_data: Dict[str, Any]):
        # Dados do personagem (antes de chamar super().__init__)
        self.character_name = character_data["name"]
        self.base_speed = character_data["speed"]
        self.spell_damage = character_data["spell_damage"]
        self.spell_cooldown = character_data["spell_cooldown"]
        self.character_color = character_data["color"]
        
        # Carrega sprite do personagem
        sprite_path = os.path.join(AssetPaths.CHARACTERS_DIR, character_data["sprite"])
        sprite_paths = [sprite_path] if os.path.exists(sprite_path) else None
        
        super().__init__(
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT - 150,
            width=GameSettings.PLAYER_SIZE[0],
            height=GameSettings.PLAYER_SIZE[1],
            health=character_data["health"],
            spell_type=character_data["spell_type"],
            sprite_paths=sprite_paths
        )
        
        # Atributos de movimento
        self.speed = self.base_speed
        self.dash_cooldown = 1000  # milliseconds
        self.last_dash_time = 0
        self.is_dashing = False
        self.dash_duration = 200
        self.dash_timer = 0
        self.dash_speed_multiplier = 3
        
        # Power-ups ativos
        self.active_powerups = []
        self.shield_active = False
        self.damage_multiplier = 1.0
        self.speed_multiplier = 1.0
        
        # Estatísticas
        self.spells_cast = 0
        self.enemies_defeated = 0
        self.damage_dealt = 0
        self.damage_taken = 0
        
        # Combo system
        self.combo_counter = 0
        self.combo_timer = 0
        self.combo_timeout = 2000  # milliseconds
        self.max_combo = 0
        
        self._create_glow_effect()
    
    def _create_image(self):
        """Cria a imagem do jogador se não houver sprite"""
        if not self.sprites:
            # Cria uma varinha mágica estilizada
            self.image.fill((0, 0, 0, 0))
            
            # Cabo da varinha
            handle_rect = pygame.Rect(
                self.rect.width // 2 - 3,
                self.rect.height // 2,
                6,
                self.rect.height // 2
            )
            pygame.draw.rect(self.image, (139, 69, 19), handle_rect)
            pygame.draw.rect(self.image, (101, 67, 33), handle_rect, 1)
            
            # Núcleo mágico
            core_center = (self.rect.width // 2, self.rect.height // 3)
            pygame.draw.circle(self.image, self.character_color, core_center, 8)
            pygame.draw.circle(self.image, Colors.WHITE, core_center, 5)
            
            # Detalhes dourados
            for i in range(3):
                y = self.rect.height // 2 + i * 8
                pygame.draw.line(self.image, Colors.GOLD,
                               (self.rect.width // 2 - 4, y),
                               (self.rect.width // 2 + 4, y), 1)
    
    def _create_glow_effect(self):
        """Cria efeito de brilho ao redor do jogador"""
        self.glow_surface = pygame.Surface(
            (self.rect.width + 40, self.rect.height + 40),
            pygame.SRCALPHA
        )
        self.glow_timer = 0
    
    def handle_input(self, keys, mouse_pos: tuple, 
                    mouse_buttons: tuple, current_time: int) -> Optional[Dict[str, Any]]:
        """Processa entrada do jogador"""
        # Movimento
        dx = dy = 0
        
        if any(keys[k] for k in Controls.MOVE_LEFT):
            dx = -1
        if any(keys[k] for k in Controls.MOVE_RIGHT):
            dx = 1
        if any(keys[k] for k in Controls.MOVE_UP):
            dy = -1
        if any(keys[k] for k in Controls.MOVE_DOWN):
            dy = 1
        
        # Normaliza movimento diagonal
        if dx != 0 and dy != 0:
            dx *= 0.707
            dy *= 0.707
        
        # Aplica velocidade
        current_speed = self.speed * self.speed_multiplier
        if self.is_dashing:
            current_speed *= self.dash_speed_multiplier
        
        self.velocity.x = dx * current_speed
        self.velocity.y = dy * current_speed
        
        # Dash
        if any(keys[k] for k in Controls.DASH) and self.can_dash(current_time):
            self.dash(current_time)
        
        # Ataque
        spell_data = None
        if mouse_buttons[0] or any(keys[k] for k in Controls.SHOOT):
            spell_data = self.cast_spell(mouse_pos[0], mouse_pos[1], current_time)
            if spell_data:
                self.spells_cast += 1
        
        return spell_data
    
    def can_dash(self, current_time: int) -> bool:
        """Verifica se pode fazer dash"""
        return (not self.is_dashing and 
                current_time - self.last_dash_time >= self.dash_cooldown)
    
    def dash(self, current_time: int):
        """Executa um dash"""
        self.is_dashing = True
        self.dash_timer = 0
        self.last_dash_time = current_time
        self.become_invulnerable(self.dash_duration, current_time)
    
    def update(self, dt: float):
        """Atualiza o jogador"""
        super().update(dt)
        
        # Movimento
        self.move(dt * 0.001)
        
        # Mantém dentro da tela
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Atualiza dash
        if self.is_dashing:
            self.dash_timer += dt
            if self.dash_timer >= self.dash_duration:
                self.is_dashing = False
                self.dash_timer = 0
        
        # Atualiza combo
        if self.combo_counter > 0:
            self.combo_timer += dt
            if self.combo_timer >= self.combo_timeout:
                self.combo_counter = 0
                self.combo_timer = 0
        
        # Atualiza efeito de brilho
        self.glow_timer += dt * 0.001
        
        # Atualiza power-ups
        self.update_powerups(dt)
    
    def update_powerups(self, dt: float):
        """Atualiza power-ups ativos"""
        # Remove power-ups expirados
        self.active_powerups = [p for p in self.active_powerups 
                               if p['timer'] < p['duration']]
        
        # Atualiza timers
        for powerup in self.active_powerups:
            powerup['timer'] += dt
        
        # Reseta multiplicadores
        self.damage_multiplier = 1.0
        self.speed_multiplier = 1.0
        self.shield_active = False
        
        # Aplica efeitos de power-ups ativos
        for powerup in self.active_powerups:
            if powerup['type'] == 'damage':
                self.damage_multiplier *= powerup['multiplier']
            elif powerup['type'] == 'speed':
                self.speed_multiplier *= powerup['multiplier']
            elif powerup['type'] == 'shield':
                self.shield_active = True
    
    def add_combo(self):
        """Adiciona ao contador de combo"""
        self.combo_counter += 1
        self.combo_timer = 0
        self.max_combo = max(self.max_combo, self.combo_counter)
    
    def get_combo_multiplier(self) -> float:
        """Retorna o multiplicador de pontos baseado no combo"""
        if self.combo_counter < 5:
            return 1.0
        elif self.combo_counter < 10:
            return 1.5
        elif self.combo_counter < 20:
            return 2.0
        else:
            return 3.0
    
    def collect_powerup(self, powerup_type: str, duration: int = 5000):
        """Coleta um power-up"""
        powerup_data = {
            'type': powerup_type,
            'duration': duration,
            'timer': 0,
            'multiplier': 2.0
        }
        self.active_powerups.append(powerup_data)
    
    def take_damage(self, damage: int, current_time: int) -> bool:
        """Recebe dano (com proteção de escudo)"""
        if self.shield_active:
            # Escudo bloqueia o dano mas é consumido
            self.active_powerups = [p for p in self.active_powerups 
                                   if p['type'] != 'shield']
            return False
        
        self.damage_taken += damage
        return super().take_damage(damage, current_time)
    
    def render(self, screen: pygame.Surface):
        """Renderiza o jogador com efeitos"""
        # Efeito de brilho
        if self.is_alive:
            self.glow_surface.fill((0, 0, 0, 0))
            glow_intensity = int(128 + 64 * pygame.math.Vector2(1, 0).rotate(
                self.glow_timer * 2).x)
            
            for i in range(3):
                radius = 20 + i * 5
                alpha = glow_intensity // (i + 1)
                color = (*self.character_color, alpha)
                pygame.draw.circle(
                    self.glow_surface,
                    color,
                    (self.glow_surface.get_width() // 2,
                     self.glow_surface.get_height() // 2),
                    radius
                )
            
            glow_rect = self.glow_surface.get_rect(center=self.rect.center)
            screen.blit(self.glow_surface, glow_rect, special_flags=pygame.BLEND_ADD)
        
        # Renderiza o jogador
        screen.blit(self.image, self.rect)
        
        # Renderiza barra de vida
        self.render_health_bar(screen)
        
        # Renderiza indicador de escudo
        if self.shield_active:
            pygame.draw.circle(screen, Colors.CYAN, self.rect.center, 
                             self.rect.width // 2 + 10, 2)