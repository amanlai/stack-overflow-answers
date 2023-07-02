import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter


# case 1

plt.bar([1,2], [1000, 2000], log=True)
plt.gca().yaxis.set_major_formatter(ScalarFormatter()) 
plt.gca().yaxis.set_minor_formatter(ScalarFormatter());   # <---- OK



#############################################################


# case 2

my_dic = {'stats': {'apr': 23083904, 'may': 16786816, 'june': 26197936}}
df = pd.DataFrame(my_dic)

ax = df['stats'].plot(kind='bar', legend=False, xlabel='Month', ylabel='Stats', rot=0)
ax.ticklabel_format(axis='y', scilimits=(0,10))   # <--- no error


#############################################################

ax = df['stats'].plot(kind='bar', legend=False, xlabel='Month', ylabel='Stats', rot=0)
ax.set_yticks(ax.get_yticks()[:-1], [f"{int(x):,}" for x in ax.get_yticks()[:-1]]);