
import pygame
import pymunk
import pymunk.pygame_util

import constants
from ball import Ball
from physics_object import PhysicsObject
from rect_barrier import RectBarrier

pygame.init()


window = pygame.display.set_mode(constants.WINDOW_SIZE)
pygame.display.set_caption("Mini Golf")

space = pymunk.Space()
space.gravity = 0, constants.GRAVITY


def main():
    wall_thickness = 10
    objects: list[PhysicsObject] = [
        RectBarrier((50, 50), (30, 200), space),
        RectBarrier((400, 50), (30, 200), space),


        RectBarrier((0, 0), (constants.WINDOW_WIDTH, wall_thickness), space),
        RectBarrier((0, constants.WINDOW_HEIGHT-wall_thickness),
                    (constants.WINDOW_WIDTH, wall_thickness), space),
        RectBarrier((0, wall_thickness), (wall_thickness,
                                          constants.WINDOW_HEIGHT-2*wall_thickness), space),
        RectBarrier((constants.WINDOW_WIDTH-wall_thickness, wall_thickness),
                    (wall_thickness, constants.WINDOW_HEIGHT-2*wall_thickness), space)
    ]

    ball = Ball((constants.WINDOW_WIDTH//2, constants.WINDOW_WIDTH//2), space)
    objects.append(ball)
    clock = pygame.time.Clock()
    running = True
    timer = pygame.time.get_ticks()
    held_pos = 0, 0
    mouse_held = False
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for x in range(constants.PHYSICS_STEPS_PER_FRAME):
            space.step(constants.DT)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ball.rect.collidepoint(mouse_pos):
                    held_pos = pygame.mouse.get_pos()
                    mouse_held = True
            if event.type == pygame.MOUSEBUTTONUP and mouse_held:
                offset = mouse_pos[0]-held_pos[0], mouse_pos[1]-held_pos[1]
                force = -offset[0]*400, -offset[1]*400
                ball.body.apply_force_at_local_point(force, (0, 0))
                mouse_held = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    pass
        keys = pygame.key.get_pressed()
        now = pygame.time.get_ticks()
        if keys[pygame.K_h] and now - timer > 5000:
            velocity_copy = pymunk.Vec2d(
                ball.body.velocity[0], ball.body.velocity[1])
            direction, speed = velocity_copy.normalized_and_length()
            ball.body.apply_impulse_at_local_point(
                (.03 * -direction.x * speed, .03 * -direction.y * speed), (0, 0))

        clock.tick(constants.FPS)
        window.fill((255, 255, 255))

        # space.debug_draw(pymunk.pygame_util.DrawOptions(window))
        for game_object in objects:
            game_object.render(window)

        pygame.display.flip()


if __name__ == "__main__":
    main()
