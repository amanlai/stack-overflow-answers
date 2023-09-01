import io
import numpy as np
import pandas as pd

txt1 = """
Date        Apples      Pears      Grapes
01/01/22      10         47          0
02/01/22      0          22          3
03/01/22      11         0           3
"""

txt2 = """
Parameter   Apples   Pears   Grapes
    alpha      132     323       56
     beta      424      31       33
    theta       13     244      323
"""


spend_df = pd.read_csv(io.StringIO(txt1), sep='\s+')
parameters_df = pd.read_csv(io.StringIO(txt2), sep='\s+')


# extract alpha, beta, theta from parameters df
alpha, beta, theta = parameters_df.iloc[:, 1:].values
# select fruit columns
current = spend_df[['Apples', 'Pears', 'Grapes']]
# find previous values of fruit columns
previous = current.shift(fill_value=0)

# calculate profit using formula
y = beta*(1 - np.exp(-(theta*previous + current) / alpha))
profit_df = spend_df[['Date']].join(y)