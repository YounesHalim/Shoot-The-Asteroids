import pygame
from pygame.sprite import AbstractGroup

import assets
import configs
from layer import Layer


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup):
        self._layer = Layer.PLAYER
        self.image = assets.get_sprite('spaceship')
        self.rect = self.image.get_rect(topleft=((configs.SCREEN_WIDTH // 2) - 32, configs.SCREEN_HEIGHT - 70))
        self.move = 10
        super().__init__(*groups)

    def update(self, *args, **kwargs):
        self.__handle_movements()
        self.__prevent_deserting()
        self.__handle_shooting()
        pass

    def __handle_movements(self) -> None:
        movements = {
            pygame.K_LEFT: (-self.move, 0),
            pygame.K_RIGHT: (self.move, 0),
            pygame.K_DOWN: (0, self.move),
            pygame.K_UP: (0, -self.move)
        }

        keys = pygame.key.get_pressed()

        for key, (dx, dy) in movements.items():
            if keys[key]:
                self.rect.x += dx
                self.rect.y += dy

    def __prevent_deserting(self):
        if self.rect.left <= 0:
            print(self.rect.left)
            self.rect.left = 0
        elif self.rect.right >= configs.SCREEN_WIDTH:
            print(self.rect.right)
            self.rect.right = configs.SCREEN_WIDTH
        if self.rect.top <= 0:
            print(self.rect.top)
            self.rect.top = 0
        elif self.rect.bottom >= configs.SCREEN_HEIGHT:
            print(self.rect.bottom)
            self.rect.bottom = configs.SCREEN_HEIGHT

    def __handle_shooting(self) -> None:
        movements = {
            pygame.K_SPACE: (-self.move, 0)
        }
        keys = pygame.key.get_pressed()
        for key, (dx, dy) in movements.items():
            if keys[key]:
                print(f'{dx} {dy}')
