import pandas as pd
import io

txt = """
    A   B   C
0   foo 0   A
1   foo 1   A
2   foo 1   B
3   bar 1   A
"""

df = pd.read_csv(io.StringIO(txt), sep='\s+')


a = df.drop_duplicates(subset=['A', 'C'], keep=False)

b = df[~df.duplicated(subset=['A', 'C'], keep=False)].copy()

c = df[~( df.duplicated(subset=['A', 'B', 'C'], keep=False) & df['A'].eq('foo') )].copy()


# to consider all columns for identifying duplicates
x = df[~df.duplicated(subset=df.columns, keep=False)].copy()

# the same is true for drop_duplicates
y = df.drop_duplicates(subset=df.columns, keep=False)

# to consider columns in positions 0 and 2 (i.e. 'A' and 'C') for identifying duplicates
z = df.drop_duplicates(subset=df.columns[[0, 2]], keep=False)