import numpy as np
from itertools import combinations
from td_parameters import MAX_NUM_ITEM, HAND_LIMIT, NOT_SPEC_COST
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
        comb[:ply_inv[sell_kind[0]], sell_kind[0]] = np.arange(1, 1 + ply_inv[sell_kind[0]], dtype=np.int8)
        comb[-ply_inv[sell_kind[1]]:, sell_kind[1]] = np.arange(1, 1 + ply_inv[sell_kind[1]], dtype=np.int8)
        comb = comb[comb.sum(1) <= MAX_NUM_ITEM - plc_inv.sum(), :]
    return comb


# Compute cost of each action
def cost(actions):
    set_trace()


# List all choices for player with certain name
def all_choices(name, public_info):
    # Buy

    # Sell
    # Discard
    set_trace()


if __name__ == '__main__':
    from pickle import load
    with open('pi.pickle', 'rb') as f:
        pi = load(f)
    plc_info = pi['Map'][2]
    plc_info['Inventory'] = ['Cow'] * 4 + ['Bean'] * 2 + ['Pig'] * 2
    comb = legal_trade(1, plc_info, ['Cow', 'Cow', 'Cow', 'Cow', 'Pig', 'Pig'])
    set_trace()
