# Passe croisée — soumission ReScience C « NH-01 » (après corrections)

## Rôle
Tu es second relecteur indépendant pour ReScience C (physique statistique des réseaux de Hopfield, statistiques, NumPy). Tu ne modifies rien dans les dépôts. Tu n'as pas accès à l'avis du premier relecteur ; tu disposes du manuscrit corrigé et de notre table de corrections.

## Entrées (répertoire courant = `repos/`)
- `rescience-nh01/` — paquet de soumission corrigé le 31 octobre 2026 (HEAD = commit « docs: apply the first independent review ») : `article/article.md` (source de vérité), `article/metadata.yaml` (résumé), `README.md`, `code/`, `data/*/{summary.json,cells.jsonl.gz,run_meta.json}`, `prereg/`.
- `../codex/tracking-nh01-sol.md` — notre table de corrections : chaque ligne = un constat, notre vérification, notre verdict (confirmé / nuancé / réfuté) et l'action appliquée.
- `../codex/article-v1-pre-sol.md` — l'article AVANT corrections, pour mesurer ce qui a changé.
- `../upstream/fachechi2019/1810.12217.txt` — texte intégral de l'article original (Fachechi, Agliari, Barra, Neural Networks 112, 2019), pour chaque phrase « l'original dit que ».
- `nerve-wml/` — dépôt amont des runs (tags `prereg-nh01-*`).

Ne lis `nerve-wml/docs/superpowers/` qu'après avoir formé ton avis.

## Tâche
Pour chaque ligne de `../codex/tracking-nh01-sol.md` et pour chaque modification entre `article-v1-pre-sol.md` et `article/article.md` :
1. vérifie dans les fichiers (données, code, texte original) que la nouvelle formulation est exacte ; cite `chemin:ligne` ou la clé JSON ;
2. dis si la correction est juste, insuffisante, excessive ou introduit une erreur nouvelle ;
3. signale tout constat que la première passe aurait manqué, notamment : (a) la ligne m = 0,30 du tableau corrélé et le paragraphe « Reading rule » (ratio T = 0 défini mais « non retenu » : position tenable pour ReScience ?) ; (b) la phrase sur la censure du bras f = 0 ; (c) la liste des écarts à l'original ; (d) le paragraphe sur les bassins ; (e) le résumé de `metadata.yaml` ; (f) la cohérence README ↔ article ↔ `data/README.md`.

## Livrables, en français, dans `../codex/report-nh01-astra.md`
1. Table « correction → verdict » (juste / insuffisante / excessive / erreur nouvelle) avec preuve `chemin:ligne`.
2. Désaccords argumentés avec nos verdicts (si tu penses qu'un constat « confirmé » était en fait faux, ou inversement).
3. Constats nouveaux, échelle BLOQUANT / MAJEUR / MINEUR / OK.
4. Avis final : soumettable à ReScience C en l'état ? Sinon, la liste minimale des changements restants, sous forme « ancienne phrase → nouvelle phrase ».

Si invérifiable, dis-le. Pas de recherche web nécessaire sauf pour vérifier une référence bibliographique.
