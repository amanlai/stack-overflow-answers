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
