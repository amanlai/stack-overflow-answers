## How to sort a list

<sup>This post is based on my answer to a Stack Overflow question that may be found at 
[1](https://stackoverflow.com/a/75326812/19123103),
[2](https://stackoverflow.com/a/75760120/19123103).</sup>

### How to sort a list of datetime objects

You can use either of `list.sort()` (which sorts in-place) or `sorted()` (which creates a new copy).

```python
lst.sort()                # now `lst` is sorted in ascending order

sorted_lst = sorted(lst)  # a brand new sorted list is created
```

---

If your list contains a list of **strings that look like datetime**, you can sort them using a datetime parser as key.

For example, to sort `lst`, you can pass a lambda that parses each string into datetime as key (for a full list of possible formats, see https://strftime.org/).
```python
from datetime import datetime, date
lst = ['02/01/2023 12:25 PM', '01/22/2023 11:00 PM', '12/01/2022 02:23 AM']
sorted_lst = sorted(lst, key=lambda x: datetime.strptime(x, '%m/%d/%Y %I:%M %p'))
# ['12/01/2022 02:23 AM', '01/22/2023 11:00 PM', '02/01/2023 12:25 PM']

# in-place sorting is also possible
lst.sort(key=lambda x: datetime.strptime(x, '%m/%d/%Y %I:%M %p'))
```
Of course, you can parse them into datetime first and then sort but that would change the type of the items in the list from 
```python
new_lst = sorted(datetime.strptime(x, '%m/%d/%Y %I:%M %p') for x in lst)
# [datetime.datetime(2022, 12, 1, 2, 23), datetime.datetime(2023, 1, 22, 23, 0), datetime.datetime(2023, 2, 1, 12, 25)]
```
If your list is a **mixture of date and datetimes**, you can normalize them all into datetime objects, and then sort; again, as a key so that the type of the items in the original list doesn't change.
```python
lst = [datetime(2013, 1, 21, 6, 14, 47), date(2013, 1, 22), date(2013, 1, 21)]
new_lst = sorted(lst, key=lambda x: x if isinstance(x, datetime) else datetime(x.year, x.month, x.day))
# [datetime.date(2013, 1, 21), datetime.datetime(2013, 1, 21, 6, 14, 47), datetime.date(2013, 1, 22)]
```


### Sort in descending order

Especially if the data is numeric, negation can be used to sort in descending order. This is especially useful if you need to pass a sorting key anyway. For example, if the data was as follows:
```python
data = ['9', '10', '3', '4.5']
sorted(data, reverse=True)                      # doesn't sort correctly
sorted(data, key=lambda x: -float(x))           # sorts correctly
#                          ^ negate here
```
That said, passing a key along with `reverse=True` also works.
```
sorted(data, key=float, reverse=True)           # ['10', '9', '4.5', '3']
```


For an example with datetime, that would look like as follows: 
```python
from datetime import datetime
ts = ["04/20/2010 10:07:30", "12/01/2009 10:07:52", "01/13/2020 10:08:22", "12/01/2009 12:07:52"]
ts.sort(key=lambda x: -datetime.strptime(x, '%m/%d/%Y %H:%M:%S').timestamp())
#                                                               ^^^^ convert to a number here
ts
# ['01/13/2020 10:08:22', '04/20/2010 10:07:30', '12/01/2009 12:07:52', '12/01/2009 10:07:52']
```