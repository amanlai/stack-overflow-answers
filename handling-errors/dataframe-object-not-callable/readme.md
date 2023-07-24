## TypeError: 'DataFrame' object is not callable

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/73603754/19123103).</sup>


This error occurs when you call a pandas DataFrame object - use round `()` brackets - as if it were a class or a function. An example where this may appear is as follows.
```python
import pandas as pd
import numpy as np

credit_card = pd.read_csv("default_of_credit_card_clients_Data.csv", skiprows=1)
    
for col in credit_card:
    var[col] = np.var(credit_card(col))
```

Long story short, pandas DataFrames are objects of type 'DataFrame' whose attribute that makes an object callable is null.

For example, in the example above, the culprit is:
```python
credit_card(col)
```
because previously, `credit_card` was defined to be a pandas DataFrame object via 
```python
credit_card = pd.read_csv("default_of_credit_card_clients_Data.csv", skiprows=1)
```
The most common way to define a dataframe is via the constructor `df = pd.DataFrame(data)` and this `df` cannot be called either: `df()` would give the same error. The list of other functions that construct a dataframe object can be found in the [pandas documentation](https://pandas.pydata.org/docs/reference/io.html).

---

This problem is essentially a typo. Here are some common causes/solutions: 

1. Perhaps you were trying to select some columns of the dataframe, in which case, use the square `[]` brackets:
   ```python
   credit_card[col]                # e.g. credit_card['colA'] or credit_card[['colA']]
   ```
2. Perhaps you were trying to call a dataframe method, in which case, write the method's name after the dataframe's name, separated by a dot `.`:
   ```python
   credit_card.some_method(col)    # e.g. credit_card.value_counts('colA')
   ```
3. Perhaps you have a function and a dataframe sharing the same name in your environment. For example,
   ```python
   credit_card = lambda x: x + 1
   credit_card = pd.DataFrame(data)
   ```
   In that case, make sure to re-define them using different names.