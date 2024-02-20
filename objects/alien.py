import pygame
from pygame.sprite import AbstractGroup
from layer import Layer


class Alien(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup):
        self._layer = Layer.ALIEN

        super().__init__(*groups)

    def update(self, *args, **kwargs):
        pass
