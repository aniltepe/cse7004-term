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
    
    # initialize objective value and selected nodes
    obj_val = 0
    added_idxs = []
    w = weights
    
    # start time of optimization
    start = datetime.datetime.now()

    while True:
        # find the max value and its index
        curr_max = max(w)
        max_idx = w.index(curr_max)

        # check whether if max node has neighbor in independent set
        neighbor = [(i, max_idx) in edges or (max_idx, i) in edges for i in added_idxs]

        # if max node doesn't have any neigbor, add to the independent set and add its value to the objective value
        if not any(neighbor):
            obj_val += curr_max
            added_idxs.append(max_idx)

        # set max value to the -1 to not appear as max value again
        w[max_idx] = -1.0

        # if all nodes traversed and independent set doesn't expand anymore
        if all([w_ == -1.0 for w_ in w]):
            break
    
    added_idxs.sort()

    # end time of optimization
    end = datetime.datetime.now()
    diff = end - start

    return {
        'selected_nodes': added_idxs,
        'objective_value': obj_val,
        'elapsed_time': diff.total_seconds()
    }
