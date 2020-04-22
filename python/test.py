from pickle import dump
from ghh_game import Game
from ghh_player import Player
from pdb import set_trace


if __name__ == '__main__':
    player_list = [Player(x) for x in ['Player_A', 'Player_B', 'Player_C', 'Player_D']]
    my_game = Game(player_list, 999, 123)
    my_game.run()
    set_trace()
