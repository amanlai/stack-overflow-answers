import pandas as pd
import perfplot
import random
import matplotlib.pyplot as plt

plt.figure(figsize=(12,5), facecolor='white')
plt.subplot(1, 2, 1)
perfplot.plot(
    setup=lambda n: pd.DataFrame([range(n+1)]),
    kernels=[lambda df: df.drop(columns=df.columns[0]), lambda df: df.loc[:, df.columns != df.columns[0]]],
    labels= ['drop', 'boolean indexing'],
    n_range=[2**k for k in range(21)],
    xlabel='Number of columns in a dataframe',
    title='Removing a single column from a dataframe',
    equality_check=pd.DataFrame.equals)

plt.subplot(1, 2, 2)
perfplot.plot(
    setup=lambda n: (pd.DataFrame([range(n+1)]), random.sample(range(n+1), k=(n+1)//2)),
    kernels=[lambda df,cols: df.drop(columns=cols), lambda df,cols: df.loc[:, ~df.columns.isin(cols)]],
    labels= ['drop', 'boolean indexing'],
    n_range=[2**k for k in range(21)],
    xlabel='Number of columns in a dataframe',
    title='Removing multiple columns from a dataframe',
    equality_check=pd.DataFrame.equals)

plt.tight_layout();