

import pygame
import pymunk

import constants
from physics_object import PhysicsObject


class Ball(PhysicsObject):
    def __init__(self, pos: tuple[int, int], space: pymunk.Space) -> None:
        mass = 1
        self.radius = 30
        inertia = pymunk.moment_for_circle(mass, 0, self.radius, (0, 0))
        self.body = pymunk.Body(mass, inertia)
        self.body.position = pos
        self.shape = pymunk.Circle(self.body, self.radius, (0, 0))
        self.shape.elasticity = .7
        self.shape.friction = 1
        super().__init__(space)

    @property
    def pos(self) -> tuple[int]:
        return self.body.position

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.pos[0]-self.radius, self.pos[1]-self.radius, 2 * self.radius, 2 * self.radius)

    def render(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, constants.Color.BLUE, self.pos, self.radius)

        # drag_constant = 0.0002

        # flight_direction = pymunk.Vec2d(
        #     self.body.velocity[0], self.body.velocity[1])
        # _, flight_speed = flight_direction.normalized_and_length()
        # # (1-abs(dot)) can be replaced with (1-dot) to make arrows turn
        # # around even when fired straight up. Might not be as accurate, but
        # # maybe look better.
        # drag_force_magnitude = (1-abs(flight_direction)) * \
        #     flight_speed ** 2 * drag_constant * self.body.mass
        # self.body.apply_impulse_at_world_point(
        #     drag_force_magnitude * -flight_direction, self.pos)

        self.body.angular_velocity = 0
