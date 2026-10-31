#!/usr/bin/env bash
# Reproduce the two pre-registered N = 1 000 runs of NH-01 (and, optionally,
# the pilot) with the exact seeds and grids of the nerve-wml tags
#   prereg-nh01-confirmatory-20261025  (commit a000f73)  -> confirmatory.py
#   prereg-nh01-correlated-20261027    (commit df9a1e7)  -> correlated.py
#   prereg-nh01-hopfield-dream-20261025 (commit bc2f838) freezes the pilot
#   PROTOCOL only (no runner in that tag); the pilot runner shipped here is
#   the one of df9a1e7, and the pilot is not covered by the provenance re-runs
#
# Seeds, load grid, dreaming-time grid, temperatures, cue noise and probe
# counts are constants inside the modules (not CLI options), so nothing here
# can change the design:
#   confirmatory: N = 1000, seeds 0-9, alpha in {0.04..0.20 step 0.02, 0.25..0.95 step 0.05},
#                 t in {0,1,3,5,7,10,15,20,30,100}, (T, flips) in {(0, 0.1), (0.2, 0.1)}, 32 probes
#   correlated:   N = 1000, seeds 100-109, m in {0, 0.15, 0.30}, alpha grid above + {0.01, 0.02}
#   pilot:        N in {64, 128, 256}, seeds 0-9, t in {0,0.3,1,3,10,30,100}, 3 conditions
# Root seed 20261025; every stream is numpy.random.default_rng([20261025, seed, N, id]).
# The worker count only changes scheduling, never the numbers.
#
# Usage:  ./run.sh [confirmatory|correlated|pilot|all] [workers]   (default: all, nproc)
# Output: results/<run>/ next to this script (cells.jsonl, summary.json,
#         figure.png, run_meta.json). Compare with ../data/<run>/ afterwards
#         (the comparator reads cells.jsonl.gz, so gzip first; then read
#         keys_equal, cells_differing_non_timing, fields_differing, max_abs_diff
#         and summary_equal_excl_run_meta in cmp.json — no failure exit status):
#         gzip -k results/nh01_confirmatory/cells.jsonl
#         python -I scripts/compare_nh01.py ../data/nh01_confirmatory results/nh01_confirmatory cmp.json
#
# Expected wall time (reference host electron-server, 8 x Xeon X5680 of 2010,
# no AVX, nice 19, shared): confirmatory 6 951 s with 4 workers (15 136 s with
# 2), correlated 22 866 s with 2 workers (30 547 s on the re-run), pilot
# 1 547 s with 4 workers. A modern CPU with AVX should be several times faster.
set -euo pipefail
cd "$(dirname "$0")"

WHAT=${1:-all}
WORKERS=${2:-$(nproc 2>/dev/null || sysctl -n hw.ncpu)}
PY=${PYTHON:-python}

# Single-threaded BLAS: the runs were produced this way and the pilot was
# once aborted because of thread oversubscription (results/nh01/run-aborted-blas-threads.log upstream).
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=$PWD${PYTHONPATH:+:$PYTHONPATH}

echo "python: $($PY -V 2>&1); numpy: $($PY -c 'import numpy; print(numpy.__version__)')"
echo "expected: Python 3.12.15, numpy 2.5.4, matplotlib 3.11.2 (requirements.txt)"

run_one() {  # <module> <out_dir>
  echo "== $1 -> $2  (workers=$WORKERS, started $(date -u +%FT%TZ))"
  nice -n 19 "$PY" -m "experiments.nh01_hopfield_dream.$1" --workers "$WORKERS" --out "$2"
  echo "== $1 done $(date -u +%FT%TZ)"
}

case "$WHAT" in
  confirmatory) run_one confirmatory results/nh01_confirmatory ;;
  correlated)   run_one correlated   results/nh01_correlated ;;
  pilot)        run_one run          results/nh01 ;;
  all)          run_one confirmatory results/nh01_confirmatory
                run_one correlated   results/nh01_correlated ;;
  *) echo "usage: $0 [confirmatory|correlated|pilot|all] [workers]" >&2; exit 2 ;;
esac
