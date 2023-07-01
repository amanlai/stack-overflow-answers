import pandas as pd

json = {
    "teams": {"home": "BOS", "away": "MIA"},
    "summary": [
        {"home_score": 0, "away_score": 0}
    ]
}

json['summary']['home_score']               # <---- TypeError: list indices must be integers or slices, not str
json['summary'][0]['home_score']            # <---- OK (returns the first item)
#              ^^^   <---- index the list here
[d['home_score'] for d in json['summary']]  # <---- OK (returns a list)


#######################################################

d = []
d['key'] = 1                                # <---- TypeError


d = {}
d['key'] = 1                                # <---- OK


#######################################################

df = pd.DataFrame([range(4), range(4)])
df = ['A', 'B', 'C', 'D']
df['A']                                     # <---- TypeError


df = pd.DataFrame([range(4), range(4)])
df.columns = ['A', 'B', 'C', 'D']
# ^^^^^^^^  <---- assign column labels here
df['A']                                     # <---- OK


#######################################################

lst = ['a', 'b', 'c']
index = input()

lst[index]                                  # <---- TypeError: list indices must be integers or slices, not str
lst[int(index)]                             # <---- OK


#######################################################

lst = ['a', 'b', 'a', 'd']

lst['a']                                    # <---- TypeError
lst[lst.index('a')]                         # <---- OK


#######################################################

for i in lst:
    if lst[i] == 'b':                       # <---- TypeError
        pass

for i in lst:
    if i == 'b':                            # <---- OK
        pass
    
for i in range(len(lst)):                   # <---- OK
    if lst[i] == 'b':
        pass