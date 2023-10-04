## How to solve the error: `Reshape your data either using array.reshape(-1, 1) if your data has a single feature or array.reshape(1, -1) if it contains a single sample`

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/75770886/19123103).</sup>

The error is basically saying to convert the flat feature array into a column array. `reshape(-1, 1)` does the job; also `[:, None]` can be used.

The second dimension of the feature array `X` must match the second dimension of whatever is passed to `predict()` as well. Since `X` is coerced into a 2D array, the array passed to `predict()` should be 2D as well.

```python
x = np.array([2.0 , 2.4, 1.5, 3.5, 3.5, 3.5, 3.5, 3.7, 3.7])
y = np.array([196, 221, 136, 255, 244, 230, 232, 255, 267])
X = x[:, None]         # X.ndim should be 2

lr = LinearRegression()
lr.fit(X, y)

prediction = lr.predict([[2.4]])
```

If your input is a pandas column, then use double brackets (`[[]]`) get a 2D feature array.
```python
df = pd.DataFrame({'feature': x, 'target': y})
lr = LinearRegression()
lr.fit(df['feature'], df['target'])            # <---- error
lr.fit(df[['feature']], df['target'])          # <---- OK
#        ^^         ^^                           <---- double brackets 
```

##### Why should `X` be 2D?

If we look at the source code of `fit()` (of any model in scikit-learn), one of the first things done is to validate the input via the [`validate_data()`][1] method, which calls [`check_array()`][2] to validate `X`. `check_array()` checks among other things, whether `X` is 2D. It is essential for `X` to be 2D because ultimately, `LinearRegression().fit()` calls `scipy.linalg.lstsq` to solve the least squares problem and `lstsq` [requires `X` to be 2D][4] to perform matrix multiplication. 

For classifiers, the second dimension is needed to get the number of features, which is essential to get the model coefficients in the correct shape.

  [1]: https://github.com/scikit-learn/scikit-learn/blob/364c77e047ca08a95862becf40a04fe9d4cd2c98/sklearn/linear_model/_base.py#L648-L650
  [2]: https://github.com/scikit-learn/scikit-learn/blob/364c77e047ca08a95862becf40a04fe9d4cd2c98/sklearn/base.py#L584
  [3]: https://github.com/scikit-learn/scikit-learn/blob/main/sklearn/utils/validation.py#L891-L907
  [4]: https://github.com/scipy/scipy/blob/c1ed5ece8ffbf05356a22a8106affcd11bd3aee0/scipy/linalg/_basic.py#L1157-L1158