from random import seed, randint
from ghh_choice import act_on
from ghh_player import Player
from pdb import set_trace


class AiRandomUniform(Player):
    def __init__(self, name, seed_p=None):
        super().__init__(name)
        self.seed = seed_p
        self.public_info_list = []

    def strategy(self, actions, public_info):
        # Select an action randomly from possible choices
        seed(self.seed)
        idx = randint(0, actions.shape[0] - 1)
        action = actions[idx, :]

        # Record the public info after taking action
        npi = act_on(self.name, public_info, action)
        self.public_info_list.append(npi)
        return action
