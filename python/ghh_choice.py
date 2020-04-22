import numpy as np
from itertools import combinations
from copy import deepcopy
from ghh_parameters import MAX_NUM_ITEM, HAND_LIMIT, NOT_SPEC_COST
from pdb import set_trace


# Twelvefold way: unlabeled balls with labeled urns(UBLU)
def ublu(n, k):
    rst = np.array(list(combinations(range(n + k - 1), n - 1)), np.int8)
    head = rst[:, 0]
    mid = np.diff(rst) - 1
    tail = (n + k - 2) - rst[:, -1]
    rst = np.hstack((head[:, None], mid, tail[:, None]))
    return rst


# Get number of UBLU cases with less than or equal to k(but larger than 1)
def ublu_leq(n, k):
    rst = [ublu(n, i) for i in range(1, k + 1)]
    rst = np.vstack(rst)
    return rst


# Generate all possible cases of discarding or playing
def card_combs():
    rst = ublu_leq(7, HAND_LIMIT)
    rst = rst[rst[:, -1] <= 3, :]
    return rst


# Define global variables for all combinations of hand and discard
comb_play = card_combs()

# Define combinations for moving
mov = [np.array([[0, 0, 0], [1, 0, 0]], np.int8), np.array([[0, 0, 0], [2, 0, 0], [0, 1, 0]], np.int8),
       np.array([[0, 0, 0], [1, 1, 0], [0, 0, 1]], np.int8)]


# Select 'legal' combinations of item traded
def legal_trade(drc, plc_info, ply_inv):
    ply_inv = np.array([ply_inv.count(x) for x in ['Bean', 'Corn', 'Pig', 'Cow']], np.int8)
    plc_inv = np.array([plc_info['Inventory'].count(x) for x in ['Bean', 'Corn', 'Pig', 'Cow']], np.int8)
    spec = ['Bean', 'Corn', 'Pig', 'Cow'].index(plc_info['Speciality'])
    sell_kind = [['Bean', 'Corn', 'Pig', 'Cow'].index(x) for x in plc_info['Selling_info'].keys()]
    buy_kind = np.arange(4, dtype=np.int8)[plc_inv != 0]
    if drc == 1:  # Buy
        coef = np.array([1 / NOT_SPEC_COST] * 4, dtype=np.float32)
        coef[spec] = 1
        comb = np.zeros((plc_inv.sum(), 4), np.int8)
        for kind in buy_kind:
            start = plc_inv[:kind].sum()
            end = plc_inv[:(kind + 1)].sum()
            if kind == spec:
                comb[start:end, kind] = np.arange(1, 1 + plc_inv[kind], dtype=np.int8)
            else:
                comb[start:end, kind] = np.arange(NOT_SPEC_COST, 1 + NOT_SPEC_COST * plc_inv[kind], NOT_SPEC_COST,
                                                  dtype=np.int8)
        comb = comb[(coef * comb).sum(1) <= MAX_NUM_ITEM - ply_inv.sum(), :]
    elif drc == -1:  # Sell
        comb = np.zeros((ply_inv[sell_kind[0]] + ply_inv[sell_kind[1]], 4), np.int8)
        if ply_inv[sell_kind[0]] > 0:
            comb[:ply_inv[sell_kind[0]], sell_kind[0]] = np.arange(1, 1 + ply_inv[sell_kind[0]], dtype=np.int8)
        if ply_inv[sell_kind[1]] > 0:
            comb[-ply_inv[sell_kind[1]]:, sell_kind[1]] = np.arange(1, 1 + ply_inv[sell_kind[1]], dtype=np.int8)
        comb = comb[comb.sum(1) <= MAX_NUM_ITEM - plc_inv.sum(), :]
    return comb


# Compute cost of each action
def cost(actions):
    if len(actions.shape) == 1:
        actions = actions[None, :]
    cond_1 = (actions[:, 2] == 1) & (actions[:, -3] == 0)  # Pay for 1-step moving
    cond_2 = (actions[:, 2] == 2) & (actions[:, -3] < 2) & (actions[:, -2] == 0)  # Pay for 2-step moving
    cond_3 = (actions[:, 2] == 3) & (actions[:, -1] == 0) & (
            (actions[:, -2] == 0) | (actions[:, -3] == 0))  # Pay for 3-step moving
    rst = (actions[:, 2] * (cond_1 | cond_2 | cond_3) + 1 * (actions[:, 3] == 0)) * (actions[:, 1] != 0)
    rst = rst.astype('int8')
    return rst


# List all choices for player with certain name
def all_choices(name, public_info):
    # Extract some basic information
    ply_plc = [x['Position'] for x in public_info['Player']]
    ply_plc.append(0)  # Exclude starting place when moving since one cannot stop at the starting place
    ply_info = [x for x in public_info['Player'] if x['Name'] == name]
    ply_info = ply_info[0]
    place = ply_info['Position']
    money = ply_info['Money']
    one_step = public_info['Place'][place]['One_Step']
    two_steps = public_info['Place'][place]['Two_Steps']
    three_steps = public_info['Place'][place]['Three_Steps']
    one_step = one_step[~np.isin(one_step, ply_plc)]
    two_steps = two_steps[~np.isin(two_steps, ply_plc)]
    three_steps = three_steps[~np.isin(three_steps, ply_plc)]
    destinations = [one_step, two_steps, three_steps]

    # Buy, sell and discard
    comb = []
    for n_steps in range(1, 4):
        for position in destinations[n_steps - 1]:
            # Buy and sell
            head_buy = np.array([place, position, n_steps, 1], dtype=np.int8)
            head_sell = np.array([place, position, n_steps, -1], dtype=np.int8)
            head_discard = np.array([place, position, n_steps, 0], dtype=np.int8)
            trade_buy = legal_trade(1, public_info['Place'][position], ply_info['Inventory'])
            trade_sell = legal_trade(-1, public_info['Place'][position], ply_info['Inventory'])
            n_movs = mov[n_steps - 1].shape[0]
            mov_buy = np.repeat(mov[n_steps - 1], trade_buy.shape[0], axis=0)
            mov_sell = np.repeat(mov[n_steps - 1], trade_sell.shape[0], axis=0)
            trade_buy = np.tile(trade_buy, (n_movs, 1))
            trade_sell = np.tile(trade_sell, (n_movs, 1))
            trade_buy = np.hstack((trade_buy, mov_buy))
            trade_sell = np.hstack((trade_sell, mov_sell))
            trade_buy = trade_buy[trade_buy.sum(1) <= HAND_LIMIT, :]
            trade_sell = trade_sell[trade_sell.sum(1) <= HAND_LIMIT, :]
            trade_buy = np.hstack((np.tile(head_buy, (trade_buy.shape[0], 1)), trade_buy))
            trade_sell = np.hstack((np.tile(head_sell, (trade_sell.shape[0], 1)), trade_sell))
            comb_discard = np.hstack((np.tile(head_discard, (comb_play.shape[0], 1)), comb_play))
            comb.append(trade_buy)
            comb.append(trade_sell)
            comb.append(comb_discard)
    comb = np.vstack(comb)

    # Move back to starting place when a player does not have enough money
    if money < 5:
        action_cost = cost(comb)
        comb_1 = comb[action_cost <= money - 1, :]
        comb_2 = comb[(action_cost > money - 1) & (comb[:, 3] == 0), :]
        if len(comb_2) > 0:
            comb_2[:, 1] = 0
            comb_2[:, 2] = 0
            comb_2 = np.unique(comb_2, axis=0)
        comb = np.vstack((comb_1, comb_2))

    # Return all choices
    return comb


# Simulate how action could change public info
def act_on(name, pub_info, action):
    public_info = deepcopy(pub_info)
    name_list = [x['Name'] for x in public_info['Player']]
    ply_idx = name_list.index(name)
    public_info['Player'][ply_idx]['Position'] = action[1]
    action_cost = cost(action)[0]
    public_info['Player'][ply_idx]['Money'] = public_info['Player'][ply_idx]['Money'] - action_cost

    # Change player money, player inventory and place inventory when buying or selling
    if action[3] != 0:
        ocl = ['Bean'] * action[4] + ['Corn'] * action[5] + ['Pig'] * action[6] + ['Cow'] * action[7]
        item = ocl[0]
        if action[3] == 1:
            # Buying: player inventory and place inventory (Check for speciality)
            if item == public_info['Place'][action[1]]['Speciality']:
                public_info['Player'][ply_idx]['Inventory'] = public_info['Player'][ply_idx]['Inventory'] + ocl
                for obj in ocl:
                    public_info['Place'][action[1]]['Inventory'].remove(obj)
            else:
                public_info['Player'][ply_idx]['Inventory'] = (public_info['Player'][ply_idx]['Inventory'] +
                                                               [item] * int(len(ocl) / NOT_SPEC_COST))
                for i in range(int(len(ocl) / NOT_SPEC_COST)):
                    public_info['Place'][action[1]]['Inventory'].remove(item)
        elif action[3] == -1:
            # Selling: player money, player inventory and place inventory
            public_info['Player'][ply_idx]['Money'] = (public_info['Player'][ply_idx]['Money'] +
                                                       public_info['Place'][action[1]]['Selling_info'][item] * len(ocl))
            for obj in ocl:
                public_info['Player'][ply_idx]['Inventory'].remove(obj)
            public_info['Place'][action[1]]['Inventory'] = public_info['Place'][action[1]]['Inventory'] + ocl
    return public_info


if __name__ == '__main__':
    set_trace()
