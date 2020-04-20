from random import shuffle
from td_map import Map
from td_parameters import HAND_LIMIT
from pdb import set_trace


class Game:
    def __init__(self, player_list, seed):
        self.draw_pile = []
        self.discard_pile = ['Cow'] * 8 + ['Pig'] * 8 + ['Corn'] * 15 + ['Bean'] * 15 + ['1_Step'] * 10 + \
                            ['2_Steps'] * 6 + ['3_Steps'] * 3
        self.players = player_list
        self.map = Map(n_players=len(player_list), seed=seed)
        self.round = 1
        self.is_final_round = False
        self.threshold = 70 - 10 * len(player_list)
        self.result = []

    def get_public_info(self):
        player_info = [{'Name': player.name, 'Money': player.money, 'Position': player.position,
                        'Inventory': player.inventory} for player in self.players]
        map_info = [{'Name': self.map.places[i].name, 'Speciality': self.map.places[i].speciality,
                     'Selling_info': self.map.places[i].selling_info, 'Inventory': self.map.places[i].inventory,
                     'One_Step': self.map.one_step[i], 'Two_Steps': self.map.two_steps[i],
                     'Three_Steps': self.map.three_steps[i]} for i in range(len(self.map.places))]
        public_info = {'Player': player_info, 'Map': map_info}
        return public_info

    def shuffle(self):
        if len(self.draw_pile) <= HAND_LIMIT:
            shuffle(self.discard_pile)
            self.draw_pile = self.draw_pile.extend(self.discard_pile)
            self.discard_pile = []

    def run(self):
        while not self.is_final_round:
            for player in self.players:
                # Shuffle the draw_pile
                self.shuffle()
