import numpy as np
from ghh_game import Game
from ghh_AI_RandomUniform import AiRandomUniform
from ghh_AI_Random import AiRandom
from ghh_AI_Lv3 import AiLv3
from ghh_AI_Greedy import AiGreedy
from winning_rate import avg_win_rt
from pdb import set_trace


def main(n=1000):
    ai_list = [AiRandomUniform, AiRandom, AiLv3, AiGreedy]
    wrm = np.zeros((len(ai_list), len(ai_list)))
    for i in range(len(ai_list)):
        for j in range(len(ai_list)):
            if i != j:
                wrm[i, j] = avg_win_rt(ai_list[i], ai_list[j], n)
    return wrm


if __name__ == '__main__':
    wrm = main()
    set_trace()
