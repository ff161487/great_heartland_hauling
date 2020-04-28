from random import shuffle
from ghh_game import Game
from ghh_HumanPlayer import HumanPlayer
from ghh_AI_RandomUniform import AiRandomUniform
from pdb import set_trace


def play_game(n):
    # Initialize the player list
    player_list = [AiRandomUniform('Computer_' + str(x + 1)) for x in range(n - 1)]
    player_list.append(HumanPlayer('Player'))
    shuffle(player_list)

    # Define the game and start to play
    game = Game(player_list)
    game.run()
    set_trace()


if __name__ == '__main__':
    play_game(4)
