import numpy as np
from random import seed, sample, randint
from scipy.spatial import distance_matrix
from ghh_place import Place

# Define all place cards
starting_place = {'West Morgan': {'Bean': -1, 'Corn': -1, 'Cow': -2, 'Pig': -2}}

place_info = {'Eureka': ['Bean', {'Pig': 3, 'Cow': 4}], 'Flint': ['Cow', {'Bean': 4, 'Pig': 4}],
              'Troy': ['Cow', {'Corn': 3, 'Bean': 2}], 'Mount Berry': ['Pig', {'Corn': 4, 'Cow': 4}],
              'Midville': ['Bean', {'Corn': 2, 'Cow': 4}], 'Bedford Falls': ['Pig', {'Corn': 2, 'Bean': 3}],
              'Popinjay': ['Corn', {'Bean': 2, 'Pig': 4}], 'Jericho': ['Corn', {'Corn': 2, 'Cow': 5}],
              'Cameron': ['Pig', {'Bean': 3, 'Pig': 3}], 'Shermer': ['Corn', {'Pig': 4, 'Cow': 3}],
              'Tatanka': ['Cow', {'Corn': 3, 'Cow': 3}], 'Fort Lee': ['Bean', {'Bean': 2, 'Pig': 5}]}

'''
# Generate map
def random_map(n_players):
    n_players = 4
    n_places = 4 + 2 * n_players
    coordinates = np.random.randint(5, size=(n_places, 2))
    dm = distance_matrix(coordinates, coordinates, p=1)
    am = (dm == 1).astype(int)
    reach_2 = (np.linalg.matrix_power(am, 2) > 0).astype(int)
    reach_3 = (np.linalg.matrix_power(am, 3) > 0).astype(int)
    reach_total = am + reach_2 + reach_3
    if am.sum(0).min() > 0 and (reach_total > 0).sum(0).min() > n_players:
        return coordinates
    else:
        random_map(n_players)
'''

# Original game graphs
# ---- 2-player graphs
graph_list = [np.empty((9, 2, 4), np.int8), np.empty((11, 2, 4), np.int8), np.empty((13, 2, 4), np.int8)]
graph_list[0][:, :, 0] = np.array([[0, 0], [1, 0], [1, -1], [2, 0], [2, 1], [-1, 0], [-1, 1], [-2, 0],
           [-2, -1]])
graph_list[0][:, :, 1] = np.array([[0, 0], [1, 0], [0, -1], [-1, 0], [0, 1], [-1, 1], [1, -1], [1, -2],
           [-1, 2]])
graph_list[0][:, :, 2] = np.array([[0, 0], [1, 0], [-1, 0], [1, 1], [-1, -1], [-1, 1], [-1, 2], [1, -1],
           [1, -2]])
graph_list[0][:, :, 3] = np.array([[0, 0], [1, 0], [0, 1], [-1, 0], [0, -1], [1, -1], [1, 1], [-1, 1],
           [-1, -1]])

# ---- 3-player graphs
graph_list[1][:, :, 0] = np.array([[0, 0], [1, 0], [-1, 0], [-1, -1], [1, -1], [1, 1], [-1, 1], [-2, 1],
           [2, 1], [2, 2], [-2, 2]])
graph_list[1][:, :, 1] = np.array([[0, 0], [0, 1], [-1, 0], [1, 0], [1, 1], [-1, 1], [-1, -1], [1, -1],
           [1, -2], [-1, -2], [0, 2]])
graph_list[1][:, :, 2] = np.array([[0, 0], [1, 0], [0, 1], [-1,0], [0, -1], [1, -1], [1, 1], [1, 2],
           [0, 2], [0, -2], [1, -2]])
graph_list[1][:, :, 3] = np.array([[0, 0], [1, 0], [0, 1], [-1, 0], [0, -1], [1, -1], [1, 1], [-1, 1],
           [-1, -1], [-2, 0], [2, 0]])
# ---- 4-player graphs
graph_list[2][:, :, 0] = np.array([[0, 0], [1, 0], [0, 1], [-1, 0], [0, -1], [1, -1], [1, 1], [-1, 1],
           [-1, -1], [-1, -2], [1, -2], [1, 2], [-1, 2]])
graph_list[2][:, :, 1] = np.array([[0, 0], [0, 1], [0, -1], [1, -1], [2, -1], [2, 0], [2, 1], [1, 1],
           [-1, 1], [-2, 1], [-2, 0], [-2, -1], [-1, -1]])
graph_list[2][:, :, 2] = np.array([[0, 0], [0, 1], [0, -1], [-1, -1], [1, 1], [-1, 1], [1, -1], [-1, 2],
           [-2, 2], [-2, 1], [1, -2], [2, -2], [2, -1]])
graph_list[2][:, :, 3] = np.array([[0, 0], [1, 0], [0, 1], [-1, 0], [0, -1], [1, -1], [1, 1], [-1, 1],
           [-1, -1], [-2, 0], [2, 0], [0, -2], [0, 2]])


# Initialization of game map
class Map:
    def __init__(self, n_players, seed_map=None):
        # Randomly arrange places
        seed(seed_map)
        places = sample(place_info.keys(), 4 + 2 * n_players)

        # Specify starting place
        self.places = [Place('West Morgan', None, starting_place['West Morgan'], not_start=False)]
        for place in places:
            self.places.append(Place(place, place_info[place][0], place_info[place][1]))
        
        # Generate map and compute simple path for every node
        self.map_index = randint(0, 3)
        self.coordinates = graph_list[n_players - 2][:, :, self.map_index]
        dm = distance_matrix(self.coordinates, self.coordinates, p=1)
        idx = np.arange(dm.shape[1], dtype=np.int8)
        self.one_step = [idx[(dm == 1)[i, :]] for i in idx]
        self.two_steps = [idx[(dm == 2)[i, :]] for i in idx]
        adj_mat = (dm == 1).astype(int)
        am2 = np.linalg.matrix_power(adj_mat, 2)
        am3 = np.linalg.matrix_power(adj_mat, 3)
        loop_count = (np.outer(np.diag(am2), np.ones(dm.shape[1], np.int8)) +
                      np.outer(np.ones(dm.shape[1], np.int8), np.diag(am2)))
        rm3 = am3 + adj_mat - loop_count * adj_mat
        self.three_steps = [idx[(rm3 > 0)[i, :]] for i in idx]
        





