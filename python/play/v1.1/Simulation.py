import numpy as np
import pandas as pd
from ghh_game import Game
from ghh_AI_Random import AiRandom
from joblib import Parallel, delayed
from pdb import set_trace


def ply_vec(ply_info):
    set_trace()


def plc_vec(plc_info):
    plc_co = ['Flint', 'Mount Berry', 'Eureka', 'Shermer', 'Jericho', 'Fort Lee', 'Cameron', 'Tatanka', 'Midville',
              'Popinjay', 'Troy', 'Bedford Falls']

    set_trace()


def simulate(seed_g, seed_m, seed_a, seed_b, seed_c, seed_d):
    # Run game simulation
    player_list = [AiRandom('A', seed_a), AiRandom('B', seed_b), AiRandom('C', seed_c), AiRandom('D', seed_d)]
    game = Game(player_list, seed_g, seed_m)
    game.run()

    # Retrieve result
    map_index = game.map.map_index
    places_names = [place.name for place in game.map.places]
    places_names = {i: places_names[i] for i in range(len(places_names))}
    set_trace()


def simulation(n):
    # Generate seed grid
    set_trace()


if __name__ == '__main__':
    # simulate(0, 1, 123, 999, 5, 666)
    simulate(0, 0, 0, 0, 0, 0)
    set_trace()
