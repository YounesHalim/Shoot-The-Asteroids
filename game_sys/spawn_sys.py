import threading
import time

from pygame.sprite import LayeredUpdates, AbstractGroup
from abc import ABC, abstractmethod
from random import randint

import assets
from game_objects.alien import AlienSpaceship
from game_objects.asteroid import Asteroid
from game_objects.background import Background
from game_objects.spaceship import Spaceship
from game_sys.ui_sys import Score, StartGame


class WaveSys(ABC):
    @abstractmethod
    def spawn_asteroids(self, number: int = None, delay: int | float = None): ...

    @abstractmethod
    def spawn_aliens(self, number: int = None, delay: int | float = None): ...

    @abstractmethod
    def game_message(self) -> None: ...


class SpawnSys(threading.Thread, WaveSys):

    def game_message(self) -> None: ...

    def __init__(self):
        self.__sprites = LayeredUpdates()
        assets.load_sprites()
        assets.load_audios()
        self.__asteroids = []
        self.__aliens = []
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self.state = GameIntroMenu(self.__sprites, spawner=self)
        super().__init__()

    def stop(self):
        self._stop_event.set()

    def __setstate__(self, state):
        self.state = state

    def wave_switcher(self, game_started: bool):

        if game_started:
            if isinstance(self.state, GameIntroMenu):
                self.state.remove_intro_layout(True)
                self.__setstate__(FirstWave(self))
            # elif isinstance(self.state, FirstWave) and not self.state.wave.is_alive() and len(self.__asteroids) == 0:
            #     self.__setstate__((WaveDifficultyManager(self)))
            #     return
            # self.__setstate__((WaveDifficultyManager(self))) if isinstance(self.state, WaveDifficultyManager) and not self.state.wave.is_alive() and len(self.__asteroids) == 0 else None

    def create_game_world_sprites(self):
        Background(0, self.__sprites)
        Background(1, self.__sprites)
        spaceship = Spaceship(self.__sprites)
        # Alien(spaceship, self.__sprites)
        StartGame(self.__sprites)
        return spaceship, Score(self.__sprites)

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
    def spawned_aliens(self) -> list[AlienSpaceship]:
        return self.__aliens

    @property
    def get_layer_updates(self) -> LayeredUpdates:
        return self.__sprites

    @property
    def lock(self):
        return self._lock


class GameIntroMenu(WaveSys, StartGame):

    def __init__(self, *groups: AbstractGroup, spawner: SpawnSys):
        self.spawner = spawner
        super().__init__(*groups)

    def game_message(self) -> None:
        self.remove_intro_layout(True)

    def spawn_asteroids(self, number: int = None, delay: int | float = None):
        pass

    def spawn_aliens(self, number: int = None, delay: int | float = None):
        pass


class FirstWave(WaveSys):
    def game_message(self) -> None:
        pass

    __ASTEROIDS = 3
    __SPEED = 1.5

    def __init__(self, spawner: SpawnSys):
        self.spawner = spawner
        self.wave = threading.Thread(target=self.spawn_asteroids, args=(self.__ASTEROIDS, self.__SPEED,))
        self.wave.start()
        AlienSpaceship(self.spawner.get_layer_updates)
        print(f'first wave {self}')

    def spawn_asteroids(self, number: int = None, delay: int | float = None):
        self.spawner.spawn_asteroids(number, delay)

    def spawn_aliens(self, number: int = None, delay: int | float = None): ...


class SecondWave(WaveSys):
    def game_message(self) -> None:
        pass

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
    def game_message(self) -> None:
        pass

    __ASTEROIDS = 3
    __SPEED = 1
    __LEVEL = 1
    __MAX_LEVEL = 7

    def __init__(self, spawner: SpawnSys):
        self.spawner = spawner
        self.spawner.asteroids = self.__ASTEROIDS
        self.speed = 1
        self.wave = threading.Thread(target=self.spawn_asteroids, args=(self.__ASTEROIDS, self.speed))
        self.wave.start()

    def spawn_asteroids(self, number: int = None, delay: int | float = None):
        self.spawner.spawn_asteroids(number, delay)
        difficulty = randint(WaveDifficultyManager.__ASTEROIDS, WaveDifficultyManager.__LEVEL * 10)
        WaveDifficultyManager.__ASTEROIDS += difficulty
        WaveDifficultyManager.__LEVEL += 1 if WaveDifficultyManager.__LEVEL != WaveDifficultyManager.__MAX_LEVEL else 0

    def spawn_aliens(self, number: int = None, delay: int | float = None): ...
