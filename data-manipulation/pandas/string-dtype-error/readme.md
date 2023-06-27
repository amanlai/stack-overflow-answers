It's a post that was first posted as an answer to the following Stack Overflow question and can be found at https://stackoverflow.com/a/75729269/19123103

## Why do I get ValueError: Cannot set non-string value '0' into a StringArray.?

> I'm using pandas to read in two datasets and reassign the `value` column of each. One dataset is a csv, loaded with `pd.read_csv()`, and the other is xlsx, loaded with `Workbook.sheets()` from the sxl library. 
> 
> Before reassignment, both value columns are string datatype (checked with `df.dtypes`). I reassign the value column like so:
> 
> ```python
> df["value"] = df["value"].replace({"A": 0, "B": 1})
> ```
> 
> This line errors for the data from the csv with 
> ```none
> ValueError: Cannot set non-string value '0' into a StringArray.
> ``` 
> I get the similar error 
> ```none
> ValueError: Cannot set non-string value 'True' into a StringArray
> ``` 
> when I try to reassign a string type column to True/False. There's no error when I run the same line on the value column of the data from the excel document.
> 
> I can fix the error for myself by casting the value before reassignment with `.astype('object')`, and I'm unsure why this works -- `value` in both dataframes is string type.
> 
> My colleague doesn't get the error, so that band-aid may not be necessary. I'm running Python 3.9.4, pandas version 1.5.3, and numpy version 1.22.0.


Long story short, the dtype of `"value"` column is `'string'`, which is an [extension dtype for string data][1] that is also nullable. That means the values in this column can be either a string or NaN. When you try to replace values in this column into integers (`"A" -> 0` and `"B" -> 1`), that's raising the error because, well, the values in this column cannot be integers.

The following code reproduces this error:
```python
df = pd.DataFrame({'value': ['A', 'B', 'A', 'C']}, dtype='string')
df["value"] = df["value"].replace({"A": 0, "B": 1})               # <------ error
```
If the replacement values are strings, there will be no errors, i.e., the following doesn't raise any errors:
```python
df["value"] = df["value"].replace({"A": '0', "B": '1'})           # <------ no error
```

### Why doesn't `dtype=object` raise any errors?

Pandas object dtype can hold any Python object, in other words, anything goes in a column with object dtype. Python objects such as integers, strings, floats, even lists, dictionaries, etc. may be stored in an `object` column. So in such a column, replacing strings with integers works without a hitch.
```python
df1 = pd.DataFrame({'value': ['A', 'B', 'A', 'C']}, dtype=object)
df1["value"] = df1["value"].replace({"A": 0, "B": 1})             # <------ no error
```
However, in that case, the column becomes a mixed column. To see the values the `'value'` column as Python objects, call `tolist()` on the column.
```python
df['value'].tolist()         # ['0', '1', '0', 'C']         <------ all strings
df1['value'].tolist()        # [0, 1, 0, 'C']               <------ integers and strings 
```

Note that `dtype=str` also converts column dtype into `object` (but the values are actually strings), so if the column dtype is changed using e.g. `astype(str)`, then its values can also be replaced by an integer.



  [1]: https://pandas.pydata.org/docs/reference/api/pandas.StringDtype.html