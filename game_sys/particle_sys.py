import random

import pygame
from pygame.sprite import AbstractGroup

import configs
from layer import Layer


class Particle(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup, pos: tuple):
        self._layer = Layer.PARTICLE
        self.image = pygame.Surface((4, 4))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=pos)
        self.vel = pygame.math.Vector2(random.randint(-1, 1), random.randint(-1, 1))
        while self.vel.length() == 0:  # Check if the length is zero
            self.vel = pygame.math.Vector2(random.randint(-1, 1), random.randint(-1, 1))
        self.vel.normalize_ip()  # Normalize the vector
        self.vel *= random.randint(1, 3)  # Scale the normalized vector
        self.lifetime = configs.FPS  # Lifetime of the particle in frames
        super().__init__(*groups)

    def update(self):
        self.rect.move_ip(self.vel)  # Move the particle
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()  # Remove the particle from the group when its lifetime expires

