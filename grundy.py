from typing import List
from tower import Tower
from constants import TOWER_N_FLOORS
from game import Game
from constants import FLOOR_SINGLE_SIDE_REVERSED, FLOOR_SINGLE_SIDE, FLOOR_FULL, FLOOR_GLUED, \
    FLOOR_GLUED_REVERSED, TOWER_DEFAULT_LAYOUT

# Minimum Excluded Value of a set
def mex(values: List[int]) -> int:
    for i in range(3) : 
        if i not in values : 
            return i
    return 3

# print(mex([2, 1, 0]))


def next_pos(a1, a2, len): 
    # a1 : row (number of piles of size 1)
    # a2 : column (!= number of piles of size 2 due to the repetitions of the columns 
    # -> 3 columns per number, because of the 3 different states of the clock)
    res = []
    # Vector (-1, 1)
    if a1-1>=0 and a2+1<len: 
        res.append((a1-1, a2+1))
    # Vector (1, -2)
    if a1+1<len and a2-2>=0:
        res.append((a1+1, a2-2))
    # Vector (0, -2)
    if a2-2>=0:
        res.append((a1, a2-2))
    return res


def prev_pos(a1, a2, len):
    # same as next_pos, but we multiply the vectors by -1
    # a1 : row (number of piles of size 1)
    # a2 : column (!= number of piles of size 2 due to the repetitions of the columns 
    # -> 3 columns per number, because of the 3 different states of the clock)
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

# print(prev_pos(0, 0, 11))
# print(prev_pos(0, 1, 11))
# print(prev_pos(1, 0, 11))
# print(prev_pos(3, 5, 11))
# print(prev_pos(10, 10, 11))

# prev = prev_pos(0, 0, 11)
# for (prow, pcol) in prev:
#     print(next_pos(prow, pcol, 11))



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
            next_positions = next_pos(row, column, 11)
            grundy_next = [grundyTable[j][k] for (j,k) in next_positions]
            grundyTable[row][column] = mex(grundy_next) 

    # the other triangle (◢) of the grundy table has to be filled diagonal by diagonal this way :  /,
    # top to bottom and left to right in the table

    for diagonal in range(1, 11):
        for j in range(10, diagonal-1, -1):
            (row, column) = (diagonal-j+10, j)
            next_positions = next_pos(row, column, 11)
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

# def clock_nim (layout: List[List[bool]]) -> 
for ligne in (grundyTable):
    print(ligne)

def clock_nim(game):
    clock = game.tower.layout[-1] % 3
    # layers0 = 0 # nb of layers of size 0 = terminal layer
    # number of layers of size 0 is not necessary for the clock nim position
    layers1 = 0 # nb of layers of size 1 = 1 turn to become terminal layer
    layers2 = 0 # nb of layers of size 2 = 2 turns to become terminal layer
    for floor in game.tower.layout[:-1]:
        if floor==FLOOR_FULL:
            layers2 += 1
        elif floor in [FLOOR_SINGLE_SIDE, FLOOR_SINGLE_SIDE_REVERSED]:
            layers1 += 1
    # period is already known = 3
    return (clock, layers1, layers2)
    

def grundy_number(clock, layers1, layers2):
    # 9-periodicity of the grundy table
    row = layers1 % 9
    column = (3*layers2+clock) % 9
    return grundyTable[row][column]


