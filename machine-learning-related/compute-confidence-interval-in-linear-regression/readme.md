## Get confidence interval for sklearn's `LinearRegression` coefficients

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/74673133/19123103).</sup>

#### Manual computation

One way is to manually compute it using the results of `LinearRegression` from scikit-learn and numpy methods. The confidence intervals can be computed directly from the mean squared error (MSE) and inverse of the parameter variances.

The workflow goes as follows.
1. Fit a LinearRegression model
2. Prepare the coefficients and features. This is a necessary step because the bias term is a separate attribute of a fit model.
3. Compute degrees of freedom. This is needed to lookup the Student's t-distribution table for the critical value.
4. Compute MSE. This can be computed from the true target values and the corresponding predictions.
5. Compute inverse of the variance of the parameters. This is diagonals of the inverse of the dot product of the features.
6. Compute distance between lower and upper bound of the confidence intervals. The values computed in (4) and (5) determine this value.
7. Compute confidence interval. This is the space created between the gap created in (6).

The code below computes the 95%-confidence interval (`alpha=0.05`). `alpha=0.01` would compute 99%-confidence interval etc.
```python
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LinearRegression

alpha = 0.05 # for 95% confidence interval; use 0.01 for 99%-CI.

# fit a sklearn LinearRegression model
lin_model = LinearRegression().fit(X_train, Y_train)

# the coefficients of the regression model
coefs = np.r_[[lin_model.intercept_], lin_model.coef_]
# build an auxiliary dataframe with the constant term in it
X_aux = X_train.copy()
X_aux.insert(0, 'const', 1)
# degrees of freedom
dof = -np.diff(X_aux.shape)[0]
# Student's t-distribution table lookup
t_val = stats.t.isf(alpha/2, dof)
# MSE of the residuals
mse = np.sum((Y_train - lin_model.predict(X_train)) ** 2) / dof
# inverse of the variance of the parameters
var_params = np.diag(np.linalg.inv(X_aux.T.dot(X_aux)))
# distance between lower and upper bound of CI
gap = t_val * np.sqrt(mse * var_params)

conf_int = pd.DataFrame({'lower': coefs - gap, 'upper': coefs + gap}, index=X_aux.columns)
```

The above code is wrapped in a convenience function wrapper that may be found on the current repo [here](./conf_int.py). This function may be used as follows.
```python
import pandas as pd
from sklearn.datasets import load_boston
from sklearn.linear_model import LinearRegression
from conf_int import get_conf_int

# load data
boston_dataset = load_boston()
data = pd.DataFrame(boston_dataset.data, columns=boston_dataset.feature_names)
X = data.filter(['LSTAT', 'RM'])
y = boston_dataset.target


# for 95% confidence interval; use 0.01 for 99%-CI.
alpha = 0.05
# fit a sklearn LinearRegression model
lin_model = LinearRegression().fit(X, y)

get_conf_int(alpha, lin_model, X, y)
```

Using the Boston housing dataset, the above code produces the dataframe below:

[![res][1]][1]


#### `statsmodels.api.OLS`

If this is too much manual code, you can always resort to the `statsmodels` and use its `conf_int` method:

```python
import statsmodels.api as sm
alpha = 0.05 # 95% confidence interval
lr = sm.OLS(Y_train, sm.add_constant(X_train)).fit()
conf_interval = lr.conf_int(alpha)
```

Since it uses the same formula, it produces the same output as above.



[Stats reference][2]


  [1]: https://i.stack.imgur.com/jtUIL.png
  [2]: https://online.stat.psu.edu/stat415/lesson/7/7.5

