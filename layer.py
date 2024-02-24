from enum import IntEnum, auto


class Layer(IntEnum):
    BACKGROUND = auto()
    UI = auto()
    SCORE = auto()
    NEW_GAME = ()
    ASTEROID = auto()
    GAME_OVER = auto()
    ALIEN = auto()
    PLAYER = auto()
    WEAPON = auto()
    EXPLOSION = auto()
    PARTICLE = auto()



