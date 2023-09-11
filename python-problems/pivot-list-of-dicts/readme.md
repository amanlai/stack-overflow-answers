## Pivot a list of dictionaries into 

<sup>This is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/75299607/19123103).</sup>

How do we "pivot" a list of dicts and aggregate on certain key's values? Suppose we have a list of dicts where each dict has a `service_order_number`. Now, we want to group by these service order numbers and collect each items with the same service order numbers in a list.

In other words, how do we convert data in the following format:
```none
my_data = [
    {"service_order_number": "ABC", "vendor_id": 0, "recipient_id": 0, "item_id": 0, "part_number": "string", "part_description": "string"},
    {"service_order_number": "ABC", "vendor_id": 0, "recipient_id": 0, "item_id": 1, "part_number": "string", "part_description": "string"},
    {"service_order_number": "DEF", "vendor_id": 0, "recipient_id": 0, "item_id": 2, "part_number": "string", "part_description": "string"},
    {"service_order_number": "DEF", "vendor_id": 0, "recipient_id": 0, "item_id": 3, "part_number": "string", "part_description": "string"}
]
```
into the following format:
```none
[{'service_order_number': 'ABC',
  'vendor_id': 0,
  'recipient_id': 0,
  'items': [{'item_id': 0, 'part_number': 'string', 'part_description': 'string'},
            {'item_id': 1, 'part_number': 'string', 'part_description': 'string'}]},
 {'service_order_number': 'DEF', 
  'vendor_id': 0, 
  'recipient_id': 0,
  'items': [{'item_id': 2, 'part_number': 'string', 'part_description': 'string'},
            {'item_id': 3, 'part_number': 'string', 'part_description': 'string'}]}]
```
What is the simplest way to do it?

----


If you don't need the original data after, you can use `dict.pop` to create common keys to group over and populate a dictionary in a loop. Note that this code destroys the original data you'll only have `res` in the end.

```python
res = {}
keys = ['service_order_number', 'vendor_id', 'recipient_id']
for d in my_data:
    vals = tuple(d.pop(k) for k in keys)
    res.setdefault(vals, {}).update(dict(zip(keys, vals)))
    # "items" key-value pairs are further nested inside 'items' key
    res[vals].setdefault('items', []).append(d)
res = list(res.values())
```