from random import sample
from timeit import repeat
from functools import partial
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

def profile(methods):
    sizes = range(1, 31, 2)
    colors = ['r', 'b', 'g']
    Ns = [100, 1000000]
    fig, axs = plt.subplots(1, len(Ns), figsize=(10, 4), facecolor='white')
    for N, ax in zip(Ns, axs):
        b = sample(range(N), k=N)
        times = {f.__name__: [] for f in methods}
        for size in sizes:
            a = sample(range(len(b)*3//2), k=size)
            for label, f in zip(times, methods):
                func = partial(f, a, b)
                times[label].append(min(repeat(func, number=10))/10)
        for (k, ts), c in zip(times.items(), colors):
            ax.plot(sizes, ts, f'{c}o-', label=k)
        ax.set_title(f'List size = {N:,d}', fontsize=18)
        ax.set_xlabel('Number of values to check', fontsize=14)
        ax.set_ylabel('Runtime', fontsize=14)
        ax.xaxis.set_major_locator(MultipleLocator(5))
        ax.legend()
    return fig