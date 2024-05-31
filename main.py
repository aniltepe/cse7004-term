import sys
import os
from solve_mwisp_gurobi import solve as solve_grb
from solve_mwisp_greedy import solve as solve_gdy
from solve_mwisp_genetic import solve as solve_gen

GRAPHS_DIR = 'graphs'
CREATE_SCRIPT = 'create_graph_file.py'

for n in [50, 100, 150, 200]:
    for d in [0.1, 0.3, 0.5, 0.7, 0.9]:
        sys.argv = [CREATE_SCRIPT, f'{n}', f'{d}', GRAPHS_DIR]  # python create_graph_file.py 50 0.1 graphs
        exec(open(CREATE_SCRIPT).read())

results = []
for file_name in os.listdir(GRAPHS_DIR):
    # print(file_name)
    file_path = f'./{GRAPHS_DIR}/{file_name}'
    file_results = []
    file_results.append(solve_grb(file_path))
    file_results.append(solve_gdy(file_path))
    for no_of_gens in [50, 100]:
        for pop_size in [50, 100]:
            file_results.append(solve_gen(file_path, no_of_gens, pop_size))

