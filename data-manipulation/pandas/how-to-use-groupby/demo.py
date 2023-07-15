import pandas as pd
from pandasql import sqldf

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