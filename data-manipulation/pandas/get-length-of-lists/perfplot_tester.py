import pandas as pd
import random
import string 
import perfplot
import matplotlib.pyplot as plt

random.seed(365)

def f1(ser):
    return ser.str.len()

def f2(ser):
    return ser.map(len)

def f3(ser):
    return list(map(len, ser.tolist()))

def f4(ser):
    return [len(x) for x in ser]


plt.figure(figsize=(9,5), facecolor='white')
perfplot.plot(
    setup=lambda n: pd.Series([random.sample(string.ascii_letters, random.randint(1, 20)) for _ in range(n)]),
    kernels=[f1, f2, f3, f4],
    labels=["ser.str.len()", "ser.map(len)", "list(map(len, ser.tolist()))", "[len(x) for x in ser]"],
    n_range=[2**k for k in range(21)],
    xlabel='Length of dataframe',
    equality_check=lambda x,y: x.eq(y).all()
)
ax = plt.gca()
xticks = ax.get_xticks()[:-1]
ax.set_xticks(xticks, [f"{int(x):,}" for x in xticks]);
