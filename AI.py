import numpy
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
        for i in range(0,len(app.board[0]) - len(stone)):
            states.append({'num_rotations': r, 'board':drop([row[:] for row in app.board],  stone, i, app.stone_y//1), 'stone_x':i})
        stone = tetris.rotate_clockwise(stone)
    print("\n")
    print("Printing States Now")
    for b in states:
        for i in range(len(b['board'])-1):
            print(['\u25a1' if n>0 else " " for n in b['board'][i]],"-",i)
        print("\n")


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
    print(height,width)
    # Find highest block in each column
    highest_blocks = [0 for _ in range(width)]
    for x in range(width):
        if (highest_blocks[x] > 0): break
        for y in range(height):
            if (board[y][x] > 0):
                print("Found a block at",y,x,"=",0 + (height-y-1))
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
                        total += height-i
                # Cell to the left of a peak is also a hole
                if(0 <= x-1 and board[y][x-1] == 0):
                    # print("Cell",(x-1,y),"is just left of peak",(x,top_blocks[x]),"+1")
                    total += 1
                continue
            # Check if cell is surrounded by a 'tower'
            if(0 <= x-1):
                if(top_blocks[x-1] <= y and board[y][x] == 0): 
                    # print("Cell",(x,y),"is to the right of peak",(x-1,top_blocks[x-1]),"+1")
                    total += 1
            if(x+1 < width):
                if(top_blocks[x+1] <= y and board[y][x] == 0): 
                    # print("Cell",(x,y),"is to the left of peak",(x+1,top_blocks[x+1]),"+1")
                    total += 1
    return total

def test(app=tetris.TetrisApp):
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
    app = tetris.TetrisApp()
    # t1 = threading.Thread(target=app.run)
    # t2 = threading.Thread(target=test, args=(app,))
    # t1.start()
    # t2.start()
    # t1.join()
    # t2.join()
    app.gameover = False
    app.paused = False
    app.init_game()
    for i in range(2):
        app.new_stone()
        app.insta_drop()
    app.print_board()
    possible_board_states(app)
    print("Actual board")
    app.print_board()
    print([str(i) for i in range(len(app.board[0]))])
    print(holes_heuristic(app.board))    
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