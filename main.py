import sys

import pygame

import configs
from game_objects.asteroid import Asteroid
from game_objects.spaceship import Spaceship
from game_objects.weapons import LaserBeam
from game_sys.explosion_fx_sys import ExplosionEffect
from game_sys.particle_sys import Particle
from game_sys.spawn_sys import SpawnSys
from game_sys.ui_sys import GameMessage, CounterHitSys
from layer import Layer

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.pre_init(44100, 24, 2, 4096)
    run = True
    game_over = False
    game_started = False
    beams = []
    screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT))
    pygame.display.set_caption('INVADERS MUST DIE')
    clock = pygame.time.Clock()

    spawner = SpawnSys()
    spaceship, score = spawner.create_game_world_sprites()
    sprites = spawner.get_layer_updates
    asteroids: list[Asteroid] = spawner.spawned_asteroids

    # assets.get_audio('ost').play(loops=-1).set_volume(.8)
    while run:
        events = pygame.event.get()
        # Handling events
        for event in events:
            if event.type == pygame.QUIT:
                run = False
                spawner.stop()
            # shooting beams
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not game_over:
                beams.append(
                    LaserBeam(sprites, x=spaceship.rect.x + 15, y=spaceship.rect.y - (spaceship.rect.height // 2)))
            # Game over
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and game_over:
                sprites.remove_sprites_of_layer(Layer.GAME_OVER)
                spaceship = Spaceship(sprites)
                game_over = False

        # Asteroids waves
        spawner.wave_switcher(game_over)

        # Collision check!
        for asteroid in asteroids:
            asteroid.asteroid_behavior(asteroids)
            if asteroid.rect.collidepoint(spaceship.rect.centerx, spaceship.rect.centery) and not game_over:
                ExplosionEffect(sprites, collided=spaceship)
                [Particle(sprites, pos=(asteroid.rect.centerx, asteroid.rect.centery)) for particle in range(100)]
                asteroid.kill()
                spaceship.kill()
                sprites.remove_sprites_of_layer(Layer.PLAYER)
                game_over = True
                # spawner.stop()
                beams.clear()
                game_over_message = GameMessage(sprites)
            if len(beams) > 0:
                for beam in beams:
                    if asteroid.rect.collidepoint(beam.rect.centerx, beam.rect.centery) and not game_over:
                        [Particle(sprites, pos=(asteroid.rect.centerx, asteroid.rect.centery)) for particle in
                         range(10)]
                        asteroid.asteroid_hit()
                        beam.kill()
                        CounterHitSys(sprites, asteroid=asteroid, score=score)
                        if asteroid.is_destroyed():
                            ExplosionEffect(sprites, collided=asteroid)
                            asteroids.remove(asteroid)
                        beams.remove(beam)

        screen.fill(0)
        sprites.draw(screen)
        sprites.update()
        pygame.display.flip()
        clock.tick(configs.FPS)

    pygame.quit()
    sys.exit()
