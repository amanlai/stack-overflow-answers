def dfs(G, output=[], N=None):

    N = N or len(G)

    if len(output) == N:
        return output

    if set() in G.values():
        return False

    degrees = {k: len(v) for k,v in G.items()}
    leafs = [k for k, v in degrees.items() if v == 1]

    if len(leafs) > 2:
        return False

    elif len(output) == 0:
        try:
            return dfs(G, [leafs[-1]], N)
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
        if dfs(G2, output, N):
            return output
        output.pop()
    return False


def square_sums(n):
    G = {i: set() for i in range(1, n+1)}
    for i in range(1, int((2*n-1)**0.5)):
        s = (i+1)**2
        for k in range(1, 1 + (s-1) // 2):
            if (v := s - k) <= n:
                G[k] |= {v}
                G[v] |= {k}
    return dfs(G)