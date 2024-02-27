import os
import pygame
from pygame.mixer import Sound
from pygame.sprite import Sprite

sprites = {}
audios = {}


def load_sprites() -> None:
    path = os.path.join("assets", "sprites")
    for file in os.listdir(path):
        try:
            sprites[file.split('.')[0]] = pygame.image.load(os.path.join(path, file))
        except Exception as e:
            continue


def get_sprite(name: str) -> Sprite:
    return sprites[name]


def load_audios() -> None:
    path = os.path.join("assets", "audios")
    for file in os.listdir(path):
        audios[file.split('.')[0]] = pygame.mixer.Sound(os.path.join(path, file))


def get_audio(name: str) -> Sound:
    return audios[name]
