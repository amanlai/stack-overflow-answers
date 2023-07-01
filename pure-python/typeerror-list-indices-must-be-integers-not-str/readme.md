This post was first used to answer [this](https://stackoverflow.com/q/32554527/19123103) Stack Overflow question.

## How to solve `TypeError: list indices must be integers or slices, not str`?

As the message says, this error occurs when a string is used to index a list. _Most_ of the cases leading to this error can be summarized in the following cases.

### 1. A list is used as if it were a dictionary

#### 1.1. Index a list as if it was a dictionary

This case commonly occurs when a json object is converted into a Python object but there's a dictionary nested inside a list. It is especially annoying (and easy to overlook) if the list has a single dictionary inside it. In the example below, the value under the `'summary'` key is a list than contains a single dictionary. So if one tries to get the home score using `json['summary']['home_score']`, it will show an error. 

```python
json = {
    "teams": {"home": "BOS", "away": "MIA"},
    "summary": [
        {"home_score": 0, "away_score": 0}
    ]
}

json['summary']['home_score']               # <---- TypeError: list indices must be integers or slices, not str
json['summary'][0]['home_score']            # <---- OK (returns the first item)
#              ^^^   <---- index the list here
[d['home_score'] for d in json['summary']]  # <---- OK (returns a list)
```

When making a http request, an API call, etc. the outcome is usually very nested and it's not very obvious how to handle that data but with a simple debugging step such as printing the type, length etc. of the data usually shows how to handle it.

```python
print(type(json['summary']))                # <class 'list'>    <---- check the data type
print(len(json['summary']))                 #                   <---- check length of data
print(type(json['summary'][0]))             # <class 'dict'>    <---- check type of item
```

#### 1.2. Assign values to a list as if it were a dictionary

Another common mistake is to initialize a list but try to assign values to it using a key. The initialization probably happened dynamically and it's not clear later on that it's in fact a list. For example, in the following case, `d` is initialized as a list but there's an attempt to add a key-value pair to it. A solution is to initialize an empty dict `{}` instead of `[]`.

```python
d = []
d['key'] = 1                                # <---- TypeError


d = {}
d['key'] = 1                                # <---- OK
```

#### 1.3. A pandas dataframe is accidentally changed into a list

A common way to change column labels of a pandas dataframe is to directly assign a list of strings intended to be the new labels to `pd.DataFrame.columns` attribute. If it's assigned to `pd.DataFrame` instead, the entire dataframe gets replaced by a list and it's not possible to access a column by label anymore.

```python
import pandas as pd
df = pd.DataFrame([range(4), range(4)])
df = ['A', 'B', 'C', 'D']
df['A']                                     # <---- TypeError


df = pd.DataFrame([range(4), range(4)])
df.columns = ['A', 'B', 'C', 'D']
# ^^^^^^^^  <---- assign column labels here
df['A']                                     # <---- OK
```


### 2. A string is used as if it were an integer

#### 2.1. Index a list using an `input()`

A very common mistake is when one tries to index a list using a value from a user input. Because `input()` returns a string, it has to be converted into an integer before being used to index a list.
   
```python
lst = ['a', 'b', 'c']
index = input()

lst[index]                                  # <---- TypeError: list indices must be integers or slices, not str
lst[int(index)]                             # <---- OK
```

#### 2.2. Using a list of strings to index a list

Another common mistake is to loop over a list and use a list item to index a list. Python's `for` is similar to Perl's `foreach` in the sense that the loop is over a collection of items. Since the list is already being iterated over, there's no need to index it again, so a solution is to use the item directly for whatever operation that needs to be done with it. Or perhaps loop over a `range` object that constructed using the length of the list.

```python
lst = ['a', 'b', 'a', 'd']

lst['a']                                    # <---- TypeError
lst[lst.index('a')]                         # <---- OK
```

This error probably happens much more often in a loop where `lst` was created dynamically.
```python
for i in lst:
    if lst[i] == 'b':                       # <---- TypeError
        pass

for i in lst:
    if i == 'b':                            # <---- OK
        pass
    
for i in range(len(lst)):                   # <---- OK
    if lst[i] == 'b':
        pass
```
N.B. This is OP's case. A for-loop over a string uses a string to index a list. The solution is to loop over a range object.