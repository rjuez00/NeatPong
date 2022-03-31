import multiprocessing
import os
import pickle

import neat
import numpy as np
from snake import *


runs_per_net = 1
max_game_steps = 2000

# Use the NN network phenotype and the discrete actuator force function.
def eval_genome(genome, config):

    net = neat.nn.FeedForwardNetwork.create(genome, config)

    fitnesses = []
    for runs in range(runs_per_net):
        
        s = SnakeGame(training=True)
        observation = s.observation()

        steps = 0
        while not s.gameOver and steps < max_game_steps:

            action = np.argmax(net.activate(observation))
            if action == 0:
                s.move(s.snakeDir.rotLeft())
            elif action == 1 or action == None: # Keep going in the direction the snake is going
                s.move(s.snakeDir)
            elif action == 2:
                s.move(s.snakeDir.rotRight())
            
            observation = s.observation()
        
            steps += 1

        fitnesses.append(s.length() - 1)
        #fitnesses.append(s.fitness())

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

    print(winner)




if __name__ == '__main__':
    run()