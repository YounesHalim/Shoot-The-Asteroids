from pygame.sprite import AbstractGroup
import assets
import configs
from game_objects.asteroid import Asteroid
from game_objects.sound import SoundFX
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

    def __init__(self, *groups: AbstractGroup,
                 asteroid: Asteroid,
                 score: Score,
                 scale: tuple = (10, 10)):

        self._layer = Layer.SCORE
        self.sprite_asset = assets.get_sprite('1')
        self.scalex, self.scale_y = scale[0], scale[1]
        self.image = pygame.transform.scale(self.sprite_asset, (self.scalex, self.scale_y))
        self.rect = self.image.get_rect(topright=(asteroid.rect.x + 10, asteroid.rect.y))
        self.__lifetime = configs.FPS
        self.__fade_start = configs.FPS // 2  # Start fading out halfway through the lifetime
        self.__fade_duration = configs.FPS // 10  # Fading duration
        self.__fade_alpha = 255  # Initial opacity
        self.score = score
        self.hit_sound = assets.get_audio(self.__HIT_SOUND_FX)
        self.play()
        self.ast_is_destroyed = asteroid.is_destroyed()
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
            self.score.value += 4
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
