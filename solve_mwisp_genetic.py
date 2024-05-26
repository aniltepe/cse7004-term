import datetime
import random

weights, edges = [], []

def _validation(individual):
    for i in range(len(individual)):
        if individual[i] == 0.0:
            continue
        for j in range(i + 1, len(individual)):
            if ((i, j) in edges or (j, i) in edges) and individual[j] == 1.0:
                return False
    return True

def _repair(individual):
    for i in range(len(individual)):
        if individual[i] == 0.0:
            continue
        for j in range(i + 1, len(individual)):
            if ((i, j) in edges or (j, i) in edges) and individual[j] == 1.0:
                individual[j] = 0.0
    return individual

def _repair_population(population):
    repaired = []
    for individual in population:
        valid = _validation(individual)
        if valid:
            repaired.append(individual)
        else:
            repaired.append(_repair(individual))
    return repaired

def _fitness(individual):
    w = [weights[i] for i in range(len(individual)) if individual[i] == 1.0]
    return sum(w)

def _tournament(population, fitness_values):
    mating_pool = []
    k = 2
    while len(mating_pool) < len(population):
        indivs = random.sample(range(len(population)), k)
        max_indiv_weight = max([fitness_values[indiv] for indiv in indivs])
        max_fit_indiv = [indiv for indiv in indivs if fitness_values[indiv] == max_indiv_weight][0]
        mating_pool.append(population[max_fit_indiv])
    return mating_pool

def _crossover(population, probability, no_of_genes):
    offsprings = []
    for i in range(0, len(population), 2):
        parent1 = population[i]
        parent2 = population[i + 1]
        if random.random() < probability:
            offspring1 = []
            offspring2 = []
            for n in range(no_of_genes):
                if random.random() < 0.5:
                    offspring1.append(parent1[n])
                    offspring2.append(parent2[n])
                else:
                    offspring1.append(parent2[n])
                    offspring2.append(parent1[n])
            offsprings.append(offspring1)
            offsprings.append(offspring2)
        else:
            offsprings.append(parent1)
            offsprings.append(parent2)
    return offsprings

def _mutation(population, probability, no_of_genes):
    mutated = []
    k = 1
    for indiv in population:
        if random.random() < probability:
            mutated_indiv = indiv
            gene = random.sample(range(no_of_genes), k)
            for g in gene:
                mutated_indiv[g] = 1.0 - mutated_indiv[g]
            mutated.append(mutated_indiv)
        else:
            mutated.append(indiv)
    return mutated

def solve(graph_file, no_of_generations, population_size, cross_probability=0.5):
    global weights, edges
    # parse graph info from file
    f = open(graph_file, 'r')
    lines = f.read().split('\n')
    no_of_nodes = int(lines[0])
    no_of_edges = int(lines[1])

    # parse weights as a list of floats
    weights = [float(lines[i].split(' ')[1]) for i in range(2, no_of_nodes + 2)]
    # parse edge indices as a list of tuple
    edges = [(int(lines[i].split(' ')[0]), int(lines[i].split(' ')[1])) for i in range(no_of_nodes + 2, no_of_nodes + no_of_edges + 2)]
    
    # start time of optimization
    start = datetime.datetime.now()

    # initialize genetic algorithm parameters
    mutation_probability = 1 / no_of_nodes
    initial_population = [[float(random.random() > 0.5) for n in range(no_of_nodes)] for i in range(population_size)]
    best_slns = []
    best_sln = (0, 0)
    
    next_pop = _repair_population(initial_population)
    K = 20

    for G in range(no_of_generations):
        curr_pop = next_pop
        fitness_values = [_fitness(indiv) for indiv in curr_pop]
        max_fitness = max(fitness_values)
        best_slns.append([indiv for indiv in curr_pop if _fitness(indiv) == max_fitness][0])
        if G > best_sln[1] + K and max([_fitness(sln) for sln in best_slns[-K:]]) <= best_sln[0]:
            print("best solution has not improved in the last K=20 generations since Gen.", best_sln[1])
            break
        if max_fitness > best_sln[0]:
            best_sln = (max_fitness, G)
        mating_pool = _tournament(curr_pop, fitness_values)
        offsprings = _crossover(mating_pool, cross_probability, no_of_nodes)
        mutated = _mutation(offsprings, mutation_probability, no_of_nodes)
        next_pop = _repair_population(mutated)
    
    mwis = [i for i, n in enumerate(best_slns[best_sln[1]]) if n == 1.0]
    
    # end time of optimization
    end = datetime.datetime.now()
    diff = end - start

    return {
        'selected_nodes': mwis,
        'objective_value': best_sln[0],
        'elapsed_time': diff.total_seconds()
    }

