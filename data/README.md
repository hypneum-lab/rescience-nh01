# data/ — committed artefacts of the three NH-01 runs

Copied unchanged from `results/nh01*/` of hypneum-lab/nerve-wml at commit
`d3eca42` (master, 2026-10-30). Each run directory keeps its upstream
`SHA256SUMS`; `MANIFEST.sha256` covers every file in this directory
(`shasum -a 256 -c MANIFEST.sha256`).

| Directory | Run | Tag (nerve-wml) | Cells | Wall |
|---|---|---|---|---|
| `nh01/` | pilot, N ∈ {64, 128, 256}, seeds 0–9 | `prereg-nh01-hopfield-dream-20261025` | 28 080 | 1 547 s |
| `nh01_confirmatory/` | N = 1 000, independent patterns, seeds 0–9 | `prereg-nh01-confirmatory-20261025` | 9 120 | 6 951 s |
| `nh01_correlated/` | N = 1 000, m ∈ {0, 0.15, 0.30}, seeds 100–109 | `prereg-nh01-correlated-20261027` | 29 640 | 22 866 s |

Files per run: `cells.jsonl.gz` (one JSON record per cell), `summary.json`
(per-condition estimates, bootstrap intervals, verdict), `figure.png`,
`run_meta.json` (host, versions, workers, wall time), `run.log`.
`provenance-rerun-20261030/` (two N = 1 000 runs) holds the re-run from a
clean clone at the tag: `comparison.json` (9 120/9 120 and 29 640/29 640
cells identical except `task_seconds`, figure byte-identical), `launch.txt`,
`uv_pip_freeze.txt`, `code_sha256_at_tag.txt`, `outputs_sha256.txt`.

Caveat: `nh01_correlated/summary.json` and `figure.png` carry the automatic
label `confirme` for the m = 0.30 level; the article reports that level as
inconclusive (Hebbian reference at the floor of the load grid, control not
computable at T = 0.2). The files are kept as produced by the tagged code.

Data DOI: 10.5281/zenodo.23833431 (nerve-wml v1.10.0, released and archived
2026-10-31, contains `results/nh01*` exactly as copied here; concept DOI
10.5281/zenodo.19656342). Cite it together with the tags above and
the Software Heritage snapshot `swh:1:snp:01242c8b5873518a503b84a80ce3a302bb69b8a8`.
Licence: CC BY 4.0 (`../LICENSE-CC-BY-4.0`).
