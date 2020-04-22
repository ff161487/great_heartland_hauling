import numpy as np
import pandas as pd
from ghh_game import Game
from ghh_AI_Random import AI_Random
from joblib import Parallel, delayed
from pdb import set_trace


def simulate(seed_g, seed_m, seed_a, seed_b, seed_c, seed_d):
    player_list = [AI_Random('A', seed_a), AI_Random('B', seed_b), AI_Random('C', seed_c), AI_Random('D', seed_d)]
    game = Game(player_list, seed_g, seed_m)
    game.run()
    set_trace()


def simulation(n):
    # Generate seed grid
    set_trace()


if __name__ == '__main__':
    # simulate(0, 1, 123, 999, 5, 666)
    simulate(0, 0, 0, 0, 0, 0)
    set_trace()
