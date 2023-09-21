## How to use SciPy's `minimize` function with multiple variables

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/75600364/19123103).</sup>

`scipy.optimize.minimize` takes two mandatory arguments: the objective function and the initial guess of the variables of the objective function (so `len(initial)==len(variables)` has to be true). As it's an iterative algorithm, it requires an initial guess for the variables in order to converge. So the initial guess has to be an educated guess, otherwise the algorithm may not converge and/or the results would be incorrect.

Also, if the objective function uses any extra arguments (e.g. coefficients of the objective function), they cannot be passed as kwargs but has to be passed via the `args=` argument of `minimize` (which admits an array-like).

Since the OP doesn't have a multi-variable objective function, let's use a common problem: [least squares minimization][1].

The optimization problem solves for values where the objective function attains its minimum value. As [unutbu][3] explained, they must be passed as a single object (`variables` in the function below) to the objective function. As mentioned before, we must pass an educated guess for these variables in order for the algorithm to converge.

```python
def obj_func(variables, coefs):
    gap = coefs[:, 0] - (variables * coefs[:, 1:]).sum(axis=1)
    return (gap**2).sum()

initial = [0, 0]
coefs = np.array([[0.4, 1, 0], [2, 1, 1], [5, 1, 2], [7, 1, 3], [8, 1, 4], [11, 1, 5], [13, 1, 6], [14, 1, 7], [16, 1, 8], [19, 1, 9]])
result = minimize(obj_func, initial, args=coefs)

minimizers = result.x         # [0.50181826, 2.00848483]
minimum = result.fun          # 2.23806060606064
```

<sup> As least squares minimization is how OLS regression coefficients are calculated, you can verify that the above indeed computes it by the following:
```python
from statsmodels.api import OLS
ols_coefs = OLS(coefs[:, 0], coefs[:, 1:]).fit().params
np.allclose(ols_coefs, minimizers)                         # True
```

  [1]: https://en.wikipedia.org/wiki/Least_squares
  [3]: https://stackoverflow.com/a/13670414/19123103