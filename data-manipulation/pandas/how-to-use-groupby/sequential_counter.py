import pandas as pd

df = pd.DataFrame(
    columns="c1    c2    v1 ".split(),
    data= [
            ["A",  "X",    3, ],
            ["A",  "X",    5, ],
            ["A",  "Y",    7, ],
            ["A",  "Y",    1, ],
            ["B",  "X",    3, ],
            ["B",  "X",    1, ],
            ["B",  "X",    3, ],
            ["B",  "Y",    1, ],
            ["C",  "X",    7, ],
            ["C",  "Y",    4, ],
            ["C",  "Y",    1, ],
            ["C",  "Y",    6, ]
])

df['counter'] = df.groupby(['c1', 'c2']).cumcount() + 1



df = pd.DataFrame(
    columns="  c1      c2    seq".split(),
    data= [
            [ "A",      1,    1 ],
            [ "A1",     0,    2 ],
            [ "A11",    0,    3 ],
            [ "A111",   0,    4 ],
            [ "B",      1,    1 ],
            [ "B1",     0,    2 ],
            [ "B111",   0,    3 ],
            [ "C",      1,    1 ],
            [ "C11",    0,    2 ] ])

# build a grouper Series for similar values
groups = df['c1'].str.contains("A$|B$|C$").cumsum()

# or build a grouper Series from flags (1s)
groups = df['c2'].eq(1).cumsum()

# groupby using the above grouper
df['seq'] = df.groupby(groups).cumcount().add(1)