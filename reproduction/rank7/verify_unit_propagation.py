"""Check the rank-25 remark using the unchanged exact star CNF generator."""
import numpy as np
from pysat.solvers import Cadical153
import kbound_exact as exact
import kbound_star as star


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


class UnitOnly:
    calls = 0

    def __init__(self, bootstrap_with):
        self.solver = Cadical153(bootstrap_with=bootstrap_with)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.solver.delete()

    def solve(self):
        UnitOnly.calls += 1
        consistent, _ = self.solver.propagate()
        require(not consistent, "unit propagation did not refute this instance")
        return False


def main():
    exact.Cadical153 = UnitOnly
    for name, tau in star.type_reps().items():
        kernel = star.nullspace(star.star_block(tau))
        rank = 12 - len(kernel)
        if rank > 8:
            continue
        D = len(kernel) - 4
        leaves = exact.enumerate_A(star.functional_sets(tau, kernel), len(kernel), D)
        if name == "(0;2,2,2)":
            require(len(leaves) == 32 and all(len(A) == D for A in leaves),
                    "expected 32 maximal-dimensional candidate annihilators")
            for A in sorted(leaves):
                require(not exact.exact_ok(tau, kernel, A), "unexpected feasible instance")
        else:
            require(not leaves, f"unexpected surviving annihilator for {name}")
        print(f"K=8 {name}: {len(leaves)} candidate subspaces", flush=True)
    require(UnitOnly.calls == 32, "expected 32 CNF propagation checks")
    print("All 32 Boolean instances refuted by unit propagation: OK")


if __name__ == "__main__":
    main()
