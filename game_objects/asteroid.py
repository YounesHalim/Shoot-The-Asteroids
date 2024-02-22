import random

import pygame
from pygame.sprite import AbstractGroup

import assets
import configs
from layer import Layer


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup, x=None, y=None):
        self._layer = Layer.ASTEROID
        self.images = []
        terminate = False
        counter = 0
        while not terminate:
            try:
                file_name = f'Asteroid-A-10-{counter}'
                asteroid_sprite = assets.get_sprite(file_name)
                self.images.append(asteroid_sprite)
                counter += 1
            except KeyError:
                terminate = True

        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(random.randint(0, configs.SCREEN_WIDTH - self.image.get_width()), 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_speed = 0
        super().__init__(*groups)

    def update(self, *args, **kwargs):
        self.__animate_asteroid()
        self.__asteroid_drop()

    def __animate_asteroid(self):
        self.animation_speed += 10
        index = self.animation_speed // 10 % len(self.images)
        self.image = self.images[index]

    def __asteroid_drop(self):
        self.rect.y += 2
        if self.rect.y >= configs.SCREEN_HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randint(0, configs.SCREEN_WIDTH - self.image.get_width())
