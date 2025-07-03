"""
Classe base para entidades que podem lançar feitiços
"""

import pygame
from typing import Optional, Dict, Any, Tuple
from .base import AnimatedGameObject, HealthBar
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.constants import *


class MagicCaster(AnimatedGameObject):
    """Classe base para personagens que podem lançar magia"""
    
    def __init__(self, x: float, y: float, width: int, height: int,
                 health: int, spell_type: SpellType = SpellType.BASIC,
                 sprite_paths: Optional[list] = None):
        super().__init__(x, y, width, height, sprite_paths)
        
        # Atributos de vida
        self.max_health = health
        self.current_health = health
        self.health_bar = HealthBar(width, 8, health)
        self.is_alive = True
        
        # Atributos de magia
        self.spell_type = spell_type
        self.spell_cooldown = 250  # milliseconds
        self.last_spell_time = 0
        self.spell_damage = 20
        self.spell_speed = 8
        self.mana = 100
        self.max_mana = 100
        
        # Estado
        self.is_invulnerable = False
        self.invulnerability_timer = 0
        self.invulnerability_duration = 0
        
        # Efeitos visuais
        self.glow_effect = None
        self.particle_emitter = None
        
    def can_cast_spell(self, current_time: int) -> bool:
        """Verifica se pode lançar um feitiço"""
        return (current_time - self.last_spell_time >= self.spell_cooldown and 
                self.is_alive and self.mana >= self.get_spell_cost())
    
    def get_spell_cost(self) -> int:
        """Retorna o custo de mana do feitiço"""
        spell_costs = {
            SpellType.BASIC: 5,
            SpellType.FIRE: 10,
            SpellType.ICE: 8,
            SpellType.LIGHTNING: 15,
            SpellType.ARCANE: 12,
            SpellType.DARK: 20
        }
        return spell_costs.get(self.spell_type, 5)
    
    def cast_spell(self, target_x: float, target_y: float, current_time: int) -> Optional[Dict[str, Any]]:
        """Lança um feitiço em direção ao alvo"""
        if not self.can_cast_spell(current_time):
            return None
        
        # Calcula direção
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        distance = (dx**2 + dy**2)**0.5
        
        if distance == 0:
            return None
        
        # Normaliza direção
        direction_x = dx / distance
        direction_y = dy / distance
        
        # Atualiza cooldown e mana
        self.last_spell_time = current_time
        self.mana -= self.get_spell_cost()
        
        # Retorna dados do feitiço
        return {
            'x': self.rect.centerx,
            'y': self.rect.centery,
            'dx': direction_x,
            'dy': direction_y,
            'speed': self.spell_speed,
            'damage': self.spell_damage,
            'type': self.spell_type,
            'caster': self
        }
    
    def take_damage(self, damage: int, current_time: int) -> bool:
        """Recebe dano e retorna True se morreu"""
        if self.is_invulnerable or not self.is_alive:
            return False
        
        self.current_health -= damage
        self.health_bar.update(self.current_health)
        
        if self.current_health <= 0:
            self.current_health = 0
            self.is_alive = False
            self.on_death()
            return True
        
        # Ativa invulnerabilidade temporária
        self.become_invulnerable(500, current_time)
        return False
    
    def heal(self, amount: int):
        """Cura o personagem"""
        if self.is_alive:
            self.current_health = min(self.current_health + amount, self.max_health)
            self.health_bar.update(self.current_health)
    
    def restore_mana(self, amount: int):
        """Restaura mana"""
        self.mana = min(self.mana + amount, self.max_mana)
    
    def become_invulnerable(self, duration: int, current_time: int):
        """Torna o personagem invulnerável temporariamente"""
        self.is_invulnerable = True
        self.invulnerability_duration = duration
        self.invulnerability_timer = 0
    
    def update_invulnerability(self, dt: float):
        """Atualiza o estado de invulnerabilidade"""
        if self.is_invulnerable:
            self.invulnerability_timer += dt
            
            if self.invulnerability_timer >= self.invulnerability_duration:
                self.is_invulnerable = False
                self.invulnerability_timer = 0
                self.image.set_alpha(255)
            else:
                # Efeito de piscar
                alpha = 128 + int(128 * abs(pygame.math.Vector2(1, 0).rotate(
                    self.invulnerability_timer * 0.01).x))
                self.image.set_alpha(alpha)
    
    def update(self, dt: float):
        """Atualiza o personagem"""
        super().update_animation(dt)
        self.update_invulnerability(dt)
        
        # Regenera mana lentamente
        if self.mana < self.max_mana:
            self.mana = min(self.mana + 0.1 * dt * 0.001, self.max_mana)
    
    def on_death(self):
        """Chamado quando o personagem morre"""
        pass
    
    def render_health_bar(self, screen: pygame.Surface):
        """Renderiza a barra de vida"""
        if self.is_alive:
            bar_x = self.rect.centerx - self.health_bar.width // 2
            bar_y = self.rect.top - 15
            self.health_bar.render(screen, bar_x, bar_y)
    
    def get_spell_color(self) -> Tuple[int, int, int]:
        """Retorna a cor do feitiço baseado no tipo"""
        spell_colors = {
            SpellType.BASIC: Colors.WHITE,
            SpellType.FIRE: Colors.SPELL_RED,
            SpellType.ICE: Colors.SPELL_BLUE,
            SpellType.LIGHTNING: Colors.SPELL_YELLOW,
            SpellType.ARCANE: Colors.SPELL_PURPLE,
            SpellType.DARK: Colors.PURPLE
        }
        return spell_colors.get(self.spell_type, Colors.WHITE)