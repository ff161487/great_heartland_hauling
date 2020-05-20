import numpy as np
from random import choices
from ghh_choice import cost
from ghh_player import Player
from pdb import set_trace


def sp_vec(sell_dict, items=['Bean', 'Corn', 'Pig', 'Cow']):
    vec = np.zeros(4, np.int8)
    for i in range(4):
        item = items[i]
        if item in sell_dict:
            vec[i] = sell_dict[item]
    return vec


def w_vec(plc_info, items=['Bean', 'Corn', 'Pig', 'Cow']):
    vec = np.zeros(4)
    spec = plc_info['Speciality']
    sell_dict = plc_info['Selling_info']
    if len(sell_dict) < 4:
        for i in range(4):
            item = items[i]
            if item == spec:
                vec[i] = 1
            elif item in sell_dict:
                vec[i] = 0.5
    return vec


class AiLv3(Player):
    def __init__(self, name):
        super().__init__(name)

    def strategy(self, actions, public_info):
        # Select an action randomly(according to certain distribution) from possible choices
        # Get game round
        r = public_info['Game']['Round']

        # Compute cost
        n_cost = cost(actions)

        # Compute selling array and buying ratio for all places
        spa = [sp_vec(x['Selling_info']) for x in public_info['Place']]
        spa = np.vstack(spa)
        wa = [w_vec(x) for x in public_info['Place']]
        wa = np.vstack(wa)

        # Compute the number of item to be bought and money earn from selling
        spa = spa[actions[:, 1]]
        wa = wa[actions[:, 1]]
        m_s = (spa * actions[:, -7:-3]).sum(1) * (actions[:, 3] == -1)
        n_b0 = (wa[:, :2] * actions[:, -7:-5]).sum(1) * (actions[:, 3] == 1)
        n_b1 = (wa[:, -2:] * actions[:, -5:-3]).sum(1) * (actions[:, 3] == 1)

        # Compute 'net profit/net gain'
        coef = np.array([101.305, 0.00274, 0.23945, 0.36015, 22.5322, 20.2168])  # Initial/baseline coefficient
        beta = coef * 1.0
        net_gain = (beta[0] - beta[1] * r) * (beta[2] * n_b0 + beta[3] * n_b1) + beta[4] * r * m_s - beta[5] * n_cost
        w = np.exp(net_gain - net_gain.max())
        idx = choices(range(actions.shape[0]), w)[0]
        action = actions[idx, :]
        return action
