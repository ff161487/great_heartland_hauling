import numpy as np
from random import choices
from ghh_choice import cost
from ghh_player import Player
from pdb import set_trace


def to_seq(idx):
    seq = np.array([(idx // x) % 2 for x in 2 ** np.arange(5)], np.int8)
    return seq


class AiSimple(Player):
    def __init__(self, name, model_index):
        super().__init__(name)
        self.model_index = model_index

    def strategy(self, actions, public_info):
        # Select an action randomly(according to certain distribution) from possible choices
        # Get game round
        r = public_info['Game']['Round']

        # Compute cost
        n_cost = cost(actions)

        # Compute destination value
        plc_lv = [sum(x['Selling_info'].values()) for x in public_info['Place']]
        l_to = np.array(plc_lv, np.int8)[actions[:, 1]]

        # Compute number of buy and sell
        n_bs = actions[:, -7:-3].sum(1)
        n_b = n_bs * (actions[:, 3] == 1)
        n_s = n_bs * (actions[:, 3] == -1)

        # Get 'gene sequence'
        seq = to_seq(self.model_index)

        # Compute 'net profit/net gain'
        beta_choice = 0.5 + 1.5 * seq
        coef = np.array([2, 0.01, 0.1, 2, 0.2])
        beta = coef * beta_choice
        net_gain = (beta[0] - beta[1] * r) * n_b + beta[2] * r * n_s - beta[3] * n_cost + beta[4] * l_to
        w = np.exp(net_gain)
        idx = choices(range(actions.shape[0]), w)[0]
        action = actions[idx, :]
        return action
