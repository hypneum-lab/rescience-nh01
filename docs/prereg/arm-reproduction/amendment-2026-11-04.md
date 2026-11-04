# Amendment 1 (2026-11-04) — tolerance of the aarch64 reproduction protocol

**Status:** tolerance decided by the PI on 2026-11-04 (1e-10); local branch `amend-noise-20261104`, not pushed, not tagged.
**Amends:** `protocol.md` section 6 and decision D1/D2 (frozen under tag
`arm-repro-gb300-freeze-20261031`, commit `e03031c`). The frozen files are not edited;
this amendment is a separate dated file.

## 1. Post hoc declaration

**The tolerance proposed in section 4 is fixed AFTER observing the GB300 result**
(attempt 2, 2026-11-01: largest bounded difference 3.759e-12 on the correlated run,
1.157e-12 on the confirmatory run, all discrete fields identical, verdict
INCONCLUSIVE_STRICT). It is therefore **post hoc**, not pre-registered. The strict
1e-12 criterion and the 1e-9 band of D1/D2 were registered before any run and are not
rewritten: the original verdict INCONCLUSIVE_STRICT stays on record. The PI decided
(2026-11-04) not to relax the threshold from the observed value alone, but first to
measure the run-to-run noise on the reference host; this document reports that
measurement and what it does and does not license.

## 2. Measurement (electron-server, 2026-11-04)

Two identical runs of `./run.sh confirmatory 2` from two fresh clones of
`hypneum-lab/rescience-nh01` at commit `f6e97fd` (descendant of the freeze tag; `code/`,
`data/`, `article/` identical to `submission-20261031`; `sha256sum -c` on
`CODE_SHA256_AT_TAG.txt` and `data/MANIFEST.sha256` passed). Python 3.12.15, numpy 2.5.4
(venv `~/scratch/nh01/venv`, the one of the 2026-10-30 provenance re-runs), single-threaded
BLAS, `nice 19`, 2 workers per run, run 1 pinned to CPUs 4-5 and run 2 to CPUs 6-7, both
concurrently, 2026-11-04 05:45Z to 08:32Z (9 999.8 s and 9 905.4 s). Comparison with
`check_arm_repro.py` (same schema as the protocol) after gzip of `cells.jsonl`.

| pair | verdict | largest bounded difference |
|---|---|---|
| ES run 1 vs ES run 2 (intra-host) | REPRODUCED | **0.0** (all 9 120 cells, summary leaves and figure.png byte-identical) |
| ES run 1 vs committed `data/` | REPRODUCED | 0.0 |
| ES run 2 vs committed `data/` | REPRODUCED | 0.0 |
| ES run 1 vs GB300 attempt 2 | INCONCLUSIVE_STRICT | 1.157e-12 (`c_fro`; `energy_own` 5.80e-13) |
| ES run 2 vs GB300 attempt 2 | INCONCLUSIVE_STRICT | 1.157e-12 (identical to the above) |
| GB300 attempt 2 vs committed `data/` | INCONCLUSIVE_STRICT | 1.157e-12 |

For the correlated run only the archived GB300-vs-committed figure exists (3.759e-12,
`energy_own`, m = 0.30, seed 109, alpha 0.45, arm shrink, t = 1; `c_fro` 1.460e-12). A
correlated run was **not** repeated on ES (about 6-8 h at 2 workers, beyond the 6 h cap
set for this measurement).

Substrate differences to keep in mind: ES 2 workers on 2 cores (committed data: 4 workers;
the worker count does not change numbers, confirmed here by the 0.0 difference to the
committed cells); GB300 4 workers on cores 56-59 (protocol D7). The ES CPU is a 2010 Xeon
X5680 (x86-64, no AVX) against Arm Neoverse V2; BLAS builds differ (the reference BLAS
is not recorded in `data/`).

## 3. What the measurement shows

1. The kernel is **bit-deterministic on the reference host**: intra-host noise is exactly
   0.0 on the confirmatory run (two runs, two core sets, concurrent load). A rule of the
   form « k x intra-host noise » therefore gives a degenerate tolerance of 0 and cannot
   be used as such.
2. The 1e-12 level is exceeded **only across hardware** (x86-64 vs aarch64), i.e. by
   reduction order / FMA / BLAS kernel differences. The cross-platform difference is
   the only available noise estimate: 1.157e-12 (confirmatory) and 3.759e-12
   (correlated), from one GB300 attempt each. This estimate is observational and post
   hoc by construction.
3. No discrete outcome, key, label or summary leaf differs on either run.

## 4. Tolerance (decided by the PI on 2026-11-04: 1e-10)

**Rule:** the cross-platform tolerance is the smallest power of 10 that is at least
10 x the largest inter-platform bounded difference observed (both runs, all bounded
fields): 10 x 3.759e-12 = 3.759e-11, rounded up to **1e-10**.

Justification: only one platform pair and one attempt per run were observed, so a
factor 10 covers unseen cells, a different Arm host or BLAS build, and the heavy tail of
the observed difference across fields (1.2e-12 to 3.8e-12 between runs); rounding to a
power of 10 removes any fit to the single observed value. 1e-10 stays one decade below
the registered band bound (1e-9) and many orders of magnitude below any discrete step of
the outcomes (probe fractions are multiples of 1/32). Alternative the PI may prefer: 1e-11
(next power of 10 above 2 x the maximum), which still accepts the observed values but
leaves only a 2.7 x margin.

The strict same-host criterion is unchanged: **1e-12 remains the criterion for a re-run on
the reference host**, where the measured noise is 0.

## 5. Effect on the verdict

- Under the amended cross-platform tolerance of 1e-10, both GB300 runs give
  REPRODUCED, every exact field being identical: study outcome « REPRODUCED under an
  amended, post hoc tolerance ».
- The original verdict under the frozen protocol remains **INCONCLUSIVE_STRICT** and is
  to be reported alongside, never replaced. Any text citing the amended verdict must say
  « post hoc tolerance (amendment of 2026-11-04) ».
- No result of the article, no `data/` file and no claim about the dreaming kernel
  changes.

## 6. Artefacts

On electron-server: `~/scratch/nh01-noise-20261104-run1` and `-run2` (results, run logs),
`~/scratch/nh01-noise-20261104-out/` (`measure.sh`, six `verdict-*.json`). GB300 side:
`~/archives/gb300-20261101/hypneum-20261101/rescience/attempt-2/record/`.
