## How to convert a json list to a DataFrame

<sup>This post is based on my answer to a Stack Overflow question that may be found [here](https://stackoverflow.com/a/75304268/19123103).</sup>

#### How to create a DataFrame from an HTTP-request

If you want to scrape data from a webpage, a common method is to the `requests` library. It has `json()` method which returns the response data as a json object, which can be directly converted into a dataframe using the `DataFrame()` constructor. So the simplest case would be 

```python
import requests
import pandas as pd

response = requests.get(url)
df = pd.DataFrame(response.json())
```


If we need to collect the json responses from multiple HTTP-requests, then the "best" way is to collect them in a Python list and create a DataFrame once at the end of the loop.

```python
import requests
import pandas as pd

def get_historical_stock(tickerList): 
    lst = []                                 # <----- list
    for item in tickerList:
        url = 'https://www.byma.com.ar/wp-admin/admin-ajax.php?action=get_historico_simbolo&simbolo=' + item + '&fecha=01-02-2018'
        response = requests.get(url)
        if response.content:
            print('ok info Historical Stock')
        data = response.json()
        lst.append(data)                     # <----- list.append()
    df = pd.DataFrame(lst)                   # <----- dataframe construction
    return df
```