"""Decision rule of the aarch64 reproduction protocol (docs/prereg/arm-reproduction).

Compares one re-run directory with the committed one (``data/<run>/``) and
classifies the result as REPRODUCED, INCONCLUSIVE_FLOAT or NOT_REPRODUCED.
Standard library only.

Usage:
    python -I check_arm_repro.py <committed_dir> <rerun_dir> <out_json>
        [--strict 1e-12] [--band 1e-9]

Exit status: 0 REPRODUCED, 1 INCONCLUSIVE_FLOAT, 2 NOT_REPRODUCED,
3 input error. ``compare_nh01.py`` stays the descriptive comparator; this
script adds the tolerance rule (``compare_nh01.py`` records no tolerance, and
its ``max_abs_diff`` drops a NaN-vs-number difference because
``max(x, nan)`` returns ``x``).
"""
import argparse
import gzip
import json
import math
import sys
from pathlib import Path

KEY_FIELDS = ("N", "seed", "alpha", "P", "arm", "t", "temp", "flips", "ancestor_m")
TIMING = {"task_seconds"}
# Discrete outcomes and design constants of a cell: must match exactly.
DISCRETE = {"n_probes", "cue_overlap", "retrieved_frac", "other_stored_frac",
            "spurious_frac", "nonconverged_frac", "sweeps"}
# Floating-point diagnostics: same NaN pattern, absolute difference bounded.
FLOAT_DIAG = {"c_fro", "c_spec", "mean_overlap", "energy_own", "energy_hebb"}


def load_cells(path):
    cells, dup = {}, 0
    with gzip.open(path, "rt") as f:
        for line in f:
            c = json.loads(line)
            key = tuple((k, c[k]) for k in KEY_FIELDS if k in c)
            dup += key in cells
            cells[key] = c
    return cells, dup


def is_nan(x):
    return isinstance(x, float) and math.isnan(x)


def float_diff(x, y):
    """Return (ok_pattern, abs_diff) for two JSON numbers (NaN-aware)."""
    if is_nan(x) or is_nan(y):
        return (is_nan(x) and is_nan(y)), 0.0
    if isinstance(x, bool) or isinstance(y, bool):
        return x == y, 0.0
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        return x == y, 0.0
    if math.isinf(x) or math.isinf(y):
        return x == y, 0.0
    return True, abs(float(x) - float(y))


def compare_summary(a, b, path, rep):
    """Recursive: strings, bools, None, ints and structure exact; floats bounded."""
    if isinstance(a, dict) and isinstance(b, dict):
        if set(a) != set(b):
            rep["summary_exact_mismatch"].append(f"{path}: keys differ")
        for k in set(a) & set(b):
            if path == "" and k == "run_meta":
                continue
            compare_summary(a[k], b[k], f"{path}/{k}", rep)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            rep["summary_exact_mismatch"].append(f"{path}: lengths differ")
        for i, (x, y) in enumerate(zip(a, b)):
            compare_summary(x, y, f"{path}[{i}]", rep)
    elif isinstance(a, float) or isinstance(b, float):
        ok, d = float_diff(a, b)
        if not ok:
            rep["summary_exact_mismatch"].append(f"{path}: {a!r} vs {b!r}")
        elif d > rep["summary_max_abs_diff"]:
            rep["summary_max_abs_diff"] = d
            rep["summary_max_abs_diff_at"] = path
    elif a != b or type(a) is not type(b):
        rep["summary_exact_mismatch"].append(f"{path}: {a!r} vs {b!r}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("committed", type=Path)
    ap.add_argument("rerun", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--strict", type=float, default=1e-12)
    ap.add_argument("--band", type=float, default=1e-9)
    a = ap.parse_args()
    try:
        ca, da = load_cells(a.committed / "cells.jsonl.gz")
        cb, db = load_cells(a.rerun / "cells.jsonl.gz")
        sa = json.loads((a.committed / "summary.json").read_text())
        sb = json.loads((a.rerun / "summary.json").read_text())
    except (OSError, ValueError) as exc:
        print(f"input error: {exc}", file=sys.stderr)
        return 3
    rep = {"n_cells": [len(ca), len(cb)], "duplicate_keys": [da, db],
           "keys_equal": set(ca) == set(cb), "strict": a.strict, "band": a.band,
           "discrete_mismatch": {}, "nan_pattern_mismatch": {},
           "unclassified_fields": [], "float_max_abs_diff": {},
           "summary_exact_mismatch": [], "summary_max_abs_diff": 0.0,
           "summary_max_abs_diff_at": None}
    unclassified = set()
    for k in set(ca) & set(cb):
        x, y = ca[k], cb[k]
        for f in (set(x) | set(y)) - TIMING - set(KEY_FIELDS):
            if f not in x or f not in y:
                rep["discrete_mismatch"][f] = rep["discrete_mismatch"].get(f, 0) + 1
            elif f in FLOAT_DIAG:
                ok, d = float_diff(x[f], y[f])
                if not ok:
                    rep["nan_pattern_mismatch"][f] = rep["nan_pattern_mismatch"].get(f, 0) + 1
                elif d > rep["float_max_abs_diff"].get(f, 0.0):
                    rep["float_max_abs_diff"][f] = d
            else:
                if f not in DISCRETE:
                    unclassified.add(f)
                if json.dumps(x[f]) != json.dumps(y[f]):
                    rep["discrete_mismatch"][f] = rep["discrete_mismatch"].get(f, 0) + 1
    rep["unclassified_fields"] = sorted(unclassified)  # compared exactly
    compare_summary(sa, sb, "", rep)
    exact_ok = (rep["keys_equal"] and len(ca) == len(cb) and da == db == 0
                and not rep["discrete_mismatch"] and not rep["nan_pattern_mismatch"]
                and not rep["summary_exact_mismatch"])
    worst = max([0.0, rep["summary_max_abs_diff"], *rep["float_max_abs_diff"].values()])
    rep["worst_float_abs_diff"] = worst
    if exact_ok and worst <= a.strict:
        verdict, code = "REPRODUCED", 0
    elif exact_ok and worst <= a.band:
        verdict, code = "INCONCLUSIVE_FLOAT", 1
    else:
        verdict, code = "NOT_REPRODUCED", 2
    rep["verdict"] = verdict
    a.out.write_text(json.dumps(rep, indent=2, sort_keys=True) + "\n")
    print(json.dumps(rep, indent=2, sort_keys=True))
    return code


if __name__ == "__main__":
    sys.exit(main())
