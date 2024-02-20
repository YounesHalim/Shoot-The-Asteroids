import pygame
from pygame.sprite import AbstractGroup

import assets
import configs
from layer import Layer
import random


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup):
        self._layer = Layer.ASTEROID
        self.images = Asteroid.get_asteroids()
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(random.randint(0, configs.SCREEN_WIDTH), 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.animate = 0
        super().__init__(*groups)

    def update(self, *args, **kwargs):
        self.animate += 1
        index = self.animate // 10 % len(self.images)
        self.image = self.images[index]
        self.rect.y += 1
        if self.rect.y >= configs.SCREEN_HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randint(0, configs.SCREEN_WIDTH)

    @staticmethod
    def get_asteroids():
        terminate = False
        counter = 0
        images = []
        while not terminate:
            try:
                file_name = f'Asteroid-A-10-{counter}'
                asteroid_sprite = assets.get_sprite(file_name)
                images.append(asteroid_sprite)
                counter += 1
            except Exception as e:
                print(e)
                terminate = True

        return images
