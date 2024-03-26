import pygame
from pygame.sprite import AbstractGroup

from game_sys import configs, assets
from game_sys.layer import Layer


class Background(pygame.sprite.Sprite):
    def __init__(self, index, *groups: AbstractGroup):
        self._layer = Layer.BACKGROUND
        bg_name = assets.get_sprite('starfield')
        self.image = pygame.transform.scale(bg_name, (configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))
        self.rect = self.image.get_rect(topleft=(0, configs.SCREEN_HEIGHT * index - configs.SCREEN_HEIGHT))
        super().__init__(*groups)

    def update(self, *args, **kwargs):
        self.rect.y += 1  # Move the background downwards
        if self.rect.top >= configs.SCREEN_HEIGHT:  # If the background goes off the bottom of the screen
            self.rect.y = -configs.SCREEN_HEIGHT  # Reset its position above the screen
