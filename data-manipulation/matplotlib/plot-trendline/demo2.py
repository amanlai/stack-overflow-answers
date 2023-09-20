import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

x_data, y_data = np.repeat(np.linspace(0, 9, 100)[None,:], 2, axis=0) + np.random.rand(2, 100)*2


fig, axs = plt.subplots(1,2, figsize=(12,3))
axs[0].scatter(x_data, y_data)
sns.regplot(x=x_data, y=y_data, ci=False, line_kws={'color':'red'}, ax=axs[1]);