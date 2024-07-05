import sys

from game_of_life.game import GameOfLife


def main():
    game = GameOfLife(
        screen_size=(1000, 1000),
        pause_fps=60,
        sim_fps=10,
        random_fill=True,
        grid_size=(100, 100),
    )
    sys.exit(game.run())


if __name__ == "__main__":
    main()
