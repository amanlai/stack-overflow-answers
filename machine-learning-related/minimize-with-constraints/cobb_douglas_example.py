from scipy.optimize import minimize, LinearConstraint

def obj_func(variables, hyperparams):
    x, y = variables
    alpha, beta = hyperparams
    return - x**alpha * y**beta

B, px, py, alphas = 30, 2, 5, [1/3, 2/3]
linear_constraint = LinearConstraint([[px, py], [1, 0], [0, 1]], [-np.inf, 0, 0], [B, np.inf, np.inf])
result = minimize(obj_func, x0=[1, 1], args=alphas, constraints=[linear_constraint])

x_opt, y_opt = result.x     # 4.9996, 4.000
optimum = result.fun        # 4.3088