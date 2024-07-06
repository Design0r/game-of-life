from abc import ABC, abstractmethod

import pygame

from .objects import Grid, State


class Game(ABC):
    def __init__(
        self, screen_size: tuple[int, int], fps: int, window_name: str = "Game Window"
    ) -> None:
        self.fps = fps
        self.screen = pygame.display.set_mode(screen_size)
        self.clock = pygame.time.Clock()
        self.running = True
        self.window_name = window_name
        self.dt = 0

    def _init(self):
        pygame.init()
        pygame.display.set_caption(self.window_name)

    def _quit(self):
        pygame.quit()

    def run(self):
        self._init()
        self.game_loop()
        self._quit()

    @abstractmethod
    def game_loop(self) -> None: ...


class GameOfLife(Game):
    def __init__(
        self,
        screen_size: tuple[int, int],
        pause_fps: int,
        sim_fps: int,
        random_fill=False,
        grid_size: tuple[int, int] = (50, 50),
    ) -> None:
        self.state = State.Drawing
        self.sim_fps = sim_fps
        self.pause_fps = pause_fps
        self.random_fill = random_fill
        self.bg_color = (100, 100, 40)
        self.grid_size = grid_size
        super().__init__(
            screen_size,
            pause_fps,
            window_name=f"Game of Life {self.grid_size[0]}x{self.grid_size[1]}",
        )

    def game_loop(self) -> None:
        self.grid = Grid(
            self.screen, self.grid_size, border_size=1, random=self.random_fill
        )
        while self.running:
            self._poll_events()
            self._check_pause()

            self.screen.fill(self.bg_color)
            self.grid.draw(self.state)

            pygame.display.flip()
            self.dt = self.clock.tick(self.fps) / 1000

    def _poll_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.grid.update_collided_rect(event.pos)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.state = State.toggle(self.state)

    def _check_pause(self):
        if self.state == State.Drawing:
            self.bg_color = (200, 100, 40)
            self.fps = self.pause_fps
        else:
            self.bg_color = (40, 40, 40)
            self.fps = self.sim_fps
