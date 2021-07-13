

import random
import os
import time
import neat
import visualize
import pickle
from board import Board


gen = 0

def eval_genomes(genomes, config):
	print('in eval')

	global gen

	gen += 1


	nets = []
	boards = []
	ge = []

	for genome_id, genome in genomes:
		genome.fitness = 0
		net = neat.nn.FeedForwardNetwork.create(genome, config)
		nets.append(net)
		boards.append(Board())
		ge.append(genome)

	score = 0

	run = True

	while run and len(boards) > 0:

		for x, board in enumerate(boards):
			ge[x].fitness += 1

			output = nets[boards.index(board)].activate((board.matrix[0][0],
															board.matrix[0][1],
															board.matrix[0][2],
															board.matrix[0][3],
															board.matrix[1][0],
															board.matrix[1][1],
															board.matrix[1][2],
															board.matrix[1][3],
															board.matrix[2][0],
															board.matrix[2][1],
															board.matrix[2][2],
															board.matrix[2][3],
															board.matrix[3][0],
															board.matrix[3][1],
															board.matrix[3][2],
															board.matrix[3][3]
															))
			max_value = max(output)
			max_index = output.index(max_value)

			if max_index == 0:
				board.left()
			if max_index == 1:
				board.right()
			if max_index == 2:
				board.up()
			if max_index == 3:
				board.down()

		for board in boards:
			if board.game_state() == 0:
				nets.pop(boards.index(board))
				ge.pop(boards.index(board))
				boards.pop(boards.index(board))




def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    print('in run')
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    print('past config')
    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))




if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)



