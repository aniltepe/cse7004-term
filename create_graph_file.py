import os
import sys
import random

NO_OF_NODES = int(sys.argv[1])
DENSITY = float(sys.argv[2])
GRAPHS_DIR = sys.argv[3]

edges = []
lines = [f'{NO_OF_NODES}']

for u in range(NO_OF_NODES):
    for v in range(u + 1, NO_OF_NODES):
        if random.random() < DENSITY:
            edges.append((u, v))
    lines.append(f'{u} {'{:.2f}'.format(random.random())}')

lines.insert(1, f'{len(edges)}')
for e in edges:
    lines.append(f'{e[0]} {e[1]}')

if not os.path.exists(GRAPHS_DIR):
    os.makedirs(GRAPHS_DIR)
f = open(f'./{GRAPHS_DIR}/graph_{NO_OF_NODES}_{DENSITY}.txt', 'w')
f.write('\n'.join(lines))
f.close()