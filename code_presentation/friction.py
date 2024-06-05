# ce code est encore incomplet et faux par endroits
from typing import List

import random
from tower import Tower
from constants import TOWER_N_FLOORS
# from game import Game
from constants import BLOCK_MASS, BLOCK_MUS, G, F_INF, F_SUP




import random

def type_of_extraction(z, x, axis, tower: Tower):
    if x==1:
        return "middle"
    else:
        axis_z = tower.axis_layer(z)
        if axis == axis_z:
            return "parallel" # with the torque
        else:
            return "perpendicular" # without torque

# returns a random force between f_inf and f_sup, for example in [0.1 N, 5 N]
def f_app(f_inf, f_sup):
    return random.uniform(f_inf, f_sup)


# returns the mass above the block (x,z), not including the mass of the block (x,z) if there is a block
# if there is no block, returns 0
# recursive
def mass_above(z, x, tower):
    if tower.layout[z][x]:
        height = len(tower.layout)
        if z == height - 1:
            return 0.
        elif z == height - 2:
            nb_blocks_above = sum(tower.layout[z+1])
            return nb_blocks_above * (BLOCK_MASS / 3) 
        else:
            nb_blocks_above = sum(tower.layout[z+1])
            if tower.layout[z+2][x]:
                return (nb_blocks_above * (BLOCK_MASS / 3)) + BLOCK_MASS + mass_above(z+2, x, tower)
            else:
                return (nb_blocks_above * (BLOCK_MASS / 3))
    else:
        return 0.
    

# returns |f_slide| friction force between removed block (x,z) and upper block (x_above, z+1) if possible
def f_slide(z, z_above, x, x_above, tower: Tower):
    if z == len(tower.layout) - 1 or not(tower.layout[z][x]):
        return 0.
    else:
        m_top = BLOCK_MASS + mass_above(z_above, x_above, tower)
        return BLOCK_MUS * m_top * G


# returns |f_bottom| friction force between removed block (x,z) and lower block (x_under, z-1) if possible
def f_bottom(z, x, x_under, tower: Tower):
    # m_bot = 0.
    # n_blocks = 0
    # for i in range(3):
    #     if tower.layout[z][i]:
    #         n_blocks += 1
    # if tower.layout[z-1][x_under]:
    #     m_bot += BLOCK_MASS + (n_blocks * BLOCK_MASS) / 3
    #     f_b = (BLOCK_MUS * m_bot * G)
    if z==0:
        return 0. # no friction force with the support
    else:
        m_bot = mass_above(z-1, x_under, tower)
        return BLOCK_MASS * m_bot * G

def f_app_max(z, x, axis, tower: Tower):
    extraction = type_of_extraction(z, x, axis, tower)
    if extraction == "perpendicular" or extraction == "middle":
        return 5. # no max of Fapp in that case
    else:
        # extraction == "parallel"
        # if there is no f2 : torque is not counteracted => the tower falls
        if not(tower.layout[z][2-x]):
            return F_INF
        else:
            


def max_fs_fb(f_slides, f_bottoms):
    max_sum = 0.
    for i in range(3):
        if f_slides[i] + f_bottoms[i] > max_sum:
            max_sum = f_slides[i] + f_bottoms[i]
    return max_sum


def f_app_min(z, x, axis, tower: Tower):
    # f_app_min does not depend on the type of extraction

    f_slides = [f_slide(z, x, x_above, tower) for x_above in range(3)]
    f_bottoms = [f_bottom(z, x, x_under, tower) for x_under in range(3)]
    

    return max_fs_fb(f_slides, f_bottoms)
