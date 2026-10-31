# Relecture indépendante — soumission ReScience C « NH-01 »

## Rôle
Tu es relecteur indépendant pour ReScience C (réplication numérique, physique statistique des réseaux de Hopfield, statistiques, Python/NumPy). Tu n'as lu aucune conclusion de l'équipe : forme ton avis à partir des fichiers seuls. Tu ne modifies rien dans les dépôts.

## Entrées (répertoire courant = `repos/`)
- `rescience-nh01/` — le paquet de soumission : `article/article.md` (source), `article/metadata.yaml`, `article/bibliography.bib`, `code/` (runner `experiments/nh01_hopfield_dream/{run,confirmatory,correlated}.py`, tests), `data/` (nh01, nh01_confirmatory, nh01_correlated : `summary.json`, `cells.jsonl.gz`, `run_meta.json`, `SHA256SUMS`, `MANIFEST.sha256`), `prereg/` (trois pré-enregistrements verbatim), `README.md`.
- `nerve-wml/` — dépôt amont où les runs ont été exécutés (tags `prereg-nh01-hopfield-dream-20261025`, `prereg-nh01-confirmatory-20261025`, `prereg-nh01-correlated-20261027` ; notes `docs/results/2026-10-2*-nh01-*.md` ; milestones `docs/milestones/2026-10-2*-nh01-*.md`).
- `../upstream/fachechi2019/1810.12217.txt` — texte intégral de l'article original (Fachechi, Agliari, Barra, Neural Networks 112, 2019, arXiv:1810.12217), pour vérifier chaque affirmation « l'original dit que ».

Ne lis `nerve-wml/docs/superpowers/` qu'après avoir formé ton avis (revues antérieures).

## Livrables, numérotés, en français, dans `../codex/report-nh01-sol.md`
1. **Conformité ReScience C** : l'article répond-il aux attentes du journal (réplication d'un résultat publié, code indépendant, description des écarts à l'original, reproductibilité) ? Ce qui manque.
2. **Code ≠ texte** : pour chaque chiffre de l'article (ratios 3,43 / 3,86 / 9,06, intervalles, t* = 7, shrink 0,975, « m = 0,30 non calculable »), retrouve-le dans `data/*/summary.json` ou recalcule-le depuis `cells.jsonl.gz` ; cite `fichier:ligne` ou la clé JSON. Signale tout écart.
3. **Fidélité à l'original** : chaque phrase sur Fachechi–Agliari–Barra (noyau, capacités 0,138 / 1,07, réglages Monte Carlo, N, réalisations, dynamique) confrontée au texte `1810.12217.txt` avec le numéro de ligne.
4. **Méthode** : nuls, contrôle « shrink apparié » (peut-il échouer ?), estimateur de capacité, bootstrap par graine (n = 10 graines : puissance), ratio à dénominateur ≈ 0 (m = 0,30), pré-enregistrement respecté (tags avant runs ? écarts déclarés ?).
5. **Reproductibilité** : `code/run.sh`, `requirements.txt`, hachages `CODE_SHA256_AT_TAG.txt` vs `nerve-wml` au tag ; manifeste des données.
6. **Rédaction** : clarté, longueur (ReScience vise ≈ 4–8 pages), figures, légendes (la figure corrélée montre une courbe à m = 0,30 que le texte neutralise : acceptable ?), bibliographie.
7. **Références 2024–2026** vérifiables (≤ 10) utiles à la discussion (dreaming/unlearning Hopfield, dense associative memories, réplications ReScience récentes).

Échelle : BLOQUANT / MAJEUR / MINEUR / OK, avec `chemin:ligne`. Si invérifiable, dis-le. Termine par une liste « corrections proposées » prêtes à appliquer (ancienne phrase → nouvelle phrase).
