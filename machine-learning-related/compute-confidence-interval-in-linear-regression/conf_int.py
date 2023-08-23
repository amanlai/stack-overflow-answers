import numpy as np
import pandas as pd
from scipy import stats


def get_conf_int(alpha, lr, X, y):
    
    """
    Returns (1-alpha) 2-sided confidence intervals
    for sklearn.LinearRegression coefficients
    as a pandas DataFrame
    """
    
    # the coefficients of the regression model
    coefs = np.r_[[lr.intercept_], lr.coef_]
    # build an auxiliary dataframe with the constant term in it
    X_aux = X.copy()
    X_aux.insert(0, 'const', 1)

    # compute degrees of freedom
    dof = -np.diff(X_aux.shape)[0]

    # MSE of the residuals
    mse = np.sum((y - lr.predict(X)) ** 2) / dof

    # inverse of the variance of the parameters
    var_params = np.diag(np.linalg.inv(X_aux.T.dot(X_aux)))

    # Student's t-distribution table lookup
    t_val = stats.t.isf(alpha/2, dof)

    # distance between lower and upper bound of CI
    gap = t_val * np.sqrt(mse * var_params)

    return pd.DataFrame({
        'lower': coefs - gap, 'upper': coefs + gap
    }, index=X_aux.columns)