## Apply function to each element of a list

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/75227292/19123103).</sup>

Say, we want to make each element in a list of strings uppercase, i.e.

```none
['this is test', 'another test']   --> ['THIS IS TEST', 'ANOTHER TEST']
```
How do we make this conversion?

---

String methods in Python are optimized, so you'll find that loop implementations such as
```python
mylis = ['this is test', 'another test']

newlis1 = [item.upper() for item in mylis]

newlis2 = list(map(str.upper, mylis))
```
to be faster than vectorized methods in other libraries such as pandas and numpy that perform the same task.

In general, you can apply a function to every element in a list using a list comprehension or `map()` as mentioned in other answers here. For example, given an arbitrary function `func`, you can either do:
```python
new_list = [func(x) for x in mylis]
# or 
new_list = list(map(func, mylis))
```

If you want to **modify a list in-place**, you can replace every element by a slice assignment.
```python
# note that you don't need to cast `map` to a list for this assignment
# this is probably the fastest way to apply a function to a list 
mylis[:] = map(str.upper, mylis)
# or
mylis[:] = [x.upper() for x in mylis]
```
or with an explicit loop:
```python
for i in range(len(mylis)):
    mylis[i] = mylis[i].upper()
```

You can also check out the built-in [itertools][3] and [operator][4] libraries for built-in methods to construct a function to apply to each element. For example, if you want to multiply each element in a list by 2, you can use `itertools.repeat` and `operator.mul`:
```python
from itertools import repeat, starmap
from operator import mul

newlis1 = list(map(mul, mylis, repeat(2)))
# or with starmap
newlis2 = list(starmap(mul, zip(mylis, repeat(2))))

# but at this point, list comprehension is simpler imo
newlis3 = [x*2 for x in mylis]
```


  [3]: https://docs.python.org/3/library/itertools.html
  [4]: https://docs.python.org/3/library/operator.html