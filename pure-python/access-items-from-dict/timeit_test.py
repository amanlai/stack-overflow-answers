import timeit

setup = """
from itertools import islice
n = 10_000_000
test = dict(zip(range(n), [0,1,2,3,4]*(n//5)))
"""

t1 = min(timeit.repeat("list(islice(test, 10, 30))", setup, repeat=7, number=100))
t2 = min(timeit.repeat("list(test)[10:30]", setup, repeat=7, number=100))
print(t1/t2)         # 43340.85778781038


#######################################################################


# small slice
t3 = min(timeit.repeat("sum(list(dct.values())[10:30])", setup, repeat=7, number=100))
t4 = min(timeit.repeat("sum(islice(dct.values(), 10, 30))", setup, repeat=7, number=100))
print(t3/t4)         # 39473.68421052631


# large slice
t5 = min(timeit.repeat("sum(list(dct.values())[1:n])", setup, repeat=7, number=100))
t6 = min(timeit.repeat("sum(islice(dct.values(), 1, n))", setup, repeat=7, number=100))
print(t5/t6)         # 1.5303867403314917