import pandas as pd
from pandasql import sqldf
from collections import ChainMap


###########################################################################
######################### NAMED AGGREGATION ###############################

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
##################### SUM, MEAN IN EACH GROUP #############################


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


###########################################################################
####################### SUM IN EACH GROUP #################################


x = df.groupby('dummy')[['A', 'B']].sum()
print(x)

x = df.groupby('dummy')[["A", "B"]].sum().add_suffix("_total")
print(x)

x = df.groupby("dummy", as_index=False)[['A', 'B']].sum()
print(x)


###########################################################################
################### TOPMOST N IN EACH GROUP ###############################

df = pd.DataFrame({'id':[1,1,1,2,2,2,2,3,4], 'value':[1,2,3,1,2,3,4,1,1]})
N = 2

x = df.groupby('id').head(N)
print(x)

df1 = df.groupby('id', as_index=False).nth[:N]
print(df1)

df2 = df.groupby('id', as_index=False).nth([0,2])
print(df2)


df1 = df.sort_values(by=['id', 'value'], ascending=[True, False])
df1 = df1.groupby('id', as_index=False).nth[:N]
print(df1)


msk = df.groupby('id')['value'].rank(method='first', ascending=False) <= N
df1 = df[msk]
print(df1)

y = df.loc[msk, 'value']
print(y)


