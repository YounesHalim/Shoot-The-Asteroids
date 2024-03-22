import sys

import pygame

import assets
import configs
from game_objects.alien import AlienSpaceship
from game_objects.asteroid import Asteroid
from game_objects.spaceship import Spaceship
from game_objects.weapons import LaserBeam
from game_sys.explosion_fx_sys import ExplosionFX
from game_sys.particle_sys import ParticleFX
from game_sys.game_sys import Game
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
    pygame.display.set_caption('Shoot The Asteroids')
    clock = pygame.time.Clock()

    game = Game()
    spaceship, score = game.init_game()
    sprites = game.get_layer_updates
    asteroids: list[Asteroid] = game.spawned_asteroids

    # assets.get_audio('ost').play(loops=-1).set_volume(.8)
    while run:
        events = pygame.event.get()
        # Handling events
        for event in events:
            if event.type == pygame.QUIT:
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

        # Asteroids waves
        game.wave_switcher(game_started)
        # Collision check!
        for asteroid in asteroids:
            asteroid.asteroid_behavior(asteroids)
            if asteroid.rect.collidepoint(spaceship.rect.centerx, spaceship.rect.centery) and not game_over:
                ExplosionFX(sprites, collided=spaceship)
                [ParticleFX(sprites, pos=(asteroid.rect.centerx, asteroid.rect.centery)) for particle in range(100)]
                asteroid.kill()
                spaceship.kill()
                sprites.remove_sprites_of_layer(Layer.PLAYER)
                game_over = True
                game.stop()
                beams.clear()
                game_over_message = GameMessage(sprites)
            if beams:
                for beam in beams:
                    if asteroid.rect.collidepoint(beam.rect.centerx, beam.rect.centery) and not game_over:
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

        # alien hit registration
        if beams:
            for beam in beams:
                alien: AlienSpaceship
                for alien in game.get_layer_updates.get_sprites_from_layer(Layer.ALIEN):
                    sprites_from_layer = sprites.get_sprites_from_layer(Layer.WEAPON)
                    if alien.rect.collidepoint(beam.rect.centerx, beam.rect.centery):
                        alien.damage()
                        CounterHitSys(sprites, game_object=alien, score=score)
                        [ParticleFX(sprites, pos=(alien.rect.centerx, alien.rect.centery)) for particle in
                         range(5)]
                        beam.kill()
                        if alien.is_destroyed():
                            [ParticleFX(sprites, pos=(alien.rect.centerx, alien.rect.centery)) for particle in
                             range(100)]
                            alien.kill()
                        beams.remove(beam)

        screen.fill(0)
        sprites.draw(screen)
        sprites.update()
        pygame.display.flip()
        clock.tick(configs.FPS)

    pygame.quit()
    sys.exit()
