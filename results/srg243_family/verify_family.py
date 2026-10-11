"""Standalone verifier (Python standard library only) for results/srg243_family.
For each edge list: srg(243,22,1,2) on all 29,403 pairs; number of induced 3x3 grids; the supplied automorphism
generators (if any) are automorphisms.  Distinct grid counts certify pairwise non-isomorphism.
Also checks that bvls243_hoffman_coclique.txt is a Hoffman coclique of BvLS (45 independent vertices, every other
vertex has exactly 5 neighbours in it).
The --full option also checks graph6 agreement, full automorphism groups and vertex orbits with nauty, and the
orders of the supplied generator groups with Schreier-Sims (requires NetworkX, pynauty and SymPy).
  python3 verify_family.py [--full]"""
import argparse
import collections
import os, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
N, K, LAM, MU = 243, 22, 1, 2

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def load(name):
    adj = [set() for _ in range(N)]
    seen = set()
    for line in open(os.path.join(HERE, name)):
        if line.strip():
            a, b = map(int, line.split())
            require(0 <= a < N and 0 <= b < N and a != b, f"invalid edge in {name}")
            edge = tuple(sorted((a, b)))
            require(edge not in seen, f"duplicate edge in {name}")
            seen.add(edge)
            adj[a].add(b); adj[b].add(a)
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
    require(os.path.isfile(path), f"missing generators: {name}")
    n = 0
    for line in open(path):
        if not line.strip() or line.startswith("#"): continue
        g = list(map(int, line.split()))
        require(sorted(g) == list(range(N)), f"invalid permutation in {name}")
        for x in range(N):
            require({g[y] for y in adj[x]} == adj[g[x]], f"not an automorphism: {name}")
        n += 1
    require(n > 0, f"no generators in {name}")
    return n

def check_full(adj, edge_file, gen_file, expected_order, expected_orbits):
    import networkx as nx
    import pynauty
    from sympy.combinatorics import Permutation, PermutationGroup

    graph = pynauty.Graph(number_of_vertices=N, adjacency_dict={x: sorted(adj[x]) for x in range(N)})
    _, mantissa, exponent, orbit_labels, _ = pynauty.autgrp(graph)
    order = int(round(mantissa * 10 ** exponent))
    orbits = sorted(collections.Counter(orbit_labels).values())
    require(order == expected_order, f"unexpected automorphism order for {edge_file}: {order}")
    require(orbits == expected_orbits, f"unexpected vertex orbits for {edge_file}: {orbits}")
    if gen_file:
        permutations = []
        for line in open(os.path.join(HERE, gen_file)):
            if line.strip() and not line.startswith("#"):
                permutations.append(Permutation(list(map(int, line.split()))))
        supplied_order = int(PermutationGroup(permutations).order())
        require(supplied_order == order, f"supplied generators do not generate the full group: {gen_file}")
        g6 = nx.read_graph6(os.path.join(HERE, edge_file.replace(".edges", ".g6")))
        edges = {(x, y) for x in range(N) for y in adj[x] if x < y}
        require(g6.number_of_nodes() == N and {tuple(sorted(e)) for e in g6.edges()} == edges,
                f"graph6 and edge list disagree: {edge_file}")
        print(f"  graph6 agreement and supplied generator group order {supplied_order}: OK")
    print(f"  full automorphism group order {order}, vertex orbit sizes {orbits}: OK")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true", help="also check automorphism groups, orbits and graph6 files")
    args = parser.parse_args()
    graphs = [("bvls243.edges", None, "BvLS (Berlekamp-van Lint-Seidel)", 1485, 3849120, [243]),
              ("twin243.edges", None, "second graph (papers/srg243_second)", 405, 4320, [3, 60, 180]),
              ("gamma3_aut864.edges", "gamma3_aut864.autgens", "Gamma3", 621, 864, [27, 108, 108]),
              ("gamma4_aut3888.edges", "gamma4_aut3888.autgens", "Gamma4", 837, 3888, [81, 162])]
    counts = {}
    for f, gens, label, expected_grids, order, orbits in graphs:
        adj = load(f)
        require(is_srg(adj), f"SRG parameters fail: {f}")
        g = grids(adj)
        require(g == expected_grids, f"unexpected grid count for {f}: {g}")
        ng = check_gens(adj, gens) if gens else None
        counts[f] = g
        print(f"{label:38s} srg(243,22,1,2): True   induced 3x3 grids: {g}" +
              (f"   {ng} automorphism generators verified" if ng else ""))
        if args.full:
            check_full(adj, f, gens, order, orbits)
    require(len(set(counts.values())) == len(counts), "grid counts do not establish pairwise non-isomorphism")
    print("pairwise non-isomorphic (distinct grid counts): True")
    adj = load("bvls243.edges")
    vertices = list(map(int, open(os.path.join(HERE, "bvls243_hoffman_coclique.txt")).read().split()))
    C = set(vertices)
    require(len(vertices) == len(C) == 45 and all(0 <= x < N for x in C), "invalid coclique vertices")
    indep = all(not (adj[x] & C) for x in C)
    five = all(len(adj[w] & C) == 5 for w in range(N) if w not in C)
    require(indep and five, "BvLS Hoffman coclique check failed")
    print("BvLS Hoffman coclique: size 45, independent: True, every outside vertex has 5 neighbours in it: True")


if __name__ == "__main__":
    main()
