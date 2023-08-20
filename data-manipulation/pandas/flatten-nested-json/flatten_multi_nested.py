import json
import pandas as pd

# load sample data
j = json.load('sample_nested.json')

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