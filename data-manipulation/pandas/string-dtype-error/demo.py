import pandas as pd

df = pd.DataFrame({'value': ['A', 'B', 'A', 'C']}, dtype='string')
df["value"] = df["value"].replace({"A": 0, "B": 1})               # <------ error

df["value"] = df["value"].replace({"A": '0', "B": '1'})           # <------ no error

df1 = pd.DataFrame({'value': ['A', 'B', 'A', 'C']}, dtype=object)
df1["value"] = df1["value"].replace({"A": 0, "B": 1})             # <------ no error

print(df['value'].tolist())         # ['0', '1', '0', 'C']         <------ all strings
print(df1['value'].tolist())        # [0, 1, 0, 'C']               <------ integers and strings 