def square_sums(n, tup=(0,)):
    if len(tup) == n+1:
        return list(tup[1:])
    for i in range(1, n+1):
        if i in tup:
            continue
        if (tup[-1]+i)**0.5 % 1 == 0:
            res = square_sums(n, (*tup, i))
            if res:
                return res
    return False