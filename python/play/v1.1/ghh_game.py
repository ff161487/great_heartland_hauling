import numpy as np
from random import seed, shuffle
from ghh_map import Map
from ghh_parameters import HAND_LIMIT
from pdb import set_trace


class Game:
    def __init__(self, player_list, seed_g=None, seed_m=None):
        self.seed = seed_g
        self.draw_pile = []
        self.discard_pile = ['Cow'] * 8 + ['Pig'] * 8 + ['Corn'] * 15 + ['Bean'] * 15 + ['1_Step'] * 10 + \
                            ['2_Steps'] * 6 + ['3_Steps'] * 3
        self.players = player_list
        self.map = Map(n_players=len(player_list), seed_map=seed_m)
        self.round = 0
        self.is_final_round = False
        self.threshold = 70 - 10 * len(player_list)
        self.result = None

    def get_public_info(self):
        player_info = [{'Name': player.name, 'Money': player.money, 'Position': player.position,
                        'Inventory': player.inventory} for player in self.players]
        place_info = [{'Name': self.map.places[i].name, 'Speciality': self.map.places[i].speciality,
                       'Selling_info': self.map.places[i].selling_info, 'Inventory': self.map.places[i].inventory,
                       'One_Step': self.map.one_step[i], 'Two_Steps': self.map.two_steps[i],
                       'Three_Steps': self.map.three_steps[i]} for i in range(len(self.map.places))]
        map_info = {'Map_Index': self.map.map_index, 'Coordinates': self.map.coordinates}
        game_info = {'Round': self.round}
        public_info = {'Player': player_info, 'Place': place_info, 'Map': map_info, 'Game': game_info}
        return public_info

    def shuffle(self):
        if len(self.draw_pile) <= HAND_LIMIT:
            seed(self.seed)
            shuffle(self.discard_pile)
            self.draw_pile.extend(self.discard_pile)
            self.discard_pile = []

    def run(self):
        # Each player draws their cards in the beginning
        self.shuffle()
        for player in self.players:
            self.draw_pile = player.refuel(self.draw_pile)

        while not self.is_final_round:
            # Initialize the number of rounds
            self.round = self.round + 1

            # Each player takes their action
            for player in self.players:
                # Shuffle the draw_pile
                self.shuffle()

                # Player take action based on public information
                public_info = self.get_public_info()
                action = player.make_decision(public_info)
                place = self.map.places[action[1]]
                self.draw_pile, self.discard_pile = player.take_action(place, self.draw_pile, self.discard_pile, action)

                # Check if this is the final round
                if player.money >= self.threshold:
                    self.is_final_round = True

        # Determine winner and loser after final round
        punish = np.array(list(self.map.places[0].selling_info.values()), np.int8)
        inventory = []
        money = []
        for player in self.players:
            inventory.append([player.inventory.count(x) for x in ['Bean', 'Corn', 'Pig', 'Cow']])
            money.append(player.money)
        inventory = np.array(inventory, dtype=np.int8)
        money = np.array(money, dtype=np.int8)
        score = money + (punish * inventory).sum(1) - 0.1 * inventory.sum(1)
        win = (score == score.max())
        self.result = win
