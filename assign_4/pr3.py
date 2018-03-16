import math
import time
import numpy as np

from pr2 import generate_random_graph

import matplotlib.pyplot as plt


def simulated_anneling(gr, start_size=None, start_temp=None, max_iteration=10000):
    assert len(gr) > 2
    def need_update(weight, best_weight, temp):
        p = min(math.exp((weight - best_weight) / temp), 1)
        return np.random.binomial(1, p, size=1)[0]

    if start_size is None:
        start_size = len(gr)
    if start_temp is None:
        start_temp = 10
    best_path = np.array(list(range(len(gr))))
    np.random.shuffle(best_path)
    best_path = best_path[:start_size]
    best_weight = np.sum(gr[best_path[:-1], best_path[1:]])
    best_unused_nodes = list(best_path[start_size:])
    temp = start_temp

    actions = np.random.randint(0, 3, size=max_iteration)
    for action in actions:
        path = best_path.copy()
        weight = -math.inf
        unused_nodes = best_unused_nodes.copy()
        # print(path, best_weight)
        if action == 0 and len(path) > 2:
            new_weight_start = best_weight - graph[path[0], path[1]]
            new_weight_end = best_weight - graph[path[-2], path[-1]]
            new_weight = best_weight - \
                (gr[path[:-2], path[1:-1]] + gr[path[1:-1], path[2:]]) + \
                gr[path[:-2], path[2:]]
            i = np.argmax(new_weight)

            if new_weight_start > max(new_weight[i], new_weight_end):
                weight = new_weight_start
                unused_nodes.append(path[0])
                path = np.delete(path, 0)
            elif new_weight_end > max(new_weight[i], new_weight_start):
                weight = new_weight_end
                unused_nodes.append(path[-1])
                path = np.delete(path, -1)
            else:
                weight = new_weight[i]
                unused_nodes.append(path[i + 1])
                path = np.delete(path, i + 1)

        elif action == 1 and len(unused_nodes) > 0:
            new_node_ind = np.random.randint(0, len(unused_nodes))
            new_node = unused_nodes[new_node_ind]
            new_weight = best_weight - gr[path[:-1], path[1:]] + \
                gr[path[:-1], new_node] + gr[new_node, path[1:]]
            new_weight_start = best_weight + gr[new_node, path[0]]
            new_weight_end = best_weight + gr[path[-1], new_node]
            # print("!", new_node, new_weight, new_weight_start, new_weight_end)
            i = np.argmax(new_weight)
            if new_weight_start > max(new_weight[i], new_weight_end):
                weight = new_weight_start
                path = np.insert(path, 0, new_node)
            elif new_weight_end > max(new_weight[i], new_weight_start):
                weight = new_weight_end
                path = np.insert(path, len(path), new_node)
            else:
                weight = new_weight[i]
                path = np.insert(path, i + 1, new_node)
            unused_nodes[new_node_ind], unused_nodes[-1] = \
                unused_nodes[-1], unused_nodes[new_node_ind]
            unused_nodes.pop()
        elif action == 2 and len(path) > 3:
            new_weight = best_weight - \
                gr[path[:-3], path[1:-2]] - \
                gr[path[2:-1], path[3:]] + \
                gr[path[:-3], path[2:-1]] + \
                gr[path[1:-2], path[3:]]
            i = np.argmax(new_weight)
            path[i+1], path[i+2] = path[i+2], path[i+1]
            weight = new_weight[i]
        if weight == -math.inf:
            continue
        if weight > best_weight or need_update(weight, best_weight, temp):
            best_path = path
            best_weight = weight
            best_unused_nodes = unused_nodes
        temp *= 1.01
        # print("unused", unused_nodes, "action", action)
    return best_path, best_weight

# np.random.seed(2)
times = []
best_weights = []
N = 100 * np.arange(1, 100)
for n in N:
    graph = generate_random_graph(n=n)
    start = time.time()
    best_path, best_weight = simulated_anneling(graph)
    end = time.time()
    times.append(end - start)
    best_weights.append(best_weight)
    print(n, times[-1], best_weights[-1])

plt.plot(N, times)
plt.title("Time")
plt.xlabel("n")
plt.ylabel("time")
plt.savefig("pr3_time.pdf")
plt.close()

plt.plot(N, best_weights)
plt.title("Path weights")
plt.xlabel("n")
plt.ylabel("weights")
plt.savefig("pr3_weights.pdf")
plt.close()
