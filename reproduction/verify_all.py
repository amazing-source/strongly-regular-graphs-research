"""Run the published verification suite and fail on unexpected results."""
from pathlib import Path
import argparse
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def run(args):
    result = subprocess.run(args, cwd=ROOT, check=True, capture_output=True, text=True)
    print(result.stdout, end="", flush=True)
    return result.stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--full", action="store_true",
                        help="also enumerate the construction and switching table with CP-SAT")
    args = parser.parse_args()
    py = sys.executable
    family_args = [py, "results/srg243_family/verify_family.py"]
    if args.full:
        family_args.append("--full")
    run(family_args)
    anc = ROOT / "papers/srg243_second/anc"
    for name, distribution, total in [
        ("srg243_new.edges", "{13: 180, 19: 60, 55: 3}", 405),
        ("bvls243.edges", "{55: 243}", 1485),
    ]:
        seen = set()
        for line in (anc / name).read_text().splitlines():
            u, v = map(int, line.split())
            require(0 <= u < v < 243 and (u, v) not in seen, "invalid or duplicate edge")
            seen.add((u, v))
        require(len(seen) == 2673, "unexpected edge count")
        output = run([py, str(anc / "verify_srg243.py"), str(anc / name)])
        require("srg(243,22,1,2): OK" in output and distribution in output and
                f"total: {total}" in output, "unexpected SRG/grid verification output")

    html = ROOT / "data/brouwer"
    require(len(list(html.glob("srgtab*-*.html"))) == 26, "missing historical table pages")
    output = run([py, "papers/s5_2adic/verify_s5.py", str(html)])
    require("rows: 4538" in output and "existing graphs excluded (must be 0): 0 []" in output and
            "main rows with status 'unknown' excluded: 35" in output and
            "main rows with status 'no' excluded: 2" in output and
            "complement rows excluded: 37" in output, "unexpected 2-adic table results")
    manuscript = (ROOT / "papers/s5_2adic/s5_2adic.tex").read_text()
    table = manuscript.split("\\midrule", 1)[1].split("\\bottomrule", 1)[0]
    expected = {tuple(map(int, p.split(","))) for p in re.findall(r"\((\d+,\d+,\d+,\d+)\)", table)}
    import importlib.util
    spec = importlib.util.spec_from_file_location("verify_s5", ROOT / "papers/s5_2adic/verify_s5.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    actual = {r[:4] for r in module.parse(str(html)) if r[5] and r[4] == "unknown" and module.excluded(*r[:4])[0]}
    require(len(expected) == 35 and expected == actual, "manuscript/table exclusion lists disagree")

    output = run([py, "papers/rank7/verify_rank7.py"])
    require("False" not in output and "all 10395 matchings: True" in output and
            "{2: 23}" in output and "k = 30 allowed" not in output,
            "unexpected rank-7 checks")
    output = run([py, "reproduction/rank7/verify_unit_propagation.py"])
    require("All 32 Boolean instances refuted by unit propagation: OK" in output,
            "rank-25 computation did not pass")

    compiler = shutil.which("cc") or shutil.which("gcc") or shutil.which("clang")
    require(compiler is not None, "install a C99 compiler for the hexagon checks")
    with tempfile.TemporaryDirectory(prefix="srg-verify-") as tmp:
        binary = str(Path(tmp) / "hexagons")
        run([compiler, "-O3", "-std=c99", str(anc / "hexagons.c"), "-o", binary])
        for name, count, excess in [("srg243_new.edges", 5000130, 19440),
                                    ("bvls243.edges", 4980690, 0)]:
            output = run([binary, str(anc / name), "243", "22"])
            require(f"H = {count}" in output and "bound = 4980690" in output and
                    f"H - bound = {excess}" in output, "unexpected hexagon count")
    if args.full:
        run([py, "reproduction/srg243_second/reproduce.py"])
    print("All requested verification checks passed.", flush=True)


if __name__ == "__main__":
    main()
