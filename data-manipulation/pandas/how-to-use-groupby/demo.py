import pandas as pd
from pandasql import sqldf
from collections import ChainMap

my_dict = {
    'Fruit': ['Apples', 'Apples', 'Apples', 'Apples', 'Apples', 'Oranges', 'Oranges', 'Oranges', 'Oranges', 'Oranges', 'Grapes', 'Grapes', 'Grapes', 'Grapes', 'Grapes'], 'Date': ['10/6/2016', '10/6/2016', '10/6/2016', '10/7/2016', '10/7/2016', '10/7/2016', '10/6/2016', '10/6/2016', '10/6/2016', '10/7/2016', '10/7/2016', '10/7/2016', '10/7/2016', '10/7/2016', '10/7/2016'], 
    'Name': ['Bob', 'Bob', 'Mike', 'Steve', 'Bob', 'Bob', 'Tom', 'Mike', 'Bob', 'Tony', 'Bob', 'Tom', 'Bob', 'Bob', 'Tony'], 
    'Number': [7, 8, 9, 10, 1, 2, 15, 57, 65, 1, 1, 87, 22, 12, 15]
}
df = pd.DataFrame(my_dict)

x = df.groupby(['Fruit','Name']).sum()
print(x)


y1 = df.groupby(['Fruit', 'Name'], as_index=False).agg(**{'Total Number': ('Number', 'sum')})
print(y1)
y2 = df.groupby(['Fruit', 'Name'], as_index=False).agg(Total=('Number', 'sum'))
print(y2)


z = sqldf("""
SELECT Fruit, Name, sum(Number) AS Total
FROM df 
GROUP BY Fruit, Name
"""
)
print(z)


###########################################################################


df = pd.DataFrame({'dummy': [0, 1, 1], 'A': range(3), 'B':range(1, 4), 'C':range(2, 5)})

# with default names
x = df.groupby('dummy')['B'].agg(['mean', 'sum'])
print(x)

# using named aggregation
y = df.groupby('dummy').agg(Mean=('B', 'mean'), Sum=('B', 'sum'))
print(y)

z = df.groupby("dummy").agg({k: ['sum', 'mean'] for k in ['A', 'B', 'C']})
print(z)


# convert a list of dictionaries into a dictionary
dct = dict(ChainMap(*reversed([{f'{k}_total': (k, 'sum'), f'{k}_mean': (k, 'mean')} for k in ['A','B','C']])))

dct = {k:v for k in ['A','B','C'] for k,v in [(f'{k}_total', (k, 'sum')), (f'{k}_avg', (k, 'mean'))]}

# aggregation
z2 = df.groupby('dummy', as_index=False).agg(**dct)
print(z2)