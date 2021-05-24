import pygame
import random
import os
import time
import neat
import visualize
import pickle
from board import Board
import numpy as np
import math
pygame.font.init()  # init font

WIN_WIDTH = 600
WIN_HEIGHT = 800
FLOOR = 730
STAT_FONT = pygame.font.SysFont("comicsans", 50)
END_FONT = pygame.font.SysFont("comicsans", 70)
DRAW_LINES = False

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird")


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
        if tab % 100 == 0:
            print('did 100 runs')
            print(tab)
            print(len(boards))

        for x, board in enumerate(boards):
            
            initZero = board.numZeros()
            init128 = board.numNum(128)
            init256 = board.numNum(256)
            init512 = board.numNum(512)
            init1024 = board.numNum(1024)
            fitness = 0
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
            ge[x].fitness += 2**(initZero - newZero)
            ge[x].fitness += 8*(8/(17-newZero) - .5)
            ge[x].fitness += math.tanh((12 - board.symCount()))*2

            if board.numNum(128) - init128 > 0:
               ge[x].fitness += 10
            if board.numNum(256) - init256 > 0:
               ge[x].fitness += 50
            if board.numNum(512) - init512 > 0:
               ge[x].fitness += 100
            if board.numNum(1024) - init1024 > 0:
               ge[x].fitness += 100000
        if x ==1:
            print('the board fitness is ')
            print (ge[x].fitness)

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
    winner = p.run(eval_genomes)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward2.txt')
    run(config_path)