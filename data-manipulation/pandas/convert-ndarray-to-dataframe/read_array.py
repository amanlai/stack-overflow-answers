from io import StringIO
import pandas as pd

def read_array(data, index_col=[0], header=0):
    sio = StringIO('\n'.join([','.join(row) for row in data.tolist()]))
    return pd.read_csv(sio, index_col=index_col, header=header)