import pygame
from pygame.sprite import AbstractGroup

import assets
from game_objects.asteroid import Asteroid
from game_objects.sound import SoundFX
from layer import Layer


class ExplosionFX(pygame.sprite.Sprite, SoundFX):
    __EXPLOSION__SOUND_FX = 'explosion'
    __SPACESHIP_EXPLOSION_SOUND_FX = 'spaceship_explosion'

    def __init__(self, *groups: AbstractGroup, collided):
        self._layer = Layer.EXPLOSION
        self.explosion_speed = 4
        terminate = False
        counter = 1
        self.images = []
        while not terminate:
            try:
                file_name = f'exp{counter}'
                explosion = assets.get_sprite(file_name)
                explosion = pygame.transform.scale(explosion, (130, 130))
                self.images.append(explosion)
                counter += 1
            except KeyError:
                terminate = True
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        x, y = collided.rect.centerx, collided.rect.centery
        self.rect.center = [x, y]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_speed = 0
        self.sound_fx = assets.get_audio(self.__EXPLOSION__SOUND_FX) if type(collided) is Asteroid else assets.get_audio(self.__SPACESHIP_EXPLOSION_SOUND_FX)
        pygame.mixer.music.set_volume(.7)
        self.play()
        super().__init__(*groups)

    def update(self, *args, **kwargs):
        self.__explosion_effect()
        self.__is_complete()

    def __explosion_effect(self):

        # update explosion animation
        self.animation_speed += 1

        if self.animation_speed >= self.explosion_speed and self.index < len(self.images) - 1:
            self.animation_speed = 0
            self.index += 1
            self.image = self.images[self.index]

    def __is_complete(self):
        # if the animation is complete, reset animation index
        if self.index >= len(self.images) - 1 and self.animation_speed >= self.explosion_speed:
            self.kill()

    def play(self):
        self.sound_fx.play()

    def pause(self):
        pass

    def fade_in(self):
        pass

    def fade_out(self):
        pass
