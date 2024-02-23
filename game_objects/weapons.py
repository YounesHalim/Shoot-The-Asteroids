import pygame.sprite
from pygame.sprite import AbstractGroup

import assets
from layer import Layer


class LaserBeam(pygame.sprite.Sprite):

    def __init__(self, *groups: AbstractGroup, x=None, y=None):
        self._layer = Layer.WEAPON
        self.image = pygame.transform.scale(assets.get_sprite('beam'), (64, 64))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.fps = 0
        super().__init__(*groups)

    def update(self, *args, **kwargs):
        self.fire_beam()
        pass

    def __throttle(self):
        # Implement throttle behavior for LaserBeam
        pass

    def __ammunition(self) -> None:
        # Implement ammunition tracking for LaserBeam
        pass

    def __reload(self):
        # Implement reloading behavior for LaserBeam
        pass

    def fire_beam(self, ):
        self.rect.y -= 15
        # remove the beam from memory if it's deserting. (going out of the y-axis)
        if self.rect.y <= -self.image.get_height():
            self.kill()
