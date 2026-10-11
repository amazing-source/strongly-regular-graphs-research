"""Reproduce the construction, orbit orders, line counts, and switching table.

This driver uses the unchanged source switching implementation and published
edge lists. It does not require private notes, cached solver output, or nauty CLI.
Run from any working directory: python3 reproduction/srg243_second/reproduce.py
"""
from collections import Counter
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import runpy
import sys

import networkx as nx
import numpy as np
import pynauty
import switch243 as sw

ROOT = Path(__file__).resolve().parents[2]
ANC = ROOT / "papers/srg243_second/anc"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def group(M):
    adj = {i: np.flatnonzero(M[i]).tolist() for i in range(len(M))}
    result = pynauty.autgrp(pynauty.Graph(len(M), adjacency_dict=adj))
    return round(result[1] * 10 ** result[2]), sorted(Counter(result[3]).values())


def grid_counts(path):
    argv = sys.argv
    try:
        sys.argv = [str(ANC / "verify_srg243.py"), str(path)]
        with redirect_stdout(StringIO()):
            result = runpy.run_path(str(ANC / "verify_srg243.py"))
        return result["g"]
    finally:
        sys.argv = argv


def line_counts(M):
    lines = [set(t) for t in sw.triangles(M)]
    counts = Counter()
    for i, a in enumerate(lines):
        for b in lines[i + 1:]:
            if not a & b:
                counts[sum(int(M[u, v]) for u in a for v in b)] += 1
    return counts


def main():
    old_path, new_path = ANC / "bvls243.edges", ANC / "srg243_new.edges"
    old, new = sw.load_edges(old_path), sw.load_edges(new_path)
    encoded = nx.from_graph6_bytes((ANC / "srg243_new.g6").read_bytes().strip())
    require(np.array_equal(nx.to_numpy_array(encoded, dtype=np.int64), new),
            "graph6 and edge-list encodings disagree")
    require(group(old) == (3849120, [243]), "unexpected BvLS automorphisms")
    require(group(new) == (4320, [3, 60, 180]), "unexpected new-graph automorphisms")
    print("graph6 encoding and both automorphism groups: OK", flush=True)

    old_lines, new_lines = line_counts(old), line_counts(new)
    require(old_lines[2] == 0 and old_lines[3] == 8910, "unexpected BvLS line counts")
    require(new_lines[2] == 19440 and new_lines[3] == 2430, "unexpected twisted line counts")
    print("two-edge line pairs: 19440; prisms: 2430 (BvLS: 8910): OK", flush=True)

    grids = grid_counts(new_path)
    triangles = sw.triangles(new)
    types = Counter(tuple(sorted(grids[v] for v in t)) for t in triangles)
    expected = {(55, 55, 55): 1, (19, 19, 55): 30, (19, 19, 19): 20,
                (13, 13, 19): 540, (13, 13, 13): 300}
    require(dict(types) == expected, "unexpected triangle-type counts")
    central = next(t for t in triangles if all(grids[v] == 55 for v in t))

    far, candidates = sw.row_candidates(old, central)
    require(len(far) == 180 and all(len(c) == 2 for c in candidates),
            "BvLS must have exactly two row solutions at each far vertex")
    rebuilt = old.copy()
    far_block = old[np.ix_(far, far)]
    for i, v in enumerate(far):
        actual = frozenset(np.flatnonzero(far_block[i]).tolist())
        require(actual in candidates[i], "true row missing from candidates")
        alternate = next(c for c in candidates[i] if c != actual)
        require(len(actual ^ alternate) == 16, "unexpected row change")
        rebuilt[v, far] = [int(j in alternate) for j in range(180)]
    require(np.array_equal(rebuilt, new), "reconstructed graph differs from published data")
    require(int(((new - old) == 1).sum()) == 1440 and
            int(((new - old) == -1).sum()) == 1440, "expected 720 added and removed edges")
    print("all 180 rows have two solutions; graph reconstructed exactly: OK", flush=True)

    for kind, count in sorted(expected.items()):
        triangle = next(t for t in triangles if tuple(sorted(grids[v] for v in t)) == kind)
        far, candidates = sw.row_candidates(new, triangle)
        choices = sw.consistent_choices(far, candidates, limit=50)
        require(len(choices) < 50, "enumeration cap reached; completeness unavailable")
        graphs = []
        for choice in choices:
            M = new.copy()
            for i, v in enumerate(far):
                M[v, far] = [int(j in candidates[i][choice[i]]) for j in range(len(far))]
            if sw.is_srg(M):
                graphs.append(M)
        require(any(np.array_equal(M, new) for M in graphs), "original graph missing")
        if kind == (55, 55, 55):
            require(len(graphs) == 2 and any(np.array_equal(M, old) for M in graphs),
                    "central triangle must recover both graphs")
        else:
            require(len(graphs) == 1, "unexpected additional strongly regular completion")
        print(f"switching type {kind}: {count} triangles; {len(graphs)} SRG completions: OK",
              flush=True)
    print("Construction and switching checks passed.")


if __name__ == "__main__":
    main()
