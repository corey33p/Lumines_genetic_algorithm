import numpy as np

class Board:
    def __init__(self,size,queue=None):
        # self.parent = parent
        self.queue = queue
        self.size=size
        self.printing_board = True
    def print_board(self,direct_print=False):
        ########
        combined_board = np.copy(self.set_blocks)
        combined_board[self.active_blocks != 0] = self.active_blocks[self.active_blocks != 0]
        rows,cols=combined_board.shape
        board_str = ""
        for row in range(rows):
            for col in range(cols):
                square_type = combined_board[row,col]
                if square_type == 0: board_str+="  "
                elif square_type == 1: board_str+="▒▒"
                elif square_type == 2: board_str+="██"
            board_str+="\n"
        board_str+="\n"
        if direct_print: print("______________________________\n"+board_str)
        # self.parent.display.text_out.overwrite(board_str)
        self.board_str = board_str
        return board_str
    def add_piece(self):
        next_piece = self.queue.pop(0)
        self.active_blocks[0:2,8:10]=next_piece
        if len(self.queue)<5:
            self.queue.append(np.random.randint(1,3,(2,2)))
    def move_piece(self,direction="down",break_override=False):
        going_to_happen=True
        set_piece = False
        if direction == "down":
            if np.any(self.active_blocks[self.active_blocks.shape[0]-1,:]):
                going_to_happen = False
                set_piece = True
            else:
                desired_loc = np.copy(self.active_blocks)
                desired_loc = np.roll(desired_loc,1,0)
                if np.any(np.logical_and(desired_loc,self.set_blocks)):
                    going_to_happen = False
                    set_piece = True
        elif direction == "left":
            if np.any(self.active_blocks[:,0]):
                going_to_happen = False
            else: 
                desired_loc = np.copy(self.active_blocks)
                desired_loc = np.roll(desired_loc,-1,1)
                if np.any(np.logical_and(desired_loc,self.set_blocks)):
                    going_to_happen = False
        elif direction == "right":
            if np.any(self.active_blocks[:,self.active_blocks.shape[1]-1]):
                going_to_happen = False
            else: 
                desired_loc = np.copy(self.active_blocks)
                desired_loc = np.roll(desired_loc,1,1)
                if np.any(np.logical_and(desired_loc,self.set_blocks)):
                    going_to_happen = False
        elif direction == "up":
            going_to_happen = False
        if going_to_happen:
            try: self.active_blocks = desired_loc
            except: 
                print("direction: " + str(direction))
                input(self.print_board())
        # else:
            # print("not going to happen")
        if set_piece: self.set_piece(break_override=break_override)
        if self.printing_board: self.print_board()
        if going_to_happen: return True
        else: return False
    def rotate(self,clockwise=True):
        if not np.any(self.active_blocks): return
        piece_loc = np.argwhere(self.active_blocks!=0)
        row,col = np.min(piece_loc[:,0]),np.min(piece_loc[:,1])
        piece = self.active_blocks[row:row+2,col:col+2]
        if clockwise:
            piece = np.rot90(piece,k=3)
        else:
            piece = np.rot90(piece)
        self.active_blocks[row:row+2,col:col+2]=piece
        if self.printing_board: self.print_board()
    def set_piece(self,break_override=False):
        self.set_blocks[self.active_blocks != 0] = self.active_blocks[self.active_blocks != 0]
        self.active_blocks[:,:]=0
        self.drape_blocks()
        if not break_override:
            self.auto_break()
        if np.any(self.set_blocks[:2,:]!=0):
            self.game_lost = True
        else:
            self.add_piece()
            self.pieces_placed += 1
    def auto_break(self):
        while self.break_blocks():
            self.drape_blocks()
    def drape_blocks(self):
        rows,cols=self.set_blocks.shape
        for col in range(cols):
            new_col = np.zeros([rows])
            elements_added = 0
            for row in reversed(range(rows)):
                block_type = self.set_blocks[row,col]
                if block_type != 0:
                    new_col[rows-elements_added-1]=block_type
                    elements_added += 1
            if elements_added > 0:
                self.set_blocks[:,col]=new_col
    def break_blocks(self):
        rows,cols=self.set_blocks.shape
        spots_to_break = []
        for row in range(rows-1):
            for col in range(cols-1):
                piece = self.set_blocks[row:row+2,col:col+2]
                if np.all(piece == 1):
                    spots_to_break.append((row,col))
                elif np.all(piece == 2):
                    spots_to_break.append((row,col))
        for spot in spots_to_break:
            row,col=spot
            self.set_blocks[row:row+2,col:col+2] = 0
        if spots_to_break:
            self.score += 2**(len(spots_to_break)-1)
            # self.parent.display.update_score(self.score)
        return bool(spots_to_break)
    def whole_board(self):
        board = np.copy(self.set_blocks)
        board[self.active_blocks!=0]=self.active_blocks[self.active_blocks!=0]
        return board
    def new_game(self,queue=None):
        self.queue = queue
        working_size = (self.size[0]+2,self.size[1])
        self.set_blocks = np.zeros(working_size,np.int32)
        self.active_blocks = np.zeros(working_size,np.int32)
        if self.queue is None: self.queue = [np.random.randint(1,3,(2,2)) for i in range(4)]
        self.add_piece()
        self.game_lost = False
        self.pieces_placed = 0
        self.score = 0
        # self.parent.display.update_score(self.score)
        if self.printing_board: self.print_board()
