import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

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



###############################################

def sine(x, a, b, c, d):
    return a + b*np.sin(-x*c + d)

# fit data to `sine` function
coefs_sine, _ = curve_fit(sine, x, y, p0=[0, 0, -2, 0])
print(coefs_sine)


###############################################


def mse(func, x, y, coefs):
    return np.mean((func(x, *coefs) - y)**2)

mse_sine = mse(sine, x, y, coefs_sine)
mse_poly3d = mse(poly3d, x, y, coefs_poly3d)

print(mse_sine, mse_poly3d)


###############################################


# sample data
x = np.linspace(0, 10)
y = x + np.random.default_rng(0).normal(0, 1, 50)
f = lambda x,a,b: np.exp(-a*x)+b

# `curve_fit` call
popt, pcov = curve_fit(f, x, y, p0=[1, 1])   # incorrect cov
print(pcov)

# `curve_fit` call with educated first guess
popt, pcov = curve_fit(f, x, y, p0=[-1,1])   # fine fit
print(pcov)

# [[1.99102540e-05 6.25250542e-04]
#  [6.25250542e-04 4.22266381e-02]]

plt.plot(x, y, label='data')
plt.plot(x, f(x, *popt), label='fit')
plt.legend();