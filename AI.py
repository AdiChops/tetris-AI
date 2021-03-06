import threading
import pygame
import time
import tetris
import os

def clearConsole():
    command = 'clear'
    if os.name in ('nt','dos'):
        command = 'cls'
    os.system(command)

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
rotations = {'T': 4, 'L':4, 'J':4, 'S': 2, 'Z': 2, 'I': 2, 'O': 1}
def possible_board_states(app=tetris.TetrisApp):
    states = []
    stone = [row[:] for row in app.stone]
    for r in range(0, rotations[app.stone_letter]):
        for i in range(0,(len(app.board[0]) - len(stone[0])+1)):
            temp_board = drop([row[:] for row in app.board],  stone, i, app.stone_y//1)
            states.append({'num_rotations': r, 'board':temp_board[:], 'stone_x':i, 'heuristic':holes_heuristic(temp_board[:])})
        stone = tetris.rotate_clockwise(stone)
    # print("\n")
    # print("Printing States Now")
    return states

    # we'll have to look at the current height
    # from the current height, we can determine where the piece would fall
    # from there, we can determine all the possible places in which the piece could fall and append it to the list of possible states

# 
def drop(board, stone, stone_x, stone_y):
    while not tetris.check_collision(board,
                        stone,
                        (stone_x, stone_y)):
            stone_y += 1
    return tetris.join_matrixes(
        board,
        stone,
        (stone_x, stone_y))


# Heuristic on the 'height' of the grid
def height_heuristic(board: list) -> int:
    height = len(board)-1
    width = len(board[0])
    # print(height,width)
    # Find highest block in each column
    highest_blocks = [0 for _ in range(width)]
    for x in range(width):
        if (highest_blocks[x] > 0): continue
        for y in range(height):
            if (board[y][x] > 0):
                # print("Found a block at",y,x,"=",0 + (height-y-1))
                highest_blocks[x] = 0 + (height-y)
                break
    return sum(highest_blocks)

# Heuristic based on the number of holes in the grid and their placement
def holes_heuristic(board: list) -> int:
    # Top-left of board is (0,0)
    height = len(board)-1
    width = len(board[0])
    total = 0
    top_blocks = [height for _ in range(width)]
    for y in range(height):
        for x in range(width):
            # Find highest block of the column
            if(board[y][x] > 0 and top_blocks[x] > y):
                top_blocks[x] = y
                # Check for holes under highest block
                for i in range(y+1,height):
                    if(board[i][x] == 0): 
                        # print("Cell",(x,i),"is under peak",(x,top_blocks[x]),"+"+str(height-i))
                        total += (height-i)**3
                # Cell to the left of a peak is also a hole
                if(0 <= x-1 and board[y][x-1] == 0):
                    # print("Cell",(x-1,y),"is just left of peak",(x,top_blocks[x]),"+1")
                    total += (height-y)**2
                continue
            # Check if cell is surrounded by a 'tower'
            if(0 <= x-1):
                if(top_blocks[x-1] <= y and board[y][x] == 0): 
                    # print("Cell",(x,y),"is to the right of peak",(x-1,top_blocks[x-1]),"+1")
                    total += (height-y)**2
            if(x+1 < width):
                if(top_blocks[x+1] <= y and board[y][x] == 0): 
                    # print("Cell",(x,y),"is to the left of peak",(x+1,top_blocks[x+1]),"+1")
                    total += (height-y)**2
    return total
    
def best_fs(states):
    min_state = states[0]
    for state in states:
        if state['heuristic'] < min_state['heuristic']:
            min_state = dict(state)
    return min_state

def AI(app = tetris.TetrisApp):
    while not app.gameover:
        state = best_fs(possible_board_states(app))
        for n in range(0, state['num_rotations']):
            app.rotate_stone()
        while state['stone_x'] < app.stone_x:
            app.move(-1)
        while state['stone_x'] > app.stone_x:
            app.move(+1)
        app.insta_drop()
        # time.sleep(0.1) # you can comment this out for some pure chaos ????
    print(app.level)
    print(app.score)
    pygame.event.post(pygame.event.Event(pygame.QUIT))

if __name__ == '__main__':
    app = tetris.TetrisApp()
    t1 = threading.Thread(target=app.run)
    t2 = threading.Thread(target=AI, args=(app,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    # app.gameover = False
    # app.paused = False
    # app.init_game()
    # for i in range(2):
    #     app.new_stone()
    #     state = best_fs(possible_board_states(app))
    #     for n in range(0, state['num_rotations']):
    #         app.rotate_stone()
    #     while state['stone_x'] < app.stone_x:
    #         app.move(-1)
    #     while state['stone_x'] > app.stone_x:
    #         app.move(+1)
    #     app.insta_drop()
    # app.print_board()
    # print("Actual board")
    # app.print_board()
    # print([str(i) for i in range(len(app.board[0]))])
    # print(holes_heuristic(app.board))    
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

# lunar_monkeys ??? Today at 12:23 AM
# # A* search algorithm
# def astar_search(init_state: list, goal_state: list, move_cost: list) -> str:
#     cost = {'u':move_cost[0], 'd':move_cost[1], 'l':move_cost[2],'r':move_cost[3]}
#     frontier = [] # Priority queue with tuples as (priority, object)
#     heappush(frontier,(heuristic(init_state, goal_state), Node(init_state,parent=None,move_made="",total_cost=0)))
#     while len(frontier)!=0:
#         node = heappop(frontier)[1]
#         if (node.state == goal_state):
#             optimal_path = ""
#             path_cost = node.cost
#             while(node.parent != None):
#                 optimal_path = optimal_path+node.move
#                 node = node.parent
#             optimal_path = optimal_path[::-1]
#             # print(init_state,"=>",goal_state,"=",optimal_path,"(cost:",path_cost,")")
#             return optimal_path
#         for (move,state) in move_puzzle(node.state):
#             hcost = heuristic(state,goal_state)
#             true_cost = node.cost + cost[move]
#             if (move == 'u'): heappush(frontier,(true_cost+hcost, Node(state,node,move,true_cost)))
#             elif (move == 'd'): heappush(frontier,(true_cost+hcost, Node(state,node,move,true_cost)))
#             elif (move == 'l'): heappush(frontier,(true_cost+hcost, Node(state,node,move,true_cost)))
#             elif (move == 'r'): heappush(frontier,(true_cost+hcost, Node(state,node,move,true_cost)))
#     return None