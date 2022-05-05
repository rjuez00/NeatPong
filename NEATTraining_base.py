import multiprocessing, os, pickle, neat, numpy as np, sys
from pong import Pong

runs_per_net = 4
max_game_steps = 50000

# Use the NN network phenotype and the discrete actuator force function.
def eval_genome(genome, config):
    pong = Pong(sizex = 40, sizey = 40, vel_paddle = 1, save_last_movements = 4)
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    fitnesses = []
    for init_vector in [[1,1],[1,-1],[-1,1],[-1,-1]]:
        pong.init_game(*init_vector)
        
        i = 0
        while pong.simulate_ball_position():
            direction = np.argmax(net.activate(pong.represent_base()))

            
            
            if direction == 0:
                pong.paddle_down()
            elif direction == 2:
                pong.paddle_up()
            
            i += 1
            if i > max_game_steps:
                break

        fitnesses.append(pong.frames_lasted)
    
    #return min(fitnesses)
    return np.mean(sorted(fitnesses)[:-2])



def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = eval_genome(genome, config)


def run():
    # Load the config file, which is assumed to live in
    # the same directory as this script.
    local_dir = os.path.dirname(__file__)
    

    config_path = os.path.join(local_dir, 'config_base')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    pop = neat.Population(config)
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.StdOutReporter(True))

    pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome)
    winner = pop.run(pe.evaluate, 100)

    # Save the winner.
    with open(f'winner_four_directions_test_base', 'wb') as f:
        pickle.dump(winner, f)





if __name__ == '__main__':
    run()