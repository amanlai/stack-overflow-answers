mylis1 = ['this is test', 'another test']
mylis2 = ['this is test', 'another test']
mylis3 = ['this is test', 'another test']

mylis1[:] = map(str.upper, mylis)

mylis2[:] = [x.upper() for x in mylis]

for i in range(len(mylis3)):
    mylis3[i] = mylis3[i].upper()