## What is the inverse of regularization strength in Logistic Regression?

In one sentence, _regularization_ makes the model perform worse on training data so that it may perform better on holdout data. 

Logistic regression is an optimization problem where the following objective function is minimized.

[![func1][1]][1]

where loss function looks like (at least for `solver='lbfgs'`) the following.

[![loss func][2]][2]

Regularization adds a norm of the coefficients to this function. The following implements the L2 penalty.

[![func2][3]][3]

From the equation, it's clear that the regularization term is there to penalize large coefficients (the minimization problem is solving for the coefficients that minimize the objective function). The regularization strength is determined by `C` and as C increases, the regularization term becomes smaller (and for extremely large C values, it's as if there is no regularization at all).

If the initial model is overfit (as in, it fits the training data too well), then adding a strong regularization term (with small `C` value) makes the model perform worse for the training data, but introducing such "noise" improves the model's performance on unseen (or test) data.

---

An example with 1000 samples and 200 features shown below. As can be seen from the plot of accuracy over different values of `C`, if `C` is large (with very little regularization), there is a big gap between how the model performs on training data and test data. However, as `C` decreases, the model performs worse on training data but performs better on test data (test accuracy increases). However, when `C` becomes too small (or the regularization becomes too strong), the model begins performing worse again because now the regularization term completely dominates the objective function.

[![C vs accuracy][4]][4]




  [1]: https://i.stack.imgur.com/mzAMA.png
  [2]: https://i.stack.imgur.com/Ho9ZH.png
  [3]: https://i.stack.imgur.com/Ke67p.png
  [4]: https://i.stack.imgur.com/O9V3R.png