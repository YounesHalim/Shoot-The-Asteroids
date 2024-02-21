from enum import IntEnum, auto


class Layer(IntEnum):
    BACKGROUND = auto()
    ASTEROID = auto()
    ALIEN = auto()
    PLAYER = auto()
    WEAPON = auto()
    EXPLOSION = auto()
    UI = auto()
