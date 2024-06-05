from typing import List
from tower import Tower
from constants import TOWER_N_FLOORS, SIZE_1, SIZE_2
from game import Game
from constants import FLOOR_SINGLE_SIDE_REVERSED, FLOOR_SINGLE_SIDE, FLOOR_FULL, FLOOR_GLUED, \
    FLOOR_GLUED_REVERSED, TOWER_DEFAULT_LAYOUT

# Minimum Excluded Value of a set
def mex(values: List[int]) -> int:
    for i in range(3) : 
        if i not in values : 
            return i
    return 3

def index_max(values):
    # returns the index of the maximum value of the array
    if len(values) == 1:
        return 0
    else:
        res = 0
        for i in range(1, len(values)):
            if values[res] < values[i]:
                res = i
        return res


def next_pos(row, col, nb_rows, nb_col): 
    # a1 : row (number of piles of size 1)
    # a2 : column (!= number of piles of size 2 due to the repetitions of the columns)
    # -> 3 columns per number except 0, because of the 3 different states of the clock)
    res = []
    # Vector (-1, 1)
    if row-1>=0 and col+1<nb_col-1: 
        res.append((row-1, col+1))
    # Vector (1, -2)
    if row+1<nb_rows-1 and col-2>=0:
        res.append((row+1, col-2))
    # Vector (0, -2)
    if col-2>=0:
        res.append((row, col-2))
    return res


def prev_pos(a1, a2, len):
    # same as next_pos, but we multiply the vectors by -1
    res = []
    # Vector (1, -1)
    if a1+1<len and a2-1>=0: 
        res.append((a1+1, a2-1))
    # Vector (-1, 2)
    if a1-1>=0 and a2+2<len:
        res.append((a1-1, a2+2))
    # Vector (0, 2)
    if a1+2<len:
        res.append((a1, a2+2))
    return res


def grundy_table() -> List[List[int]]:
    # Thanks to the periodicity of the grundy table, we can calculate
    # grundy values only for the first 11x11 table. 
    # At first, we fill it with -1, so that we can still use the 
    # mex function to calculate grundy values.
    grundyTable = [[-1 for i in range(11)] for j in range(11)]

    grundyTable[0][0] = 0
    grundyTable[0][1] = 0
    grundyTable[1][0] = mex([grundyTable[0][0], grundyTable[0][1]]) # = mex(0,0) = 1

    # the first triangle (◤) of the grundy table has to be filled diagonal by diagonal this way :  /,
    # top to bottom and left to right in the table

    for diagonal in range(2, 11):
        for i in range(diagonal, -1, -1):
            (row, column) = (diagonal-i, i)
            next_positions = next_pos(row, column, 11, 11)
            grundy_next = [grundyTable[j][k] for (j,k) in next_positions]
            grundyTable[row][column] = mex(grundy_next) 

    # the other triangle (◢) of the grundy table has to be filled diagonal by diagonal this way :  /,
    # top to bottom and left to right in the table

    for diagonal in range(1, 11):
        for j in range(10, diagonal-1, -1):
            (row, column) = (diagonal-j+10, j)
            next_positions = next_pos(row, column, 11, 11)
            if column==10:
                next_positions.append((row-1, 2)) # periodicity of the table
            if row==10:
                next_positions.append((2, column-2)) # idem
            grundy_next = [grundyTable[j][k] for (j,k) in next_positions]
            grundyTable[row][column] = mex(grundy_next) 

    # once the first square is filled, we can use the 
    # periodicity of the grundy values to fill the rest of the table       
    
    return grundyTable

grundyTable = grundy_table()

def forbidden_rows(game: Game):
    if game.tower.layout[-1] == FLOOR_FULL:
        return 1
    else:
        return 2

def clock_nim(game: Game):
    clock_value = sum(game.tower.layout[-1]) % 3
    # number of layers of size 0 is not necessary for the clock nim position
    layers1 = 0 # nb of layers of size 1 = 1 turn to become terminal layer
    layers2 = 0 # nb of layers of size 2 = 2 turns to become terminal layer
    nb_forbidden_rows = forbidden_rows(game)
    for floor in game.tower.layout[:-nb_forbidden_rows]:
        if floor==FLOOR_FULL:
            layers2 += 1
        elif floor in [FLOOR_GLUED, FLOOR_GLUED_REVERSED]:
            layers1 += 1
    return (clock_value, layers1, layers2)
    

def grundy_number(clock, row, column):
    # 9-periodicity of the grundy table
    # row = layers1 % 9
    # column = (3*layers2-1+clock) % 9 
    return grundyTable[row][column]


def get_moves(game: Game, row, column, new_row, new_column):
    vector = (new_row - row, new_column - column)
    nb_forbidden_rows = forbidden_rows(game)
    nb_allowed_floors = len(game.tower.layout) - nb_forbidden_rows

    # blocks contains coordinates of all the blocks that can be removed to get to the new position 
    blocks = []

    if vector not in [(0, -2), (1, -2), (-1, 1)]:
        raise ValueError(f"invalid vector")

    if vector == (0, -2):
        # remove middle block from a pile of size 2 (=> remove 1 pile of size 2)
        for i in range(nb_allowed_floors):
            layer = game.tower.layout[i]
            if layer in SIZE_2:
                blocks.append((1, i)) # remove middle block

    elif vector == (1, -2):
        # remove 1 lateral block from a pile of size 2 (=> remove 1 pile of size 2, add 1 pile of size 1)
        for i in range(nb_allowed_floors):
            layer = game.tower.layout[i]
            if layer in SIZE_2:
                # remove side block
                blocks.append((0, i))
                blocks.append((2, i)) 

    else: # vector == (-1,1)
        # remove 1 lateral block from a pile of size 1 (=> remove 1 pile of size 1)
        for i in range(nb_allowed_floors):
            layer = game.tower.layout[i]
            if layer in SIZE_1:
                # remove side block 
                if layer == FLOOR_GLUED:
                    blocks.append((0, i)) 
                else:
                    blocks.append((2, i))

    return blocks


    