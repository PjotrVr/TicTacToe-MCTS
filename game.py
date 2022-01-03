from copy import deepcopy
from tree_search import Node, MCTS


# Board class for TicTacToe
class TicTacToe:
    def __init__(self, num_iterations=1000, board=None):
        # Defining players
        self.player_1 = "x"
        self.player_2 = "o"
        self.empty = "."
        self.num_iterations = num_iterations

        # Creates board
        self.position = {}
        self.create_board()

        # Copies board position if it's passed
        if board is not None:
            self.__dict__ = deepcopy(board.__dict__)

    # Creates 3x3 board
    def create_board(self):
        for row in range(3):
            for col in range(3):
                self.position[row, col] = self.empty
    
    # Print board state
    # Reason why I use __str__ is because we are constantly passing objects
    # so in the end it will be easier doing it this way
    def __str__(self):
        board_str = ""
        for row in range(3):
            for col in range(3):
                board_str += f"{self.position[row, col]}\t"
            board_str += "\n"
        
        board_str += f"\n-----------------\nPlayer {self.player_1} to move:\n-----------------\n" 
        
        return board_str
    
    # Make a possible move
    def make_move(self, row, col):
        # Creating new board object of our current position
        board = TicTacToe(board=self)

        # Play the move
        board.position[row, col] = board.player_1
        board.player_1, board.player_2 = board.player_2, board.player_1

        return board

    def is_win(self):
        # Checking for vertical win
        for col in range(3):
            if self.position[0, col] == self.player_2 and self.position[1, col] == self.player_2 and self.position[2, col] == self.player_2:
                return True

        # Checking for horizontal win
        for row in range(3):
            if self.position[row, 0] == self.player_2 and self.position[row, 1] == self.player_2 and self.position[row, 2] == self.player_2:
                return True
            
        # Checking for / diagonal
        if self.position[0, 2] == self.player_2 and self.position[1, 1] == self.player_2 and self.position[2, 0] == self.player_2:
            return True

        # Checking for \ diagonal
        if self.position[0, 0] == self.player_2 and self.position[1, 1] == self.player_2 and self.position[2, 2] == self.player_2:
            return True

        return False

    def is_draw(self):
        '''
            All positions must be filled with combination of symbols
            from player 1 and player 1, thus 0 of them can be symbol
            that is used for empty positions. First we always check if
            filled board is won, because if it is then it doesn't matter
            if every position is taken.
        '''
        for row, col in self.position:
            if self.position[row, col] == self.empty:
                return False
        
        return True

    # Generates legal states as data
    def generate_states(self):
        action_list = []

        for row in range(3):
            for col in range(3):
                if self.position[row, col] == self.empty:
                    action_list.append(self.make_move(row, col))

        return action_list

    def run(self):

        print(self)

        mcts = MCTS(num_iterations=self.num_iterations)

        while True:    
            user_input = input("Enter coordinates (x, y): ")
            x_cor = int(user_input[0]) - 1
            y_cor = int(user_input[-1]) - 1
            '''
            ### UNCOMMENT THIS IF YOU WANT TO CHECK VALIDITY OF INPUT
            while x_cor not in [0, 1, 2] and y_cor not in [0, 1, 2]:
                print("Wrong input!")
                user_input = input("Enter coordinates (x, y): ")
                x_cor = int(user_input[0])
                y_cor = int(user_input[-1])
            '''

            self = self.make_move(y_cor, x_cor)
            
            print(self)

            # Now AI plays a move
            best_move = mcts.search(self)
            try:
                self = best_move.board
                print(self)
            
            # Case where game is over
            except:
                pass

                
            if self.is_win():
                print(f"Player {self.player_2} has won the game!")
                break

            elif self.is_draw():
                print("Game is drawn!")
                break
            

if __name__ == "__main__":
    board = TicTacToe()
    ### I used 5 iterations here just to test all cases, in reality you'd use around 1000 iterations
    mcts = MCTS(num_iterations=5)
    
    # AI vs AI
    while True:
        try:
            best_move = mcts.search(board)
            board = best_move.board
            
        except:
            print(board)
            if board.is_win():
                print(f"Player {board.player_2} won the game!")
            else:
                print("Game is drawn!")

            break
    