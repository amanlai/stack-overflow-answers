import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

# sample data
y_true, y_pred = np.random.default_rng(0).choice(list('abc'), size=(2,100), p=[.8,.1,.1])


cmaps = [
    mpl.colors.ListedColormap(['yellow', 'red', 'brown', 'purple']),
    mpl.colors.ListedColormap(['yellow', 'blue', 'pink', 'purple']),
    mpl.colors.ListedColormap(['yellow', 'green', 'orange', 'purple'])
]

plot_mcm(y_true, y_pred, cmaps=cmaps)  # plot multilabel confusion matrices




# plot multiclass confusion matrices
cmap1 = mpl.colors.ListedColormap(['yellow', 'red', 'red','blue', 'yellow', 'blue', 'green', 'green', 'yellow'])
cmap2 = mpl.colors.ListedColormap(['yellow', 'pink', 'orange','brown', 'yellow', 'orange', 'brown', 'pink', 'yellow'])
fig, ax = plt.subplots(1, 2, facecolor='white', figsize=(12,3))
plot_confusion_matrix(y_true, y_pred, ax=ax[0], cmap=cmap1)
ax[0].set_xlabel('Recall', fontsize=20)
plot_confusion_matrix(y_true, y_pred, ax=ax[1], cmap=cmap2)
ax[1].set_xlabel('Precision', fontsize=20);