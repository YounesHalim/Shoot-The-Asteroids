import os

import pygame.sprite
from pygame.sprite import AbstractGroup
from pygame.math import Vector2

import assets
import configs
from game_objects.sound import SoundFX
from game_objects.spaceship import Spaceship
from layer import Layer


class LaserBeam(pygame.sprite.Sprite, SoundFX):
    __SOUND_FX = 'beam'

    def __init__(self, *groups: AbstractGroup, obj=None, x=None, y=None):
        self._layer = Layer.WEAPON
        self.object = obj
        self.vel = Vector2(0, 15)
        self.sprite_asset = assets.get_sprite('red-beam')
        self.image = pygame.transform.scale(self.sprite_asset, (64, 90)).convert_alpha()
        self.image = pygame.transform.flip(self.image.copy(), False, True) if not isinstance(self.object,
                                                                                             Spaceship) else self.image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.fps = configs.FPS
        self.sound_fx = assets.get_audio(self.__SOUND_FX)
        self.play()
        super().__init__(*groups)

    def update(self, *args, **kwargs):
        self.fire_beam()
        if self.rect.y >= configs.SCREEN_HEIGHT:
            self.kill()
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
        if isinstance(self.object, Spaceship):
            vel = Vector2(0, -15)
            self.rect.move_ip(vel)
            # remove the beam from memory if it's deserting. (going out of the y-axis)
            if self.rect.y <= -self.image.get_height():
                self.kill()
            return
        else:
            self.rect.move_ip(self.vel)
            if self.rect.y > configs.SCREEN_HEIGHT + self.image.get_height():
                self.kill()
            return

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
