## How to solve ValueError: Target is multiclass but average='binary'

The error is pretty self-explanatory. It is saying for a problem with more than 2 classes, there needs to be some kind of averaging rule. The valid rules are: `'micro'`, `'macro'`, `'weighted'` and `None` (the documentation lists `'samples'` but it's not applicable for multi-class targets). 

If we look at its [source code][1], multi-class problems are treated like a multi-label problem when it comes to precision and recall score computation because the underlying confusion matrix used (`multilabel_confusion_matrix`) is the same.<sup>1</sup> This confusion matrix creates a 3D array where each "plane" is the 2x2 confusion matrix where the positive value is one of the labels.

### What are the differences between each averaging rule?

- With `average=None`, the precision/recall scores of each class is returned (without any averaging), so we get an array of scores whose length is equal to the number of classes.<sup>2</sup>

- With `average='macro'`, precision/recall is computed for each class and then the average is taken.

  [![macro][2]][2]

- With `average='micro'`, the contributions of all classes are summed up to compute the average precision/recall.

  [![micro][3]][3]

- `average='weighted'` is really a weighted macro average where the weights are the actual positive classes.

  [![weighted][4]][4]

---

Let's consider an example.
```python
import numpy as np
from sklearn import metrics
y_true, y_pred = np.random.default_rng(0).choice(list('abc'), size=(2,100), p=[.8,.1,.1])
```
The multilabel confusion matrix for this example looks like the following.


[![confusion matrix][5]][5]


The respective precision/recall scores are as follows:

- `average='macro'` precision/recall are:
  ```python
  recall_macro = (57 / (57 + 16) + 1 / (1 + 10) + 6 / (6 + 10)) / 3
  precision_macro = (57 / (57 + 15) + 1 / (1 + 13) + 6 / (6 + 8)) / 3

  # verify using sklearn.metrics.precision_score and sklearn.metrics.recall_score
  recall_macro == metrics.recall_score(y_true, y_pred, average='macro')        # True
  precision_macro == metrics.precision_score(y_true, y_pred, average='macro')  # True
  ```

- `average='micro'` precision/recall are:
  ```python
  recall_micro = (57 + 1 + 6) / (57 + 16 + 1 + 10 + 6 + 10)
  precision_micro = (57 + 1 + 6) / (57 + 15 + 1 + 13 + 6 + 8)

  # verify using sklearn.metrics.precision_score and sklearn.metrics.recall_score
  recall_micro == metrics.recall_score(y_true, y_pred, average='micro')        # True
  precision_micro == metrics.precision_score(y_true, y_pred, average='micro')  # True
  ```

- `average='weighted'` precision/recall are:
  ```python
  recall_weighted = (57 / (57 + 16) * (57 + 16) + 1 / (1 + 10) * (1 + 10) + 6 / (6 + 10) * (6 + 10)) / (57 + 16 + 1 + 10 + 6 + 10)
  precision_weighted = (57 / (57 + 15) * (57 + 16) + 1 / (1 + 13) * (1 + 10) + 6 / (6 + 8) * (6 + 10)) / (57 + 16 + 1 + 10 + 6 + 10)

  # verify using sklearn.metrics.precision_score and sklearn.metrics.recall_score
  recall_weighted == metrics.recall_score(y_true, y_pred, average='weighted')        # True
  precision_weighted == metrics.precision_score(y_true, y_pred, average='weighted')  # True
  ```

As you can see, the example here is imbalanced (class `a` has 80% frequency while `b` and `c` have 10% each). The main difference between the averaging rules is that macro-averaging doesn't account for class imbalance but micro and weighted do. So `'macro'` may result in an "artificially" high or low score depending on the imbalance.

Also, it's very easy to see from the formula that recall scores for `'micro'` and `'weighted'` are equal.


### Why is accuracy == recall == precision == f1-score for `average='micro'`?


If we look at the multilabel confusion matrix as constructed above, each sub-matrix corresponds to a One vs Rest classification problem; i.e. in each _not_ column/row of a sub-matrix, the other two labels are accounted for. 

[![confusion matrices][6]][6]







---


The code used to make the multiclass confusion matrix plots.

```python
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
```


<sup>1</sup> You can check that it is indeed the case by constructing a random multi-class classification problem and its corresponding multi-label version and check the equality of the precision and recall scores.

```python
import numpy as np
from sklearn import metrics
y_true, y_pred = np.random.default_rng().choice(3, size=(2,100))             # multi-class
y_true_multilabel, y_pred_multilabel = map(pd.get_dummies, (y_true, y_pred)) # multi-label

for avg in (None, 'micro', 'macro', 'weighted'):
    # precision and recall scores are the same for all averaging rules for both problems
    p1 = metrics.precision_score(y_true, y_pred, average=avg)
    p2 = metrics.precision_score(y_true_multilabel, y_pred_multilabel, average=avg)
    r1 = metrics.recall_score(y_true, y_pred, average=avg)
    r2 = metrics.recall_score(y_true_multilabel, y_pred_multilabel, average=avg)
    assert np.array([p1 == p2]).all() and np.array([r1 == r2]).all()
```

Also the `multilabel_confusion_matrix()` method is essentially a confusion matrix for each class. So its implementation looks very much like:
```python
from sklearn import metrics
def multilabel_confusion_matrix(y_true, y_pred, labels)
    out = np.empty(shape=(len(labels), 2, 2), dtype='int')
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    for i, label in enumerate(sorted(labels)):
        # only consider the current label
        true = y_true == label
        pred = y_pred == label
        # compute the confusion matrix for the current label
        mcm[i] = metrics.confusion_matrix(true, pred)
    return mcm
```

<sup>2</sup> With `average=None`, the precision/recall scores of each class is returned (without any averaging), so we get an array of scores whose length is equal to the number of classes.

```python
def custom_scorer(scorer, y_true, y_pred, labels=list('abc')):
    
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    out = np.empty(shape=len(labels))
    
    for i, label in enumerate(sorted(labels)):
        true = np.array([f'not {label}']*len(y_true))
        pred = true.copy()
        # only consider the current label
        true[y_true == label] = label
        pred[y_pred == label] = label
        out[i] = scorer(true, pred, pos_label=label)
        
    return out

(custom_scorer(metrics.precision_score, y_true, y_pred) == metrics.precision_score(y_true, y_pred, average=None)).all() # True
(custom_scorer(metrics.recall_score, y_true, y_pred) == metrics.recall_score(y_true, y_pred, average=None)).all()       # True
```


  [1]: https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/metrics/_classification.py#L1714-L1740
  [2]: https://i.stack.imgur.com/e01xN.png
  [3]: https://i.stack.imgur.com/fp4td.png
  [4]: https://i.stack.imgur.com/JMDrn.png
<!---  [5]: https://i.stack.imgur.com/Iuf1G.png --->
  [5]: https://i.stack.imgur.com/JsedR.png
  [6]: https://i.stack.imgur.com/wkJRn.png