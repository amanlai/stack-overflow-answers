import pandas as pd
import perfplot
import matplotlib.pyplot as plt

constructor = lambda n: pd.DataFrame({'A': 'foo bar foo baz foo bar foo foo'.split()*n, 'B': np.random.rand(8*n)})

fig, axs = plt.subplots(1, 2, figsize=(20, 5), facecolor='white')
plt.sca(axs[0])
perfplot.plot(
    setup=constructor,
    kernels=[lambda df: df[(df.B%5)**2<0.1], lambda df: df.query("(B%5)**2<0.1")],
    labels= ['df[(df.B % 5) **2 < 0.1]', 'df.query("(B % 5) **2 < 0.1")'],
    n_range=[2**k for k in range(4, 24)],
    xlabel='Rows in DataFrame',
    title='Multiple mathematical operations on numbers',
    equality_check=pd.DataFrame.equals);
plt.sca(axs[1])
perfplot.plot(
    setup=constructor,
    kernels=[lambda df: df[df.A == 'foo'], lambda df: df.query("A == 'foo'")],
    labels= ["df[df.A == 'foo']", """df.query("A == 'foo'")"""],
    n_range=[2**k for k in range(4, 24)],
    xlabel='Rows in DataFrame',
    title='Comparison operation on strings',
    equality_check=pd.DataFrame.equals);