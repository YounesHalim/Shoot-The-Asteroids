import sys

import pygame
from pygame.sprite import collide_mask

from game_objects.asteroid import Asteroid
from game_objects.spaceship import Spaceship
from game_objects.weapons import LaserBeam
from game_sys import configs, assets
from game_sys.explosion_fx_sys import ExplosionFX
from game_sys.game_sys import Game
from game_sys.layer import Layer
from game_sys.particle_sys import ParticleFX
from game_sys.ui_sys import GameMessage, CounterHitSys

if __name__ == '__main__':

    game = Game()
    screen = game.get_screen
    clock = game.get_clock
    spaceship, score = game.init_game()
    sprites = game.get_layer_updates
    asteroids: list[Asteroid] = game.spawned_asteroids
    beams: list[LaserBeam] = []
    run = True
    game_over = False
    game_started = False

    while run:
        events = pygame.event.get()
        # Handling events
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False
                game.stop()
            # shooting beams
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not game_over:
                beams.append(
                    LaserBeam(sprites, obj=spaceship, x=spaceship.rect.x + 15,
                              y=spaceship.rect.y - (spaceship.rect.height // 2)))
            # Game over
            if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE and game_over:
                sprites.remove_sprites_of_layer(Layer.GAME_OVER)
                spaceship = Spaceship(sprites)
                game_over = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and not game_started:
                game_started = True
                assets.get_audio('ost').play(loops=-1).set_volume(.8)

        # Asteroids waves
        game.wave_switcher(game_started)
        # Collision check!
        for asteroid in asteroids:
            asteroid.asteroid_behavior(asteroids)
            if pygame.sprite.spritecollide(asteroid, pygame.sprite.Group(spaceship), False, collide_mask) and not game_over:
                ExplosionFX(sprites, collided=spaceship)
                [ParticleFX(sprites, pos=(asteroid.rect.centerx, asteroid.rect.centery)) for particle in range(100)]
                asteroid.kill()
                spaceship.kill()
                sprites.remove_sprites_of_layer(Layer.PLAYER)
                game_over = True
                beams.clear()
                game_over_message = GameMessage(sprites)
            if beams:
                for beam in beams:
                    if pygame.sprite.spritecollide(asteroid, pygame.sprite.Group(beam), False, collide_mask) and not game_over:
                        [ParticleFX(sprites, pos=(asteroid.rect.centerx, asteroid.rect.centery)) for particle in
                         range(10)]
                        asteroid.asteroid_hit()
                        beam.kill()
                        CounterHitSys(sprites, game_object=asteroid, score=score)
                        if asteroid.is_destroyed():
                            ExplosionFX(sprites, collided=asteroid)
                            asteroids.remove(asteroid)
                        beams.remove(beam)

        if len(game.get_layer_updates.get_sprites_from_layer(Layer.PLAYER)) == 0 and not game_over:
            game_over = True
            game_started = False
            GameMessage(sprites)

        screen.fill(0)
        sprites.draw(screen)
        sprites.update()
        pygame.display.flip()
        clock.tick(configs.FPS)

    pygame.quit()
    sys.exit()
