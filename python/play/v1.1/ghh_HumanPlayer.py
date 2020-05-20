from sys import exit
from copy import deepcopy
from textwrap import fill
from pandas import Series
from matplotlib.pyplot import subplots, show, rcParams, ion
from ghh_player import Player
from ghh_parameters import ENG_CHS
from pdb import set_trace

rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
ion()


def output_null(x):
    if x is None:
        rst = '无'
    else:
        rst = ENG_CHS[x]
    return rst


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
    print(rst)


class HumanPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
        self.fig, self.ax = subplots(figsize=(16, 9))  # From Elliot Gao, add figure attribute to class
        self.ax.axis([-4, 3, -3, 3])

    def check_hand(self):
        hand = [self.hand.count(x) for x in ['Bean', 'Corn', 'Pig', 'Cow', '1_Step', '2_Steps', '3_Steps']]
        chn_name = ['大豆', '玉米', '猪', '牛', '一步油卡', '两步油卡', '三步油卡']
        hand = [(chn_name[i], hand[i]) for i in range(7) if hand[i] > 0]
        hand = '，'.join(['{}：{}张'.format(x[0], x[1]) for x in hand])
        return hand

    def visualize(self, public_info):
        self.ax.cla()
        self.ax.axis([-4, 3, -3, 3])
        public_info = deepcopy(public_info)
        ply_info = public_info['Player']
        plc_info = public_info['Place']
        coordinates = public_info['Map']['Coordinates']

        # Get color list
        color_list = ['moccasin'] * coordinates.shape[0]
        for i in range(len(ply_info)):
            color_list[ply_info[i]['Position']] = ['r', 'y', 'g', 'b'][i]
        color_list[0] = 'grey'

        # Keep useful place info
        plc_info = [(x['Name'], x['Speciality'], x['Selling_info'], x['Inventory']) for x in plc_info]

        # Draw map
        for i in range(coordinates.shape[0]):
            # Get text for each place
            plc_n = output_null(plc_info[i][0])
            plc_s = output_null(plc_info[i][1])
            plc_p = {output_null(key): plc_info[i][2][key] for key in plc_info[i][2]}
            if i != 0:
                plc_i = {output_null(item): plc_info[i][3].count(item) for item in ['Bean', 'Corn', 'Pig', 'Cow']
                         if plc_info[i][3].count(item) > 0}
            else:
                plc_i = output_null(plc_info[i][3])
            plc_txt = '序号：{}， 特产：{} 名称：{}， 售价：{}， 库存：{}'.format(i, plc_s, plc_n, plc_p, plc_i)
            plc_txt = fill(plc_txt, width=14)
            self.ax.text(x=coordinates[i][0], y=coordinates[i][1], s=plc_txt, fontsize=10, ha='center', va='center',
                         bbox=dict(boxstyle='round,pad=0.1', fc=color_list[i], ec='w', lw=1, alpha=0.5))

        # Add player info
        for ply in ply_info:
            ply['Inventory'] = {output_null(item): ply['Inventory'].count(item) for item in
                                ['Bean', 'Corn', 'Pig', 'Cow']
                                if ply['Inventory'].count(item) > 0}
            ply_txt = '名称:{Name}, 钱:{Money}, 库存:{Inventory}'.format(**ply)
            ply_txt = fill(ply_txt, width=14)
            idx = ply_info.index(ply)
            if ply['Position'] == 0:
                color = 'grey'
            else:
                color = ['r', 'y', 'g', 'b'][idx]
            self.ax.text(x=-4, y=1 - idx, s=ply_txt, fontsize=14, ha='left', va='center',
                         bbox=dict(boxstyle='round,pad=0.1', fc=color, ec='w', lw=1, alpha=0.5))

        # Add player's hand
        hand = self.check_hand()
        self.ax.set_title("玩家的手牌为：{}".format(hand))
        show()

    def take_input(self, array_s, public_info):
        s = None
        set_s = [str(x) for x in array_s]
        while s not in set_s:
            s = input("请输入{}中的字符，或输入'h'查看帮助，或输入帮助中给定的字符：".format(array_s))
            if s == 'h':
                print('''帮助文档：
                输入单个字符'h'：查看帮助；
                输入单个字符'm'：查看地图等场上公开信息；
                输入单个字符'q'：退出游戏；''')  # From Elliot Gao's improvement
            elif s == 'm':
                self.visualize(public_info)
            elif s == 'q':
                exit("以后再玩~拜拜~")  # Based on Elliot Gao's improvement
            elif s not in set_s:
                print("抱歉，您输入的字符为无效字符，请重新输入。。。")
        s = int(s)
        return s

    def strategy(self, actions, public_info):
        # Show map at first
        self.visualize(public_info)

        # Step 1: select action type
        print("请输入您本轮要执行的动作类型：'0'表示换牌；'1'表示买入；'-1'表示卖出。")
        set_at = set(actions[:, 3])
        s = self.take_input(set_at, public_info)
        actions = actions[actions[:, 3] == s]

        # Step 2: select n_steps
        set_n_steps = set(actions[:, 2])
        print("您可以移动的步数为：{}".format(set_n_steps))
        s = self.take_input(set_n_steps, public_info)
        actions = actions[actions[:, 2] == s]

        # Step 3: select destination
        set_dst = set(actions[:, 1])
        print("您可以移动至的地点为：{}".format(set_dst))
        s = self.take_input(set_dst, public_info)
        actions = actions[actions[:, 1] == s]

        # Step 4: select action
        print("你可以执行的操作为：")
        check_actions(actions)
        set_act_idx = list(range(actions.shape[0]))
        s = self.take_input(set_act_idx, public_info)
        action = actions[s]
        return action
