## How to plot boxplots

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/75774057/19123103).</sup>

#### Create multiple boxplots using a dictionary

`labels=` parameter can be used to set x-axis labels in one function call.
```python
my_dict = {'ABC': [34.54, 34.345, 34.761], 'DEF': [34.541, 34.748, 34.482]}
plt.boxplot(my_dict.values(), labels=my_dict.keys());
```
If it were a pandas dataframe, the labels are also applied automatically.
```python
df = pd.DataFrame(my_dict)
df.plot(kind='box');
```
[![result][1]][1]


  [1]: https://i.stack.imgur.com/d2oEB.png