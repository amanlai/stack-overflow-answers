## How to convert a dictionary to a dataframe

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/75779669/19123103)./</sup>


#### How to set index while converting dictionary to dataframe

Suppose you have a dictionary such as the following:
```python
mydict = {
    'Open': ['47.47', '47.46', '47.38'],
   'Close': ['47.48', '47.45', '47.40'],
   'Date': ['2016/11/22 07:00:00', '2016/11/22 06:59:00','2016/11/22 06:58:00']
}
```
The question is, how do you set `Date` as the index upon dataframe construction.

The simplest answer is to simply call `set_index()`:
```python
df = pd.DataFrame(dictionary, columns=['Date', 'Open', 'Close']).set_index('Date')
```

If the original dictionary is not needed, then an alternative is to simply pop the `Date` key.
```python
df = pd.DataFrame(mydict, index=pd.Series(mydict.pop('Date'), name='Date'))
```
That said, I think `set_index` is the more convenient and less verbose option that can be called immediately on the newly created frame:
```python
df = pd.DataFrame(mydict).set_index('Date')
```
[![res][1]][1]


  [1]: https://i.stack.imgur.com/6BjHz.png