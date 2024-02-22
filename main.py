from __future__ import annotations
from typing import Callable, Generator
from pathlib import Path
import curses
import time


class Pattern:
    def __init__(self, path: Path) -> None:
        self._path = path
        self.pattern = self._read()

    def _read(self) -> list[str]:
        with open(self._path, "r", encoding="utf-8") as f:
            content = f.read().splitlines()
        return content


class Grid:
    def __init__(self, width, height):
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.width = width
        self.height = height

    @classmethod
    def from_pattern(cls, pattern: Pattern) -> Grid:
        g = Grid(len(pattern.pattern[0]), len(pattern.pattern))
        g.grid = [
            [int(j) for j in i.replace(".", "0").replace("x", "1")]
            for i in pattern.pattern
        ]
        return g

    def __str__(self) -> str:
        return "\n".join(
            [
                " ".join([str(j).replace("0", ".").replace("1", "#") for j in i])
                for i in self.grid
            ]
        )

    def __iter__(self) -> Generator[tuple[tuple[int, int], int], None, None]:
        for x, i in enumerate(self.grid):
            for y, j in enumerate(i):
                yield (x, y), j


class Simulator:
    dir = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))

    def __init__(self, grid: Grid) -> None:
        self._grid = grid

    def get_neighbour_count(self, y: int, x: int) -> int:
        count = 0
        for i, j in self.dir:
            col, row = j + y, i + x
            if 0 <= row < self._grid.width and 0 <= col < self._grid.height:
                value = self._grid.grid[col][row]
                count += value

        return count

    def simulate(self) -> Grid:
        new_grid = Grid(self._grid.width, self._grid.height)
        for (y, x), value in self._grid:
            n = self.get_neighbour_count(y, x)

            if value == 1:
                if n < 2:
                    new_grid.grid[y][x] = 0
                elif n in {2, 3}:
                    new_grid.grid[y][x] = 1

                elif n > 3:
                    new_grid.grid[y][x] = 0
            else:
                if n == 3:
                    new_grid.grid[y][x] = 1

        self._grid = new_grid
        return new_grid


class ConsoleRenderer:
    def __init__(self, stdscr, render: Callable, timeout: float) -> None:
        curses.curs_set(0)
        self.stdscr = stdscr
        self.render = render
        self.timeout = timeout

    def draw(self) -> None:
        self.stdscr.clear()
        while True:
            self.stdscr.clear()
            self.stdscr.addstr(str(self.render()))
            self.stdscr.refresh()
            time.sleep(self.timeout)


def main(stdscr):
    pattern = Pattern(Path(__file__).parent / "patterns/pattern_01.txt")
    grid = Grid.from_pattern(pattern)
    sim = Simulator(grid)
    renderer = ConsoleRenderer(stdscr, sim.simulate, 0.25)
    renderer.draw()


if __name__ == "__main__":
    curses.wrapper(main)
