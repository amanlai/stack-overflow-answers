import matplotlib.pyplot as plt
import random

plt.figure(1, figsize = (8.5,11))
plt.suptitle('plot title')
ax = []
paramValues = range(10)
for i in range(1, 4):
    aPlot = plt.subplot(3,2,i, title=f"Year {i}")
    ax.append(aPlot)
    aPlot.plot(paramValues, [random.randint(20,200) for _ in paramValues], color='#340B8C', marker='o', ms=5, mfc='#EB1717')
    aPlot.grid(True);

plt.setp(ax, ylim=(20,250), facecolor='w', xticks=paramValues, ylabel='Average Price', xlabel='Mark-up')
#            ^^^^  <---- ylim here
plt.tight_layout();