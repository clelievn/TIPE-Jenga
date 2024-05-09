import random

from agent import Agent
from constants import LEFT, MID, RIGHT
from game import Game

agent_random = Agent(mode="random")
agent_grundy = Agent(mode="grundy")
game = Game()
random_turn = random.choice([False, True])  # indicates whether it's agent_random's or grundy's turn

while not game.is_game_over():
    if random_turn:
        print("\n", "🧮 Current game status:", "\n", game.tower, "\n")
        print("\n", "🤖 agent_random playing...", "\n")
        agent_random.play(game)
        random_turn = False
        continue

    else:
        print("\n", "🧮 Current game status:", "\n", game.tower, "\n")
        print("\n", "👾 agent_grundy playing...", "\n")
        agent_grundy.play(game)
        random_turn = True

print("\n", "🧮 Current game status:", "\n", game.tower, "\n")
if random_turn:
    print("GAME OVER! The random agent won")
else:
    print("GAME OVER! The grundy agent won")
