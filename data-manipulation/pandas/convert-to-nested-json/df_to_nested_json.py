import numpy as np
import pandas as pd

def jsonify(df, groupers):
    res = {}
    for row in df.itertuples(index=False):
        res.setdefault(row[:5], {})[row.timestamp] = row.tide
    j = json.dumps([dict(zip(groupers, k)) | {'Tide-Data': v} for k, v in res.items()])
    return j


def groupby_apply(df, groupers):
    return (
        df.groupby(groupers)
        .apply(lambda x: x.set_index('timestamp')['tide'].to_dict())
        .reset_index(name='Tide-Data')
        .to_json(orient='records')
    )

df = pd.DataFrame(
    np.random.default_rng().choice(10, size=(100000, 7)), 
    columns=['ID','Location','Country','Latitude','Longitude', 'timestamp', 'tide']
)
groupers = ['ID','Location','Country','Latitude','Longitude']


%timeit jsonify(df, groupers)
# 502 ms ± 17.8 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
%timeit groupby_apply(df, groupers)
# 25 s ± 1.38 s per loop (mean ± std. dev. of 7 runs, 1 loop each)
```
If the groups are large, then the difference is much smaller but the loop implementation is still faster than `groupby.apply`:
```python
df = pd.DataFrame(np.random.default_rng().choice(3, size=(100000, 7)), columns=['ID','Location','Country','Latitude','Longitude', 'timestamp', 'tide'])

%timeit jsonify(df, groupers)
# 155 ms ± 6.45 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

%timeit df.groupby(groupers).apply(lambda x: x.set_index('timestamp')['tide'].to_dict()).reset_index(name='Tide-Data').to_json(orient='records')
# 201 ms ± 6.63 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)