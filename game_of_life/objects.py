from __future__ import annotations

import random
from enum import Enum, auto
from typing import Optional

import pygame


class State(Enum):
    Drawing = auto()
    Simulating = auto()

    @staticmethod
    def toggle(state: State) -> State:
        return State.Simulating if state == State.Drawing else State.Drawing


class Rect:
    def __init__(self, pos_x, pos_y, width, height):
        self.rect = pygame.Rect(pos_x, pos_y, width, height)
        self.color = "black"
        self.clicked_color = "white"
        self.is_clicked = False
        self._debug_color = "red"

    def draw(self, screen):
        current_color = self.clicked_color if self.is_clicked else self.color
        pygame.draw.rect(screen, current_color, self.rect)

    def check_click(self, mouse_pos) -> bool:
        if self.rect.collidepoint(mouse_pos):
            self.is_clicked = not self.is_clicked
            return True

        return False


class Grid:
    DIRECTIONS = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))

    def __init__(
        self,
        screen: pygame.Surface,
        size: tuple[int, int],
        border_size=10,
        random=False,
    ) -> None:
        self.screen = screen
        self.width, self.height = size
        self.border_size = border_size
        self.rect_width = (self.screen.get_width() // self.width) - self.border_size
        self.rect_height = (self.screen.get_height() // self.height) - self.border_size
        self.random = random

        self.rects: list[list[Rect]] = []
        self._init_grid()

    def _init_grid(self):
        for y in range(self.height):
            row = []
            for x in range(self.width):
                pos_x = x * (self.rect_width + self.border_size) + self.border_size // 2
                pos_y = (
                    y * (self.rect_height + self.border_size) + self.border_size // 2
                )

                rect = Rect(pos_x, pos_y, self.rect_width, self.rect_height)
                rect.is_clicked = bool(random.randint(0, 1)) if self.random else False
                row.append(rect)

            self.rects.append(row)

    def update_collided_rect(self, pos) -> Optional[Rect]:
        for rect_row in self.rects:
            for rect in rect_row:
                rect.check_click(pos)

    def draw(self, game_state: State):
        self.snapshot = [[int(rect.is_clicked) for rect in row] for row in self.rects]
        for p_y, rect_row in enumerate(self.snapshot):
            for p_x, rect_state in enumerate(rect_row):
                rect = self.rects[p_y][p_x]
                if game_state == State.Simulating:
                    self._simulate(p_x, p_y, rect_state)

                rect.draw(self.screen)

    def _simulate(self, p_x: int, p_y: int, rect_state: int):
        n = self._get_alive_neighbour_count(p_x, p_y)

        rect = self.rects[p_y][p_x]

        if rect_state == 1:
            rect.is_clicked = n in {2, 3}
        else:
            rect.is_clicked = n == 3

    def _get_alive_neighbour_count(self, pos_x, pos_y) -> int:
        count = 0
        for dx, dy in self.DIRECTIONS:
            ny, nx = dy + pos_y, dx + pos_x
            if 0 <= ny < self.height and 0 <= nx < self.width:
                count += self.snapshot[ny][nx]

        return count
