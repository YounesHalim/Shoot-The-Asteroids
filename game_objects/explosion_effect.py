import pygame
from pygame.sprite import AbstractGroup

import assets
from layer import Layer


class ExplosionEffect(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup, x, y):
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
            except Exception as e:
                print(e)
                terminate = True

        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_speed = 0
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
