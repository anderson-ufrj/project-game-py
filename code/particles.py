import pygame
import math
import random
from font_manager import font_manager
from professional_renderer import professional_renderer

class CollectParticle(pygame.sprite.Sprite):
    """Particle animation when collecting gems"""
    def __init__(self, pos, groups, color=(255, 255, 100)):
        super().__init__(groups)
        
        # Position and movement
        self.pos = pygame.math.Vector2(pos)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 5)
        self.velocity = pygame.math.Vector2(math.cos(angle) * speed, math.sin(angle) * speed)
        self.gravity = 0.3
        
        # Visual
        self.color = color
        self.size = random.randint(3, 7)
        self.alpha = 255
        self.fade_speed = 10
        
        # Create image
        self.image = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (*self.color, self.alpha), (self.size, self.size), self.size)
        self.rect = self.image.get_rect(center=pos)
        
    def update(self):
        # Movement
        self.velocity.y += self.gravity
        self.pos += self.velocity
        self.rect.center = self.pos
        
        # Fade out
        self.alpha -= self.fade_speed
        if self.alpha <= 0:
            self.kill()
        else:
            # Recreate image with new alpha
            self.image = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (*self.color, int(self.alpha)), (self.size, self.size), self.size)
            # Inner glow
            if self.size > 3:
                pygame.draw.circle(self.image, (*self.color, int(self.alpha * 0.5)), (self.size, self.size), self.size // 2)

class GemCollectAnimation(pygame.sprite.Sprite):
    """Sparkle effect when collecting gems"""
    def __init__(self, pos, groups):
        super().__init__(groups)
        
        self.frame_index = 0
        self.animation_speed = 0.5
        
        # Create sparkle frames
        self.frames = []
        for i in range(8):
            size = 32 + i * 4
            surf = pygame.Surface((size, size), pygame.SRCALPHA)
            
            # Draw star shape
            center = size // 2
            points = []
            for j in range(8):
                angle = j * math.pi / 4
                if j % 2 == 0:
                    radius = size // 2
                else:
                    radius = size // 4
                x = center + math.cos(angle) * radius
                y = center + math.sin(angle) * radius
                points.append((x, y))
            
            alpha = 255 - i * 30
            pygame.draw.polygon(surf, (255, 255, 100, alpha), points)
            pygame.draw.polygon(surf, (255, 255, 255, alpha // 2), points, 2)
            
            self.frames.append(surf)
        
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=pos)
        
    def update(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]
            self.rect = self.image.get_rect(center=self.rect.center)

class DeathParticle(pygame.sprite.Sprite):
    """Particle for enemy death animation"""
    def __init__(self, pos, groups, color=(200, 0, 0)):
        super().__init__(groups)
        
        # Position and movement
        self.pos = pygame.math.Vector2(pos)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(3, 8)
        self.velocity = pygame.math.Vector2(math.cos(angle) * speed, math.sin(angle) * speed - 3)
        self.gravity = 0.5
        
        # Visual
        self.color = color
        self.size = random.randint(4, 10)
        self.alpha = 255
        self.fade_speed = 5
        
        # Create image
        self.image = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (*self.color, self.alpha), (self.size, self.size), self.size)
        self.rect = self.image.get_rect(center=pos)
        
    def update(self):
        # Movement
        self.velocity.y += self.gravity
        self.pos += self.velocity
        self.rect.center = self.pos
        
        # Fade out
        self.alpha -= self.fade_speed
        if self.alpha <= 0:
            self.kill()
        else:
            # Recreate image with new alpha
            self.image = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (*self.color, int(self.alpha)), (self.size, self.size), self.size)

class EnemyDeathAnimation(pygame.sprite.Sprite):
    """Death explosion effect for enemies"""
    def __init__(self, pos, groups, enemy_size=64):
        super().__init__(groups)
        
        self.pos = pos
        self.frame_index = 0
        self.animation_speed = 0.3
        
        # Create explosion frames
        self.frames = []
        for i in range(10):
            size = enemy_size + i * 10
            surf = pygame.Surface((size, size), pygame.SRCALPHA)
            
            # Draw explosion circle
            center = size // 2
            radius = size // 2
            alpha = 200 - i * 20
            
            # Outer ring
            pygame.draw.circle(surf, (255, 100, 0, alpha), (center, center), radius, 5)
            # Inner ring
            pygame.draw.circle(surf, (255, 200, 0, alpha // 2), (center, center), radius - 10, 3)
            # Core
            if i < 5:
                pygame.draw.circle(surf, (255, 255, 200, alpha), (center, center), radius // 3)
            
            self.frames.append(surf)
        
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=pos)
        
    def update(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]
            self.rect = self.image.get_rect(center=self.pos)

class FloatingText(pygame.sprite.Sprite):
    """Texto flutuante dinâmico para coleta de pedras"""
    def __init__(self, pos, groups, text, color=(255, 255, 255), size=20):
        super().__init__(groups)
        
        # Posição e movimento
        self.pos = pygame.math.Vector2(pos)
        self.velocity = pygame.math.Vector2(0, -1.5)  # Move para cima
        self.life_time = 120  # frames de vida
        self.current_life = 0
        
        # Modern text rendering setup
        self.text = text
        self.color = color
        self.alpha = 255
        self.font_size = 'small' if size <= 16 else 'text'  # Map size to font categories
        
        # Efeitos (definir antes de create_text_surface)
        self.scale = 1.0
        self.scale_speed = 0.02
        self.bounce_amplitude = 3
        self.bounce_frequency = 0.1
        
        # Criar surface inicial com renderização moderna
        self.create_text_surface()
        
    def create_text_surface(self):
        """Criar a surface do texto com renderização moderna"""
        # Usar renderização profissional
        text_surf, text_rect = professional_renderer.render_text_professional(
            self.text, 
            self.font_size, 
            self.color,
            shadow=True,
            glow=True,
            anti_alias=True
        )
        
        # Aplicar escala se necessário
        if self.scale != 1.0:
            new_width = int(text_surf.get_width() * self.scale)
            new_height = int(text_surf.get_height() * self.scale)
            text_surf = pygame.transform.scale(text_surf, (new_width, new_height))
        
        # Aplicar transparência
        text_surf.set_alpha(int(self.alpha))
        self.image = text_surf
        self.rect = self.image.get_rect(center=self.pos)
    
    def update(self):
        self.current_life += 1
        
        # Movimento
        # Efeito bounce
        bounce_offset = math.sin(self.current_life * self.bounce_frequency) * self.bounce_amplitude
        self.pos.x += bounce_offset * 0.1
        self.pos.y += self.velocity.y
        
        # Efeito de escala (cresce no início, diminui no final)
        if self.current_life < 20:
            self.scale = 1.0 + (self.current_life / 20) * 0.3  # Cresce até 1.3x
        elif self.current_life > self.life_time - 30:
            remaining = self.life_time - self.current_life
            self.scale = 1.3 * (remaining / 30)  # Diminui até 0
        
        # Efeito de fade out
        life_ratio = 1.0 - (self.current_life / self.life_time)
        self.alpha = 255 * life_ratio
        
        # Atualizar visual
        self.create_text_surface()
        
        # Morrer quando acabar a vida
        if self.current_life >= self.life_time:
            self.kill()

class FireParticle(pygame.sprite.Sprite):
    """Partícula de fogo para inimigos em chamas"""
    def __init__(self, pos, groups):
        super().__init__(groups)
        
        # Position with random offset around enemy
        offset_x = random.randint(-20, 20)
        offset_y = random.randint(-30, 10)
        self.pos = pygame.math.Vector2(pos[0] + offset_x, pos[1] + offset_y)
        
        # Movement - flames rise upward
        self.velocity = pygame.math.Vector2(
            random.uniform(-1, 1),  # Slight horizontal drift
            random.uniform(-3, -1)  # Upward movement
        )
        
        # Visual properties
        self.life_time = random.randint(20, 40)
        self.current_life = 0
        self.size = random.randint(3, 8)
        
        # Fire colors
        self.colors = [
            (255, 255, 100),  # Yellow hot
            (255, 150, 50),   # Orange
            (255, 100, 0),    # Red
            (200, 50, 0)      # Dark red
        ]
        
        self.update_image()
    
    def update_image(self):
        """Update fire particle appearance"""
        # Choose color based on life
        life_ratio = self.current_life / self.life_time
        color_index = min(int(life_ratio * len(self.colors)), len(self.colors) - 1)
        color = self.colors[color_index]
        
        # Create fire particle
        self.image = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        alpha = int(255 * (1 - life_ratio))
        
        # Draw flame particle with gradient
        pygame.draw.circle(self.image, (*color, alpha), (self.size, self.size), self.size)
        if self.size > 3:
            inner_color = (min(255, color[0] + 50), min(255, color[1] + 50), min(255, color[2] + 50))
            pygame.draw.circle(self.image, (*inner_color, alpha), (self.size, self.size), self.size // 2)
        
        self.rect = self.image.get_rect(center=self.pos)
    
    def update(self):
        self.current_life += 1
        
        # Movement
        self.pos += self.velocity
        
        # Update visual
        self.update_image()
        
        # Die when life ends
        if self.current_life >= self.life_time:
            self.kill()

class IceParticle(pygame.sprite.Sprite):
    """Partícula de gelo/água para inimigos congelados"""
    def __init__(self, pos, groups):
        super().__init__(groups)
        
        # Position with random offset around enemy
        offset_x = random.randint(-25, 25)
        offset_y = random.randint(-25, 25)
        self.pos = pygame.math.Vector2(pos[0] + offset_x, pos[1] + offset_y)
        
        # Movement - ice crystals float slowly
        self.velocity = pygame.math.Vector2(
            random.uniform(-0.5, 0.5),  # Gentle drift
            random.uniform(-1, 1)       # Floating motion
        )
        
        # Visual properties
        self.life_time = random.randint(30, 60)
        self.current_life = 0
        self.size = random.randint(2, 6)
        
        # Ice colors
        self.colors = [
            (200, 255, 255),  # Light ice blue
            (150, 220, 255),  # Ice blue
            (100, 200, 255),  # Water blue
            (50, 150, 255)    # Deep blue
        ]
        
        self.update_image()
    
    def update_image(self):
        """Update ice particle appearance"""
        # Choose color based on life
        life_ratio = self.current_life / self.life_time
        color_index = min(int(life_ratio * len(self.colors)), len(self.colors) - 1)
        color = self.colors[color_index]
        
        # Create ice particle
        self.image = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        alpha = int(255 * (1 - life_ratio))
        
        # Draw ice crystal (diamond shape)
        points = [
            (self.size, 0),                    # Top
            (self.size * 2, self.size),        # Right
            (self.size, self.size * 2),        # Bottom
            (0, self.size)                     # Left
        ]
        pygame.draw.polygon(self.image, (*color, alpha), points)
        
        # Inner sparkle
        if self.size > 3:
            inner_color = (255, 255, 255)
            pygame.draw.circle(self.image, (*inner_color, alpha // 2), (self.size, self.size), 1)
        
        self.rect = self.image.get_rect(center=self.pos)
    
    def update(self):
        self.current_life += 1
        
        # Movement
        self.pos += self.velocity
        
        # Update visual
        self.update_image()
        
        # Die when life ends
        if self.current_life >= self.life_time:
            self.kill()

class MagicImpactEffect(pygame.sprite.Sprite):
    """Efeito de impacto quando magia atinge o alvo"""
    def __init__(self, pos, groups, magic_style):
        super().__init__(groups)
        
        self.sprite_type = 'effect'  # Add sprite_type to avoid collision detection
        self.pos = pygame.math.Vector2(pos)
        self.magic_style = magic_style
        self.life_time = 20
        self.current_life = 0
        
        self.update_image()
    
    def update_image(self):
        """Update impact effect appearance"""
        life_ratio = self.current_life / self.life_time
        size = int(30 * (1 - life_ratio))
        alpha = int(255 * (1 - life_ratio))
        
        if size <= 0:
            size = 1
        
        self.image = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        
        if self.magic_style == 'flame':
            # Fire explosion
            colors = [(255, 255, 0), (255, 150, 0), (255, 50, 0)]
            for i, color in enumerate(colors):
                radius = size - i * 3
                if radius > 0:
                    pygame.draw.circle(self.image, (*color, alpha), (size, size), radius)
        else:
            # Ice explosion
            colors = [(255, 255, 255), (200, 255, 255), (100, 200, 255)]
            for i, color in enumerate(colors):
                radius = size - i * 3
                if radius > 0:
                    pygame.draw.circle(self.image, (*color, alpha), (size, size), radius)
        
        self.rect = self.image.get_rect(center=self.pos)
    
    def update(self):
        self.current_life += 1
        self.update_image()
        
        if self.current_life >= self.life_time:
            self.kill()