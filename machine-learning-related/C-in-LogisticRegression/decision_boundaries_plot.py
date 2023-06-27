import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap



def plot_class_regions(clf, transformer, X, y, ax=None):

    if ax is None:
        fig, ax = plt.subplots(figsize=(6,6))
    
    # lighter cmap for contour filling and darker cmap for markers
    cmap_light = ListedColormap(['lightgray', 'khaki'])
    cmap_bold  = ListedColormap(['black', 'yellow'])

    # create a sample for contour plot
    x_min, x_max = X[:, 0].min()-0.5, X[:, 0].max()+0.5
    y_min, y_max = X[:, 1].min()-0.5, X[:, 1].max()+0.5
    x2, y2 = np.meshgrid(np.arange(x_min, x_max, 0.03), np.arange(y_min, y_max, 0.03))
    
    # transform sample
    sample = np.c_[x2.ravel(), y2.ravel()]
    if transformer:
        sample = transformer.transform(sample)
        
    # make predictions
    preds = clf.predict(sample).reshape(x2.shape)
    # plot contour
    ax.contourf(x2, y2, preds, cmap=cmap_light, alpha=0.8)
    # scatter plot
    ax.scatter(X[:, 0], X[:, 1], c=y_train, cmap=cmap_bold, s=50, edgecolor='black')
    ax.set(xlim=(x_min-0.5, x_max+0.5), ylim=(y_min-0.5, y_max+0.5))
    
    return ax