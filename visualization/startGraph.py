from visualize import draw_net
import neat, pickle, sys

config_path = sys.argv[2]
winner_path = sys.argv[1]

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     config_path)

with open(winner_path, "rb") as f:
        genome = pickle.load(f)


def get_input_output_nn_names():
    names_dict = {}
    # Inputs
    names_dict[-1] = "Ball X"
    names_dict[-2] = "Ball Y"
    names_dict[-3] = "Paddle Y"
    
    
    names_dict[0] = "Paddle Down"
    names_dict[2] = "Paddle Up"
    names_dict[1] = "Do not move"
    return names_dict


draw_net(config, 
         genome, 
         view=True, 
         filename=None, 
         node_names=get_input_output_nn_names(), 
         show_disabled=True, 
         prune_unused=False,
         node_colors=None, fmt='svg')