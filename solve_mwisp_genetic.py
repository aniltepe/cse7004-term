import datetime
import random

weights, edges = [], []

def _validation(individual):
    for i in range(len(individual)):
        if individual[i] == 0.0:
            continue  # if a node is not in the independent set, continue to the next one
        for j in range(i + 1, len(individual)):
            if ((i, j) in edges or (j, i) in edges) and individual[j] == 1.0:
                return False  # if two nodes in the independent set are neighbors, then it's an infeasible solution
    return True  # if all nodes in the independent set don't have adjacency with each other, then it's a feasible solution

def _repair(individual):
    for i in range(len(individual)):
        if individual[i] == 0.0:
            continue  # if a node is not in the independent set, continue to the next one
        for j in range(i + 1, len(individual)):
            if ((i, j) in edges or (j, i) in edges) and individual[j] == 1.0:
                individual[j] = 0.0  # if two nodes in the independent set are neighbors, remove the second one from independent set
    return individual  # return the new independent set which is new feasible solution

def _repair_population(population):
    repaired = []
    for individual in population:
        valid = _validation(individual)  # check whether the solution is feasible or not
        if valid:
            repaired.append(individual)  # if the solution is feasible, it should not be repaired.
        else:
            repaired.append(_repair(individual))  # if the solution is infeasible, it should be repaired
    return repaired  # return new population, which every individual is a feasible solution

def _fitness(individual):
    w = [weights[i] for i in range(len(individual)) if individual[i] == 1.0]
    return sum(w)  # return sum of the weights of the nodes in the independent set

def _tournament(population, fitness_values):
    mating_pool = []
    k = 2  # binary tournament selection, so k = 2
    while len(mating_pool) < len(population):  # continue until mating pool's population reached to the population size
        indivs = random.sample(range(len(population)), k)  # get two random individual from population
        max_indiv_weight = max([fitness_values[indiv] for indiv in indivs])
        max_fit_indiv = [indiv for indiv in indivs if fitness_values[indiv] == max_indiv_weight][0]
        mating_pool.append(population[max_fit_indiv])  # add the best individual among two random indiviuals, to the mating pool
    return mating_pool

def _crossover(population, probability, no_of_genes):
    offsprings = []
    for i in range(0, len(population), 2):  # get two parents from mating pool
        parent1 = population[i]
        parent2 = population[i + 1]
        if random.random() < probability:  # if dice is less than crossover probability
            offspring1 = []
            offspring2 = []
            for n in range(no_of_genes):
                if random.random() < 0.5:  # uniform crossover
                    offspring1.append(parent1[n])
                    offspring2.append(parent2[n])
                else:
                    offspring1.append(parent2[n])
                    offspring2.append(parent1[n])
            offsprings.append(offspring1)
            offsprings.append(offspring2)
        else:  # if dice is greater than or equal to crossover probability
            offsprings.append(parent1)  # add the parents as offsprings
            offsprings.append(parent2)
    return offsprings

def _mutation(population, probability, no_of_genes):
    mutated = []
    k = 1  # the number of mutated genes in a individual, which is the number of node in the independent set
    for indiv in population:
        if random.random() < probability:  # if dice is less than mutation probability
            mutated_indiv = indiv
            gene = random.sample(range(no_of_genes), k)  # select one gene
            for g in gene:
                mutated_indiv[g] = 1.0 - mutated_indiv[g]  # flip the bit
            mutated.append(mutated_indiv)
        else:
            mutated.append(indiv)  # if dice is greater than or equal to mutation probability, don't mutate
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
    next_pop = _repair_population(initial_population) # repair initial population and make all the solutions feasible 

    K = 20
    not_improved_desc = ""

    for G in range(no_of_generations):
        curr_pop = next_pop
        fitness_values = [_fitness(indiv) for indiv in curr_pop]

        # get the best solution of the generation
        # compare with the best solution in the all generations
        # if the best solution has not improved in the last K generations, break the loop
        max_fitness = max(fitness_values)
        best_slns.append([indiv for indiv in curr_pop if _fitness(indiv) == max_fitness][0])
        if G > best_sln[1] + K and max([_fitness(sln) for sln in best_slns[-K:]]) <= best_sln[0]:
            # print("best solution has not improved in the last K=20 generations since Gen.", best_sln[1])
            not_improved_desc = f"Best solution has not improved in the last K=20 generations since Gen.{best_sln[1]}"
            break
        if max_fitness > best_sln[0]:
            best_sln = (max_fitness, G)

        # genetic algorithm operations
        mating_pool = _tournament(curr_pop, fitness_values)
        offsprings = _crossover(mating_pool, cross_probability, no_of_nodes)
        mutated = _mutation(offsprings, mutation_probability, no_of_nodes)
        next_pop = _repair_population(mutated)
    
    # maximum-weighted independent set
    mwis = [i for i, n in enumerate(best_slns[best_sln[1]]) if n == 1.0]
    
    # end time of optimization
    end = datetime.datetime.now()
    diff = end - start

    return {
        'selected_nodes': mwis,
        'objective_value': best_sln[0],
        'elapsed_time': diff.total_seconds(),
        'description': not_improved_desc
    }

