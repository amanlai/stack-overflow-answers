import pandas as pd
import perfplot
import matplotlib.pyplot as plt

kernels = [lambda s: list(s), lambda s: s.tolist()]
labels = ['list()', '.tolist()']
n_range = [2**k for k in range(4, 20)]
xlabel = 'Rows in DataFrame'
eq_chk = lambda x,y: all([x,y])

numeric = lambda n: pd.Series(range(5)).repeat(n)
string = lambda n: pd.Series(['some word', 'another word', 'a word']).repeat(n)
datetime = lambda n: pd.to_datetime(pd.Series(['2012-05-14', '2046-12-31'])).repeat(n)
timedelta = lambda n: pd.to_timedelta(pd.Series([1,2]), unit='D').repeat(n)
categorical = lambda n: pd.Series(pd.Categorical([1, 2, 3, 1, 2, 3])).repeat(n)

fig, axs = plt.subplots(3, 2, figsize=(15, 15), facecolor='white')

for i, lst in enumerate([[('Numeric', numeric), ('Object dtype', string)],
                      [('Datetime', datetime), ('Timedelta', timedelta)], 
                      [('Categorical', categorical), (None,)]]):
    for j, (n, f) in enumerate(lst):
        plt.sca(axs[i, j])
        if n is not None:
            perfplot.plot(setup=f, kernels=kernels, labels=labels, n_range=n_range, 
                          xlabel=xlabel, title=f'{n} column', equality_check=eq_chk);
        else:
            axs[i, j].set_axis_off()

fig.savefig('perfplot_test.png')