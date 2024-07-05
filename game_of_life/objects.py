import random
from typing import Optional

import pygame


class Rect:
    def __init__(self, pos_x, pos_y, width, height):
        self.rect = pygame.Rect(pos_x, pos_y, width, height)
        self.color = "black"
        self.clicked_color = "white"
        self.is_clicked = False
        self._debug_color = "red"

    def draw(self, screen, debug=False):
        if debug:
            current_color = self._debug_color
        else:
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
                pos_x = (
                    x * self.rect_width + x * self.border_size + self.border_size / 2
                )
                pos_y = (
                    y * self.rect_height + y * self.border_size + self.border_size / 2
                )
                rect = Rect(pos_x, pos_y, self.rect_width, self.rect_height)
                rand_state = random.randint(0, 1) if self.random else 0
                rect.is_clicked = bool(rand_state)
                row.append(rect)

            self.rects.append(row)

    def update_collided_rect(self, pos) -> Optional[Rect]:
        for rect_row in self.rects:
            for rect in rect_row:
                rect.check_click(pos)

    def draw(self, is_paused=False):
        self.snapshot = self._generate_snapshot()
        for p_y, rect_row in enumerate(self.snapshot):
            for p_x, rect_state in enumerate(rect_row):
                rect = self.rects[p_y][p_x]
                if not is_paused:
                    self._simulate(p_x, p_y, rect_state)

                rect.draw(self.screen)

    def _simulate(self, p_x: int, p_y: int, rect_state: int):
        n = self._get_alive_neighbour_count(p_x, p_y)

        rect = self.rects[p_y][p_x]

        if rect_state == 1:
            if n < 2:
                rect.is_clicked = False
            elif n in {2, 3}:
                rect.is_clicked = True
            elif n > 3:
                rect.is_clicked = False
        else:
            if n == 3:
                rect.is_clicked = True

    def _get_alive_neighbour_count(self, pos_x, pos_y) -> int:
        count = 0
        for p_x, p_y in self.DIRECTIONS:
            row, col = p_y + pos_y, p_x + pos_x
            if 0 <= row < self.height and 0 <= col < self.width:
                rect_state = self.snapshot[row][col]
                count += rect_state

        return count

    def _generate_snapshot(self) -> list[list[int]]:
        snapshot = []
        for row in self.rects:
            snapshot_row = []
            for rect in row:
                snapshot_row.append(1 if rect.is_clicked else 0)

            snapshot.append(snapshot_row)

        return snapshot
