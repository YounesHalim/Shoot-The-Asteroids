from pygame.sprite import AbstractGroup

import assets
import configs
from layer import Layer
import pygame


class Score(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup):
        self._layer = Layer.UI
        self.value = 0
        self.image = pygame.surface.Surface((0, 0), pygame.SRCALPHA)
        self.__create()
        super().__init__(*groups)

    def __create(self):
        self.str_value = str(self.value)
        self.images = []
        self.width = 0

        for str_value_char in self.str_value:
            img = assets.get_sprite(str_value_char)
            self.images.append(img)
            self.width += img.get_width()

        self.height = self.images[0].get_height()
        self.image = pygame.surface.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topright=(configs.SCREEN_WIDTH - 30, 30))

        x = 0
        for img in self.images:
            self.image.blit(img, (x, 0))
            x += img.get_width()

    def update(self):
        self.__create()


class GameMessage(pygame.sprite.Sprite):
    def __init__(self, *groups, sprite_name: str):
        self._layer = Layer.UI
        self.image = assets.get_sprite(sprite_name)
        self.rect = self.image.get_rect(center=(configs.SCREEN_WIDTH / 2, configs.SCREEN_HEIGHT / 2))
        super().__init__(*groups)