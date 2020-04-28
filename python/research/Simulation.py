import numpy as np
import pandas as pd
from ghh_game import Game
from ghh_AI_Random import AiRandom
from joblib import Parallel, delayed
from pdb import set_trace


def ply_vec(ply_info, idx):
    ply_info = ply_info[idx:] + ply_info[:idx]
    ply_info = [np.array([dic['Money'], dic['Position']] + [dic['Inventory'].count(x) for x in ['Bean', 'Corn', 'Pig',
                'Cow']], np.int8) for dic in ply_info]
    ply_info = np.hstack(ply_info)
    return ply_info


def plc_vec(plc_info):
    plc_co = ['Flint', 'Mount Berry', 'Eureka', 'Shermer', 'Jericho', 'Fort Lee', 'Cameron', 'Tatanka', 'Midville',
              'Popinjay', 'Troy', 'Bedford Falls']
    plc_info = {x['Name']: [x['Inventory'].count(y) for y in ['Bean', 'Corn', 'Pig', 'Cow']] for x in plc_info[1:]}
    plc_info = [plc_info[key] for key in plc_co]
    plc_info = np.hstack(plc_info).astype(np.int8)
    return plc_info


def simulate(seed_g, seed_m, seed_a, seed_b, seed_c, seed_d):
    # Run game simulation
    player_list = [AiRandom('A', seed_a), AiRandom('B', seed_b), AiRandom('C', seed_c), AiRandom('D', seed_d)]
    game = Game(player_list, seed_g, seed_m)
    game.run()

    # Retrieve result
    df = []
    map_index = game.map.map_index
    places_names = [place.name for place in game.map.places]
    places_names = {i: places_names[i] for i in range(len(places_names))}
    for i in range(4):
        ply = game.players[i]
        ply_rst = np.array([game.result[i]] * game.round, np.int8)
        # Reshape action
        action = np.hstack((np.arange(1, game.round + 1, dtype=np.int8)[:, None], np.vstack(ply.actions)))
        # Reshape player info
        ply_info = [ply_vec(x['Player'], i) for x in ply.public_info_list]
        ply_info = np.vstack(ply_info)

        # Reshape place info
        plc_info = [plc_vec(x['Place']) for x in ply.public_info_list]
        plc_info = np.vstack(plc_info)
        df.append(np.hstack((ply_rst[:, None], action, ply_info, plc_info)))
    df = np.vstack(df)
    df = np.hstack((df, np.array([map_index] * df.shape[0], np.int8)[:, None]))

    # Replace place index with name
    df = pd.DataFrame(df)
    for i in [2, 3, 14, 20, 26, 32]:
        df.iloc[:, i].replace(places_names, inplace=True)
        df.iloc[:, i] = df.iloc[:, i].astype('category')
    return df


def simulation(n):
    # Generate seed grid
    grid = np.random.randint(99999999, size=(int(n), 6))

    # Generate column names
    items = ['Bean', 'Corn', 'Pig', 'Cow']
    plc_co = ['Flint', 'Mount Berry', 'Eureka', 'Shermer', 'Jericho', 'Fort Lee', 'Cameron', 'Tatanka', 'Midville',
              'Popinjay', 'Troy', 'Bedford Falls']
    col_0 = ['Win', 'Round']
    col_1 = ['Action_' + x for x in ['From', 'To', 'N_Steps', 'Type', 'Bean', 'Corn', 'Pig', 'Cow', '1_Step', '2_Steps',
                                     '3_Steps']]
    col_2 = ['Player_{}_{}'.format(i, x) for i in range(4) for x in ['Money', 'Position'] + items]
    col_3 = ['{}_{}'.format(place, item) for place in plc_co for item in items]
    col = col_0 + col_1 + col_2 + col_3 + ['Map_Index']

    # Parallel simulations
    rst = Parallel(n_jobs=-1, verbose=10)(delayed(simulate)(*seed_vec) for seed_vec in grid)
    rst = pd.concat(rst).reset_index(drop=True)
    rst.columns = col

    # Change data type
    for i in [2, 3, 14, 20, 26, 32]:
        rst.iloc[:, i] = rst.iloc[:, i].astype('category')

    # Save data to feather
    rst.to_feather('ghh.f')


if __name__ == '__main__':
    simulation(100)
