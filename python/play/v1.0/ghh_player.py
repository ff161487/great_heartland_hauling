import numpy as np
from ghh_choice import all_choices
from ghh_parameters import INIT_MONEY, HAND_LIMIT, NOT_SPEC_COST
from pdb import set_trace


class Player:
    def __init__(self, name):
        self.name = name
        self.inventory = []
        self.money = INIT_MONEY
        self.position = 0
        self.hand = []
        self.actions = []

    def __draw(self, draw_pile, n):
        if n > HAND_LIMIT:
            print('One cannot draw more than {} cards from the pile.'.format(HAND_LIMIT))
        else:
            self.hand = self.hand + draw_pile[:n]
            return draw_pile[n:]

    def __discard(self, discard_pile, to_be_discarded):
        for card in to_be_discarded:
            self.hand.remove(card)
            discard_pile.append(card)
        return discard_pile

    def refuel(self, draw_pile):
        if len(self.hand) < HAND_LIMIT:
            draw_pile = self.__draw(draw_pile, HAND_LIMIT - len(self.hand))
        return draw_pile

    def take_action(self, place, draw_pile, discard_pile, action_array):
        # Move
        self.position = action_array[1]
        cond_1 = (action_array[2] == 1) and (action_array[-3] == 0)  # Pay for 1-step moving
        cond_2 = (action_array[2] == 2) and (action_array[-3] < 2) and (action_array[-2] == 0)  # Pay for 2-step moving
        cond_3 = (action_array[2] == 3) and (action_array[-1] == 0) and (
                    (action_array[-2] == 0) or (action_array[-3] == 0))  # Pay for 3-step moving
        if cond_1 or cond_2 or cond_3:
            self.money = self.money - action_array[2]  # Pay for movement if not using fuel card

        # Buy, sell or discard
        # First, take those cards(played or discarded) out of hands
        cards = action_array[-7:]
        order = action_array[-7:-3]
        tbd = (['Bean'] * cards[0] + ['Corn'] * cards[1] + ['Pig'] * cards[2] + ['Cow'] * cards[3] +
               ['1_Step'] * cards[4] + ['2_Steps'] * cards[5] + ['3_Steps'] * cards[6])
        ocl = ['Bean'] * order[0] + ['Corn'] * order[1] + ['Pig'] * order[2] + ['Cow'] * order[3]
        discard_pile = self.__discard(discard_pile, tbd)
        if action_array[3] == 1:
            # Buying: player inventory and place inventory (Check for speciality)
            name = ocl[0]
            if name == place.speciality:
                self.inventory = self.inventory + ocl
                place.player_buy(name, len(ocl))
            else:
                self.inventory = self.inventory + [name] * int(len(ocl) / NOT_SPEC_COST)
                place.player_buy(name, int(len(ocl) / NOT_SPEC_COST))
        elif action_array[3] == -1:
            # Selling: player money, player inventory and place inventory
            name = ocl[0]
            self.money = self.money + place.selling_info[name] * len(ocl)
            for item in ocl:
                self.inventory.remove(item)
            place.player_sell(name, len(ocl))
        elif action_array[3] == 0:
            # Pay $1 for discarding if not restarting
            if action_array[1] != 0:
                self.money = self.money - 1

        # Refuel
        draw_pile = self.refuel(draw_pile)

        # Add to action list
        self.actions.append(action_array)
        return draw_pile, discard_pile

    def possible_choices(self, public_info):
        actions = all_choices(self.name, public_info)
        hand = np.array([self.hand.count(x) for x in ['Bean', 'Corn', 'Pig', 'Cow', '1_Step', '2_Steps', '3_Steps']],
                        np.int8)
        hand = np.tile(hand, (actions.shape[0], 1))
        cond = (hand - actions[:, -7:]).min(1) >= 0
        actions = actions[cond, :]
        if self.money < 5:
            if (actions[:, 1] != 0).sum() > 0:  # Still have choices not to go bankruptcy
                actions = actions[actions[:, 1] != 0, :]
        return actions

    def strategy(self, actions, public_info):
        idx = self.money % actions.shape[0]
        return actions[idx, :]

    def make_decision(self, public_info):
        actions = self.possible_choices(public_info)
        action = self.strategy(actions, public_info)
        return action
