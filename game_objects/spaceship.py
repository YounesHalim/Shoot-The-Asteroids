import pygame
from pygame.sprite import AbstractGroup

import assets
import configs
from layer import Layer
from abc import ABC, abstractmethod


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup):
        self._layer = Layer.PLAYER
        self.images = [
            pygame.transform.scale(assets.get_sprite('idle'), (100, 100)),
        ]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(topleft=((configs.SCREEN_WIDTH // 2) - 32, configs.SCREEN_HEIGHT - 70))
        self.move = 4
        self.health = 100
        self.state = IdleState(self)
        super().__init__(*groups)

    def __set_spaceship_state(self, state):
        self.state = state

    def update(self, *args, **kwargs):
        self.__handle_movements()
        self.__prevent_deserting()

    def __handle_movements(self) -> None:
        # Get pressed keys
        keys = pygame.key.get_pressed()

        # Check for left and right movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.__set_spaceship_state(TiltLeftState(self))
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.__set_spaceship_state(TiltRightState(self))

        # Check for up and down movement
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.move
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.move

        # Check for exponential movement (up and left)
        # if keys[pygame.K_UP] and keys[pygame.K_LEFT]:
        #     self.rect.x -= self.move * 2
        #     self.rect.y -= self.move * 2

        # If no keys pressed, return to idle state
        if not any(keys):
            self.__set_spaceship_state(IdleState(self))

    def __prevent_deserting(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= configs.SCREEN_WIDTH:
            self.rect.right = configs.SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= configs.SCREEN_HEIGHT:
            self.rect.bottom = configs.SCREEN_HEIGHT

    def decrease_health(self, hit_damage: int = 50):
        self.health -= hit_damage
        if self.health <= 0:
            self.kill()

    def get_health(self):
        return self.health


class SpaceshipState(ABC):
    @abstractmethod
    def fire(self, event=None): ...

    @abstractmethod
    def tilt_wing_left(self, event=None): ...

    @abstractmethod
    def tilt_wing_right(self, event=None): ...

    @abstractmethod
    def idle_state(self, event=None): ...


class FireState(SpaceshipState):

    def __init__(self, spaceship: Spaceship):
        self.spaceship = spaceship

    def tilt_wing_left(self, event=None):
        pass

    def tilt_wing_right(self, event=None):
        pass

    def idle_state(self, event=None):
        pass

    def fire(self, event=None):
        pass


class TiltLeftState(SpaceshipState):

    def __init__(self, spaceship: Spaceship):
        self.spaceship = spaceship
        self.tilt_wing_left()

    def fire(self, event=None): ...

    def tilt_wing_left(self, event=None):
        self.spaceship.image = self.spaceship.image = pygame.transform.scale(assets.get_sprite('tilt_left'), (100, 100))
        self.spaceship.rect.x -= self.spaceship.move

    def tilt_wing_right(self, event=None): ...

    def idle_state(self, event=None): ...


class TiltRightState(SpaceshipState):

    def __init__(self, spaceship: Spaceship):
        self.spaceship = spaceship
        self.tilt_wing_right()

    def fire(self, event=None): ...

    def tilt_wing_left(self, event=None): ...

    def tilt_wing_right(self, event=None):
        self.spaceship.image = pygame.transform.scale(assets.get_sprite('tilt_right'), (100, 100))
        self.spaceship.rect.x += self.spaceship.move

    def idle_state(self, event=None): ...


class IdleState(SpaceshipState):
    def __init__(self, spaceship: Spaceship):
        self.spaceship = spaceship
        self.idle_state()

    def fire(self, event=None): ...

    def tilt_wing_left(self, event=None): ...

    def tilt_wing_right(self, event=None): ...

    def idle_state(self, event=None):
        self.spaceship.image = pygame.transform.scale(assets.get_sprite('idle'), (100, 100))
        self.spaceship.index = 0
