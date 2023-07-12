import timeit
import numpy as np
import pandas as pd

df = pd.DataFrame({'A': 'foo bar foo baz foo bar foo foo'.split()*10000, 
                   'B': np.random.rand(80000)})


t1 = np.mean(timeit.repeat("""df[df.A == 'foo']""", globals=globals(), repeat=7, number=100))        # 8.5 ms
t2 = np.mean(timeit.repeat("""df.query("A == 'foo'")""", globals=globals(), repeat=7, number=100))   # 6.36 ms
print(t1, t2)


t3 = np.mean(
    timeit.repeat(
        """df[((df.A == 'foo') & (df.A != 'bar')) | ((df.A != 'baz') & (df.A != 'buz'))]""", 
        globals=globals(), repeat=7, number=100)
)   # 29 ms

t4 = np.mean(
    timeit.repeat(
        """df.query("A == 'foo' & A != 'bar' | A != 'baz' & A != 'buz'")""", 
        globals=globals(), repeat=7, number=100)
)   # 16 ms

print(t3, t4)



t5 = np.mean(
    timeit.repeat(
        """df[(df.B % 5) **2 < 0.1]""", 
        globals=globals(), repeat=7, number=100)
)   # 5.35 ms

t6 = np.mean(
    timeit.repeat(
        """df.query("(B % 5) **2 < 0.1")""", 
        globals=globals(), repeat=7, number=100)
)   # 4.37 ms

print(t5, t6)