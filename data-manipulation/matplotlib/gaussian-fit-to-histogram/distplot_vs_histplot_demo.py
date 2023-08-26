import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from add_fit_to_histplot import add_fit_to_histplot

# sample data
x = np.random.default_rng(0).normal(1, 4, size=500) * 0.1

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,4))

# left subplot
sns.distplot(x, kde=False, fit=stats.norm, ax=ax1)
ax1.set_title('Using distplot')

# right subplot
sns.histplot(x, stat='density', color='#1f77b4', alpha=0.4, edgecolor='none', ax=ax2)
add_fit_to_histplot(x, fit=stats.norm, ax=ax2)
ax2.set_title('Using histplot+fit');

fig.savefig('distplot_vs_histplot.png')