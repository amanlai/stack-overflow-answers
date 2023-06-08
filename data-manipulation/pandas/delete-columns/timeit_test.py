from timeit import timeit
setup = "import pandas as pd; df=pd.DataFrame([range(10000)])"

for _ in range(3):
    t1 = timeit("df = df.drop(columns=df.columns[0])", setup, number=10000)
    t2 = timeit("del df[df.columns[0]]", setup, number=10000)
    print(f"{t2/t1:.2f}")
    
# 37.40
# 37.45
# 37.34