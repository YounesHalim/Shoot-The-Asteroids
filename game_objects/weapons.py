import os

import pygame.sprite
from pygame.sprite import AbstractGroup

import assets
import configs
from game_objects.sound import SoundFX
from layer import Layer


class LaserBeam(pygame.sprite.Sprite, SoundFX):

    __SOUND_FX = 'beam'

    def __init__(self, *groups: AbstractGroup, x=None, y=None):
        self._layer = Layer.WEAPON
        self.image = pygame.transform.scale(assets.get_sprite('red-beam'), (64, 90))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.fps = configs.FPS
        self.sound_fx = assets.get_audio(self.__SOUND_FX)
        self.play()
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

    def play(self):
        try:
            self.sound_fx.play().set_volume(.5)
        except AttributeError:
            pass

    def pause(self):
        raise NotImplemented()

    def fade_in(self):
        raise NotImplemented()

    def fade_out(self):
        raise NotImplemented()

