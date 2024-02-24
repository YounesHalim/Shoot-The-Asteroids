import pygame
from pygame.sprite import AbstractGroup

import assets
import configs
from layer import Layer


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, *groups: AbstractGroup):
        self._layer = Layer.PLAYER
        self.images = [
            pygame.transform.scale(assets.get_sprite('tile000'), (100, 100))
        ]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(topleft=((configs.SCREEN_WIDTH // 2) - 32, configs.SCREEN_HEIGHT - 70))
        self.move = 4
        self.is_idle = True
        self.tilting_right = False
        self.tilting_left = False
        self.health = 100
        self.last_frame_update = 0  # Store the time of the last frame update
        self.animation_delay = 50  # Set the delay between animation frames in milliseconds
        super().__init__(*groups)

    def update(self, *args, **kwargs):
        self.__handle_movements()
        self.__prevent_deserting()

    def __handle_movements(self) -> None:
        # Get pressed keys
        keys = pygame.key.get_pressed()

        # Check for left and right movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.tilting_left = True
            self.rect.x -= self.move
            self.__tilt_left()
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.tilting_right = True
            self.rect.x += self.move
            self.__tilt_right()

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
            self.__return_to_idle()

    def __return_to_idle(self):
        current_time = pygame.time.get_ticks()  # Get the current time
        if current_time - self.last_frame_update >= self.animation_delay:
            self.index = 0
            self.image = self.images[self.index]
            if len(self.images) > 1:
                self.index = 0
                self.image = self.images[self.index]
                self.image = pygame.transform.scale(assets.get_sprite('tile000'), (100, 100))
            self.last_frame_update = current_time  # Update the last frame update time

    def __tilt_left(self):
        if not self.tilting_left:
            return
        current_time = pygame.time.get_ticks()  # Get the current time
        if current_time - self.last_frame_update >= self.animation_delay:
            self.images = [
                pygame.transform.scale(assets.get_sprite('tile001l'), (100, 100)),
                pygame.transform.scale(assets.get_sprite('tile002l'), (100, 100)),
            ]
            if self.index < len(self.images) - 1:
                self.index += 1
                self.image = self.images[self.index]
            self.last_frame_update = current_time  # Update the last frame update time

    def __tilt_right(self):
        if not self.tilting_right:
            return
        current_time = pygame.time.get_ticks()  # Get the current time
        if current_time - self.last_frame_update >= self.animation_delay:
            self.images = [
                pygame.transform.scale(assets.get_sprite('tile006r'), (100, 100)),
                pygame.transform.scale(assets.get_sprite('tile007r'), (100, 100)),
            ]
            if self.index < len(self.images) - 1:
                self.index += 1
                self.image = self.images[self.index]
            self.last_frame_update = current_time  # Update the last frame update time

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
