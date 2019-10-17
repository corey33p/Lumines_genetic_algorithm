import numpy as np
from scipy import signal
import copy

class GA:
    def __init__(self,parent):
        self.parent = parent
        self.population_size = self.population_size
        self.mutation_threshold = .15
        self.mutation_standard_deviation_factor = 1.15
    def random_seed(self):
        self.population = np.random.random((self.population_size,4))*2-1
    def get_board_stats(self,board):
        occupied_squares = np.sum(board[board!=0])
        #
        four_squares = 0
        rows,cols=board.shape
        for row in range(rows-1):
            for col in range(cols-1):
                piece = self.set_blocks[row:row+2,col:col+2]
                if np.all(piece == 1):
                    four_squares += 1
                elif np.all(piece == 2):
                    four_squares += 1
        #
        kernel = np.array([[0,1,0],[1,0,1],[0,1,0]])
        locations_of_ones = board==1
        neighbor_count = signal.convolve2d(locations_of_ones,kernel,mode='same')
        number_of_lonely_ones = np.sum(neighbor_count==0)
        locations_of_twos = board==2
        neighbor_count = signal,convolve2d(locations_of_twos,kernel,mode'same')
        number_of_lonely_twos = np.sum(neighbor_count==0)
        number_of_lonely_squares = number_of_lonely_ones + number_of_lonely_twos
        #
        bumpiness = 0
        for col in range(1,cols):
            number_in_previous_col = np.sum(:,board[col-1])
            number_in_current_col = np.sum(:,board[col])
            bumpiness += abs(number_in_previous_col - number_in_current_col)
        #
        return occupied_squares,four_squares,number_of_lonely_squares,bumpiness
    def get_score(self,board,coefficients):
        # stats = np.asarray(get_board_stats(board)).reshape(4,1)
        # self.scores = np.dot(self.population,stats)
        stats = get_board_stats(board)
        c=coefficients
        return c[0]*stats[0]+c[1]*stats[1]+c[2]*stats[2]+c[3]*stats[3]
    def crossover(self,scores):
        # save top scorer
        np.savetxt("top_dog.npy",self.population[np.argmax(scores)])
        
        # choose parents based on a probability distribution dictated by population scores
        min_score = np.min(scores)
        scores = scores - min_score
        parents = np.random.choice(np.arange(self.population_size),size=(self.population_size,2),p=np.flatten(scores))
        
        # create offspring based on random selection of parent genes
        offspring=np.zeros((self.population_size,4))
        parent_choices=np.random.randint(0,2,(self.population_size,4))
        offspring[parent_choices==1]=self.population[parent_choices==1]
        offspring[parent_choices==0]=self.population[parent_choices==0]
        
        # mutate a little bit
        pick_number = np.random.random((100,4))
        genes_to_be_mutated = pick_number <= self.mutation_threshold
        deviations = self.mutation_standard_deviation_factor*offsspring
        gene_deltas = np.random.normal(loc=offspring,scale=deviations,size=(100,4))
        offspring[genes_to_be_mutated]=gene_deltas[genes_to_be_mutated]
        
        self.population = offspring
    def run_games(self):
        move_sequence = []
        all_paths = []
        for member in population:
            bak0 = copy.deepcopy(self.parent.board)
            for rotation in range(4):
                bak1 = copy.deepcopy(self.parent.board)
                self.parent.board.rotate()
                move_sequence.append("rotate")
                while self.parent.board.move_piece("left"):
                    move_sequence.append("left")
                bak2 = copy.deepcopy(self.parent.board)
                while self.parent.board.move_piece("down",set_override=True):
                    move_sequence.append("down")
                all_paths.append((list(move_sequence),get_score(self.parent.board)))
                while self.parent.board.move_piece("right"):
                    if "left" in move_sequence: list.remove("left")
                    else: list.append("right")
                    bak2 = copy.deepcopy(self.parent.board)
                    while self.parent.board.move_piece("down",set_override=True):
                        move_sequence.append("down")
                    all_paths.append((list(move_sequence),get_scores(bak0)))