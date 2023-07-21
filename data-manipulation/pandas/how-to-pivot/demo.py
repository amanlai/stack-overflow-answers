import pandas as pd
import numpy as np

df = pd.DataFrame(np.random.default_rng().choice(3, size=(100,3)), columns=['colA', 'colB', 'colC'])

agg_df = df.pivot(*df).add_prefix('week_').reset_index().rename_axis(columns=None)


# pivot table
rows = ['colA']
cols = ['colB']
vals = ['colC']
x = df.groupby(rows+cols)[vals].agg(aggfuncs).unstack(cols)
y = df.pivot_table(vals, rows, cols, aggfuncs)
x.equals(y)


# crosstab
x = pd.crosstab(df['colA'], df['colB'])
y = df.pivot_table(index='colA', columns='colB', aggfunc='size', fill_value=0)
z = df.groupby(['colA', 'colB']).size().unstack(fill_value=0)
x.equals(y) and y.equals(z)





#######################################################


df = pd.DataFrame({'A': [1, 1, 1, 2, 2, 2], 'B': [*'xxyyzz'], 
                    'C': [*'CCDCDD'], 'E': [100, 200, 300, 400, 500, 600]})

rows, cols, vals = ['A', 'B'], ['C'], 'E'

# using pivot syntax
df1 = (
    df.assign(ix=df.groupby(rows+cols).cumcount())
    .pivot([*rows, 'ix'], cols, vals)
    .fillna(0, downcast='infer')
    .droplevel(-1).reset_index().rename_axis(columns=None)
)
  
# equivalently, using set_index + unstack syntax
df1 = (
    df
    .set_index([*rows, df.groupby(rows+cols).cumcount(), *cols])[vals]
    .unstack(fill_value=0)
    .droplevel(-1).reset_index().rename_axis(columns=None)
)



df1 = (
    df.assign(ix=df.groupby(rows+cols).cumcount())
    .pivot(rows, [*cols, 'ix'])[vals]
    .fillna(0, downcast='infer')
)
df1 = df1.set_axis([f"{c[0]}_{c[1]}" for c in df1], axis=1).reset_index()

# equivalently, using the set_index + unstack syntax
df1 = (
    df
    .set_index([*rows, df.groupby(rows+cols).cumcount(), *cols])[vals]
    .unstack([-1, *range(-2, -len(cols)-2, -1)], fill_value=0)
)
df1 = df1.set_axis([f"{c[0]}_{c[1]}" for c in df1], axis=1).reset_index()


#######################################################


# pivot table
pv_1 = df.pivot_table(index=rows, columns=cols, values=vals, aggfunc=aggfuncs, fill_value=0)
# internal operation of `pivot_table()`
gb_1 = df.groupby(rows+cols)[vals].agg(aggfuncs).unstack(cols).fillna(0, downcast="infer")
pv_1.equals(gb_1) # True

# pivot
pv_2 = df.pivot(index=rows, columns=cols)
su_2 = df.set_index(rows+cols).unstack(cols)
pv_2.equals(su_2) # True

# pivot
pv_3 = df.pivot(index=rows, columns=cols, values=vals)
su_3 = df.set_index(rows+cols)[vals].unstack(cols)
pv_3.equals(su_3) # True

# this is the precise method used internally (building a new DF seems to be faster than set_index of an existing one)
pv_4 = df.pivot(index=rows, columns=cols, values=vals)
su_4 = pd.DataFrame(df[vals].values, index=pd.MultiIndex.from_arrays([df[c] for c in rows+cols]), columns=vals).unstack(cols)
pv_4.equals(su_4) # True

# cross tab
indexes, columns, values = [df[r] for r in rows], [df[c] for c in cols], next(df[v] for v in vals)
ct_5 = pd.crosstab(indexes, columns, values, aggfunc=aggfuncs)
# internal operation (abbreviated)
from functools import reduce
data = pd.DataFrame({f'row_{i}': r for i, r in enumerate(indexes)} | {f'col_{i}': c for i, c in enumerate(columns)} | {'v': values}, 
                    index = reduce(lambda x, y: x.intersection(y.index), indexes[1:]+columns, indexes[0].index)
                   )
pv_5 = data.pivot_table('v', [k for k in data if k[:4]=='row_'], [k for k in data if k[:4]=='col_'], aggfuncs)
ct_5.equals(pv_5) # True


#######################################################


df = pd.DataFrame({
    'c0': ['A','A','B','C'],
    'c01': ['A','A1','B','C'],
    'c02': ['b','b','d','c'],
    'v1': [1, 3,4,5],
    'v2': [1, 3,4,5]})

df2 = pd.pivot_table(df, index=["c0"], columns=["c01","c02"], values=["v1","v2"]).reset_index()

df2.columns = ['_'.join(map(str, c)).strip('_') for c in df2]
print(df)

df2 = (
    df.pivot_table(index=["c0"], columns=["c01","c02"], values=['1','2'])
    .reorder_levels([1,2,0], axis=1)                # makes "v1","v2" the last level
    .pipe(lambda x: x.set_axis(
        map('_'.join, x)                            # if all column names are strings
        #('_'.join(map(str, c)) for c in x)         # if some column names are not strings
        , axis=1)
         )                                          # rename columns
    .reset_index()
)
print(df2)


#######################################################


df = pd.DataFrame({'A':['x','y','z','x','y','z'],
                 'B':['one','one','one','two','two','two'],
                 'C':[2,18,2,8,2,18]})
table = (
    df
    .pivot_table(index=['A', 'B'], aggfunc=np.sum, margins=True, margins_name='Total')
    .assign(**{
        # must exclude the last row (which are the Totals) for sum and group-specific sum
        '% of Total': lambda x: x['C'] / x.iloc[:-1]['C'].sum() * 100,
        '% of B': lambda x: x['C'] / x.iloc[:-1].groupby(level='A')['C'].transform('sum') * 100
    })
)
print(table)