import pandas as pd
import numpy as np
import timeit

df = pd.DataFrame([
    {'gender': 'male', 'pet1': 'dog', 'pet2': 'dog'}, 
    {'gender': 'male', 'pet1': 'cat', 'pet2': 'cat'}, 
    {'gender': 'male', 'pet1': 'dog', 'pet2': 'cat'},
    {'gender': 'female', 'pet1': 'cat', 'pet2': 'squirrel'},
    {'gender': 'female', 'pet1': 'dog', 'pet2': 'dog'},
    {'gender': 'female', 'pet1': 'squirrel', 'pet2': 'cat'},
    {'gender': 'squirrel', 'pet1': 'dog', 'pet2': 'cat'}
]*15_000)


np_where_eval = """np.where(df.eval("gender == 'male' and pet1 == pet2 or gender == 'female' and pet1 == ['cat','dog'] or gender == 'female' and pet2 == ['squirrel','dog'] or pet1 == 'cat' and pet2 == 'cat'"), 5, 0)"""

np_where = """np.where( ( (df['gender'] == 'male') & (df['pet1'] == df['pet2'] ) ) | ( (df['gender'] == 'female') & (df['pet1'].isin(['cat','dog'] ) ) ) | ( (df['gender'] == 'female') & (df['pet2'].isin(['squirrel','dog'] ) ) ) | ( (df['pet1'] == 'cat') & (df['pet2'] == 'cat') ), 5, 0)"""

np_select = """np.select([df['gender'].eq('male') & df['pet1'].eq(df['pet2']), df['gender'].eq('female') & df['pet1'].isin(['cat', 'dog']), df['gender'].eq('female') & df['pet2'].isin(['squirrel', 'dog']), df['pet1'].eq('cat') & df['pet2'].eq('cat')], [5,5,5,5], default=0)"""


t1 = min(timeit.repeat(np_where_eval, globals=globals(), number=100, repeat=10)) / 10   # 0.3692055799998343
t2 = min(timeit.repeat(np_where,      globals=globals(), number=100, repeat=10)) / 10   # 0.48299628000022493
t3 = min(timeit.repeat(np_select,     globals=globals(), number=100, repeat=10)) / 10   # 0.4258716299998923

print(t1)
print(t2)
print(t3)