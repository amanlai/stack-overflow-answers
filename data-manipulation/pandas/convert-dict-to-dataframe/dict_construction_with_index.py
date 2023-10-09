import pandas as pd


mydict = {
    'Open': ['47.47', '47.46', '47.38'],
   'Close': ['47.48', '47.45', '47.40'],
   'Date': ['2016/11/22 07:00:00', '2016/11/22 06:59:00','2016/11/22 06:58:00']
}


df1 = pd.DataFrame(mydict, columns=['Date', 'Open', 'Close']).set_index('Date')

df2 = pd.DataFrame(mydict, index=pd.Series(mydict.pop('Date'), name='Date'))