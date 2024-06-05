import random

from constants import LEFT, MID, RIGHT
from game import Game
from tower import Tower
from grundy import grundyTable, clock_nim, grundy_number, next_pos, index_max, get_moves, forbidden_rows
from friction import f_app_max, f_app_min


class Agent:
    AVAILABLE_MODES = ["random", "grundy", "grundy_friction"]

    def __init__(self, mode: str):
        if mode not in Agent.AVAILABLE_MODES:
            raise ValueError(f"invalide `type` parameter, must be one of {Agent.AVAILABLE_MODES} but {mode} was given.")

        self.mode = mode

    def play(self, game: Game):
        if self.mode == "random":
            Agent._play_random(game)
        if self.mode == "grundy":
            Agent._play_grundy(game)
        if self.mode == "grundy_friction":
            Agent._play_grundy_friction(game)


    def _play_random(game: Game):
        nb_forbidden_rows = forbidden_rows(game)
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
        # game.play((x, z), (new_x, create_new_row))
        game.play_friction((x, z), (new_x, create_new_row))

    def play_grundy(game: Game):
        # winning position : grundy_value = 0
        clock, layers1, layers2 = clock_nim(game)
        row = layers1 
        column = (3*layers2-1+clock)  
        create_new_row = False

        grundy_value = grundy_number(clock, row % 9, column % 9)

        next_positions = next_pos(row, column, game.tower.height, game.tower.height * 3 - 1)
        next_grundy = [grundyTable[next_row % 9][next_col % 9] for (next_row, next_col) in next_positions]

        # if the position is not winning, we play the move with the highest grundy value 
        # (next player is more likely to play a move with a grundy value > 0)
        if grundy_value == 0:
            (next_row, next_col) = next_positions[index_max(next_grundy)]
        else:
            i=0
            while i<len(next_grundy) and next_grundy[i]>0:
                i += 1
            (next_row, next_col) = next_positions[i]
        
        # we must now choose our move among all the moves that lead to the wanted next position
        moves = get_moves(game, row, column, next_row, next_col)
        (x,z) = random.choice(moves)

        # last row is full
        if game.tower[-1] == [True, True, True]:
            create_new_row = True

        if create_new_row:
            new_x = random.choice([LEFT, MID, RIGHT])
        else:
            new_x = random.choice([i for i in range(3) if game.tower[-1][i] is False])

        if x == 1: # middle block
            axis = game.tower.axis_layer(z)
        else:
            axis = random.choice(["x", "y"])
        # game.play((x, z), (new_x, create_new_row))
        return game.play_friction((x, z), (new_x, create_new_row), axis)

    def play_grundy_friction(game: Game):
        # winning position : grundy_value = 0
        clock, layers1, layers2 = clock_nim(game)
        row = layers1 
        column = (3*layers2-1+clock)  
        create_new_row = False

        grundy_value = grundy_number(clock, row % 9, column % 9)

        next_positions = next_pos(row, column, game.tower.height, game.tower.height * 3 - 1)
        next_grundy = [grundyTable[next_row % 9][next_col % 9] for (next_row, next_col) in next_positions]

        # if the position is not winning, we play the move with the highest grundy value 
        # (next player is more likely to play a move with a grundy value > 0)
        if grundy_value == 0:
            (next_row, next_col) = next_positions[index_max(next_grundy)]
        else:
            i=0
            while i<len(next_grundy) and next_grundy[i]>0:
                i += 1
            (next_row, next_col) = next_positions[i]
        
        # we must now choose our move among all the moves that lead to the wanted next position
        moves = get_moves(game, row, column, next_row, next_col)

        (x, z) = moves[0]   # moves is never empty
        axis = "x" # initialization of (x, z, axis)

        f_applied_min = 20.
        for move in moves:
            (x_move,z_move) = move
            axis_z = game.tower.axis_layer(z)

            if x_move==1: # middle block
                axis_extraction = axis_z
                f_app_min_move = f_app_min(z_move, x_move, axis_extraction, game.tower)
                # f_app_max_move = f_app_max(z_move, x_move, axis_extraction, game.tower) # no f_app_max in that case
                if f_app_min_move < f_applied_min:
                    f_applied_min = f_app_min_move
                    (x, z, axis) = (x_move, z_move, axis_extraction)

            else: # lateral block
                # no f_app_max if the extraction is perpendicular => safer to extract perpendicularly
                if axis_z == "x":
                    axis_extraction = "y"
                else:
                    axis_extraction = "x"
                # f_app_max_move_x = f_app_max(z_move, x_move, "x", game.tower)
                # f_app_max_move_y = f_app_max(z_move, x_move, "y", game.tower)
                f_app_min_move = f_app_min(z_move, x_move, axis_extraction, game.tower)

                if f_app_min_move < f_applied_min:
                    f_applied_min = f_app_min_move
                    (x, z, axis) = (x_move, z_move, axis_extraction)
                # elif f_app_max_move_y > f_applied_max:
                #     f_applied_max = f_app_max_move
                #     (x, z, axis) = (x_move, z_move, "y")

        # last row is full
        if game.tower[-1] == [True, True, True]:
            create_new_row = True

        if create_new_row:
            new_x = random.choice([LEFT, MID, RIGHT])
        else:
            new_x = random.choice([i for i in range(3) if game.tower[-1][i] is False])
        # game.play((x, z), (new_x, create_new_row))
        return game.play_friction((x, z), (new_x, create_new_row), axis)        
