"""Independent implementation of the 2-adic criterion (Theorem 1 of s5_2adic.tex) and cross-check against the rows of
Brouwer's table (v <= 1300, HTML snapshot of 26/09/2026 in conway99-structures-lab/logs/brouwer).
Usage: python3 verify_s5.py BROUWER_HTML_DIR"""
import sys, glob, re, math
from fractions import Fraction


def vp(n, p):
    n = abs(n); c = 0
    if n == 0: return 99
    while n % p == 0: n //= p; c += 1
    return c


def primes(n):
    n = abs(n); out = []; p = 2
    while p * p <= n:
        if n % p == 0:
            out.append(p)
            while n % p == 0: n //= p
        p += 1
    if n > 1: out.append(n)
    return out


def eig(v, k, l, mu):
    D = (l - mu) ** 2 + 4 * (k - mu); d = math.isqrt(D)
    if d * d != D: return None                     # conference graph, irrational eigenvalues
    r, s = ((l - mu) + d), ((l - mu) - d)
    if r % 2 or s % 2: return None
    r //= 2; s //= 2
    g = Fraction(k * (r + 1) * (k - r), (k + r * s) * (r - s)) if (k + r * s) != 0 else None   # mult of s
    if g is None or g.denominator != 1: return None
    g = int(g); f = v - 1 - g
    return r, s, f, g


def excluded(v, k, l, mu):
    """True if Theorem 1 / Corollary excludes srg(v,k,l,mu); returns (True, theta, reason) or (False, ...)"""
    e = eig(v, k, l, mu)
    if e is None: return (False, None, "no integral eigenvalues")
    r, s, f, g = e; d = r - s
    if d % 2 == 0: return (False, None, "d even")
    for th, thp, m in ((r, s, f), (s, r, g)):
        if vp(k - thp, 2) < vp(v, 2): continue
        if m % 2: return (True, th, f"multiplicity {m} odd")
        if all(q % 4 == 1 for q in primes(d)):
            P = 1
            for q in primes(v):
                if d % q and vp(k - thp, q) < vp(v, q): P *= q ** vp(v, q)
            if ((-1) ** (m // 2) * P) % 4 != 1:
                return (True, th, f"m={m}, P={P}: (-1)^(m/2) P = {(-1) ** (m // 2) * P} not 1 mod 4")
    return (False, None, "")


def parse(dirpath):
    rows = []
    for path in sorted(glob.glob(dirpath + "/srgtab*-*.html")):
        html = open(path, encoding="utf-8", errors="replace").read(); vcur = None
        for m in re.finditer(r'<tr bgcolor="(#[0-9a-f]+)">(.*?)</tr>', html, re.S):
            colour, body = m.group(1), m.group(2)
            cells = [re.sub(r"<.*?>", "", c).replace("&nbsp;", "").strip() for c in re.findall(r"<td>(.*?)</td>", body, re.S)]
            if len(cells) < 5: continue
            if cells[1]: vcur = int(cells[1])
            try: k, l, mu = int(cells[2]), int(cells[3]), int(cells[4])
            except ValueError: continue
            st = {"#b0ffb0": "exists", "#ffffb0": "unknown", "#ffb0b0": "no"}.get(colour, colour)
            rows.append((vcur, k, l, mu, st, bool(cells[1]), cells[7] if len(cells) > 7 else ""))
    return rows


if __name__ == "__main__":
    rows = parse(sys.argv[1])
    print("rows:", len(rows), {s: sum(r[4] == s for r in rows) for s in ("exists", "unknown", "no")})
    bad = [r for r in rows if r[4] == "exists" and excluded(*r[:4])[0]]
    print("existing graphs excluded (must be 0):", len(bad), bad[:5])
    for st in ("unknown", "no"):
        lst = [r for r in rows if r[5] and r[4] == st and excluded(*r[:4])[0]]
        print(f"main rows with status '{st}' excluded: {len(lst)}")
        for r in lst:
            print("   srg(%d,%d,%d,%d)" % r[:4], "|", excluded(*r[:4])[2], "|", r[6][:60])
    comp = [r for r in rows if not r[5] and excluded(*r[:4])[0]]
    print("complement rows excluded:", len(comp))
    # infinite family NL_e(n): v=n^2, k=e(n+1), l=-n+e^2+3e, mu=e^2+e
    print("NL_e(n) checks:", [(e, n, excluded(n * n, e * (n + 1), -n + e * e + 3 * e, e * e + e)[0])
                              for n in (5, 13, 17, 25) for e in (1, 2, 3, 4, 5) if e * e + e > 0 and -n + e * e + 3 * e >= 0])
    print("pg(14,14,4) point graph srg(750,210,55,60):", excluded(750, 210, 55, 60))
