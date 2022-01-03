from argparse import ArgumentParser

from game import TicTacToe

parser = ArgumentParser()
parser.add_argument("-i", "--iterations", help="number of iterations that tree search will use", type=int, default=1000)
args = vars(parser.parse_args())

num_iterations = list(args.values())[0]
board = TicTacToe(num_iterations=num_iterations)
board.run()