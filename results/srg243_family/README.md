# Four strongly regular graphs with parameters (243,22,1,2)

**Status: computational results of October 2026, awaiting independent mathematical review and a check of novelty.**
The standalone verifier checks the four graphs' SRG parameters, the listed grid counts, pairwise non-isomorphism,
the supplied automorphism generators, and the explicit BvLS Hoffman coclique witness. Its default mode uses only
the Python standard library:

```bash
python3 results/srg243_family/verify_family.py
```

With the repository's pinned Python dependencies installed, the extended mode also checks the full automorphism
group orders and vertex orbit sizes for all four graphs, the orders of the supplied generator groups for Γ₃ and Γ₄,
and agreement of their graph6 files with the edge lists:

```bash
python3 results/srg243_family/verify_family.py --full
```

Neither mode reproduces the cover-search classification, the Hoffman-coclique infeasibility searches, or the fixed-design
completion search described below. Those programs and records are available separately from the author on request.

Brouwer's table lists a single graph for these parameters (the Berlekamp–van Lint–Seidel graph) in its September 2026
snapshot. The manuscript [`papers/srg243_second`](../../papers/srg243_second) gives a second one. This folder adds two more.

| graph | file | \|Aut\| | vertex orbits | induced 3×3 grids |
|---|---|---:|---|---:|
| BvLS | `bvls243.edges` | 3,849,120 | 243 | 1,485 |
| second graph (manuscript) | `twin243.edges` | 4,320 | 3, 60, 180 | 405 |
| **Γ₄** (new) | `gamma4_aut3888.edges`, `.g6` | **3,888** | 81, 162 | 837 |
| **Γ₃** (new) | `gamma3_aut864.edges`, `.g6` | **864** | 27, 108, 108 | 621 |

- The four grid counts are distinct, so the four graphs are pairwise non-isomorphic.
- Full automorphism group orders are checked with nauty. For Γ₃ and Γ₄, the orders of the supplied generator groups are
  also checked by Schreier–Sims and must agree with the full group. Generators are supplied in `*.autgens` (images of
  0..242); their validity is checked even in the default mode.

## How Γ₃ and Γ₄ arise
All four graphs are 3-fold covers of the Brouwer–Haemers graph srg(81,20,1,6) along a regular spread, that is, a
partition of the 243 vertices into 81 triangles. The new graphs are obtained from BvLS by changing the Z₃-voltages of
this cover:
- Γ₄: the voltage changes are required to be invariant under the stabiliser of a non-adjacent pair of vertices of the
  Brouwer–Haemers graph;
- Γ₃: the voltage changes are invariant under the stabiliser of a line together with a point.

The author's separate cover-search computations report that, for each of these prescribed symmetry conditions,
the constraint system was solved completely, and every solution is isomorphic to one of the four graphs above.
This is a classification under those symmetry conditions, not of all graphs with these parameters.

Each of the four graphs keeps the order-3 symmetry of the cover. In particular, none of them is asymmetric.

## Hoffman cocliques: separately reported computational results
The Hoffman bound for these parameters is 45. A 45-vertex coclique C attains it iff every other vertex has exactly
5 neighbours in C. In that case the neighbourhoods form a 2-(45,5,2) design with 198 blocks.

- **BvLS has such cocliques.** One is given in `bvls243_hoffman_coclique.txt` and checked by the script. The solver found
  at least 1,691 of them.
- **The second graph, Γ₃ and Γ₄ have none, according to the separate exhaustive computations.** The CP-SAT search uses
  the exact formulation (A + 5I)x = 5·𝟏 with x ∈ {0,1}²⁴³; the recorded solver results are infeasible.
- **Reconstruction from the coclique.** Fix one such coclique of BvLS together with all its incidences, and solve for the
  other 198 vertices (81 % of the graph) exhaustively, with no symmetry or partition assumed. The result is exactly
  **one** completion: BvLS itself.

Among the four graphs supplied here, this tight structure is reported only in the most symmetric one. The completion
result fixes one particular BvLS 2-(45,5,2) design and all its incidences; it does not classify every possible such design.
The programs and records for these two computations are available from the author on request.
