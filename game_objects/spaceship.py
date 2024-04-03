from typing import Union

import pygame
from pygame.sprite import AbstractGroup
from pygame.math import Vector2

from game_sys import configs, assets
from game_sys.explosion_fx_sys import ExplosionFX
from game_sys.particle_sys import ParticleFX
from game_sys.layer import Layer
from abc import ABC, abstractmethod


class Spaceship(pygame.sprite.Sprite):
    __SPACESHIP_HEALTH = 100

    def __init__(self, *groups: AbstractGroup):
        self._layer = Layer.PLAYER
        self.images = []
        self.index = 0
        self.state = IdleState(self)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(topleft=((configs.SCREEN_WIDTH // 2) - 32, configs.SCREEN_HEIGHT - 70))
        self.spaceship_health = self.__SPACESHIP_HEALTH
        self.mask = pygame.mask.from_surface(self.image)
        self.groups = groups
        self.destroy: Union[ExplosionFX, None] = None
        super().__init__(*groups)

    def set_state(self, state):
        self.state = state

    def update(self, *args, **kwargs):
        self.__handle_movements()
        self.__prevent_deserting()

    def __handle_movements(self) -> None:
        # Get pressed keys
        keys = pygame.key.get_pressed()

        # Check for left and right movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.set_state(TiltLeftState(self))
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.set_state(TiltRightState(self))
        # Check for up and down movement
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.set_state(MoveBackward(self))
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            self.set_state(MoveForward(self))

        # If no keys pressed, return to idle state
        if not any(keys):
            self.set_state(IdleState(self))

    def __prevent_deserting(self) -> None:
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= configs.SCREEN_WIDTH:
            self.rect.right = configs.SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= configs.SCREEN_HEIGHT:
            self.rect.bottom = configs.SCREEN_HEIGHT

    def manage_health(self) -> None:
        self.set_state(HealthManagementState(self))

    def get_health(self) -> int:
        return self.spaceship_health


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

    def tilt_wing_left(self, event=None): ...

    def tilt_wing_right(self, event=None): ...

    def idle_state(self, event=None): ...

    def fire(self, event=None): ...


class TiltLeftState(SpaceshipState):

    def __init__(self, spaceship: Spaceship):
        self.spaceship = spaceship
        self.spaceship.images = [
            pygame.transform.scale(assets.get_sprite('tilt_left_1'), (100, 100)),
            pygame.transform.scale(assets.get_sprite('tilt_left_2'), (100, 100))
        ]
        self.vel = Vector2(-5, 0)
        self.tilt_wing_left()

    def fire(self, event=None): ...

    def tilt_wing_right(self, event=None): ...

    def idle_state(self, event=None): ...

    def tilt_wing_left(self, event=None):
        self.spaceship.rect.move_ip(self.vel)
        self.spaceship.index += .1
        if self.spaceship.index < len(self.spaceship.images):
            self.spaceship.image = self.spaceship.images[int(self.spaceship.index)]

        # self.spaceship.image = pygame.transform.scale(assets.get_sprite('tilt_left_1'), (100, 100))


class TiltRightState(SpaceshipState):

    def __init__(self, spaceship: Spaceship):
        self.spaceship = spaceship
        self.spaceship.images = [
            pygame.transform.scale(assets.get_sprite('tilt_right_1'), (100, 100)),
            pygame.transform.scale(assets.get_sprite('tilt_right_2'), (100, 100))
        ]
        self.animation_speed = 0
        self.vel = Vector2(5, 0)
        self.tilt_wing_right()

    def tilt_wing_right(self, event=None):
        self.spaceship.rect.move_ip(self.vel)
        self.spaceship.index += .1
        if self.spaceship.index < len(self.spaceship.images):
            self.spaceship.image = self.spaceship.images[int(self.spaceship.index)]

        # self.spaceship.image = pygame.transform.scale(assets.get_sprite('tilt_right'), (100, 100))

    def fire(self, event=None): ...

    def tilt_wing_left(self, event=None): ...

    def idle_state(self, event=None): ...


class IdleState(SpaceshipState):
    def __init__(self, spaceship: Spaceship):
        self.spaceship = spaceship
        self.spaceship.images = [
            pygame.transform.scale(assets.get_sprite('idle'), (100, 100))
        ]
        self.reversed = False
        self.spaceship.index = 0
        self.vel = Vector2(0, 0)
        self.idle_state()

    def idle_state(self, event=None):
        self.spaceship.image = self.spaceship.images[self.spaceship.index]

    def fire(self, event=None):
        ...

    def tilt_wing_left(self, event=None):
        ...

    def tilt_wing_right(self, event=None):
        ...


class HealthManagementState(SpaceshipState):

    def __init__(self, spaceship: Spaceship):
        self.spaceship = spaceship
        self.destroyed()
        pass

    def fire(self, event=None): ...

    def tilt_wing_left(self, event=None): ...

    def tilt_wing_right(self, event=None): ...

    def idle_state(self, event=None): ...

    def damage_spaceship(self):
        self.spaceship.spaceship_health -= 20

    def destroyed(self) -> None:
        self.damage_spaceship()
        if self.spaceship.spaceship_health == 0:
            ExplosionFX(self.spaceship.groups[0], collided=self.spaceship)
            [ParticleFX(self.spaceship.groups[0], pos=(self.spaceship.rect.centerx, self.spaceship.rect.centery)) for _
             in range(100)]
            self.spaceship.kill()
            return
        [ParticleFX(self.spaceship.groups[0], pos=(self.spaceship.rect.centerx, self.spaceship.rect.centery)) for _
         in range(10)]


class MoveForward(SpaceshipState):
    def __init__(self, spaceship: Spaceship):
        self.spaceship = spaceship
        self.vel = Vector2(0, -5)
        self.move_forward()

    def fire(self, event=None):
        pass

    def tilt_wing_left(self, event=None):
        pass

    def tilt_wing_right(self, event=None):
        pass

    def idle_state(self, event=None):
        pass

    def move_forward(self):
        self.spaceship.rect.move_ip(self.vel)
        pass


class MoveBackward(SpaceshipState):
    def __init__(self, spaceship: Spaceship):
        self.spaceship = spaceship
        self.vel = Vector2(0, 5)
        self.move_backward()

    def fire(self, event=None):
        pass

    def tilt_wing_left(self, event=None):
        pass

    def tilt_wing_right(self, event=None):
        pass

    def idle_state(self, event=None):
        pass

    def move_backward(self):
        self.spaceship.rect.move_ip(self.vel)
        pass

    def super_speed(self):
        pass
