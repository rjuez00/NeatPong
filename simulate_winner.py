from pong import Pong
import pickle, numpy as np, neat


def replay_genome(config_path = "config", genome_path="winner"):
    # Load requried NEAT config
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # Unpickle saved winner
    with open(genome_path, "rb") as f:
        genome = pickle.load(f)

    # Convert loaded genome into required data structure
    genomes = [(1, genome)]

    # Call game with only the loaded genome
    return neat.nn.FeedForwardNetwork.create(genome, config)





net = replay_genome()

pong = Pong(sizex = 40, sizey = 40, vel_paddle = 1, vel_ball_x = 1, vel_ball_y = 1, size_paddle = 4, save_last_movements = 4)

fitnesses = []
pong.init_game()

while pong.simulate_ball_position():
    pong.visual()
    input()
    direction = np.argmax(net.activate(pong.represent_base()))
    #direction = np.argmax(net.activate(pong.represent_direction()))
    #direction = np.argmax(net.activate(pong.represent_last_positions()))
    if direction == 0:
        pong.paddle_down()
    elif direction == 2:
        pong.paddle_up()