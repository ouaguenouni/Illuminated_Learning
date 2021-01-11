from Evolution.Algorithms import *
from Genomes.Simple_Neuron import *
from Evolution.Selector import *
import random

from deap import algorithms
from deap import base
from deap import benchmarks
from deap import creator
from deap import tools

creator.create("MyFitness", base.Fitness, weights=(1.0,))
creator.create("Individual", array.array, typecode="d", fitness=creator.MyFitness, strategy=None)
creator.create("Strategy", array.array, typecode="d")


kw={
    'gym_name': 'FastsimSimpleNavigation-v0',
    'env_params': {"still_limit": 10, 'reward_kind': "continuous"},

    'nb_input': 5, # number of NN inputs
    'nb_output': 2, # number of NN outputs
    'nb_layers': 2, # number of layers
    'nb_neurons_per_layer': 10, # number of neurons per layer
    'max_action': 2,
    'episode_nb_step': 1000, 
    'episode_reward_kind': 'final', 
    'episode_bd': 'robot_pos', 
    'episode_bd_slice': (0,2,None), 
    'episode_bd_kind': 'final', 
    'episode_log': {'collision': 'cumul', 
                    'dist_obj': 'final', 
                    'exit_reached': 'final', 
                    'robot_pos': 'final'},
    'dim_grid': [100, 100],
    'grid_min_v': [0,0],
    'grid_max_v': [600,600],
    'goal': [60,60],
    'watch_max': 'dist_obj',
    'min_value': -30, # min genotype value
    'max_value': 30, # max genotype value
    'min_strategy': 0.5, # min value for the mutation
    'max_strategy': 3, # max value for the mutation
    'nb_gen': 25, # number of generations
    'mu': 100, # population size
    'lambda': 200, # number of individuals generated
    'nov_k': 15, # k parameter of novelty search
    'nov_add_strategy': "random", # archive addition strategy (either 'random' or 'novel')
    'nov_lambda': 6, # number of individuals added to the archive
    'selection' : "blablabla"
}


def test_SHINE():
    resdir="res/RUN_SHINE_"+"_"+datetime.datetime.now().strftime("%Y_%m_%d_%H:%M:%S")
    os.mkdir(resdir)
    pop,select = Simple_NSGA(Regression, Selector_SHINE, ngen=200, resdir=resdir, weights=(1.0,), **kw)

def test_NS():
    resdir="res/RUN_SHINE_"+"_"+datetime.datetime.now().strftime("%Y_%m_%d_%H:%M:%S")
    os.mkdir(resdir)
    pop,select = Simple_NSGA(Regression, Selector_SHINE, ngen=200, resdir=resdir, weights=(1.0,), **kw)

def test_FIT():
    resdir="res/RUN_SHINE_"+"_"+datetime.datetime.now().strftime("%Y_%m_%d_%H:%M:%S")
    os.mkdir(resdir)
    pop,select = Simple_NSGA(Regression, Selector_SHINE, ngen=200, resdir=resdir, weights=(1.0,), **kw)


if (__name__ == "__main__"):
    resdir="res/RUN_SHINE_"+"_"+datetime.datetime.now().strftime("%Y_%m_%d_%H:%M:%S")
    os.mkdir(resdir)
    pop,select = Simple_NSGA(Regression, Selector_SHINE, ngen=200, resdir=resdir, weights=(1.0,), **kw)
