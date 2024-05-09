import random

from constants import LEFT, MID, RIGHT
from game import Game
from grundy import grundyTable, clock_nim, grundy_number, next_pos, index_max, get_moves, forbidden_rows


class Agent:
    AVAILABLE_MODES = ["random", "grundy"]

    def __init__(self, mode: str):
        if mode not in Agent.AVAILABLE_MODES:
            raise ValueError(f"invalide `type` parameter, must be one of {Agent.AVAILABLE_MODES} but {mode} was given.")

        self.mode = mode

    def play(self, game: Game):
        if self.mode == "random":
            Agent._play_random(game)
        if self.mode == "grundy":
            Agent._play_grundy(game)


    def _play_random(game: Game):
        nb_forbidden_rows = forbidden_rows(game)
        print("height = ", len(game.tower.layout))
        z = random.randint(0, game.tower.height - nb_forbidden_rows - 1)
        x = random.choice([i for i in range(3) if game.tower[z][i] is True])
        create_new_row = False

        # last row is full
        if game.tower[-1] == [True, True, True]:
            create_new_row = True

        if create_new_row:
            new_x = random.choice([LEFT, MID, RIGHT])
        else:
            new_x = random.choice([i for i in range(3) if game.tower[-1][i] is False])
        game.play((x, z), (new_x, create_new_row))

    def _play_grundy(game: Game):
        # winning position : grundy_value = 0
        clock, layers1, layers2 = clock_nim(game)
        print(f"clock = {clock}, layers1 = {layers1}, layers2 = {layers2}")
        row = layers1 
        column = (3*layers2-1+clock)  
        create_new_row = False

        grundy_value = grundy_number(clock, row % 9, column % 9)
        print("grundy_value = ", grundy_value)

        next_positions = next_pos(row, column, game.tower.height, game.tower.height * 3 - 1)
        next_grundy = [grundyTable[next_row % 9][next_col % 9] for (next_row, next_col) in next_positions]
        print("next_positions = ", next_positions)
        print("next_grundy = ", next_grundy)

        # if the position is not winning, we play the move with the highest grundy value 
        # (next player is more likely to play a move with a grundy value > 0)
        if grundy_value == 0:
            print("index_max = ", index_max(next_grundy))
            (next_row, next_col) = next_positions[index_max(next_grundy)]
        else:
            i=0
            while i<len(next_grundy) and next_grundy[i]>0:
                i += 1
            (next_row, next_col) = next_positions[i]
        
        # next_clock = (clock + 1) % 3
        # next_layers1 = next_row
        # next_layers2 = (next_col - clock + 1) // 3
        # we must now choose our move among all the moves that lead to the wanted next position
        moves = get_moves(game, row, column, next_row, next_col)
        print("moves = ", moves)

        (x,z) = random.choice(moves)

        # last row is full
        if game.tower[-1] == [True, True, True]:
            create_new_row = True

        if create_new_row:
            new_x = random.choice([LEFT, MID, RIGHT])
        else:
            new_x = random.choice([i for i in range(3) if game.tower[-1][i] is False])
        game.play((x, z), (new_x, create_new_row))
