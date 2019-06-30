from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import Statistics

import threading

A            = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
TOTAL        = len(A) 
result       = []

def eval_func(genome):
    score = 0.0
    step = 0

    for value in genome:

        if value == 0:
            score += 0.1
        elif value-step>=1:
            score += 0.5
        elif value-step<=2:
            score += 0.4

        step = value

    return score

def evolve():

    genome = G1DList.G1DList(TOTAL)
    genome.setParams(rangemin=0, rangemax=TOTAL-1)
    genome.evaluator.set(eval_func)
    ga = GSimpleGA.GSimpleGA(genome)

    ga.selector.set(Selectors.GRouletteWheel)
    ga.setMutationRate(0.6)
    ga.setGenerations(100)
    ga.terminationCriteria.set(GSimpleGA.ConvergenceCriteria)

    ga.evolve(freq_stats=20)

    '''
    pop = ga.getPopulation()
    bf = pop.bestFitness()
    print bf

    br = pop.bestRaw()
    print br

    for ind in pop:
        print ind.fitness

    '''

    best = ga.bestIndividual()
    print best

    pop = ga.getPopulation()
    print pop

    for c in best.genomeList:
        result.append(A[c])

    print result

if __name__ == "__main__":
    evolve()

    '''
    ticker = threading.Event()
    while not ticker.wait(5):
        evolve()
    '''
