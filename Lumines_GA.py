import numpy as np
from scipy import signal
from scipy.ndimage import measurements
import copy
import random
import os

np.set_printoptions(suppress=True, precision=2, linewidth=140)

class GA:
    def __init__(self):
        self.population_size = 7
        self.mutation_threshold = .35
        self.mutation_standard_deviation_factor = 1.15
        self.random_seed()
    def random_seed(self):
        if os.path.isfile("save/top_dog.npy"):
            top_dog = np.loadtxt("save/top_dog.npy")
            self.population = np.random.normal(loc=top_dog,scale=abs(top_dog),size=(self.population_size,4))
            self.population[0,:] = top_dog
            # input("self.population:\n" + str(self.population))
        else: self.population = np.random.random((self.population_size,4))*2-1
    def get_board_stats(self,board):
        def average_cluster_size(ar):
            unique_vals = set(ar.flatten().tolist())
            unique_vals.remove(0)
            cluster_sizes = np.array(())
            for val in unique_vals:
                working_ar = (ar == val).astype(np.int32)
                a,b=measurements.label(working_ar)
                area=measurements.sum(working_ar,a,index=np.arange(1,a.max()+1))
                cluster_sizes=np.concatenate((cluster_sizes,np.array(area)))
            return np.mean(cluster_sizes)
        # aggregate height
        aggregate_height = np.sum(np.sum(board!=0,axis=0))
        
        # four squares (blocks that will break)
        locations_of_ones = board==1
        locations_of_twos = board==2
        kernel = np.array([[1,1],[1,1]])
        four_ones = signal.convolve2d(locations_of_ones,kernel,mode='same')
        four_twos = signal.convolve2d(locations_of_twos,kernel,mode='same')
        four_squares = np.sum(four_ones==4)+np.sum(four_twos==4)
        
        # # number of isolated pieces
        # kernel = np.array([[0,1,0],[1,0,1],[0,1,0]])
        # neighbor_count = signal.convolve2d(locations_of_ones,kernel,mode='same')
        # number_of_lonely_ones = np.sum(np.logical_and(neighbor_count==0,locations_of_ones!=0))
        # neighbor_count = signal.convolve2d(locations_of_twos,kernel,mode='same')
        # number_of_lonely_twos = np.sum(np.logical_and(neighbor_count==0,locations_of_twos!=0))
        # number_of_lonely_squares = number_of_lonely_ones + number_of_lonely_twos
        
        # average cluster size
        acs = average_cluster_size(board)
        
        # bumpiness
        column_heights = np.sum(board!=0,axis=0)
        adjacent_column_heights = np.roll(column_heights,1,0)
        column_deltas = abs(column_heights - adjacent_column_heights)
        bumpiness = np.sum(column_deltas)
        #
        return aggregate_height,four_squares,acs,bumpiness
    def get_score(self,board,coefficients):
        s = np.asarray(self.get_board_stats(board.whole_board())).reshape(4,1)
        c = coefficients
        # self.scores = np.dot(self.population,stats)
        return float(c[0]*s[0]+c[1]*s[1]+c[2]*s[2]+c[3]*s[3])
        # return random.random()*100;1
    def test_crossover(self):
        self.random_seed()
        scores = np.array([random.randint(0,999) for i in range(self.population_size)])
        self.crossover(scores)
    def crossover(self,scores):
        debug = False
        if debug: print("old population:\n" + str(self.population))
        if debug: print("scores: " + str(scores))
        # save top scorer
        top_dog = self.population[np.argmax(scores)]
        if debug: print("top_dog:\n" + str(top_dog))
        np.savetxt("save/top_dog.npy",top_dog,fmt='%f')
        
        # choose parents based on a probability distribution dictated by population scores
        min_score = np.min(scores)
        scores = scores / np.sum(scores)
        parents = np.random.choice(np.arange(self.population_size),size=(self.population_size,2),p=scores)
        if debug: print("parents:\n" + str(parents))
        
        # choose crossover method randomly
        method = np.random.randint(0,2,(self.population_size))
        
        # create offspring by averaging the parent genes
        parentA_ar = self.population[parents[...,0]]
        parentB_ar = self.population[parents[...,1]]
        offspring1=(parentA_ar+parentB_ar)/2
        if debug: print("parentA_ar:\n" + str(parentA_ar))
        if debug: print("parentB_ar:\n" + str(parentB_ar))
        if debug: print("offspring1:\n" + str(offspring1))

        # create offspring based on random selection of parent genes
        parent_choices = np.random.randint(0,2,(self.population_size,4))
        offspring2=np.zeros((self.population_size,4))
        offspring2[parent_choices==0]=parentA_ar[parent_choices==0]
        offspring2[parent_choices==1]=parentB_ar[parent_choices==1]
        if debug: print("parent_choices:\n" + str(parent_choices))
        if debug: print("offspring2:\n" + str(offspring2))
        
        if debug: print("method:\n" + str(method))
        offspring=np.zeros((self.population_size,4))
        offspring[method==0]=offspring1[method==0]
        offspring[method==1]=offspring2[method==1]
        if debug: print("offspring:\n" + str(offspring))
        
        # mutate a little bit
        pick_number = np.random.random((self.population_size,4))
        genes_to_be_mutated = pick_number <= self.mutation_threshold
        deviations = abs(self.mutation_standard_deviation_factor*offspring)
        gene_deltas = np.random.normal(loc=offspring,scale=deviations,size=(self.population_size,4))
        offspring[genes_to_be_mutated]=gene_deltas[genes_to_be_mutated]
        
        # save top dog
        offspring[0,:] = top_dog
        if debug: print("offspring:\n" + str(offspring))
        
        self.population = offspring
    def find_move(self,board,coefficients,first=True):
        if board.game_lost: 1/0
        animate=False
        c=coefficients
        # board.printing_board=False
        board.move_sequence = []
        all_paths = []
        scores = set()
        
        bak0 = copy.deepcopy(board)
        used_pieces = []
        for rotation in range(4):
            board.rotate()
            piece = list(board.active_blocks[board.active_blocks!=0])
            if piece not in used_pieces:
                used_pieces.append(piece)
                bak1 = copy.deepcopy(board)
                board.move_sequence.append("rotate")
                while board.move_piece("left"):
                    board.move_sequence.append("left")
                
                bak2 = copy.deepcopy(board)
                while board.move_piece("down",set_override=(not first)): pass
                board.move_sequence.append("drop")
                if animate: print(board.print_board())
                if first: 
                    if not board.game_lost: all_paths.append((list(board.move_sequence),self.find_move(board,c,first=False)))
                    else: all_paths.append((list(board.move_sequence),0))
                else: scores.add(self.get_score(board,c))
                
                board = copy.deepcopy(bak2)
                while board.move_piece("right"):
                    if "left" in board.move_sequence: board.move_sequence.remove("left")
                    else: board.move_sequence.append("right")
                    bak2 = copy.deepcopy(board)
                    while board.move_piece("down",set_override=(not first)): pass
                    board.move_sequence.append("drop")
                    if animate: print(board.print_board())
                    if first: 
                        if not board.game_lost: all_paths.append((list(board.move_sequence),self.find_move(board,c,first=False)))
                        else: all_paths.append((list(board.move_sequence),0))
                    else: scores.add(self.get_score(board,c))
                    
                    board = copy.deepcopy(bak2)
                board = copy.deepcopy(bak1)
        if first:
            # self.board = copy.deepcopy(bak0)
            # input("board restored.\n"+board.print_board())
            maxIndex=None
            maxScore=None
            for i,thing in enumerate(all_paths):
                if maxScore is None: maxScore = thing[1]
                if maxIndex is None: maxIndex = i
                if thing[1] > maxScore: 
                    maxScore = thing[1]
                    maxIndex = i

            bestMove = all_paths[maxIndex][0]
            board.printing_board=True
            return bestMove
        else:
            return max(scores)
    def find_move1(self,board,coefficients):
        if board.game_lost: 1/0
        animate=False
        c=coefficients
        # board.printing_board=False
        board.move_sequence = []
        all_paths = []
        scores = set()
        
        bak0 = copy.deepcopy(board)
        used_pieces = []
        for rotation in range(4):
            board.rotate()
            piece = list(board.active_blocks[board.active_blocks!=0])
            if piece not in used_pieces:
                used_pieces.append(piece)
                bak1 = copy.deepcopy(board)
                board.move_sequence.append("rotate")
                while board.move_piece("left"):
                    board.move_sequence.append("left")
                
                bak2 = copy.deepcopy(board)
                while board.move_piece("down",set_override=True): pass
                board.move_sequence.append("drop")
                if animate: print(board.print_board())
                if not board.game_lost: all_paths.append((list(board.move_sequence),self.get_score(board,c)))
                else: all_paths.append((list(board.move_sequence),-99999))
                
                board = copy.deepcopy(bak2)
                while board.move_piece("right"):
                    if "left" in board.move_sequence: board.move_sequence.remove("left")
                    else: board.move_sequence.append("right")
                    bak2 = copy.deepcopy(board)
                    while board.move_piece("down",set_override=True): pass
                    board.move_sequence.append("drop")
                    if animate: print(board.print_board())
                    if not board.game_lost: all_paths.append((list(board.move_sequence),self.get_score(board,c)))
                    else: all_paths.append((list(board.move_sequence),-99999))
                    
                    board = copy.deepcopy(bak2)
                board = copy.deepcopy(bak1)
            
        # self.board = copy.deepcopy(bak0)
        # input("board restored.\n"+board.print_board())
        maxIndex=None
        maxScore=None
        for i,thing in enumerate(all_paths):
            if maxScore is None: maxScore = thing[1]
            if maxIndex is None: maxIndex = i
            if thing[1] > maxScore: 
                maxScore = thing[1]
                maxIndex = i

        bestMove = all_paths[maxIndex][0]
        board.printing_board=True
        return bestMove