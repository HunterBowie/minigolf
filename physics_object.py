
from abc import ABC, abstractmethod

import pygame
import pymunk


class PhysicsObject(ABC):
    def __init__(self, space: pymunk.Space):
        self.space = space
        self.space.add(self.body, self.shape)

    @property
    @abstractmethod
    def pos(self) -> tuple[int]:
        "The position of the Physics Object."

    @abstractmethod
    def render(self, screen: pygame.Surface) -> None:
        "Render the Physics Object onto the screen."
