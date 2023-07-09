import pandas as pd

df = pd.DataFrame({
    'Date': [
        '12/07/2013 21:50:00',
        '13/07/2013 00:30:00',
        '15/07/2013',
        '11/07/2013'
    ]
})

# option 1: `dayfirst`
df['Date1'] = pd.to_datetime(df['Date'], dayfirst=True)

# option 2: 2-step `format`
df['Date2'] = pd.to_datetime(df['Date'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
df['Date2'] = df['Date2'].fillna(pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce'))

print(df)