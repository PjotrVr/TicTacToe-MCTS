from copy import deepcopy

# Board class for TicTacToe
class Board:
    def __init__(self, board=None):
        # Defining players
        self.player_1 = "x"
        self.player_2 = "o"
        self.empty = "."

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
        board = Board(self)

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
        pass

if __name__ == "__main__":
    board = Board()
    print(board.__dict__)
    print(board)
    
    print(board.generate_states()[3])
    '''
    board_1 = board.make_move(1, 1) 
    print(board_1.__dict__)
    print(board_1)
    
    board_2 = board_1.make_move(2, 2) 
    print(board_2.__dict__)
    print(board_2)
    '''