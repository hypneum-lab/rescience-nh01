# NH-01 code — verbatim extraction from nerve-wml

`experiments/nh01_hopfield_dream/` is copied byte-for-byte from
https://github.com/hypneum-lab/nerve-wml at tag `prereg-nh01-correlated-20261027`
(commit `df9a1e7`, SWHID `swh:1:rev:df9a1e7634113599c9b38cb4259068a29a5bdd2a`);
`CODE_SHA256_AT_TAG.txt` lists the SHA-256 of each file and matches
`data/nh01_correlated/provenance-rerun-20261030/code_sha256_at_tag.txt`. The
package path `experiments.nh01_hopfield_dream` is kept so that the three
`from experiments.nh01_hopfield_dream import …` lines are untouched; `run.sh`
sets `PYTHONPATH` to this directory.

| File | Role | Lines |
|---|---|---|
| `experiments/nh01_hopfield_dream/run.py` | kernel, matched-shrink control, capacity estimator, dynamics, bootstrap, pilot runner (N ≤ 256) | 713 |
| `experiments/nh01_hopfield_dream/confirmatory.py` | N = 1 000 confirmatory runner (seeds 0–9) and verdict | 384 |
| `experiments/nh01_hopfield_dream/correlated.py` | N = 1 000 correlated-pattern runner (seeds 100–109, m ∈ {0, 0.15, 0.30}) | 237 |
| `tests/test_nh01_*.py` | 20 unit tests (kernel identities, projector limit, shrink inertness at T = 0, estimator edge cases, verdict logic) | 296 |
| `scripts/compare_nh01.py` | cell-by-cell comparison of a new run with `data/` (NaN-aware, ignores `task_seconds`) | |
| `scripts/rerun_nh01.sh` | the provenance re-run wrapper used on 2026-10-30 (clean clone at tag, hash check; kept for the record, paths are site-specific) | |

Note on the confirmatory tag: `run.py` at `prereg-nh01-confirmatory-20261025`
(SHA-256 `31a23b9f…`) differs from the file here (`35f69477…`) only by the
`correlated_patterns()` helper and the `ancestor_m` branch added for the
correlated run (`git diff prereg-nh01-confirmatory-20261025 prereg-nh01-correlated-20261027 -- experiments/nh01_hopfield_dream/run.py`,
+19/−1 lines); with `ancestor_m` unset the code path is identical, and the
confirmatory provenance re-run of 2026-10-30 was executed at its own tag.

## Environment

Python 3.12 (runs: 3.12.15), `requirements.txt` pinned to the versions that
produced `data/` (`numpy==2.5.4`, `matplotlib==3.11.2`, `pytest==9.1.1`). No
GPU, no torch. Single-threaded BLAS (`*_NUM_THREADS=1`) is required for the
timings below and was used for all runs.

```bash
python3.12 -m venv venv && . venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. python -m pytest tests/          # seconds
./run.sh confirmatory 4                       # ~2 h on the reference host
./run.sh correlated 2                         # ~6.5 h on the reference host
python -I scripts/compare_nh01.py ../data/nh01_confirmatory results/nh01_confirmatory cmp.json
```

`--analyze-only` (any module) recomputes `summary.json` and `figure.png` from
an existing `cells.jsonl`; `--probe` (confirmatory/correlated) runs a 2–3 min
timing probe on seed 999/998 and discards it; `--smoke` (pilot) runs a tiny
grid for implementation checks.

## Expected duration and host

| Run | Cells | Workers | Wall | Host |
|---|---|---|---|---|
| pilot (`run`) | 28 080 | 4 | 1 547 s (26 min) | electron-server |
| confirmatory | 9 120 | 4 | 6 951 s (1.9 h) | electron-server |
| confirmatory, provenance re-run | 9 120 | 2 | 15 136 s (4.2 h) | electron-server |
| correlated | 29 640 | 2 | 22 866 s (6.4 h) | electron-server |
| correlated, provenance re-run | 29 640 | 2 | 30 547 s (8.5 h) | electron-server |

electron-server: 8 × Intel Xeon X5680 (2010, no AVX), Linux 6.8.0-136,
`nice 19`, shared with other jobs (load 6–7 at launch). The wall times are
upper bounds for a dedicated modern machine. Results must match `data/` on
every cell except `task_seconds`; `figure.png` must be byte-identical.
