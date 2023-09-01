from profiler import profile


def try_index(a, b):
    c = []
    for x in a:
        try:
            c.append(b.index(x))
        except ValueError:
            c.append(-1)
    return c


def set_in(a, b):
    s = set(b)
    return [b.index(x) if x in s else -1 for x in a]


def dict_lookup(a, b):
    # for faster lookups, convert dict to a function beforehand
    reverse_lookup = {x:i for i, x in enumerate(b)}.get
    return [reverse_lookup(x, -1) for x in a]


methods = [try_index, set_in, dict_lookup]
fig = profile(methods)
fig.suptitle('Get index of values that exist in a list', fontsize=20)
fig.tight_layout();
fig.savefig('second_benchmark.png');