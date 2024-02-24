import random

import pygame
from pygame.sprite import AbstractGroup

import assets
import configs
from layer import Layer


class Asteroid(pygame.sprite.Sprite):

    def __init__(self,
                 *groups: AbstractGroup,
                 asteroid_scale: tuple = (64, 64),
                 x: int = None,
                 y: int = None):

        self._layer = Layer.ASTEROID
        self.images = []
        terminate = False
        counter = 0
        while not terminate:
            try:
                file_name = f'Asteroid-A-10-{counter}'
                asteroid_sprite = assets.get_sprite(file_name)
                self.images.append(pygame.transform.scale(asteroid_sprite, (asteroid_scale[0], asteroid_scale[1])))
                counter += 1
            except KeyError:
                terminate = True

        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(random.randint(0, configs.SCREEN_WIDTH - self.image.get_width()), 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.__health = 100
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
        self.rect.y += 3.5
        if self.rect.y >= configs.SCREEN_HEIGHT:
            self.kill()

    def asteroid_hit(self, damage: int = 30):
        self.__health -= damage
        self.rect.y -= 10.5
        if self.__health <= 0:
            self.kill()

    def get_health(self) -> int:
        return self.__health

    def is_destroyed(self) -> bool:
        return True if self.__health <= 0 else False

