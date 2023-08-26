import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from add_fit_to_histplot import add_fit_to_histplot

# sample data
x = np.random.default_rng(0).normal(1, 4, size=500) * 0.1

# plot histogram with gaussian fit
sns.histplot(x, stat='density')
add_fit_to_histplot(x, fit=stats.norm);
plt.savefig('first graph.png')