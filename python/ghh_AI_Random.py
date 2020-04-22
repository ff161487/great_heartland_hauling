import numpy as np
from random import seed, choices
from ghh_choice import cost, act_on
from ghh_player import Player
from pdb import set_trace


def profit(actions):
    buy = np.array([5 / 3, 5 / 3, 11 / 6, 11 / 6])
    sell = np.array([8 / 3, 8 / 3, 23 / 6, 23 / 6])
    pf = ((actions[:, -7:-3] * buy).sum(1) * (actions[:, 3] == 1) +
          (actions[:, -7:-3] * sell).sum(1) * (actions[:, 3] == -1))
    return pf


class AI_Random(Player):
    def __init__(self, name, seed_p):
        super().__init__(name)
        self.seed = seed_p
        self.public_info_list = []

    def strategy(self, actions, public_info):
        # Select an action randomly(according to certain distribution) from possible choices
        seed(self.seed)
        ac = cost(actions)
        ap = profit(actions)
        w = np.exp(ap - ac)
        idx = choices(range(actions.shape[0]), w)[0]
        action = actions[idx, :]

        # Record the public info after taking action
        npi = act_on(self.name, public_info, action)
        self.public_info_list.append(npi)
        return action
