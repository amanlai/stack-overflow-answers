import timeit
from df_to_nested_json import jsonify, groupby_apply, df_small, df_large, groupers


t1 = min(timeit.repeat(lambda: jsonify(df_small, groupers), number=1))         # 0.502
t2 = min(timeit.repeat(lambda: groupby_apply(df_small, groupers), number=1))   # 25


t3 = min(timeit.repeat(lambda: jsonify(df_large, groupers), number=1))         # 0.155
t4 = min(timeit.repeat(lambda: groupby_apply(df_large, groupers), number=1))   # 0.201