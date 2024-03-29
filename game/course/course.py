import json

import pygame
import pymunk

import util
from game.course.block import Block
from game.course.hole import Hole
from game.course.key import Key


class Course:
    def __init__(self, course_id: str, space: pymunk.Space, screen: pygame.Surface) -> None:
        self.screen = screen
        self.space = space
        data = json.load(open(f'courses/{course_id}.json'))
        self.blocks = [Block(block_data['pos'], util.load_image(block_data["id"], "assets/blocks"),
                             self.space, self.screen) for block_data in data["blocks"]]

    def shift(self, pos_change: tuple[int, int]) -> None:
        for block in self.blocks:
            block.move(pos_change)

    def update(self) -> None:
        for block in self.blocks:
            block.update()
