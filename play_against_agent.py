from src.agent import Agent
from src.constants import LEFT, MID, RIGHT
from src.game import Game

agent = Agent(mode="random")
game = Game()
agent_turn = False  # human starts playing

while not game.is_game_over():
    if agent_turn:
        print("\n", "18 agent playing...", "\n")
        agent.play(game)
        agent_turn = False
        continue

    while not agent_turn:
        try:
            print("\n", "🧮 Current game status:", "\n", game.tower, "\n")

            # y
            valid_y = list(range(game.tower.height))
            y = None
            while y not in valid_y:
                y = input(f"y (must be one of {valid_y}): ")
                y = int(y)

            # x
            valid_x = [i for i in [LEFT, MID, RIGHT] if game.tower[y][i]]
            x = None
            while x not in valid_x:
                x = input(f"x (must be one of {valid_x}): ")
                x = int(x)

            # create new row
            create_new_row = input("create_new_row [Y/n]: ")
            if create_new_row.lower() in ["yes", "true", "y", ""]:
                create_new_row = True
            else:
                create_new_row = False

            valid_new_x = [LEFT, MID, RIGHT]
            if not create_new_row:
                valid_new_x = [i for i in [LEFT, MID, RIGHT] if not game.tower[-1][i]]
            new_x = None
            while new_x not in valid_new_x:
                new_x = input(f"new_x (must be one of {valid_new_x}: ")
                new_x = int(new_x)

            print("playing...")
            game.play((x, y), (new_x, create_new_row))
            agent_turn = True
        except Exception as e:
            print(f"ERROR: {e}")

if agent_turn:
    print("GAME OVER! The agent won")
else:
    print("YOU WIN!")
