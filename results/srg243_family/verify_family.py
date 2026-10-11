"""Standalone verifier (Python standard library only) for results/srg243_family.
For each edge list: srg(243,22,1,2) on all 29,403 pairs; number of induced 3x3 grids; the supplied automorphism
generators (if any) are automorphisms.  Distinct grid counts certify pairwise non-isomorphism.
Also checks that bvls243_hoffman_coclique.txt is a Hoffman coclique of BvLS (45 independent vertices, every other
vertex has exactly 5 neighbours in it).
  python3 verify_family.py"""
import os, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
N, K, LAM, MU = 243, 22, 1, 2

def load(name):
    adj = [set() for _ in range(N)]
    for line in open(os.path.join(HERE, name)):
        if line.strip():
            a, b = map(int, line.split()); adj[a].add(b); adj[b].add(a)
    return adj

def is_srg(adj):
    if any(len(a) != K for a in adj): return False
    for x in range(N):
        for y in range(x + 1, N):
            c = len(adj[x] & adj[y])
            if c != (LAM if y in adj[x] else MU): return False
    return True

def grids(adj):
    """count induced 3x3 grids: each is found once from each of its 9 vertices (its two lines through that vertex)."""
    total = 0
    for x in range(N):
        lines = []
        seen = set()
        for a in adj[x]:
            if a in seen: continue
            b = (adj[x] & adj[a]).pop(); seen |= {a, b}; lines.append((a, b))
        for L1, L2 in itertools.combinations(lines, 2):
            c = {}
            ok = True
            for i, a in enumerate(L1):
                for j, b in enumerate(L2):
                    if b in adj[a]: ok = False; break
                    rest = (adj[a] & adj[b]) - {x}
                    c[i, j] = rest.pop()
                if not ok: break
            if not ok: continue
            pts = [x, *L1, *L2, *c.values()]
            if len(set(pts)) != 9: continue
            E = sum(1 for p, q in itertools.combinations(pts, 2) if q in adj[p])
            if E == 18 and all(c[i, 0] in adj[c[i, 1]] for i in (0, 1)) and all(c[0, j] in adj[c[1, j]] for j in (0, 1)):
                total += 1
    assert total % 9 == 0
    return total // 9

def check_gens(adj, name):
    path = os.path.join(HERE, name)
    if not os.path.exists(path): return None
    n = 0
    for line in open(path):
        if not line.strip() or line.startswith("#"): continue
        g = list(map(int, line.split()))
        assert sorted(g) == list(range(N))
        for x in range(N):
            assert {g[y] for y in adj[x]} == adj[g[x]], "not an automorphism"
        n += 1
    return n

graphs = [("bvls243.edges", None, "BvLS (Berlekamp-van Lint-Seidel)"),
          ("twin243.edges", None, "second graph (papers/srg243_second)"),
          ("gamma3_aut864.edges", "gamma3_aut864.autgens", "Gamma3"),
          ("gamma4_aut3888.edges", "gamma4_aut3888.autgens", "Gamma4")]
counts = {}
for f, gens, label in graphs:
    adj = load(f)
    ok = is_srg(adj); g = grids(adj); ng = check_gens(adj, gens) if gens else None
    counts[f] = g
    print(f"{label:38s} srg(243,22,1,2): {ok}   induced 3x3 grids: {g}" + (f"   {ng} automorphism generators verified" if ng else ""))
    assert ok
print("pairwise non-isomorphic (distinct grid counts):", len(set(counts.values())) == len(counts))
adj = load("bvls243.edges")
C = set(map(int, open(os.path.join(HERE, "bvls243_hoffman_coclique.txt")).read().split()))
indep = all(not (adj[x] & C) for x in C)
five = all(len(adj[w] & C) == 5 for w in range(N) if w not in C)
print(f"BvLS Hoffman coclique: size {len(C)}, independent: {indep}, every outside vertex has 5 neighbours in it: {five}")
