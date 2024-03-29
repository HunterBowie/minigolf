import pygame
import pymunk
import pymunk.pygame_util

import game.constants as constants
import util


class Block:
    def __init__(self, pos: tuple[int, int], image: pygame.Surface, space: pymunk.Space, screen: pygame.Surface) -> None:
        self.screen = screen
        self.image = image
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.rect = pygame.Rect(
            pos[0], pos[1], image.get_width(), image.get_height())
        self.shape = pymunk.Poly(self.body, [
            self.rect.topleft, self.rect.topright, self.rect.bottomleft, self.rect.bottomright])

        self.shape.elasticity = 1
        self.shape.friction = 1
        space.add(self.body, self.shape)

    @property
    def pos(self) -> tuple[int]:
        return self.rect.topleft

    def move(self, pos_change: tuple[int, int]) -> None:
        pos_change = pymunk.pygame_util.from_pygame(pos_change, self.screen)
        self.body.position = self.body.position[0] + \
            pos_change[0], self.body.position[1] + pos_change[1]

    def update(self) -> None:
        self.screen.blit(self.image, self.body.position)
