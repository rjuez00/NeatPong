import multiprocessing
import os
import pickle

import neat
import numpy as np
from pong import Pong

runs_per_net = 1
max_game_steps = 2000

# Use the NN network phenotype and the discrete actuator force function.
def eval_genome(genome, config):
    pong = Pong(sizex = 40, sizey = 40, vel_paddle = 1, vel_ball_x = 1, vel_ball_y = 1, size_paddle = 4, save_last_movements = 4)
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    fitnesses = []
    for runs in range(runs_per_net):
        pong.init_game()
        
        while pong.simulate_ball_position():
            direction = np.argmax(net.activate(pong.represent_base()))
            #direction = np.argmax(net.activate(pong.represent_direction()))
            #direction = np.argmax(net.activate(pong.represent_last_positions()))
            if direction == 0:
                pong.paddle_down()
            elif direction == 2:
                pong.paddle_up()

        fitnesses.append(pong.frames_lasted)
    
    #return min(fitnesses)
    return np.mean(fitnesses)


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = eval_genome(genome, config)


def run():
    # Load the config file, which is assumed to live in
    # the same directory as this script.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    pop = neat.Population(config)
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.StdOutReporter(True))

    pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome)
    winner = pop.run(pe.evaluate, 300)

    # Save the winner.
    with open('winner', 'wb') as f:
        pickle.dump(winner, f)





if __name__ == '__main__':
    run()