import numpy as np
from pandas import Series
from ghh_player import Player
from pdb import set_trace


def read_action(action):
    if action[3] == 1:
        msg_t = '买入'
    elif action[3] == -1:
        msg_t = '卖出'
    else:
        msg_t = '换牌'
    chn_name = ['大豆', '玉米', '猪', '牛', '一步油卡', '两步油卡', '三步油卡']
    hand = [(chn_name[i], action[4 + i]) for i in range(7) if action[4 + i] > 0]
    hand = '，'.join(['{}：{}张'.format(x[0], x[1]) for x in hand])
    msg = '从点{}, 走{}步，走到点{}，{}。共使用或弃置卡牌：{}'.format(action[0], action[2], action[1], msg_t, hand)
    return msg


def check_actions(actions):
    rst = Series([read_action(action) for action in actions])
    return rst


def visualize(public_info):
    ply_info = public_info['Player']
    plc_info = public_info['Place']
    coordinates = public_info['Map']['Coordinates']

    # Keep useful place info
    plc_info = [(x['Name'], x['Speciality'], x['Selling_info'], x['Inventory']) for x in plc_info]
    set_trace()


class HumanPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    def check_hand(self):
        hand = [self.hand.count(x) for x in ['Bean', 'Corn', 'Pig', 'Cow', '1_Step', '2_Steps', '3_Steps']]
        chn_name = ['大豆', '玉米', '猪', '牛', '一步油卡', '两步油卡', '三步油卡']
        hand = [(chn_name[i], hand[i]) for i in range(7) if hand[i] > 0]
        hand = '，'.join(['{}：{}张'.format(x[0], x[1]) for x in hand])
        print(hand)

    def strategy(self, actions, public_info):
        # Select an action based on human input
        visualize(public_info)
        set_trace()
        return action
