It's a post that was first posted as an answer to the following Stack Overflow question and can be found at https://stackoverflow.com/a/73436639/19123103

## Replace and merge rows in pandas according to condition

> I have a dataframe:
> 
> ```none
>    lft rel rgt num
> 0	t3	r3	z2	3
> 1	t1	r3	x1	9
> 2	x2	r3	t2	8
> 3	x4	r1	t2	4
> 4	t1	r1	z3	1
> 5	x1	r1	t2	2
> 6	x2	r2	t4	4
> 7	z3	r2	t4	5
> 8	t4	r3	x3	4
> 9	z1	r2	t3	4
> ```
> 
> And a reference dictionary:
> 
> ```python
> replacement_dict = {
>     'X1' : ['x1', 'x2', 'x3', 'x4'],
>     'Y1' : ['y1', 'y2'],
>     'Z1' : ['z1', 'z2', 'z3']
> }
> ```
> 
> My goal is to replace all occurrences of `replacement_dict['X1']` with 'X1', and then merge the rows together. For example, any instance of 'x1', 'x2', 'x3' or 'x4' will be replaced by 'X1', etc. 
> 
> I can do this by selecting the rows that contain any of these strings and replacing them with 'X1':
> 
> ```python
> keys = replacement_dict.keys()
> for key in keys:
>     DF.loc[DF['lft'].isin(replacement_dict[key]), 'lft'] = key
>     DF.loc[DF['rgt'].isin(replacement_dict[key]), 'rgt'] = key
> ```
> 
> giving:
> 
> ```none
> 	lft	rel	rgt	num
> 0	t3	r3	Z1	3
> 1	t1	r3	X1	9
> 2	X1	r3	t2	8
> 3	X1	r1	t2	4
> 4	t1	r1	Z1	1
> 5	X1	r1	t2	2
> 6	X1	r2	t4	4
> 7	Z1	r2	t4	5
> 8	t4	r3	X1	4
> 9	Z1	r2	t3	4
> ```
> 
> Now, if I select all the rows containing 'X1' and merge them, I should end up with:
> 
> ```none
> 	lft	rel	rgt	num
> 0	X1	r3	t2	8
> 1	X1	r1	t2	6
> 2	X1	r2	t4	4
> 3	t1	r3	X1	9
> 4	t4	r3	X1	4
> ```
> 
> So the three columns ['lft', 'rel', 'rgt'] are unique while the 'num' column is added up for each of these rows. The row 1 above : ['X1'  'r1'  't2'  6] is the sum of two rows ['X1'  'r1'  't2'  4] and ['X1'  'r1'  't2'  2].
> 
> I can do this easily for a small number of rows, but I am working with a dataframe with 6 million rows and a replacement dictionary with 60,000 keys. This is taking forever using a simple row wise extraction and replacement. 
> 
> How can this (specifically the last part) be scaled efficiently? Is there a pandas trick that someone can recommend?

Reverse the `replacement_dict` mapping and `map()` this new mapping to each of lft and rgt columns to substitute certain values (e.g. x1->X1, y2->Y1 etc.). As some values in lft and rgt columns don't exist in the mapping (e.g. t1, t2 etc.), call `fillna()` to fill in these values.<sup>1</sup>

You may also `stack()` the columns whose values need to be replaced (lft and rgt), call map+fillna and `unstack()` back but because there are only 2 columns, it may not be worth the trouble for this particular case.

The second part of the question may be answered by summing num values after grouping by lft, rel and rgt columns; so `groupby().sum()` should do the trick.
```python
# reverse replacement map
reverse_map = {v : k for k, li in replacement_dict.items() for v in li}

# substitute values in lft column using reverse_map
df['lft'] = df['lft'].map(reverse_map).fillna(df['lft'])
# substitute values in rgt column using reverse_map
df['rgt'] = df['rgt'].map(reverse_map).fillna(df['rgt'])

# sum values in num column by groups
result = df.groupby(['lft', 'rel', 'rgt'], as_index=False)['num'].sum()
```

<sup>1</sup>: `map()` + `fillna()` may perform better for your use case than `replace()` because under the hood, `map()` implements a Cython optimized `take_nd()` method that performs particularly well if there are a lot of values to replace, while `replace()` implements `replace_list()` method which uses a Python loop. So if `replacement_dict` is particularly large (which it is in your case), the difference in performance will be huge, but if `replacement_dict` is small, `replace()` may outperform `map()`.