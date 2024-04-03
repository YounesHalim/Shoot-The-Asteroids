import threading
import time

from pygame.sprite import LayeredUpdates, AbstractGroup
from abc import ABC, abstractmethod
from random import randint

from game_sys import assets
from game_objects.alien import AlienSpaceship
from game_objects.asteroid import Asteroid
from game_objects.background import Background
from game_objects.spaceship import Spaceship
from game_sys.ui_sys import StartGame, Score


class WaveSys(ABC):
    @abstractmethod
    def spawn_asteroids(self, number: int = None, delay: int | float = None): ...

    @abstractmethod
    def spawn_aliens(self, number: int = None, delay: int | float = None): ...

    @abstractmethod
    def game_message(self) -> None: ...


class GameState(ABC):
    @abstractmethod
    def game_started(self): ...

    @abstractmethod
    def game_over(self): ...

    @abstractmethod
    def main_menu(self): ...


class Game(threading.Thread, WaveSys):

    def game_message(self) -> None:
        ...

    def __init__(self):
        self.__sprites = LayeredUpdates()
        assets.load_sprites()
        assets.load_audios()
        self.__asteroids = []
        self.__aliens = []
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self.state = MainMenu(self.__sprites, game=self)
        super().__init__()

    def stop(self):
        self._stop_event.set()

    def set_state(self, state):
        self.state = state

    def wave_switcher(self, game_started: bool):

        if game_started:
            if isinstance(self.state, MainMenu):
                self.state.remove_intro_layout(True)
                self.set_state(FirstWave(self))
            elif isinstance(self.state, FirstWave) and not self.state.wave.is_alive() and len(self.__asteroids) == 0:
                self.set_state((WaveDifficultyManager(self)))
                return
            self.set_state((WaveDifficultyManager(self))) if isinstance(self.state,
                                                                        WaveDifficultyManager) and not self.state.wave.is_alive() and len(
                self.__asteroids) == 0 else None

    def init_game(self):
        Background(0, self.__sprites)
        Background(1, self.__sprites)
        spaceship = Spaceship(self.__sprites)
        StartGame(self.__sprites)
        return spaceship, Score(self.__sprites)

    def spawn_aliens(self, number: int = 0, delay: int | float = 1):
        AlienSpaceship(self.__sprites)

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
    def spawned_aliens(self) -> list[threading.Thread]:
        return self.__aliens

    @property
    def get_layer_updates(self) -> LayeredUpdates:
        return self.__sprites

    @property
    def lock(self):
        return self._lock


class MainMenu(WaveSys, StartGame):

    def __init__(self, *groups: AbstractGroup, game: Game):
        self.game = game
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

    def __init__(self, game: Game):
        self.game = game
        self.wave = threading.Thread(target=self.spawn_asteroids, args=(self.__ASTEROIDS, self.__SPEED,))
        self.wave.start()
        self.spawn_aliens()

    def spawn_asteroids(self, number: int = None, delay: int | float = None):
        self.game.spawn_asteroids(number, delay)

    def spawn_aliens(self, number: int = None, delay: int | float = None):
        self.game.spawn_aliens(number)


class WaveDifficultyManager(WaveSys):
    def game_message(self) -> None:
        pass

    __ASTEROIDS = 3
    __SPEED = 1
    __LEVEL = 1
    __MAX_LEVEL = 7

    def __init__(self, game: Game):
        self.game = game
        self.game.asteroids = self.__ASTEROIDS
        self.speed = 1
        self.wave = threading.Thread(target=self.spawn_asteroids, args=(self.__ASTEROIDS, self.speed))
        self.wave.start()

    def spawn_asteroids(self, number: int = None, delay: int | float = None):
        self.game.spawn_asteroids(number, delay)
        difficulty = randint(WaveDifficultyManager.__ASTEROIDS, WaveDifficultyManager.__LEVEL * 10)
        WaveDifficultyManager.__ASTEROIDS += difficulty
        WaveDifficultyManager.__LEVEL += 1 if WaveDifficultyManager.__LEVEL != WaveDifficultyManager.__MAX_LEVEL else 0

    def spawn_aliens(self, number: int = None, delay: int | float = None): ...
