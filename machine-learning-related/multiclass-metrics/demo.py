import numpy as np
from sklearn import metrics

y_true, y_pred = np.random.default_rng(0).choice(list('abc'), size=(2,100), p=[.8,.1,.1])
mcm = metrics.multilabel_confusion_matrix(y_true, y_pred)


# verify macro averaging
assert recall_macro == metrics.recall_score(y_true, y_pred, average='macro')        # True
assert precision_macro == metrics.precision_score(y_true, y_pred, average='macro')  # True


# verify micro averaging
assert recall_micro == metrics.recall_score(y_true, y_pred, average='micro')        # True
assert precision_micro == metrics.precision_score(y_true, y_pred, average='micro')  # True


# verify weighted averaging
assert recall_weighted == metrics.recall_score(y_true, y_pred, average='weighted')        # True
assert precision_weighted == metrics.precision_score(y_true, y_pred, average='weighted')  # True

mccm = metrics.confusion_matrix(y_true, y_pred)