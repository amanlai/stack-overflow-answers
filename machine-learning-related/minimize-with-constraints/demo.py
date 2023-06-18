import numpy as np
from scipy.optimize import minimize, LinearConstraint

def matr_t(t):
    return np.array([[t[0], 0],[t[2]+complex(0,1)*t[3], t[1]]]

def target(t):
    arr2 = matr_t(t)
    ret = 0
    for i, v1 in enumerate(arr):
          for j, v2 in enumerate(v1):
               ret += abs(arr[i][j]-arr2[i][j])**2
    return ret

arr = np.array([[0.8, 0.2],[-0.1, 0.14]])
linear_constraint = LinearConstraint([[1, 1, 0, 0]], [1], [1])
result = minimize(target, x0=[0.5, 0.5, 0, 0], constraints=[linear_constraint])

x_opt = result.x            # array([ 0.83,  0.17, -0.1 , 0.])
minimum = result.fun        # 0.0418



