import pandas as pd
import io

data = """
id    val1     val2
 1     1.1      2.2
 1     1.1      2.2
 2     2.1      5.5
 3     8.8      6.2
 4     1.1      2.2
 5     8.8      6.2
"""

df = pd.read_csv(io.StringIO(data), sep='\s\s+', engine='python')
msk = df.groupby(['val1', 'val2'])['val1'].transform('size') > 1
df1 = df[msk]