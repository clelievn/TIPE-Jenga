G = 9.81 # N/kg
BLOCK_MASS = 0.0165  # g
BLOCK_MUS = 0.534  
TOWER_N_BLOCKS = 54  # source: https://reglesdejeux.github.io/regles-du-jeu-jenga/index.html
TOWER_N_FLOORS = 9
TOWER_DEFAULT_LAYOUT = [[True, True, True] for _ in range(TOWER_N_FLOORS)]
FLOOR_FULL = [True, True, True]
FLOOR_EMPTY = [False, False, False]
FLOOR_MIDDLE = [False, True, False]
FLOOR_APART = [True, False, True]
FLOOR_GLUED = [True, True, False]
FLOOR_GLUED_REVERSED = FLOOR_GLUED[::-1]
FLOOR_SINGLE_SIDE = [True, False, False]
FLOOR_SINGLE_SIDE_REVERSED = FLOOR_SINGLE_SIDE[::-1]
LEFT, MID, RIGHT = 0, 1, 2

SIZE_2 = [FLOOR_FULL]
SIZE_1 = [FLOOR_GLUED, FLOOR_GLUED_REVERSED]
SIZE_0 = [FLOOR_MIDDLE, FLOOR_APART]

F_INF = 0.1 # N
F_SUP = 5 # N