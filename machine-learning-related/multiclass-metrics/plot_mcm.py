import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.utils.multiclass import unique_labels

def plot_confusion_matrix(y_true, y_pred, ax, cmap=None):
    
    cm = metrics.confusion_matrix(y_true, y_pred)
    n_classes = cm.shape[0]
    Z = np.arange(1,n_classes**2+1).reshape(n_classes, n_classes)
    X = np.arange(n_classes + 1)
    Y = np.arange(n_classes + 1)[::-1]
    
    ax.pcolormesh(X, Y, Z, cmap=cmap)
    for i in X[:-1]:
        for j in Y[1:]:
            ax.text(j+0.5, n_classes-i-0.5, cm[i,j], ha="center", va="center", color='black', fontsize=20)

    display_labels = unique_labels(y_true, y_pred)
    ax.set(xticks=X[1:]-0.5, yticks=Y[:-1]-0.5, xticklabels=display_labels, yticklabels=display_labels)

    
def plot_mcm(y_true, y_pred, labels=list('abc'), cmaps=None):

    fig, ax = plt.subplots(1,len(labels), figsize=(12,3), facecolor='white')
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    for i, (label, cmap) in enumerate(zip(labels, cmaps)):
        true = np.array([f'not {label}']*len(y_true))
        pred = true.copy()
        # only consider the current label
        true[y_true == label] = label
        pred[y_pred == label] = label
        # compute the confusion matrix for the current label
        plot_confusion_matrix(true, pred, ax=ax[i], cmap=cmap)
            
    fig.supxlabel('Predicted label', size=20)
    fig.supylabel('True label', size=20)
    fig.tight_layout()


