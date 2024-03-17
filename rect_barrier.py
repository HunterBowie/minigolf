import pygame
import pymunk

import constants
from physics_object import PhysicsObject


class RectBarrier(PhysicsObject):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], space: pymunk.Space) -> None:
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.shape = pymunk.Poly(self.body, [
            self.rect.topleft, self.rect.topright, self.rect.bottomleft, self.rect.bottomright])

        self.shape.elasticity = .7
        self.shape.friction = 1
        super().__init__(space)

    @property
    def pos(self) -> tuple[int]:
        return self.rect.topleft

    def render(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, constants.Color.GREEN, self.rect)
