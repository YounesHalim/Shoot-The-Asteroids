import math
from typing import Union

import pygame
from pygame.math import Vector2
from pygame.sprite import AbstractGroup

import assets
import configs
from game_objects.spaceship import Spaceship
from game_objects.weapons import LaserBeam
from layer import Layer
from random import randint


class AlienSpaceship(pygame.sprite.Sprite):

    def __init__(self, *groups: AbstractGroup, scale_x: int = 64, scale_y: int = 64):
        self._layer = Layer.ALIEN
        self.groups = groups
        self.spaceship: Spaceship = \
            [sprite for sprite in self.groups[0] if hasattr(sprite, '_layer') and sprite._layer == Layer.PLAYER][0]
        self.beams = []
        self.alien_sprite = assets.get_sprite('spaceship')
        self.image = pygame.transform.scale(self.alien_sprite, (scale_x, scale_y)).convert_alpha()
        self.rand_pos = randint(self.image.get_width(), configs.SCREEN_WIDTH - self.image.get_width())
        self.rect = self.image.get_rect(topleft=(self.rand_pos, - self.image.get_height()))
        self.mask = pygame.mask.from_surface(self.image)
        self.spaceship_vector = Vector2(self.spaceship.rect.x, self.spaceship.rect.y)
        self.alien_vector = Vector2(self.rect.x, self.rect.y)
        self.vel = Vector2(0, 0)
        self.counter = 0
        self.distance = 0
        self.speed = 15
        self.encounter_delay = configs.FPS * 4
        self.spaceship_arrived = False
        self.spaceship_health = 100
        self.game_clock = pygame.time.Clock()
        self.delta_time: float = 0.0
        self.previous_time = 0
        self.hit_registration = None
        self.beams = 5
        self.laser_beam: Union[LaserBeam, None] = None
        super().__init__(*groups)

    def update(self, *args, **kwargs):
        self.counter += 1
        if self.counter == configs.FPS * 1 and not self.spaceship_arrived:
            self.counter = 0
            self.alien_vector = Vector2(self.rect.x, self.rect.y)
            self.spaceship_vector = Vector2(self.spaceship.rect.x, self.spaceship.rect.y)
            self.distance = self.__compute_distance()

        self.enemy_encounter()
        self.__encounter_finished()
        # self.__damage(None)
        if self.laser_beam is not None and self.laser_beam.rect.collidepoint(self.spaceship.rect.centerx, self.spaceship.rect.centery):
            self.laser_beam.kill()
            self.spaceship.manage_health()
            self.laser_beam = None

    def __compute_distance(self) -> float:
        return math.sqrt(
            (self.rect.x - self.spaceship.rect.centerx) ** 2 + (self.rect.y - self.spaceship.rect.centery) ** 2)

    def enemy_encounter(self):
        if self.distance != 0:
            if self.distance <= configs.SCREEN_HEIGHT / 2:
                self.rect.x += self.speed * (self.spaceship_vector.x - self.rect.x) / self.distance
                # self.rect.move_ip(Vector2(1, -3))
                self.encounter_delay -= 1.3
                self.attack_player()
                return
            self.rect.x += self.speed * (self.spaceship_vector.x - self.rect.x) / self.distance
            self.rect.y += self.speed * (self.spaceship_vector.y - self.rect.y) / self.distance

    def attack_player(self) -> None:
        self.beams -= .15
        if int(self.beams) == 0:
            self.laser_beam = LaserBeam(self.groups[0], x=self.rect.centerx - self.image.get_width() / 2, y=self.rect.y)
            self.beams = 5

    def __encounter_finished(self):
        if int(self.encounter_delay) == 0:
            self.spaceship_arrived = True
            self.distance = 0
            self.rect.move_ip(Vector2(5, -3))
            self.attack_player()
        if self.rect.right > configs.SCREEN_WIDTH + self.image.get_width():
            self.kill()
            self.encounter_delay = configs.FPS * 4
            self.spaceship_arrived = False

    def damage(self) -> None:
        self.spaceship_health -= 20

    def is_destroyed(self) -> bool:
        return self.spaceship_health <= 0 or not self.alive()

