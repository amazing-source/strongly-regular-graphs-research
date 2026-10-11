"""Checks for 'The 7-rank of a putative srg(99,14,1,2)':
(1) the windmill block F-3I (closed neighbourhood of a vertex) and its inverse, exactly;
(2) the Schur complement formula mod 7 for two second-neighbourhood vertices y={a,b}, z={c,d}:
    -B^T (F-3I)^{-1} B [y,z] = 4 s + 6 p' + 2 - 3 [y=z]... (we test the full local matrix formula of Lemma 4);
(3) rank_7 of the star block H_tau + P' + J is 11 - 2 e(tau) for all 10395 matchings tau of the 12 labels;
(4) the genus arithmetic of Section 2."""
import itertools, sympy as sp
from fractions import Fraction

# (1) windmill: vertex 0 = x, labels 1..14 with mates (2i-1, 2i)
n = 15
F = sp.zeros(n)
for i in range(1, 15):
    F[0, i] = F[i, 0] = 1
for i in range(1, 15, 2):
    F[i, i + 1] = F[i + 1, i] = 1
W = F - 3 * sp.eye(n)
print("det(F-3I) =", sp.factorint(W.det()), " invertible mod 7:", W.det() % 7 != 0)
Winv = W.inv()
P = sp.zeros(14)
for i in range(0, 14, 2): P[i, i + 1] = P[i + 1, i] = 1
G_claim = -sp.Rational(3, 8) * sp.eye(14) - sp.Rational(1, 8) * P + sp.ones(14) / 16
print("label block of (F-3I)^{-1} equals -(3/8)I - (1/8)P + J/16:", Winv[1:, 1:] == G_claim)

# (2) Schur complement: for y={a,b}, z={c,d} (non-mate pairs), the correction C0[y,z] = (e_a+e_b)^T G (e_c+e_d)
def mod7(q): q = sp.Rational(q); return (q.p * pow(q.q, -1, 7)) % 7
labels = [(a, b) for a in range(14) for b in range(a + 1, 14) if not (a // 2 == b // 2)]
assert len(labels) == 84
bad = 0
for (a, b), (c, d) in itertools.product(labels, repeat=2):
    C0 = sum(G_claim[i, j] for i in (a, b) for j in (c, d))
    s = len({a, b} & {c, d}); pp = sum(1 for i in (a, b) for j in (c, d) if i // 2 == j // 2 and i != j)
    if mod7(C0) != (4 * s + 6 * pp + 2) % 7: bad += 1
print("C0[y,z] == 4 s + 6 p' + 2 (mod 7) for all 84^2 pairs:", bad == 0)

# (3) star ranks: star(a) = 12 labels {a,b}; matrix H_tau + P' + J over F7 where P' pairs b with mate(b)
def rank7(M):
    M = [[x % 7 for x in row] for row in M]; r = 0; rows, cols = len(M), len(M[0])
    for c in range(cols):
        p = next((i for i in range(r, rows) if M[i][c]), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]; inv = pow(M[r][c], -1, 7)
        M[r] = [(x * inv) % 7 for x in M[r]]
        for i in range(rows):
            if i != r and M[i][c]:
                f = M[i][c]; M[i] = [(x - f * y) % 7 for x, y in zip(M[i], M[r])]
        r += 1
    return r
def matchings(items):
    if not items: yield []; return
    a = items[0]
    for j in range(1, len(items)):
        for rest in matchings(items[1:j] + items[j + 1:]): yield [(a, items[j])] + rest
others = list(range(12))            # the 12 labels b of star(a): mates are (2i, 2i+1) -> 6 classes
mate = lambda b: b ^ 1
from collections import Counter
cnt = Counter(); ok = True
for mt in matchings(others):
    tau = {}
    for u, w in mt: tau[u] = w; tau[w] = u
    M = [[(1 if tau[i] == j else 0) + (1 if mate(i) == j else 0) + 1 for j in range(12)] for i in range(12)]
    # class graph: classes c=b//2, edges from tau; e = number of even-length cycles (2-cycles count, loops do not)
    seen = set(); e = 0
    for c0 in range(6):
        if c0 in seen: continue
        # walk: from class c take label 2c, go tau, move to the other label of that class, ...
        length = 0; b = 2 * c0; start = b
        while True:
            seen.add(b // 2); b2 = tau[b]; length += 1
            if b2 // 2 == b // 2 and length == 1: break      # loop (untwisted class)
            b = mate(b2)
            if b == start: break
        if not (tau[2 * c0] // 2 == c0) and length % 2 == 0: e += 1
    r = rank7(M); cnt[(r, e)] += 1
    ok &= (r == 11 - 2 * e)
print("rank_7(H_tau + P' + J) = 11 - 2 e(tau) for all", sum(cnt.values()), "matchings:", ok, dict(cnt))

# (4) genus arithmetic: oddity 0, 3-excess of 9^{+-1}: 1*(9-1)=8, 7-excess of 7^{eps*alpha}: 6 alpha + 4 delta
for k in range(0, 31):
    alpha = 14 + k
    sols = [delta for delta in (0, 1) if (44 + 8 + 6 * alpha + 4 * delta) % 8 == 0]
    # k=30: U=0 so (det V|7)=(9|7)=+1 forces delta=0
    if k == 30: sols = [d for d in sols if d == 0]
    if sols: print("k =", k, "allowed (delta_V in", sols, ")", end="; ")
print()
