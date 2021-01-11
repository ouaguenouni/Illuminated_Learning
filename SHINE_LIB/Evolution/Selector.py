
from .Archive import *
from deap import algorithms
from deap import base
from deap import benchmarks
from deap import creator
from deap import tools


class Selector():
    def __init__(self, archive_class, **kwargs):
        self.archive = archive_class(k=kwargs["nov_k"], lambda_ = kwargs["nov_lambda"])
        self.grid = Grid(kwargs["grid_min_v"],kwargs["grid_max_v"],kwargs["dim_grid"])

    def update_with_offspring(self, offspring):
        for ind in offspring:
            self.grid.add(ind)
        self.archive.update_offspring(offspring)
        pass

    def compute_objectifs(self, population):
        pass

    def select(self, pq, mu):
        return tools.selNSGA2(pq,mu)


class Selector_FITNS(Selector):

    def __init__(self, **kwargs):
        super().__init__(Novelty_Archive_random, **kwargs)


    def compute_objectifs(self, population):
        self.archive.apply_novelty_estimation(population)
        for i in population:
            i.fitness.values = (i.fit, i.novelty)


class Selector_NS(Selector):

    def __init__(self, **kwargs):
        super().__init__(Novelty_Archive_random, **kwargs)


    def compute_objectifs(self, population):
        self.archive.apply_novelty_estimation(population)
        for i in population:
            i.fitness.values = (i.novelty, )


class Selector_SHINE(Selector):
    def __init__(self, **kwargs):
        self.archive = Shine_Archive(600,600)

    def update_with_offspring(self, offspring):
        self.archive.update_offspring(offspring)
        pass

    def compute_objectifs(self, population):
        for i in population:
            n = self.archive.search(Behaviour_Descriptor(i))
            if(len(n.val) > 0):
                i.fitness.values = (self.archive.beta / (self.archive.beta*n.level + len(n.val) ),)
            else:
                i.fitness.values = (-np.inf,)
        pass

    def select(self, pq, mu):
        return tools.selNSGA2(pq,mu)