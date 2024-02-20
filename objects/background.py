import pygame
from pygame.sprite import AbstractGroup

import assets
import configs
from layer import Layer


class Background(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup):
        self._layer = Layer.BACKGROUND
        self.image = assets.get_sprite('background')
        self.rect = self.image.get_rect(topleft=(configs.SCREEN_WIDTH, 0))
        super().__init__(*groups)

    def update(self, *args, **kwargs):
        pass
