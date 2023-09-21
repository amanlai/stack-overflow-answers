## How to fit a curve to data using python

<sup> This post is based on my answers to Stack Overflow questions that can be found at 
[1](https://stackoverflow.com/a/75598551/19123103),
[2](https://stackoverflow.com/q/50371428/19123103). </sup>



`np.polyfit` fits a polynomial function to data (which is always a good starting point) but `scipy.optimize.curve_fit` is much more flexible because you can fit any function you want to the data ([Greg][1] also mentions this). 

For example, to fit a polynomial function of degree 3, initialize a polynomial function `poly3d` and pass it off to `curve_fit` to compute its coefficients using the training values, `x` and `y`. Once you have `coefs_poly3d` computed, you can plug in other values to generate fitted values and plot a general function "around" the original training values. The following code produces the very same plot in [jabaldonedo's post][2].

```python
def poly3d(x, a, b, c, d):
    return a + b*x + c*x**2 + d*x**3

# initial data to fit
x, y = np.array([(1, 1), (2, 4), (3, 1), (9, 3)]).T
# fit poly3d to x, y
coefs_poly3d, _ = curve_fit(poly3d, x, y)

# initialize some points
x_data = np.linspace(min(x), max(x), 50)
# transform x_data to y-axis values via poly3d
y_data = poly3d(x_data, *coefs_poly3d)
# plot the points
plt.plot(x, y, 'ro', x_data, y_data);
```

As mentioned before, `curve_fit` is more flexible in that you can fit any function. For example, looking at the data, it seems we can fit a sine function as well. Then simply initialize a sine function and pass it to `curve_fit` to compute `coefs_sine`. 

Note that since `curve_fit` is an iterative algorithm, choosing an appropriate initial guess for the parameters (`a`, `b`, `c`, `d`) is sometimes crucial for the algorithm to converge. In the example below, it is initialized by `p0=[0, 0, -2, 0]`. You can, of course, make an educated guess by trial-and-error by plotting the data with different coefficients.
```python
def sine(x, a, b, c, d):
    return a + b*np.sin(-x*c + d)

# fit data to `sine` function
coefs_sine, _ = curve_fit(sine, x, y, p0=[0, 0, -2, 0])
```
Using the very same setup as before (`x`, `y` and `x_data` defined as in `poly3d` case), `sine` produces the following graph:

[![sine][3]][3]


##### Which function fits the data better?

A common way to check goodness-of-fit is to compare the mean squared error (i.e. MSE) of the fitted values. It basically computes how far away from the actual data is the fitted values are; closer the better, so small MSE values are good. For the example at hand, if we compare the MSE of the two functions (`sine` and `poly3d`), `sine` fits the data better (because its MSE is smaller).

```python
def mse(func, x, y, coefs):
    return np.mean((func(x, *coefs) - y)**2)

mse_sine = mse(sine, x, y, coefs_sine)
mse_poly3d = mse(poly3d, x, y, coefs_poly3d)
```

N.B. This post is only about fitting a function to an existing data. No attempts were made to build predictive models (in which case, how the function fares depends on how it performs on unseen data and both functions here are probably very overfit).


---

### [How to fit a step function](https://stackoverflow.com/q/50371428/19123103)

[![function definition][4]][4]


This function as is will raise OptimizeWarning because it uses `start` and `end` as cutoff points. However, if re-written to make it not explicitly depend on `start` and `end` as cutoff points, `curve_fit` will work. For example, `if x < start, then -1` can be written by shifting `x` by `start`, checking its sign, i.e. `np.sign(x - start)`. Then it becomes a matter of writing a separate definition for each condition of the function and adding them up into a single function.

```python
def f(x, start, end):
    left_tail = np.sign(x - start)
    left_tail[left_tail > -1] = 0         # only -1s are needed from here
    right_tail = np.sign(x - end)
    right_tail[right_tail < 1] = 0        # only 1s are needed from here
    rest = 1 / (end-start) * (x - start)
    rest[(rest < 0) | (rest > 1)] = 0     # only the values between 0 and 1 are needed from here
    return left_tail + rest + right_tail  # sum for a single value

popt, pcov = curve_fit(f, xdata, ydata, p0=[495., 505.])
```

The above function can be written substantially more concisely using `np.clip()` (to limit the values in an array) which can replace the boolean indexing and replacing done above.

```python
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def f(x, start, end):
    left_tail = np.clip(np.sign(x - start), -1, 0)
    rest = np.clip(1 / (end-start) * (x - start), 0, 1)
    return left_tail + rest

# sample data (as in the OP)
xdata = np.linspace(0, 1000, 1000)
ydata = np.r_[[-1.]*500, [1]*500]
ydata += np.random.normal(0, 0.25, len(ydata))

# fit function `f` to the data
popt, pcov = curve_fit(f, xdata, ydata, p0=[495., 505.])
print(popt, pcov)

# plot data along with the fitted function
plt.plot(xdata, ydata, 'b-', label='data')
plt.plot(xdata, f(xdata, *popt), 'r-', label='fit')
plt.legend();

# [499.4995098  501.51244722] [[ 1.24195553 -0.25654186]
#  [-0.25654186  0.2538896 ]]
```

Then we get coefficients (499.499, 501.51) (that are pretty close to (500, 500)) and the plot looks like below.

[![img][5]][5]


### What is `curve_fit()` anyway?

For unbounded optimization problems, `curve_fit` uses `leastsq` which is a Python wrapper for the Fortran `minpack` library, specifically the `lmdif` routine which is an implementation of the Levenberg-Marquardt algorithm. Consider the following `curve_fit()` call that fits function `func` to the the data given by `x` and `y`.
```python
import numpy as np
from scipy import optimize, linalg

def func(xs, *params):
    return np.array(params) @ xs

x = np.random.default_rng(0).normal(0,1, size=10)
y = x.copy()
x = np.array([x, x, x, x])
y = x.sum(axis=0)
res = optimize.curve_fit(func, x, y, p0=[1]*len(x), full_output=1)
```
This is equivalent to a `leastsq()` call that looks like the following. Note that `func` needs to be wrapped in another function that doesn't explicitly use `x` and `y`, in order to use `leastsq()`.

```python
def wrap_func(func, xdata, ydata):
    def func_wrapped(params, *args):
        return func(xdata, *params) - ydata
    return func_wrapped

f = wrap_func(func, x, y)
res = optimize.leastsq(f, [1]*len(x), full_output=1)
```

This in turn is equivalent to calling the Fortran `lmdif` routine directly.

```python
retval = optimize._minpack._lmdif(f, [1]*len(x), ((),), 1)
```
In fact, under the hood, this is the precise call that is made to fit the curve. Then the covariance matrix is computed using the following bit of code.

```python
info = retval[-1]
perm = retval[1]['ipvt'] - 1
n = len(perm)
r = np.triu(retval[1]['fjac'].T[:n, :])
inv_triu = linalg.get_lapack_funcs('trtri', (r,))
invR, trtri_info = inv_triu(r)
print(trtri_info, end='\n\n')

invR[perm] = invR.copy()
cov_x = invR @ invR.T
print(cov_x)
```
As it's evident from the code above, the upper triangle of estimation of the Jacobian matrix (`r`) is inverted using `inv_triu()`, permuted using the `perm` array and its norm is the covariance matrix `cov_x`. In other words, the estimation of the Jacobian matrix have to invertible, which implies that  it cannot be singular.


#### How to solve `OptimizeWarning` it sometimes throws?

##### Tune initial guess `p0`

Depending on the function that is being fit, it is sometimes important to feed an educated initial guess. For example, suppose we have `x` and `y` and try to fit `f` to it with an initial guess of `[1, 1]` for the parameters. However, the exponential function behaves very differently depending on the sign of the power, so it's important to start at the correct sign, which the initial guess of `[1, 1]` doesn't do a good job of. So the covariance is not estimated correctly.<sup>1</sup>

```python
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# sample data
x = np.linspace(0, 10)
y = x + np.random.default_rng(0).normal(0, 1, 50)
f = lambda x,a,b: np.exp(-a*x)+b

# `curve_fit` call
popt, pcov = curve_fit(f, x, y, p0=[1, 1])   # incorrect cov
print(pcov)

# [[inf inf]
#  [inf inf]]
```

If we make an educated initial guess, it works fine.

```python
popt, pcov = curve_fit(f, x, y, p0=[-1,1])   # fine fit
print(pcov)

# [[1.99102540e-05 6.25250542e-04]
#  [6.25250542e-04 4.22266381e-02]]

plt.plot(x, y, label='data')
plt.plot(x, f(x, *popt), label='fit')
plt.legend();
```
[![case1][6]][6]




---

<sup>1</sup> The reason is that the Jacobian matrix doesn't have full rank, i.e., its determinant is zero, so there is no inverse and the covariance matrix is ill-defined.



  [1]: https://stackoverflow.com/a/19165437/19123103
  [2]: https://stackoverflow.com/a/19165440/19123103
  [3]: https://i.stack.imgur.com/5lN2s.png
  [4]: https://i.stack.imgur.com/22ZYx.gif
  [5]: https://i.stack.imgur.com/h7Ccj.png
  [6]: https://i.stack.imgur.com/mn5vt.png

