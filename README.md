# Strongly Regular Graphs Research

Research manuscripts by **Dilan Djematene**, with their LaTeX sources, PDFs, graph data, and executable verification material.

**Status: research manuscripts awaiting independent review.** The results below are the claims of the manuscripts. The accompanying computations reproduce their finite checks; they do not replace independent review of the proofs, novelty, or literature context. This repository does not claim to settle the existence of a strongly regular graph with parameters `(99,14,1,2)`.

## Manuscripts

| Paper | Main claims | Files |
| --- | --- | --- |
| *A second strongly regular graph with parameters (243,22,1,2)* | Constructs a graph not isomorphic to the Berlekamp–van Lint–Seidel graph; gives its automorphism group and local grid counts; presents a counterexample to Reimbayev's hexagon conjecture and a rigidity result for nontrivial Godsil–McKay switching. | [PDF](papers/srg243_second/srg243_second.pdf) · [LaTeX](papers/srg243_second/srg243_second.tex) · [Ancillary files](papers/srg243_second/anc/) |
| *A 2-adic nonexistence condition for strongly regular graphs* | Derives a feasibility condition from integral eigenvalue lattices; applies it to 35 parameter sets marked open in a September 2026 table snapshot, an infinite negative Latin square type family, and `pg(14,14,4)`. | [PDF](papers/s5_2adic/s5_2adic.pdf) · [LaTeX](papers/s5_2adic/s5_2adic.tex) · [Verifier](papers/s5_2adic/verify_s5.py) |
| *On the 7-rank of a putative strongly regular graph with parameters (99,14,1,2)* | Proves that `rank₇(A − 3I)` is odd and lies between 23 and 43; an additional finite computation raises the lower bound to 25. Gives an exact local Schur complement formula and star-rank formula. | [PDF](papers/rank7/rank7.pdf) · [LaTeX](papers/rank7/rank7.tex) · [Verifier](papers/rank7/verify_rank7.py) |

### The second graph on 243 vertices

The construction replaces the subgraph on the 180 vertices at distance two from a chosen triangle in the Berlekamp–van Lint–Seidel graph (BvLS). The explicit edge list allows the claimed strongly regular parameters to be checked directly on every pair of vertices.

| Invariant | New graph | BvLS |
| --- | ---: | ---: |
| Vertices / degree / λ / μ | 243 / 22 / 1 / 2 | 243 / 22 / 1 / 2 |
| Automorphism group order | 4,320 | 3,849,120 |
| Vertex orbit sizes | 3, 60, 180 | 243 |
| Induced 3×3 grids | 405 | 1,485 |
| Grids through a vertex | 13 on 180 vertices; 19 on 60; 55 on 3 | 55 on all vertices |
| Induced hexagons | 5,000,130 | 4,980,690 |
| Disjoint triangle pairs joined by two edges | 19,440 | 0 |
| Disjoint triangle pairs joined by three edges | 2,430 | 8,910 |

The differing grid distributions certify that the supplied graphs are not isomorphic. The manuscript compares the hexagon counts with the bound `4,980,690` and describes the triangle switching class. The graph is supplied in both graph6 and edge-list formats; edge-list vertex labels are `0,...,242`.

### The 2-adic condition

For integral nonprincipal eigenvalues `r > s` with odd difference, the paper studies the lattices `ℤᵛ ∩ ker(A − θI)`. Under its stated 2-adic hypothesis, evenness and odd determinant impose a congruence modulo four. The arithmetic verifier applies this criterion to a fixed historical table rather than relying on a changing live website.

The included snapshot has 4,538 rows, including complements: 1,183 marked as existing, 2,889 unknown, and 466 nonexistent. The verifier excludes no row marked as existing and reproduces the 35 primary unknown rows listed in the manuscript. These status labels describe the historical snapshot, not current classification claims.

### The 7-rank condition

For a hypothetical adjacency matrix `A` with parameters `(99,14,1,2)`, the paper obtains the oddness and upper bound from the genus of the integral `−4` eigenvalue lattice. A local decomposition around any vertex reduces the rank to `15 + rank₇(Mₓ)` for an explicit 84×84 matrix.

The original verifier checks the windmill inverse, all `84²` local correction entries, the star formula over all 10,395 perfect matchings, and the genus arithmetic. The supplementary scripts reproduce the stronger bound: two admissible star types have no candidate subspaces; the remaining type has 32 candidates, whose Boolean constraints are each refuted by unit propagation.

## Reproducing the computations

Use **Python 3.12** (the tested version) and a **C99 compiler** such as GCC or Clang. Install the pinned Python dependencies in an isolated environment:

```bash
git clone https://github.com/amazing-source/strongly-regular-graphs-research.git
cd strongly-regular-graphs-research
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate with `.venv\Scripts\activate` and ensure a C compiler is on `PATH`.

Run the main verification suite:

```bash
python reproduction/verify_all.py
```

It checks the supplied edge lists, both SRG and grid verifiers, the historical table and its agreement with the manuscript's list, all star ranks, the 32 unit-propagation refutations, and both hexagon counts. It exits with an error if an expected check fails. Compiled executables are placed in a temporary directory.

To additionally check graph6 agreement, both automorphism groups, line-pair counts, the reconstruction of the new graph from all 180 row enumerations, and one representative of each triangle switching type:

```bash
python reproduction/verify_all.py --full
```

The full run performs exhaustive CP-SAT enumerations and takes longer. The switching-table computation, like the manuscript's table, tests one triangle representative of each listed type. Automorphism orders are computed with nauty through `pynauty`; the publication driver does not require a separate nauty command-line installation.

### Original verification commands

All commands below are run from the repository root. The original manuscript verifiers are preserved unchanged.

```bash
python papers/srg243_second/anc/verify_srg243.py papers/srg243_second/anc/srg243_new.edges
python papers/srg243_second/anc/verify_srg243.py papers/srg243_second/anc/bvls243.edges
cc -O3 -std=c99 papers/srg243_second/anc/hexagons.c -o hexagons
./hexagons papers/srg243_second/anc/srg243_new.edges 243 22
./hexagons papers/srg243_second/anc/bvls243.edges 243 22
```

```bash
python papers/s5_2adic/verify_s5.py data/brouwer
python papers/rank7/verify_rank7.py
python reproduction/rank7/kbound_exact.py 8
python reproduction/rank7/verify_unit_propagation.py
```

`verify_s5.py` and `verify_srg243.py` use only the Python standard library. `verify_rank7.py` requires SymPy. The stronger rank computation uses NumPy and Python-SAT with CaDiCaL. The full graph construction uses NumPy, OR-Tools, NetworkX, and pynauty. Versions tested for this release are pinned in [requirements.txt](requirements.txt).

## Building the manuscripts

The supplied PDFs are the original manuscript versions. To build separate copies, install a TeX distribution with `amsart`, `amsmath`, `amssymb`, `booktabs`, and `hyperref`, then run:

```bash
mkdir -p build
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=build papers/srg243_second/srg243_second.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=build papers/s5_2adic/s5_2adic.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=build papers/rank7/rank7.tex
```

Run each command twice to resolve references. The manuscripts use `\today`, so rebuilding may change the displayed date. All bibliographies are embedded in the LaTeX sources; no separate bibliography database or external figures are needed.

## Contents and provenance

The three paper directories contain all their original files. [PROVENANCE.json](PROVENANCE.json) records their Git blob hashes and the pinned source snapshot so byte-level integrity can be checked. The repository starts with its own publication history.

Additional material is limited to reproducibility dependencies:

- `data/brouwer/`: the 26 historical HTML table pages required by the 2-adic verifier. These are reference data, credited to A. E. Brouwer's [strongly regular graph tables](https://aeb.win.tue.nl/graphs/srg/srgtab.html), rather than experimental run logs.
- `reproduction/rank7/`: the original star-relation and exact enumeration implementations, with a driver that checks the unit-propagation claim without loading private cache files.
- `reproduction/srg243_second/`: the original triangle switching implementation and a driver that uses the published edge lists and portable dependencies.
- `reproduction/verify_all.py`: an assertion-based runner for the documented checks.

The mathematical content of the papers has not been changed. Their existing acknowledgements of assistance from Claude (Anthropic) are retained. Computational checks support the stated finite results; the general lattice arguments, switching rigidity proof, and claims of novelty remain subject to independent mathematical review. Corrections and reproducible review findings are welcome through GitHub issues.
