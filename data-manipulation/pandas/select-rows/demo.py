import pandas as pd
import numpy as np

df = DataFrame({'A' : [5, 6, 3, 4], 'B' : [1, 2, 3, 5]})


col = 'A'
x = df.query(f"{col} == 'foo'")
print(x)

#####################################################

col = 'A'
my_var = 'foo'
y = df.query(f"{col} == '{my_var}'") # if my_var is a string
print(y)

my_num = 1
z = df.query(f"{col} == {my_num}") # if my_var is a number
print(z)

my_date = '2022-12-10'
w = df.query(f"{col} == @my_date") # must use @ for datetime though
print(w)


#####################################################


list_of_values = [3,6]

df1 = df[df['A'].isin(list_of_values)]
print(df1)

df2 = df.query("A in @list_of_values")
print(df2)


#####################################################


list_of_values = [3, 4, 5, 6] # a range of values

x = df[df['A'].between(3, 6)]  # or
print(x)

y = df.query('3<=A<=6')
print(y)


#####################################################


list_of_values = [3, 6]
x = df.set_index('A').loc[list_of_values].reset_index()
print(x)

list_of_values = [3, 6, 3]
y = df.reset_index().set_index('A').loc[list_of_values].reset_index().set_index('index').rename_axis(None)
print(y)


#####################################################


xx1 = df[(2*df['A']-5).isin(list_of_values)]         # or
xx2 = df[df['A'].mul(2).sub(5).isin(list_of_values)] # or
xx3 = df.query("A.mul(2).sub(5) in @list_of_values")
print(xx1)
print(xx2)
print(xx3)


#####################################################


df4 = df[~df['A'].isin(list_of_values)]
print(df4)
df4 = df.query("A not in @list_of_values")
print(df4)
df4 = df.query("A != @list_of_values")
print(df4)


#####################################################


df5 = df[df[['A','B']].isin(list_of_values).any(1)]
print(df5)
df5 = df.query("A in @list_of_values or B in @list_of_values")
print(df5)

df6 = df[df[['A','B']].isin(list_of_values).all(1)] 
print(df6)
df6 = df.query("A in @list_of_values and B in @list_of_values")
print(df6)


#####################################################


df = pd.DataFrame({'A' : ['hi', 'hello', 'day'], 'B' : [1, 2, 3]})

col_A_len = map(len, df['A'])
col_B_len = map(len, df['B'])
m = [a==3 and b==3 for a,b in zip(col_A_len, col_B_len)]
x = df[m]
print(x)

x = df[[a==3 for a in map(len, df['A'])]]
print(x)
x = df[df['A'].map(len)==3]
print(x)

x = df.query('A.str.len() != 3')
print(x)


#####################################################


df = pd.DataFrame(np.random.default_rng(0).integers(1, 9, size=(10,3)), columns=['A', 'B', 'C'])

m1 = df['B'] > 50
m2 = df['C'] != 900
m3 = df['C'].pow(2) > 1000
m4 = df['B'].mul(4).between(50, 500)

# filter rows where all of the conditions are True
df[m1 & m2 & m3 & m4]

# filter rows of column A where all of the conditions are True
df.loc[m1 & m2 & m3 & m4, 'A']
```
or put the conditions in a list and reduce it via `bitwise_and` from `numpy` (wrapper for `&`).
```python
conditions = [
    df['B'] > 50,
    df['C'] != 900,
    df['C'].pow(2) > 1000,
    df['B'].mul(4).between(50, 500)
]
# filter rows of A where all of conditions are True
df.loc[np.bitwise_and.reduce(conditions), 'A']