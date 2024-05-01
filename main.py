import sys
import os
from solve_mwisp_gurobi import solve

GRAPHS_DIR = 'graphs'
CREATE_SCRIPT = 'create_graph_file.py'

for n in [50, 100, 150, 200]:
    for d in [0.1, 0.3, 0.5, 0.7, 0.9]:
        sys.argv = [CREATE_SCRIPT, f'{n}', f'{d}', GRAPHS_DIR]  # python create_graph_file.py 50 0.1 graphs
        exec(open(CREATE_SCRIPT).read())


for filename in os.listdir(GRAPHS_DIR):
    print(filename)

