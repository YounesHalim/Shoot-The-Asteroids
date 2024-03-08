import random

import pygame
from pygame.sprite import AbstractGroup
from pygame.math import Vector2

import assets
import configs
from layer import Layer


class Asteroid(pygame.sprite.Sprite):
    __COUNTER = 2
    __ASTEROIDS = []

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
        self.vel = Vector2(random.randint(-4, 1), 3.5)
        self.mask = pygame.mask.from_surface(self.image)
        self.__health = 100
        self.counter = 0
        self.animation_speed = 0
        self.delay = configs.FPS // 3
        super().__init__(*groups)

    def update(self, *args, **kwargs):
        self.__animate_asteroid()

    def __animate_asteroid(self):
        self.animation_speed += 10
        index = self.animation_speed // 10 % len(self.images)
        self.image = self.images[index]
        self.mask = pygame.mask.from_surface(self.image)

    def __asteroid_drop(self):
        self.rect.y += 3.5
        if self.rect.y >= configs.SCREEN_HEIGHT:
            self.kill()

    def asteroid_hit(self, damage: int = 30):
        self.__health -= damage
        self.vel.rotate(40)
        if self.__health <= 0:
            self.kill()

    def get_health(self) -> int:
        return self.__health

    def is_destroyed(self) -> bool:
        return True if self.__health <= 0 else False

    def asteroid_behavior(self, asteroids: list):
        self.rect.move_ip(self.vel)

        if self.rect.x <= 0 or self.rect.x > configs.SCREEN_WIDTH - self.image.get_width():
            self.vel.reflect_ip(Vector2(-3, 0))
            # print('Wall hit')

        if self.rect.bottom >= configs.SCREEN_HEIGHT or self.rect.top == 0:
            self.counter += 1
            self.vel.y += 1
            self.vel.reflect_ip(Vector2(0, 3))
            # print('bottom hit!')

        if self.rect.top <= 0:
            self.counter += 1
            self.vel.y += 1
            self.vel.reflect_ip(Vector2(0, -3))
            # print('top hit')

        if self.counter > self.__COUNTER:
            # print('Hi !')
            self.kill()
            asteroids.remove(self)
