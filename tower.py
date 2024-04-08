from typing import List

from constants import FLOOR_SINGLE_SIDE_REVERSED, FLOOR_SINGLE_SIDE, FLOOR_FULL, FLOOR_GLUED, \
    FLOOR_GLUED_REVERSED, TOWER_DEFAULT_LAYOUT


class Tower(object):
    """A jenga tower

    Attributes:
        layout  : List[List[bool]]
            A list of lists representing the current layout of the tower. The first list represents the bottom row of
            the tower, the second list represents the second row of the tower, and so on. Each list contains booleans
            representing whether a block is present in that position.

            For example, the layout [[True, False, True], [False, True, False]] represents a tower with two rows,
            the first row having blocks in the first and third positions, and the second row having a block in the
            second position.
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

    def __str__(self):
        n = len(self.layout)
        return "\n".join([f"\t {n - i - 1} \t {self.layout[n - i - 1]}" for i in range(n)])

    def __eq__(self, other):
        return self.layout == other.layout

    def __getitem__(self, item):
        return self.layout[item]

    def is_stable(self) -> bool:
        """Determines whether the tower is stable"""
        if len(self.layout) == 0:
            return True  # an empty tower is stable

        if len(self.layout) == 1:
            return True  # a tower with only one row is stable

        for floor in self.layout[:-1]:  # skip last row
            if floor in [FLOOR_SINGLE_SIDE, FLOOR_SINGLE_SIDE_REVERSED]:
                return False
        return True

    def _strip(layout: List[List[bool]]) -> List[List[bool]]:
        """Strips empty rows from the bottom/top of a layout"""
        if len(layout) == 0:
            return []

        if len(layout) == 1 and sum(layout[0]) == 0:
            return []

        start, stop = 0, len(layout) - 1
        while sum(layout[start]) == 0:
            start += 1

        while sum(layout[stop]) == 0:
            stop -= 1

        return layout[start:stop + 1]

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

    def _is_terminal(layout: List[List[bool]]) -> bool:
        """Determines whether a layout is terminal"""
        if len(layout) == 1:
            return True

        for floor in layout[:-1]:  # skip last floor (cannot play with blocks from last row)
            if floor in [FLOOR_FULL, FLOOR_GLUED, FLOOR_GLUED_REVERSED]:
                return False
        return True

    def is_terminal(self) -> bool:
        return Tower._is_terminal(self.layout)
