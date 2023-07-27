import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# assuming we have a more complete data

x = np.random.default_rng(0).normal(size=(1000, 8))

median = np.median(x, axis=0)
q1 = np.quantile(x, 0.25, axis=0)
q3 = np.quantile(x, 0.75, axis=0)

# compute whiskers' locations
whislo = [np.min(x[x[:, i] > v, i]) for i, v in enumerate(q1 - (q3 - q1)*1.5)]
whishi = [np.max(x[x[:, i] < v, i]) for i, v in enumerate(q3 + (q3 - q1)*1.5)]
# identify fliers
fliers = [x[(x[:, i] < lo) | (x[:, i] > hi), i] for i, (lo, hi) in enumerate(zip(whislo, whishi))]

keys = ['med', 'q1', 'q3', 'whislo', 'whishi', 'fliers']
stats2 = [dict(zip(keys, vals)) for vals in zip(median, q1, q3, whislo, whishi, fliers)]

plt.subplot().bxp(stats2);
plt.gcf().set_facecolor('white');
a, b = plt.ylim()
plt.gcf().savefig('second_image.png')


###################################################################################


# assuming normal distribution

means = x.mean(axis=0)
q1 = means + std * stats.norm.ppf(0.25)
q3 = means + std * stats.norm.ppf(0.75)
whislo = q1 - (q3 - q1)*1.5
whishi = q3 + (q3 - q1)*1.5

keys = ['med', 'q1', 'q3', 'whislo', 'whishi']
stats1 = [dict(zip(keys, vals)) for vals in zip(means, q1, q3, whislo, whishi)]
plt.subplot().bxp(stats1, showfliers=False);
plt.ylim(a, b)
plt.gcf().set_facecolor('white');
plt.gcf().savefig('first_image.png');