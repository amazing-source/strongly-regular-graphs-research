"""Standalone verifier (pure Python, integers only).  Usage: python3 verify_srg243.py FILE.edges
Checks srg(243,22,1,2): 22-regular, every adjacent pair has exactly 1 common neighbour, every non-adjacent pair exactly 2.
Also prints the distribution of induced 3x3 grids (K3 x K3) through a vertex: an isomorphism invariant
(Berlekamp-van Lint-Seidel graph: 55 at every vertex, 1485 grids)."""
import sys, itertools
n = 243
adj = [set() for _ in range(n)]
for line in open(sys.argv[1]):
    if line.strip():
        i, j = map(int, line.split()); adj[i].add(j); adj[j].add(i)
assert all(len(adj[i]) == 22 for i in range(n)), "not 22-regular"
for i in range(n):
    for j in range(i + 1, n):
        c = len(adj[i] & adj[j])
        if j in adj[i]:
            assert c == 1, (i, j, c)
        else:
            assert c == 2, (i, j, c)
print("srg(243,22,1,2): OK")
def grids_at(x):
    T = [(y, z) for y in adj[x] for z in adj[x] & adj[y] if y < z]
    cnt = 0
    for (a, b), (c, d) in itertools.combinations(T, 2):
        if {c, d} & (adj[a] | adj[b]):
            continue
        def comp(p, q):
            cn = (adj[p] & adj[q]) - {x}
            return next(iter(cn)) if len(cn) == 1 else None
        e = [comp(a, c), comp(a, d), comp(b, c), comp(b, d)]
        if None in e:
            continue
        S = [x, a, b, c, d] + e
        if len(set(S)) == 9 and all(len(adj[s] & set(S)) == 4 for s in S):
            cnt += 1
    return cnt
g = [grids_at(x) for x in range(n)]
dist = {}
for c in g:
    dist[c] = dist.get(c, 0) + 1
print("induced 3x3 grids through a vertex:", dict(sorted(dist.items())), " total:", sum(g) // 9)
