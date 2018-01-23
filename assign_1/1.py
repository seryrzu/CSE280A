from scipy.optimize import minimize
import numpy as np

def MostLikelyFrequences(freqs, n, k):
    def opt_fun(p):
        res = 0
        for i in range(len(freqs)):
            for j in range(len(freqs[i])):
                res += (2 * p[i] * p[i+j+1] - freqs[i][j] / n)**2
        return res

    p_0 = np.ones(k) / k
    return minimize(opt_fun, p_0, bounds=[(0, 1)]*k,
                    constraints={'type':'eq', 'fun': lambda p: sum(p) - 1})


freqs = [[18, 21, 12], [7, 3], [5]]
n, k = 100, 4
res = MostLikelyFrequences(freqs, n, k)
print(res.x)
print(sum(res.x))
print(MostLikelyFrequences(freqs, n, k))
