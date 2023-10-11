## Create a pandas DataFrame from a numpy array

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/75804890/19123103).</sup>

Given an ndarray such as the following:
```python
data = np.array([['','Col1','Col2'],['Row1',1,2],['Row2',3,4]])
```
How do we construct a DataFrame to have `Row1` and `Row2` as index values, and `Col1`, `Col2` as header values.


#### 1. Dtypes need to be recast

The problem with the original array is that it mixes strings with numbers, so the dtype of the array is either `object` or `str` which is not optimal for the dataframe. That can be remedied by calling `astype` at the end of dataframe construction.
```python
df = pd.DataFrame(data[1:, 1:], index=data[1:, 0], columns=data[0, 1:]).astype(int)
```
#### 2. Use `read_csv` for convenience 

Since `data` in the OP is almost like a text file read in as a numpy array, one could convert it into a file-like object (using `StringIO` from the built-in `io` module) and use `pd.read_csv` instead. Since `read_csv` reads the first row as column labels, the only thing that needs to be specified is to read the first column as index. Also, `read_csv` infers the dtypes, so no need for `astype()` etc. either.
```python
from io import StringIO
df = pd.read_csv(StringIO('\n'.join([','.join(row) for row in data.tolist()])), index_col=[0])
```

A convenience wrapper function for the latter case:
```python
from io import StringIO
def read_array(data, index_col=[0], header=0):
    sio = StringIO('\n'.join([','.join(row) for row in data.tolist()]))
    return pd.read_csv(sio, index_col=index_col, header=header)

df = read_array(data)
```
[![res][1]][1]

One advantage of this method is that if there were MultiIndex columns or indices, there will need to be some manual work to construct the dataframe correctly with `pd.DataFrame`. Meanwhile, it's very easy with `read_array()` (because `read_csv` handles it internally, just delegate that stuff to pandas). For example, for the following data, just specify which rows are supposed to be read in as headers:

```python
data = np.array([['', 'Col0', 'Col0'], ['', 'Col1', 'Col2'], ['Row1', 1, 2],['Row2', 3, 4]])

df = read_array(data, header=[0,1])

# to produce the equivalent with pd.DataFrame, pd.MultiIndex object needs to be constructed
df = pd.DataFrame(data[2:, 1:], index=data[2:, 0], columns=pd.MultiIndex.from_arrays(data[:2, 1:])).astype(int)
```
[![res3][2]][2]

#### 3. Cast numpy arrays to dataframe

This is for different cases than specified in the OP but in general, it's possible to cast a numpy array immediately into a pandas dataframe. If a custom stringified column labels are needed, just call `add_prefix()`. For example, 
```python
arr = np.arange(9).reshape(-1,3)
df = pd.DataFrame(arr).add_prefix('Col')
```
[![res2][3]][3]


  [1]: https://i.stack.imgur.com/48ddz.png
  [2]: https://i.stack.imgur.com/T5PmA.png
  [3]: https://i.stack.imgur.com/W0DAY.png