---
title: "[Re] Dreaming neural networks: forgetting spurious memories and reinforcing pure ones"
author: Clément Saillant (Hypneum Lab, Grandris, France)
note: >
  Markdown source of content.tex for the ReScience C template (regenerated
  by md2tex.sh). Every number is read from a file of data/ of this
  repository (copied from hypneum-lab/nerve-wml); the short identifiers
  D1-D4 and S1-S4 refer to the provenance table of the Appendix.
---

# Introduction

Fachechi, Agliari and Barra [@fachechi2019dreaming] (Neural Networks 112,
2019, 24–40; arXiv:1810.12217) revisit the "unlearning" idea of Hopfield,
Feinstein and Palmer [@hopfield1983unlearning] and derive a closed-form
"dreaming" kernel for the Hopfield model. Starting from the Hebbian coupling
matrix $J = \frac{1}{N}\sum_{\mu=1}^{P}\xi^\mu\xi^{\mu\mathsf T}$ built from
$P = \alpha N$ random $\pm1$ patterns, a sleep phase of duration $t$ produces

$$J(t) = J\,(1+t)\,(\mathbb 1 + tJ)^{-1},$$

which equals $J$ at $t = 0$ and tends to the projection (pseudo-inverse) rule
of Kanter and Sompolinsky [@kanter1987projector] as $t \to \infty$. The
article's statistical-mechanics analysis predicts that the critical storage
load $\alpha_c(t)$ rises from the Amit–Gutfreund–Sompolinsky value
[@amit1985storing] $\approx 0.138$ at $t = 0$ towards the theoretical bound $\alpha = 1$, that
spurious (mixture) attractors are removed, that pure patterns are reinforced,
and that the gain is robust to thermal noise. The original Monte Carlo
checks (Section 2.5 of the published article) use, for the magnetisation
curves, single-spin-flip Glauber dynamics measured after equilibration on
networks of $N = 5\,000$ neurons averaged over $M = 10$ pattern realisations
(their Fig. 7, loads $P/N \in \{0.02, 0.08, 0.32\}$, $t \in \{0, 0.1, 1, 10,
100, 1000\}$) and a finite-size comparison at $N \in \{500, 1\,000,
5\,000\}$ (their Fig. 8). The zero-noise internal-field and basin analyses
(their Figs. 9–10) use the *parallel* sign update of their Eq. (2.17) at
$N = 1\,000$, $P = 50$. For the fields (Fig. 9) the network starts from
random configurations, 20 evolutions for each of 20 pattern realisations;
for the basins (Fig. 10) it starts from the first stored pattern with each
bit flipped independently with probability $p$, success being declared when
that pattern carries the largest Mattis overlap, 200 evolutions for each of
200 realisations. The replica-symmetric capacity rises from
$\alpha_c(0) \simeq 0.138$ to $\alpha_c \simeq 1.07$ as $t \to \infty$,
the excess over Gardner's bound being attributed to replica-symmetry
breaking. No capacity curve is measured by Monte Carlo in the original: the
simulations verify magnetisations, fields and basins against the theory.

We independently implement the published kernel and *partially*
replicate its qualitative claims at finite size ($N \le 1\,000$) with a new,
noisy-cue capacity estimator and new random seeds: we test the retrieval
gain, the removal of spurious final states, the robustness to thermal noise
and the projector limit, and we do not reproduce the replica-symmetric
capacity curve nor the original Monte Carlo figures. Each of the three
studies was pre-registered and frozen by an annotated git tag before its own
main run; the later registrations were informed by the preceding studies
(Section "Pre-registration"). The replication was carried out inside
the Hypneum Lab research programme (issue hypneum-lab/nerve-wml#68), where the
dreaming kernel serves as a reference operation; the replication stands on
its own and makes no claim about that programme.

Beyond replicating, we add one control absent from the original work: a
uniform multiplicative rescaling ("downscale") of the Hebbian couplings,
matched to the dreamed kernel on the Frobenius norm. This control answers a
question the original article does not ask — whether the benefit of dreaming
could be reproduced by a global reduction of synaptic strength, as in
homeostatic-downscaling accounts of sleep [@tononi2014shy] — and it provides
a calibrated null for the capacity ratio. Finally, we test the kernel on
correlated patterns, which the original article treats only for
independent patterns.

# Methods

## Original model

Binary units $s_i \in \{\pm1\}$, $i = 1 \dots N$; patterns
$\xi^\mu \in \{\pm1\}^N$ i.i.d. uniform; Hebbian kernel as above; dreamed
kernel $J(t)$. In pattern space, $J_{ij}(t) = \frac1N\sum_{\mu\nu}\xi_i^\mu
[(1+t)(\mathbb 1 + tC)^{-1}]_{\mu\nu}\xi_j^\nu$ with
$C_{\mu\nu} = \frac1N\xi^\mu\!\cdot\xi^\nu$. The eigenvalues
$\lambda \ge 0$ of $J$ map to $\lambda(1+t)/(1+t\lambda)$. Retrieval is
assessed by the overlap $m = \frac1N\sum_i s_i\xi_i^\mu$ of the final state
with a stored pattern.

## Implementation

Our code (S1: `run.py`, `confirmatory.py`, `correlated.py`; 713 + 384 +
237 lines, NumPy only, no original code reused) computes $J(t)$
by spectral decomposition of the symmetric $J$ (`numpy.linalg.` `eigh`, negative
numerical eigenvalues clipped to 0). Twenty test functions (23 executed
cases) check that $J(0) = J$, that the spectral form equals the pattern-space
closed form on 2-pattern and many-pattern cases, that $t = 10^{8}$
approximates the projector within the tested tolerance, that the matched
shrink is exactly inert at zero temperature
(S2), and cover the confirmatory and
correlated runners.

The diagonal $J_{ii}$ is set to 0 in every arm before the dynamics. The
dynamics are asynchronous with one fresh random permutation of the $N$ units
per sweep, shared by the probes of a cell. At $T = 0$,
$s_i \leftarrow \operatorname{sign}(h_i)$ with ties ($|h_i| \le
10^{-12} N \max|J|$) resolved by keeping the current spin — a tolerance
chosen so that the rule is exactly invariant under $J \to cJ$; the run stops
at the first sweep without a flip, cap 100 sweeps (non-convergence counted
as not retrieved; none occurred in any run). At $T = 0.2$, Glauber updates
with $P(s_i = +1) = 1/(1+e^{-2\beta h_i})$, $\beta = 5$, 40 sweeps, overlap
averaged over the last 10.

Cue: a stored pattern with exactly $\operatorname{round}(0.10\,N)$ bits
flipped (overlap 0.80 at $N = 1\,000$; 0.8125, 0.797, 0.797 at $N = 64$,
128, 256 because of rounding). Probes: the first $\min(P, 32)$ stored
patterns, i.e. 10 and 20 probes at the loads 0.01 and 0.02 of the correlated
run. The pilot also includes a descriptive $T = 0$ condition with $f = 0$
(unperturbed stored-pattern cues), absent from the two $N = 1\,000$ studies.
Final states are classified as `retrieved` ($m \ge 0.9$; $0.8$ at
$T = 0.2$), `other_stored` or `spurious`. Capacity estimator per
(arm, seed): $\hat\alpha_c$ is the linearly interpolated 0.5 crossing
of the retrieval fraction $r(\alpha)$ immediately after the *last* grid load
with $r \ge 0.5$, on the grid
$\alpha \in \{0.04,\allowbreak 0.06,\allowbreak \dots,\allowbreak 0.20,\allowbreak 0.25,\allowbreak \dots,\allowbreak 0.95\}$ (24 values;
0.01 and 0.02 added for the correlated run). If the largest load still has
$r \ge 0.5$ the estimate is right-censored at 0.95; if no load reaches 0.5
the code records the flag `below_grid` and a zero sentinel, which marks
censoring, not a measured zero capacity. Patterns are nested in
$\alpha$ and the same patterns, cues and update orders are used for every
arm of a cell (paired design). Statistics are paired per-seed ratios and
differences, mean over 10 seeds with a 95 % percentile bootstrap CI (10 000
seed-level resamples, bootstrap seed 20261025). Every random draw comes from
`numpy.random.default_rng(` `[20261025, seed, N, stream])`.

## Matched uniform-shrink control (added)

For each $t > 0$, $J_c = c(t)\,J$ with
$c(t) = \|\mathrm{offdiag}\,J(t)\|_F / \|\mathrm{offdiag}\,J\|_F$, i.e.
equal global synaptic budget; $c$ depends on $t$, $\alpha$, $N$ and the
seed and the correlation level; across the shrink arms it ranges from
0.0884 to 0.9985. Two facts were declared
before any run so that the control cannot be misread: at $T = 0$ the sign
dynamics is invariant under $c > 0$, so the control must give a ratio of
exactly 1 (an implementation check, not an empirical hypothesis); at $T > 0$,
$J_c$ at inverse temperature $\beta$ has the same transition probabilities as
$J$ at $c\beta$, i.e. the control is the Hebbian network at temperature
$T/c$. (The same rescaling of $\beta$ makes the $(1+t)$-normalised kernel
used here and its unnormalised ridge form statistically equivalent: their
partition functions coincide up to $\beta \to \beta (P/N)(1+t)/t$, as noted
by Agliari et al. [@agliari2024regularization] in their footnote 9 (also
footnote 2, p. 117 [PDF 121], of Aquaro's thesis [@aquaro2025thesis]); at $T = 0$ the
normalisation has no effect.) This identity does not impose a deterministic inequality on a
finite-time, thresholded, single-realisation capacity estimate (in the pilot,
seed 6 at $N = 256$, $T = 0.2$ gives a shrink ratio of 1.012), so the effect
at $T = 0.2$ is measured empirically.

## Correlated patterns (added)

One ancestor $a \in \{\pm1\}^N$ per (seed, level); each pattern bit equals
$a_i$ with probability $(1+m)/2$, so the mean pairwise overlap is $m^2$.
Levels $m \in \{0, 0.15, 0.30\}$ ($q \in \{0, 0.0225, 0.09\}$), seeds
100–109 (disjoint from the independent-pattern seeds 0–9).

## Pre-registration and decision rules

Three L1 pre-registrations, each frozen by an annotated tag pushed to GitHub
before launch and each archived by Software Heritage (verbatim copies in
`prereg/` of the submission repository, S3):

- **Pilot** (tag of 2026-10-25, S3): $N \in \{64, 128,
  256\}$, $t \in \{0, 0.3, 1, 3, 10, 30, 100\}$, three conditions.
- **Confirmatory** (second tag of 2026-10-25): $N = 1\,000$,
  $t \in \{0,\allowbreak 1,\allowbreak 3,\allowbreak 5,\allowbreak 7,\allowbreak 10,\allowbreak 15,\allowbreak 20,\allowbreak 30,\allowbreak 100\}$, $T \in \{0, 0.2\}$.
- **Correlated** (tag of 2026-10-27): as confirmatory, three
  correlation levels, 26 loads.

Binding criteria at $t = 10$: **C1** (gain) confirmed if the CI lower bound
of the ratio $R$ of the dreamed ($t = 10$) to the Hebbian capacity at
$T = 0$ is $\ge 3$, refuted if the CI upper bound of the paired difference is
$< 0.1$; **C2′** (shape) holds if the median curve $t \mapsto \hat\alpha_c$
is unimodal within 0.02 with an interior maximum $t^*$; **C3′** (control)
holds if the CI upper bound of
the ratio $S$ of the shrink ($c(10)$) to the Hebbian capacity at
$T = 0.2$ is $< 1.1$, refutes if the lower bound is $\ge 2$; the $T = 0$
ratio must be exactly 1 on every seed, otherwise the run is void. **P4**
(secondary label): spurious final states at $\alpha \in \{0.14, 0.20\}$
reduced by $\ge 50$ %. **C4** (correlated run): paired difference
$R(m = 0.30) - R(m = 0)$ with CI excluding 0. Seeds whose Hebbian
$\hat\alpha_c$ is below the grid have an undefined ratio.

These are the confirmatory and correlated criteria. The pilot registration
used the original C2 (monotonicity of the median curve, tolerated decrease
0.05 per grid step), C3 at $T = 0$ only, and P4 at loads 0.10 and 0.14; the
confirmatory amendment replaced C2 by C2′ and moved C3 to $T = 0.2$ after
the pilot had been observed, and the correlated registration was written
after both independent-pattern studies. The pilot's median curve decreases
from 0.600 to 0.522 between $t = 10$ and $t = 100$ and passed C2 only because
no single step exceeded 0.05.

## What was changed with respect to the original, and why

1. Finite $N \le 1\,000$ and an empirical, noisy-cue, 0.5-crossing capacity
   estimator instead of the replica-theory $\alpha_c(t)$: absolute
   capacities are therefore not comparable with the published curve; the
   replication tests ratios and qualitative claims (gain, spurious removal,
   projector limit).
2. Self-coupling removed ($J_{ii} = 0$) in all arms. The field printed
   in the original article sums over $j = 1 \dots N$ (their Eq. 2.16), and
   the later work of the original group and its students does not follow
   a single convention. Some algorithms remove the diagonal before the
   dynamics: "Remove the diagonal terms from $J$" opens Algorithm 1 of
   Agliari et al. [@agliari2024hebbian], Algorithm 2 of Agliari et al.
   [@agliari2024regularization] as numbered in arXiv:2308.01421v2, where
   the kernel itself is computed with its diagonal (footnotes 4-5) and the
   diagonal is zeroed only for the dynamics; Aquaro's thesis
   [@aquaro2025thesis] is a secondary source here: its Algorithm 7 (p. 120
   [PDF 124]) is identical to Algorithm 2 above, and its Algorithm 4
   (p. 104 [PDF 108]) is the only one of the three without a published
   counterpart. In both, the thesis removes the diagonal only in the
   dynamics: the kernel keeps it (Eqs. 2.117 and 2.200) and the loss
   allows $j = i$ (note 1, Sec. 2.3). Thesis page numbers are printed
   pages, with the PDF page in brackets where recorded. A master's thesis supervised by
   Agliari sets $J_{ii} = 0$ and leaves it unchanged by unlearning
   [@canali2017thesis] (winter session, academic year 2016-2017; Definition
   5.1 and Eq. 6.2, pp. 35 and 52-56); the
   zero-temperature update of Agliari et al. [@agliari2026exponential]
   uses overlaps with site $i$ excluded (Algorithm 1). Barra et al.
   [@barra2025supralinear] (Eqs. 42-44) handle repeated-index tuples that
   are double-counted in the perfect square of their dense Hamiltonian; this
   concerns the combinatorics of the dense energy, not the $J_{ii}$
   convention. Others keep it: the 2022 preprint by
   the same six authors as [@agliari2024hebbian] iterates
   $\sigma \leftarrow \operatorname{sign}(J\sigma)$ with the full kernel
   [@aquaro2022recurrent] (Eqs. 2.41-2.42); the multidirectional dreaming
   model of Barra et al. [@barra2027dlam] sums over all $i, j$ (Eq. 4 and
   Algorithm 1 as numbered in arXiv:2605.13721v1); Alemanno's thesis
   [@alemanno2021thesis] keeps it in the dreamed kernel (Eq. 2.29, p. 72 [PDF 77])
   while excluding $j = i$ from the field of its reference Hopfield model
   (PDF p. 45); and Agliari et al. [@agliari2025empty] include self-interactions
   in their main analysis (Appendix E), set the diagonal to zero only in the
   training of their Appendix A, and note that in the Hopfield model the
   diagonal raises the one-step magnetisation from
   $\operatorname{erf}(1/\sqrt{2\alpha})$ to
   $\operatorname{erf}((1+\alpha)/\sqrt{2\alpha})$ (footnote 3). Table
   \ref{tbl:conv} lists fourteen further texts, from the same school and
   outside it. Two of them compare the two conventions, for the Hebbian
   kernel only. Folli, Leonetti and Ruocco [@folli2017maximum] keep the
   diagonal and test whether each stored pattern is a fixed point after
   one parallel sign update: the diagonal adds $P$ coherent terms to the
   local field ($N + P - 1$ instead of $N - 1$; Sec. 3.1 and footnote 2,
   p. 3), and the second region of near-perfect recall that they find at
   $P \gg N$ disappears when $J_{ii} = 0$ (Fig. 6 and text, p. 6).
   Vinci, Galluzzi and Mattia [@vinci2025beyond], for deterministic
   graded units with $J_{ii} = g\alpha$, find an overlap with the
   pattern used as initial state close to 1 at loads where the same
   networks with $J_{ii} = 0$ lose recall near $\alpha \approx 0.14$
   (Fig. 3, p. 5), and critical temperatures of pure and mixture states
   that are lower when $J_{ii} = 0$ (Fig. 7, p. 9); they mention dreaming
   only as an alternative that their autapses make unnecessary (p. 10),
   and the dreaming procedure they call unnecessary there (their ref. [44])
   is the article replicated here [@fachechi2019dreaming]. Their recall
   criterion, $|m_1| > 5\sqrt{v/N}$ (p. 6; Figs. 5b and 7). Our estimate from their Fig. 4b, with the
   formula $5\sqrt{v/N}$ at $N = 1\,000$, is 0.158 for $v = 1$ and 0.354 for
   $v \approx 5$, that is about 0.16 to 0.35; Vinci et al. themselves
   simulate $N = 500$. This criterion is not comparable with the overlap $\ge 0.9$
   after a cue with 10 % of flipped bits used here, so their capacities and
   ours cannot be compared directly. The rise of the Hebbian baseline in
   our ablation D4 when the diagonal is kept (0.157 to 0.251, dream/Hebb
   ratio 3.90 to 1.90; Table \ref{tbl:diag}) is the effect they predict
   (Figs. 3-4, pp. 5-6). Our inference, not tested: the freezing of the
   kept-diagonal dynamics near the cue seen in D4 is their self-field
   "flip-flop" mechanism (pp. 6-7), read with a stricter threshold. Vinci
   et al. themselves flag an open contradiction: for Kanter and Sompolinsky
   [@kanter1987projector], autapses keep recall stable beyond $\alpha_c$
   but its basin shrinks to zero at large $\alpha$ (p. 9). In the other
   direction, Sumikawa and Kabashima [@sumikawa2026diagonal] state, for
   higher-order Hopfield models, that the slowdown "cannot be attributed
   primarily to diagonal self-interaction effects" (abstract only, to be
   checked).
   None of these texts measures the effect of the convention on a
   dreamed-to-Hebb capacity ratio. NH-01 follows the first
   convention, which is also required for detailed balance under
   sequential updates (see Coolen, Kühn and Sollich [@coolen2005theory],
   and Proposition 1.3.1 of [@aquaro2025thesis], p. 11 [PDF 15], which
   restates it); this matters only for the $T = 0.2$ arm, since at
   $T = 0$ the dynamics is deterministic and no stationary distribution
   is invoked.
   ReScience C asks that replication work "be based exclusively on the
   originally published paper, although exceptions are admitted if
   properly documented in the replication article" [@rougier2017rescience]
   (p. 4). The convention $J_{ii} = 0$ is such an exception, and we
   declare it as one: it is taken from the 2024-2025 algorithms of the
   original group cited above, not from the 2019 article, whose field
   (Eq. 2.16) keeps the diagonal. Its effect is measured by the
   post-freeze ablation (Table \ref{tbl:diag}): at $t = 10$ the
   dream/Hebb ratio is 3.90 with the diagonal zeroed in both arms, 1.90
   with it kept in both arms, and the mixed ratio (kept-diagonal dream
   over zero-diagonal Hebb) is 3.05. See also
   Benedetti et al. [@benedetti2024eigenvector] (Sec. III C), for whom
   correcting the diagonal once at the end rather than at each step of an
   unlearning procedure changes which eigenvector is dreamed and lets the
   negative eigenvalue plateau overtake the positive one ("inversion"),
   and Krotov and Hopfield [@krotov2016dense] (footnote 1), for whom
   excluding repeated indices from the energy of a dense associative
   memory changes the prefactor of its capacity. For $\pm1$ spins the diagonal only adds
   the configuration-independent constant $-\frac12\sum_i J_{ii}$ to the
   energy; it acts through the zero-temperature update rule and hence
   through the capacity estimator. After the freeze of this package we
   pre-registered and ran an ablation keeping the diagonal (Section
   "Self-coupling convention", Table \ref{tbl:diag}, Figure \ref{fig:diagonal}):
   the dream/Hebb ratio depends on the convention used in both arms (with
   the diagonal kept, neither confirmed nor refuted under rule C1, applied
   as a reading aid), and
   the contribution of the self-coupling removal to the finite optimum in
   $t$ is not isolated (registered test C5 inconclusive).
3. Dynamics and success criterion: asynchronous updates at $T = 0$ instead
   of the parallel sign update of the original zero-noise field and basin
   experiments (their Eq. 2.17); a fixed number of
   flipped cue bits, $\operatorname{round}(0.10\,N)$, instead of independent
   flips with probability $p$; an absolute overlap threshold (0.9, or 0.8 at
   $T = 0.2$) instead of "largest Mattis overlap"; at $T = 0.2$, a fixed
   40-sweep window without an equilibration diagnostic.
4. Matched shrink control and correlated patterns: additions, not changes.
5. Parameters and decision rules fixed before each study's main run (grids,
   seeds, thresholds); one voided launch of the pilot (BLAS thread
   oversubscription, killed after ~150 s before the main run; log kept in
   the upstream repository, D1).

Table: Self-coupling conventions in further texts (complement to item 2;
pages as printed). "Kept": the sum over $i, j$ includes $i = j$ in the
energy or the field; "zero": $J_{ii} = 0$ is imposed. No text of this
table measures the effect of the convention on a dreamed-to-Hebb
capacity ratio. {#tbl:conv}

| Text | Convention | Where |
|----------|--------------|----------|
| Albanese et al. 2026 [@albanese2026serial], Hebbian BEG networks | kept, stated as "autapses"; the authors "speculate" that autapses contribute to the absence of a blackout catastrophe, citing [@vinci2025beyond] | Eqs. (2.2), (2.18), pp. 3, 6; Fig. 4 caption, p. 13; Fig. 7 discussion, p. 29 |
| Albanese, Barra, Cirillo 2025 [@albanese2025guerra], Gaussian couplings | zero, by definition | Definition 1, p. 3 |
| Agliari, Duarte Mourão, Fachechi, Vivo 2026 [@agliari2026spectral] | zero in the four matrices studied; the replica computation is done with the diagonal, then removed as a shift of the spectrum ($\bar\lambda(t)$ for the dreamed kernel, Lemma 1 and Theorem 1): a result on the limiting spectral density, not on fixed points | Eqs. (3), (5), (7), (8) and note 2, p-2; SM pp. p-13 to p-16 |
| Agliari, Alessandrelli, Barra, Fachechi 2026 [@agliari2026dense] | kept, repeated indices included | Eqs. (2.2)-(2.4), p. 3 |
| Agliari, Alessandrelli, Duarte Mourão, Fachechi 2025 [@agliari2025multichannel] | kept in the intra-layer field $J\sigma$, $J = N^{-1}\xi\xi^{\mathsf T}$ | p. 2 |
| Agliari, Lepre, Roscani 2026 [@agliari2026modular] | kept, prefactor $1/(2N)$ | Eq. (2.2), p. 3 |
| Agliari et al. 2026 [@agliari2026networks] | kept in the energy and in the field of the dynamics; Appendix H, on the dual of an isolated Hopfield network, writes $i < j$ | Eq. (2.1), p. 2; Eq. (4.3), p. 4; p. 17 |
| Personnaz, Guyon, Dreyfus 1985 [@personnaz1985information] | projection rule $C = AA^{I}$ with no zeroing of $C_{ii}$ stated; the stability condition $C\sigma^k = \sigma^k$ is written for this full projector | Eq. (6), p. L-362; Eq. (7), p. L-363 |
| Agliari, Barra, Bianco, Fachechi, Pallara 2026 [@agliari2026infinite] | kept in the Hamiltonian (equilibrium theory) | Eq. (2.1), PDF p. 5 (printed p. 4) |
| Benedetti, Ventura, Marinari, Ruocco, Zamponi 2022 [@benedetti2022supervised] | zero: Hebbian $J_{ii} = 0$, reset to 0 after each unlearning step; "autapses" absent | Eq. (3), p. 1; Eq. (9), p. 3; p. 9 |
| Alemanno 2026 [@alemanno2026attention] | zero in the pairwise model; in the exponential model the self-coupling, "the exponential-model analogue of the diagonal term $J_{ii}$", is kept | Definition 3, p. 3; p. 6; p. 7 |
| Barra 2008 [@barra2008thesis] | diagonal terms added to a cavity Hamiltonian give a contribution independent of the spins that vanishes after the disorder average (equilibrium, no dynamics) | Eq. (3.134), p. 97 |
| Folli, Leonetti, Ruocco 2017 [@folli2017maximum] | kept, compared with zero for the Hebbian kernel (one-step stability of stored patterns) | pp. 3, 6 |
| Vinci, Galluzzi, Mattia 2025 [@vinci2025beyond] | kept ($J_{ii} = g\alpha$), compared with zero for the Hebbian kernel (graded units); recall criterion $\lvert m_1\rvert > 5\sqrt{v/N}$, not comparable with ours; cite the replicated article as made unnecessary by autapses | Fig. 3, p. 5; p. 6; Fig. 7, p. 9; p. 10 |

# Results

## Independent patterns

Pilot (D1), $N = 256$, $T = 0$, $t = 10$: Hebb
$\hat\alpha_c = 0.175$ [0.167, 0.183] $\to$ dream 0.599 [0.591, 0.606],
ratio **3.43 [3.26, 3.60]**, difference 0.423 [0.411, 0.435]; shrink ratio
1.000 on every seed, every $N$, every $t$. Ratios at $N = 64$ and 128: 3.13
[2.74, 3.57] and 3.38 [3.21, 3.53].

Confirmatory (D2), $N = 1\,000$,
10 seeds, 9 120 cells:

| Criterion (cell) | Result | Label |
|---|---|---|
| C1 gain ($T = 0$, $t = 10$) | Hebb 0.157 [0.155, 0.160] → dream 0.607 [0.604, 0.610]; ratio **3.86 [3.79, 3.93]**; difference 0.450 [0.445, 0.454] | confirmed |
| C2′ shape ($T = 0$) | medians 0.158, 0.413, 0.571, 0.603, **0.616**, 0.606, 0.595, 0.582, 0.569, 0.527 for $t$ = 0 … 100; $t^* = 7$ (9 seeds at 7, 1 at 10); drop $\hat\alpha_c(7) - \hat\alpha_c(100)$ = 0.088 [0.082, 0.092] | holds |
| C3′ control ($T = 0.2$, $t = 10$) | Hebb 0.126 [0.125, 0.128] → shrink 0.123 [0.121, 0.125]; ratio **0.975 [0.967, 0.982]**; $T = 0$ ratio exactly 1 on every seed and $t$ | holds |
| P4 spurious ($T = 0$) | $\alpha = 0.14$: 0.159 → 0.000; $\alpha = 0.20$: 0.994 → 0.000 | holds |
| Overall | | confirmed |

At $T = 0.2$ the dreaming gain persists: ratio 3.58 [3.53, 3.64] at
$t = 10$, 3.62 [3.55, 3.68] at $t = 7$. At $T = 0$ the Hebbian estimate
falls with size (0.211, 0.179, 0.175, 0.157 for $N$ = 64, 128, 256, 1 000; the
thermodynamic value is 0.138) while the dreamed capacity stays
$\approx 0.60$; the ratio grows for that reason. At loads 0.14 and 0.20 no
dream $t = 10$ probe is classified as spurious; at higher loads some are
(e.g. all 32 at $\alpha = 0.8$, seed 0), so the claim is load-specific.

![NH-01 confirmatory run, $N = 1\,000$, seeds 0–9 (D2; publication rendering by `code/scripts/publication_figures.py`, the runner's own figure is kept in `data/`). (a) Empirical capacity $\hat\alpha_c$ versus dreaming time $t$ for the dreamed kernel (circles) and the matched uniform-shrink control (squares) at $T = 0$ (solid) and $T = 0.2$ (dashed); the horizontal lines are the Hebbian reference; the dotted vertical line marks $t^* = 7$. (b) Retrieved fraction versus load $\alpha$ at $T = 0$ for Hebb, dream $t = 10$, dream $t^* = 7$ and shrink $c(10)$. (c) Fraction of probes whose final state is classified as spurious, versus load, $T = 0$. (d) Capacity ratio to Hebb with seed-level 95 % bootstrap intervals; the dotted lines are the pre-registered thresholds 3.0 (confirmation) and 1.1 (control).](figures/figure-confirmatory.png){#fig:confirmatory width=100%}

## Correlated patterns

Correlated run (D3), $N = 1\,000$, seeds 100–109,
29 640 cells, $t = 10$ unless stated.

Table: $T = 0$, $t = 10$ (C1, C2′). {#tbl:corr0}

| Level $m$ ($q = m^2$) | Hebb $\hat\alpha_c$ | dream $\hat\alpha_c$ | C1 ratio | C2′ $t^*$ (per-seed range); drop to $t = 100$ |
|---|---|---|---|---|
| 0 (0) | 0.160 [0.158, 0.162] | 0.611 [0.606, 0.616] | **3.82 [3.77, 3.88]** — confirmed | 7 (5–10); 0.084 [0.079, 0.089] — holds |
| 0.15 (0.0225) | 0.068 [0.066, 0.070] | 0.616 [0.612, 0.619] | **9.06 [8.84, 9.29]** — confirmed | 7 (7–10); 0.088 [0.085, 0.090] — holds |
| 0.30 (0.09) | 0.014 [0.014, 0.015] (every seed between loads 0.01 and 0.02) | 0.636 [0.633, 0.639] | **44.38 [42.56, 46.97]** — registered C1 confirmed; crossings bracketed by loads 0.01–0.02, magnitude grid-sensitive (see text) | 10 (7–10); 0.103 [0.098, 0.108] — holds |

Table: $T = 0.2$, $t = 10$ (C3′) and level verdict. {#tbl:corr02}

| Level $m$ | Hebb $\hat\alpha_c$ | C3′ shrink ratio | Level verdict |
|---|---|---|---|
| 0 | 0.127 [0.125, 0.129] | **0.979 [0.974, 0.984]** — holds | **confirmed** |
| 0.15 | 0.054 [0.053, 0.056] | **0.986 [0.979, 0.993]** — holds | **confirmed** |
| 0.30 | 5/10 seeds below grid; zero-coded mean 0.007 [0.003, 0.011] | undefined on 5 seeds; zero-coded five-seed statistic 0.6 [0.2, 1.0], two of its shrink numerators also below grid | registered: confirmed; post-analysis assessment: **inconclusive** |

Reading rule for $m = 0.30$. At $T = 0$ all ten Hebbian crossings are
bracketed by the loads 0.01 and 0.02 (flags `ok`; the registration added
these two loads for that purpose), so the registered ratio 44.38 is defined
and its C1 label is confirmed. Its bootstrap interval describes seed
variation conditional on the interpolation rule and does not include the
load-grid discretisation error; reading the crossings as anywhere inside
their bracketing intervals gives a ratio between about 30 and 65. We
therefore do not interpret the magnitude as a precise model-level capacity
ratio. At $T = 0.2$ five Hebbian estimates are below the grid; among the five
seeds with a positive Hebbian denominator, two shrink estimates are also
below the grid. The archived code replaces below-grid capacities by zero,
so the Hebbian mean 0.007 [0.003, 0.011] and the five-seed shrink statistic
0.6 [0.2, 1.0] (per-seed 1, 0, 1, 1, 0) are outputs of that coding
convention, not censoring-adjusted estimates. The absolute capacities at
$T = 0$, also interpolated but less sensitive to the small denominator, are
the more robust reading: the
dreamed capacity barely moves with correlation (0.611, 0.616, 0.636) while
the Hebbian capacity collapses (0.160, 0.068, 0.014), so the paired absolute
gain grows 0.451 [0.445, 0.456] → 0.548 [0.543, 0.552] → 0.621 [0.618,
0.625]. The tagged code labels C3′ "holds" and the level "confirmed" in
`summary.json`, computed on the five seeds with a positive denominator.
This article keeps that registered label and adds, next to it, a
post-analysis assessment of inconclusive for the level (decision of
2026-10-30, commit `5884927`): a methodological reservation, not a
registered rule. Its ground is censoring: five denominators and two further
numerators are below the grid and coded as zero, so the available bootstrap
does not estimate the ten-seed control ratio; Hebbian retrieval at
$T = 0.2$ survives only within the first load interval. The registered
labels are kept unchanged in the raw outputs. The pre-registered below-grid rule was written for C1 only;
a future amendment should extend it to C3′ and the load grid below 0.01.

C4 trend: the registered estimate is $R(0.30) - R(0)$ = 40.6 [38.7,
43.2]. The label is `gain_increases`. Its magnitude depends on the interpolation of
the small Hebbian denominator at $m = 0.30$ and the interval does not
account for load-grid resolution; we retain the increasing direction as a
descriptive result only. P4 holds at every level (0 spurious
final states under dreaming at $\alpha \in \{0.14, 0.20\}$); the $T = 0$
exactness check passed at every level. $m = 0$ reproduces the independent-
pattern run on new seeds (3.82 vs 3.86; $t^* = 7$ in both; shrink 0.979 vs
0.975).

![NH-01 correlated-pattern run, $N = 1\,000$, seeds 100–109 (D3; publication rendering by `code/scripts/publication_figures.py`). (a) Capacity ratio to Hebb versus dreaming time at $T = 0$ for ancestor overlap $m = 0$ and $0.15$ (left axis; dream: circles, matched shrink: squares, 95 % seed-bootstrap intervals); the $m = 0.30$ curves are drawn in grey on the right axis because their Hebbian denominator is bracketed by the loads 0.01 and 0.02, so the ratio is defined but set by the load grid. (b) Same at $T = 0.2$; $m = 0.30$ is omitted because five of its ten Hebbian estimates, and two further shrink estimates, are below the grid, so its ratios are undefined or zero-coded. (c) Absolute capacity versus $t$ at $T = 0$ for the three levels (leftmost point: Hebb), the robust reading at $m = 0.30$. The unmodified runner figure, whose automatic title labels every level "confirme", is kept in `data/`.](figures/figure-correlated.png){#fig:correlated width=100%}

## Internal reproduction of the $N = 1\,000$ studies

Both $N = 1\,000$ runs were re-executed on 2026-10-30 from a fresh clone
checked out at the tag, with the SHA-256 of the executed files checked
against `git show` `<tag>:` `<file>` before launch and the tag record fetched from
the GitHub API before launch (D2 and D3, directory
`provenance-rerun-20261030/`). Result: **9 120 /
9 120** and **29 640 / 29 640** cells identical to the committed
`cells.jsonl.gz` on every field except the wall-clock `task_seconds` (cells
matched by key, NaN compared as NaN); `summary.json` identical except its
`run_meta` block; `figure.png` byte-identical (SHA-256 `3b64a94e…` and
`de3ee720…`). The re-runs used 2 worker processes instead of 4 for the
confirmatory run; the worker count changes only the scheduling.

## Self-coupling convention (post-freeze ablation)

This subsection reports a study run after the submission package was
frozen on 2026-10-31; every number above is unchanged. A
fourth L1 pre-registration (S4: hypneum-lab/nerve-wml, tag
`prereg-nh01-` `diagonal-20261031`, 2026-10-31 16:38:17 UTC; run launched
58 s later; data D4) compares, at $N = 1\,000$, $T = 0$, on new seeds
200–209, two arms at every $t$ of the confirmatory grid: `dream_offdiag`,
an exact replica of the confirmatory dream arm ($J_{ii}(t) = 0$), and
`dream_diag`, in which the diagonal of $J(t)$ is kept in the update field,
as in the field printed in the original article. At $t = 0$ each arm is
the Hebbian kernel in its own convention ($J_{ii} = P/N$ kept in
`dream_diag`). Cues, dynamics, estimator and bootstrap are those of the
confirmatory run; 4 800 cells, no non-converged probe, no right-censored
estimate.

The registered question was the cause of the finite optimum $t^* = 7$,
through the per-seed drop $D = \hat\alpha_c(7) - \hat\alpha_c(100)$. The
positive control passed ($D$ = 0.086 [0.082, 0.090] in `dream_offdiag`,
overlapping the confirmatory 0.088 [0.082, 0.092]). **C5** (primary):
$D$ = 0.048 [0.043, 0.054] in `dream_diag`, **inconclusive** under the
registered thresholds ($\le 0.020$ for "cause", $\ge 0.050$ with a lower
bound above 0.020 for "not the cause"). **C6** (secondary): the paired
difference of the drops is 0.038 [0.032, 0.043], positive on 10/10 seeds:
removing the self-coupling contributes to the drop between $t = 7$ and
$t = 100$, but whether it causes the finite optimum is not decided. With
the diagonal kept the curve has another shape (Figure \ref{fig:diagonal}):
it peaks on the grid at $t = 1$ (all ten seeds; the only grid point
strictly between 0 and 3 is $t = 1$) and then decreases monotonically to 0.441 (median) at
$t = 100$.

The headline ratio depends on the convention used in both arms
(Table \ref{tbl:diag}). The ablation did not register C1; its thresholds
are applied here as a reading aid only.

Table: Dream/Hebb capacity ratio at $T = 0$, $t = 10$, by self-coupling
convention. Mean over seeds, 95 % seed-level percentile bootstrap (10 000
resamples, seed 20261025); D2: confirmatory run, D4: ablation. {#tbl:diag}

| Convention (both arms) | Seeds | Hebb $\hat\alpha_c$ | dream $\hat\alpha_c$, $t = 10$ | Ratio | Reading under rule C1 |
|---------|------|----------|----------|---------|----------|
| $J_{ii} = 0$ (D2, this article) | 0–9 | 0.157 [0.155, 0.160] | 0.607 [0.604, 0.610] | **3.86 [3.79, 3.93]** | confirmed (registered) |
| $J_{ii} = 0$ (D4) | 200–209 | 0.157 [0.155, 0.159] | 0.611 [0.607, 0.614] | **3.90 [3.86, 3.94]** | above the C1 threshold (descriptive) |
| diagonal kept (D4) | 200–209 | 0.251 [0.246, 0.256] | 0.477 [0.475, 0.480] | **1.90 [1.86, 1.95]** | neither confirmed nor refuted under rule C1 |

Note to the table: the Hebb value 0.251 for the kept diagonal is the mean
over seeds; the median is 0.250, and it is the median that the data file
carries. A mixed ratio, the kept-diagonal dreamed capacity over
the zero-diagonal Hebbian baseline, is 3.05 [3.00, 3.09]; it corresponds
to no published protocol and is given for completeness only. Student-$t$
intervals, as quoted in our comment on the submission issue, are
[1.85, 1.96] for the kept-diagonal ratio and [2.99, 3.10] for the mixed
one. For the kept-diagonal convention the lower bound 1.86 is below the
confirmation threshold 3 and the paired difference, 0.226 [0.220, 0.233],
is above the refutation bound 0.1.

The diagonal acts in opposite directions on the two arms. In the Hebbian
baseline the self-coupling $J_{ii} = P/N$ adds an inertia term to every
field and raises the noisy-cue estimate from 0.157 to 0.251 (at
$\alpha = 0.20$, 298/320 probes retrieved against 3/320 with $J_{ii} = 0$);
in the dreamed kernel at $t = 10$ it lowers the estimate from 0.611 to
0.477. At high load the kept-diagonal arm freezes near the cue: at $t = 7$,
$\alpha = 0.50$ it retrieves 129/320 probes (318/320 with $J_{ii} = 0$)
with a mean overlap of 0.90 with the cued pattern, against a retrieval
threshold of 0.9 and a cue overlap of 0.80, so in that arm
$\hat\alpha_c$ depends on the threshold more than in the zero-diagonal
arm. The ablation does not test cue noise, synchronous dynamics, finite
$N$, $T = 0.2$, correlated patterns or the matched-shrink control.

![Post-freeze self-coupling ablation, $N = 1\,000$, $T = 0$, seeds 200–209 (D4; rendering by `code/scripts/figure_diagonal_ablation.py` from `summary.json`). (a) Empirical capacity versus dreaming time for the zero-diagonal arm (`dream_offdiag`, the protocol of this article, circles) and the kept-diagonal arm (`dream_diag`, squares); the leftmost point of each curve is the Hebbian kernel in the same convention; the dotted vertical line marks the registered $t^* = 7$. (b) Ratio to the Hebbian baseline, each arm over its own $t = 0$ point; grey: mixed ratio of the kept-diagonal dream to the zero-diagonal Hebbian baseline, which corresponds to no published protocol; the dotted line is the C1 threshold 3.0. Error bars: 95 % seed-level percentile bootstrap.](figures/figure-diagonal.png){#fig:diagonal width=100%}

# Conclusion

Under decision rules fixed before each study's main run, this partial
replication **supports** the central qualitative claims of Fachechi, Agliari
and Barra within our finite-size protocol: the dreamed kernel raises the
empirical storage capacity of the Hopfield network by a large factor
(3.4–3.9 at $t = 10$ for independent patterns, $N$ = 256 to 1 000), leaves
0/320 probes classified as spurious at each of the loads 0.14 and 0.20 in
the confirmatory run at $T = 0$, against 51/320 and 318/320 under Hebb
(which does not establish the absence of spurious attractors elsewhere in
state space), keeps its
advantage under thermal noise, and behaves as the projector rule for large
$t$ (the pilot's $f = 0$ capacity estimate is right-censored at $\alpha =
0.95$ at the tested times $t \in \{10, 30, 100\}$ for $N \in \{64, 128,
256\}$ — a 50 %-retrieval criterion on at most 32 probed
patterns, not a test that every stored pattern is a fixed point). The ratios
3.86 and 9.06 are results of this study, not numbers published in 2019. On
correlated patterns the gain
grows with correlation at $m \le 0.15$, consistent with the projector
limit's insensitivity to pattern correlations.

Two points go beyond, or qualify, the original. First, the added control
shows that the Frobenius-matched uniform rescalings of the Hebbian couplings
tested here do not reproduce the gain: they are inert at $T = 0$ by scale
invariance and give a mean paired relative capacity reduction of 2.52 % at
$T = 0.2$ (seed-bootstrap 95 % interval 1.80–3.35 %). The dreaming effect is a
spectral change of the attractor landscape, not a global downscaling at
equal synaptic budget. Second, with the
self-coupling removed and a noisy cue, the finite-size capacity is not
monotone in $t$: it peaks at $t^* = 7$ and loses 0.088 [0.082, 0.092] by
$t = 100$. This does not contradict the mean-field $\alpha_c(t)$: our
noisy-cue threshold differs from the equilibrium retrieval boundary of the
theory. We
observe a lower empirical capacity at $t = 100$ than at the grid optimum
$t = 7$ without measuring basin sizes or isolating the cause (self-coupling
removal, cue noise, asynchronous dynamics, finite $N$). The original article
does quantify retrieval basins, at $N = 1\,000$ and $\alpha = 0.05$ under
parallel zero-noise dynamics, and finds them stabilised by dreaming; that
experiment does not cover our higher-load protocol. An interior optimum
in a dreaming budget is published elsewhere. For Hopfield-Feinstein-Palmer
unlearning, Marinari, Rossi and Zamponi [@marinari2026clipping] report a
recognition rate that peaks at a finite number of dreaming steps and then
returns to zero, the optimal number growing with the load (Fig. 2a,
p. 5), and an optimum in the balance of learning and dreaming steps that
is a narrow line without synaptic bounds and a broad region with them
(Figs. 4 and 5, pp. 6-7). In the multidirectional model of Barra et al.
[@barra2027dlam] the optimum is interior in the fraction of a fixed total
dreaming budget given to one layer (Fig. 8, p. 13), while the retrieval
region of the same article widens with $t$ in its phase diagrams (Fig. 4,
right, p. 10; Fig. 6, left, p. 12). Neither uses the closed-form kernel
$J(t)$ with our estimator, and neither bears on the cause of the optimum
observed here.

The $t^*$ of this article is a dreaming time. It differs from the
early-stopping time
$t^*(t_d) \approx (2\bar\lambda)^{-1}\log(1 + t_d\bar\lambda)$, with
$\bar\lambda$ the mean eigenvalue of the empirical correlation matrix of
the centred, $1/P$-normalised stored vectors (Eq. 33 of Agliari et al. [@agliari2024regularization], Appendix C, a
rough estimate restated as Eq. 4.50 of Aquaro's thesis
[@aquaro2025thesis], Appendix E, p. 154 [PDF 158]),
which is a training time. In the equivalence established by Agliari et
al. [@agliari2024regularization] the dreamed kernel with dreaming time
$t_d$ is the ridge estimator with Tikhonov parameter $\epsilon_J = 1/t_d$,
and $t^*(t_d)$ is the time at which unregularised gradient descent must
be stopped to approximate it. Under that identity a finite optimal
dreaming time reads as a finite optimal regularisation strength; this is
a reading, not a result of this study. The same group reports that, when
the stored vectors are noisy examples of archetypes, too long a dreaming
time leads to overfitting (their Sections 4 and 5); that
mechanism has no direct counterpart in our protocol, whose stored
patterns are noise-free and whose noise is in the cue.

Recent work situates these observations. Benedetti et al.
[@benedetti2024eigenvector] follow the eigenvectors of the coupling matrix
during unlearning, the spectral reading that distinguishes dreaming from a
rescaling in our control. Serricchio et al. [@serricchio2025daydreaming]
combine reinforcement and removal in a "daydreaming" algorithm and report
its effectiveness on correlated data generated by a random-features model,
a correlation structure different from our single ancestor. Lucibello and
Mézard [@lucibello2024exponential] make precise, for dense associative
memories, the distinction between the capacity of a typical pattern, of all
patterns and the size of the basins — the distinction that also separates
our noisy-cue estimator from a test of the stability of every stored
pattern.

What this replication cannot settle: absolute capacities (finite-size,
estimator-dependent), temperatures other than 0 and 0.2, correlation
structures other than a single ancestor, and the $m = 0.30$ level, where the
Hebbian crossings lie inside the first load interval (0.01–0.02) at $T = 0$
and below the grid on five seeds at $T = 0.2$. Nor does it settle whether
dreaming removes mixture states as such: the `spurious` label of P4 is a
residual class (neither retrieved nor another stored pattern), not a test
of mixtures. Two tests would address this; neither was run. The first
follows the stability of the symmetric 3-mixtures
$\operatorname{sign}(\xi^1 + \xi^2 + \xi^3)$ as a function of $t$. The
second is the spectral acceptance test of Agliari et al.
[@agliari2025multichannel]: a final state $\bar\sigma$ is accepted only if
$\bar\sigma^{\mathsf T} J^{K} \bar\sigma / N > 0.8$, where $J^{K}$ is the
pseudo-inverse coupling matrix, obtained there as the fixed point of an
iterative unlearning rule started from the Hebbian matrix; the stored
patterns span the eigenspace of eigenvalue 1 of $J^{K}$, and spurious
states fall outside it because of the nonlinearity of the sign (p. 3;
Appendix C, p. 8). The threshold 0.8 is fixed there without
calibration against a null. A scale sweep (nerve-wml#90) is open and not included here.

# Reproducibility

The submission repository <https://github.com/hypneum-lab/rescience-nh01>
(MIT for the code, CC BY 4.0 for the text and figures) holds the runners
(S1), the tests (S2), the three pre-registrations (S3), the three data sets
(D1–D3) and the provenance files of the internal re-runs. The runners are
the files of `experiments/` `nh01_hopfield_dream/` of hypneum-lab/nerve-wml at
the tag `prereg-nh01-correlated-20261027` (commit `df9a1e7`), whose SHA-256
are recorded in `code/CODE_SHA256_AT_TAG.txt`; the pilot tag freezes the
pilot protocol only, the code it ran is the first runner commit after it.
Software Heritage snapshot
\texttt{swh:1:snp:\allowbreak{}0124\allowbreak{}2c8b\allowbreak{}5873\allowbreak{}518a\allowbreak{}503b\allowbreak{}84a8\allowbreak{}0ce3\allowbreak{}a302\allowbreak{}bb69\allowbreak{}b8a8}
(visit 2026-10-29) holds the three tags as releases; the data are archived
at Zenodo under DOI 10.5281/\allowbreak{}zenodo.23833431 (nerve-wml v1.10.0, concept DOI
10.5281/\allowbreak{}zenodo.19656342).

The post-freeze ablation adds its pre-registration (S4) and its data (D4,
not in that Zenodo version). They were produced by the runner
`diagonal_ablation.py` of hypneum-lab/nerve-wml at the tag of S4, which
imports the frozen `run.py` unchanged (identical SHA-256).

Environment: Python 3.12.15, numpy 2.5.4, matplotlib 3.11.2 (full freeze in
the re-run provenance directory of D2 and D3), single-threaded BLAS
(the OpenMP, OpenBLAS, MKL and NumExpr thread counts set to 1), no GPU;
host electron-server, 8 logical CPUs (Intel Xeon X5680, no AVX), Linux
6.8.0, shared with other jobs (load 7–20), `nice 19`. Every random draw
comes from NumPy's default generator seeded by (20261025, seed, $N$,
stream); bootstrap seed 20261025, 10 000 resamples.

Commands (from `code/`; wall times from each `run_meta.json`):

```
python -m experiments.nh01_hopfield_dream.run \
    --workers 4 --out results/nh01           # D1: 1 547 s
python -m experiments.nh01_hopfield_dream.confirmatory \
    --workers 4 --out results/nh01_confirmatory   # D2: 6 951 s
python -m experiments.nh01_hopfield_dream.correlated \
    --workers 2 --out results/nh01_correlated     # D3: 22 866 s
gzip -k results/<run>/cells.jsonl   # the comparator reads .gz
python -I scripts/compare_nh01.py \
    ../data/<run> results/<run> cmp.json
```

The confirmatory run started 14 s after its tag was pushed (2026-10-25,
13:47:22 UTC); the correlated run on 2026-10-27 at 16:48:06 UTC. The
comparator does not set a failure exit status; it writes five fields into
`cmp.json`:

```
keys_equal   cells_differing_non_timing   fields_differing
max_abs_diff   summary_equal_excl_run_meta
```

Exact reproduction means matching keys and zero non-timing differences; on
another platform, the reported differences are read against the tolerance
below. The exit status alone validates nothing. The option `--analyze-only` recomputes `summary.json` and
`figure.png` from an
existing `cells.jsonl`. Unit tests run in seconds; the pilot takes about
26 min on 8 cores; the two $N = 1\,000$ runs 2–8 h depending on the number
of workers (the re-runs with 2 workers took 15 136 s and 30 547 s).

Expected outputs are the committed `summary.json` files. The two
$N = 1\,000$ studies were reproduced on the original host with exact
non-timing cell values and identical figure files; on another platform,
cell keys and discrete outcomes (classifications, flags, sweeps) should
match exactly and floating-point diagnostics (`c_fro`, `energy_own`) to
about $10^{-12}$, while PNG byte identity is not required. The pilot is not
covered by the internal re-run.

# Appendix: provenance table

| Id | Content | Location in the submission repository |
|--|------|------------|
| D1 | pilot, $N \in \{64, 128, 256\}$, 28 080 cells | `data/nh01/` (`summary.json`, `cells.jsonl.gz`, `run_meta.json`, `figure.png`, `SHA256SUMS`) |
| D2 | confirmatory, $N = 1\,000$, 9 120 cells, re-run provenance | `data/nh01_confirmatory/` (same files; `provenance-rerun-` `20261030/`) |
| D3 | correlated, $N = 1\,000$, 29 640 cells, re-run provenance | `data/nh01_correlated/` (same files; `provenance-rerun-` `20261030/`) |
| D4 | post-freeze self-coupling ablation, $N = 1\,000$, 4 800 cells (nerve-wml commit `d6c42c2`) | `data/nh01_diagonal_` `ablation/` (`summary.json`, `cells.jsonl.gz`, `run_meta.json`, `run.log`, `launch_record.md`, `SHA256SUMS`) |
| S1 | runners `run.py`, `confirmatory.py`, `correlated.py` at the correlated tag | `code/experiments/` `nh01_hopfield_dream/`; hashes in `code/` `CODE_SHA256_AT_TAG.txt` |
| S2 | unit tests (20 functions, 23 cases) | `code/tests/` `test_nh01_hopfield_dream.py` |
| S3 | the three pre-registrations, verbatim copies of the tagged files (tag names in `prereg/README`) | `prereg/` |
| S4 | post-freeze pre-registration of the self-coupling ablation, verbatim copy at tag `prereg-nh01-` `diagonal-` `20261031` (revision `swh:1:rev:` `6e1b006…`) | `prereg/2026-10-31-` `nh01-diagonal-ablation.md` |
| F | publication rendering of the figures | `code/scripts/` `publication_figures.py`; `code/scripts/` `figure_diagonal_ablation.py` (D4) |

# AI usage

Claude Code (Anthropic) was used as a tool for the code, the documentation and drafts of this text, in sessions driven by the author; every draft was read, corrected and arbitrated by the author. Codex CLI (OpenAI; gpt-6.1-sol, then gpt-6-astra) ran two automated checks of the finished package before submission; the briefs, reports and verdict tables are in `review/`. These checks are not peer review. The design, the three pre-registrations, every verdict and every number in this article were checked and decided by the author. Development history: hypneum-lab/nerve-wml pull requests #81, #86 and #87, issue #68.

# References

- [@fachechi2019dreaming] Fachechi A., Agliari E., Barra A. (2019).
  Dreaming neural networks: forgetting spurious memories and reinforcing
  pure ones. *Neural Networks* 112, 24–40. doi:10.1016/j.neunet.2019.01.006.
  arXiv:1810.12217.
- [@hopfield1983unlearning] Hopfield J. J., Feinstein D. I., Palmer R. G.
  (1983). "Unlearning" has a stabilizing effect in collective memories.
  *Nature* 304, 158–159.
- [@amit1985storing] Amit D. J., Gutfreund H., Sompolinsky H. (1985).
  Storing infinite numbers of patterns in a spin-glass model of neural
  networks. *Phys. Rev. Lett.* 55, 1530.
- [@benedetti2024eigenvector] Benedetti M., Carillo L., Marinari E., Mézard M.
  (2024). Eigenvector dreaming. *J. Stat. Mech.* 2024, 013302.
  doi:10.1088/1742-5468/ad138e.
- [@serricchio2025daydreaming] Serricchio L., Bocchi D., Chilin C., Marino R.,
  Negri M., Cammarota C., Ricci-Tersenghi F. (2025). Daydreaming Hopfield
  networks and their surprising effectiveness on correlated data. *Neural
  Networks* 186, 107216. doi:10.1016/j.neunet.2025.107216.
- [@lucibello2024exponential] Lucibello C., Mézard M. (2024). Exponential
  capacity of dense associative memories. *Phys. Rev. Lett.* 132, 077301.
  doi:10.1103/PhysRevLett.132.077301.
- [@kanter1987projector] Kanter I., Sompolinsky H. (1987). Associative
  recall of memory without errors. *Phys. Rev. A* 35, 380.
- [@tononi2014shy] Tononi G., Cirelli C. (2014). Sleep and the price of
  plasticity. *Neuron* 81, 12–34.
- [@agliari2024hebbian] Agliari E., Alemanno F., Aquaro M., Barra A.,
  Durante F., Kanter I. (2024). Hebbian dreaming for small datasets.
  *Neural Networks* 173, 106174. doi:10.1016/j.neunet.2024.106174.
- [@agliari2024regularization] Agliari E., Alemanno F., Aquaro M.,
  Fachechi A. (2024). Regularization, early-stopping and dreaming: a
  Hopfield-like setup to address generalization and overfitting. *Neural
  Networks* 177, 106389. doi:10.1016/j.neunet.2024.106389.
  arXiv:2308.01421.
- [@aquaro2025thesis] Aquaro M. (2025). Applications of spin glass theory
  in neural networks and evolutionary models. PhD thesis, Sapienza
  Università di Roma (defended 2025-02-21). hdl:11573/1739810,
  https://iris.uniroma1.it/handle/11573/1739810. Page numbers from the
  author's PDF dated 2024-10-28 (167 pp.), which may differ from the
  deposited version; printed pages, PDF page = printed + 4.
- [@coolen2005theory] Coolen A. C. C., Kühn R., Sollich P. (2005). *Theory
  of neural information processing systems*. Oxford University Press.
  doi:10.1093/oso/9780198530237.001.0001.
- [@canali2017thesis] Canali A. (2017, winter session, AY 2016-2017). Intelligenza artificiale nella
  fase REM. Master's thesis (supervisor E. Agliari), Sapienza Università
  di Roma. In Italian.
- [@alemanno2021thesis] Alemanno F. (2021). Neural networks and learning
  machines: from mathematical foundation to applications in biological
  complexity. PhD thesis, Università del Salento.
- [@aquaro2022recurrent] Aquaro M., Alemanno F., Kanter I., Durante F.,
  Agliari E., Barra A. (2022). Recurrent neural networks that generalize
  from examples and optimize by dreaming. arXiv:2204.07954.
- [@agliari2025empty] Agliari E., Fachechi A., Luongo D. (2025). The
  importance of being empty: a spectral approach to Hopfield neural
  networks with diluted examples. arXiv:2503.15353.
- [@barra2025supralinear] Barra A., Centonze M. S., Marra Solazzo M.,
  Tantari D. (2025). On the supra-linear storage in dense networks of grid
  and place cells. arXiv:2511.02441.
- [@agliari2026exponential] Agliari E., Barra A., Ladiana A., Lepre A.
  (2026). Exponential capacity in multilayer hetero-associative neural
  networks. arXiv:2607.29554.
- [@barra2027dlam] Barra A., Durante F., Ladiana A., Marra Solazzo M.
  (2027). Do Hopfield networks dream of stored patterns? A
  statistical-mechanical theory of dreaming in multidirectional
  associative memories. *Neural Networks* 206, 109729.
  doi:10.1016/j.neunet.2026.109729. arXiv:2605.13721.
- [@krotov2016dense] Krotov D., Hopfield J. J. (2016). Dense associative
  memory for pattern recognition. *Advances in Neural Information
  Processing Systems* 29, 1172–1180. arXiv:1606.01164.
- [@albanese2026serial] Albanese L., Alessandrelli A., Barra A., Cirillo
  E. N. M. (2026). Serial vs parallel recall in the Blume-Every-Griffiths
  neural networks. arXiv:2601.07777.
- [@albanese2025guerra] Albanese L., Barra A., Cirillo E. N. M. (2025).
  Guerra interpolation for inverse freezing. *J. Math. Phys.* 66, 123305.
  doi:10.1063/5.0280543. arXiv:2505.06202.
- [@agliari2026spectral] Agliari E., Duarte Mourão P., Fachechi A., Vivo
  P. (2026). Spectral criteria for generalization in unsupervised Hebbian
  nets. arXiv:2606.04651.
- [@agliari2026dense] Agliari E., Alessandrelli A., Barra A., Fachechi A.
  (2026). Dense auto-hetero associative memories applied to noisy
  communication channels. arXiv:2609.32605.
- [@agliari2025multichannel] Agliari E., Alessandrelli A., Duarte Mourão
  P., Fachechi A. (2025). Multi-channel pattern reconstruction through
  L-directional associative memories. arXiv:2503.06274.
- [@agliari2026modular] Agliari E., Lepre A., Roscani E. (2026).
  Classifications in modular restricted Boltzmann machines.
  arXiv:2610.08612.
- [@agliari2026networks] Agliari E., Alessandrelli A., Barra A., Centonze
  M., Ricci-Tersenghi F. (2026). Networks of Hebbian networks: more is
  different. *Neural Networks* 194, 108181.
  doi:10.1016/j.neunet.2025.108181. arXiv:2501.16789.
- [@personnaz1985information] Personnaz L., Guyon I., Dreyfus G. (1985).
  Information storage and retrieval in spin-glass like neural networks.
  *J. Physique Lettres* 46, L359–L365.
  doi:10.1051/jphyslet:01985004608035900.
- [@agliari2026infinite] Agliari E., Barra A., Bianco P., Fachechi A.,
  Pallara D. (2026). The infinite volume limit of the Hopfield neural
  networks in the replica-symmetric regime. *Ann. Henri Poincaré*.
  doi:10.1007/s00023-026-01770-4. arXiv:2409.10145.
- [@benedetti2022supervised] Benedetti M., Ventura E., Marinari E.,
  Ruocco G., Zamponi F. (2022). Supervised perceptron learning vs
  unsupervised Hebbian unlearning. *J. Chem. Phys.* 156, 104107.
  doi:10.1063/5.0084219. arXiv:2201.00032.
- [@alemanno2026attention] Alemanno F. (2026). Attention over noisy
  examples: generalization and memorization in the exponential Hopfield
  network. arXiv:2610.22191.
- [@barra2008thesis] Barra A. (2008). Mean field spin glasses: exact
  results without the replica trick. PhD thesis.
- [@folli2017maximum] Folli V., Leonetti M., Ruocco G. (2017). On the
  maximum storage capacity of the Hopfield model. *Front. Comput.
  Neurosci.* 10, 144. doi:10.3389/fncom.2016.00144.
- [@vinci2025beyond] Vinci G. V., Galluzzi A., Mattia M. (2025). Beyond
  catastrophic forgetting in associative networks with self-interactions.
  arXiv:2504.04560.
- [@sumikawa2026diagonal] Sumikawa Y., Kabashima Y. (2026). Testing the
  role of diagonal interactions in high-order Hopfield models via
  dynamical mean-field theory. arXiv:2604.03115.
- [@rougier2017rescience] Rougier N. P., Hinsen K., et al. (2017).
  Sustainable computational science: the ReScience initiative. *PeerJ
  Comput. Sci.* 3, e142. doi:10.7717/peerj-cs.142. arXiv:1707.04393.
- [@marinari2026clipping] Marinari E., Rossi S., Zamponi F. (2026).
  Dreaming improves memorization in a Hopfield model with bounded
  synaptic strength. arXiv:2603.09384.
