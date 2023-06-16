## How to fit a curve to data using python

<sup> It's a post that was first posted as an answer to a Stack Overflow question that can be found at [here](https://stackoverflow.com/a/75598551/19123103). </sup>



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

  [1]: https://stackoverflow.com/a/19165437/19123103
  [2]: https://stackoverflow.com/a/19165440/19123103
  [3]: https://i.stack.imgur.com/5lN2s.png