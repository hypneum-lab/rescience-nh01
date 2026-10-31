# Review log — aarch64 reproduction protocol

**Pass 1:** Codex CLI 0.162.1, model `gpt-6.1-sol`, reasoning effort `high`, 2026-10-31
(about 21:45–22:30 CET), blind on the repository (branch head `da8518c`); brief and
report in this folder (`codex-brief-pass1.md`, `codex-report-pass1.md`, in French). The
reviewer ran small counterexamples on `data/` and changed no repository file. Each
finding was checked against the source before a change. Counts: 4 BLOQUANT confirmed,
12 MAJEUR confirmed, 0 rejected; one MAJEUR (P8, cross-ISA identity not guaranteed) is
a disclosed limitation, not a fix.

| id | finding | verdict | change |
|---|---|---|---|
| V1 | float branch accepts bool/int as numbers in `summary.json` and cells | confirmed by rerun of the counterexamples | strict type checks; bool never a number |
| V2 | key equality mixes 1000 / 1000.0 / True | confirmed | typed key schema |
| V3 | « no result » not implemented | confirmed | NO_RESULT (exit 3): unreadable files, strict-subset cells, runner exit code or wall cap (wrapper) |
| V4 | `run_meta` compared before removal | confirmed | removed at the root before the comparison |
| V5 | no schema, reference not verified, repeated JSON members | confirmed | required fields per run, `MANIFEST.sha256` check, duplicate members rejected |
| V6 | inf accepted, NaN allowed anywhere | confirmed | NaN only for `c_spec`, inf invalid |
| V7 | thresholds not validated | confirmed | finite, 0 ≤ strict ≤ band, exit 4 |
| TBD-3 / cue_overlap | computed float of a constant, exactness trivial-reject | confirmed (0.8 and 0.8000000000000002 in the cells) | bounded field |
| summary grid leaves | `t_star` etc. tolerated as floats | confirmed | exact list |
| P1 | lock absent, interpreter not selected | confirmed (expected at L0) | wrapper asserts 3.12.15 aarch64; lock and archive hash listed as pre-freeze work |
| P2 | threads only set inside `run.sh` | confirmed | wrapper exports them before every step |
| P3 | `gzip -k` can validate a stale archive | confirmed | fresh clone per run and attempt; pre-existing `.gz` gives NO_RESULT |
| P4 | no stop on technical failure; codes not captured | confirmed | wrapper with `set -euo pipefail`, checker codes captured |
| P5 | runner wall caps vs time budget | confirmed (`WALL_CAP_SECONDS`) | worker rule against the caps, both probes |
| P6 | series vs concurrent recipes differ | confirmed | concurrent only, one clone and core list per run |
| P7 | 64 KiB pages | confirmed as a risk | native smoke test before the runs |
| P8 | one seed and one thread do not guarantee cross-ISA identity | confirmed | disclosed in section 6; RNG witness recorded |
| P9 | figure failure vs « crash = no result » | confirmed | TBD-6 |
| P10 | manifests not executed | confirmed | both manifests checked by the wrapper |
| I1 | « bit level » wording | confirmed | « strict tolerance »; REPRODUCED is not bit identity |
| I2 | « claims stand » must keep the m = 0.30 reservation | confirmed | section 6 |
