import pandas as pd
import perfplot
from random import choices
from datetime import datetime

mdYHMSf = range(1,13), range(1,29), range(2000,2024), range(24), *[range(60)]*2, range(1000)
perfplot.show(
    kernels=[lambda x: pd.to_datetime(x), 
             lambda x: pd.to_datetime(x, format='%m/%d/%Y %H:%M:%S.%f'), 
             lambda x: pd.to_datetime(x, infer_datetime_format=True),
             lambda s: s.apply(lambda x: datetime.strptime(x, '%m/%d/%Y %H:%M:%S.%f'))],
    labels=["pd.to_datetime(df['date'])", 
            "pd.to_datetime(df['date'], format='%m/%d/%Y %H:%M:%S.%f')", 
            "pd.to_datetime(df['date'], infer_datetime_format=True)", 
            "df['date'].apply(lambda x: datetime.strptime(x, '%m/%d/%Y %H:%M:%S.%f'))"],
    n_range=[2**k for k in range(20)],
    setup=lambda n: pd.Series([f"{m}/{d}/{Y} {H}:{M}:{S}.{f}" 
                               for m,d,Y,H,M,S,f in zip(*[choices(e, k=n) for e in mdYHMSf])]),
    equality_check=pd.Series.equals,
    xlabel='len(df)'
)
