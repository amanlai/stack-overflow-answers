## How to use `minimize` from `scipy` with constraints

<sup> It's a post that was first posted as an answer to a Stack Overflow question that can be found [here](https://stackoverflow.com/a/75709136/19123103). </sup>

> Let's suppose I have a matrix
> ```python
> arr = array([[0.8, 0.2],[-0.1, 0.14]])
> ```
> with a target function
> ```python
> def matr_t(t):
>     return array([[t[0], 0],[t[2]+complex(0,1)*t[3], t[1]]]
> 
> def target(t):
>     arr2 = matr_t(t)
>     ret = 0
>     for i, v1 in enumerate(arr):
>           for j, v2 in enumerate(v1):
>                ret += abs(arr[i][j]-arr2[i][j])**2
>     return ret
> ```
> now I want to minimize this target function under the assumption that the `t[i]` are real numbers, and something like `t[0]+t[1]=1`.


Instead of writing a custom constraint function, you can construct a `scipy.optimize.LinearConstraint` object and pass it as the constraint. Its construction asks for upper and lower bounds; also the vector of independent variables has to have the same length as the variable length passed to the objective function, so the constraint such as `t[0] + t[1] = 1` should be reformulated as the following (because `t` is length 4 as can be seen from its manipulation in `matr_t()`):

[![constraint][0]][0]

Also `minimize` optimizes over the real space, so the restriction of `t[i]` being real is already embedded into the algorithm. Then the complete code becomes:
```python
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
```

--- 

For a more involved example, let's use a common problem in economics, [Cobb-Douglas utility maximization][1] as an illustrative example. This is actually a constrained maximization problem but because `minimize` is a minimization function, it has to be coerced into a minimization problem (just negate the objective function). Also in order to pass the constraints as a `scipy.optimize.LinearConstraint` object, we have to write them to have lower and upper bounds. So the optimization problem is as follows:

[![problem][2]][2]

In this function, there are two variables `x` and `y`; the rest are all hyperparameters that have to be externally supplied (alpha, beta, `px`, `py` and `B`). Among them only alpha and beta are parameters of the objective function, so they must be passed to it through `args=` argument of `minimize` (`alphas` in the example below).

The optimization problem solves for `x` and `y` values where the objective function attains its minimum value given the constraint. They must be passed as a single object (`variables` in the function below) to the objective function. As mentioned before, we must pass an educated guess for these variables (`x` and `y` of the objective function) in order for the algorithm to converge.

```python
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
```
`result.x` are the minimizers and `result.fun` is the local minimum.

<sup>Cobb-Douglas has a closed form solution where for the example input, the correct solution is `(x_opt, y_opt) = (5, 4)`. The result of `minimize` is not quite equal to that but since `minimize` is an iterative algorithm, this is as close as it got before it stopped.</sup>


  [0]: https://i.stack.imgur.com/3farR.png
  [1]: https://www.sfu.ca/~wainwrig/Econ201/6500/mrs-notes.pdf
  [2]: https://i.stack.imgur.com/dNJe7.png