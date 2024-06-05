from typing import List

from constants import FLOOR_SINGLE_SIDE_REVERSED, FLOOR_SINGLE_SIDE, FLOOR_APART, FLOOR_MIDDLE, FLOOR_FULL,\
    TOWER_DEFAULT_LAYOUT


class Tower(object):
    """Attributes:
        layout  : List[List[bool]]
            A list of lists representing the current layout of the tower. The first list represents the bottom row of
            the tower, the second list represents the second row of the tower, and so on. Each list contains booleans
            representing whether a block is present in that position.

            example : [[True, False, True], [False, True, False]] 
    """

    def __init__(self, layout: List[List[bool]] = None):
        if layout is None:
            layout = TOWER_DEFAULT_LAYOUT

        if layout == [[]]:
            layout = []

        if not Tower._is_valid(layout):
            raise ValueError("invalid `layout` parameter, must be of type List[List[bool]]")
        self.layout = layout
        self.height = len(self.layout)

    
    def _is_valid(layout: List[List[bool]]) -> bool:
        """Determines whether a layout is valid"""
        if len(layout) == 0:
            return True  # [] is ok
        if len(layout) == 1 and len(layout[0]) == 0:
            return True  # [[]] is ok

        n_floors = len(layout)
        for i in range(n_floors):
            floor = layout[i]
            if len(floor) != 3:
                return False
            if sum(floor) == 0 and i < n_floors - 1:
                return False  # floating blocks
        return True

    def _is_stable(layout: List[List[bool]]) -> bool:
        """Determines whether a layout is stable"""
        if len(layout) == 1:
            return True
        if layout[-1] == FLOOR_FULL:
            nb_forbidden_rows = 1
        else:
            nb_forbidden_rows = 2

        for floor in layout[:-nb_forbidden_rows]:  # skip last floor(s) (cannot play with blocks from last completed row)
            if floor in [FLOOR_SINGLE_SIDE, FLOOR_SINGLE_SIDE_REVERSED, [False, False, False]]:
                return False
        return True

    def is_stable(self) -> bool:
        return Tower._is_stable(self.layout)


    def _is_terminal(layout: List[List[bool]]) -> bool:
        """Determines whether a layout is terminal"""
        if len(layout) == 1:
            return True
        if layout[-1] == FLOOR_FULL:
            nb_forbidden_rows = 1
        else:
            nb_forbidden_rows = 2

        for floor in layout[:-nb_forbidden_rows]:  # skip last floor(s) (cannot play with blocks from last completed row)
            if floor not in [FLOOR_MIDDLE, FLOOR_APART]:
                return False   
        return True

    def is_terminal(self) -> bool:
        return Tower._is_terminal(self.layout)
    
    def axis_layer(self, z):
        if z % 2 == 0:
            return "x"
        else:
            return "y"
