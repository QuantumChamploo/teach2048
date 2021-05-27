
import random
import os
import time
import neat
import visualize
import pickle
from bareSnake import snakeGame
import numpy as np
import math

gen = 0

def makeList(mat):
	hld = []
	for i in mat:
		for j in i:
			#print(j)
			hld.append(j)
	return hld

def find_index(array):
    s = np.array(array)
    sort_index = np.argsort(s)
    return sort_index

def eval_genomes(genomes, config):
    print('in eval')

    global gen

    gen += 1


    nets = []
    games = []
    ge = []

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        games.append(snakeGame())
        ge.append(genome)
    run = True
    tab = 0

    while run and len(games) > 0:
        tab +=1
        if tab % 100 == 0:
            print('did 100 runs')
            print(tab)
            print(len(games))

        for x, game in enumerate(games):
            moved = False
            output = nets[games.index(game)].activate((makeList(game.toString())))

            ind_arr = find_index(output)
            max_index = ind_arr[-1]
            nex_index = ind_arr[-2]
            third_index = ind_arr[-3]
            fourth_index = ind_arr[-4]

            initScore = game.score
            if max_index == 0:
                game.move_left()
            if max_index == 1:
                game.move_right()
            if max_index == 2:
                game.move_up()
            if max_index == 3:
                game.move_down()

            newScore = game.score
            # print('gene num is ')
            # print(x)
            # print(max_index)
            # print(game.direction)
            alive = game.checkGame()
            if game.popCount > 40:
            	alive = False
            if alive == False:
                nets.pop(games.index(game))
                ge.pop(games.index(game))
                games.pop(games.index(game))
                #print('popped one')
            else:
                ge[x].fitness += 1
                ge[x].fitness += 4*2**(-1*game.distToFood()/15)
                if game.d2f < game.d2fPrev:
                    ge[x].fitness += 3
                    if x == 0:
                        print("got closer")
                else:
                    ge[x].fitness -= 2
                if x == 0:

                    print(4*2**(-1*game.distToFood()/15))
                if newScore - initScore > 0:
                    ge[x].fitness += 100
            if tab % 100 == 0:
                print('did 100 runs')
                print(tab)
                print(len(games))
                print('gene num is ')
                print(x)
                print(max_index)
                print(game.direction)
                print(game.pos)
            # if x == 0:
            # 	print(game.toString())
            # 	print("---")
            # 	print("---")

def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    print('post config')
    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(eval_genomes)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))



if __name__ == '__main__':
    print('in start')
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforwardSnake.txt')
    run(config_path)