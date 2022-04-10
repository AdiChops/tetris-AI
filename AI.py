import numpy
import threading
import pygame
import time
from tetris import TetrisApp
import os

# def clearConsole():
#     command = 'clear'
#     if os.name in ('nt','dos'):
#         command = 'cls'
#     os.system(command)

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
    app.stone # we can access the currently dropping stone like this
    states = []
    current_x = app.stone_x
    while current_x-1 >= 0:
        current_x -= 1
        print(current_x)
        copy = TetrisApp()
        copy.stone = app.stone
        copy.board = app.board
        copy.stone_x = current_x
        states.append(project(copy))
    print(states)



    # we'll have to look at the current height
    # from the current height, we can determine where the piece would fall
    # from there, we can determine all the possible places in which the piece could fall and append it to the list of possible states

def sample_board_replace(board):
    board[len(board)//2][len(board[0])//2] = 0
    return board


# 
def project(app=TetrisApp):
    app.insta_drop()
    return app.board

# Heuristic used for A* search
def heuristic(board: list) -> int:
    height = len(board)-1
    width = len(board[0])
    print(height,width)
    # Find highest block in each column
    highest_blocks = [0 for _ in range(width)]
    for y in range(width):
        if (highest_blocks[y] > 0): break
        for x in range(height):
            if (board[x][y] > 0):
                print("Found a block at",x,y,"=",0 + (height-x-1))
                highest_blocks[y] = 0 + (height-x)
                break
    return sum(highest_blocks)

def test(app=TetrisApp):
    while not app.gameover:
        # app.rotate_stone()
        # pygame.event.post(pygame.event.Event(pygame.QUIT))
        possible_board_states(app)
        time.sleep(0.5)

        # for i in app.board:
        #     print(i)
        # print('\n')
    print("Game is over!")
    time.sleep(1) # sleep for 1 second to process what happened and then quit
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    

if __name__ == '__main__':
    app = TetrisApp()
    # t1 = threading.Thread(target=app.run)
    # t2 = threading.Thread(target=test, args=(app,))
    # t1.start()
    # t2.start()
    # t1.join()
    # t2.join()
    key_actions = {
        'ESCAPE':   app.quit,
        'LEFT':     lambda:app.move(-1),
        'RIGHT':    lambda:app.move(+1),
        'DOWN':     lambda:app.drop(True),
        'UP':       app.rotate_stone,
        'p':        app.toggle_pause,
        'SPACE':    app.start_game,
        'RETURN':   app.insta_drop
    }

    app.gameover = False
    app.paused = False
    app.init_game()
    app.new_stone()
    app.insta_drop()
    for i in range(len(app.board)):
        print(app.board[i],"-",i)
    print([i for i in range(len(app.board[0]))])
    print(heuristic(app.board))
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