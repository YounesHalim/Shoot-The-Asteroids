import threading
import time

from pygame.sprite import LayeredUpdates
from abc import ABC, abstractmethod
from random import randint

import assets
from game_objects.alien import Alien
from game_objects.asteroid import Asteroid
from game_objects.background import Background
from game_objects.spaceship import Spaceship
from game_sys.ui_sys import Score


class WaveSys(ABC):
    @abstractmethod
    def spawn_asteroids(self, number: int = None, delay: int | float = None): ...

    @abstractmethod
    def spawn_aliens(self, number: int = None, delay: int | float = None): ...


class SpawnSys(threading.Thread, WaveSys):

    def __init__(self):
        self.__sprites = LayeredUpdates()
        assets.load_sprites()
        assets.load_audios()
        self.__asteroids = []
        self.__aliens = []
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self.state = FirstWave(self)
        super().__init__()

    def stop(self):
        self._stop_event.set()

    def __setstate__(self, state):
        self.state = state

    def wave_switcher(self, game_over: bool):
        if not game_over:
            if isinstance(self.state, FirstWave) and not self.state.wave.is_alive() and len(self.__asteroids) == 0:
                self.__setstate__((SecondWave(self)))
                return
            elif isinstance(self.state, SecondWave) and not self.state.wave.is_alive() and len(self.__asteroids) == 0:
                self.__setstate__((WaveDifficultyManager(self)))
                return
            elif isinstance(self.state, WaveDifficultyManager) and not self.state.wave.is_alive() and len(
                    self.__asteroids) == 0:
                self.__setstate__((WaveDifficultyManager(self)))

    def create_game_world_sprites(self):
        Background(0, self.__sprites)
        Background(1, self.__sprites)

        return Spaceship(self.__sprites), Score(self.__sprites)

    def spawn_aliens(self, number: int = None, delay: int | float = None):
        ...

    def spawn_asteroids(self, number: int = 2, delay: int | float = 1):
        for i in range(number):
            if not self._stop_event.is_set():
                with self._lock:
                    self.__asteroids.append(Asteroid(self.__sprites))
            time.sleep(delay)

    @property
    def spawned_asteroids(self) -> list[Asteroid]:
        return self.__asteroids

    @property
    def spawned_aliens(self) -> list[Alien]:
        return self.__aliens

    @property
    def get_layer_updates(self) -> LayeredUpdates:
        return self.__sprites

    @property
    def lock(self):
        return self._lock


class FirstWave(WaveSys):
    __ASTEROIDS = 3
    __SPEED = 1.5

    def __init__(self, spawner: SpawnSys):
        self.spawner = spawner
        self.wave = threading.Thread(target=self.spawn_asteroids, args=(self.__ASTEROIDS, self.__SPEED,))
        self.wave.start()
        print(f'first wave {self}')

    def spawn_asteroids(self, number: int = None, delay: int | float = None):
        self.spawner.spawn_asteroids(number, delay)

    def spawn_aliens(self, number: int = None, delay: int | float = None): ...


class SecondWave(WaveSys):
    __ASTEROIDS = 10
    __SPEED = 1

    def __init__(self, spawner: SpawnSys):
        self.spawner = spawner
        self.wave = threading.Thread(target=self.spawn_asteroids, args=(self.__ASTEROIDS, self.__SPEED,))
        self.wave.start()
        print(f'second wave {self}')

    def spawn_asteroids(self, number: int = None, delay: int | float = None):
        self.spawner.spawn_asteroids(number, delay)

    def spawn_aliens(self, number: int = None, delay: int | float = None): ...


class WaveDifficultyManager(WaveSys):
    __DIFFICULTY = 3
    __SPEED = 1
    __LEVEL = 1
    __MAX_LEVEL = 6

    def __init__(self, spawner: SpawnSys):
        self.spawner = spawner
        self.spawner.asteroids = self.__DIFFICULTY
        self.speed = 1
        self.wave = threading.Thread(target=self.spawn_asteroids, args=(self.__DIFFICULTY, self.speed))
        self.wave.start()
        print(f'Difficulty incrementer {self}')

    def spawn_asteroids(self, number: int = None, delay: int | float = None):
        self.spawner.spawn_asteroids(number, delay)
        difficulty: int = randint(WaveDifficultyManager.__DIFFICULTY, WaveDifficultyManager.__LEVEL * 10)
        WaveDifficultyManager.__DIFFICULTY += difficulty
        WaveDifficultyManager.__LEVEL += 1 if WaveDifficultyManager.__LEVEL != WaveDifficultyManager.__MAX_LEVEL else ...

    def spawn_aliens(self, number: int = None, delay: int | float = None): ...
