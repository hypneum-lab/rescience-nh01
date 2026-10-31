"""Decision rule of the aarch64 reproduction protocol (docs/prereg/arm-reproduction).

Compares one re-run directory with the committed one (``data/<run>/``) and
classifies the run as REPRODUCED, INCONCLUSIVE_STRICT, NOT_REPRODUCED or
NO_RESULT (protocol, section 6). Standard library only.

Usage:
    python -I check_arm_repro.py <run> <committed_dir> <rerun_dir> <out_json>
        [--manifest data/MANIFEST.sha256] [--strict 1e-12] [--band 1e-9]

<run> is ``nh01_confirmatory`` or ``nh01_correlated``. Exit status:
0 REPRODUCED, 1 INCONCLUSIVE_STRICT, 2 NOT_REPRODUCED, 3 NO_RESULT,
4 invalid reference or arguments, 5 checker error (report written when possible). The JSON report is written in every case
where the arguments could be parsed.

``compare_nh01.py`` stays the descriptive comparator. This script adds the
schema, the tolerance rule and the outcome classes; ``compare_nh01.py``
records no tolerance, and its ``max_abs_diff`` drops a NaN-vs-number
difference because ``max(x, nan)`` returns ``x``.
"""
import argparse
import gzip
import hashlib
import json
import math
import sys
from pathlib import Path

RUNS = {"nh01_confirmatory": False, "nh01_correlated": True}  # has ancestor_m
KEY_TYPES = {"N": int, "seed": int, "alpha": float, "P": int, "arm": str,
             "t": float, "temp": float, "flips": float, "ancestor_m": float}
# Discrete outcomes and design constants of a cell: exact value and type.
DISCRETE = {"n_probes": int, "sweeps": int, "retrieved_frac": float,
            "other_stored_frac": float, "spurious_frac": float,
            "nonconverged_frac": float}
# Floating-point diagnostics: same NaN pattern, |difference| bounded.
# cue_overlap is a design constant (0.8) computed by a float reduction; the
# committed cells already hold 0.8 and 0.8000000000000002 (TBD-3).
FLOAT_DIAG = {"c_fro", "c_spec", "mean_overlap", "energy_own", "energy_hebb",
              "cue_overlap"}
NAN_ALLOWED = {"c_spec"}  # NaN by design for dream / shrink rows
TIMING = {"task_seconds"}
# summary.json leaves that are grid or design choices: exact, never bounded.
SUMMARY_EXACT = {"temp", "flips", "t_primary", "t_star", "per_seed_t_star",
                 "tolerance", "temperature"}


class InvalidInput(Exception):
    pass


def no_dup_hook(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise InvalidInput(f"repeated JSON member {k!r}")
        d[k] = v
    return d


def jload(text):
    return json.loads(text, object_pairs_hook=no_dup_hook)


def typed(x, t):
    if t is float:
        return isinstance(x, float)
    return type(x) is t  # bool is not int


def load_cells(path, has_m):
    cells, dup = {}, 0
    want = [k for k in KEY_TYPES if k != "ancestor_m" or has_m]
    with gzip.open(path, "rt") as f:
        for n, line in enumerate(f, 1):
            c = jload(line)
            if not isinstance(c, dict):
                raise InvalidInput(f"{path}:{n}: not an object")
            if ("ancestor_m" in c) != has_m:
                raise InvalidInput(f"{path}:{n}: ancestor_m presence")
            for k in want:
                if k not in c or not typed(c[k], KEY_TYPES[k]):
                    raise InvalidInput(f"{path}:{n}: key field {k} missing or mistyped")
            for k, t in DISCRETE.items():
                if k not in c or not typed(c[k], t):
                    raise InvalidInput(f"{path}:{n}: field {k} missing or mistyped")
            for k in FLOAT_DIAG:
                v = c.get(k)
                if not isinstance(v, float) or math.isinf(v) or (
                        math.isnan(v) and k not in NAN_ALLOWED):
                    raise InvalidInput(f"{path}:{n}: field {k} missing or invalid")
            key = tuple((k, c[k]) for k in want)
            dup += key in cells
            cells[key] = c
    return cells, dup


def same_exact(x, y):
    return type(x) is type(y) and json.dumps(x, sort_keys=True) == json.dumps(y, sort_keys=True)


def compare_summary(a, b, path, rep, name=""):
    if isinstance(a, dict) and isinstance(b, dict):
        if set(a) != set(b):
            rep["summary_exact_mismatch"].append(f"{path}: keys differ")
        for k in sorted(set(a) & set(b)):
            compare_summary(a[k], b[k], f"{path}/{k}", rep, k)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            rep["summary_exact_mismatch"].append(f"{path}: lengths differ")
        for i, (x, y) in enumerate(zip(a, b)):
            compare_summary(x, y, f"{path}[{i}]", rep, name)
    elif isinstance(a, float) and isinstance(b, float) and name not in SUMMARY_EXACT:
        if math.isinf(a) or math.isinf(b):
            if a != b:
                rep["summary_exact_mismatch"].append(f"{path}: {a!r} vs {b!r}")
        elif math.isnan(a) or math.isnan(b):
            if not (math.isnan(a) and math.isnan(b)):
                rep["summary_exact_mismatch"].append(f"{path}: {a!r} vs {b!r}")
        else:
            d = abs(a - b)
            if d > rep["summary_max_abs_diff"]:
                rep["summary_max_abs_diff"], rep["summary_max_abs_diff_at"] = d, path
    elif not same_exact(a, b):
        rep["summary_exact_mismatch"].append(f"{path}: {a!r} vs {b!r}")


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def check_reference(run, ref, manifest):
    if manifest is None:
        return
    want = {}
    for line in Path(manifest).read_text().splitlines():
        h, _, name = line.partition("  ")
        want[name] = h
    for f in ("cells.jsonl.gz", "summary.json"):
        if want.get(f"{run}/{f}") != sha256(ref / f):
            raise InvalidInput(f"reference {run}/{f} does not match {manifest}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run", choices=sorted(RUNS))
    ap.add_argument("committed", type=Path)
    ap.add_argument("rerun", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--strict", type=float, default=1e-12)
    ap.add_argument("--band", type=float, default=1e-9)
    a = ap.parse_args()
    rep = {"run": a.run, "strict": a.strict, "band": a.band, "verdict": None,
           "reason": None}

    def finish(verdict, code, reason=None):
        rep["verdict"], rep["reason"] = verdict, reason
        a.out.write_text(json.dumps(rep, indent=2, sort_keys=True) + "\n")
        print(json.dumps({k: rep[k] for k in ("run", "verdict", "reason")}))
        return code

    if not (math.isfinite(a.strict) and math.isfinite(a.band) and 0 <= a.strict <= a.band):
        return finish("INVALID", 4, "thresholds must be finite with 0 <= strict <= band")
    has_m = RUNS[a.run]
    try:
        check_reference(a.run, a.committed, a.manifest)
        ca, da = load_cells(a.committed / "cells.jsonl.gz", has_m)
        sa = jload((a.committed / "summary.json").read_text())
        if da or not ca or not isinstance(sa, dict):
            raise InvalidInput("reference empty, duplicated or malformed")
    except (OSError, ValueError, EOFError, InvalidInput) as exc:
        return finish("INVALID", 4, f"reference: {exc}")
    try:
        cb, db = load_cells(a.rerun / "cells.jsonl.gz", has_m)
        sb = jload((a.rerun / "summary.json").read_text())
        if not isinstance(sb, dict):
            raise InvalidInput("summary is not an object")
    except InvalidInput as exc:  # readable, but a field differs in type or validity
        return finish("NOT_REPRODUCED", 2, f"rerun schema: {exc}")
    except (OSError, ValueError, EOFError) as exc:  # missing, truncated or unparseable
        return finish("NO_RESULT", 3, f"rerun unreadable: {exc}")
    ka, kb = set(ca), set(cb)
    rep.update({"n_cells": [len(ca), len(cb)], "duplicate_keys": db,
                "missing_keys": len(ka - kb), "extra_keys": len(kb - ka),
                "missing_examples": [dict(k) for k in sorted(ka - kb, key=repr)[:5]],
                "extra_examples": [dict(k) for k in sorted(kb - ka, key=repr)[:5]]})
    rep.update({"discrete_mismatch": {}, "nan_pattern_mismatch": {},
                "unexpected_fields": [], "float_max_abs_diff": {},
                "float_max_abs_diff_at": {}, "summary_exact_mismatch": [],
                "summary_max_abs_diff": 0.0, "summary_max_abs_diff_at": None})
    known = set(KEY_TYPES) | set(DISCRETE) | FLOAT_DIAG | TIMING
    unexpected = set()
    for k in sorted(ka & kb, key=repr):
        x, y = ca[k], cb[k]
        unexpected |= (set(x) | set(y)) - known
        for f in DISCRETE:
            if not same_exact(x[f], y[f]):
                rep["discrete_mismatch"][f] = rep["discrete_mismatch"].get(f, 0) + 1
        for f in FLOAT_DIAG:
            u, v = x[f], y[f]
            if math.isnan(u) or math.isnan(v):
                if not (math.isnan(u) and math.isnan(v)):
                    rep["nan_pattern_mismatch"][f] = rep["nan_pattern_mismatch"].get(f, 0) + 1
                continue
            d = abs(u - v)
            if d > rep["float_max_abs_diff"].get(f, 0.0):
                rep["float_max_abs_diff"][f] = d
                rep["float_max_abs_diff_at"][f] = dict(k)
    rep["unexpected_fields"] = sorted(unexpected)
    sa.pop("run_meta", None)
    sb.pop("run_meta", None)
    compare_summary(sa, sb, "", rep)
    exact_ok = (ka == kb and not db and not unexpected and not rep["discrete_mismatch"]
                and not rep["nan_pattern_mismatch"] and not rep["summary_exact_mismatch"])
    worst = max([0.0, rep["summary_max_abs_diff"], *rep["float_max_abs_diff"].values()])
    rep["worst_float_abs_diff"] = worst
    if exact_ok and worst <= a.strict:
        return finish("REPRODUCED", 0)
    if exact_ok and worst <= a.band:
        return finish("INCONCLUSIVE_STRICT", 1, "floating-point difference in (strict, band]")
    return finish("NOT_REPRODUCED", 2, "exact field, key or label difference, or float difference > band")


def guarded():
    try:
        return main()
    except SystemExit:
        raise
    except BaseException as exc:  # never let a crash look like exit 1
        print(json.dumps({"verdict": "CHECKER_ERROR", "reason": repr(exc)}))
        return 5


if __name__ == "__main__":
    sys.exit(guarded())
