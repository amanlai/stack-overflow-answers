from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LogisticRegression
from decision_boundaries_plot import plot_class_regions


# sample
X, y = make_blobs(centers=8, cluster_std=1.3, random_state=4)
y %= 2

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X_train)

# train logistic regression
lr = LogisticRegression()
lr.fit(X_poly, y_train)

# plot class decision boundaries along with scatter plot
ax = plot_class_regions(lr, poly, X_train, y_train)
ax.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=ListedColormap(['black', 'yellow']), 
           s=50, marker='^', edgecolor='black');