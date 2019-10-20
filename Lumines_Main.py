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
        while forever:
            self.GA.scores = np.zeros((self.GA.population_size))
            for i,member in enumerate(self.GA.population):
                self.board.new_game()
                while (not self.board.game_lost) and self.board.pieces_placed < 50:
                    move = self.GA.find_move(copy.deepcopy(self.board),member)
                    # print("move: " + str(move))
                    for step in move: 
                        # print("step: " + str(step))
                        if step == "left": self.board.move_piece("left")
                        elif step == "right": self.board.move_piece("right")
                        elif step == "rotate": self.board.rotate()
                        elif step == "drop": 
                            while self.board.move_piece("down"): pass
                        if self.board.game_lost: break
                    # print(self.board.print_board())
                # print("self.board.game_lost: " + str(self.board.game_lost))
                self.GA.scores[i]=self.board.score+self.board.pieces_placed
                print("self.GA.scores["+str(i)+"]: " + str(self.GA.scores[i]))
            self.GA.crossover()
    def resize_CLI_window(self):
        def get_windows():
            def check(hwnd, param):
                title = win32gui.GetWindowText(hwnd)
                if 'Rubiks_Main' in title and 'Notepad++' not in title:
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
    