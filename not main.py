
import pygame
import pymunk
import pymunk.pygame_util

import game.constants as constants
import util
from game.ball import Ball
from game.course.block import RectBarrier
from game.physics_object import PhysicsObject
from util.window import Window

pygame.init()


window = Window(constants.SCREEN_SIZE, "Mini Golf",
                util.load_image("icon", "assets"))
space = pymunk.Space()
space.gravity = 0, constants.GRAVITY


def shift_map(x_change: int, y_change: int, other_objects: list[PhysicsObject]) -> None:
    for object in other_objects:
        object.pos = object.pos[0], object.pos[1]+1
        print(object.pos)


def main():
    wall_thickness = 10
    objects: list[PhysicsObject] = [
        RectBarrier((50, 50), (30, 200), space),
        RectBarrier((400, 50), (30, 200), space),


        RectBarrier((0, 0), (constants.SCREEN_WIDTH, wall_thickness), space),
        RectBarrier((0, constants.SCREEN_HEIGHT-wall_thickness),
                    (constants.SCREEN_WIDTH, wall_thickness), space),
        RectBarrier((0, wall_thickness), (wall_thickness,
                                          constants.SCREEN_HEIGHT-2*wall_thickness), space),
        RectBarrier((constants.SCREEN_WIDTH-wall_thickness, wall_thickness),
                    (wall_thickness, constants.SCREEN_HEIGHT-2*wall_thickness), space)
    ]

    ball = Ball((constants.SCREEN_WIDTH//2, constants.SCREEN_WIDTH//2), space)
    other_objects = objects.copy()
    objects.append(ball)
    clock = pygame.time.Clock()
    running = True
    timer = util.Timer()
    held_pos = 0, 0
    mouse_held = False
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for x in range(constants.PHYSICS_STEPS_PER_FRAME):
            space.step(constants.DT)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ball.rect.collidepoint(mouse_pos):
                    held_pos = pygame.mouse.get_pos()
                    mouse_held = True
            if event.type == pygame.MOUSEBUTTONUP and mouse_held:
                offset = mouse_pos[0]-held_pos[0], mouse_pos[1]-held_pos[1]
                force = -offset[0]*400, -offset[1]*400
                ball.body.apply_force_at_local_point(force, (0, 0))
                timer.start()
                mouse_held = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            shift_map(0, 0, other_objects)

        if timer.passed(4):
            velocity_copy = pymunk.Vec2d(
                ball.body.velocity[0], ball.body.velocity[1])
            direction, speed = velocity_copy.normalized_and_length()
            ball.body.apply_impulse_at_local_point(
                (.07 * -direction.x * speed, .07 * -direction.y * speed), (0, 0))

        if mouse_held:
            pygame.draw.line(window.screen, util.Color.BLACK,
                             mouse_pos, ball.rect.center, width=4)
        for game_object in objects:
            game_object.render(window.screen)

        window.update()


if __name__ == "__main__":
    main()
