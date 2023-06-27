import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap



def plot_class_regions(clf, transformer, X, y, ax):
    
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


# sample

X, y = make_blobs(centers=8, cluster_std=1.3, random_state=4)
y %= 2

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

fig, ax = plt.subplots(figsize=(6, 6))

lr = LogisticRegression()
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X_train)
lr.fit(X_poly, y_train)

# plot class decision boundaries along with scatter plot
plot_class_regions(lr, poly, X_train, y_train, ax);
ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=ListedColormap(['black', 'yellow']), 
           s=50, marker='^', edgecolor='black');