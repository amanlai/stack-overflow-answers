from itertools import repeat, starmap
from operator import mul

mylis = list(range(5))

newlis1 = list(map(mul, mylis, repeat(2)))
# or with starmap
newlis2 = list(starmap(mul, zip(mylis, repeat(2))))

# but at this point, list comprehension is simpler imo
newlis3 = [x*2 for x in mylis]

print(newlis1)
print(newlis2)
print(newlis3)