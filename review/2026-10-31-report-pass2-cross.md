# Passe croisée indépendante — NH-01 après corrections

**31 octobre 2026 — paquet examiné : `rescience-nh01`, commit `1f7c6b67c32446c46768719d4fc211dbfa781d4b`, « docs: apply the first independent review ».**

**Avis : pas soumettable en l’état ; corrections ciblées encore nécessaires.** Les résultats numériques principaux sont solides dans le protocole effectivement exécuté. La plupart des corrections sont justes. Les difficultés restantes concernent surtout le traitement éditorial et statistique de `m = 0.30`, une nouvelle généralisation erronée sur les états parasites, et un PDF dont certains éléments sont coupés ou se chevauchent. Je ne demande ni de refaire les trois campagnes ni de reproduire toutes les figures de 2019 pour conserver le cadrage annoncé de réplication partielle.

## Périmètre et vérifications

Je n’ai pas ouvert `report-nh01-sol.md`, les journaux de cette première relecture, ni `nerve-wml/docs/superpowers/`. La table de corrections et le contexte préchargé de la session exposent déjà certains constats antérieurs : l’indépendance revendiquée ici est celle des vérifications, pas l’absence de connaissance de ces constats.

J’ai confronté les 30 entrées de la table de suivi et les **24 blocs de modification** du diff Markdown aux fichiers. Tous les chemins `article/…`, `code/…`, `data/…`, `prereg/…` ci-dessous sont relatifs à **`repos/rescience-nh01/`** ; les autres chemins sont donnés depuis `repos/`. Les lignes de `cells.jsonl.gz` désignent le flux décompressé ; les sélecteurs JSON constituent une identification plus stable que l’ordre des lignes.

Vérifications exécutées, sans écriture dans les dépôts :

- Lecture de **66 840 cellules uniques** : 28 080 pilote, 9 120 confirmatoires, 29 640 corrélées. Recalcul indépendant des **2 690 courbes de capacité**, de leurs drapeaux et des moyennes/intervalles bootstrap des capacités, rapports et différences : aucun désaccord avec les résumés à `10⁻¹⁴` près.
- **23 cas de test réussis**, correspondant aux 20 fonctions annoncées. Environnement de cette vérification : Python 3.14.8, NumPy 2.4.3, pytest 9.0.2 ; ce n’est pas une validation de l’installation des versions épinglées de la campagne.
- Réexécution du code fourni : **912 cellules confirmatoires, graine 0**, et **18 cellules corrélées**, `m=0.30`, graine 103, charges 0.01/0.02/0.04, bras Hebb/dream 10/shrink 10, deux températures. Résultats discrets et overlaps identiques ; seuls `c_fro` et `energy_own` diffèrent, au maximum de `9.71×10⁻¹³` sur les 930 cellules. Durée totale locale : 184 s.
- **33/33** entrées de `data/MANIFEST.sha256` conformes. Les trois `SHA256SUMS` sont conformes, y compris le hash de `cells.jsonl` après décompression en mémoire. Les quatre fichiers de `CODE_SHA256_AT_TAG.txt` correspondent au tag corrélé ; les trois préenregistrements correspondent à leurs tags ; les 15 fichiers principaux des trois runs sont identiques à ceux de `nerve-wml` au commit `d3eca42`.
- Régénération de `content.tex` dans une copie extérieure : identique au fichier fourni. Compilation complète : **9 pages, 5 références, 39 `Overfull \\hbox`, maximum 273,53 pt**. Inspection visuelle des pages 5–8, notamment du tableau corrélé et des chemins coupés. Le premier essai a échoué sur l’extraction du binaire universel Biber de la machine ; l’emploi de sa tranche arm64 dans le répertoire temporaire a permis la compilation, sans modification du paquet. Ce problème d’environnement n’est pas un défaut attribué au manuscrit.

Les preuves de provenance archivées sont cohérentes avec le récit des deux réexécutions intégrales. Je n’ai pas réexécuté leurs 38 760 cellules en entier, ni revérifié en ligne Zenodo, Software Heritage, la visibilité publique du dépôt ou l’heure du push GitHub. Je distingue donc ces attestations archivées des vérifications indépendantes effectuées ici. Aucune recherche web n’a été nécessaire ; aucune référence récente proposée dans la table n’a été ajoutée au manuscrit.

## 1. Table « correction → verdict »

Le numéro est celui de `../codex/tracking-nh01-sol.md`. Le verdict porte sur **l’action réellement appliquée**, et pas seulement sur la vérité du constat initial. « Insuffisante » n’implique pas que tout le passage est faux.

| Nº | Correction / décision examinée | Verdict | Preuve et appréciation |
|---|---|---|---|
| 1 | « Every stored pattern is a fixed point » → estimateur censuré | **Juste** | `article/article.md:311` précise enfin seuil 50 % et au plus 32 motifs. `data/nh01/summary.json → conditions.T0_f0_N{64,128,256}.dream.{10,30,100}.flags` : 90/90 drapeaux `censored`. Les 17 cellules imparfaites à `t=10` existent ; exemple `cells.jsonl.gz:15894`, N=128, seed=7, α=.95, f=0 : 30/32 récupérés, 2/32 `spurious`. Ne pas étendre cette censure à tous les t : voir §3, N4. |
| 2 | `m=.30,T=0` : « not computable » → « computable but not retained » | **Insuffisante ; exclusion éditoriale excessive** | `article/article.md:251` et `:253` reconnaissent correctement les dix dénominateurs positifs, mais escamotent encore **44,3848 [42,5575 ; 46,9733]**, calculé par la règle annoncée. Preuve : `data/nh01_correlated/summary.json → levels["0.3"].conditions.T0_f0.1_N1000.dream["10"].ratio_mean_ci`, Hebb `flags=ok×10`. Une réserve de résolution est justifiée ; elle ne transforme pas ce résultat enregistré en non-résultat. La censure au numérateur à T=.2 reste omise. |
| 3 | Déclaration des écarts de dynamique, cues et succès | **Juste, portée à préciser** | `article/article.md:199` décrit les différences réelles : `code/experiments/nh01_hopfield_dream/run.py:148`, `:179`, `:246`. Original : `../upstream/fachechi2019/1810.12217.txt:1073`, `:1100`, `:1104`. Ajouter « for the original zero-noise field/basin experiments » : le Monte Carlo thermique original emploie déjà le single-spin-flip Glauber (`:926`). Le mot « original » sans cette restriction peut faire croire que tout l’original était parallèle. |
| 4 | Réplication partielle ; ratios propres à NH-01 | **Juste** | `article/article.md:47`, `:51`, `:314`. Les rapports 3,86/9,06 figurent dans les résumés NH-01 ; l’original mesure des magnétisations, champs et fréquences de récupération, pas cet estimateur : original `:916`, `:923`, `:1005`, `:1085`. Le tableau original→NH-01 promis dans le suivi n’a pas été ajouté comme tel, mais la liste explicite des écarts remplit sa fonction. |
| 5 | Reconnaissance des bassins quantifiés dans l’original | **Juste** | `article/article.md:331`–`:336` retire l’inférence de bassins rétrécis et la fausse absence de mesure originale. Original `:1099`–`:1108`, légende `:1162` : N=1000, P=50, bruit initial variable, 200×200 évolutions/réalisations. NH-01 varie principalement la charge avec f=.10 : `run.py:37`, `:48`. Réserve sur la parenthèse f=0 à `article.md:330`, §3 N4. |
| 6 | Labels C1/C2′/C3′ ≠ confirmation intégrale de 2019 | **Juste dans l’ensemble** | Le cadrage de `article/article.md:47` et `:302` rend la portée partielle explicite ; les critères sont définis à `:164`. C2′ est une hypothèse ajoutée après pilote et C3′ un contrôle ajouté, pas deux prédictions originales. Leur origine ressort de `prereg/2026-10-25-nh01-confirmatory-n1000.md:18`, `:39`, `:40`. Une ligne « labels refer to our operational criteria » améliorerait la lecture, sans rendre indispensable un nouveau tableau. |
| 7 | Nombre de tests, t du projecteur, chemin | **Juste** | `article/article.md:88` ; `code/tests/test_nh01_hopfield_dream.py:30` fournit quatre cas paramétrés, `:57` teste `t=1e8` avec `np.allclose(..., atol=1e-6)` ; 23 cas exécutés avec succès. « Within the tested tolerance » est préférable à l’ancienne égalité sans précision. |
| 8 | Overlap initial après arrondi | **Juste** | `article/article.md:108` ; `run.py:148`. `data/nh01/cells.jsonl.gz`, f=.1 : `cue_overlap=0.8125` à N=64, `0.796875` à N=128 et 256. Les 0,797 imprimés sont des arrondis corrects. |
| 9 | Suppression de « to be created » | **Juste pour le paquet local ; statut public non revérifié** | `article/article.md:352` donne l’URL et le dépôt local existe avec cette origine Git. La suppression d’un provisoire est cohérente. La publication à 09:17 UTC n’est pas démontrable par ces seuls fichiers. |
| 10 | Fig. 9 : ajout de 20×20 | **Juste pour les effectifs ; erreur nouvelle de rattachement possible** | `article/article.md:37` est conforme à original `:1055`–`:1061`. Mais la suite `article.md:39`–`:41` rattache grammaticalement la cue bruitée du premier motif et le succès au Mattis maximal aux deux figures. Fig. 9 part de **configurations initiales aléatoires** (original `:1019`, `:1056`) ; le protocole cue/succès décrit ne vaut que pour Fig. 10 (`:1100`). Séparer les deux phrases. |
| 11 | « Towards 0.138 » → décroissance descriptive avec N | **Juste** | `article/article.md:234` évite une extrapolation thermodynamique. `data/nh01/summary.json → conditions.T0_f0.1_N{64,128,256}.hebb.mean_ci` et résumé confirmatoire : 0,210993 ; 0,179143 ; 0,175340 ; 0,157475 environ. La proximité de 0,138 ne prouve pas une limite commune, et la phrase ne l’affirme plus. |
| 12 | Retrait de « as a heating must » | **Juste** | Doublon de 14. `article/article.md:320` rapporte un effet observé ; `run.py:219` établit l’identité des probabilités avec β→cβ, pas une inégalité déterministe de cet estimateur. |
| 13 | Chiffres des résultats retrouvés | **Juste pour l’arithmétique ; ne valide pas chaque interprétation** | Recalcul indépendant des 66 840 cellules et IC sans écart. Les valeurs de `article/article.md:215`, `:226`–`:229`, `:249`–`:251`, `:273` concordent avec les clés correspondantes des trois résumés. Mais « 0.007 [0.003,0.011] » à m=.30,T=.2 est une moyenne **incluant cinq sentinelles zéro**, pas une estimation non censurée de capacité moyenne. |
| 14 | Identité thermique, contre-exemple, baisse de 2,52 % | **Juste sur le fond ; erreur nouvelle mineure sur la plage de c** | `article/article.md:136`–`:141` est exact. Pilote `conditions.T0.2_f0.1_N256`, seed=6 : Hebb=.14, shrink10=.1416667, ratio=1.0119048. Confirmatoire : moyenne de `100(1−S_seed)` = **2,522746 [1,798913 ; 3,348970] %**. En revanche `article.md:132` affirme tous les c dans [.09,.999] alors que le minimum observé est **.088445268** (sélecteur §3 N6). |
| 15 | Dernier croisement, censure, sentinelle | **Juste** | `article/article.md:113`–`:120` décrit `run.py:343`–`:353`. Je retrouve **22 courbes pilote** avec retour au-dessus de .5, aucune à N=1000. Aucune courbe de ces données ne commence sous .5 puis remonte, de sorte que la différence de formulation « premier point sous le seuil » / « aucun point au-dessus » n’altère pas les résultats archivés. |
| 16 | Préenregistrements successifs et critères du pilote | **Juste** | `article/article.md:178` ; pilote prereg `:62`, `:69`, `:70` ; amendement confirmatoire `:4`, `:7`, `:18` ; prereg corrélé `:7`. Médianes pilote N=256 : .600→.559318→.522222 ; décroissances .040682 et .037096, toutes deux ≤.05. La temporalité est désormais correctement exposée. |
| 17 | Override m=.30 déclaré postérieur à l’analyse | **Insuffisante** | `article/article.md:265` nomme correctement une réserve post hoc ; commit amont `5884927` du 30/10 vérifié. Le motif invoqué à `:268`, « cannot discriminate shrink from Hebb », est trop absolu. Les données distinguent déjà les bras sur certaines cellules ; l’obstacle est l’interprétation du **rapport moyen sur les dix graines** avec censure, exclusion de cinq dénominateurs et deux numérateurs remplacés par zéro. Voir §2. |
| 18 | « Spurious » opérationnel et restriction aux charges | **Insuffisante ; erreur nouvelle dans la conclusion** | Les réserves de `article/article.md:236` et `:309` sont justes ; le contre-exemple α=.8, seed=0 est réel. Mais `:307`–`:308` dit que Hebb a « almost only spurious final states » aux charges .14 **et** .20 : moyenne **.159375** à .14, **.99375** à .20, clé `conditions.T0_f0.1_N1000.spurious`. Le tableau à `:229` donne déjà les bonnes valeurs. |
| 19 | Pilot tag sans runner : laissé hors article | **Insuffisante à l’échelle du paquet** | `git ls-tree -r prereg-nh01-hopfield-dream-20261025 -- experiments/nh01_hopfield_dream` est vide. La restriction du rerun à N=1000 est juste (`article/article.md:399`). Mais `code/run.sh:6` associe encore explicitement `bc2f838` à `run.py (pilot)`. Nommer ce tag comme gel du **protocole**, et le code pilote distribué comme version ultérieure à `df9a1e7`. Le décalage des SHA `run_meta` est visible ; son attribution à un clone superficiel n’est pas prouvée par ces SHA seuls. |
| 20 | Ajout de gzip et avertissement sur exit status | **Insuffisante** | `README.md:85`, `code/README.md:41`, `article/article.md:375` réparent bien l’incompatibilité `.jsonl`/`.gz` (`run.py:658`, `compare_nh01.py:37`). Mais `article.md:378` ne demande de lire que `keys_equal` et `summary_equal_excl_run_meta` : ils peuvent être vrais avec des cellules différentes. Il faut aussi lire `cells_differing_non_timing`, `fields_differing`, `max_abs_diff` (`compare_nh01.py:58`). Le commentaire d’usage `code/run.sh:21` reste ancien. |
| 21 | Reproduction limitée aux deux N=1000 et tolérance interplateformes | **Juste, avec réserve de formulation** | `article/article.md:285`, `:393`–`:399`, `code/README.md:62` distinguent l’identité locale et les tolérances. Mes 930 cellules concordent à <10⁻¹². Cela n’établit pas une garantie universelle d’identité discrète pour toute plateforme. `README.md:22` conserve « bit-exactly » ; mieux vaut harmoniser avec « identical non-timing cell values on the original host », car les fichiers de cellules ne sont pas identiques en octets. |
| 22 | Hash du data README | **Juste** | `data/MANIFEST.sha256` : 33 entrées, 33 concordances indépendamment recalculées. Cela corrige l’intégrité du fichier, **pas sa phrase périmée** à `data/README.md:24`. |
| 23 | Génération md→tex et retrait du TODO | **Juste** | `article/Makefile:20` ajoute la dépendance, `:32` la relie au PDF ; `article/md2tex.sh:9` effectue la conversion. Une régénération donne exactement le `content.tex` fourni ; compilation à cinq références et neuf pages. |
| 24 | Débordements : xurl ajouté, problème reporté | **Insuffisante** | `article/article.tex:6` ajoute xurl, mais les chemins en `\\texttt` restent non sécables. PDF reconstruit : **39** débordements, dont 273,53 pt ; page 8 des identifiants/chemins sortent physiquement de la feuille. Source notamment `article/content.tex:522` et `:541`, correspondant à `article/article.md:346`–`:374`. Un PDF sans erreur LaTeX n’est pas pour autant lisible. |
| 25 | Figure corrélée brute conservée, légende longue | **Insuffisante ; interdiction d’interpréter les courbes excessive** | `article/article.md:283` explique utilement les labels automatiques. `correlated.py:160` montre leur origine. Mais dire que les courbes « must not be read as a result » contredit leur statut de résultats de l’estimateur déclaré. On peut conserver une figure des résultats enregistrés **avec réserves explicites**, ou créer une figure de publication distincte ; supprimer le résultat T=0 n’est pas nécessaire. Le panneau thermique exige l’avertissement sur les sentinelles, pas seulement n=5. |
| 26 | Suppression de l’attribution causale à la diagonale / finite size | **Juste** | `article/article.md:196`, `:331`, `article/metadata.yaml:64` disent que la cause n’est pas isolée. `run.py:296` retire la diagonale pour tous les bras : il n’existe pas de comparaison avec diagonale conservée dans ces données. La baisse empirique en t reste établie. |
| 27 | Citation AGS dans le corps | **Juste** | `article/article.md:27`, `article/bibliography.bib:23` ; original `:802` pour la valeur limite. Cinq entrées effectivement rendues dans le PDF reconstruit. Aucun besoin d’une recherche bibliographique supplémentaire pour valider cette modification. |
| 28 | Titre PNG « Spurious attractors » laissé inchangé | **Insuffisante, mineure** | `confirmatory.py:268` et `article/figures/figure-confirmatory.png`, panneau c. L’ordonnée à `confirmatory.py:267` dit déjà « spurious final states (fraction) ». La légende correcte et les réserves dans le texte atténuent le problème ; pour publication, harmoniser le titre ou préciser explicitement que ce titre désigne la fraction de sondes classées, pas une proportion d’attracteurs recensés. Le gel du code des runs n’interdit pas une figure éditoriale distincte. |
| 29 | Hachages, préregs, Zenodo/SWH, tests et 912 cellules | **Juste pour ce qui est vérifié localement ; partiellement invérifiable hors ligne** | Code, trois préregs, 15 fichiers amont et manifestes vérifiés ici ; 23 tests et 912+18 cellules réexécutés. `data/nh01{_confirmatory,_correlated}/provenance-rerun-20261030/comparison.json` indique 0 différence hors temps et mêmes figures. La disponibilité distante et l’identité des 15 fichiers **sur Zenodo** n’ont pas été revérifiées : l’identité avec l’amont local ne suffit pas à les attester. |
| 30 | Références 2024–2026 proposées mais non ajoutées | **Juste de ne pas les ajouter automatiquement ; références non auditées** | `article/bibliography.bib:1`–`:52` contient toujours cinq entrées, aucune des huit propositions. Rien dans cette passe ne rend une revue de littérature récente obligatoire pour établir la fidélité au travail de 2019. Les notices proposées ne sont pas assez détaillées dans le suivi pour une vérification bibliographique locale ; je ne les valide pas. |

## 2. Désaccords argumentés avec vos verdicts et arbitrages

### 2.1 `m=0.30,T=0` : résultat défini à rapporter, précision à limiter

Je confirme le constat initial nº2 : « not computable » était faux. Je ne valide pas le maintien de son effet éditorial sous « computable but not retained ».

Les dix capacités de référence sont **0,0116667 à 0,0152632**, toutes `ok`. La statistique préenregistrée est la moyenne des rapports par graine, **44,38 [42,56 ; 46,97]**, et non le rapport des moyennes, qui vaut 44,13. Les dénominateurs sont petits et la précision en charge est grossière ; cela justifie de ne pas présenter « ×44 » comme une propriété précise du modèle ou comme une capacité thermodynamique. En revanche, le résultat de l’estimateur est parfaitement défini et son label C1 enregistré est `confirmed`.

Le préenregistrement corrélé a **expressément ajouté 0.01 et 0.02 pour rendre ce croisement mesurable** (`prereg/2026-10-27-nh01-correlated-patterns.md:19`). Sa règle d’inconclusivité C1 concerne plus de deux graines sans charge atteignant 50 % (`:35`) ; à T=0, il y en a zéro. La résolution de grille ne peut donc être présentée comme une règle enregistrée qui invaliderait C1.

**Position tenable pour ReScience : oui à une réserve post hoc explicite, oui à une conclusion globale prudente, mais avec le résultat préenregistré chiffré et son statut visible.** La nouvelle réserve doit s’ajouter au résultat, pas le remplacer dans la case qui devrait le rapporter. Ne pas retenir une interprétation quantitative extrapolée est raisonnable ; ne pas présenter la statistique enregistrée ne l’est pas à mon sens, surtout lorsqu’on publie à côté C4=40,6, qui utilise exactement ce même rapport.

L’augmentation qualitative ne dépend pas d’une précision à la deuxième décimale. Dans les données à T=0, les croisements Hebb sont entre .01 et .02 et les croisements dream10 entre .60 et .65. Sous la lecture à croisement unique entre ces charges, cela donne un encadrement conservateur **30 à 65** pour le rapport, sans choisir l’interpolation. Ce n’est **pas un IC**, ni une nouvelle analyse confirmatoire. Cela explique pourquoi l’ampleur exacte est mal résolue alors que le gain ne disparaît pas. Les capacités absolues, elles aussi interpolées, ne sont pas exemptes de cette incertitude ; la différence absolue est simplement moins sensible au petit dénominateur.

### 2.2 À T=0.2, les « cinq ratios définis » contiennent deux zéros de censure

Clé commune : `data/nh01_correlated/summary.json → levels["0.3"].conditions.T0.2_f0.1_N1000`.

| Graines | Hebb | Shrink t=10 | Ce que les données permettent de dire |
|---|---|---|---|
| 100, 104, 105 | `ok` | `ok` | Trois rapports d’estimateurs = 1. |
| 103, 107 | `ok` | `below_grid` | Le code met le numérateur à zéro ; les deux rapports codés = 0 ne sont pas des rapports de capacités mesurés à zéro. |
| 101, 102, 106, 108, 109 | `below_grid` | `below_grid` | Cinq dénominateurs codés zéro ; rapports `NaN`, exclus du bootstrap. |

`run.py:347` crée la sentinelle ; `:424` teste seulement le dénominateur ; `:364` écarte les valeurs non finies mais conserve les deux zéros. **0,6 [0,2 ; 1,0]** est donc exactement la sortie du programme sur cinq valeurs codées, et **pas un IC tenant compte de la censure**. La moyenne Hebb imprimée **0,006613 [0,002542 ; 0,010690]** a le même problème : elle utilise cinq zéros imputés.

À titre d’illustration, en traitant une capacité censurée sous .01 comme inconnue entre 0 et .01, et en gardant les autres estimations fixées, la moyenne Hebb des dix graines serait située entre **.006613 et .011613**, et la moyenne du rapport sur les cinq dénominateurs positifs entre **.600 et .926984**. Ces encadrements ne sont pas des IC et n’intègrent ni toute l’incertitude de grille ni l’échantillonnage ; ils montrent seulement pourquoi l’étiquette « censuré » ne permet pas d’interpréter directement les statistiques zéro-imputées.

Le constat nº17 doit donc être **nuancé**, pas simplement confirmé dans sa nouvelle justification. Le contrôle ne devient pas incapable de toute discrimination : à α=.01, T=.2, les fractions récupérées valent .6→.4 pour seed103 et .7→.4 pour seed107 ; la moyenne des dix graines vaut **.51 pour Hebb, .45 pour shrink**. « Hebbian retrieval essentially gone » est excessif sans préciser « beyond the first load interval ». Ces observations ne suffisent pas à une inférence générale sur dix rapports, mais elles réfutent la formulation d’une impossibilité absolue de distinguer les bras.

L’override global « inconclusive » reste défendable comme **prudence de l’auteur après analyse**, parce que l’estimand sur toutes les graines n’est pas correctement traité par le bootstrap disponible. Présenter côte à côte le verdict enregistré et cette réserve est plus transparent que remplacer le premier.

### 2.3 Bras f=0 : le constat bloquant était vrai, la correction principale suffit

Je ne conteste ni les 17 contre-exemples ni l’abandon de « every stored pattern ». Un taux de récupération à seuil d’overlap .9 ne teste pas l’identité exacte d’un point fixe ; même 32/32 récupérés ne testerait pas les autres motifs stockés. `article/article.md:311`–`:313` corrige bien cela.

Il serait toutefois excessif de rejeter la nouvelle phrase parce qu’il reste 17 cellules avec récupération <1 : la **censure à seuil 50 %** est une autre propriété, et elle est effectivement observée pour les trois tailles, les dix graines et **t∈{10,30,100}**. Le résidu à corriger est la parenthèse non qualifiée de `article.md:330` et sa fonction d’argument « in agreement », pas la véracité de la censure pour ces temps.

### 2.4 « Tout est corrigé » ne vaut ni pour le paquet ni pour le PDF

Le nº19 ne peut être clos par « hors article » lorsque le wrapper associe encore le tag pilote à un runner absent de ce tag. Le nº22 est clos pour les octets, mais le `data/README.md` qu’il protège contient encore l’ancienne explication. Les nº24–25–28 laissés à arbitrage ne sont pas neutralisés par « 0 erreur » de compilation ou par le gel des données : on peut conserver les artefacts bruts et produire une présentation de publication distincte.

Je ne demande pas systématiquement une nouvelle figure corrélée : la figure enregistrée est publiable si son statut et ses limites sont clairement exposés, sans consigne paradoxale de ne pas la lire comme un résultat. En revanche, le PDF actuellement coupé n’est pas un choix de prudence scientifique acceptable.

## 3. Constats nouveaux ou résiduels, par sévérité

### BLOQUANT

**Aucun nouveau défaut démontré du noyau NumPy ou des gains principaux qui impose d’abandonner l’étude ou de refaire les campagnes.** Le faux énoncé universel sur les points fixes a été retiré. L’avis négatif « en l’état » vient des points majeurs ci-dessous, pas d’une invalidation de 3,86 ou 9,06.

### MAJEUR

**N1 — Censure au numérateur et statistiques zéro-imputées non expliquées.** C’est le manque principal de la nouvelle ligne m=.30 (`article/article.md:251`), du Reading rule (`:257`–`:269`) et de la légende (`:283`). Cinq dénominateurs manquent, mais aussi deux des cinq numérateurs restants sont censurés. Il faut nommer la sortie du code comme telle, pas comme un IC de capacité non censurée. Preuves et graines au §2.2.

**N2 — Résultat enregistré T=0 toujours absent du tableau, et verdict global trop amalgamé.** C1 à T=0, C3′ à T=.2 et la réserve globale ne sont pas le même résultat. Le résumé `article/metadata.yaml:64` transforme encore cette situation en un niveau simplement « inconclusive », avec référence « at the lower limit » à T=0. Cela occulte le croisement strictement intérieur à .01–.02 et le verdict enregistré. Publication de 44,38 avec réserve de résolution, puis séparation du verdict enregistré et de l’appréciation post hoc : voir §2.1.

**N3 — Nouvelle erreur dans la conclusion sur Hebb à α=.14.** `article/article.md:307`–`:308` est contredit par son propre tableau `:229`. Le nombre de sondes classées parasites est **51/320** à .14, **318/320** à .20, et 0/320 sous dream10 dans les deux cas. Employer les nombres ou restreindre « almost only » à .20. Les 0/320 sont des résultats opérationnels ; je ne leur attribue pas un IC binomial de 320 essais indépendants, car les sondes partagent les motifs et la dynamique au sein d’une graine.

**N4 — Parenthèse f=0 non qualifiée et présentée comme accord avec la théorie.** `article/article.md:330` dit « our f=0 arm is censored at the grid maximum, in agreement ». Le bras n’existe **que dans le pilote**, à N≤256. À t=.3 et 1, aucun des 30 estimateurs n’est censuré ; à t=3, seuls 6/30 le sont, tous à N=64 ; à t=10,30,100, ils le sont tous. Le résultat ne compare pas la frontière d’équilibre originale au protocole NH-01 et ne suffit pas à établir cet « accord ». La reformulation sur les bassins à `:331`–`:336` est, elle, correcte et utile.

**N5 — Vérification documentaire pouvant donner un faux succès.** `article/article.md:378` ne cite pas le champ de comparaison des valeurs des cellules. J’ai vérifié sur une copie synthétique minimale du format : changer uniquement `energy_own` donne `keys_equal=true`, `summary_equal_excl_run_meta=true`, **`cells_differing_non_timing=1`**, avec exit code 0. Les deux champs recommandés ne constituent donc pas un contrôle suffisant. Il n’est pas nécessaire de modifier le runner figé : compléter les instructions et lire les champs existants.

**N6 — Lisibilité matérielle insuffisante.** Page 6, la nouvelle prose dans la case C1 m=.30 déborde sur le « 10 » de la colonne C2′. Pages 7–8, des références de provenance sont coupées ; page 8, chemins et SWHID dépassent le bord droit. Sources : `article/content.tex:377`, `:453`, `:522`, `:541`. Déplacer la prose des cellules dans une note et rendre les identifiants sécables ou les remplacer par des renvois courts résout le problème sans toucher aux données.

### MINEUR

**N7 — Plage numérique de c fausse comme encadrement.** `article/article.md:132` : le minimum est `.08844526804562963`, pour `data/nh01_correlated/cells.jsonl.gz`, `{ancestor_m:.3,N:1000,seed:107,alpha:.95,arm:"shrink",t:100,temp:0,flips:.1}`, clé `c_fro`. Maximum global hors Hebb : `.9984599080771526` (pilote). Écrire approximativement .0884–.9985, ou un véritable encadrement [.088,.999]. Ajouter m aux dépendances si elles se veulent exhaustives.

**N8 — Description originale encore ambiguë.** Le taux de flips p et le succès par Mattis maximal sont propres à Fig. 10, pas aux départs aléatoires de Fig. 9 ; les mises à jour parallèles concernent les expériences à bruit thermique nul, pas la totalité du Monte Carlo original. Sources détaillées aux nº3 et 10. Ne pas extrapoler non plus la suppression de diagonale à une modification de la thermodynamique : pour des spins ±1, le terme diagonal de l’énergie est constant ; ce sont les champs de la règle explicite (2.16)–(2.17) qui changent ici.

**N9 — Cohérence README ↔ article ↔ data README inachevée.**

| Sujet | Constat vérifié | Correction attendue |
|---|---|---|
| m=.30, T=0 | Article `:253` reconnaît un croisement encadré ; conclusion `:341`, résumé `metadata.yaml:64`, README `:18` et `:124` continuent de dire « lower limit »/« grid floor ». | Employer partout « crossing bracketed by .01 and .02, flags ok ». |
| m=.30, T=.2 | `data/README.md:24` dit « control not computable » ; article `:251` dit cinq rapports définis mais omet leurs deux numérateurs censurés. | Décrire cinq dénominateurs censurés, deux numérateurs supplémentaires censurés, et la nature zéro-codée du résumé. |
| Reproduction | `README.md:22` garde « bit-exactly » ; `data/README.md:19` et article `:294` excluent les temps. | Employer la même expression précise sur les valeurs hors temps, sur l’hôte original. |
| Build | `README.md:112` dit huit pages, alors que le PDF corrigé en a neuf. `README.md:40` dit le Makefile copié inchangé, mais `article/Makefile:20` est ajouté. | Mettre à jour ces deux indications ; mentionner aussi pandoc parmi les outils du build. |
| Tests | `README.md:81` dit « 20 tests », l’article dit 20 fonctions/23 cas. | Harmoniser sans prétendre qu’il s’agit de 23 fonctions. |
| Vérification des hashes | Les `SHA256SUMS` incluent `cells.jsonl`, absent sous forme décompressée dans `data/`. | `MANIFEST.sha256` fonctionne directement ; préciser la décompression si l’on veut exécuter aussi chacun des SHA256SUMS. Il n’y a pas de hash faux. |

**N10 — Petites précisions de méthode et résumé.** `article/metadata.yaml:64`, « ten seeds per cell » est ambigu puisque chaque ligne de cellules contient déjà une graine : écrire « ten independent seed-level realizations per condition ». `article/article.md:107` ne présente que f=.10 ; définir le bras pilote f=0 à cet endroit, avant de l’utiliser en conclusion. À m=.30, P=10/20 aux deux premières charges, donc les capacités Hebb utilisent **10/20 sondes**, pas 32 ; la règle `min(P,32)` est correcte dans l’article (`:109`, `run.py:301`), mais `prereg/2026-10-27-nh01-correlated-patterns.md:15` abrège en « 32 probes ». Signaler l’application de `min(P,32)` aux petites charges suffit ; ne pas réécrire rétrospectivement le préenregistrement figé.

**N11 — Provenance pilote et labels de figures.** Le tag pilote gèle le protocole seul (`code/run.sh:6` à corriger). Le titre « Spurious attractors » (`confirmatory.py:268`) reste plus fort que la variable opérationnelle. Le code des expériences peut rester immuable : une clarification dans le wrapper documentaire et une figure de publication n’altèrent pas la campagne.

### OK

- Les rapports **3,43**, **3,86**, **9,06**, leurs IC, la baisse moyenne du contrôle thermique et l’optimum de grille t*=7 à motifs indépendants sont soutenus par les données.
- L’identité thermique et l’invariance à T=0 sont correctement distinguées des résultats empiriques après correction.
- La différence entre capacité empirique avec cue bruitée et frontière théorique est maintenant exposée ; aucun calcul de bassin n’est artificiellement déduit de la seule baisse en t.
- Les historiques successifs des préenregistrements sont correctement déclarés. Le remplacement de C2 par C2′ n’est plus présenté comme antérieur à toute observation.
- Le projecteur est un résultat algébrique du noyau et un contrôle numérique ciblé, pas une preuve expérimentale de stabilité universelle à t=10.
- La conservation des sorties brutes et des préenregistrements figés est appropriée. Les corrections de présentation doivent vivre dans le manuscrit et sa documentation, sans effacer l’analyse enregistrée.

## 4. Couverture de chaque modification du manuscrit

Diff exact entre `../codex/article-v1-pre-sol.md` et `article/article.md`. Les lignes V1 et courantes sont celles des fichiers fournis ; les références de preuve sont développées dans la table principale et les constats ci-dessus.

| Bloc | Anciennes lignes → nouvelles lignes (`article/article.md`) | Verdict et vérification |
|---|---|---|
| D01 | 27 → 27 | **Juste** : citation AGS rendue, nº27. |
| D02 | 30–37 → 30–41 | **Juste pour paramètres, effectifs et deux dynamiques ; insuffisante pour le rattachement de la cue** : original `:926`, `:964`, `:990`, `:1055`, `:1073`, `:1100`, `:1162`. Nº3/10, N8. |
| D03 | 43–46 → 47–55 | **Juste** : portée partielle et séquence des préregs. Nº4/16. « Studies frozen » doit être compris comme protocole pour le pilote, nº19. |
| D04 | 79–84 → 88–94 | **Juste** : 20 fonctions/23 cas, t=1e8, chemin. Nº7. |
| D05 | 98 → 108–110 | **Juste** : overlaps 0,8125 / 0,796875 / 0,796875. Nº8. |
| D06 | 101–102 → 113–115 | **Juste** : dernier point au-dessus du seuil, `run.py:348`. Nº15. |
| D07 | 104–105 → 117–120 | **Juste** : deux types de censure et sentinelle, `run.py:346`–`:350`. Leur traitement statistique ultérieur reste à préciser, N1. |
| D08 | 116–121 → 131–141 | **Juste pour l’identité et le contre-exemple ; erreur nouvelle mineure sur [.09,.999]**. Nº14, N7. |
| D09 | insertion après 157 → 178–186 | **Juste** : amendement informé et deux baisses pilote inférieures à .05. Nº16. |
| D10 | 166–171 → 195–209 | **Juste pour la diagonale, la liste d’écarts, l’abandon causal et le retrait de « before any output was read » ; portée à préciser pour « original parallel »**. Nº3/26. Le log amont du lancement interrompu existe et finit à 142,3 s avec 9 360 cellules (`nerve-wml/results/nh01/run-aborted-blas-threads.log:10`) ; il ne prouve pas à lui seul l’instant exact de l’arrêt à ~150 s ni les conditions de consultation humaine. |
| D11 | 196–198 → 234–238 | **Juste** : tailles descriptives et spurious aux charges élevées. Nº11/18. Préciser T=0 pour la séquence .211→.157 éviterait de la rattacher à la phrase précédente sur T=.2. |
| D12 | 211 → 251 | **Insuffisante / nouvelle ambiguïté statistique** : nombres calculés exacts, omission de 44,38 et des numérateurs censurés. Nº2, N1–N2. |
| D13 | 213–215 → 253–259 | **Insuffisante** : définissabilité correctement réparée, mais non-rétention excessive et « absolute capacities robust » trop général sans rappeler l’interpolation. §2.1–2.2. |
| D14 | 220–226 → 264–271 | **Insuffisante** : post hoc bien reconnu, impossibilité de discrimination exagérée. Nº17. Le label global dépend de C1/C2′ et du C3′ calculé sur cinq valeurs : ce ne sont pas tous les critères qui utilisent seulement cinq graines. |
| D15 | 228–230 → 273–277 | **Juste comme réserve descriptive** : C4=40,5611 [38,7233 ; 43,1640], clé `C4_trend.diff_high_minus_zero_mean_ci`. L’IC bootstrap ignore l’erreur de discrétisation, comme les autres IC de cet estimateur ; cela ne rend pas la statistique non calculable. |
| D16 | 236 → 283 | **Insuffisante et restriction excessive** : la légende dévoile l’override mais ordonne d’ignorer un résultat réel ; la censure du numérateur n’y figure pas. Nº25. |
| D17 | 238 → 285 | **Juste** : titre limité aux deux études N=1000 ; fichiers `comparison.json` correspondants. Nº21. |
| D18 | 255–262 → 302–315 | **Juste pour “supports”, f=0 et ratios propres à NH-01 ; erreur nouvelle pour “almost only” à .14**. Nº1/4/18, N3. |
| D19 | 267–270 → 320–325 | **Juste** : restriction aux rescalings testés, effet thermique observé. Nº14/26. Préciser que 2,52 % et son IC sont la moyenne des réductions relatives appariées, pas un nouvel IC du rapport des moyennes. |
| D20 | 273–277 → 328–336 | **Juste pour les bassins et l’absence d’attribution causale ; insuffisante pour la parenthèse f=0**. Nº5/26, N4. |
| D21 | 282–283 → 341–342 | **Insuffisante** : cinq below_grid à T=.2 est exact ; « sits at the lower limit » à T=0 remplace une fausseté par une approximation encore trompeuse. Le croisement est à l’intérieur du premier intervalle, pas à la borne. |
| D22 | 293–294 → 352–353 | **Juste localement ; visibilité publique non revérifiée**. Nº9. |
| D23 | 316–318 → 375–381 | **Insuffisante** : gzip juste, champs conseillés incomplets. Nº20/N5. `--analyze-only` lit bien le fichier non compressé et régénère résumé/figure. |
| D24 | 330–331 → 393–399 | **Juste comme objectif de comparaison documenté** : restriction de provenance et tolérance cohérentes avec mes 930 cellules ; pas de preuve d’une garantie universelle de résultats discrets interplateformes. Nº21/29. |

## 5. Changements minimaux avant soumission

Les propositions suivantes sont rédigées en anglais pour être directement utilisables dans le manuscrit. Elles changent la présentation ; **aucune n’exige de réécrire les résultats archivés ni les préenregistrements**.

1. **Rapport T=0 dans le tableau**, `article/article.md:251` :
   - Ancienne : « computable but **not retained** (…) ».
   - Nouvelle : « **44.38 [42.56, 46.97] — registered C1 confirmed**; crossing bracketed by loads 0.01–0.02; magnitude sensitive to load-grid resolution. »
   - Raccourcir la case à la valeur et un appel de note ; placer l’avertissement dans le texte pour éviter le débordement.

2. **Reading rule T=0**, `article/article.md:253`–`:256` :
   - Ancienne : « defined, but its magnitude is set by the interpolation inside that interval and is not retained for quantitative interpretation ».
   - Nouvelle : « defined and reported above as the registered finite-grid statistic. Its bootstrap interval describes seed variation conditional on the interpolation rule and does not include load-grid discretisation error; we therefore do not interpret its magnitude as a precise model-level capacity ratio. »

3. **Case thermique et censure**, `article/article.md:251`, `:257`–`:269` :
   - Ancienne : « 0.007 [0.003, 0.011]; 5/10 seeds below grid (…) 0.6 [0.2, 1.0] on the 5 defined seeds (…) a five-seed control cannot discriminate shrink from Hebb ».
   - Nouvelle : « Five of ten Hebbian estimates are below-grid; among the five positive Hebbian denominators, two shrink estimates are also below-grid. The archived code replaces below-grid capacities by zero, giving a zero-coded Hebbian mean of 0.0066 [0.0025, 0.0107] and a five-seed shrink statistic of 0.6 [0.2, 1.0]. These are outputs of that coding convention, not censoring-adjusted estimates. The registered overall label is confirmed; we withhold a full ten-seed interpretation of C3′ and report an additional, post-analysis overall assessment of inconclusive. »
   - Dans la colonne globale, employer « registered: confirmed; post-analysis assessment: inconclusive » avec note, plutôt qu’un seul label. Ne pas masquer la limite du contrôle par une impossibilité absolue de discrimination.

4. **Résumé et documentation m=.30**, `article/metadata.yaml:64`, `README.md:18`, `:124`, `data/README.md:22`, conclusion `article/article.md:340` :
   - Ancienne : « at m = 0.30 the Hebbian capacity sits at the lower limit (…) so that level is reported as inconclusive » / « control not computable at T = 0.2 ».
   - Nouvelle commune : « At m = 0.30, the registered T=0 ratio is 44.38 [42.56, 46.97], with all Hebbian crossings bracketed by loads 0.01–0.02 and a grid-sensitive magnitude. At T=0.2, five Hebbian denominators and two additional shrink numerators are below-grid. We retain the registered results and distinguish them from a post-analysis inconclusive overall assessment due to the unresolved censoring of the control statistic. »
   - Dans le résumé, remplacer aussi « ten seeds per cell » par « ten seed-level realizations per condition ». La nouvelle rédaction sur le caractère partiel, les états parasites opérationnels et la cause non isolée peut être conservée.

5. **Légende corrélée**, `article/article.md:283` :
   - Ancienne : « the m=0.30 ratio curves must not be read as a result; the absolute capacities (…) are the robust reading ».
   - Nouvelle : « The figure shows the registered finite-grid outputs. At m=0.30 the T=0 ratios are defined but grid-sensitive; the T=0.2 ratios exclude five below-grid Hebbian denominators and the shrink series also includes zero-coded below-grid numerators. The automatic labels refer to the registered analysis and do not incorporate the post-analysis censoring reservation stated in the text. »
   - Une figure de publication distincte est possible, mais pas indispensable si cette distinction est clairement lisible. Pour la figure confirmatoire, « Spurious attractors » → « Probes classified as spurious » ou précision équivalente explicite dans la légende.

6. **Conclusion sur les états parasites**, `article/article.md:307` :
   - Ancienne : « leaves no probe classified as spurious at loads 0.14 and 0.20 where the Hebbian network has almost only spurious final states ».
   - Nouvelle : « in the independent-pattern confirmatory run at T=0, dream t=10 leaves 0/320 probes classified as spurious at each of loads 0.14 and 0.20, compared with 51/320 and 318/320, respectively, under Hebb ».
   - Garder la réserve sur l’absence de preuve concernant tout l’espace des états.

7. **Bras f=0**, `article/article.md:311` et `:330` :
   - « for t ≥ 10 » → « at the tested times t∈{10,30,100}, for N∈{64,128,256} ».
   - « (our f=0 arm is censored at the grid maximum, in agreement) » → **supprimer la parenthèse** ; la phrase précédente suffit à distinguer les estimateurs.
   - Ajouter à la méthode après `article.md:110` : « The pilot also includes a descriptive T=0 condition with f=0, i.e. unperturbed stored-pattern cues; this condition is absent from the two N=1000 studies. »

8. **Description de l’original**, `article/article.md:39` et `:199` :
   - « the cue being the first pattern (…) » → « For Fig. 9, initial configurations are random. For Fig. 10, the first stored pattern is independently flipped with probability p, and success means that its Mattis overlap is maximal. »
   - « asynchronous updates instead of the original parallel sign update » → « asynchronous updates at T=0 instead of the parallel sign update used in the original zero-noise field and basin experiments ».

9. **Plage et contexte thermique**, `article/article.md:132`, `:234`, `:322` :
   - « all observed values lie in [0.09, 0.999] » → « across the tested shrink arms, c ranges from approximately 0.0884 to 0.9985 and also depends on the correlation level ».
   - « The Hebbian estimate falls with size » → « At T=0, the Hebbian estimate falls with size ».
   - « lower the mean empirical capacity by 2.52 % » → « give a mean paired relative capacity reduction of 2.52 % » ; conserver l’IC correspondant.

10. **Comparaison de réexécution**, `article/article.md:378` :
    - Ancienne : « a reading of its keys_equal and summary_equal_excl_run_meta fields ».
    - Nouvelle : « inspect keys_equal, cells_differing_non_timing, fields_differing, max_abs_diff and summary_equal_excl_run_meta. Exact reproduction requires matching keys and zero non-timing cell differences; for another numerical platform, inspect any reported differences against the stated tolerance while checking discrete outcomes. The exit status alone is not a validation result. »
    - Ajouter cette instruction aux deux README de reproduction et l’étape gzip au commentaire de `code/run.sh:21`.

11. **Provenance pilote et cohérence de documentation** :
    - `code/run.sh:6`, « commit bc2f838 → run.py (pilot) » → « commit bc2f838 freezes the pilot protocol only; the distributed pilot runner is from df9a1e7 and the pilot is not covered by the internal provenance reruns ».
    - `README.md:22`, « reproduced bit-exactly » → « reproduced on the original host with identical non-timing cell values ».
    - `README.md:112`, « 8 pages » → « 9 pages » ; `:40`, « copied unchanged » → « adapted from the template », en précisant les ajouts réels ; `:81`, « 20 tests » → « 20 test functions, 23 executed cases ».

12. **Présentation PDF** :
    - « longs chemins littéraux non sécables dans les paragraphes et longues réserves dans les cellules du tableau » → « renvois courts vers la documentation de reproductibilité, identifiants/URL sécables et notes de tableau hors colonnes ».
    - Recompiler depuis le Markdown et vérifier visuellement au minimum les pages du tableau corrélé et de la reproductibilité. Un simple décompte d’erreurs LaTeX ne suffit pas. Après correction de `data/README.md`, régénérer son entrée du manifeste.

**Décision finale : révision ciblée avant soumission.** Une fois ces points corrigés, le paquet est défendable comme implémentation indépendante et réplication qualitative partielle, complétée par des expériences originales. Les données disponibles suffisent à cette version sobre de la conclusion ; elles ne justifient ni l’effacement du résultat enregistré à m=.30,T=0, ni l’interprétation des sentinelles comme des capacités mesurées, ni une preuve universelle sur les attracteurs ou les bassins.
