import threading
import time

from pygame.sprite import LayeredUpdates

import assets
from game_objects.alien import Alien
from game_objects.asteroid import Asteroid
from game_objects.background import Background
from game_objects.spaceship import Spaceship
from game_objects.ui import Score


class SpawnSys(threading.Thread):
    def __init__(self, container: LayeredUpdates):
        self.sprites = container
        assets.load_sprites()
        assets.load_audios()
        self.__asteroids = []
        self.__aliens = []
        self._stop_event = threading.Event()
        super().__init__()

    def stop(self):
        self._stop_event.set()

    def create_game_world_sprites(self):
        Background(0, self.sprites)
        Background(1, self.sprites)

        return Spaceship(self.sprites), Score(self.sprites)

    def spawn_asteroids(self, number: int = 100, delay: int = 1):
        for i in range(number):
            if not self._stop_event.is_set():
                self.__asteroids.append(Asteroid(self.sprites))
                time.sleep(delay)

    def spawned_asteroids(self) -> list[Asteroid]:
        return self.__asteroids

    def spawned_aliens(self) -> list[Alien]:
        return self.__aliens
