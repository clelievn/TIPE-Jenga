import random

from constants import LEFT, MID, RIGHT
from game import Game


class Agent:
    AVAILABLE_MODES = ["random"]

    def __init__(self, mode: str = "random"):
        if mode not in Agent.AVAILABLE_MODES:
            raise ValueError(f"invalide `type` parameter, must be one of {Agent.AVAILABLE_MODES} but {mode} was given.")

        self.mode = mode

    def play(self, game: Game):
        if self.mode == "random":
            Agent._play_random(game)

    def _play_random(game: Game):
        y = random.randint(0, game.tower.height - 1)
        x = random.choice([i for i in range(3) if game.tower[y][i] is True])
        create_new_row = random.choice([True, False])

        # last row is full
        if game.tower[-1] == [True, True, True]:
            create_new_row = True

        if create_new_row:
            new_x = random.choice([LEFT, MID, RIGHT])
        else:
            new_x = random.choice([i for i in range(3) if game.tower[-1][i] is False])
        game.play((x, y), (new_x, create_new_row))
