import numpy as np
from sklearn.datasets import make_classification

class MyLogisticRegression:
    
    def __init__(self, C=None, fit_intercept=True, step_size=0.005, max_iter=100, verbose=True):
        """
        C: float/int, default: None.
           Inverse of the L2-regularization strength. If None, no regularization is applied.
        fit_intercept: bool, default: True.
           Specifies if intercept should be added to the regression function.
        step_size: float, default: 0.005.
           The scale of the step size in each iteration, aka. learning rate.
        max_iter: int, default: 100.
           The number of iterations to take for the gradient descent to converge
        verbose: bool, default: True.
           Whether to print intermediate log-likelihood values.
        """
        self.l2_penalty = 1 / C if C else 0
        self.step_size = step_size
        self.max_iter = max_iter
        self.verbose = verbose
        self.fit_intercept = fit_intercept
        
    def fit(self, X, y, x0=None):
        """
        X: np.ndarray. 
           Feature matrix
        y: np.ndarray. 
           Target variable
        x0: iterable, default: None. 
           Initial guess of the coefficients. If None, all 0 array is initialized
        """

        X_ = np.c_[[1]*len(X), X] if self.fit_intercept else X
        self.coef_ = np.array(x0 if x0 else [0]*X_.shape[1], dtype=float)
        
        for ctr in range(1, self.max_iter+1):
            # predict P(y_i = 1 | x_i, w)
            scores = X_.dot(self.coef_)
            predicted_proba = 1 / (1 + np.exp(-scores))
            # compute error
            errors = y - predicted_proba
            
            # compute the derivative for the coefficients
            # add L2 penalty term for all Xi that isn't the intercept
            penalty_term = 2*self.l2_penalty*self.coef_*[0, *[1]*(len(self.coef_)-1)]
            derivatives = X_.T.dot(errors) - penalty_term
            # update the coefficients
            self.coef_ += self.step_size * derivatives

            if self.verbose:
                s = int(np.log10(self.max_iter)+0.5)
                if ctr<11 or ctr in np.linspace(10, self.max_iter, 10).astype(int):
                    lp = self.log_likelihood(X_, y)
                    print(f"iteration {ctr: >{s}}: log likelihood = {lp:.4f}")
        return self

    def log_likelihood(self, X, y):
        # compute score
        scores = X.dot(self.coef_)
        penalty_term = self.l2_penalty*np.sum(self.coef_[1:]**2)
        # compute log-likelihood
        return np.sum((y-1)*scores - np.log(1 + np.exp(-scores))) - penalty_term

    def compute_accuracy(self, X, y):
        X_ = np.c_[[1]*len(X), X] if self.fit_intercept else X
        # make predictions
        predictions = X_.dot(self.coef_) > 0
        # compute accuracy
        return np.mean(predictions == y)


X, y = make_classification()
my_lr = MyLogisticRegression(C=0.01)
my_lr.fit(X, y)
print(my_lr.compute_accuracy(X, y))