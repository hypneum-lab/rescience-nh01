Rôle : relecteur indépendant (reproductibilité numérique, statistiques, ReScience C). Tu relis un brouillon de protocole L0 ; tu n'en es pas l'auteur.

Entrée : le dépôt `repos/rescience-nh01`, branche `prereg/arm-reproduction-gb300` (PR #6, brouillon), un commit au-dessus du tag `submission-20261031` / `origin/main` :
- `docs/prereg/arm-reproduction/protocol.md` ;
- `docs/prereg/arm-reproduction/check_arm_repro.py`.
Contexte : `README.md` (sections « Reproduce » et « Determinism », lignes 80–107), `code/README.md`, `code/run.sh`, `code/requirements.txt`, `code/scripts/compare_nh01.py`, `code/experiments/nh01_hopfield_dream/*.py`, `data/*/` (cells, summary, run_meta, provenance-rerun-20261030). Fiche matérielle de la cible : `../stack.md` (DGX Station GB300, Grace aarch64).

Objet : une reproduction post-tag, sur aarch64, des runs confirmatory et correlated (N = 1 000). Contraintes : ne pas toucher le tag, l'article, `README.md`, `code/`, `data/` ; tolérances reprises du critère existant (« clés et résultats discrets identiques, diagnostics flottants à environ 1e-12, figure.png non exigée ») ; bande 1e-12–1e-9 = bit-exactitude « inconclusive » mais affirmations confirmées si les résultats discrets sont identiques (seuil marqué TBD by PI) ; NumPy, BLAS et un seul thread fixés.

Livrables (rapport en français, chemin:ligne pour chaque constat) :
1. Erreurs factuelles du protocole vs le dépôt (versions, graines, nombres de cellules et de tâches, durées et estimations, commandes, chemins).
2. `check_arm_repro.py` : bugs, cas non couverts (NaN, inf, types int/float, champs absents, ordre, doublons, summary), classement des champs discrets vs flottants justifié ou non par le code des runners ; le script implémente-t-il exactement la règle de la section 6 ?
3. Failles de protocole : la règle peut-elle conclure « reproduced » à tort, ou « not reproduced » pour une raison triviale ; la bande inconclusive est-elle cohérente ; les commandes (pip --require-hashes, probe, run.sh, gzip, comparateur) marchent-elles telles qu'écrites ; risques propres à aarch64 (BLAS, eigh, pages 64 Ko).
4. « TBD by PI » mal posés ou manquants ; ce qui manque avant le gel.
Échelle : BLOQUANT / MAJEUR / MINEUR / OK. Si c'est invérifiable, dis-le. Ne modifie rien dans `repos/`. Tu peux lancer `python3 -I` sur de petits fichiers de `data/` (pas de run NH-01). Écris le rapport dans `../report-sol.md`.
