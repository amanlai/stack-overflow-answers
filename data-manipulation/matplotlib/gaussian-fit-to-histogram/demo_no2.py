import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from add_fit_to_histplot import add_fit_to_histplot 


# ohtotasche (https://stackoverflow.com/a/66893884/19123103)'s function
def normal(mean, std, color="black"):
    x = np.linspace(mean-4*std, mean+4*std, 200)
    p = stats.norm.pdf(x, mean, std)
    z = plt.plot(x, p, color, linewidth=2)



data = np.random.default_rng(0).poisson(0.5, size=500)

fig, (a1, a2) = plt.subplots(1, 2, facecolor='white', figsize=(10,4))

# left subplot
sns.histplot(data, stat='density', color='#1f77b4', alpha=0.4, edgecolor='none', ax=a1)
add_fit_to_histplot(data, fit=stats.norm, ax=a1)
a1.set_title("With add_fit_to_histplot")

# right subplot
sns.histplot(x=data, stat="density", ax=a2)
normal(data.mean(), data.std())
a2.set_title("With ohtotasche's normal function")

fig.savefig('gaussian_fit_on_poisson_data.png')