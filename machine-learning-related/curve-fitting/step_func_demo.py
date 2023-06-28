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