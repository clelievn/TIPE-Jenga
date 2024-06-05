import random

from agent import Agent
from tower import Tower
from game import Game
from constants import TOWER_N_FLOORS
# from game import Game
from constants import FLOOR_SINGLE_SIDE_REVERSED, FLOOR_SINGLE_SIDE, FLOOR_FULL, FLOOR_GLUED, \
    FLOOR_GLUED_REVERSED, FLOOR_APART, LEFT, MID, RIGHT
from grundy import *
from friction import mass_above, f_slide, f_slide_tot, f_bottom, f_bottom_tot, f_app_min

def create_random_jenga_tower():
    layout = [random.choice([FLOOR_FULL, FLOOR_GLUED, FLOOR_GLUED_REVERSED, FLOOR_APART]) for _ in range(TOWER_N_FLOORS)]
    layout[-2] = FLOOR_FULL # jenga rules impose that penultimate row is always full
    return Tower(layout)


def print_tower(tower: Tower):
    for row in reversed(tower.layout):
        print(row)
    return


random_tower = create_random_jenga_tower()


print_tower(random_tower)
print("is_stable : ", Tower.is_stable(random_tower))

game = Game(random_tower)
height = len(game.tower.layout)
# # Agent.play(game)
# clock, layers1, layers2 = clock_nim(game)
# print(f"clock = {clock}, layers1 = {layers1}, layers2 = {layers2}")
# row = layers1 % 9
# column = (3*layers2-1+clock) % 9
# grundy_value = grundy_number(clock, row, column)
# print(f"grundy value = {grundy_value}")

# create_new_row = False

# next_positions = next_pos(row, column, game.tower.height, game.tower.height * 3 - 1)
# next_grundy = [grundyTable[next_row][next_col] for (next_row, next_col) in next_positions]
# print("next_positions = ", next_positions)
# print("next_grundy = ", next_grundy)

# # if the position is not winning, we play the move with the highest grundy value 
# # (next player is more likely to play a move with a grundy value > 0)
# if grundy_value == 0:
#     next_grundy_value = next_grundy[index_max(next_grundy)]
#     (next_row, next_col) = next_positions[index_max(next_grundy)]
# else:
#     i=0
#     while i<len(next_grundy) and next_grundy[i]>0:
#         i += 1
#     next_grundy_value = next_grundy[i]
#     (next_row, next_col) = next_positions[i]

# print("next_grundy_value = ", next_grundy_value)

# next_clock = (clock + 1) % 3
# next_layers1 = next_row
# next_layers2 = (next_col - clock + 1) // 3
# we must now choose our move among all the moves that lead to the wanted next position
# moves = get_moves(game, row, column, next_row, next_col)
# print("moves = ", moves)
# vector = (next_row - row, next_col - column)

# (x,z) = random.choice(moves)

# # last row is full
# if game.tower[-1] == [True, True, True]:
#     create_new_row = True

# if create_new_row:
#     new_x = random.choice([LEFT, MID, RIGHT])
# else:
#     new_x = random.choice([i for i in range(3) if game.tower[-1][i] is False])

# print("vector = ", vector)
# print("create_new_row=", create_new_row)
# print("(x,z) = ", (x,z))


# print("\n")
# masses_above = [[mass_above(z, x, game) for x in range(3)] for z in range(height)]
# for row in (reversed(masses_above)):
#     print(row)

# print("\n")
# f_slides = [[f_slide(z, x, game) for x in range(3)] for z in range(height)]

# print("\n")
# for row in (reversed(f_slides)):
#     print(row)


layout1 = [[True, True, True] for _ in range(3)]
tower1 = Tower(layout1)

game1 = Game(tower1)

print("\n")
print_tower(tower1)
height1 = len(game1.tower.layout)

f_slides1 = [[f_slide(z, x, game1) for x in range(3)] for z in range(height1)]

print("\n")
for row in (reversed(f_slides1)):
    print(row)

f_bottoms1 = [[f_bottom(z, x, game1, f_slides1[z]) for x in range(3)] for z in range(height1)]

print("\n")
for row in (reversed(f_bottoms1)):
    print(row)

f_app_mins = [[f_app_min(z, x, game1) for x in range(3)] for z in range(height1)]

print("\n")
for row in (reversed(f_app_mins)):
    print(row)