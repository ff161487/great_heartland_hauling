import numpy as np
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


class AiGreedy(Player):
    def __init__(self, name):
        super().__init__(name)

    def strategy(self, actions, public_info):
        # Select an action randomly(according to certain distribution) from possible choices
        # Get game round
        r = public_info['Game']['Round']

        # Compute cost
        m_cost = cost(actions)

        # Compute selling array and buying ratio for all places
        spa = [sp_vec(x['Selling_info']) for x in public_info['Place']]
        spa = np.vstack(spa)
        wa = [w_vec(x) for x in public_info['Place']]
        wa = np.vstack(wa)

        # Compute the number of item to be bought and money earn from selling
        spa = spa[actions[:, 1]]
        wa = wa[actions[:, 1]]
        m_s = (spa * actions[:, -7:-3]).sum(1) * (actions[:, 3] == -1)
        dm = m_s - m_cost
        dn = ((wa * actions[:, -7:-3]).astype('int8') * (actions[:, 3] == 1)[:, None] -
              actions[:, -7:-3] * (actions[:, 3] == -1)[:, None])
        dx = np.hstack((dm[:, None], dn))

        # Compute 'net profit/net gain'
        coef = np.array([0.1677 + 0.0102 * r, 0.3514 - 0.0052 * r, 0.3684 - 0.0079 * r,
                         0.6371 - 0.0382 * r, 0.5885 - 0.0319 * r])
        net_gain = dx.dot(coef)
        action = actions[np.argmax(net_gain)]
        return action
