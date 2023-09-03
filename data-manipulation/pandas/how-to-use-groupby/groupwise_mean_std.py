import io
import pandas as pd

txt = """
   a      b      c      d
0  Apple  3      5      7
1  Banana 4      4      8
2  Cherry 7      1      3
3  Apple  3      4      7
"""

df = pd.read_csv(io.StringIO(txt), sep='\s+')

new_df1 = (
    df.groupby(['a', 'b', 'd'])['c'].agg(['mean', 'std'])   # groupby operation
    .set_axis(['c', 'e'], axis=1)                           # rename columns
    .reset_index()                                          # make groupers into columns
    [['a', 'b', 'c', 'd', 'e']]                             # reorder columns
)
print(new_df1)


# named aggregation

new_df2 = (
    df.groupby(['a', 'b', 'd'])['c'].agg([('c', 'mean'), ('e', 'std')])
    .reset_index()                                          # make groupers into columns
    [['a', 'b', 'c', 'd', 'e']]                             # reorder columns
)
print(new_df2)



# named agg with lambda

new_df3 = (
    df.groupby(['a', 'b', 'd'])['c'].agg([('c', 'mean'), ('e', lambda g: g.std(ddof=0))])
    .reset_index()[['a', 'b', 'c', 'd', 'e']]
)
print(new_df3)