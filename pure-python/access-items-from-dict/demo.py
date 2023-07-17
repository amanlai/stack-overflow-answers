from operator import itemgetter
from itertools import islice

d = {'a':2, 'b':4, 'c':7}
x = list(d.values())
print(x)

*values, = d.values()
print(values)


list_of_keys = ['a', 'c']
res = [d[k] for k in list_of_keys] 
print(res)
res = [d.get(k) for k in list_of_keys]
print(res)


res = list(itemgetter(*list_of_keys)(d))
print(res)

list_of_keys = ['a','c']
print([d.get(k) for k in list_of_keys])
print(list(itemgetter(*list_of_keys)(d)))


############################################################################


list_of_dicts = [ {"title": "A", "body": "AA"}, {"title": "B", "body": "BB"} ]
list_comp = [d['title'] for d in list_of_dicts]
itmgetter = list(map(itemgetter('title'), list_of_dicts))
print(list_comp)
print(itmgetter)


############################################################################



test = {'foo': 'bar', 'hello': 'world'}
# first key
print(next(iter(test)))
# slice test.keys from index l to index u
some_keys = list(islice(test, l, u))
print(some_keys)



dct = {'A':1, 'B':2, 'C':3, 'D':4}
the_sum = sum(islice(dct.values(), 1, 3))
print(f"The sum of the 2nd and 3rd value in dictionary {dct} is {the_sum}")