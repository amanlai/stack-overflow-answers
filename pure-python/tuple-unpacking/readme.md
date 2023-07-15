## Tuple unpacking in a comprehension

<sup> This is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/72916302/19123103). </sup>

> How to convert a string of the form `'A=5, b=7'` into a dict of the form `{'A': 5, 'b': 7}` in a dictionary comprehension?

[Since Python 3.8](https://docs.python.org/3/whatsnew/3.8.html#assignment-expressions), you can use walrus operator (`:=`) for this kind of operation. It allows to assign variables in the middle of expressions (in this case, assign the list created by `.split('=')` to `kv`).
```python
s = 'A=5, b=7'
{(kv := item.split('='))[0]: int(kv[1]) for item in s.split(', ')}
# {'A': 5, 'b': 7}
```
One feature is that it leaks the assigned variable, `kv`, outside the scope it was defined in. If you want to avoid that, you can use a nested for-loop where the inner loop is over a singleton list (as suggested in mgilson's answer).
```python
{k: int(v) for item in s.split(', ') for k,v in [item.split('=')]}
```
[Since Python 3.9](https://docs.python.org/3/whatsnew/3.9.html#optimizations), loops over singleton lists are optimized to be as fast as simple assignments, i.e. `y in [expr]` is as fast as `y = expr`.