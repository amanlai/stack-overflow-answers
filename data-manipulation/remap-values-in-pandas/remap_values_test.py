import numpy as np
import pandas as pd
from perfplot import plot
import matplotlib.pyplot as plt


# Code used to produce the plots

kernels = [lambda df, di: df['col1'].replace(di), 
           lambda df, di: df['col1'].map(di).fillna(df['col1'])]
labels = ["replace", "map+fillna"]


# first plot
N, m = 100000, 20
plot(
    setup=lambda n: (pd.DataFrame({'col1': np.resize(np.arange(m*n), N)}), 
                     {k: (k+1)/2 for k in range(n)}),
    kernels=kernels, labels=labels,
    n_range=range(1, 21),
    xlabel='Length of replacement dictionary',
    title=f'Remapping values in a column (len(df)={N:,}, {100//m}% replaced)',
    equality_check=pd.Series.equals)
_, xmax = plt.xlim()
plt.xlim((0.5, xmax+1))
plt.xticks(np.arange(1, xmax+1, 2));


# second plot
N, m = 100000, 1000
di = {k: (k+1)/2 for k in range(m)}
plot(
    setup=lambda n: pd.DataFrame({'col1': np.resize(np.arange((n-100)*m//100, n*m//100), N)}),
    kernels=kernels, labels=labels,
    n_range=[1, 5, 10, 15, 25, 40, 55, 75, 100],
    xlabel='Percentage of values replaced',
    title=f'Remapping values in a column (len(df)={N:,}, len(di)={m})',
    equality_check=pd.Series.equals);


# third plot
m, n = 10, 0.01
di = {k: (k+1)/2 for k in range(m)}
plot(
    setup=lambda N: pd.DataFrame({'col1': np.resize(np.arange((n-1)*m, n*m), N)}),
    kernels=kernels, labels=labels,
    n_range=[2**k for k in range(6, 21)], 
    xlabel='Length of dataframe',
    logy=False,
    title=f'Remapping values in a column (len(di)={m}, {int(n*100)}% replaced)',
    equality_check=pd.Series.equals);

# fourth plot
m, n = 100, 0.01
di = {k: (k+1)/2 for k in range(m)}
plot(
    setup=lambda N: pd.DataFrame({'col1': np.resize(np.arange((n-1)*m, n*m), N)}),
    kernels=kernels, labels=labels,
    n_range=[2**k for k in range(6, 21)], 
    xlabel='Length of dataframe',
    title=f'Remapping values in a column (len(di)={m}, {int(n*100)}% replaced)',
    equality_check=pd.Series.equals);