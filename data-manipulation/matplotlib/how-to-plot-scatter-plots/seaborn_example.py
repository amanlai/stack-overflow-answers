import seaborn as sns
import matplotlib.pyplot as plt


# sample data
x = [1, 2, 3]

fig, axs = plt.subplots(1, 2, figsize=(12,4), facecolor='white')

sns.scatterplot(x=x, y=x, s=1000, ec='black', ax=axs[0])   # <---- edge width unchanged
sns.scatterplot(x=x, y=x, s=1000, ec='black', ax=axs[1]) 
axs[1].collections[0].set_lw(5)                            # <---- edge width changed
plt.setp(axs, xlim=(0.5, 3.5), ylim=(0.5, 3.5));