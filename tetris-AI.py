import numpy
import threading
import pygame
import time
from tetris import TetrisApp

# tetris_shapes = [
#     [[1, 1, 1],
#      [0, 1, 0]],

#     [[0, 2, 2],
#      [2, 2, 0]],

#     [[3, 3, 0],
#      [0, 3, 3]],

#     [[4, 0, 0],
#      [4, 4, 4]],

#     [[0, 0, 5],
#      [5, 5, 5]],

#     [[6, 6, 6, 6]],

#     [[7, 7],
#      [7, 7]]
# ]
def possible_board_states(app=TetrisApp):
    app.board # we can access the current board like this
    app.stone # we can access the next stone like this
    # we'll have to look at the current height
    # from the current height, we can determine where the piece would fall
    # from there, we can determine all the possible places in which the piece could fall and append it to the list of possible states


def test(app=TetrisApp):
    while not app.gameover:
        app.insta_drop()
        time.sleep(0.5)
    print("Game is over!")
    time.sleep(1) # sleep for 1 second to process what happened and then quit
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    

if __name__ == '__main__':
    App = TetrisApp()
    t1 = threading.Thread(target=App.run)
    t2 = threading.Thread(target=test, args=(App,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print("Done!")
        

# def astar_search(init_state, goal_state, move_cost):
#     costs = dict({'u': move_cost[0], 'd': move_cost[1], 'l': move_cost[2], 'r': move_cost[3]})
#     init_arr = numpy.reshape(init_state, (-1,BOARD_SIZE), 'F')
#     goal_arr = numpy.reshape(goal_state, (-1,BOARD_SIZE), 'F')
#     goal_dict = dict()

#     for y in range(0, len(goal_arr)):
#         for x in range(0, len(goal_arr[y])):
#             goal_dict[goal_arr[y][x]] = [x, y]
    
#     frontiers = [dict({"state": numpy.copy(init_arr), "path":'', "f(n)": heuristic(init_arr, goal_dict), "g(n)": 0})]
#     min_cost_index = 0

#     # loop until the minimum cost frontier node state is not in the goal state
#     while (frontiers[min_cost_index]["state"] != goal_arr).any():
#         node_state = frontiers.pop(min_cost_index)
#         frontiers = expand_frontiers(frontiers, node_state, costs, goal_dict)
#         min_cost_index = min_cost_finder(frontiers)

#     return frontiers[min_cost_index]["path"] # total cost can easily be found by also returning/printing frontiers[min_cost_index]["g(n)"]