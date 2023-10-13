import numpy as np
import pandas as pd
import perfplot


def itertuples_(df):
    mydict = {}
    for row in df.itertuples(index=False):
        mydict.setdefault(row[0], []).append(list(row[1:]))
    return mydict
        
def groupby_(df):
    return {k: g[['A', 'B', 'C']].values.tolist() for k, g in df.groupby('ID')}


perfplot.plot(
    setup=lambda n: pd.DataFrame({'ID': np.arange(n)}).join(pd.DataFrame(np.random.default_rng().choice(10, size=(n, 3)), columns=[*'ABC'])),
    kernels=[lambda df: dict(zip(df['ID'], df.set_index('ID').values.tolist())), 
             lambda df: df.set_index('ID').T.to_dict('list'), 
             lambda df: {x[0]: list(x[1:]) for x in df.itertuples(index=False)}],
    labels= ["dict(zip(df['ID'], df.set_index('ID').values.tolist()))", 
             "df.set_index('ID').T.to_dict('list')", 
             "{x[0]: list(x[1:]) for x in df.itertuples(index=False)}"],
    n_range=[2**k for k in range(18)],
    xlabel='Number of rows',
    title='Unique IDs',
    equality_check=lambda x,y: x==y);



perfplot.plot(
    setup=lambda n: pd.DataFrame(np.random.default_rng().choice(n, size=(n, 4)), columns=['ID','A','B','C']),
    kernels=[itertuples_, groupby_],
    labels= ["itertuples", "groupby"],
    n_range=[2**k for k in range(17)],
    xlabel="Number of rows",
    title="Duplicated IDs",
    equality_check=lambda x,y: x==y);