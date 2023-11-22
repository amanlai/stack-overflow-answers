def dfs(G, output=[]):

    exhausted = set() in G.values()
    if len(G) == 1 and exhausted:
        return output

    if exhausted:
        return False

    degrees = {k: len(v) for k,v in G.items()}
    leafs = [k for k, v in degrees.items() if v == 1]

    if len(leafs) > 2:
        return False

    elif len(output) == 0:
        try:
            return dfs(G, [leafs[-1]])
        except IndexError:
            pass

        for d in range(2, max(degrees.values())+1):
            for k, v in degrees.items():
                if v == d:
                    if sol:=dfs(G, [k]):
                        return sol
        return False

    elif len(leafs) == 2:
        if output[-1] not in leafs:
            return False

    last = output[-1]
    for curr in G[last]:
        output.append(curr)
        G2 = {k: G[k] - {last} if k in G[last] else G[k] for k in G.keys() - {last}}
        if dfs(G2, output):
            return output
        output.pop()
    return False


def square_sums(n):
    G = {i: set() for i in range(1, n+1)}
    for i in range(1, int((2*n-1)**0.5)):
        s = (i+1)**2
        for k in range(1, 1 + (s-1) // 2):
            if (v := s - k) <= n:
                G[k].add(v)
                G[v].add(k)
    return dfs(G)



# driver
n = 37
x = square_sums(n)
print(x)
if x:
    print(all((i+j)**0.5 % 1 == 0 for i,j in zip(x, x[1:])))  # True
    print(sorted(x) == list(range(1, n+1)))                   # True