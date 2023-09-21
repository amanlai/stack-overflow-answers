from scipy.optimize import minimize
import numpy as np

def obj_func(variables, coefs):
    gap = coefs[:, 0] - (variables * coefs[:, 1:]).sum(axis=1)
    return (gap**2).sum()

initial = [0, 0]
coefs = np.array([[0.4, 1, 0], [2, 1, 1], [5, 1, 2], [7, 1, 3], [8, 1, 4], [11, 1, 5], [13, 1, 6], [14, 1, 7], [16, 1, 8], [19, 1, 9]])
result = minimize(obj_func, initial, args=coefs)

minimizers = result.x         # [0.50181826, 2.00848483]
minimum = result.fun          # 2.23806060606064



# sanity check

from statsmodels.api import OLS
ols_coefs = OLS(coefs[:, 0], coefs[:, 1:]).fit().params
assert np.allclose(ols_coefs, minimizers)