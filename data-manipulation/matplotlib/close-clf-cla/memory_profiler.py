import os
import tracemalloc
import matplotlib.pyplot as plt

def close(n):
    for i in range(n):
        fig = plt.figure(facecolor='white', figsize=(6,3), dpi=36)
        ax = fig.add_subplot()
        ax.plot([100, 0, i])
        fig.savefig(f'{i}.png')
        plt.close(fig)


def cla(n):
    fig = plt.figure(facecolor='white', figsize=(6,3), dpi=36)
    ax = fig.add_subplot()
    for i in range(n):
        ax.plot([100, 0, i])
        fig.savefig(f'{i}.png')
        ax.cla()


def clf(n):
    fig = plt.figure(facecolor='white', figsize=(6,3), dpi=36)
    for i in range(n):
        ax = fig.add_subplot()
        ax.plot([100, 0, i])
        fig.savefig(f'{i}.png')
        fig.clf()


def cla_wrong(n):
    for i in range(n):
        fig = plt.figure(facecolor='white', figsize=(6,3), dpi=36)
        ax = fig.add_subplot()
        ax.plot([100, 0, i])
        fig.savefig(f'{i}.png')
        ax.cla()


def clf_wrong(n):
    for i in range(n):
        fig = plt.figure(facecolor='white', figsize=(6,3), dpi=36)
        ax = fig.add_subplot()
        ax.plot([100, 0, i])
        fig.savefig(f'{i}.png')
        fig.clf()


if __name__ == '__main__':
    
    for func in (close, cla, clf, clf_wrong, cla_wrong):
        tracemalloc.start()
        func(100)
        size, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        # delete the saved image files
        for f in os.listdir():
            if f.endswith('.png'):
                os.remove(f)
        print(f"{func.__name__}:\ncurrent memory usage is {size/1024:,.0f} KB; \
peak was {peak/1024:,.0f} KB.")
        print("======================================================")