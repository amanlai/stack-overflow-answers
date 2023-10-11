## Index names in Pandas

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/75807245/19123103).</sup>

##### 1. Use `pd.Index` to name an index (or column) from construction

Pandas has `Index` (`MultiIndex`) objects that accepts names. Passing those as index or column on dataframe construction constructs frames with named indices/columns.
```python
data = {'Column 1': [1,2,3,4], 'Index Title': ["Apples","Oranges","Puppies","Ducks"]}

# for RangeIndex
df = pd.DataFrame(data, index=pd.Index(range(4), name='foo'))
#                             ^^^^^^^^  <---- here

# for Index
df = pd.DataFrame(data, index=pd.Index(data['Index Title'], name='foo'))
#                             ^^^^^^^^  <---- here

# for columns
df = pd.DataFrame(data, columns=pd.Index(data.keys(), name='foo'))
#                               ^^^^^^^^  <---- here

# for MultiIndex
df = pd.DataFrame(data, index=pd.MultiIndex.from_arrays([['Fruit', 'Fruit', 'Animal', 'Animal'], data['Index Title']], names=['foo', 'bar']))
#                             ^^^^^^^^^^^^^  <---- here
```

##### 2. Change MultiIndex level name

If the dataframe has MultiIndex and an index name at a specific level has to be changed, `index.set_names` may be used. For example, to change the name of the second index level, use the following. Don't forget `inplace=True`.
```python
df.index.set_names('foo', level=1, inplace=True)

# equivalently, rename could be used with a dict
df.index.rename({'Index Title 2': 'foo'}, inplace=True)
```
[![res1][2]][2]

---

`set_names` can also be used for just regular index (set `level=None`). However, `rename_axis` is probably easier.

```python
df.index.set_names('foo', level=None, inplace=True)

# equivalent to the following
df.index.name = 'foo'
df = df.rename_axis('foo')
```
[![res2][3]][3]

---

There's a corresponding `columns.set_names` for columns.

```python
df.columns.set_names('foo', level=None, inplace=True)
# equivalent to 
df = df.rename_axis(columns='foo')

# for MultiIndex columns
df.columns.set_names('foo', level=0, inplace=True)
```
[![res3][4]][4]


  [1]: https://i.stack.imgur.com/naREK.png
  [2]: https://i.stack.imgur.com/uRpMq.png
  [3]: https://i.stack.imgur.com/Jqkm2.png
  [4]: https://i.stack.imgur.com/mRCFU.png