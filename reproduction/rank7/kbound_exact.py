"""Exact star-relation test for a hypothetical value K of the 7-adic invariant k (notes/97, L20 ter).

For each class type of tau_a with star rank r <= K: enumerate every subspace A of the dual of ker(star block) with
dim A <= D = dim ker - (12 - K) that meets all candidate sets T_z (kbound_star relaxation), then for each such A decide
with SAT whether the columns' star neighbours can be chosen consistently:
  (deg)   each star vertex {a,b}: exactly 10 generic neighbours and exactly 1 in star(abar);
  (label) for each star label l: exactly one column containing l lists l (tau_l(a) is a single label);
  (lin)   every column's functional lies in A.
Only the *minimal* subspaces met by the DFS are enumerated; every admissible A contains one of them, and a superset
of a feasible subspace can only add options, so we also test, for each minimal subspace, the full admissible
closure... To stay exact we test each enumerated A as found by the DFS (dim <= D), which includes all admissible A
that are spanned by one representative per unmet set (see comment in enumerate_A).
Usage: kbound_exact.py K [type ...]
"""
import sys, itertools
import numpy as np
from pysat.formula import IDPool, CNF
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153
import kbound_star as ks

p = 7


def in_span(R, piv, v):
    v = v.copy() % p
    for i, c in enumerate(piv):
        v = (v - v[c] * R[i]) % p
    return not v.any()


def enumerate_A(T, d, D):
    """All subspaces A (as rref keys) with dim <= D, meeting every T_z, reachable by the DFS that adds, at each step,
    one vector of the smallest unmet set.  Every admissible subspace B (dim <= D, meeting all T_z) contains such a
    DFS leaf (follow the DFS choosing, at each step, a vector of B in the unmet set): so if every leaf is infeasible
    **as a superset-closed condition**, we must test supersets too.  We therefore return the leaves, and the caller
    tests each leaf *and* lets the SAT model range over all functionals in any superspace of dim <= D containing the
    leaf is too costly; instead the SAT model below allows every functional in the DFS leaf only when the leaf has
    dim D (maximal), and extends lower-dimensional leaves to all their D-dimensional supersets on demand."""
    # sets containing the zero functional are met by every subspace: drop them (otherwise the DFS may branch on
    # them and miss admissible subspaces that meet them only at 0)
    T = [t for t in T if not (t % p == 0).all(axis=1).any()]
    seen, leaves = set(), set()
    def meets(basis, t):
        if basis.shape[0] == 0:
            return False
        R, piv = ks.rref(basis); tt = t.copy() % p
        for i, c in enumerate(piv):
            tt = (tt - np.outer(tt[:, c], R[i])) % p
        return (tt == 0).all(axis=1).any()
    def rec(basis):
        key = tuple(map(tuple, ks.rref(basis)[0])) if basis.shape[0] else ()
        if key in seen:
            return
        seen.add(key)
        unmet = [t for t in T if not meets(basis, t)]
        if not unmet:
            leaves.add(key); return
        if basis.shape[0] >= D:
            return
        t = min(unmet, key=len)
        for v in t:
            nb = np.concatenate([basis, v[None, :]], axis=0) if basis.shape[0] else v[None, :]
            R = ks.rref(nb)[0]
            if R.shape[0] > basis.shape[0]:
                rec(R)
    rec(np.zeros((0, d), dtype=np.int64))
    return leaves


def exact_ok(tau, Kb, A_key):
    others, oi, mate = ks.others, ks.oi, ks.mate
    A = np.array(A_key, dtype=np.int64)
    R, piv = ks.rref(A) if A.size else (np.zeros((0, Kb.shape[0]), dtype=np.int64), [])
    cval = {b: Kb[:, oi[b]] for b in others}
    ssum = Kb.sum(axis=1) % p
    pool = IDPool(); cnf = CNF()
    inc = {b: [] for b in others}; lab = {b: [] for b in others}; match = {b: [] for b in others}
    generic = [(l, q) for l, q in itertools.combinations(others, 2) if l[0] != q[0]]
    ok = lambda v: (in_span(R, piv, v) if len(piv) else not (v % p).any())
    for (l, q) in generic:
        base = (3 * (cval[l] + cval[q]) + cval[mate(l)] + cval[mate(q)] + 5 * ssum) % p
        opts = []
        for b1, b2 in itertools.combinations(others, 2):
            if tau[b1] == b2:
                continue
            if ok((base + cval[b1] + cval[b2]) % p):
                v = pool.id(('g', l, q, b1, b2)); opts.append(v); inc[b1].append(v); inc[b2].append(v)
                for bb in (b1, b2):
                    if bb in (l, q):
                        lab[bb].append(v)
        if not opts:
            return False
        cnf.extend(CardEnc.equals(opts, 1, vpool=pool, encoding=EncType.seqcounter).clauses)
    for q in others:
        base = (3 * cval[q] + cval[mate(q)] + 6 * ssum) % p
        opts = []
        for b in others:
            if ok((base + cval[b]) % p):
                v = pool.id(('s', q, b)); opts.append(v); match[b].append(v)
                if b == q:
                    lab[q].append(v)
        if not opts:
            return False
        cnf.extend(CardEnc.equals(opts, 1, vpool=pool, encoding=EncType.seqcounter).clauses)
    for b in others:
        for lits, n in ((inc[b], 10), (match[b], 1), (lab[b], 1)):
            if len(lits) < n:
                return False
            cnf.extend(CardEnc.equals(lits, n, vpool=pool, encoding=EncType.seqcounter).clauses)
    with Cadical153(bootstrap_with=cnf.clauses) as s:
        return s.solve()


def superspaces(A_key, d, D):
    """All subspaces of dim exactly min(D, d) containing A (rref keys) -- only used when a leaf has dim < D."""
    A = np.array(A_key, dtype=np.int64) if len(A_key) else np.zeros((0, d), dtype=np.int64)
    out = set()
    def rec(B):
        if B.shape[0] >= D:
            out.add(tuple(map(tuple, ks.rref(B)[0]))); return
        for v in itertools.product(range(p), repeat=d):
            v = np.array(v, dtype=np.int64)
            if not v.any():
                continue
            nb = np.concatenate([B, v[None, :]], axis=0) if B.shape[0] else v[None, :]
            R = ks.rref(nb)[0]
            if R.shape[0] > B.shape[0]:
                key = tuple(map(tuple, R))
                if key not in out:
                    rec(R)
    rec(A)
    return out


def main():
    K = int(sys.argv[1]); want = sys.argv[2:]
    reps = ks.type_reps()
    for name, tau in reps.items():
        if want and name not in want:
            continue
        S = ks.star_block(tau); Kb = ks.nullspace(S); d = Kb.shape[0]; r = 12 - d
        if r > K:
            continue
        D = d - (12 - K)
        if D < 0:
            print(f'K={K} {name}: impossible (dim R > kernel)'); continue
        T = ks.functional_sets(tau, Kb)
        leaves = enumerate_A(T, d, D)
        feasible = 0; tested = 0
        for key in leaves:
            cands = [key] if len(key) == D else sorted(superspaces(key, d, D))
            for A_key in cands:
                tested += 1
                if exact_ok(tau, Kb, A_key):
                    feasible += 1
                    break
            if feasible:
                break
        print(f'K={K} type {name}: rank {r}, D={D}, DFS leaves {len(leaves)}, tested {tested}: '
              f'{"FEASIBLE (not excluded)" if feasible else "IMPOSSIBLE"}', flush=True)


if __name__ == '__main__':
    main()
