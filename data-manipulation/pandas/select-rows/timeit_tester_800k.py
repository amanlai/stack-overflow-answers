import timeit
import pandas as pd
import numpy as np

df = pd.DataFrame({'A': 'foo bar foo baz foo bar foo foo'.split()*100000, 
                   'B': np.random.rand(800000)})



t1 = np.mean(
    timeit.repeat(
        """df[df.A == 'foo']""", 
        globals=globals(), repeat=7, number=100)
)   # 87.9 ms

t2 = np.mean(
    timeit.repeat(
        """df.query("A == 'foo'")""", 
        globals=globals(), repeat=7, number=100)
)   # 54.4 ms

print(t1, t2)

######################################################

t3 = np.mean(
    timeit.repeat(
        """df[((df.A == 'foo') & (df.A != 'bar')) | ((df.A != 'baz') & (df.A != 'buz'))]""", 
        globals=globals(), repeat=7, number=100)
)   # 310 ms

t4 = np.mean(
    timeit.repeat(
        """df.query("A == 'foo' & A != 'bar' | A != 'baz' & A != 'buz'")""", 
        globals=globals(), repeat=7, number=100)
)   # 132 ms

print(t3, t4)

######################################################

t5 = np.mean(
    timeit.repeat(
        """df[(df.B % 5) **2 < 0.1]""", 
        globals=globals(), repeat=7, number=100)
)   # 54 ms

t6 = np.mean(
    timeit.repeat(
        """df.query("(B % 5) **2 < 0.1")""", 
        globals=globals(), repeat=7, number=100)
)   # 26.3 ms

print(t5, t6)