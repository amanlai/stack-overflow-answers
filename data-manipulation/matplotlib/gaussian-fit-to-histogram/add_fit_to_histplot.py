import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def add_fit_to_histplot(a, fit=stats.norm, ax=None):

    if ax is None:
        ax = plt.gca()

    # compute bandwidth
    bw = len(a)**(-1/5) * a.std(ddof=1)
    # initialize PDF support
    x = np.linspace(a.min()-bw*3, a.max()+bw*3, 200)
    # compute PDF parameters
    params = fit.fit(a)
    # compute PDF values
    y = fit.pdf(x, *params)
    # plot the fitted continuous distribution
    ax.plot(x, y, color='#282828')
    return ax