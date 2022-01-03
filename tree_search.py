import math
import random


class Node:
    def __init__(self, board, parent=None):
        self.board = board
        self.parent = parent

        # Checking if state is terminal
        if self.board.is_win() or self.board.is_draw():
            self.is_terminal = True
        else:
            self.is_terminal = False

        # Checking if state is fully expanded
        self.is_fully_expanded = self.is_terminal

        self.visits = 0
        self.total_score = 0

        self.children = {}


class MCTS:
    def __init__(self, num_iterations=1000):
        self.num_iterations = num_iterations

    def search(self, initial_state):
        self.root = Node(initial_state)

        for _ in range(self.num_iterations):
            # Selection phase
            node = self.select(self.root)

            # Simulation phase
            score = self.rollout(node.board)

            # Backpropagation phase
            self.backpropagate(node, score)

        try:
            return self.select_best_node(self.root, 0)
        except:
            pass

    def select(self, node):
        while not node.is_terminal:
            if node.is_fully_expanded:
                node = self.select_best_node(node, 2)
            else:
                return self.expand(node)

        return node

    def expand(self, node):
        # Generating all valid states that node has
        states = node.board.generate_states()

        for state in states:
            if str(state.position) not in node.children:
                ''' 
                Creating new node with position generated from
                the parent node, that is the node that was sent as parameter
                '''
                new_node = Node(state, node)
                
                # Adding new node to list of children of parent node
                node.children[str(state.position)] = new_node

                # Checking if node is fully expanded
                if len(states) == len(node.children):
                    node.is_fully_expanded = True

                return new_node

    # Get to the terminal state by making random moves
    def rollout(self, board):
        while not board.is_win():
            '''
                This will output an error in case terminal state that is 
                not a win, in that scenario we return 0
            '''
            try:
                board = random.choice(board.generate_states())

            # Game is drawn
            except:
                #print(board)
                return 0
        
        #print(board)
        if board.player_2 == "x": return 1
        elif board.player_2 == "o": return -1

    def backpropagate(self, node, score):
        while node is not None:
            node.visits += 1
            node.total_score += score
            node = node.parent

    def select_best_node(self, node, exploration_constant):
        best_score = float("-inf")
        best_moves = []

        for child_node in node.children.values():
            if child_node.board.player_2 == "x": current_player = 1
            elif child_node.board.player_2 == "o": current_player = -1

            # UCT formula
            move_score = current_player * child_node.total_score / child_node.visits + exploration_constant * math.sqrt(math.log(node.visits) / child_node.visits)
            
            # Comparing calculated move with the best move
            if move_score > best_score:
                best_score = move_score
                best_moves = [child_node]

            # In case that calculated move is just as good as best move
            elif move_score == best_score:
                best_moves.append(child_node)

        return random.choice(best_moves)