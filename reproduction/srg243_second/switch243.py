"""Triangle far-graph switching for srg(n,k,1,2): for a triangle T, enumerate all far graphs compatible with the
integer row equations (B_C x = t per far vertex), choose globally consistent (symmetric) combinations, and return the
resulting srg's.  Usage: python3 switch243.py GRAPH.edges TRIANGLE_INDEX_LIST OUTPREFIX"""
import sys, itertools, time, json, subprocess
import numpy as np
from ortools.sat.python import cp_model

NAUTY = "/tmp/solvers/nauty_src/nauty2_8_8/"


def load_edges(path, n=243):
    M = np.zeros((n, n), dtype=np.int64)
    for line in open(path):
        if line.strip():
            i, j = map(int, line.split()); M[i, j] = M[j, i] = 1
    return M


def is_srg(M, k=22, lam=1, mu=2):
    n = len(M); M2 = M @ M
    I = np.eye(n, dtype=bool)
    return bool((M.sum(1) == k).all() and (M2[M == 1] == lam).all() and (M2[(M == 0) & ~I] == mu).all())


def triangles(M):
    n = len(M); out = []
    for i in range(n):
        for j in np.nonzero(M[i])[0]:
            if j > i:
                for k in np.nonzero(M[i] & M[j])[0]:
                    if k > j:
                        out.append((i, int(j), int(k)))
    return out


def row_candidates(M, T):
    n = len(M); NB = [set(np.nonzero(M[u])[0]) for u in range(n)]
    ball = set(T) | NB[T[0]] | NB[T[1]] | NB[T[2]]
    C = sorted(ball - set(T)); far = sorted(set(range(n)) - ball); F = len(far)
    deg = int(M[far[0], far].sum())
    Cs = set(C)
    cands = []
    for wi, w in enumerate(far):
        m = cp_model.CpModel(); x = [m.NewBoolVar("") for _ in range(F)]
        m.Add(x[wi] == 0); m.Add(sum(x) == deg)
        for u in C:
            tgt = (2 - M[u, w]) - len(NB[u] & NB[w] & Cs)
            m.Add(sum(x[j] for j in range(F) if M[u, far[j]]) == tgt)
        sols = []
        class CB(cp_model.CpSolverSolutionCallback):
            def on_solution_callback(s_):
                sols.append(frozenset(j for j in range(F) if s_.Value(x[j])))
        s = cp_model.CpSolver(); s.parameters.enumerate_all_solutions = True; s.parameters.num_workers = 1
        s.Solve(m, CB()); cands.append(sols)
    return far, cands


def consistent_choices(far, cands, limit=50):
    """choose one candidate per row with symmetric adjacency; enumerate up to `limit` solutions."""
    F = len(far)
    m = cp_model.CpModel()
    ch = [[m.NewBoolVar("") for _ in cands[i]] for i in range(F)]
    for i in range(F):
        m.AddExactlyOne(ch[i])
    # adjacency literal a_ij = OR over candidates of i containing j ; symmetric: a_ij == a_ji
    for i in range(F):
        for j in range(i + 1, F):
            aij = sum(ch[i][c] for c, S in enumerate(cands[i]) if j in S)
            aji = sum(ch[j][c] for c, S in enumerate(cands[j]) if i in S)
            m.Add(aij == aji)
    sols = []
    class CB(cp_model.CpSolverSolutionCallback):
        def on_solution_callback(s_):
            sols.append([next(c for c in range(len(cands[i])) if s_.Value(ch[i][c])) for i in range(F)])
            if len(sols) >= limit:
                s_.StopSearch()
    s = cp_model.CpSolver(); s.parameters.enumerate_all_solutions = True; s.parameters.num_workers = 1
    s.Solve(m, CB())
    return sols


def canon(M):
    import networkx as nx
    g6 = nx.to_graph6_bytes(nx.from_numpy_array(M), header=False)
    out = subprocess.run([NAUTY + "labelg", "-q"], input=g6, capture_output=True).stdout.strip()
    return out


def aut_order(M):
    n = len(M)
    lines = [f"n={n} g"] + [" ".join(str(j) for j in np.nonzero(M[i])[0] if j > i) + ";" for i in range(n)]
    out = subprocess.run([NAUTY + "dreadnaut"], input="\n".join(lines) + "\nx\nq\n", capture_output=True, text=True).stdout
    l = [x for x in out.split("\n") if "grpsize" in x]
    return l[0].strip() if l else "?"


if __name__ == "__main__":
    M = load_edges(sys.argv[1]); tri_idx = [int(t) for t in sys.argv[2].split(",")]; outp = sys.argv[3]
    tris = triangles(M)
    for ti in tri_idx:
        T = tris[ti]; t0 = time.time()
        far, cands = row_candidates(M, T)
        dist = {}
        for c in cands:
            dist[len(c)] = dist.get(len(c), 0) + 1
        sols = consistent_choices(far, cands)
        res = []
        for sol in sols:
            B = M.copy()
            for i, wi in enumerate(far):
                S = cands[i][sol[i]]
                for j, wj in enumerate(far):
                    B[wi, wj] = 1 if j in S else 0
            ok = is_srg(B)
            res.append((ok, B))
        print(f"triangle {ti} {T}: candidates/row {dist}; consistent choices {len(sols)}; srg among them "
              f"{sum(1 for ok, _ in res if ok)}; {time.time() - t0:.0f}s", flush=True)
        for r_i, (ok, B) in enumerate(res):
            if ok:
                c = canon(B)
                np.save(f"{outp}_t{ti}_s{r_i}.npy", B)
                print("   srg", r_i, "canon", c[:24], "aut", aut_order(B), flush=True)
