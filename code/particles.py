import pygame
import math
import random

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
        
        # Criar fonte
        try:
            self.font = pygame.font.Font('../graphics/font/PressStart2P.ttf', size)
        except:
            self.font = pygame.font.Font(None, size)
        
        # Criar texto
        self.text = text
        self.color = color
        self.alpha = 255
        
        # Efeitos (definir antes de create_text_surface)
        self.scale = 1.0
        self.scale_speed = 0.02
        self.bounce_amplitude = 3
        self.bounce_frequency = 0.1
        
        # Criar surface inicial
        self.create_text_surface()
        
    def create_text_surface(self):
        """Criar a surface do texto com alpha"""
        # Criar texto base
        text_surf = self.font.render(self.text, True, self.color)
        
        # Aplicar escala se necessário
        if self.scale != 1.0:
            new_width = int(text_surf.get_width() * self.scale)
            new_height = int(text_surf.get_height() * self.scale)
            text_surf = pygame.transform.scale(text_surf, (new_width, new_height))
        
        # Criar surface com alpha
        self.image = pygame.Surface(text_surf.get_size(), pygame.SRCALPHA)
        self.image.set_alpha(int(self.alpha))
        self.image.blit(text_surf, (0, 0))
        
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