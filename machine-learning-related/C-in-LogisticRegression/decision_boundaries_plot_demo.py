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


##################################################################

def plotter(X, y):
    
    # train-test-split
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
    # add more features
    poly = PolynomialFeatures(degree=6)
    X_poly = poly.fit_transform(X_train)

    fig, axs = plt.subplots(1, 2, figsize=(12,4))

    for i, lr in enumerate([LogisticRegression(penalty=None, max_iter=10000), 
                            LogisticRegression(max_iter=2000)]):
        
        lr.fit(X_poly, y_train)

        plot_class_regions(lr, poly, X_train, y_train, axs[i])
        axs[i].scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap=ListedColormap(['black', 'yellow']), 
                   s=50, marker='^', edgecolor='black', label='Test')
        axs[i].set_title(f"{'No' if i == 0 else 'With'} penalty\nTest accuracy = {lr.score(poly.transform(X_test), y_test)}")
        axs[i].legend()
        
X, y = make_circles(factor=0.7, noise=0.2, random_state=2023)
plotter(X, y)