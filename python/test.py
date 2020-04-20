from pickle import dump
from td_game import Game
from td_player import Player
from pdb import set_trace

if __name__ == '__main__':
    player_list = [Player(x) for x in ['Alex', 'Bob', 'Cindra']]
    my_game = Game(player_list, 999)
    pi = my_game.get_public_info()
    with open('pi.pickle', 'wb') as f:
        dump(pi, f)
