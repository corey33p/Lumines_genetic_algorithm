from PIL import Image, ImageTk, ImageDraw
import tkinter as tk
from tkinter import Canvas,Tk,ttk,Label,Entry,Button,mainloop,Text,Frame,IntVar,Checkbutton,Grid
import os
import numpy as np
from tkinter import filedialog
import math
from text_window import TextWriter
import random
import time

class Display:
    def __init__(self, parent,size):
        self.parent = parent
        self.size = size
        self.main_font = ("Courier", 38, "bold")
        self.max_win_size = (1111,755)
        self.canvas_dimension = min(((self.max_win_size[0]-40)/2,self.max_win_size[1]-230))
        self.setup_window()
    def setup_window(self):
        # initial setup
        self.primary_window = Tk()
        self.primary_window.wm_title("Lumines_Main")
        self.primary_window.geometry('1031x777-1+0')
        # self.primary_window.geometry('1274x960+1274-1055')
        self.primary_window.minsize(width=100, height=30)
        self.primary_window.maxsize(width=self.max_win_size[0], height=self.max_win_size[1])
        
        # the textbox
        self.textbox=Text(self.primary_window, background="black", height=self.size[0]+2, width=self.size[1]*2,foreground="green",font=self.main_font)
        self.textbox.grid(row=0,column=0,sticky='ew')
        self.primary_window.grid_columnconfigure(0, weight=1)
        # sys.stdout = self.parent.text_out = TextWriter(self.textbox)
        self.text_out = TextWriter(self.textbox)
        
        # button bindings
        self.primary_window.bind("<Left>", lambda event: self.arrow_key("L"))
        self.primary_window.bind("<Right>", lambda event: self.arrow_key("R"))
        self.primary_window.bind("<Up>", lambda event: self.arrow_key("U"))
        self.primary_window.bind("<Down>", lambda event: self.arrow_key("D"))
        self.primary_window.bind("<space>", lambda event: self.parent.board.new_game())
        
        #
        self.score_entry = Entry(self.primary_window,justify='center')
        self.score_entry.insert("end","0")
        self.score_entry.config(font=self.main_font,width=5,background="black",foreground="green")
        # self.score_entry.config(state="disabled")
        self.score_entry.grid(row=1,column=0)
    def arrow_key(self,which):
        if which == "L":
            self.parent.board.move_piece(direction="left")
        elif which == "R":
            self.parent.board.move_piece(direction="right")
        elif which == "U":
            self.parent.board.rotate()
        elif which == "D":
            self.parent.board.move_piece(direction="down")
    def update_score(self,val):
        val = str(val)
        self.score_entry.delete(0,'end')
        self.score_entry.insert('end',val)
