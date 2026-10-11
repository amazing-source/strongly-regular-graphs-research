# Strongly Regular Graphs Research

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23305123.svg)](https://doi.org/10.5281/zenodo.23305123)

Research manuscripts by **Dilan Djematene** ([ORCID 0009-0009-2947-7746](https://orcid.org/0009-0009-2947-7746)), with their LaTeX sources, PDFs, graph data, and executable verification material.

**Status: research manuscripts awaiting independent review.** The results below are the claims of the manuscripts. The included verification programs reproduce the public finite checks described below; some Conway computations and formal proofs are available separately from the author. These checks do not replace independent review of the proofs, novelty, or literature context. The existence of a strongly regular graph with parameters `(99,14,1,2)` remains open.

## Conway's 99-graph: the automorphism group

A Conway 99-graph is a strongly regular graph with parameters `(99,14,1,2)`; its existence is open. Published work
(Makhnev–Minakova 2004, Behbahani–Lam 2011, Crnković–Maksimović 2020, Cesarz–Woldar 2025) leaves `|Aut| ∈ {1, 2, 3}`.
The manuscripts below exclude the remaining cases. Together they give: **a Conway 99-graph, if it exists, is asymmetric.**

| Document | Claim | Method | Status | Files |
| --- | --- | --- | --- | --- |
| *A Conway 99-graph, if it exists, is asymmetric: statement and dependencies* | `Aut(Γ)` is trivial, assembled prime by prime from the results below and the literature | short note, no new mathematics | assembled result; awaiting independent review; see the C2 version note below | [PDF](papers/conway99_asymmetric/asymmetric.pdf) · [LaTeX](papers/conway99_asymmetric/asymmetric.tex) |
| *A strongly regular graph with parameters (99,14,1,2) has no automorphism of order two* | no involution | first half by hand (an involution gives a 51-vector frame in one of Borcherds' 156 odd unimodular lattices of rank 24); second half computer-assisted, lattice by lattice | computer-assisted proof; the author reports the transfer check completed in the 11 October 2026 status update; not refereed | [PDF](papers/conway99_order2/order2.pdf) · [LaTeX](papers/conway99_order2/order2.tex) |
| *Le graphe de Conway srg(99,14,1,2) n'a pas d'automorphisme d'ordre 3* (in French) | no automorphism of order 3 | by hand: discriminants of eigenvector lattices over ℤ and the Eisenstein integers | **formalised in Lean 4 / Mathlib** (no `sorry`, standard axioms, `lake comparator`); not refereed | [PDF](papers/conway99_order3/preuve_c3.pdf) · [LaTeX](papers/conway99_order3/preuve_c3.tex) |
| *A computer-free proof that a Conway 99-graph has no automorphism of order seven* | no automorphism of order 7 (previously known only by computer, Behbahani–Lam) | by hand, completing the framework of Cesarz–Woldar | **formalised in Lean 4 / Mathlib**; not refereed | [PDF](papers/conway99_order7/order7.pdf) · [LaTeX](papers/conway99_order7/order7.tex) |

The programs, records and certificates of the order-2 computation (including a 90-page supplement with the three
computer-assisted lemmas), and the Lean formalisations of orders 3 and 7, are kept in private repositories and are
available from the author on request.

**C2 version note (11 October 2026).** The author confirms that the transfer-pair check has been completed.
The supplied order-2 manuscript and combined note retain their earlier version wording about pending validation;
their mathematical text and PDFs have been preserved unchanged. Reviewers should request the latest check records
alongside these manuscripts. This README records the author's updated status, rather than a new independent audit
of that computation.

## Further results on (243,22,1,2) (October 2026)

[`results/srg243_family/`](results/srg243_family) adds **two more strongly regular graphs with parameters (243,22,1,2)**:
- Γ₃, with |Aut| = 864;
- Γ₄, with |Aut| = 3,888.

The four supplied graphs are pairwise non-isomorphic. A standalone verifier checks their parameters and distinct
grid counts, the supplied generators, and one BvLS Hoffman coclique. Its `--full` option also checks full automorphism
group orders, vertex orbits, and the supplied graph6 files.

Separate computational results report that, among these four graphs, only BvLS contains a Hoffman coclique (45
vertices), and that one fixed BvLS coclique and its full incidence design determine the remaining 198 vertices uniquely.
The programs and records for these two exhaustive computations are available from the author on request; they are
outside the public verification suite. The reconstruction statement concerns the supplied fixed design, rather than
a classification of all possible Hoffman coclique designs.

## Other manuscripts

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

It checks the four supplied SRG edge lists and grid counts, the family generators and BvLS coclique witness, the historical table and its agreement with the manuscript's list, all star ranks, the 32 unit-propagation refutations, and both original hexagon counts. It exits with an error if an expected check fails. Compiled executables are placed in a temporary directory.

To additionally check graph6 agreement, all four automorphism groups and vertex orbits, line-pair counts for the original two graphs, the reconstruction of the second graph from all 180 row enumerations, and one representative of each triangle switching type:

```bash
python reproduction/verify_all.py --full
```

The full run performs exhaustive CP-SAT enumerations and takes longer. The switching-table computation, like the manuscript's table, tests one triangle representative of each listed type. Automorphism orders are computed with nauty through `pynauty`; the publication driver does not require a separate nauty command-line installation.

The family checks can also be run separately:

```bash
python results/srg243_family/verify_family.py
python results/srg243_family/verify_family.py --full
```

The default family check needs only the Python standard library. The extended check uses the pinned NetworkX,
pynauty and SymPy dependencies. Neither command checks the Conway C2 computation or Lean proofs, the cover-search
classification, the absence of Hoffman cocliques in the other three graphs, or the unique-completion computation.

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

The supplied PDFs are the original manuscript versions. To build separate copies, install a TeX distribution with `amsart`, `amsmath`, `amssymb`, `booktabs`, `hyperref`, `tikz`, `cleveref` and French `babel` support, then run:

```bash
mkdir -p build
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=build papers/srg243_second/srg243_second.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=build papers/s5_2adic/s5_2adic.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=build papers/rank7/rank7.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=build papers/conway99_asymmetric/asymmetric.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=build papers/conway99_order3/preuve_c3.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=build papers/conway99_order7/order7.tex
(cd papers/conway99_order2 && pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error -output-directory=../../build order2.tex)  # uses table156.tex
```

Run each command twice to resolve references. The manuscripts use `\today`, so rebuilding may change the displayed date. All bibliographies are embedded in the LaTeX sources; no separate bibliography database or external figures are needed.

## Contents and provenance

The original three paper directories (`srg243_second`, `s5_2adic`, `rank7`) contain all their original files.
[PROVENANCE.json](PROVENANCE.json) records their Git blob hashes and the pinned source snapshot so byte-level integrity
can be checked. The Conway manuscripts and graph-family data were added in the subsequent
[11 October publication commit](https://github.com/amazing-source/strongly-regular-graphs-research/commit/6711f1802a8dbe24c268ae6a7201967142735e56).
The repository starts with its own publication history.

Additional material is limited to reproducibility dependencies:

- `data/brouwer/`: the 26 historical HTML table pages required by the 2-adic verifier. These are reference data, credited to A. E. Brouwer's [strongly regular graph tables](https://aeb.win.tue.nl/graphs/srg/srgtab.html), rather than experimental run logs.
- `reproduction/rank7/`: the original star-relation and exact enumeration implementations, with a driver that checks the unit-propagation claim without loading private cache files.
- `reproduction/srg243_second/`: the original triangle switching implementation and a driver that uses the published edge lists and portable dependencies.
- `reproduction/verify_all.py`: an assertion-based runner for the documented checks.

The mathematical content of the papers has not been changed. Their existing acknowledgements of assistance from Claude (Anthropic) are retained. For the four Conway 99-graph documents, the only changes from the author's private originals are: the author line (AI assistance is declared in a dedicated section of each text instead), links to private repositories replaced by "available on request", and, for the order-3 text, a font package so that it compiles with pdfLaTeX. Computational checks support the stated finite results; the general lattice arguments, switching rigidity proof, and claims of novelty remain subject to independent mathematical review. Corrections and reproducible review findings are welcome through GitHub issues.

## License and citation

The author's material is licensed under [CC BY 4.0](LICENSE.md). The exception is the third-party snapshot in
`data/brouwer/`. Each release of this repository is archived on Zenodo with a permanent DOI. Please cite:

> D. Djematene, *Strongly regular graphs: the automorphism group of a Conway 99-graph, new graphs with parameters
> (243,22,1,2), and a 2-adic feasibility condition*, version v1.0, Zenodo, 11 October 2026.
> [doi:10.5281/zenodo.23305123](https://doi.org/10.5281/zenodo.23305123)

All versions: [doi:10.5281/zenodo.23305122](https://doi.org/10.5281/zenodo.23305122).

## Author and contact

I pursue this research independently. I would be very
grateful for any of the following:
- independent review of any of these manuscripts;
- advice on where and how to publish them;
- mentoring or supervision.

Corrections and comments are welcome through GitHub issues, or at the correspondence address given in the manuscripts.
