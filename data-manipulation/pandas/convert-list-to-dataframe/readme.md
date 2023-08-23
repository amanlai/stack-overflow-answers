## How to convert a list into a dataframe

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/75179588/19123103).</sup>


The following is a list of the common problems related to converting a Python list into a pandas DataFrame.

1. The simplest method is to cast it to DataFrame object. The data types are inferred if you don't specify it.
   ```python
   df = pd.DataFrame(my_list)
   # or
   df = pd.DataFrame({'col1': my_list})
   ```
   [![res1][1]][1]

   ---

2. If you have a nested list, again, DataFrame constructor works. Make sure that the number of column names are equal to the length of the longest sub-list.
   ```python
   col_names = ['col1', 'col2']
   df = pd.DataFrame(my_list, columns=col_names)
   ```
   [![res2][2]][2]

   ---

3. If you want to convert a flat list into a dataframe row, then convert it into a nested list first:
   ```python
   df = pd.DataFrame([my_list])
   ```
   [![res3][3]][3]

   ---

4. If you want to convert a nested list into a DataFrame where each sub-list is a DataFrame column, convert it into a dictionary and cast into a DataFrame. Make sure that the number of column names match the length of the list, i.e. `len(col_names) == len(my_list)` must be True.
   ```python
   col_names = ['col1', 'col2', 'col3']
   df = pd.DataFrame(dict(zip(col_names, my_list)))
   ```
   [![res4][4]][4]

   ---

5. If you want to convert a flat list into a multi-column DataFrame (as in the OP), one way is to transpose the list using `iter()` and `zip()` functions and cast to a DataFrame.
   ```python
   col_names = ['col1', 'col2', 'col3']
   df = pd.DataFrame(zip(*[iter(my_list)]*len(col_names)), columns=col_names)
   ```
   [![res5][5]][5]

   ---

6. If you want to convert a flat list into a multi-column DataFrame but consecutive values are column values (not row values as above), then you'll have to transpose into a different shape.
   ```python
   col_names = ['col1', 'col2', 'col3']
   df = pd.DataFrame(zip(*[iter(my_list)]*(len(my_list)//len(col_names))), index=col_names).T
   ```
   [![res6][6]][6]


  [1]: https://i.stack.imgur.com/vB4La.png
  [2]: https://i.stack.imgur.com/G8rq7.png
  [3]: https://i.stack.imgur.com/TWzas.png
  [4]: https://i.stack.imgur.com/rory9.png
  [5]: https://i.stack.imgur.com/jwYxQ.png
  [6]: https://i.stack.imgur.com/mS9we.png