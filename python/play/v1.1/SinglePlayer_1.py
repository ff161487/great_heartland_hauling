from random import shuffle
from ghh_game import Game
from ghh_HumanPlayer import HumanPlayer
from ghh_AI_Random import AiRandom
from pdb import set_trace


def play_game(n):
    # Initialize the player list
    player_list = [AiRandom('Computer_' + str(x + 1)) for x in range(n - 1)]
    player_list.append(HumanPlayer('Player'))
    shuffle(player_list)

    # Define the game and start to play
    game = Game(player_list)
    game.run()

    # Draw final public info
    final_public_info = game.get_public_info()
    for player in game.players:
        if isinstance(player, HumanPlayer):
            player.visualize(final_public_info)

    # Output winner
    if game.result.sum() == 0:
        print("很抱歉，本次游戏没有玩家获胜。要再接再厉哦~")
    else:
        winner = [game.players[i].name for i in range(n) if game.result[i]]
        print("本次游戏获胜的玩家是：{}".format(winner))

    # Enter 'q' to quit
    s = None
    while s != 'q':
        s = input("请输入'q'以退出游戏：")


if __name__ == '__main__':
    play_game(4)
