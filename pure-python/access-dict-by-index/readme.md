## Accessing dictionary elements by index

<sup>This post is based on my answers to Stack Overflow questions that may be found [here](https://stackoverflow.com/a/72511703/19123103) and [here](https://stackoverflow.com/a/72511573/19123103)</sup>

#### Slice keys by index

If you need to slice dictionary keys (not just the first key), instead of calling `list()` on `test`, a generalized method of [Mark's answer](https://stackoverflow.com/a/27638751/19123103) is to use `islice` from the standard `itertools` module.

```python
from itertools import islice
test = {'foo': 'bar', 'hello': 'world'}
# slice test.keys from index l to index u
some_keys = list(islice(test, l, u))
```
Depending on the size of the slice relative to the size of the dictionary, this method is 50% to >40000x faster than
```python
list(test)[l:u]
```

For example, in the example that may be found on [this repo](./timeit_test.py), it's >43000x faster.


For completeness, for the first index `next()` may be used.
```python
next(iter(test))
```


#### Slice values by index


As mentioned above, creating a new list using `list()` constructor, only to slice it is wasteful. Using `itertools.islice` is more efficient.

```python
from itertools import islice
dct = {'A':1, 'B':2, 'C':3, 'D':4}
arr = dct.values()
the_sum = sum(islice(arr, 1, 3))
the_sum                             # 5
```
The difference is efficiency is noticeable especially if the dictionary is very large but the slice is small relative to it. For example, for a dictionary of 10mil key-value pairs, if you're slicing 20 pairs and summing their values, `islice` is ~39400x faster than constructing a list and slicing it.