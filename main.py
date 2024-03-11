from abc import ABC, abstractmethod

import pygame
import pymunk
import pymunk.pygame_util

import constants


class PhysicsObject(ABC):
    def add_to_space(self, space: pymunk.Space):
        space.add(self.body, self.shape)


class Ball(PhysicsObject):
    def __init__(self, pos: tuple[int, int]) -> None:
        mass = 1
        self.body = pymunk.Body(mass, inertia)
        radius = 30
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        self.body.position = pos
        self.shape = pymunk.Circle(self.body, radius, (0, 0))
        self.shape.elasticity = 1
        self.shape.friction = 0.0


class RectBarrier(PhysicsObject):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int]) -> None:
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        # body.position = pos
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.shape = pymunk.Poly(self.body, [
            self.rect.topleft, self.rect.topright, self.rect.bottomleft, self.rect.bottomright])

        self.shape.elasticity = 1
        self.shape.friction = 0


pygame.init()


window = pygame.display.set_mode(constants.WINDOW_SIZE)
pygame.display.set_caption("Physics Sim")

space = pymunk.Space()
space.gravity = 0, constants.GRAVITY


def add_ball_with_joint(pos: tuple[int]) -> None:
    body = add_ball(pos)
    pj = pymunk.PinJoint(space.static_body, body,
                         (body.position[0], -125 + body.position[1]), (0, 0))
    space.add(pj)


def add_ball_with_force(pos: tuple[int], force: tuple[float, float]) -> pymunk.Body:
    body = add_ball(pos)
    body.apply_force_at_local_point(force)
    return body


def add_ball(pos: tuple[int]) -> pymunk.Body:
    mass = 1
    radius = 30
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
    body = pymunk.Body(mass, inertia)
    body.position = pos
    shape = pymunk.Circle(body, radius, (0, 0))
    shape.elasticity = 1
    shape.friction = 0.0
    space.add(body, shape)
    return body


def add_floor(height: int) -> None:
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape = pymunk.Segment(body, (0, constants.WINDOW_HEIGHT-height),
                           (constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT-height), 5)

    shape.elasticity = 1
    shape.friction = 0.0
    space.add(body, shape)


def add_slanted_floor(height: int) -> None:
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    shape = pymunk.Segment(body, (100, constants.WINDOW_HEIGHT-height-100),
                           (constants.WINDOW_WIDTH-300, constants.WINDOW_HEIGHT-height + 20), 5)

    shape.elasticity = 1
    shape.friction = .0
    space.add(body, shape)


def main():
    add_floor(20)
    # add_slanted_floor(220)
    box = RectBarrier((50, 50), (60, 60))
    box.add_to_space(space)
    clock = pygame.time.Clock()
    running = True
    held_pos = 0, 0
    while running:
        for x in range(constants.PHYSICS_STEPS_PER_FRAME):
            space.step(constants.DT)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                held_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                offset = mouse_pos[0]-held_pos[0], mouse_pos[1]-held_pos[1]
                force = -offset[0]*400, -offset[1]*400
                add_ball_with_force(held_pos, force)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    add_ball_with_joint(pygame.mouse.get_pos())

        clock.tick(constants.FPS)
        window.fill((255, 255, 255))

        space.debug_draw(pymunk.pygame_util.DrawOptions(window))

        pygame.display.flip()


if __name__ == "__main__":
    main()
