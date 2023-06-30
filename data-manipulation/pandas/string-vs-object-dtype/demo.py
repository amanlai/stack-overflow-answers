import pandas as pd


x = pd.Series(['a', float('nan'), 1], dtype=object)
print(x.astype(str).tolist())           # ['a', 'nan', '1']
print(x.astype('string').tolist())      # ['a', <NA>, '1']



#####################################################


x = pd.Series(['a', float('nan'), 'b'], dtype=object)
print(x == 'a')

y = pd.Series(['a', float('nan'), 'b'], dtype='string')
print(y == 'a')


#####################################################


x = pd.Series(['a', 'b'], dtype=str)
y = pd.Series(['a', 'b'], dtype='string')
x[1] = 3                        # OK
y[1] = 3                        # ValueError
y[1] = '3'                      # OK


#####################################################


df = pd.DataFrame({'A': ['a', 'b', 'c'], 'B': [[1], [2,3], [4,5]]}).astype({'A': 'string'})
print(df.select_dtypes('string'))      # only selects the string column

df = pd.DataFrame({'A': ['a', 'b', 'c'], 'B': [[1], [2,3], [4,5]]})
print(df.select_dtypes('object'))      # selects the mixed dtype column as well


#####################################################


lst = np.random.default_rng().integers(1000000, size=1000).astype(str).tolist()

x = pd.Series(lst, dtype=object)
y = pd.Series(lst, dtype='string[pyarrow]')
print(x.memory_usage(deep=True))       # 63041
print(y.memory_usage(deep=True))       # 10041

z = x * 1000
w = (y.astype(str) * 1000).astype('string[pyarrow]')
print(z.memory_usage(deep=True))       # 5970128
print(w.memory_usage(deep=True))       # 5917128