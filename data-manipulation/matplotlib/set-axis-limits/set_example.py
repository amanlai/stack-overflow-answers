import matplotlib.pyplot as plt
import numpy as np


fig, ax = plt.subplots()
ax.set(ylim=(20, 250), xlim=(0, 100))
ax.plot(np.random.default_rng().random(size=10));