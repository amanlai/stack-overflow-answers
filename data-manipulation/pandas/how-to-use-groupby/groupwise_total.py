import pandas as pd

my_dict = {
    'Fruit': ['Apples', 'Apples', 'Apples', 'Apples', 'Apples', 'Oranges', 'Oranges', 'Oranges', 'Oranges', 'Oranges', 'Grapes', 'Grapes', 'Grapes', 'Grapes', 'Grapes'], 
    'Date': ['10/6/2016', '10/6/2016', '10/6/2016', '10/7/2016', '10/7/2016', '10/7/2016', '10/6/2016', '10/6/2016', '10/6/2016', '10/7/2016', '10/7/2016', '10/7/2016', '10/7/2016', '10/7/2016', '10/7/2016'], 
    'Name': ['Bob', 'Bob', 'Mike', 'Steve', 'Bob', 'Bob', 'Tom', 'Mike', 'Bob', 'Tony', 'Bob', 'Tom', 'Bob', 'Bob', 'Tony'], 
    'Number': [7, 8, 9, 10, 1, 2, 15, 57, 65, 1, 1, 87, 22, 12, 15]
}
df1 = pd.DataFrame(my_dict)

df = pd.DataFrame({
    'dummy': [0, 1, 1], 
    'A': range(3), 
    'B': range(1, 4), 
    'C': range(2, 5)
})



x1 = df1.groupby(['Fruit','Name']).sum()



x1 = df.groupby('dummy')[['A', 'B']].sum()

x2 = df.groupby('dummy')[["A", "B"]].sum().add_suffix("_total")

x3 = df.groupby("dummy", as_index=False)[['A', 'B']].sum()
