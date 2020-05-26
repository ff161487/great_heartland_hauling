import numpy as np
from ghh_game import Game
from itertools import permutations
from joblib import Parallel, delayed
from pdb import set_trace


def win_rt(base, test, seed):
    # Run game simulation
    player_list = [base(name=x) for x in ['A', 'B', 'C']]
    player_list.append(test(name='D'))
    order = np.arange(4)
    rst = []
    for od_g in permutations(order, 4):
        players = [player_list[i] for i in od_g]
        game = Game(player_list=players, seed_g=seed)
        game.run()
        rst.append(game.result[od_g.index(3)])

    # Count how many times did each player win
    rst = np.array(rst).mean()
    return rst


def avg_win_rt(ai_baseline, ai_test, num_sims):
    # Generate a grid for random seeds
    grid = np.random.randint(999999, size=num_sims)

    # Parallel simulations
    rst = Parallel(n_jobs=-1, verbose=10)(delayed(win_rt)(ai_baseline, ai_test, seed) for seed in grid)
    rst = np.array(rst).mean()
    return rst


if __name__ == '__main__':
    pass
