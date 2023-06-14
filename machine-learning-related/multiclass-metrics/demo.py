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






################################################################################
### multiclass has a corresponding multilabel problem

y_true, y_pred = np.random.default_rng().choice(3, size=(2,100))             # multi-class
y_true_multilabel, y_pred_multilabel = map(pd.get_dummies, (y_true, y_pred)) # multi-label

for avg in (None, 'micro', 'macro', 'weighted'):
    # precision and recall scores are the same for all averaging rules for both problems
    p1 = metrics.precision_score(y_true, y_pred, average=avg)
    p2 = metrics.precision_score(y_true_multilabel, y_pred_multilabel, average=avg)
    r1 = metrics.recall_score(y_true, y_pred, average=avg)
    r2 = metrics.recall_score(y_true_multilabel, y_pred_multilabel, average=avg)
    assert np.array([p1 == p2]).all() and np.array([r1 == r2]).all()




###############################################
# with `average=None`, all scores are returned

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