It's a post that was first posted as an answer to the following Stack Overflow question and can be found at https://stackoverflow.com/a/75709136/19123103

## How to use `minimize` from `scipy` with constraints

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

[![constraint][1]][1]

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

  [1]: https://i.stack.imgur.com/3farR.png