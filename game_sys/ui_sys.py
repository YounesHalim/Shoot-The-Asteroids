from typing import Union, Any

import pygame
from pygame.sprite import AbstractGroup

from game_sys import configs, assets
from game_objects.asteroid import Asteroid
from game_objects.sound import SoundFX
from game_sys.layer import Layer


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

    def counter_sys(self) -> None:
        return self.__create()


class GameMessage(pygame.sprite.Sprite):

    def __init__(self, *groups, sprite_name: str = 'game_over'):
        self._layer = Layer.GAME_OVER
        self.image = pygame.transform.scale(assets.get_sprite(sprite_name), (300, 300))
        self.rect = self.image.get_rect(center=((configs.SCREEN_WIDTH / 2) + 30, configs.SCREEN_HEIGHT / 2))
        super().__init__(*groups)


class CounterHitSys(pygame.sprite.Sprite, SoundFX):
    __COUNTER = 0
    __HIT_SOUND_FX = 'hit'
    __ALIEN_SPACESHIP = 20
    __ASTEROID = 4

    def __init__(self, *groups: AbstractGroup,
                 game_object: Union[Asteroid | Any],
                 score: Score,
                 scale: tuple = (10, 10)):

        self._layer = Layer.SCORE
        self.groups = groups
        self.game_object = game_object
        self.sprite_asset = assets.get_sprite('1')
        self.scalex, self.scale_y = scale[0], scale[1]
        self.image = pygame.transform.scale(self.sprite_asset, (self.scalex, self.scale_y))
        self.rect = self.image.get_rect(topright=(self.game_object.rect.x + 10, self.game_object.rect.y))
        self.__lifetime = configs.FPS
        self.__fade_start = configs.FPS // 2  # Start fading out halfway through the lifetime
        self.__fade_duration = configs.FPS // 10  # Fading duration
        self.__fade_alpha = 255  # Initial opacity
        self.score = score
        self.hit_sound = assets.get_audio(self.__HIT_SOUND_FX)
        self.play()
        self.ast_is_destroyed = self.game_object.is_destroyed()
        self.alien_is_destroyed = self.game_object.is_destroyed()
        self.mask = pygame.mask.from_surface(self.image)

        super().__init__(*groups)

    def update(self, *args, **kwargs):
        self.__fadeout()
        self.__scale_image()

    def __fadeout(self):
        self.__lifetime -= 3
        if self.__lifetime <= self.__fade_start:
            self.__fade_alpha -= 255 / self.__fade_duration
            self.image.set_alpha(max(0, int(self.__fade_alpha)))

        if self.__lifetime <= 0:
            self.kill()
        if self.ast_is_destroyed:
            self.score.value += self.__ASTEROID
            self.ast_is_destroyed = False

    def __scale_image(self):
        self.rect.y -= 1
        self.scalex += 1
        self.scale_y += 1
        self.image = pygame.transform.scale(self.sprite_asset, (self.scalex, self.scale_y))

    def play(self):
        try:
            self.hit_sound.play().set_volume(.3)
        except AttributeError as error:
            print(error)

    def pause(self):
        raise NotImplemented()

    def fade_in(self):
        raise NotImplemented()

    def fade_out(self):
        raise NotImplemented()


class StartGame(pygame.sprite.Sprite):

    def __init__(self, *groups: AbstractGroup):
        self.__fade_duration = configs.FPS
        self.__fade_alpha = 255
        self._layer = Layer.NEW_GAME
        self.images = [
            pygame.transform.scale(assets.get_sprite('enter_white'), (200, 64)),
            pygame.transform.scale(assets.get_sprite('enter_black'), (200, 64))
        ]
        self.index = 0
        self.size = len(self.images)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(configs.SCREEN_WIDTH / 2, configs.SCREEN_HEIGHT / 2))
        self.animation_speed = configs.FPS
        self.groups = groups
        self.counter = 0
        super().__init__(*groups)

    def update(self, *args, **kwargs):
        self.animate()
        pass

    def animate(self):
        self.index += 0.03
        index = int(self.index % self.size)  # Ensures index wraps around the size of images
        alpha = (abs(self.size / 2 - index) / (self.size / 2)) * 255  # Calculate alpha value for fading effect
        self.image = self.images[index].copy()  # Make a copy to avoid modifying original images
        self.image.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)

    def remove_intro_layout(self, gameplay_started: bool) -> None:
        if gameplay_started:
            for sprite in self.groups[0].sprites():
                if hasattr(sprite, '_layer') and sprite.layer == Layer.NEW_GAME:
                    sprite.kill()
                    sprite.remove()
