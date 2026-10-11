"""Can the global 7-adic invariant k (L19/L20) take the value K?  Star-relation test (notes/97, L20 bis).

k = rank_7(M_x), M_x = H + 4I + 3S + P' + 5J (84 x 84 over F_7).  If k = K, every star block (rank r_a = 11 - 2e(tau_a))
has r_a <= K, and the star's full-row relations R_a = ker(V_a) (V = factor of M_x = V^T Q V) form a subspace of
ker(star block) of dimension >= 12 - K.  For c in R_a and every column z outside the star:
   z = {l,q} (a, abar not in z):  c_{b1} + c_{b2} + 3(c_l + c_q) + (c_lbar + c_qbar) + 5 sum(c) = 0
   z = {abar,q}:                  c_{b1} + 3 c_q + c_qbar + 6 sum(c) = 0
where {a,b1},{a,b2} (resp. {a,b1}) are z's neighbours in the star (unknown; b1 != b2 not tau_a-partners).
So Ann(R_a) (dim <= dim ker - (12 - K)) must meet, for every z, the finite set T_z of possible functionals.
If no subspace of that dimension meets all T_z, the star type is impossible for k = K; if all admissible types are
impossible, k != K.  (Relaxation: global degree constraints on the b's are not used, so 'impossible' is sound.)
Usage: kbound_star.py K
"""
import sys, itertools
import numpy as np

p = 7
labels = [(c, s) for c in range(7) for s in (0, 1)]
mate = lambda l: (l[0], 1 - l[1])
a = (0, 0); abar = mate(a)
others = [l for l in labels if l[0] != 0]          # star indices
oi = {l: i for i, l in enumerate(others)}


def rref(M):
    M = M.copy() % p; r = 0; piv = []
    for c in range(M.shape[1]):
        rows = [i for i in range(r, M.shape[0]) if M[i, c]]
        if not rows:
            continue
        M[[r, rows[0]]] = M[[rows[0], r]]
        M[r] = (M[r] * pow(int(M[r, c]), -1, p)) % p
        for i in range(M.shape[0]):
            if i != r and M[i, c]:
                M[i] = (M[i] - M[i, c] * M[r]) % p
        piv.append(c); r += 1
    return M[:r], piv


def nullspace(M):
    R, piv = rref(M)
    n = M.shape[1]; free = [c for c in range(n) if c not in piv]
    basis = []
    for f in free:
        v = np.zeros(n, dtype=np.int64); v[f] = 1
        for i, c in enumerate(piv):
            v[c] = (-R[i, f]) % p
        basis.append(v)
    return np.array(basis, dtype=np.int64)


def type_reps():
    """one tau_a per class type with small rank: dict name -> matching dict"""
    reps = {}
    def pairs_to_tau(pairs):
        t = {}
        for b, c in pairs:
            t[b], t[c] = c, b
        return t
    # (0;2,2,2): swap classes 1<->2, 3<->4, 5<->6 sign-preserving
    reps['(0;2,2,2)'] = pairs_to_tau([((1, s), (2, s)) for s in (0, 1)] + [((3, s), (4, s)) for s in (0, 1)] + [((5, s), (6, s)) for s in (0, 1)])
    # (0;2,4): swap 1<->2; 4-cycle on classes 3,4,5,6: (3,0)-(4,0), (4,1)-(5,0), (5,1)-(6,0), (6,1)-(3,1)
    reps['(0;2,4)'] = pairs_to_tau([((1, s), (2, s)) for s in (0, 1)] + [((3, 0), (4, 0)), ((4, 1), (5, 0)), ((5, 1), (6, 0)), ((6, 1), (3, 1))])
    # (2;2,2): classes 1,2 untwisted (mates), swap 3<->4, 5<->6
    reps['(2;2,2)'] = pairs_to_tau([((1, 0), (1, 1)), ((2, 0), (2, 1))] + [((3, s), (4, s)) for s in (0, 1)] + [((5, s), (6, s)) for s in (0, 1)])
    # rank-9 types (for K >= 10): (0;6), (1;2,3), (2;4), (4;2)
    reps['(0;6)'] = pairs_to_tau([((1, 0), (2, 0)), ((2, 1), (3, 0)), ((3, 1), (4, 0)), ((4, 1), (5, 0)), ((5, 1), (6, 0)), ((6, 1), (1, 1))])
    reps['(1;2,3)'] = pairs_to_tau([((1, 0), (1, 1)), ((2, 0), (3, 0)), ((2, 1), (3, 1)), ((4, 0), (5, 0)), ((5, 1), (6, 0)), ((6, 1), (4, 1))])
    reps['(2;4)'] = pairs_to_tau([((1, 0), (1, 1)), ((2, 0), (2, 1)), ((3, 0), (4, 0)), ((4, 1), (5, 0)), ((5, 1), (6, 0)), ((6, 1), (3, 1))])
    reps['(4;2)'] = pairs_to_tau([((1, 0), (1, 1)), ((2, 0), (2, 1)), ((3, 0), (3, 1)), ((4, 0), (4, 1)), ((5, 0), (6, 0)), ((5, 1), (6, 1))])
    return reps


def star_block(tau):
    S = np.zeros((12, 12), dtype=np.int64)
    for b in others:
        for c in others:
            if b == c:
                S[oi[b], oi[c]] = 1
            else:
                S[oi[b], oi[c]] = (int(tau[b] == c) + int(mate(b) == c) + 1) % p
    return S


def functional_sets(tau, Kb):
    """For each column z outside the star: array of candidate functionals (values on the kernel basis Kb)."""
    d = Kb.shape[0]
    cval = {b: Kb[:, oi[b]] for b in others}          # c_b as functional (vector of length d)
    ssum = Kb.sum(axis=1) % p                          # sum(c)
    T = []
    # generic z = {l, q}, a, abar not in z
    for l, q in itertools.combinations(others, 2):
        if l[0] == q[0]:
            continue
        base = (3 * (cval[l] + cval[q]) + cval[mate(l)] + cval[mate(q)] + 5 * ssum) % p
        cands = set()
        for b1, b2 in itertools.combinations(others, 2):
            if tau[b1] == b2:
                continue
            cands.add(tuple((base + cval[b1] + cval[b2]) % p))
        T.append(np.array(sorted(cands), dtype=np.int64))
    # z = {abar, q}
    for q in others:
        base = (3 * cval[q] + cval[mate(q)] + 6 * ssum) % p
        cands = {tuple((base + cval[b]) % p) for b in others}
        T.append(np.array(sorted(cands), dtype=np.int64))
    return T


def exists_subspace(T, d, D):
    """Is there a subspace A of F_7^d with dim A <= D meeting every set in T?  Depth-first with pruning."""
    zero = np.zeros(d, dtype=np.int64)
    if any((t == 0).all(axis=1).any() for t in T):
        T = [t for t in T if not (t == 0).all(axis=1).any()]
    seen = set()

    def meets(basis, t):
        if basis.shape[0] == 0:
            return False
        # t (m x d) in span(basis)?  rank test via projection onto complement
        M = np.concatenate([basis, t], axis=0) % p
        R, piv = rref(basis)
        # reduce each row of t by R
        tt = t.copy() % p
        for i, c in enumerate(piv):
            coef = tt[:, c].copy()
            tt = (tt - np.outer(coef, R[i])) % p
        return (tt == 0).all(axis=1).any()

    def rec(basis):
        key = tuple(map(tuple, rref(basis)[0])) if basis.shape[0] else ()
        if key in seen:
            return False
        seen.add(key)
        unmet = [t for t in T if not meets(basis, t)]
        if not unmet:
            return True
        if basis.shape[0] >= D:
            return False
        t = min(unmet, key=len)
        for v in t:
            nb = np.concatenate([basis, v[None, :]], axis=0) if basis.shape[0] else v[None, :]
            if rref(nb)[0].shape[0] > basis.shape[0]:
                if rec(rref(nb)[0]):
                    return True
        return False
    return rec(np.zeros((0, d), dtype=np.int64))


def main():
    K = int(sys.argv[1])
    reps = type_reps()
    for name, tau in reps.items():
        assert all(tau[tau[b]] == b and tau[b] != b for b in others)
        S = star_block(tau)
        Kb = nullspace(S)                   # kernel basis, shape (d, 12)
        r = 12 - Kb.shape[0]
        if r > K:
            continue
        D = Kb.shape[0] - (12 - K)          # max dim of Ann(R)
        if D < 0:
            print(f'{name}: rank {r}, kernel {Kb.shape[0]}: dim R >= {12-K} exceeds kernel -> impossible'); continue
        T = functional_sets(tau, Kb)
        ok = exists_subspace(T, Kb.shape[0], D)
        print(f'K={K} type {name}: star rank {r}, kernel dim {Kb.shape[0]}, need Ann(R) of dim <= {D}: '
              f'{"POSSIBLE (not excluded)" if ok else "IMPOSSIBLE"}', flush=True)


if __name__ == '__main__':
    main()
