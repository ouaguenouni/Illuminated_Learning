
from .Archive import *
from deap import algorithms
from deap import base
from deap import benchmarks
from deap import creator
from deap import tools
from .grid_management import *


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
    
    def save_stats(self,resdir):
        self.grid.dump(resdir)
        self.grid.get_stats(resdir, 1000)


class Selector_FITNS(Selector):

    def __init__(self, **kwargs):
        super().__init__(Novelty_Archive_random, **kwargs)


    def compute_objectifs(self, population):
        self.archive.apply_novelty_estimation(population)
        for i in population:
            i.fitness.values = (i.fit, i.novelty)



class Selector_FIT(Selector):

    def __init__(self, **kwargs):
        super().__init__(Novelty_Archive_random, **kwargs)


    def compute_objectifs(self, population):
        self.archive.apply_novelty_estimation(population)
        for i in population:
            i.fitness.values = (i.fit, )

class Selector_NS(Selector):

    def __init__(self, **kwargs):
        super().__init__(Novelty_Archive_random, **kwargs)


    def compute_objectifs(self, population):
        self.archive.apply_novelty_estimation(population)
        for i in population:
            i.fitness.values = (i.novelty, )


class Selector_SHINE(Selector):

    def __init__(self, **kwargs):
        self.archive = Shine_Archive(600,600,alpha=kwargs["alpha"],beta=kwargs["beta"])
        self.grid = Grid(kwargs["grid_min_v"],kwargs["grid_max_v"],kwargs["dim_grid"])

    def update_with_offspring(self, offspring):
        for ind in offspring:
            self.grid.add(ind)
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


class Selector_SHINE_DISC(Selector): #M.O
    
    def __init__(self, **kwargs):
        self.archive = Shine_Archive(600,600,alpha=kwargs["alpha"],beta=kwargs["beta"])
        self.grid = Grid(kwargs["grid_min_v"],kwargs["grid_max_v"],kwargs["dim_grid"])

    def update_with_offspring(self, offspring):
        for ind in offspring:
            self.grid.add(ind)
        self.archive.update_offspring(offspring)
        pass

    def compute_objectifs(self, population):
        for i in population:
            n = self.archive.search(Behaviour_Descriptor(i))
            if(n!= None and len(n.val) > 0):
                i.fitness.values = (n.level  ,len(n.val) )
            else:
                i.fitness.values = (np.inf,self.archive.beta,len(n.val))
        pass

    def select(self, pq, mu):
        return tools.selNSGA2(pq,mu)


class Selector_SHINE_COL(Selector):
    
    def __init__(self, **kwargs):
        self.archive = Shine_Archive_COL(600,600,alpha=kwargs["alpha"],beta=kwargs["beta"])
        self.grid = Grid(kwargs["grid_min_v"],kwargs["grid_max_v"],kwargs["dim_grid"])

    def update_with_offspring(self, offspring):
        for ind in offspring:
            self.grid.add(ind)
        self.archive.update_offspring(offspring)
        pass

    def compute_objectifs(self, population):
        for i in population:
            n = self.archive.search(Behaviour_Descriptor(i))
            if(n!= None and len(n.val) > 0):
                i.fitness.values = (n.level  ,len(n.val) )
            else:
                i.fitness.values = (np.inf,self.archive.beta,len(n.val))
        pass

    def select(self, pq, mu):
        return tools.selNSGA2(pq,mu)




class Selector_SHINE_PARETO(Selector):
    
    def __init__(self, **kwargs):
        self.archive = Shine_Archive_PARETO(600,600,alpha=kwargs["alpha"],beta=kwargs["beta"])
        self.grid = Grid(kwargs["grid_min_v"],kwargs["grid_max_v"],kwargs["dim_grid"])

    def update_with_offspring(self, offspring):
        for ind in offspring:
            self.grid.add(ind)
        self.archive.update_offspring(offspring)
        pass

    def compute_objectifs(self, population):
        for i in population:
            n = self.archive.search(Behaviour_Descriptor(i))
            if(n!= None and len(n.val) > 0):
                i.fitness.values = (n.level  ,len(n.val) )
            else:
                i.fitness.values = (np.inf,self.archive.beta,len(n.val))
        pass

    def select(self, pq, mu):
        return tools.selNSGA2(pq,mu)










class Selector_MAPElites_FIT(Selector):
    def __init__(self, **kwargs):
        self.grid = Grid(kwargs["grid_min_v"],kwargs["grid_max_v"],kwargs["dim_grid"], comparator=self.compare)

    def update_with_offspring(self, offspring):
        for i in offspring:
            self.grid.add(i)
        pass

    def compute_objectifs(self, population):
        for i in population:
            i.fitness.values = (i.fit, )
        pass

    def compare(self,ind1,ind2):
        return ind1.fit > ind2.fit

    def select(self, pq, mu):
        self.update_with_offspring(pq)
        inds = sorted(self.grid.content.values(), key = lambda x:(x.fitness.values[0]), reverse=True)[:mu] #Descendant
        return inds


class Selector_MAPElites_COL(Selector):
    def __init__(self, **kwargs):
        self.grid = Grid(kwargs["grid_min_v"],kwargs["grid_max_v"],kwargs["dim_grid"])

    def update_with_offspring(self, offspring):
        for i in offspring:
            self.grid.add(i)
        pass

    def compute_objectifs(self, population):
        for i in population:
            i.fitness.values = (i.fit, )
        pass


    def select(self, pq, mu):
        self.update_with_offspring(pq)
        inds = sorted(self.grid.content.values(), key = lambda x:(x.fitness.values[0]), reverse=True)[:mu] #Ascendant
        return inds



class Selector_MAPElites_POL(Selector):
    def __init__(self, **kwargs):
        self.grid = Grid_POL(kwargs["grid_min_v"],kwargs["grid_max_v"],kwargs["dim_grid"])

    def update_with_offspring(self, offspring):
        for i in offspring:
            self.grid.add(i)
        pass

    def compute_objectifs(self, population):
        for i in population:
            i.fitness.values = (i.fit, )
        pass


    def select(self, pq, mu):
        self.update_with_offspring(pq)
        inds = sorted(self.grid.content.values(), key = lambda x:(x.fitness.values[0]), reverse=True)[:mu+1] #Descendant
        #print("Selected individuals : ",[(self.grid.get_grid_coord(ind),ind.fit) for ind in inds])
        return inds

