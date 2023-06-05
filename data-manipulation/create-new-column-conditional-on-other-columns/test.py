import pandas as pd
import numpy as np
import numba as nb

def pd_loc(df):
    df['rno_defined'] = 'Other'
    df.loc[df['eri_nat_amer'] == 1, 'rno_defined'] = 'A/I AK Native'
    df.loc[df['eri_asian'] == 1, 'rno_defined'] = 'Asian'
    df.loc[df['eri_afr_amer'] == 1, 'rno_defined'] = 'Black/AA'
    df.loc[df['eri_hawaiian'] == 1, 'rno_defined'] = 'Haw/Pac Isl.'
    df.loc[df['eri_white'] == 1, 'rno_defined'] = 'White'
    df.loc[df[['eri_afr_amer', 'eri_asian', 'eri_hawaiian', 'eri_nat_amer', 'eri_white']].sum(1) > 1, 'rno_defined'] = 'Two Or More'
    df.loc[df['eri_hispanic'] == 1, 'rno_defined'] = 'Hispanic'
    return df

def np_select(df):
    conditions = [df['eri_hispanic'] == 1,
                  df[['eri_afr_amer', 'eri_asian', 'eri_hawaiian', 'eri_nat_amer', 'eri_white']].sum(1).gt(1),
                  df['eri_nat_amer'] == 1,
                  df['eri_asian'] == 1,
                  df['eri_afr_amer'] == 1,
                  df['eri_hawaiian'] == 1,
                  df['eri_white'] == 1]
    outputs = ['Hispanic', 'Two Or More', 'A/I AK Native', 'Asian', 'Black/AA', 'Haw/Pac Isl.', 'White']
    df['rno_defined'] = np.select(conditions, outputs, 'Other')
    return df


@nb.jit(nopython=True)
def conditional_assignment(arr, res):
    
    length = len(arr)
    for i in range(length):
        if arr[i][3] == 1 :
            res[i] = 'Hispanic'
        elif arr[i][0] + arr[i][1] + arr[i][2] + arr[i][4] + arr[i][5] > 1 :
            res[i] = 'Two Or More'
        elif arr[i][0]  == 1:
            res[i] = 'Black/AA'
        elif arr[i][1] == 1:
            res[i] = 'Asian'
        elif arr[i][2] == 1:
            res[i] = 'Haw/Pac Isl.'
        elif arr[i][4] == 1 :
            res[i] = 'A/I AK Native'
        elif arr[i][5] == 1:
            res[i] = 'White'
        else:
            res[i] = 'Other'
            
    return res

def nb_loop(df):
    cols = [c for c in df.columns if c.startswith('eri_')]
    res = np.empty(len(df), dtype=f"<U{len('A/I AK Native')}")
    df['rno_defined'] = conditional_assignment(df[cols].values, res)
    return df