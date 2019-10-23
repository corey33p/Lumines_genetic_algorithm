from Lumines_board import Board
from Lumines_Display import Display
from Lumines_GA import GA
from tkinter import mainloop
import os
import win32gui
import win32con
import threading
from queue import Queue
import numpy as np
import copy

np.set_printoptions(suppress=True, precision=2, linewidth=140)

class Parent:
    def __init__(self):
        self.board_size=(10,16)
        self.board = Board(self.board_size)
        # self.display  = Display(self,self.board_size)
        self.GA = GA()
        # self.resize_CLI_window()
        #
        # training_thread = threading.Thread(target=self.simulate_games)
        # training_thread.daemon = True
        # training_thread.start()
        self.simulate_games()
        #
        # mainloop()
    def simulate_games(self):
        forever = True
        generation = 0
        while forever:
            generation += 1
            self.GA.scores = np.zeros((self.GA.population_size))
            queue = [np.random.randint(1,3,(2,2)) for i in range(75)]
            self.board.new_game(queue=queue)
            game_bak = copy.deepcopy(self.board)
            for i,member in enumerate(self.GA.population):
                # print("member: " + str(member))
                self.board = copy.deepcopy(game_bak)
                moves = 0
                max_moves = 0
                while (not self.board.game_lost) and self.board.pieces_placed < 500:
                    move = self.GA.find_move1(copy.deepcopy(self.board),member)
                    moves+=1
                    for step in move: 
                        # print("step: " + str(step))
                        if step == "left": self.board.move_piece("left")
                        elif step == "right": self.board.move_piece("right")
                        elif step == "rotate": self.board.rotate()
                        elif step == "drop": 
                            while self.board.move_piece("down"): pass
                        if self.board.game_lost: break
                    # print("moves: " + str(moves),end="\r")
                    # print(self.board.print_board())
                    if moves > max_moves: max_moves = moves
                # print("moves: " + str(moves))
                # print("self.board.game_lost: " + str(self.board.game_lost))
                self.GA.scores[i]=self.board.score+.05*self.board.pieces_placed**2
                print("self.GA.scores["+str(i)+"]: " + str(self.GA.scores[i]//.01/100),end="                      \r")
            scores = np.asarray(self.GA.scores)
            print("Generation "+str(generation)+"; mean score: "+str(np.mean(scores)//.01/100)+"; max score: "+str(max(scores)//.01/100)+"; max moves: "+str(max_moves))
            self.GA.crossover(np.asarray(self.GA.scores))
            print("self.GA.top_dog: " + str(self.GA.top_dog))
    def resize_CLI_window(self):
        def get_windows():
            def check(hwnd, param):
                title = win32gui.GetWindowText(hwnd)
                if 'Lumines_Main' in title and 'Notepad++' not in title:
                    param.append(hwnd)
            wind = []
            win32gui.EnumWindows(check, wind)
            return wind
        self.cli_handles = get_windows()
        for window in self.cli_handles:
            # win32gui.MoveWindow(window,-1020,300,1015,640,True)
            win32gui.MoveWindow(window,16,62,1087,851,True)
            # win32gui.MoveWindow(window,-141,1107,1002,989,True)
    def close(self):
        for handle in self.cli_handles:
            win32gui.PostMessage(handle,win32con.WM_CLOSE,0,0)

if __name__ == '__main__':
    main_object = Parent()