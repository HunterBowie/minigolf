
import pygame
import pymunk

import util
from game.ball import Ball
from game.constants import DT, PHYSICS_STEPS_PER_FRAME
from game.course import Course


class Game:
    def __init__(self, screen: pygame.Surface) -> None:
        self.putt_count = 0
        self.is_over = False
        self.screen = screen
        self.space = pymunk.Space()
        self.course = Course("0001", self.space, screen)
        self.ball = Ball((350, 100), util.load_image(
            "ball_blue_large_alt", "assets"), self.course.space, self.screen)
        self.timer = util.Timer()
        self.held_pos = 0, 0
        self.mouse_held = False

    def update(self) -> None:

        mouse_pos = pygame.mouse.get_pos()
        for x in range(PHYSICS_STEPS_PER_FRAME):
            self.space.step(DT)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.ball.rect.collidepoint(mouse_pos):
                    self.held_pos = pygame.mouse.get_pos()
                    self.mouse_held = True
            if event.type == pygame.MOUSEBUTTONUP and self.mouse_held:
                offset = mouse_pos[0] - \
                    self.held_pos[0], mouse_pos[1]-self.held_pos[1]
                force = -offset[0]*400, -offset[1]*400
                self.ball.body.apply_force_at_local_point(force, (0, 0))
                self.timer.start()
                self.mouse_held = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.course.shift((0, -10))
            self.ball.move((0, -10))
        if keys[pygame.K_DOWN]:
            self.course.shift((0, 10))
            self.ball.move((0, 10))
        if keys[pygame.K_LEFT]:
            self.course.shift((-10, 0))
            self.ball.move((-10, 0))
        if keys[pygame.K_RIGHT]:
            self.course.shift((10, 0))
            self.ball.move((10, 0))

        if self.timer.passed(4):
            velocity_copy = pymunk.Vec2d(
                self.ball.body.velocity[0], self.ball.body.velocity[1])
            direction, speed = velocity_copy.normalized_and_length()
            self.ball.body.apply_impulse_at_local_point(
                (.07 * -direction.x * speed, .07 * -direction.y * speed), (0, 0))

        if self.mouse_held:
            pygame.draw.line(self.screen, util.Color.BLACK,
                             mouse_pos, self.ball.rect.center, width=4)

        self.ball.update()
        self.course.update()
