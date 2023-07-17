## Find and replace values in list

<sup>This is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/72923909/19123103).</sup>


#### Find and replace string values in a list

Suppose we have a list as follows.
```python
words = ['how', 'much', 'is[br]', 'the', 'fish[br]', 'no', 'really']
```
and we want to replace `[br]` with some `<br />` and thus getting a new list that looks like as follows.
```none
['how', 'much', 'is<br />', 'the', 'fish<br />', 'no', 'really']
```

In that case the canonical method is a list comprehension where the `str.replace()` is called in a loop.
```python
words = [w.replace('[br]', '<br />') for w in words]
```

If performance is important, including an `if-else` clause improves performance (by about 5% for a list of 1mil strings, no negligible really).
```python
replaced = [w.replace('[br]','<br />') if '[br]' in w else w for w in words]
```
`map()` implementation can be improved by calling `replace` via `operator.methodcaller()` (by about 20%) but still slower than list comprehension (as of Python 3.9).
```python
from operator import methodcaller
list(map(methodcaller('replace', '[br]', '<br />'), words))
```
If it suffices to modify the strings in-place, a loop implementation may be the fastest.
```python
for i, w in enumerate(words):
    if '[br]' in w:
        words[i] = w.replace('[br]', '<br />')
```