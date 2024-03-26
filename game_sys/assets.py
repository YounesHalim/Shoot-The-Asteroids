import os
import pygame
from pygame.mixer import Sound
from pygame.surface import Surface, SurfaceType

sprites = {}
audios = {}


def load_sprites() -> None:
    path = os.path.join(os.path.abspath(''), "assets/sprites")
    for file in os.listdir(path):
        try:
            sprites[file.split('.')[0]] = pygame.image.load(os.path.join(path, file))
        except pygame.error:
            pass


def get_sprite(name: str) -> Surface | SurfaceType:
    return sprites[name]


def load_audios() -> None:
    path = os.path.join(os.path.abspath(''), "assets/audios")
    for file in os.listdir(path):
        try:
            audios[file.split('.')[0]] = pygame.mixer.Sound(os.path.join(path, file))
        except pygame.error:
            pass


def get_audio(name: str) -> Sound:
    return audios[name]
