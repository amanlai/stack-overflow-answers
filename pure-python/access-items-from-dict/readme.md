## Get keys or values from a dictionary

<sup>This post is based on my answers to Stack Overflow questions that may be found at [1](https://stackoverflow.com/a/72511703/19123103), [2](https://stackoverflow.com/a/72511573/19123103) and [3](https://stackoverflow.com/a/72930789/19123103).</sup>

### Get list of values

`dict.values()` returns a view of a dictionary's values, so to copy it into a list, `list()` must be called.
```python
list(d.values())
```

If you need to assign the values as a list to a variable, another method using the unpacking `*` operator is
```python
*values, = d.values()
```

#### a. Get a list of values of specific keys in a dictionary

Most straightforward way is to use a comprehension by iterating over `list_of_keys`. If `list_of_keys` includes keys that are not keys of `d`, `.get()` method may be used to return a default value (`None` by default but can be changed).
```python
res = [d[k] for k in list_of_keys] 
# or
res = [d.get(k) for k in list_of_keys]
```
As often the case, there's a method built into Python that can get the values under keys: `itemgetter()` from the built-in `operator` module.
```python
from operator import itemgetter
res = list(itemgetter(*list_of_keys)(d))
```
Demonstration:
```python
d = {'a':2, 'b':4, 'c':7}
list_of_keys = ['a','c']
print([d.get(k) for k in list_of_keys])
print(list(itemgetter(*list_of_keys)(d)))
# [2, 7]
# [2, 7]
```

#### b. Get values of the same key from a list of dictionaries

Again, a comprehension works here (iterating over list of dictionaries). As does mapping `itemgetter()` over the list to get the values of specific key(s).
```python
list_of_dicts = [ {"title": "A", "body": "AA"}, {"title": "B", "body": "BB"} ]

list_comp = [d['title'] for d in list_of_dicts]
itmgetter = list(map(itemgetter('title'), list_of_dicts))
print(list_comp)
print(itmgetter)
# ['A', 'B']
# ['A', 'B']
```


### Accessing dictionary elements by index

#### a. Slice keys by index

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


#### b. Slice values by index


As mentioned above, creating a new list using `list()` constructor, only to slice it is wasteful. Using `itertools.islice` is more efficient.

```python
from itertools import islice
dct = {'A':1, 'B':2, 'C':3, 'D':4}
arr = dct.values()
the_sum = sum(islice(arr, 1, 3))
the_sum                             # 5
```
The difference is efficiency is noticeable especially if the dictionary is very large but the slice is small relative to it. For example, for a dictionary of 10mil key-value pairs, if you're slicing 20 pairs and summing their values, `islice` is ~39400x faster than constructing a list and slicing it.