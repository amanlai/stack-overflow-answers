## Flattening a multi-nested json into a dataframe

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/74539549/19123103).</sup>

Suppose you have a json that looks like the following:
```json
j = [
    {
        "id": 401281949,
        "teams": [
            {
                "school": "Louisiana Tech",
                "conference": "Conference USA",
                "homeAway": "away",
                "points": 34,
                "stats": [
                    {"category": "rushingTDs", "stat": "1"},
                    {"category": "puntReturnYards", "stat": "24"},
                    {"category": "puntReturnTDs", "stat": "0"},
                    {"category": "puntReturns", "stat": "3"},
                ],
            }
        ],
    }
]
```
and you want to flatten it so that all of the stats are on their own column in each row.

---

The standard pandas function that flattens a json is `json_normalize()`. However, you need to pass the parameters correctly to get the output you want. In this case, you have to explicitly pass the paths to the meta data for each column in a single `json_normalize()` call. For example, `['teams', 'school']` would be one path, `['teams', 'conference']` is another path, etc. This will create a long dataframe similar to what you already have.

Then you can call `pivot()` to reshape this output into the correct shape.

```python
# normalize json
df = pd.json_normalize(
    j, record_path=['teams', 'stats'], 
    meta=['id', *(['teams', c] for c in ('school', 'conference', 'homeAway', 'points'))]
)
# column name contains 'teams' prefix; remove it
df.columns = [c.split('.')[1] if '.' in c else c for c in df]

# pivot the intermediate result
df = (
    df.astype({'points': int, 'id': int})
    .pivot(['id', 'school', 'conference', 'homeAway', 'points'], 'category', 'stat')
    .reset_index()
)
# remove index name
df.columns.name = None
```
[![res][1]][1]


  [1]: https://i.stack.imgur.com/CMRS6.png