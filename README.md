# [Re] Dreaming neural networks — NH-01 replication (ReScience C submission)

Independent NumPy replication of the dreaming (Hebbian-unlearning) kernel of
Fachechi, Agliari & Barra, *Neural Networks* 112 (2019) 24–40,
DOI [10.1016/j.neunet.2019.01.006](https://doi.org/10.1016/j.neunet.2019.01.006)
(arXiv:1810.12217), with a pre-registered design, a matched uniform-shrink
control, correlated patterns, and an internal provenance re-run of both
$N = 1\,000$ studies.

Author: Clément Saillant (Hypneum Lab, ORCID
[0000-0002-8414-185X](https://orcid.org/0000-0002-8414-185X)).
Status: **submission package frozen on 2026-10-31** (tag `submission-20261031`); the ReScience C submission issue will be linked here once opened.

Headline: dreaming at $t = 10$ multiplies the empirical capacity by
3.86 [3.79, 3.93] at $N = 1\,000$ (confirmed), 9.06 [8.84, 9.29] on correlated
patterns with ancestor overlap $m = 0.15$ (confirmed), and the $m = 0.30$
level carries its registered C1 label (ratio 44.38 [42.56, 46.97], Hebbian
crossings inside the first load interval 0.01–0.02, grid-sensitive
magnitude) next to a **post-analysis assessment of inconclusive** (at
$T = 0.2$ five Hebbian and two shrink estimates are below the grid and
coded as zero, so the control statistic is not censoring-adjusted). The matched uniform-shrink
control is exactly inert at $T = 0$ and lowers capacity by 2.5 per cent at
$T = 0.2$. Both $N = 1\,000$ runs were reproduced on the original host from a clean
clone at the tagged commit with identical non-timing cell values (9 120/9 120
and 29 640/29 640 cells).

## Layout

```
rescience-nh01/
├── README.md                  this file
├── LICENSE                    MIT — code/ (as upstream nerve-wml)
├── LICENSE-CC-BY-4.0          CC BY 4.0 — article/ text and figures, data/
├── article/
│   ├── metadata.yaml          ReScience metadata (template fields)
│   ├── article.md             Markdown source of the article (edit this)
│   ├── content.tex            generated: pandoc -f markdown --biblatex article.md, \autocite → \supercite
│   ├── bibliography.bib       8 entries
│   ├── figures/               figure-pilot.png (= data/nh01/figure.png); figure-{confirmatory,correlated}.png
│   │                          rendered by code/scripts/publication_figures.py from data/*/cells.jsonl.gz
│   ├── article.tex            template + longtable/booktabs/amssymb and the pandoc helpers (3 lines)
│   └── header.tex, rescience.cls, article.py, yaml-to-latex.py, Makefile, COPYING, fonts/
│                              from github.com/ReScience/template (0978d0e); Makefile adds the article.md → content.tex rule
├── code/
│   ├── experiments/nh01_hopfield_dream/   run.py, confirmatory.py, correlated.py (verbatim, tag prereg-nh01-correlated-20261027)
│   ├── tests/                 3 files, 20 test functions (23 cases)
│   ├── scripts/               compare_nh01.py (cell-by-cell check), rerun_nh01.sh (provenance wrapper),
│   │                          publication_figures.py (article figures, pinned numpy/matplotlib)
│   ├── requirements.txt       numpy==2.5.4 matplotlib==3.11.2 pytest==9.1.1
│   ├── run.sh                 reproduces the confirmatory and correlated grids (exact seeds/parameters)
│   ├── CODE_SHA256_AT_TAG.txt
│   └── README.md              durations and reference host
├── data/                      summary.json, figure.png, run_meta.json, cells.jsonl.gz, run.log of the
│   │                          three runs + provenance-rerun-20261030/ ; MANIFEST.sha256 ; README.md
│   ├── nh01/                  pilot, N ∈ {64, 128, 256}, 28 080 cells
│   ├── nh01_confirmatory/     N = 1 000, independent patterns, 9 120 cells
│   └── nh01_correlated/       N = 1 000, m ∈ {0, 0.15, 0.30}, 29 640 cells
├── prereg/                    the three frozen pre-registration files (verbatim) + README.md
└── review/                    two independent automated review passes (2026-10-31): briefs, reports,
                               verdict table, article as it stood before the review + README.md
```

## Upstream provenance

| Run | nerve-wml tag | commit | SWHID (revision) |
|---|---|---|---|
| pilot (N ≤ 256) | `prereg-nh01-hopfield-dream-20261025` | `bc2f838` | `swh:1:rev:bc2f838919756a8dc2249e577cc5fac0f21cf0d2` |
| confirmatory (N = 1 000) | `prereg-nh01-confirmatory-20261025` | `a000f73` | `swh:1:rev:a000f73addde8ff8ac0f28e72a038ad886848f48` |
| correlated (N = 1 000) | `prereg-nh01-correlated-20261027` | `df9a1e7` | `swh:1:rev:df9a1e7634113599c9b38cb4259068a29a5bdd2a` |

Software Heritage snapshot of https://github.com/hypneum-lab/nerve-wml:
`swh:1:snp:01242c8b5873518a503b84a80ce3a302bb69b8a8` (visit 2026-10-29T10:55:51Z).
Zenodo (nerve-wml): concept DOI [10.5281/zenodo.19656342](https://doi.org/10.5281/zenodo.19656342);
version v1.10.0 = [10.5281/zenodo.23833431](https://doi.org/10.5281/zenodo.23833431)
(2026-10-31) archives the NH-01 code and `results/nh01*`. **Data DOI:
10.5281/zenodo.23833431.** The exact runs are pinned by tag + SWHID.
Merged PRs: hypneum-lab/nerve-wml#81 (pilot), #86 (confirmatory + provenance
re-run), #87 (correlated + provenance re-run). Issue #68.

## Reproduce

Requirements: Python 3.12, `code/requirements.txt`. No GPU, no torch.

```bash
cd code
python3.12 -m venv venv && . venv/bin/activate && pip install -r requirements.txt
PYTHONPATH=. python -m pytest tests/        # 20 test functions, 23 cases, seconds
./run.sh confirmatory 4                     # N = 1 000, seeds 0-9: 6 951 s on the reference host
./run.sh correlated 2                       # N = 1 000, seeds 100-109: 22 866 s on the reference host
./run.sh pilot 4                            # optional, N <= 256: 1 547 s
gzip -k results/nh01_confirmatory/cells.jsonl   # the comparator reads cells.jsonl.gz
python -I scripts/compare_nh01.py ../data/nh01_confirmatory results/nh01_confirmatory cmp.json
```

Reference host: electron-server, 8 × Xeon X5680 (2010, no AVX), Linux 6.8,
`nice 19`, single-threaded BLAS, shared with other jobs — wall times are
upper bounds. Reduced mode for reviewers: `./run.sh confirmatory $(nproc)`
(~2 h on 4 old cores) is enough to check the confirmed claims; the
correlated run adds ~6 h. `--analyze-only` recomputes `summary.json` and
`figure.png` from an existing `cells.jsonl`.

Determinism: every random stream is `numpy.random.default_rng([20261025, seed, N, <stream id>])`;
the bootstrap uses seed 20261025 with 10 000 resamples. The worker count
only changes scheduling. Expected outputs: the committed `summary.json`;
cell keys and discrete outcomes must match exactly and floating-point
diagnostics to about 1e-12; `figure.png` byte identity is not required on
another platform (it held on the original host).

## Build the article

```bash
cd article && make          # xelatex + biber; needs Python 3 + PyYAML (yaml-to-latex.py)
```

`content.tex` is generated from `article.md` by `article/md2tex.sh` (pandoc
3.12, `--biblatex`, `\autocite` → `\supercite`, drops the References section);
rerun it after editing `article.md`. Build checked 2026-10-31 with
TeX Live 2026 (XeLaTeX + Biber): 10 pages, 8 references, no LaTeX error.

## Independent review before submission

Before any human review, the package went through two automated review
passes on 2026-10-31 (Codex CLI, `gpt-6.1-sol` blind on the repositories,
then `gpt-6-astra` cross-checking the corrected package and the verdict
table). Every finding was verified against the cells, the summaries, the
runner code and the original paper before a line was changed; the PI
decided the open points. Pass 1 found one blocking statement in the
conclusion (fixed) and confirmed every number by independent recount;
pass 2 found one more numerical error (fixed) and argued for publishing
the registered m = 0.30 ratio next to its reservation. Briefs, reports,
verdicts and the pre-review article are in `review/`. The commits are
`1f7c6b6` (pass 1) and `d78590c` (pass 2).

## Expected headline numbers (from `data/*/summary.json`)

| Run | Cell | Hebb α̂_c | dream t = 10 | ratio [95 % CI] | shrink ratio |
|---|---|---|---|---|---|
| pilot | N = 256, T = 0 | 0.175 [0.167, 0.183] | 0.599 [0.591, 0.606] | 3.43 [3.26, 3.60] | 1.000 (exact) |
| confirmatory | N = 1 000, T = 0 | 0.157 [0.155, 0.160] | 0.607 [0.604, 0.610] | 3.86 [3.79, 3.93] | 1.000 (exact) |
| confirmatory | N = 1 000, T = 0.2 | 0.126 [0.125, 0.128] | 0.453 [0.450, 0.455] | 3.58 [3.53, 3.64] | 0.975 [0.967, 0.982] |
| correlated m = 0 | N = 1 000, T = 0 | 0.160 [0.158, 0.162] | 0.611 [0.606, 0.616] | 3.82 [3.77, 3.88] | 1.000 (exact) |
| correlated m = 0.15 | N = 1 000, T = 0 | 0.068 [0.066, 0.070] | 0.616 [0.612, 0.619] | 9.06 [8.84, 9.29] | 1.000 (exact) |
| correlated m = 0.30 | N = 1 000, T = 0 | 0.014 [0.014, 0.015] (grid floor) | 0.636 [0.633, 0.639] | 44.38 [42.56, 46.97] registered C1 confirmed (grid-sensitive: Hebbian crossing inside 0.01–0.02); post-analysis level assessment inconclusive | 1.000 (exact) |
| correlated m = 0.30 | N = 1 000, T = 0.2 | 0.007 [0.003, 0.011], 5/10 seeds below grid | 0.463 [0.458, 0.468] | — | undefined on 5 seeds; zero-coded 0.6 [0.2, 1.0] on the rest |

Note: `data/nh01_correlated/{summary.json,figure.png}` carry the automatic
label `confirme` for m = 0.30 as produced by the tagged code; the article
overrides that label (see `data/README.md`).

## AI assistance (transparency)

This repository is developed by a one-person lab with AI assistants
used as tools, never as authors:

- **Claude Code (Anthropic)** assists with code, documentation,
  drafts of the article text, operations and literature search in interactive sessions driven by
  the PI.
- **Codex CLI (OpenAI, `gpt-6.1-sol` / `gpt-6-astra`)** runs
  independent review passes before a release, a pre-registration or a
  submission; the briefs, reports and verdict tables are published next
  to the reviewed material whenever a pass is run.

Every scientific claim, verdict and pre-registration decision is taken
by the PI; results are reproduced by the test suite and CI, and review
reports are evidence, not endorsements. No model is listed as a
co-author of a publication or as a co-author of a commit.

Details: docs/ai_use.md.

## Licence

Code (`code/`): MIT, © 2026 L'Electron Rare (`LICENSE`). Article text,
figures and data (`article/`, `data/`): CC BY 4.0 (`LICENSE-CC-BY-4.0`).
The ReScience template files in `article/` keep their own licences
(GPL-3+, Apache 2.0 and SIL OFL for the fonts; see `article/COPYING`).

## Links

- Upstream repository: https://github.com/hypneum-lab/nerve-wml
- Original article: https://doi.org/10.1016/j.neunet.2019.01.006 · https://arxiv.org/abs/1810.12217
- ReScience C: https://rescience.github.io/write/ · https://github.com/ReScience/submissions
