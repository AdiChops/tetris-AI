from random import choice
from itertools import permutations

cols =      10
rows =      20

tetris_shapes = {'T':
    [[1, 1, 1],
     [0, 1, 0]],

    'S': [[0, 2, 2],
        [2, 2, 0]],

    'Z':[[3, 3, 0],
        [0, 3, 3]],

    'J':[[4, 0, 0],
        [4, 4, 4]],

    'L':[[0, 0, 5],
        [5, 5, 5]],

    'I':[[6, 6, 6, 6]],

    'O':[[7, 7],
        [7, 7]]
}
perms = list(permutations('TSZJLIO', 7))


# Define the shapes of the single parts

def rotate_clockwise(shape):
    return [
        [ shape[y][x] for y in range(len(shape)) ]
        for x in range(len(shape[0]) - 1, -1, -1)
    ]

def check_collision(board, shape, offset):
    off_x, off_y = offset
    for cy, row in enumerate(shape):
        for cx, cell in enumerate(row):
            try:
                if cell and board[ cy + off_y ][ cx + off_x ]:
                    return True
            except IndexError:
                return True
    return False

def remove_row(board, row):
    del board[row]
    return [[0 for i in range(cols)]] + board

def join_matrixes(mat1, mat2, mat2_off):
    off_x, off_y = mat2_off
    for cy, row in enumerate(mat2):
        for cx, val in enumerate(row):
            # print('cy',cy+off_y-1)
            # print('cx',cx+off_x)
            # print('mat=', len(mat1))
            # print('mat[0]=',len(mat1[0]))
            mat1[cy+off_y-1 ][cx+off_x] += val
    return mat1

def new_board():
    board = [[ 0 for x in range(cols) ] for y in range(rows)]
    board += [[ 1 for x in range(cols)]]
    return board

class TetrisGame(object):
    def __init__(self):
        self.rows = rows
        self.cols = cols
        self.stack = [i for i in choice(perms)]
        self.next_letter = self.stack.pop()
        self.next_stone = tetris_shapes[self.next_letter]
        self.gameover = False
        self.paused = False
        self.new_game()
    
    def new_game(self):
        self.board = new_board()
        self.new_stone()
        self.level = 1
        self.score = 0
        self.lines = 0

    
    def start_game(self):
        if self.gameover:
            self.init_game()
            self.gameover = False
    
    def new_stone(self):
        if len(self.stack) == 0:
            self.stack = [i for i in choice(perms)]
        self.stone_letter = self.next_letter
        self.stone = self.next_stone[:]
        self.next_letter = self.stack.pop()
        self.next_stone = tetris_shapes[self.next_letter]
        self.stone_x = int(cols / 2 - len(self.stone[0])/2)
        self.stone_y = 0

        if check_collision(self.board, self.stone,(self.stone_x, self.stone_y)):
            self.gameover = True
    
    def print_board(self):
        for i in range(len(self.board)-1):
            print(['\u25a1' if n>0 else " " for n in self.board[i]],"-",i)
    
    def add_cl_lines(self, n):
        linescores = [0, 40, 100, 300, 1200]
        self.lines += n
        self.score += linescores[n] * self.level
        if self.lines >= self.level*6:
            self.level += 1
            newdelay = 1000-50*(self.level-1)
            newdelay = 100 if newdelay < 100 else newdelay
            return newdelay
        else:
            return None
    
    def move(self, delta_x):
        if not self.gameover and not self.paused:
            new_x = self.stone_x + delta_x
            if new_x < 0:
                new_x = 0
            if new_x > cols - len(self.stone[0]):
                new_x = cols - len(self.stone[0])
            if not check_collision(self.board,
                                   self.stone,
                                   (new_x, self.stone_y)):
                self.stone_x = new_x
    
    def drop(self, manual):
        if not self.gameover and not self.paused:
            self.score += 1 if manual else 0
            self.stone_y += 1
            if check_collision(self.board,
                               self.stone,
                               (self.stone_x, self.stone_y)):
                self.board = join_matrixes(
                  self.board,
                  self.stone,
                  (self.stone_x, self.stone_y))
                self.new_stone()
                cleared_rows = 0
                while True:
                    for i, row in enumerate(self.board[:-1]):
                        if 0 not in row:
                            self.board = remove_row(
                              self.board, i)
                            cleared_rows += 1
                            break
                    else:
                        break
                self.add_cl_lines(cleared_rows)
                return True
        return False

    def toggle_pause(self):
        self.paused = not self.paused
    
    def rotate_stone(self):
        if not self.gameover and not self.paused:
            new_stone = rotate_clockwise(self.stone)
            if not check_collision(self.board,
                                   new_stone,
                                   (self.stone_x, self.stone_y)):
                self.stone = new_stone
    
    def insta_drop(self):
        if not self.gameover and not self.paused:
            while(not self.drop(True)):
                pass
