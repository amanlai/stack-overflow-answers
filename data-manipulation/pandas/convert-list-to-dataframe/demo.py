import pandas as pd

# 1
my_list = [1, 2, 3, 4]
df1 = pd.DataFrame({'col1': my_list})


# 2

col_names = ['col1', 'col2']
my_list = [['a', 1], ['a', 2], ['b', 1]]
df2 = pd.DataFrame(my_list, columns=col_names)


# 3
my_list = [1, 2, 3, 4]
df3 = pd.DataFrame([my_list])


# 4

col_names = ['col1', 'col2', 'col3']
my_list = [[1, 2], ['a', 'b'], [0.5, 0.7]]
df4 = pd.DataFrame(dict(zip(col_names, my_list)))


# 5

col_names = ['col1', 'col2', 'col3']
my_list = [1, 2, 3, 4, 5, 6]
data = zip(*[iter(my_list)]*len(col_names))
df5 = pd.DataFrame(data, columns=col_names)


# 6

col_names = ['col1', 'col2', 'col3']
my_list = [1, 2, 3, 4, 5, 6]
data = zip(*[iter(my_list)]*(len(my_list)//len(col_names)))
df6 = pd.DataFrame(data, index=col_names).T