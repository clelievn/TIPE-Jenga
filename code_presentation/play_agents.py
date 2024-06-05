import random

from agent import Agent
from constants import LEFT, MID, RIGHT
from game import Game

# agent_random = Agent(mode="random")
# agent_grundy = Agent(mode="grundy")
# game = Game()
# random_turn = random.choice([False, True])  # indicates whether it's agent_random's or grundy's turn

# while not game.is_game_over():
#     if random_turn:
#         print("\n", "🧮 Current game status:", "\n", game.tower, "\n")
#         print("\n", "🤖 agent_random playing...", "\n")
#         agent_random.play(game)
#         random_turn = False
#         continue

#     else:
#         print("\n", "🧮 Current game status:", "\n", game.tower, "\n")
#         print("\n", "👾 agent_grundy playing...", "\n")
#         agent_grundy.play(game)
#         random_turn = True

# print("\n", "🧮 Current game status:", "\n", game.tower, "\n")
# if random_turn:
#     print("GAME OVER! The random agent won")
# else:
#     print("GAME OVER! The grundy agent won")


# agent_grundy_1 = Agent(mode="grundy")
# agent_grundy_2 = Agent(mode="grundy")
# game = Game()
# turn_grundy_1 = random.choice([False, True])  # indicates whether it's grundy_1's or grundy_2's turn
# start_playing_1 = turn_grundy_1


# while not game.is_game_over():
#     if turn_grundy_1:
#         print("\n", "🧮 Current game status:", "\n", game.tower, "\n")
#         print("\n", "🎮 agent_grundy_1 playing...", "\n")
#         agent_grundy_1.play(game)
#         turn_grundy_1 = False
#         continue

#     else:
#         print("\n", "🧮 Current game status:", "\n", game.tower, "\n")
#         print("\n", "💻 agent_grundy_2 playing...", "\n")
#         agent_grundy_2.play(game)
#         turn_grundy_1 = True

# print("\n", "🧮 Current game status:", "\n", game.tower, "\n")
# if start_playing_1:
#     print("Grundy_1 started playing", "\n")
# else:
#     print("Grundy_2 started playing !", "\n")
# if turn_grundy_1:
#     print("GAME OVER! The grundy_2 agent won", "\n")
# else:
#     print("GAME OVER! The grundy_1 agent won", "\n")


agent_grundy = Agent(mode="grundy")
agent_grundy_friction = Agent(mode="grundy_friction")
game = Game()
turn_grundy = random.choice([False, True])  # indicates whether it's grundy_friction's or grundy's turn
start_playing_grundy = turn_grundy
game_over = False


while not game_over:
    if turn_grundy:
        print("\n", "🧮 Current game status:", "\n", game.tower, "\n")
        print("\n", "🎮 agent_grundy playing...", "\n")
        missed_extraction = agent_grundy.play_grundy(game)
        turn_grundy = False
        if (missed_extraction):
            game_over = True
        else:
            game_over = game.is_game_over()

    else:
        print("\n", "🧮 Current game status:", "\n", game.tower, "\n")
        print("\n", "💻 agent_grundy_friction playing...", "\n")
        agent_grundy_friction.play_grundy_friction(game)
        turn_grundy = True
        if (missed_extraction):
            game_over = True
        else:
            game_over = game.is_game_over()


print("\n", "🧮 Current game status:", "\n", game.tower, "\n")
if start_playing_grundy:
    print("Grundy started playing", "\n")
else:
    print("Grundy_friction started playing !", "\n")
if turn_grundy:
    print("GAME OVER! The grundy agent won", "\n")
else:
    print("GAME OVER! The grundy_friction agent won", "\n")

