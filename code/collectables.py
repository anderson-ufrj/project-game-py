import pygame
from settings import *
from support import import_folder

class HealthOrbs(pygame.sprite.Sprite):
    def __init__(self, pos,groups):
        super().__init__(groups)

        self.frames = import_folder('../graphics/objects/healthOrbs')
        self.frame_index = 0
        self.animation_speed = 0.12

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, -10)

    def animate(self):
        animation = self.frames

        # Loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # Set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.animate()
class AttackOrbs(pygame.sprite.Sprite):
    def __init__(self, pos,groups):
        super().__init__(groups)

        self.frames = import_folder('../graphics/objects/attackOrbs')
        self.frame_index = 0
        self.animation_speed = 0.12

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, -10)

    def animate(self):
        animation = self.frames

        # Loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # Set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.animate()
class ZappaguriMysticStone(pygame.sprite.Sprite):
    def __init__(self, pos,groups):
        super().__init__(groups)

        self.frames = import_folder('../graphics/objects/EldrichGem')
        self.frame_index = 0
        self.animation_speed = 0.12

        self.image = self.frames[self.frame_index]
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, -10)

    def animate(self):
        animation = self.frames

        # Loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # Set the image
        self.image = animation[int(self.frame_index)]
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.animate()

# Alias para compatibilidade com código existente
EldritchGem = ZappaguriMysticStone

class SpeedOrbs(pygame.sprite.Sprite):
    def __init__(self, pos,groups):
        super().__init__(groups)

        self.frames = import_folder('../graphics/objects/speedOrbs')
        self.frame_index = 0
        self.animation_speed = 0.12

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, -10)

    def animate(self):
        animation = self.frames

        # Loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # Set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.animate()

class Key(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        self.frames = import_folder('../graphics/objects/key')
        self.frame_index = 0
        self.animation_speed = 0.12

        self.image = self.frames[self.frame_index]
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-10, -10)

    def animate(self):
        animation = self.frames

            # Loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

            # Set the image
        self.image = animation[int(self.frame_index)]
        self.image = pygame.transform.scale2x(self.image)
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.animate()



