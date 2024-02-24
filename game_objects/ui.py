from pygame.sprite import AbstractGroup
import assets
import configs
from game_objects.asteroid import Asteroid
from layer import Layer
import pygame


class Score(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup):
        self._layer = Layer.SCORE
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
    asteroids = []

    def __init__(self, *groups, sprite_name: str = 'game_over'):
        self._layer = Layer.GAME_OVER
        self.image = pygame.transform.scale(assets.get_sprite(sprite_name), (300, 300))
        self.rect = self.image.get_rect(center=((configs.SCREEN_WIDTH / 2) + 30, configs.SCREEN_HEIGHT / 2))
        self.last_frame_update = 0
        self.animation_delay = 50
        super().__init__(*groups)


class CounterHitSys(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup, asteroid: Asteroid):
        self._layer = Layer.SCORE
        self.image = pygame.transform.scale(assets.get_sprite('1'), (10, 10))
        self.rect = self.image.get_rect(topright=(asteroid.rect.x + 10, asteroid.rect.y))
        self.last_frame_updated = 0
        self.animation = 300
        super().__init__(*groups)

    def update(self, *args, **kwargs):
        self.__fadeout()

    def __fadeout(self):
        self.rect.y -= 4
        current_time = pygame.time.get_ticks()  # Get the current time
        if current_time - self.last_frame_updated >= self.animation:
            self.kill()
            self.last_frame_updated = current_time
