from profiler import profile


def list_in(a, b):
    return [x in b for x in a]


def set_in(a, b):
    s = set(b)
    return [x in s for x in a]


methods = [list_in, set_in]
fig = profile(methods)
fig.tight_layout();
fig.savefig('first_figure.png')