from constants import LEFT, MID, RIGHT
from tower import Tower


class Game:
    """Jenga game class"""

    def __init__(self, tower: Tower = None):
        if tower is None:
            tower = Tower()
        self.tower = tower

    def fresh_play(self, position: tuple[int, int], new_position: tuple[int, bool]) -> None:
        """Plays a block from a row/position to a new position and returns the new tower without modifying the current tower"""
        x, z = position
        new_x, create_new_row = new_position
        tower_height = len(self.tower.layout)

        new_layout = self.tower.layout.copy()
        new_tower = Tower(new_layout)

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
        new_tower[z][x] = False

        # put it back on top
        if create_new_row:
            new_layout.append([False, False, False])
        new_tower[-1][new_x] = True

        return new_tower



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

    def is_game_over(self):
        """Determines whether the game is over"""
        return (not self.tower.is_stable()) or self.tower.is_terminal()
