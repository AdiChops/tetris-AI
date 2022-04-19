#!/usr/bin/env python3
#-*- coding: utf-8 -*-

# Very simple tetris implementation
#
# Control keys:
#       Down - Drop stone faster
# Left/Right - Move stone
#         Up - Rotate Stone clockwise
#     Escape - Quit game
#          P - Pause game
#     Return - Instant drop
#
# Have fun!

# NOTE: If you're looking for the old python2 version, see
#       <https://gist.github.com/silvasur/565419/45a3ded61b993d1dd195a8a8688e7dc196b08de8>

# Copyright (c) 2010 "Laria Carolin Chabowski"<me@laria.me>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import pygame, sys

from logic import TetrisGame
# import AI

# The configuration
cell_size = 40
maxfps =    60

colors = [
    (0, 0, 0),
    (160, 0, 235),
    (40, 175, 65),
    (240, 35, 45),
    (40, 0, 230),
    (240, 151, 40),
    (35, 190, 235),
    (245, 210, 50),
    (35, 35, 35) # Helper color for background grid
]
class TetrisApp(object):
    def __init__(self):
        self.game = TetrisGame()
        pygame.init()
        pygame.key.set_repeat(250,25)
        self.width = cell_size*(self.game.cols+6)
        self.height = cell_size*self.game.rows
        self.rlim = cell_size*self.game.cols
        self.bground_grid = [[ 8 if x%2==y%2 else 0 for x in range(self.game.cols)] for y in range(self.game.rows)]

        self.default_font =  pygame.font.Font(pygame.font.match_font("calibri"), 18)

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.event.set_blocked(pygame.MOUSEMOTION)

        self.init_game()

    def init_game(self):
        pygame.time.set_timer(pygame.USEREVENT+1, 1000)

    def disp_msg(self, msg, topleft):
        x,y = topleft
        for line in msg.splitlines():
            self.screen.blit(
                self.default_font.render(
                    line,
                    False,
                    (255,255,255),
                    (0,0,0)),
                (x,y))
            y+=14

    def center_msg(self, msg):
        for i, line in enumerate(msg.splitlines()):
            msg_image =  self.default_font.render(line, False,
                (255,255,255), (0,0,0))

            msgim_center_x, msgim_center_y = msg_image.get_size()
            msgim_center_x //= 2
            msgim_center_y //= 2

            self.screen.blit(msg_image, (
              self.width // 2-msgim_center_x,
              self.height // 2-msgim_center_y+i*22))

    def draw_matrix(self, matrix, offset):
        off_x, off_y  = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(
                        self.screen,
                        colors[val],
                        pygame.Rect(
                            (off_x+x) * cell_size,
                            (off_y+y) * cell_size,
                            cell_size,
                            cell_size
                        ),
                        0
                    )
                    pygame.draw.rect(
                        self.screen,
                        (0,0,0),
                        pygame.Rect(
                            (off_x+x) * cell_size,
                            (off_y+y) * cell_size,
                            cell_size,
                            cell_size
                        ),
                        1
                    )

    def add_cl_lines(self, n):
        newdelay = self.game.add_cl_lines(n)
        if newdelay:
            pygame.time.set_timer(pygame.USEREVENT+1, newdelay)

    def quit(self):
        self.center_msg("Exiting...")
        pygame.display.update()
        sys.exit()


    def start_game(self):
        self.game.start_game()

    def run(self):
        key_actions = {
            'ESCAPE':   self.quit,
            'LEFT':     lambda:self.game.move(-1),
            'RIGHT':    lambda:self.game.move(+1),
            'DOWN':     lambda:self.game.drop(True),
            'UP':       self.game.rotate_stone,
            'p':        self.game.toggle_pause,
            'SPACE':    self.start_game,
            'RETURN':   self.game.insta_drop
        }

        self.gameover = False
        self.paused = False

        dont_burn_my_cpu = pygame.time.Clock()
        while 1:
            self.screen.fill((0,0,0))
            if self.gameover:
                self.center_msg("""Game Over!\nYour score: %d
Press space to continue""" % self.game.score)
            else:
                if self.paused:
                    self.center_msg("Paused")
                else:
                    pygame.draw.line(self.screen,
                        (255,255,255),
                        (self.rlim+1, 0),
                        (self.rlim+1, self.height-1))
                    self.disp_msg("Next:", (
                        self.rlim+cell_size,
                        2))
                    self.disp_msg("Score: %d\n\n\nLevel: %d\
\n\nLines: %d" % (self.game.score, self.game.level, self.game.lines),
                        (self.rlim+cell_size, cell_size*5))
                    self.draw_matrix(self.bground_grid, (0,0))
                    self.draw_matrix(self.game.board, (0,0))
                    self.draw_matrix(self.game.stone, (self.game.stone_x, self.game.stone_y))
                    self.draw_matrix(self.game.next_stone, (self.game.cols+1,2))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.USEREVENT+1:
                    self.game.drop(False)
                elif event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    for key in key_actions:
                        if event.key == eval("pygame.K_"+key):
                            key_actions[key]()

            dont_burn_my_cpu.tick(maxfps)

if __name__ == '__main__':
    App = TetrisApp()
    App.run()