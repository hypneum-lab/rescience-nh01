"""Publication rendering of the post-freeze NH-01 diagonal ablation (D4).

Reads only ``data/nh01_diagonal_ablation/summary.json`` (per-seed capacity
estimates of the two arms at every dreaming time) and writes
``article/figures/figure-diagonal.png``. It is a plot, not an experiment:
no cell is recomputed. Intervals are the seed-level percentile bootstrap of
the frozen runner (``bootstrap_mean_ci`` imported verbatim from
``code/experiments/nh01_hopfield_dream/run.py``: 10 000 resamples, seed
20261025), the same as in the article tables.

* (a) empirical capacity versus t for ``dream_offdiag`` (J_ii(t) = 0, the
  protocol of the article) and ``dream_diag`` (diagonal of J(t) kept in the
  field); the leftmost point of each curve is t = 0, i.e. the Hebbian
  kernel in the same convention.
* (b) dream/Hebb capacity ratio versus t, each arm over its own t = 0
  baseline; the mixed ratio (kept-diagonal dream over zero-diagonal Hebb),
  which corresponds to no published protocol, is drawn in grey.

Usage (from the repository root, pinned environment of code/requirements.txt):

    python -I code/scripts/figure_diagonal_ablation.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))
from experiments.nh01_hopfield_dream.run import bootstrap_mean_ci  # noqa: E402

DATA = ROOT / "data" / "nh01_diagonal_ablation"
OUT = ROOT / "article" / "figures"
GREEN, PURPLE = "#1b9e77", "#7570b3"
T0_POS = 0.3  # plotting position of t = 0 on the log axis (Hebbian kernel)


def per_seed(curves: dict, arm: str) -> tuple[list[float], np.ndarray]:
    ts = sorted(curves[arm], key=float)
    return [float(t) for t in ts], np.array([curves[arm][t]["alpha_c_per_seed"] for t in ts])


def ci_rows(rows: np.ndarray) -> np.ndarray:
    return np.array([bootstrap_mean_ci(r) for r in rows])


def errorbar(ax, x, d, **kw):
    ax.errorbar(x, d[:, 0], yerr=[d[:, 0] - d[:, 1], d[:, 2] - d[:, 0]], capsize=2, **kw)


def main() -> None:
    summary = json.loads((DATA / "summary.json").read_text())
    curves = summary["curves"]
    t_star = summary["t_star_fixed"]
    ts, off = per_seed(curves, "dream_offdiag")
    ts_d, dia = per_seed(curves, "dream_diag")
    assert ts == ts_d and ts[0] == 0.0
    x = np.log10(np.array([T0_POS] + ts[1:]))

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.3))

    ax = axes[0]
    errorbar(ax, x, ci_rows(off), color=GREEN, marker="o",
             label="J_ii(t) = 0 (dream_offdiag, protocol of this article)")
    errorbar(ax, x, ci_rows(dia), color=PURPLE, marker="s", ls="--",
             label="diagonal of J(t) kept (dream_diag)")
    ax.axvline(np.log10(t_star), color="grey", lw=0.8, ls=":")
    ax.set_xticks(x, ["0\n(Hebb)"] + [f"{t:g}" for t in ts[1:]])
    ax.set_xlabel("dreaming time t (log scale; leftmost point: Hebb, t = 0)")
    ax.set_ylabel("empirical capacity (mean, 95 % seed-bootstrap CI)")
    ax.set_title(f"(a) Capacity vs t, N = 1000, T = 0, seeds 200–209 (dotted: t = {t_star:g})",
                 fontsize=9)
    ax.legend(fontsize=7.5, loc="lower right")

    ax = axes[1]
    xr = x[1:]
    errorbar(ax, xr, ci_rows(off[1:] / off[0]), color=GREEN, marker="o",
             label="J_ii = 0 in both arms")
    errorbar(ax, xr, ci_rows(dia[1:] / dia[0]), color=PURPLE, marker="s", ls="--",
             label="diagonal kept in both arms")
    errorbar(ax, xr, ci_rows(dia[1:] / off[0]), color="grey", marker="^", ls=":", mfc="none",
             label="mixed: kept-diagonal dream / zero-diagonal Hebb (no published protocol)")
    ax.axhline(3.0, color="grey", lw=0.8, ls=":")
    ax.set_xticks(xr, [f"{t:g}" for t in ts[1:]])
    ax.set_xlabel("dreaming time t (log scale)")
    ax.set_ylabel("capacity ratio to Hebb (mean, 95 % CI)")
    ax.set_ylim(0.9, 4.1)
    ax.set_title("(b) Ratio to the Hebbian baseline (dotted: C1 threshold 3.0)", fontsize=9)
    ax.legend(fontsize=7.5, loc="lower left")

    fig.tight_layout()
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "figure-diagonal.png", dpi=130)
    plt.close(fig)
    print("written:", OUT / "figure-diagonal.png")


if __name__ == "__main__":
    main()
