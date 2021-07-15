
import random
import os
import time
import neat
import visualize
import pickle
from board import Board
import numpy as np
import math

from neat.graphs import feed_forward_layers
from neat.graphs import required_for_output






gen = 0


def find_index(array):
    s = np.array(array)
    sort_index = np.argsort(s)
    return sort_index

def pick_two(array):
    max_value = max(array)
    max_index = array.index(max_value)
    cpy_arry = [array[i] for i in range(len(array))]
    cpy_arry.sort()
    nex_value = cpy_arry[-2]
    thrd_value = cpy_arry[-3]
    fourth_value = cpy_arry[-4]
    nex_index = array.index(nex_value)
    third_index = array.index(thrd_value)
    fourth_index = array.index(fourth_value)
    return max_index, nex_index, third_index, fourth_index

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

    tab = 0

    norml = 64


    while run and len(boards) > 0:
        #boards[0].toString()
        tab += 1
        # if tab % 100 == 0:
        #     print('did 100 runs')
        #     print(tab)
        #     print(len(boards))

        for x, board in enumerate(boards):
            
            initZero = board.numZeros()
            init128 = board.numNum(128)
            init256 = board.numNum(256)
            init512 = board.numNum(512)
            init1024 = board.numNum(1024)
            init2048 = board.numNum(2048)
            #fitness = 0
            moved = False
            output = nets[boards.index(board)].activate((board.matrix[0][0]/norml,
                                                            board.matrix[0][1]/norml,
                                                            board.matrix[0][2]/norml,
                                                            board.matrix[0][3]/norml,
                                                            board.matrix[1][0]/norml,
                                                            board.matrix[1][1]/norml,
                                                            board.matrix[1][2]/norml,
                                                            board.matrix[1][3]/norml,
                                                            board.matrix[2][0]/norml,
                                                            board.matrix[2][1]/norml,
                                                            board.matrix[2][2]/norml,
                                                            board.matrix[2][3]/norml,
                                                            board.matrix[3][0]/norml,
                                                            board.matrix[3][1]/norml,
                                                            board.matrix[3][2]/norml,
                                                            board.matrix[3][3]/norml
                                                            ))
            #print('output is')
            #print(output)
            #max_index, nex_index, third_index, fourth_index = pick_two(output)
            #print(max_index, nex_index,third_index, fourth_index)

            ind_arr = find_index(output)
            #print(ind_arr)
            max_index = ind_arr[-1]
            nex_index = ind_arr[-2]
            third_index = ind_arr[-3]
            fourth_index = ind_arr[-4]

            if max_index == 0:
                move = board.left()
            if max_index == 1:
                move = board.right()
            if max_index == 2:
                move = board.up()
            if max_index == 3:
                move = board.down()
            if move:
                moved = True
            else:
                #print('in second')
                #print(nex_index)
                if nex_index == 0:
                    move = board.left()
                if nex_index == 1:
                    move = board.right()
                if nex_index == 2:
                    move = board.up()
                if nex_index == 3:
                    move = board.down()
                if move:
                    #print('found move')
                    moved = True
                else:
                    #print('im in third')
                    #print(nex_index)
                    if third_index == 0:
                        move = board.left()
                    if third_index == 1:
                        move = board.right()
                    if third_index == 2:
                        move = board.up()
                    if third_index == 3:
                        move = board.down()
                    if move:
                        #print('found move')
                        moved = True
                    else:
                        #print('im in fourth')
                        #print(fourth_index)
                        if fourth_index == 0:
                            move = board.left()
                        if fourth_index == 1:
                            move = board.right()
                        if fourth_index == 2:
                            move = board.up()
                        if fourth_index == 3:
                            move = board.down()
                        if move:
                            #print('found move')
                            moved = True
                        else:
                            #print(board.matrix)
                            #print('this broke')
                            nets.pop(boards.index(board))
                            ge.pop(boards.index(board))
                            boards.pop(boards.index(board))
        #boards[0].toString()
            #print(board.toString())
        #print('tab is :')
        #print(tab)
            newZero = board.numZeros()
            if moved:
                # print('the added value is ')
                # print(2**(initZero - newZero))
                # print(8/(17-newZero))
                # print(math.tanh((2 - board.symCount()))*2)
                # print(board.symCount())
                ge[x].fitness += 1
                ge[x].fitness += 8*2**(initZero - newZero)
                ge[x].fitness += 10*(8/(17-newZero) - .5)
                ge[x].fitness += math.tanh((12 - board.symCount()))*2
                #print (ge[x].fitness)

                if board.numNum(128) - init128 > 0:
                   ge[x].fitness += 10
                if board.numNum(256) - init256 > 0:
                   ge[x].fitness += 50
                if board.numNum(512) - init512 > 0:
                   ge[x].fitness += 100
                if board.numNum(1024) - init1024 > 0:
                   ge[x].fitness += 7000
                if board.numNum(2048) - init2048 > 0:
                   ge[x].fitness += 100000
                # print('x  and fitness are ')
                # print(x)
                # print (ge[x].fitness)

        if x ==0:
            # print('the board fitness is ')
            # print (ge[x].fitness)
            a = 3

        for board in boards:
            if board.game_state() == 0:

                #print('something broke')
                nets.pop(boards.index(board))
                ge.pop(boards.index(board))
                boards.pop(boards.index(board))
                if len(boards) == 0:
                    board.toString()

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
    winner = p.run(eval_genomes,3000)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))
    node_names = {0: 'left', 1: 'right', 2: 'up', 3: 'down', -1: '00', -2: '01', -3: '02'
        , -4: '03', -5: '10', -6: '11'
        , -7: '12', -8: '13', -9: '20'
        , -10: '21', -11: '22', -12: '23'
        , -13: '30', -14: '31', -15: '32'
        , -16: '33'}
    visualize.draw_net(config, winner, True, '2048MultLayer', node_names=node_names)
    print(repr(winner))
    print("the fitness is ")
    print(winner.fitness)
    visualize.plot_stats(stats, "Population's average and best fitness", ylog=False,
                         view=True)
    visualize.plot_species(stats, view=True)

    connections = [cg.key for cg in winner.connections.values() if cg.enabled]
    print("printing connections")
    print(connections)

    layers = feed_forward_layers(config.genome_config.input_keys, config.genome_config.output_keys, connections)
    print("printing layers")
    print(layers)

    req = required_for_output(config.genome_config.input_keys, config.genome_config.output_keys, connections)
    print("printing required")
    print(req)


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)