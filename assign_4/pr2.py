import math
import numpy as np

def generate_random_graph(n):
    k = min(n, 2 * int(math.ceil(math.log2(n))))
    w = np.zeros((n, n))
    w[np.triu_indices_from(w)] = np.random.randint(-10, 4, size=n*(n-1)//2 + n)
    w[np.tril_indices_from(w, k=-1)] = -math.inf
    w = np.maximum(w, w.T)
    path = list(range(n))
    np.random.shuffle(path)
    path = np.array(path[:k])
    path_vals = np.random.randint(0, 2, size=k-1)
    path_vals[path_vals == 0] = 10
    path_vals[path_vals == 1] = -3
    w[path[:-1], path[1:]] = path_vals
    w[path[1:], path[:-1]] = w[path[:-1], path[1:]]
    return w


if __name__ == '__main__':
    np.savetxt('2_n3.txt', generate_random_graph(3), fmt='%d')
    np.savetxt('2_n5.txt', generate_random_graph(5), fmt='%d')
    np.savetxt('2_n10.txt', generate_random_graph(10), fmt='%d')
