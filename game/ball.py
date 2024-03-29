

import pygame
import pymunk
import pymunk.pygame_util

import game.constants as constants
import util


class Ball:
    def __init__(self, pos: tuple[int, int], image: pygame.Surface, space: pymunk.Space, screen: pygame.Surface) -> None:
        mass = 1
        self.radius = image.get_width()//2
        inertia = pymunk.moment_for_circle(mass, 0, self.radius, (0, 0))
        self.body = pymunk.Body(mass, inertia)
        self.body.position = pymunk.pygame_util.from_pygame(pos, screen)
        self.shape = pymunk.Circle(self.body, self.radius, (0, 0))
        self.shape.elasticity = .7
        self.shape.friction = 1
        self.image = image
        self.screen = screen
        space.add(self.body, self.shape)

    def move(self, pos_change: tuple[int, int]) -> None:
        pos_change = pymunk.pygame_util.from_pygame(pos_change, self.screen)
        self.body.position = self.body.position[0] + \
            pos_change[0], self.body.position[1] + pos_change[1]

    @property
    def pos(self) -> tuple[int]:
        return self.body.position

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.pos[0]-self.radius, self.pos[1]-self.radius, 2 * self.radius, 2 * self.radius)

    def update(self) -> None:
        self.screen.blit(self.image, self.rect)
