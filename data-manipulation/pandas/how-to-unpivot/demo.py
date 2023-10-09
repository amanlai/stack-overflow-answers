import io
import pandas as pd

data = """
   2014  2015  farm  fruit
0    10    11     A  apple
1    12    13     B  apple
2     6     7     A   pear
3     8     9     B   pear
"""

df = pd.read_csv(io.StringIO(data), sep='\s\s+', engine='python')

df1 = df.melt(id_vars=['farm', 'fruit'], var_name='year', value_name='value')

df2 = df.set_index(['farm', 'fruit']).rename_axis(columns='year').stack().reset_index(name='value')

df3 = pd.wide_to_long(df, 'value', i=['farm', 'fruit'], j='year', sep='_').reset_index()