from constants import LEFT, MID, RIGHT, F_INF, F_SUP
from tower import Tower
from friction import *


class Game:
    """Jenga game class"""

    def __init__(self, tower: Tower = None):
        if tower is None:
            tower = Tower()
        self.tower = tower

    def play(self, position: tuple[int, int], new_position: tuple[int, bool]) -> None:
        """Plays a block from a row/position to a new position"""

        x, z = position
        new_x, create_new_row = new_position
        tower_height = len(self.tower.layout)

        if x not in [LEFT, MID, RIGHT]:
            raise ValueError(f"invalid position: no such position. Must be in [{LEFT}, {MID}, {RIGHT}]")

        if z == -1:
            z = tower_height - 1
        if z < 0 or z >= len(self.tower.layout) - 1:
            raise ValueError(f"invalid position: no such row. Must be in [0, {tower_height - 2}]")

        if new_x not in [LEFT, MID, RIGHT]:
            raise ValueError(f"invalid new_position: no such row. Must be in [{LEFT}, {MID}, {RIGHT}]")

        if create_new_row and sum(self.tower.layout[-1]) != 3:
            raise ValueError(f"invalid new_position: cannot create new row when the last row is not full")

        if not create_new_row:
            if self.tower.layout[-1][new_x] == True:
                raise ValueError(f"invalid new_position: already occupied")

        # take jenga piece
        self.tower[z][x] = False

        # put it back on top
        if create_new_row:
            self.tower.layout.append([False, False, False])
        self.tower[-1][new_x] = True

    def play_friction(self, position: tuple[int, int], new_position: tuple[int, bool], axis) -> None:
        """Plays a block from a row/position to a new position"""

        x, z = position
        new_x, create_new_row = new_position
        tower_height = len(self.tower.layout)

        if x not in [LEFT, MID, RIGHT]:
            raise ValueError(f"invalid position: no such position. Must be in [{LEFT}, {MID}, {RIGHT}]")

        if z == -1:
            z = tower_height - 1
        if z < 0 or z >= len(self.tower.layout) - 1:
            raise ValueError(f"invalid position: no such row. Must be in [0, {tower_height - 2}]")

        if new_x not in [LEFT, MID, RIGHT]:
            raise ValueError(f"invalid new_position: no such row. Must be in [{LEFT}, {MID}, {RIGHT}]")

        if create_new_row and sum(self.tower.layout[-1]) != 3:
            raise ValueError(f"invalid new_position: cannot create new row when the last row is not full")

        if not create_new_row:
            if self.tower.layout[-1][new_x] == True:
                raise ValueError(f"invalid new_position: already occupied")

        missed_extraction = False
        f_applied_max = f_app_max(z, x, axis, self.tower)
        f_applied_min = f_app_min(z, x, axis, self.tower)
        f_applied = f_app(F_INF, F_SUP)

        if (f_applied > f_applied_max or f_applied < f_applied_min):
            missed_extraction = True # the player pulled the block with too much / little force => he missed the extraction

        # take jenga piece
        self.tower[z][x] = False

        # put it back on top
        if create_new_row:
            self.tower.layout.append([False, False, False])
        self.tower[-1][new_x] = True

        return missed_extraction

    def is_game_over(self):
        """Determines whether the game is over"""
        return (not self.tower.is_stable()) or self.tower.is_terminal()
