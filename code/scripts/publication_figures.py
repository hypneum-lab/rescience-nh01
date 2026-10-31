"""Publication rendering of the NH-01 confirmatory and correlated figures.

Reads only the frozen outputs in ``data/`` (``summary.json`` and, for the
retrieval curves, ``cells.jsonl.gz``) and writes the two figures used in the
article. The runners' own figures (``data/*/figure.png``) are left untouched;
this script changes the rendering, never a number:

* confirmatory: same four panels as the runner's figure; panel (c) is titled
  "final states classified as spurious" (the runner wrote "spurious
  attractors"); no verdict labels in the title.
* correlated: the m = 0.30 ratio curve is drawn at T = 0 on a separate right
  axis in grey (its Hebbian denominator is bracketed by the loads 0.01 and
  0.02, so the ratio is defined but set by the load grid), and it is omitted
  at T = 0.2, where five of the ten Hebbian estimates are below the grid and
  the ratio is undefined. Absolute capacities at T = 0 are kept for every
  level. The runner's automatic "confirme" labels are not reproduced.

Usage (from the repository root, pinned environment of code/requirements.txt):

    python -I code/scripts/publication_figures.py

Environment used on 2026-10-31: numpy 2.5.4, matplotlib 3.11.2.
"""

from __future__ import annotations

import gzip
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"
OUT = ROOT / "article" / "figures"

N = 1000
FLIPS = 0.1
T_CONTROL = 0.2
T_PRIMARY = 10.0
T_GRID = (1.0, 3.0, 5.0, 7.0, 10.0, 15.0, 20.0, 30.0, 100.0)
GREEN, PURPLE, ORANGE = "#1b9e77", "#7570b3", "#d95f02"


def load_summary(name: str) -> dict:
    return json.loads((DATA / name / "summary.json").read_text())


def load_cells(name: str) -> list[dict]:
    with gzip.open(DATA / name / "cells.jsonl.gz", "rt") as f:
        return [json.loads(line) for line in f]


def mean_curve(records: list[dict], temp: float, arm: str, t: float, field: str) -> tuple[np.ndarray, np.ndarray]:
    sel = [r for r in records if r["temp"] == temp and r["arm"] == arm and r["t"] == t]
    alphas = sorted({r["alpha"] for r in sel})
    seeds = {r["seed"] for r in sel}
    curve = np.zeros(len(alphas))
    for r in sel:
        curve[alphas.index(r["alpha"])] += r[field] / len(seeds)
    return np.array(alphas), curve


def ci_arrays(entry: dict, key: str) -> np.ndarray:
    return np.array([entry[f"{t:g}"][key] for t in T_GRID])


def errorbar(ax, x, d, **kw):
    ax.errorbar(x, d[:, 0], yerr=[d[:, 0] - d[:, 1], d[:, 2] - d[:, 0]], **kw)


def figure_confirmatory() -> None:
    summary = load_summary("nh01_confirmatory")
    records = load_cells("nh01_confirmatory")
    conds = summary["conditions"]
    t_star = summary["verdict"]["C2_unimodal"]["t_star"]
    x = np.log10(np.array(T_GRID))
    fig, axes = plt.subplots(2, 2, figsize=(11, 8.5))

    ax = axes[0, 0]
    for temp, ls in ((0.0, "-"), (T_CONTROL, "--")):
        e = conds[f"T{temp:g}_f{FLIPS:g}_N{N}"]
        errorbar(ax, x, ci_arrays(e["dream"], "mean_ci"), color=GREEN, ls=ls, marker="o",
                 label=f"dream, T = {temp:g}")
        ax.plot(x, ci_arrays(e["shrink"], "mean_ci")[:, 0], color=ORANGE, ls=ls, marker="s",
                label=f"matched shrink c(t), T = {temp:g}")
        ax.axhline(e["hebb"]["mean_ci"][0], color="k", ls=ls, lw=0.8)
    ax.axvline(np.log10(t_star), color="grey", lw=0.8, ls=":")
    ax.set_xlabel("log10 dreaming time t")
    ax.set_ylabel("empirical capacity (mean, 95 % seed-bootstrap CI)")
    ax.set_title(f"(a) Capacity vs t, N = {N} (black: Hebb; dotted: t* = {t_star:g})")
    ax.legend(fontsize=7)

    sel = [
        ("hebb", 0.0, "Hebb", "k", "-"),
        ("dream", T_PRIMARY, f"dream t = {T_PRIMARY:g}", GREEN, "-"),
        ("dream", t_star, f"dream t* = {t_star:g}", PURPLE, "-"),
        ("shrink", T_PRIMARY, f"shrink c({T_PRIMARY:g})", ORANGE, "--"),
    ]
    ax = axes[0, 1]
    for arm, t, label, color, ls in sel:
        if label.startswith("dream t*") and t_star == T_PRIMARY:
            continue
        a, c = mean_curve(records, 0.0, arm, t, "retrieved_frac")
        ax.plot(a, c, marker="o", ms=3, color=color, ls=ls, label=label)
    ax.axhline(0.5, color="grey", lw=0.8)
    ax.set_xlabel("load alpha = P/N")
    ax.set_ylabel("retrieved fraction (mean over seeds)")
    ax.set_title(f"(b) Retrieval curves, N = {N}, T = 0")
    ax.legend(fontsize=8)

    ax = axes[1, 0]
    for arm, t, label, color, ls in sel[:2] + sel[3:]:
        a, c = mean_curve(records, 0.0, arm, t, "spurious_frac")
        ax.plot(a, c, marker="o", ms=3, color=color, ls=ls, label=label)
    ax.set_xlabel("load alpha = P/N")
    ax.set_ylabel("fraction of probes")
    ax.set_title(f"(c) Final states classified as spurious, N = {N}, T = 0")
    ax.legend(fontsize=8)

    ax = axes[1, 1]
    for temp, ls in ((0.0, "-"), (T_CONTROL, "--")):
        e = conds[f"T{temp:g}_f{FLIPS:g}_N{N}"]
        errorbar(ax, x, ci_arrays(e["dream"], "ratio_mean_ci"), color=GREEN, ls=ls, marker="o",
                 label=f"dream / Hebb, T = {temp:g}")
        errorbar(ax, x, ci_arrays(e["shrink"], "ratio_mean_ci"), color=ORANGE, ls=ls, marker="s",
                 label=f"shrink / Hebb, T = {temp:g}")
    ax.axhline(3.0, color="grey", lw=0.8, ls=":")
    ax.axhline(1.1, color="grey", lw=0.8, ls=":")
    ax.set_xlabel("log10 dreaming time t")
    ax.set_ylabel("capacity ratio to Hebb (mean, 95 % CI)")
    ax.set_title(f"(d) Ratios, N = {N}: T = 0 (solid) vs T = {T_CONTROL:g} (dashed)")
    ax.legend(fontsize=7)

    fig.tight_layout()
    fig.savefig(OUT / "figure-confirmatory.png", dpi=130)
    plt.close(fig)


def figure_correlated() -> None:
    summary = load_summary("nh01_correlated")
    levels = summary["levels"]
    x = np.log10(np.array(T_GRID))
    colors = {"0": GREEN, "0.15": PURPLE, "0.3": ORANGE}
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.8))

    # (a) T = 0: m = 0 and 0.15 on the left axis, m = 0.30 on a grey right axis
    ax = axes[0]
    ax2 = ax.twinx()
    for mk, lv in levels.items():
        e = lv["conditions"][f"T0_f{FLIPS:g}_N{N}"]
        d, s = ci_arrays(e["dream"], "ratio_mean_ci"), ci_arrays(e["shrink"], "ratio_mean_ci")
        if mk == "0.3":
            errorbar(ax2, x, d, color="grey", marker="o", mfc="none", ls=":",
                     label="dream m = 0.30 (right axis; Hebbian crossing inside loads 0.01–0.02)")
            ax2.plot(x, s[:, 0], color="grey", marker="s", mfc="none", ls="--",
                     label="shrink m = 0.30 (right axis)")
            continue
        errorbar(ax, x, d, color=colors[mk], marker="o", label=f"dream m = {mk}")
        ax.plot(x, s[:, 0], color=colors[mk], marker="s", ls="--", label=f"shrink m = {mk}")
    ax.axhline(3.0, color="grey", lw=0.8, ls=":")
    ax.axhline(1.1, color="grey", lw=0.8, ls=":")
    ax.set_xlabel("log10 dreaming time t")
    ax.set_ylabel("capacity ratio to Hebb, m = 0 and 0.15 (mean, 95 % CI)")
    ax2.set_ylabel("ratio, m = 0.30 (grid-limited denominator)", color="grey")
    ax2.tick_params(axis="y", colors="grey")
    ax.set_title(f"(a) Ratios, N = {N}, T = 0")
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, fontsize=6.5, loc="center right")

    # (b) T = 0.2: m = 0.30 omitted (five Hebbian denominators below the grid)
    ax = axes[1]
    for mk, lv in levels.items():
        if mk == "0.3":
            continue
        e = lv["conditions"][f"T{T_CONTROL:g}_f{FLIPS:g}_N{N}"]
        errorbar(ax, x, ci_arrays(e["dream"], "ratio_mean_ci"), color=colors[mk], marker="o",
                 label=f"dream m = {mk}")
        errorbar(ax, x, ci_arrays(e["shrink"], "ratio_mean_ci"), color=colors[mk], marker="s",
                 ls="--", label=f"shrink m = {mk}")
    flags = levels["0.3"]["conditions"][f"T{T_CONTROL:g}_f{FLIPS:g}_N{N}"]["hebb"]["flags"]
    n_below = sum(f == "below_grid" for f in flags)
    ax.text(0.02, 0.97, f"m = 0.30 omitted: Hebbian estimate below the load grid on {n_below}/10 seeds\n"
            "(ratio undefined)", transform=ax.transAxes, va="top", fontsize=7.5, color="dimgrey")
    ax.axhline(3.0, color="grey", lw=0.8, ls=":")
    ax.axhline(1.1, color="grey", lw=0.8, ls=":")
    ax.set_xlabel("log10 dreaming time t")
    ax.set_ylabel("capacity ratio to Hebb (mean, 95 % CI)")
    ax.set_title(f"(b) Ratios, N = {N}, T = {T_CONTROL:g}")
    ax.legend(fontsize=7, loc="center left")

    # (c) absolute capacities at T = 0, every level
    ax = axes[2]
    for mk, lv in levels.items():
        e = lv["conditions"][f"T0_f{FLIPS:g}_N{N}"]
        h = e["hebb"]["mean_ci"][0]
        d = [h] + [e["dream"][f"{t:g}"]["mean_ci"][0] for t in T_GRID]
        ax.plot(np.log10(np.array([0.3] + list(T_GRID))), d, color=colors[mk], marker="o",
                label=f"m = {mk} (t* = {lv['verdict']['C2_unimodal']['t_star']:g})")
    ax.set_xlabel("log10 t (leftmost point: Hebb)")
    ax.set_ylabel("empirical capacity (mean over seeds)")
    ax.set_title("(c) Capacity vs t, T = 0")
    ax.legend(fontsize=8)

    fig.tight_layout()
    fig.savefig(OUT / "figure-correlated.png", dpi=130)
    plt.close(fig)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    figure_confirmatory()
    figure_correlated()
    print("written:", OUT / "figure-confirmatory.png", OUT / "figure-correlated.png")
