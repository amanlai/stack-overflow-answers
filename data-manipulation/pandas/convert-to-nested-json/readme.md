## How to convert a dataframe into a nested json

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/75780569/19123103).</sup>

Setup:

```none
,ID,Location,Country,Latitude,Longitude,timestamp,tide
0,1,BREST,FRA,48.383,-4.495,1807-01-01,6905.0  
1,1,BREST,FRA,48.383,-4.495,1807-02-01,6931.0  
2,1,BREST,FRA,48.383,-4.495,1807-03-01,6896.0  
3,1,BREST,FRA,48.383,-4.495,1807-04-01,6953.0  
4,1,BREST,FRA,48.383,-4.495,1807-05-01,7043.0  
2508,7,CUXHAVEN 2,DEU,53.867,8.717,1843-01-01,7093.0  
2509,7,CUXHAVEN 2,DEU,53.867,8.717,1843-02-01,6688.0  
2510,7,CUXHAVEN 2,DEU,53.867,8.717,1843-03-01,6493.0  
2511,7,CUXHAVEN 2,DEU,53.867,8.717,1843-04-01,6723.0  
2512,7,CUXHAVEN 2,DEU,53.867,8.717,1843-05-01,6533.0  
4525,9,MAASSLUIS,NLD,51.918,4.25,1848-02-01,6880.0  
4526,9,MAASSLUIS,NLD,51.918,4.25,1848-03-01,6700.0  
4527,9,MAASSLUIS,NLD,51.918,4.25,1848-04-01,6775.0  
4528,9,MAASSLUIS,NLD,51.918,4.25,1848-05-01,6580.0  
4529,9,MAASSLUIS,NLD,51.918,4.25,1848-06-01,6685.0  
6540,8,WISMAR 2,DEU,53.898999999999994,11.458,1848-07-01,6957.0  
6541,8,WISMAR 2,DEU,53.898999999999994,11.458,1848-08-01,6944.0  
6542,8,WISMAR 2,DEU,53.898999999999994,11.458,1848-09-01,7084.0  
6543,8,WISMAR 2,DEU,53.898999999999994,11.458,1848-10-01,6898.0  
6544,8,WISMAR 2,DEU,53.898999999999994,11.458,1848-11-01,6859.0  
8538,10,SAN FRANCISCO,USA,37.806999999999995,-122.465,1854-07-01,6909.0  
8539,10,SAN FRANCISCO,USA,37.806999999999995,-122.465,1854-08-01,6940.0  
8540,10,SAN FRANCISCO,USA,37.806999999999995,-122.465,1854-09-01,6961.0  
8541,10,SAN FRANCISCO,USA,37.806999999999995,-122.465,1854-10-01,6952.0  
8542,10,SAN FRANCISCO,USA,37.806999999999995,-122.465,1854-11-01,6952.0  
```

A native pandas method is to use `groupby.apply`. However, `groupby.apply` forces data manipulations on each group to create the nested structure which is really slow. A simple for-loop approach using `itertuples` and a list comprehension to create the nested structure and serializing it via `json.dumps` is much faster. If the groups are small-ish, then this approach is especially useful because `groupby.apply` is really slow for those.<sup>1</sup>
```python
import json
keys = ['ID', 'Location', 'Country', 'Latitude', 'Longitude']
mydict = {}
for row in df.itertuples(index=False):
    mydict.setdefault(row[:5], {})[row.timestamp] = row.tide
mylist = [{**dict(zip(keys, k)), 'Tide-Data': v} for k, v in mydict.items()]
j = json.dumps(mylist)
```
Note that `groupby.apply` approach of [MaxU][1] should be changed slightly (the lambda passed to `apply` should be a bit different) to produce the expected output:
```python
j = df.groupby(keys).apply(lambda x: x.set_index('timestamp')['tide'].to_dict()).reset_index(name='Tide-Data').to_json(orient='records')
```
Both produce the following output for the given input:
```none
[
  {
    "ID": 1,
    "Location": "BREST",
    "Country": "FRA",
    "Latitude": 48.383,
    "Longitude": -4.495,
    "Tide-Data": {
      "1807-01-01": 6905.0,
      "1807-02-01": 6931.0,
      "1807-03-01": 6896.0,
      "1807-04-01": 6953.0,
      "1807-05-01": 7043.0
    }
  },
  {
    "ID": 7,
    "Location": "CUXHAVEN 2",
    "Country": "DEU",
    "Latitude": 53.867,
    "Longitude": 8.717,
    "Tide-Data": {
      "1843-01-01": 7093.0,
      "1843-02-01": 6688.0,
      "1843-03-01": 6493.0,
      "1843-04-01": 6723.0,
      "1843-05-01": 6533.0
    }
  },
  {
    "ID": 9,
    "Location": "MAASSLUIS",
    "Country": "NLD",
    "Latitude": 51.918,
    "Longitude": 4.25,
    "Tide-Data": {
      "1848-02-01": 6880.0,
      "1848-03-01": 6700.0,
      "1848-04-01": 6775.0,
      "1848-05-01": 6580.0,
      "1848-06-01": 6685.0
    }
  },
  {
    "ID": 8,
    "Location": "WISMAR 2",
    "Country": "DEU",
    "Latitude": 53.899,
    "Longitude": 11.458,
    "Tide-Data": {
      "1848-07-01": 6957.0,
      "1848-08-01": 6944.0,
      "1848-09-01": 7084.0,
      "1848-10-01": 6898.0,
      "1848-11-01": 6859.0
    }
  },
  {
    "ID": 10,
    "Location": "SAN FRANCISCO",
    "Country": "USA",
    "Latitude": 37.807,
    "Longitude": -122.465,
    "Tide-Data": {
      "1854-07-01": 6909.0,
      "1854-08-01": 6940.0,
      "1854-09-01": 6961.0,
      "1854-10-01": 6952.0,
      "1854-11-01": 6952.0
    }
  }
]
```

---

<sup>1</sup> Benchmark result: On a frame with 100k rows, the loop approach is approx. 50 times faster than the `groupby.apply` approach if each group is relatively small. The code used to produce the benchmark result may be found on this repo [here](./benchmark.py)

  [1]: https://stackoverflow.com/a/40490276/19123103