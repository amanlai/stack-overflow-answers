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




df_small = pd.DataFrame(
    np.random.default_rng().choice(10, size=(100000, 7)), 
    columns=['ID', 'Location', 'Country', 'Latitude', 'Longitude', 'timestamp', 'tide']
)

df_large = pd.DataFrame(
    np.random.default_rng().choice(3, size=(100000, 7)), 
    columns=['ID', 'Location', 'Country', 'Latitude', 'Longitude', 'timestamp', 'tide']
)

groupers = ['ID','Location','Country','Latitude','Longitude']


