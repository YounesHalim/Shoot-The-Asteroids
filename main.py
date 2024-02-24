import sys
import threading

import pygame

import configs
from game_objects.asteroid import Asteroid
from game_objects.explosion_effect import ExplosionEffect
from game_objects.particle_system import Particle
from game_objects.spawner import SpawnSys
from game_objects.ui import GameMessage, CounterHitSys
from game_objects.weapons import LaserBeam

if __name__ == '__main__':
    pygame.init()
    running = True
    game_over = False
    game_started = False
    beams = []
    screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))
    # my_font = pygame.font.SysFont('Times New Roman', 25)
    # font = pygame.font.Font(None, 36)
    pygame.display.set_caption('INVADERS MUST DIE')
    clock = pygame.time.Clock()

    spawner = SpawnSys(pygame.sprite.LayeredUpdates())
    spaceship, score = spawner.create_game_world_sprites()
    sprites = spawner.sprites
    asteroids: list[Asteroid] = spawner.spawned_asteroids()

    asteroid_spawn_thread = threading.Thread(target=spawner.spawn_asteroids)
    asteroid_spawn_thread.start()

    while running:
        events = pygame.event.get()
        # Handling events
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                spawner.stop()
            # shooting beams
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not game_over:
                beams.append(LaserBeam(sprites, x=spaceship.rect.x + 15, y=spaceship.rect.y))

        # Collision check!
        for asteroid in asteroids:
            if asteroid.rect.collidepoint(spaceship.rect.centerx, spaceship.rect.centery) and not game_over:
                ExplosionEffect(sprites, x=spaceship.rect.centerx, y=spaceship.rect.centery)
                [Particle(sprites, pos=(asteroid.rect.centerx, asteroid.rect.centery)) for particle in range(10)]
                asteroid.kill()
                spaceship.kill()
                game_over = True
                game_over_message = GameMessage(sprites)
            if len(beams) > 0:
                for beam in beams:
                    if asteroid.rect.collidepoint(beam.rect.centerx, beam.rect.centery) and not game_over:
                        [Particle(sprites, pos=(asteroid.rect.centerx, asteroid.rect.centery)) for particle in
                         range(10)]
                        score.value += 1
                        asteroid.asteroid_hit()
                        beam.kill()
                        CounterHitSys(sprites, asteroid=asteroid)
                        if asteroid.is_destroyed():
                            ExplosionEffect(sprites, x=asteroid.rect.centerx, y=asteroid.rect.centery)
                            asteroids.remove(asteroid)
                        beams.remove(beam)

        screen.fill(0)
        sprites.draw(screen)
        sprites.update()
        pygame.display.flip()
        clock.tick(configs.FPS)

    pygame.quit()
    sys.exit()
