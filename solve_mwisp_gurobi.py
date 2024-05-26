import gurobipy as gp
from gurobipy import GRB
import datetime

def solve(graph_file):
    # parse graph info from file
    f = open(graph_file, 'r')
    lines = f.read().split('\n')
    no_of_nodes = int(lines[0])
    no_of_edges = int(lines[1])

    # parse weights as a list of floats
    weights = [float(lines[i].split(' ')[1]) for i in range(2, no_of_nodes + 2)]
    # parse edge indices as a list of tuple
    edges = [(int(lines[i].split(' ')[0]), int(lines[i].split(' ')[1])) for i in range(no_of_nodes + 2, no_of_nodes + no_of_edges + 2)]

    # initialize model
    m = gp.Model("mip_mwisp")
    
    # set time limit to 30 mins
    m.setParam('TimeLimit', 30 * 60)

    # add decision variable for each node
    x = m.addVars(no_of_nodes, vtype=GRB.BINARY)

    # add constraint for each edge
    m.addConstrs(x[i] + x[j] <= 1 for i, j in edges)

    # set objective function, maximize sum of the weights
    m.setObjective(gp.quicksum(x[i] * weights[i] for i in range(no_of_nodes)), GRB.MAXIMIZE)

    # start time of optimization
    start = datetime.datetime.now()

    # solve
    m.optimize()

    # end time of optimization
    end = datetime.datetime.now()
    diff = end - start

    return {
        'selected_nodes': [i for i in range(no_of_nodes) if x[i].x > 0.5],
        'objective_value': m.objVal,
        'elapsed_time': diff.total_seconds()
    }
