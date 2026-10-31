# Relecture indépendante — soumission ReScience C « NH-01 »

31 octobre 2026. Avis : **révision majeure avant soumission**. Le gain de récupération est bien étayé dans le protocole exécuté ; les principaux nombres sont exacts. L'article doit toutefois corriger une affirmation de stabilité démentie par les données, distinguer résultat publié et nouvel estimateur, rectifier le statut des ratios à forte corrélation, et rendre cohérentes les commandes et les sources de publication.

Périmètre : lecture des fichiers du paquet, du code, des cellules, des pré-enregistrements et du texte original fourni ; vérification ultérieure des notes de résultats et de la provenance amont. **Aucun fichier de `nerve-wml/docs/superpowers/`, aucune revue antérieure et aucun rapport de revue de l'équipe n'ont été consultés pour cet avis.** Je n'ai modifié aucun fichier dans les dépôts examinés. Les exécutions, compilations et téléchargements ont été faits dans `/tmp/nh01-review/`. `rescience-nh01/article/article.md` était déjà modifié à l'ouverture de la revue ; la version examinée a pour SHA-256 `936aa2d19808e7eacf882b395e84e718c2277467b33931e2b054a622d38aa738`, sur le HEAD initial `2addde661cc0c4f5fa5d85eb06449c989e482f65`. HEAD amont initial : `d974dbbd45f132e4370578877db5c17910be1b60`.

Conventions : les chemins préfixés par `rescience-nh01/` ou `nerve-wml/` partent de `repos/`. Les chemins abrégés `article/`, `code/`, `data/`, `prereg/` et `README.md` sont relatifs à `rescience-nh01/`. Les seuls noms `run.py`, `confirmatory.py` et `correlated.py` désignent les fichiers de `rescience-nh01/code/experiments/nh01_hopfield_dream/` ; `run.sh` et `scripts/compare_nh01.py` sont relatifs à `rescience-nh01/code/`. `A:L` désigne `rescience-nh01/article/article.md:L`. `O:L` désigne `../upstream/fachechi2019/1810.12217.txt:L` ; il s'agit de la transcription fournie, dont la mise en page introduit quelques fragments de légendes entrelacés. **BLOQUANT** : empêche l'acceptation en l'état ; **MAJEUR** : affecte l'interprétation ou la vérifiabilité ; **MINEUR** : correction locale ; **OK** : vérifié dans le périmètre indiqué. « Invérifiable » n'équivaut pas à « faux ».

## 1. Conformité ReScience C

Les critères officiels demandent une méthode rigoureuse, un code original et des éléments substantiels montrant la réplication, ou expliquant son échec. Le processus exige aussi que les relecteurs puissent exécuter le code et retrouver les résultats. Les extensions sont compatibles avec cet objectif si le résultat répliqué demeure identifiable. [Critères et portée de ReScience C](https://rescience.github.io/write/), [consignes aux relecteurs](https://resciencec.readthedocs.io/en/latest/reviewer_guidelines.html).

| Évaluation | Constat et localisation |
|---|---|
| **OK** | Résultat publié clairement identifié : noyau de Fachechi–Agliari–Barra, référence complète, DOI exact, modèle et limites analytiques exposés (`A:14`, `A:21`, `article/metadata.yaml:57`, `article/bibliography.bib:1`, chemins ici préfixés par `rescience-nh01/`). |
| **OK, avec limite de vérification** | Implémentation NumPy autonome, sans dépendance au logiciel des auteurs de 2019 : identités matricielles cohérentes, primitives lisibles, tests utiles. La déclaration « no original code reused » (`A:77`) est compatible avec les fichiers ; l'historique disponible ne permet pas de prouver l'absence de consultation ni l'indépendance personnelle vis-à-vis des auteurs originaux. Une courte déclaration de provenance du développement suffirait à clarifier ce point. |
| **MAJEUR** | Le paquet réplique **qualitativement une amélioration de récupération par le noyau**, et étend l'étude. Il ne reproduit ni la courbe théorique de capacité de la Fig. 3, ni les courbes Monte Carlo des Figs. 7–10 avec leur protocole. Les ratios 3,86 et 9,06 sont de nouveaux résultats de NH-01, pas des nombres publiés en 2019. `A:43`, `A:158`, `A:255` doivent présenter une réplication partielle et préciser la correspondance « résultat original → mesure NH-01 → conclusion permise ». Une petite expérience de raccord aux réglages originaux renforcerait beaucoup la soumission ; elle n'est pas nécessaire pour corriger honnêtement son périmètre. |
| **MAJEUR** | La suppression des auto-couplages est déclarée, mais le passage parallèle → asynchrone pour les analyses à bruit nul et l'absence de contrôle d'équilibrage à température finie ne le sont pas comme écarts explicites (`A:86`, `A:158` ; `O:941`, `O:1072`, `O:1099`). |
| **BLOQUANT** | L'affirmation « every stored pattern is a fixed point » (`A:261`) est fausse même pour les motifs sondés : contre-exemple chiffré en §2. Elle doit disparaître avant soumission. |
| **MAJEUR** | Les labels pré-enregistrés C1/C2′/C3′ concernent les hypothèses internes de NH-01. Leur conjonction « confirmed » ne suffit pas à déclarer confirmées toutes les conclusions de Fachechi et al. Le contrôle ajouté et la corrélation ne sont pas des critères de fidélité à l'original (`A:144`, `A:192`, `A:255`). |
| **OK / MAJEUR pour l'accès pratique** | Code et données sont publics, licences explicites ; l'archive Zenodo a effectivement été contrôlée (§5). Mais les instructions de comparaison échouent sans compression manuelle, le manifeste est périmé pour un README, et la compilation ne régénère pas automatiquement le texte LaTeX depuis la source déclarée. |

Les champs éditoriaux après acceptation laissés vides dans `article/metadata.yaml:78` sont normaux pour un brouillon. Le DOI propre au dépôt de soumission peut attendre l'acceptation, comme le prévoit le journal ; son absence actuelle n'invalide pas les données, déjà archivées. La mention « to be created » à `A:294` est périmée : l'API GitHub confirme le dépôt public, créé le 31 octobre à 09:17:32 UTC. [Dépôt de soumission](https://github.com/hypneum-lab/rescience-nh01).

## 2. Code ≠ texte : audit des nombres

### 2.1 Procédure et locateurs JSON

J'ai décompressé les **28 080 + 9 120 + 29 640 = 66 840 cellules**, vérifié l'unicité de leurs clés, reconstruit séparément les capacités à partir des fractions de récupération, puis les moyennes, différences et ratios appariés. Pour chaque intervalle, j'ai utilisé les 10 000 ré-échantillonnages de graines prescrits, RNG 20261025, quantiles 2,5 et 97,5 %. Le recalcul indépendant retrouve **toutes les capacités par graine et tous les triplets `mean_ci`, `ratio_mean_ci`, `diff_mean_ci`** ; les fonctions `analyze()` redonnent aussi tous les résumés et verdicts, hors bloc `run_meta`. Ce contrôle vérifie la transformation données → statistiques ; le nouveau calcul dynamique indépendant du stockage est décrit en §5.

Les triplets JSON sont `[moyenne, borne basse, borne haute]`. Pour alléger les tables, voici les préfixes exacts :

| Abréviation | Fichier et objet JSON |
|---|---|
| `P(N,T,f)` | `rescience-nh01/data/nh01/summary.json` → `conditions["T{T}_f{f}_N{N}"]` |
| `C(T)` | `rescience-nh01/data/nh01_confirmatory/summary.json` → `conditions["T{T}_f0.1_N1000"]` |
| `K(m,T)` | `rescience-nh01/data/nh01_correlated/summary.json` → `levels["{m}"].conditions["T{T}_f0.1_N1000"]` ; la clé forte corrélation est **`"0.3"`**, pas `"0.30"`. |
| `VC` | résumé confirmatoire → `verdict` |
| `VK(m)` | résumé corrélé → `levels["{m}"].verdict` |

Dans chacun de ces objets : `H = hebb.mean_ci`, `D10 = dream["10"].mean_ci`, `R10 = dream["10"].ratio_mean_ci`, `Δ10 = dream["10"].diff_mean_ci`, `S10 = shrink["10"].ratio_mean_ci`. Il s'agit bien de la **moyenne des ratios par graine**, pas du quotient des moyennes.

### 2.2 Pilote et confirmation : valeurs retrouvées

| Passage | Objet et clés ci-dessus | Recalcul, avant arrondi | Évaluation |
|---|---|---|---|
| `A:178–179` | `P(256,0,0.1)` : H | 0,175339899 [0,167469733 ; 0,183198503] | **OK** : 0,175 [0,167 ; 0,183] |
| idem | D10 | 0,598556399 [0,590830998 ; 0,606254762] | **OK** : 0,599 [0,591 ; 0,606] |
| idem | R10 | **3,432320977 [3,260720361 ; 3,602295070]** | **OK** : 3,43 [3,26 ; 3,60] |
| idem | Δ10 | 0,423216500 [0,410671232 ; 0,435218653] | **OK** : 0,423 [0,411 ; 0,435] |
| `A:180–181` | `P(64,0,0.1).dream["10"].ratio_mean_ci` | 3,129967351 [2,735781074 ; 3,571799869] | **OK** : 3,13 [2,74 ; 3,57] |
| idem | `P(128,0,0.1).dream["10"].ratio_mean_ci` | 3,382000938 [3,208552564 ; 3,530049039] | **OK** : 3,38 [3,21 ; 3,53] |
| `A:188` | `C(0)` : H | 0,157358059 [0,154799904 ; 0,159931868] | **OK** |
| idem | D10 | 0,606996095 [0,604222078 ; 0,610081232] | **OK** |
| idem | R10 | **3,860505375 [3,786967243 ; 3,933004022]** | **OK** : 3,86 [3,79 ; 3,93] |
| idem | Δ10 | 0,449638037 [0,445113909 ; 0,454353957] | **OK** : 0,450 [0,445 ; 0,454] |
| `A:190` | `C(0.2)` : H | 0,126487932 [0,124979615 ; 0,127816488] | **OK** |
| idem | `shrink["10"].mean_ci` | 0,123300569 [0,121457864 ; 0,125038170] | **OK** |
| idem | S10 | **0,974772542 [0,966510297 ; 0,982010865]** | **OK** : 0,975 [0,967 ; 0,982] |
| `A:194` | `C(0.2).dream["10"].ratio_mean_ci` | 3,578997707 [3,526696490 ; 3,636296619] | **OK** : 3,58 [3,53 ; 3,64] |
| `A:195` | `C(0.2).dream["7"].ratio_mean_ci` | 3,618321313 [3,554583773 ; 3,677340972] | **OK** : 3,62 [3,55 ; 3,68] |

`A:196` : la série Hebb 0,211 / 0,179 / 0,175 / 0,157 correspond à `P(64,0,0.1).hebb.mean_ci[0]`, `P(128,0,0.1)...`, `P(256,0,0.1)...`, `C(0).hebb.mean_ci[0]`. À t = 10, les capacités dreamed correspondantes sont 0,631625 / 0,602310 / 0,598556 / 0,606996. **OK pour les nombres**, mais « towards 0.138 » est une tendance descriptive sur quatre tailles, pas une extrapolation validée.

`A:189` : `VC.C2_unimodal.median_alpha_c_by_t` donne, dans l'ordre t = 0, 1, 3, 5, 7, 10, 15, 20, 30, 100 : **0,157564 / 0,412701 / 0,570754 / 0,603348 / 0,616442 / 0,606111 / 0,595089 / 0,581579 / 0,569211 / 0,526932**. Les dix arrondis de l'article sont exacts. `t_star = 7` ; `per_seed_t_star = [10,7,7,7,7,7,7,7,7,7]`. `drop_star_to_end_mean_ci = [0.087581354, 0.082295269, 0.092282907]`, soit **0,088 [0,082 ; 0,092]**. **OK**, avec « optimum sur la grille » à préciser.

`A:191` : `C(0).spurious["0.14"]` donne Hebb **0,159375** → dream **0** ; `spurious["0.2"]` donne **0,99375** → **0**. Les valeurs 0,159 et 0,994 et la réduction relative de 100 % sont exactes ; le label P4 suit les seuils enregistrés. Elles portent sur les états atteints par les sondes, pas sur le dénombrement des attracteurs.

### 2.3 Corrélations : nombres exacts et statut des estimations

Toutes les lignes suivantes concernent t = 10. Les préfixes `K` et les clés H/D10/R10/Δ10/S10 sont définis en §2.1.

| Objet / passage | H | D10 | R10 | Δ10 | S10 |
|---|---|---|---|---|---|
| `K(0,0)`, `A:209` | 0,159800 [0,158060 ; 0,161604] | 0,610809 [0,605794 ; 0,615761] | **3,823674 [3,767431 ; 3,876689]** | 0,451009 [0,445388 ; 0,456288] | 1 [1 ; 1] |
| `K(0.15,0)`, `A:210` | 0,068105 [0,066347 ; 0,069634] | 0,615720 [0,611649 ; 0,619487] | **9,055164 [8,839494 ; 9,293185]** | 0,547615 [0,543309 ; 0,551549] | 1 [1 ; 1] |
| `K(0.3,0)`, `A:211` | 0,014401 [0,013694 ; 0,014912] | 0,635534 [0,632781 ; 0,638823] | **44,384759 [42,557542 ; 46,973281]** | 0,621133 [0,618118 ; 0,624531] | 1 [1 ; 1] |
| `K(0,0.2)`, `A:209` | 0,127262 [0,125419 ; 0,128618] | 0,452771 [0,447244 ; 0,457761] | 3,559149 [3,501431 ; 3,617168] | 0,325509 [0,320018 ; 0,330557] | **0,978993 [0,973842 ; 0,984215]** |
| `K(0.15,0.2)`, `A:210` | 0,054452 [0,052805 ; 0,056090] | 0,455653 [0,451523 ; 0,459447] | 8,388369 [8,137272 ; 8,665960] | 0,401201 [0,397065 ; 0,405564] | **0,985781 [0,978747 ; 0,992716]** |
| `K(0.3,0.2)`, `A:211` | 0,006613 [0,002542 ; 0,010690] (*) | 0,463170 [0,458023 ; 0,467597] | 35,446983 [32,842713 ; 38,158623] (**) | 0,456557 [0,451517 ; 0,462041] (*) | **0,6 [0,2 ; 1]** (**) |

**OK pour tous les arrondis effectivement cités** à `A:209–218`. Les capacités et ratios non cités dans l'article figurent ici pour auditer le traitement des dénominateurs.

(*) À T = 0,2, les cinq capacités Hebb hors grille sont remplacées par le **code sentinelle 0**. La moyenne 0,006613 et son intervalle concernent cette convention ; ce n'est pas une mesure établissant une capacité physique nulle sur cinq graines. Avec une interprétation en censure [0 ; 0,01), la moyenne des dix valeurs serait comprise entre 0,006613 et 0,011613, avant incertitude d'échantillonnage.

(**) Moyenne et bootstrap sur **cinq graines définies seulement**. `K(0.3,0.2).shrink["10"].ratio_per_seed` vaut `[1, NaN, NaN, 0, 1, 1, NaN, 0, NaN, NaN]`, dans l'ordre 100–109. La sous-liste `[1,0,1,1,0]` donnée dans l'article est exacte. La fonction filtre les NaN (`code/experiments/nh01_hopfield_dream/run.py:360`, `:424`). Ces résumés conditionnels ne sont pas un ratio populationnel sur les dix graines.

**MAJEUR — « non calculable » à T = 0 est impropre.** Les dix `K(0.3,0).hebb.flags` valent `"ok"`, les dix dénominateurs sont strictement positifs, entre 0,011667 et 0,015263, et les croisements sont encadrés par les charges 0,01 et 0,02. Le ratio 44,384759 est donc calculable **selon l'estimateur pré-enregistré**, et C1 satisfait sa règle. Il reste très sensible à la résolution de grille. Il faut écrire « calculable, mais amplitude mal résolue sur la grille », ou « non retenu pour l'interprétation quantitative », sans confondre avec les divisions réellement indéfinies à T = 0,2 (`A:211–225`, `article/metadata.yaml:64`, `README.md:18`). Le verdict global prudent « inconclusive » est défendable en raison du contrôle à T = 0,2, mais constitue une restriction après résultats, explicitement déclarée par l'article.

`A:209–211` : les objets `VK(m).C2_unimodal` confirment t* = **7, 7, 10**, plages des t* individuels **5–10, 7–10, 7–10** et baisses vers t = 100 **0,083876955 [0,078661857 ; 0,089144631]**, **0,087621715 [0,085496272 ; 0,089728276]**, **0,102528383 [0,098189394 ; 0,107561261]**. **OK**.

`A:228` : `data/nh01_correlated/summary.json → C4_trend.diff_high_minus_zero_mean_ci` vaut **[40.561085594, 38.723314759, 43.164038644]** ; le label est `gain_increases`. **OK pour 40,6 [38,7 ; 43,2]**, mais le texte ne peut à la fois annoncer un ratio mathématiquement non calculable et en présenter la différence C4 comme résultat. La direction peut être discutée avec prudence : même un encadrement grossier des dénominateurs dans [0,01 ; 0,02] laisse ici un contraste très supérieur au ratio ≈ 3,8 à m = 0. Cela ne valide pas la précision décimale de 44,4 ou 40,6.

`A:230–234` : `VK(m).P4_spurious` et `K(m,0).spurious` confirment 0 état classé spurious sous dream t = 10 aux deux charges, à chaque niveau ; `exact_one_at_T0 = true` partout. Les comparaisons 3,82 vs 3,86 et 0,979 vs 0,975 sont exactes. **OK**.

### 2.4 Autres nombres et écarts établis

| Passage | Vérification et verdict |
|---|---|
| `A:77–84` | Les runners font bien 713, 384 et 237 lignes. Les tests ont **20 fonctions et 23 cas exécutés**, du fait d'une paramétrisation ; 23 passent. « Ten + ten » peut compter les fonctions, mais doit être précisé. Le test du projecteur utilise **t = 10⁸**, pas 10⁶ (`code/tests/test_nh01_hopfield_dream.py:53–57`). Chemin local des tests : `code/tests/`, et non `tests/unit/`. **MINEUR**. |
| `A:89–110` | Tolérance 10⁻¹² N max\|J\|, 100 balayages à T = 0, 40 dont 10 moyennés à T = 0,2, β = 5, 32 sondes maximum, seuils 0,9 / 0,8, 24 / 26 charges et bootstrap 10 000 sont conformes au code (`run.py:36–59`, `:157–224`, `:301`, `:343`, `correlated.py:43`). **OK**. À N = 64/128/256, l'arrondi des bits donne un overlap de **0,8125 / 0,796875 / 0,796875**, pas exactement 0,80 ; à N = 1000, il vaut bien 0,80 (`cells.jsonl.gz`, clé `cue_overlap`). **MINEUR**. |
| `A:125–128` | m = 0 / 0,15 / 0,30 et q = m² = 0 / 0,0225 / 0,09, graines 100–109 : conformes au générateur et au pré-enregistrement (`run.py:131`, `correlated.py:40`). **OK**. Notation m réutilisée pour le paramètre de l'ancêtre et l'overlap de récupération : confusion à lever. |
| `A:179–180`, `A:190`, `A:232` | Contrôle à T = 0 : égalité exacte des fractions retrieved, other_stored, spurious, overlaps, balayages et convergences entre chaque cellule shrink et sa cellule Hebb ; tous les ratios définis valent exactement 1, tous N et t. **OK**, plus fort que le seul `np.isclose` du verdict. |
| `A:93` | Aucune cellule à T = 0 n'a de sonde non convergée ; maximum 36 / 72 / 80 balayages, pilote / confirmatoire / corrélé. **OK**. À T = 0,2, `nonconverged_frac = 0` est assigné par le code et ne mesure pas l'équilibrage (`run.py:327`). |
| **`A:261–262`** | **BLOQUANT : « every stored pattern is a fixed point up to α = 0.95 for t ≥ 10 » est démenti.** Parmi les cellules dream, f = 0, T = 0, t ≥ 10 du pilote, **17** ont une fraction retrieved < 1, toutes à t = 10 ; minimum **0,9375**. Exemple : `data/nh01/cells.jsonl.gz`, **ligne décompressée 22446**, clé `(N=256,seed=3,alpha=0.95,arm=dream,t=10,temp=0,flips=0)` : retrieved = **31/32**, spurious = **1/32**, overlap moyen = **0,98486328125**. De plus, ≥ 0,9 n'est pas l'égalité exacte à un motif et seules 32 sondes sont testées, pas tous les P motifs. Le résultat vrai est que l'**estimateur à seuil 50 %** de cette condition est censuré à 0,95 pour ces t et ces tailles (`P(N,0,0).dream[t].flags`). |
| `A:268–269`, `README.md:20` | 1 − 0,974772542 = **2,5227458 %**, IC par transformation **[1,7989135 % ; 3,3489703 %]**. « 2.5 per cent » et « 2–3 % » sont des arrondis descriptifs acceptables de la moyenne. « as a heating must » ne découle pas du théorème pour cet estimateur fini (§4). |
| `A:245–251` | Les comparaisons archivées déclarent 9 120/9 120 et 29 640/29 640 cellules égales hors temps ; résumés égaux hors `run_meta`, images égales en octets. Les deux SHA cités sont exacts. Les cellules brutes des re-runs ne sont **pas fournies** dans le paquet : le décompte complet est donc une attestation interne, non revalidée cellule par cellule ici (§5). |
| `A:302–315` | Python 3.12.15 et NumPy 2.5.4 : `run_meta.json`; Matplotlib 3.11.2 : freeze et métadonnées PNG. Temps originaux 1547,3 / 6951,4 / 22866,4 s, re-runs 15135,8 / 30547,4 s : conformes aux `run_meta`. Effectifs et graines conformes aux cellules. Hôte et matériel : informations déclarées dans les métadonnées, pas matériel inspecté par ce relecteur. L'expression « 8 × Xeon X5680 » gagnerait à distinguer processeurs physiques et huit CPU logiques visibles. |

## 3. Fidélité au texte de Fachechi–Agliari–Barra

La comparaison suivante couvre les affirmations attribuées à l'original dans l'introduction, la description du modèle et la conclusion. Elle porte sur le texte intégral fourni, sans substituer les notes de l'équipe à la source.

| Affirmation de NH-01 | Texte original, lignes | Évaluation |
|---|---|---|
| Hebb J = ξᵀξ/N, motifs binaires i.i.d., P = αN (`A:18`, `A:65`) | `O:108–116`, `O:411–431` | **OK**. |
| Noyau `(1+t)(I+tC)⁻¹` en espace des motifs (`A:67`) | Hamiltonien (2.1), `O:414–431` | **OK**. La forme neuronale `J(1+t)(I+tJ)⁻¹` et sa transformation spectrale sont une réécriture algébrique correcte ; l'identité est testée indépendamment en espace des motifs. |
| Hebb à t = 0, pseudo-inverse à l'infini (`A:23`) | `O:433–435`, renvoi à l'appendice B | **OK**. Pour l'inverse ordinaire de C, il faut l'indépendance linéaire des motifs ; la formulation en projecteur reste valable avec pseudo-inverse appropriée. |
| Valeur 0,138 et croissance vers 1 (`A:25–29`) | `O:800–809`, `O:1753–1757` | **OK** comme présentation physique, sous réserve de préciser l'approximation RS : le calcul RS tend à 1,07, et non exactement 1. La phrase ajoutée à `A:37–40` le fait correctement. |
| Capacité RS ≈ 1,07, excès attribué à la brisure de symétrie des répliques (`A:37–40`) | `O:802–807` ; également `O:854–857` | **OK** : c'est bien l'explication des auteurs. Ne pas présenter 1,07 comme une capacité physique démontrée au-delà de la borne 1. |
| Suppression des mélanges, renforcement des motifs purs, résistance au bruit (`A:28–29`) | `O:436–438`, `O:932–935`, `O:1754–1760` | **OK** pour les conclusions de l'original ; la portée de leur vérification par NH-01 est plus limitée (§4). |
| Monte Carlo single-spin-flip Glauber, mesures après équilibre (`A:30`) | `O:924–941` | **OK pour §2.5.1 / Figs. 7–8 seulement**. Le contrôle d'équilibre y est explicite. Généraliser cette description à toutes les simulations est trompeur : les Figs. 9–10 utilisent la règle parallèle (2.17). |
| Fig. 7 : N = 5000, M = 10, α = 0,02 / 0,08 / 0,32, t = 0 / 0,1 / 1 / 10 / 100 / 1000 (`A:31–33`) | `O:960–969` | **OK**, tous les paramètres concordent. La légende précise aussi T de 0 à 1,2. |
| Fig. 8 : N = 500 / 1000 / 5000 (`A:34`) | `O:990–1000` | **OK** ; α = 0,08 et M = 10, détails absents de NH-01 mais non contredits. |
| Figs. 9–10 : N = 1000, P = 50 (`A:35–36`) | `O:1011–1012`, `O:1099` | **OK**. |
| Fig. 9, nombre de réalisations | `O:1055–1062` | **20 évolutions et 20 réalisations**. NH-01 ne donne pas ce nombre ; ajouter ce détail évitera d'étendre par erreur les 200 × 200 aux deux figures. |
| Fig. 10 : 200 évolutions pour chacune de 200 réalisations (`A:36–37`) | `O:1162–1164` | **OK** ; temps t = 0 / 0,1 / 1 / 1000. |
| Bruit du signal et règle de succès pour les bassins | `O:1099–1105` | L'original retourne chaque bit **avec probabilité p** et reconnaît ξ¹ lorsque m₁ est le Mattis overlap maximal. NH-01 retourne **exactement round(0,1N) bits** et impose un seuil absolu 0,9 / 0,8. **MAJEUR : écarts à ajouter à `A:158`**. |
| Dynamique à bruit nul des champs et bassins | `O:1065–1077`, renvoi de `O:1102` à (2.17) | Le texte écrit explicitement **parallel update** et inclut j = 1…N dans le champ. NH-01 est asynchrone et supprime Jii. **MAJEUR : différence réelle, pas un détail de vitesse**. La formule du Hamiltonien inclut la diagonale, mais celle-ci est constante en énergie pour les spins binaires : sa suppression ne change pas les poids de Gibbs, tandis que son inclusion naïve dans une règle de champ change la dynamique. |
| Pas de courbe de capacité mesurée par Monte Carlo (`A:40–41`) | Capacité calculée par équations théoriques : `O:800–809`, `O:816` ; simulations : `O:916–940`, `O:1052`, `O:1162` | **OK dans §2.5** : les figures Monte Carlo portent sur aimantation/température, champs et fréquences de récupération. Cela n'enlève pas le fait que l'original vérifie numériquement des prédictions de la théorie. |
| L'étude originale est sur motifs indépendants, les corrélations sont ajoutées (`A:58–59`) | `O:115–116`, `O:422–431` | **OK pour le modèle et les expériences de réplication visés**. L'original cite aussi des travaux sur les corrélations ; ne pas étendre la phrase à toute la littérature qu'il discute. |
| La théorie de capacité ne concernerait que « stability of the stored patterns » (`A:274`) | Transition retrieval / spin glass et discussion des régions : `O:795–809`, `O:916–940` | **MAJEUR** : « only stability » est réducteur. La théorie caractérise une phase de récupération et ses overlaps à l'équilibre, distincte du seuil empirique de succès à partir de cues bruités. Une expérience f = 0 censurée ne valide pas à elle seule cette phase théorique. |
| Bassins plus petits à grand t, phénomène « que l'analyse originale ne quantifie pas » (`A:276–277`) | Section **2.5.3**, `O:1085`, `O:1099–1108`, Fig. 10 `O:1162–1164` | **MAJEUR** : l'original quantifie bien des bassins, à faible charge α = 0,05, et rapporte leur stabilisation avec t. NH-01 ne mesure pas une courbe en bruit du signal à charge fixée ; son optimum de capacité ne suffit pas à établir une réduction générale des bassins. On peut dire que le **régime NH-01**, à charges plus élevées et avec d'autres mises à jour, n'est pas couvert par cette figure. |

Les références historiques de `article/bibliography.bib` ne présentent pas d'erreur bibliographique évidente. La valeur AGS est correctement attribuée ; sa citation explicite manque toutefois dans le corps généré (§6).

## 4. Méthode, nuls et pré-enregistrement

### 4.1 Le contrôle shrink est utile, mais sa portée doit être exacte

**OK — théorème à T = 0.** Pour tout c > 0, le signe du champ c·h est celui de h. La tolérance proportionnelle à max\|J\| préserve aussi les égalités à zéro dans la précision considérée. Avec les mêmes cues et permutations, les trajectoires doivent coïncider. Le contrôle mesure ici une identité d'implémentation, pas une hypothèse empirique incertaine sur le sommeil. Une réfutation par ratio ≥ 2 à T = 0 ne pourrait signaler qu'une implémentation ou une comparaison incorrecte (`run.py:157–192`, pré-enregistrement pilote `:24–29`, `:68–78`). Le travail en est conscient ; il faut conserver cette distinction dans la conclusion.

**MAJEUR — à T > 0, seule l'identité de température est un théorème général ici.** L'égalité des probabilités de transition sous `(cJ,β)` et `(J,cβ)` est correcte, soit T effectif = T/c. En revanche, elle n'implique pas une inégalité déterministe `S ≤ 1` pour une capacité interpolée après 40 balayages, avec une seule réalisation des tirages thermiques et un seuil d'overlap. Le régime d'équilibre théorique d'AGS n'est pas cet estimateur fini. Le propre pilote donne un contre-exemple à l'inégalité graine par graine :

`data/nh01/summary.json → conditions.T0.2_f0.1_N256`, graine **6** : `hebb.alpha_c_per_seed[6] = 0.140000000`, `shrink["10"].alpha_c_per_seed[6] = 0.141666667`, donc **S = 1,011904762 > 1**. Cela n'invalide ni l'identité de température ni la baisse moyenne observée ; cela invalide la formulation d'un « must » universel pour cette mesure (`A:120`, `A:223`, `A:269`).

**Peut-il échouer ?** À T = 0, seulement comme contrôle de l'implémentation, sous ses hypothèses. À T = 0,2, **oui, le critère statistique peut ne pas être satisfait** : fluctuation des trajectoires, effet de durée de relaxation, variance des dix graines, c proche de 1, censure du dénominateur, ou éventuelle amélioration de l'accès à un bassin par le bruit. L'identité de température, à elle seule, n'interdit pas ces situations dans le protocole fini. Le seuil de réfutation ≥ 2 porte sur un très gros effet ; il ne constitue pas un test d'équivalence fine entre shrink et Hebb.

**OK — appariement.** Le code utilise les mêmes motifs et cues pour toutes les branches ; il réinitialise le générateur de dynamique par cellule (`run.py:275–306`). Les permutations sont partagées jusqu'à l'arrêt de chaque trajectoire et les tirages thermiques sont communs à durée égale. c dépend en réalité de **t, α, N et de la graine**, et non de t seul ; le contrôle a donc un T effectif différent à chaque charge. Cela mérite une phrase.

**MAJEUR — portée du résultat.** La norme de Frobenius égalise une grandeur globale bien définie ; elle n'égalise ni le spectre, ni les marges de stabilité, ni tous les champs locaux. L'échec de **ce** rescaling apparié est convaincant. À température finie, on n'a pas balayé tous les facteurs c possibles : « no uniform rescaling ... reproduces the gain » (`A:267`) doit rester limité aux facteurs appariés testés. À température nulle, l'absence d'effet de tout c > 0 est au contraire générale. La distinction mathématique entre une transformation spectrale et une simple échelle est déjà claire sans attribuer au contrôle une réfutabilité qu'il n'a pas.

Dans les données exécutées, tous les c sont bien < 1 : plages **[0,244550 ; 0,998460]**, **[0,261811 ; 0,980975]**, **[0,088445 ; 0,996539]** pour pilote, confirmatoire et corrélé, d'après les clés `c_fro` des cellules shrink. Le ratio de normes, tel qu'écrit dans le code, n'impose pas par une instruction un plafond 1 ; si « by construction » est revendiqué comme propriété mathématique du générateur de noyaux, il faut l'établir, ou simplement rapporter l'observation.

### 4.2 Que mesure la capacité ?

**OK / MAJEUR pour la présentation.** L'estimateur est déterministe et conforme au protocole, mais la phrase de `A:101–105` est insuffisante : le code choisit **le dernier point de grille avec r ≥ 0,5**, puis son croisement suivant. Il ne choisit pas le premier croisement et ne fait pas de régression monotone (`run.py:343–353`). J'ai trouvé **22 courbes du pilote** présentant une descente sous 0,5 suivie d'un retour au-dessus ; aucune dans les deux séries N = 1000. Le choix du dernier croisement peut favoriser les rebonds de bruit à petite taille. Ici, aucun cas ne commence sous 0,5 puis réussit plus loin : l'ambiguïté de la phrase « below_grid when ... at the lowest load » n'a donc pas modifié les résultats, mais elle ne décrit pas la règle générale du code. Le pré-enregistrement corrélé précise correctement « no load with r ≥ 0.5 » (`prereg/2026-10-27-nh01-correlated-patterns.md:35`).

Le nombre de motifs est arrondi, `P = round(αN)`, tandis que l'interpolation utilise α nominal. À N = 1000, les charges sont réalisées exactement ; à petite taille, α et P/N diffèrent légèrement. À corrélation forte et très faible charge, le nombre de sondes est **10 puis 20**, et non 32. La grille et les sondes bornées limitent la résolution ; le bootstrap ne corrige pas ce biais de discrétisation. Une sensibilité à une grille affinée, à un premier croisement ou à une courbe monotone serait informative si l'amplitude précise du ratio devient un argument central. Le protocole gelé doit rester le résultat principal.

Le seuil de succès n'est pas identique entre T = 0 et T = 0,2 (0,9 contre 0,8). Cela autorise une comparaison dream/Hebb **à température fixée**, mais interdit d'interpréter directement l'écart des capacités entre températures comme une mesure pure de l'effet thermique. Quarante balayages et la moyenne des dix derniers sont une durée fixée, **sans diagnostic d'équilibre**, contrairement à `O:941`. Un avantage à T = 0,2 est établi dans cette fenêtre, pas sur toute la phase thermodynamique.

### 4.3 Dix graines, bootstrap, sélection du maximum et nuls

**OK** : la graine est la bonne unité de ré-échantillonnage ; considérer les 32 sondes ou les milliers de cellules comme autant de répétitions indépendantes serait de la pseudoréplication. Les motifs imbriqués et les bras partagent des tirages, ce qui renforce l'intérêt de l'appariement. Les niveaux corrélés sont également appariés par graine et par identifiants de flux (`correlated.py:85–105`).

**MAJEUR, sans annuler le résultat central** : dix grappes indépendantes restent peu nombreuses pour calibrer les queues d'un intervalle percentile à 95 %. Dix mille tirages bootstrap n'ajoutent aucune graine. La puissance n'est pas un nombre qu'on peut déduire du seul n = 10 : elle dépend de l'effet et de la variance prévus ; aucune analyse de puissance prospective n'est fournie. Ici l'effet est assez éloigné du seuil pour que la conclusion descriptive soit solide : R confirmatoire a un écart-type inter-graines **0,124877** autour de **3,860505** ; les moyennes en retirant une graine restent entre **3,842941 et 3,879896**. Les moyennes analogues du shrink restent entre **0,973247 et 0,977525**. Ce diagnostic de sensibilité, calculé pendant la revue, n'est pas une garantie de couverture nominale.

t* = 7 est **l'argmax de la médiane sur dix valeurs de t**, pas un optimum continu identifié à l'unité près. La baisse vers t = 100 est nette, mais son IC est calculé après sélection de t* sur les mêmes données (`confirmatory.py:101–118`), sans correction de sélection. À titre descriptif, ré-échantillonner les dix graines et recalculer l'argmax des médianes donne t* = 7 dans **9923/10000** tirages, 10 dans 69 et 5 dans 8 ; cela soutient le maximum de grille et ne fournit pas un intervalle pour un optimum continu. Les IC sont ponctuels : ils ne sont pas des bandes simultanées sur tous les t, tailles et niveaux.

**MAJEUR — « spurious » est une classe opérationnelle.** `run.py:241–254` appelle spurious tout échec au motif ciblé qui n'est pas assez proche d'un autre motif. Cela inclut des récupérations imparfaites et, en principe, l'anti-motif ciblé, dont l'overlap absolu est effacé lors de la recherche d'un autre motif. À T = 0,2, la classification porte sur les overlaps moyens dans une fenêtre, pas nécessairement sur un état final fixe. Les fichiers agrégés ne permettent pas de recompter séparément les mélanges, les anti-motifs et les autres échecs. Une réduction à zéro dans 320 sondes, avec dix jeux de motifs partagés, n'établit donc pas la disparition des attracteurs spurious du paysage. Le bootstrap d'une série entièrement nulle donne mécaniquement [0 ; 0] ; ce n'est pas une borne universelle de fréquence. À α = 0,8, t = 10, graine 0, le confirmatoire a même `spurious_frac = 1` (`data/nh01_confirmatory/cells.jsonl.gz`, ligne décompressée **2594**), ce qui montre pourquoi la charge doit accompagner l'affirmation.

**MAJEUR — nuls et données hors grille.** À m = 0,30, T = 0,2, l'absence d'une mesure Hebb résolue rend le contrôle peu informatif. L'article a raison de refuser une conclusion générale depuis les cinq ratios restants. La justification appropriée est la **censure et la sélection du sous-échantillon**, pas un théorème `S ≤ 1`. À T = 0, en revanche, aucun dénominateur n'est nul : ne pas convertir une réserve de résolution en impossibilité de calcul (§2.3). La prudence doit s'appliquer également aux moyennes absolues contenant des zéros sentinelles.

### 4.4 Pré-enregistrement : ce qui est attesté, ce qui ne l'est pas

**OK** : les trois copies `prereg/2026-*.md` sont identiques octet pour octet aux fichiers `docs/milestones/` dans leurs tags respectifs. Les SHA-256 annoncés dans les annotations sont corrects : pilote **b1ccbb63736178d5…**, confirmatoire **6c29566bbcc5b31b…**, corrélé **be9ef311f33ab771…**. Constantes, graines, températures, charges, seuils, effectifs et budgets de temps des runs complets correspondent aux protocoles. Aucun dépassement de budget ni exclusion de graine n'est observé dans ces données.

| Étude | Date UTC de l'objet tag local | Début déclaré du run | Portée de la preuve |
|---|---|---|---|
| pilote, `bc2f838` | 25/10 **08:40:27** | 25/10 **08:51:11** | Protocole dans le tag ; **aucun code NH-01 dans ce tag**. |
| confirmatoire, `a000f73` | 25/10 **13:47:06** | 25/10 **13:47:22** | Protocole et code présents. La note amont annonce un push à 13:47:08. |
| corrélé, `df9a1e7` | 27/10 **16:48:01** | 27/10 **16:48:06** | Protocole et code présents. La note amont annonce push et lancement à la même seconde 16:48:06, en ordre séquentiel. |

Sources : `git show --no-patch --format=fuller <tag>` ; `data/nh01/run_meta.json:134`, `data/nh01_confirmatory/run_meta.json:53`, `data/nh01_correlated/run_meta.json:12` ; `nerve-wml/docs/results/2026-10-25-nh01-confirmatory.md:3–4`, `.../2026-10-27-nh01-correlated.md:3–4`.

**Invérifiable indépendamment : l'heure du push public initial et l'absence de lecture des résultats avant gel.** Les dates Git sont déclaratives et les heures des runs proviennent des journaux des auteurs. Les références SWH résolvent bien aujourd'hui, mais le snapshot annoncé du 29 octobre est postérieur aux runs initiaux : il ne prouve pas à lui seul la publication préalable du 25/27. Les fichiers `launch.txt` des re-runs attestent une consultation du tag GitHub avant ces **re-runs du 30**, pas avant les runs initiaux. Les objets Git, les notes et les métadonnées sont cohérents ; je n'ai pas trouvé de preuve contraire. Pour étayer les « 14 s after the tag push », fournir l'événement public ou un journal contemporain horodaté qui contient le push.

**MAJEUR — distinguer trois étapes successives.** Le confirmatoire est explicitement un amendement **informé par le pilote** : C2 monotone devient C2′ unimodal, C3 passe de T = 0 à T = 0,2, P4 change ses charges (`prereg/2026-10-25-nh01-confirmatory-n1000.md:4–23`). Le corrélé est informé par les deux premiers. Ce séquençage est déclaré et recevable ; « all rules fixed before any run » et la liste unique de critères à `A:144` masquent néanmoins l'évolution. Le pilote portait P4 sur **0,10 et 0,14**, non 0,14 et 0,20, et C2 sur une monotonie tolérée à **0,05**. Sa médiane descend de 0,600 à 0,559 puis 0,522 ; il passe seulement parce qu'aucune baisse adjacente ne dépasse 0,05. Il ne démontre pas une monotonie stricte.

**MAJEUR — amendement d'interprétation après résultats.** Le retrait du label « confirmé » à m = 0,30 et la règle de non-publication de son ratio T = 0 ne figuraient pas dans les critères gelés. L'article le reconnaît (`A:220–226`) : conserver séparément **verdict enregistré**, **réserve méthodologique après analyse**, **conclusion retenue**. Ne pas réécrire rétrospectivement C1 comme si les dix croisements à T = 0 avaient été hors grille.

**MINEUR — écart opérationnel sans effet sur les critères principaux ici** : le pré-enregistrement pilote décrit `other_stored` avec un seuil absolu 0,9 (`prereg/2026-10-25-nh01-hopfield-dream-vs-downscale.md:51`), tandis que `classify()` reçoit aussi le seuil 0,8 pour les autres motifs à T = 0,2 (`run.py:241–254`, `:326`). Les critères principaux de capacité utilisent la récupération du motif ciblé, et P4 est évalué à T = 0 : cet écart ne change donc pas leurs verdicts. Il doit être déclaré pour les statistiques descriptives de classification à température finie.

**MINEUR — garde-fous à renforcer pour de futures exécutions** : le verdict confirmatoire vérifie l'invariance shrink à T = 0 au seul t principal et par `np.isclose` (`confirmatory.py:128–129`), alors que l'engagement porte sur toute cellule. Les runners arrêtés au budget de temps ne forcent pas systématiquement un verdict non concluant avant analyse et ne valident pas explicitement la complétude des grilles (`confirmatory.py:349–375`, `correlated.py:211–227`). Les présents fichiers sont complets et mon contrôle externe trouve l'égalité exacte pour tous les t ; ces limites du programme n'ont donc pas contaminé les résultats audités.

**MINEUR / transparence** : le pilote a eu un lancement interrompu pour BLAS ; le journal existe en amont mais manque au paquet (`A:169–171`). Il contient dix lignes de progression jusqu'à 142,3 s (`nerve-wml/results/nh01/run-aborted-blas-threads.log:1–10`). Cela est compatible avec des cellules calculées en mémoire puis abandonnées ; ce journal ne prouve pas qu'aucun résultat n'a été lu. Les sondes de chronométrage 999 et 998 sont annoncées dans les deux protocoles ; écrire « avant le run principal », plutôt que « avant toute cellule », est exact.

## 5. Reproductibilité, hachages et archive

### 5.1 Vérifications exécutées par ce relecteur

- Installation réussie des trois versions de `code/requirements.txt` dans un environnement isolé : **NumPy 2.5.4, Matplotlib 3.11.2, pytest 9.1.1**. Python local **3.12.13**, macOS ARM64 ; le producteur utilisait Python 3.12.15, Linux x86-64. **23 cas de test réussis** en environ deux secondes. Une vérification préalable avec Python 3.14.8 / NumPy 2.4.3 avait aussi réussi.
- Analyse de l'intégralité des **66 840 cellules**, sans doublon, et reconstruction indépendante de toutes les statistiques de capacité (§2).
- Nouveau calcul **complet d'une tâche confirmatoire**, N = 1000, graine 0, toutes les 24 charges, 19 bras, deux températures : **912 cellules**, en **186,84 s**, depuis une copie inchangée du code. Clés identiques et égalité exacte des champs de récupération, overlaps moyens, classifications, convergence, balayages et `energy_hebb`. Hors temps, seules `c_fro` (**864 cellules**, écart maximal **6,958 × 10⁻¹³**) et `energy_own` (**816**, maximal **3,507 × 10⁻¹³**) diffèrent. C'est une reproduction numérique très convaincante à cette taille, avec les différences attendues entre bibliothèques de calcul ; ce n'est pas une reproduction bit à bit de tous les champs.
- Exécution du mode pilote `--smoke` sur une copie, qui produit bien un jeu de cellules et les métadonnées ; elle sert aussi à constater le problème du comparateur ci-dessous.
- Régénération des trois figures depuis les cellules, avec les versions épinglées. Confirmatoire et corrélé : **pixels RGBA exactement identiques**, mais **octets PNG différents**. Le pilote diffère sur seulement **21 pixels** sur 1 580 150. Les fichiers de figures inclus dans l'article sont bien identiques à leurs équivalents `data/*/figure.png`.
- Compilation sur une copie de l'article, après régénération du texte, avec XeLaTeX + Biber : **8 pages, bibliographie rendue**, avec débordements typographiques (§6). Biber universel échouait d'abord lors de son extraction ARM64 locale ; exécuter sa copie ARM64 a résolu ce problème d'environnement. Ce n'était pas une erreur du manuscrit.

**Limite explicite** : je n'ai pas recalculé les trois grilles dynamiques complètes, ni les 38 760 cellules des deux re-runs internes. Les totaux « bit-exact » de ces re-runs restent documentés par leurs rapports de comparaison ; ils ne constituent pas une seconde vérification indépendante de tous les runs. Une acceptation finale selon la procédure du journal devra compléter les exécutions jugées nécessaires par les relecteurs.

### 5.2 `CODE_SHA256_AT_TAG.txt` et code amont

**OK** : les quatre entrées de `code/CODE_SHA256_AT_TAG.txt:1–4` égalent les fichiers locaux et les blobs obtenus par `git show prereg-nh01-correlated-20261027:<chemin>` :

| Fichier dans `code/experiments/nh01_hopfield_dream/` | SHA-256 intégral |
|---|---|
| `__init__.py` | `46be9bd5ac12b13fbd1b02fb46b8ee078e259738e44696208ea311ec3a813e6b` |
| `confirmatory.py` | `d19aa6d0d322a74e0b2c67984064a4cb684725208b4b25f713bce83f0a6972b9` |
| `correlated.py` | `8f269de6dad106a079b0aeac9905d24dfbe1a3851f0522a10ef001d421a19f87` |
| `run.py` | `35f694771885c64f3fd24e2fa1c5b2277be2523e976d040126dc007020d53ecb` |

Le tag confirmatoire contient le même `confirmatory.py`, mais `run.py` y a pour hash **`31a23b9f25cd89e9af968f32f9bb8779509f290373e19ad294ecd4de3a1a8876`**. Le diff jusqu'au tag corrélé ajoute seulement le générateur corrélé et la branche `ancestor_m` ; la branche indépendante est inchangée. C'est déclaré dans `code/README.md:21–26`. **OK**.

**MAJEUR pour la formulation de provenance** : le tag pilote `bc2f838` ne contient aucun runner NH-01. Il gèle le protocole, pas le code. Le premier runner est au commit `86bfbfd`, suivi de `6606aa6` et du refactoring de configuration confirmatoire. Ne pas annoncer une reproduction du pilote « depuis le code au tag pilote » : elle est impossible. Épingler séparément son protocole et la version du code réellement utilisée. La note pilote le fait en partie (`nerve-wml/docs/results/2026-10-25-nh01-pilot.md:4`). Les trois `run_meta.json` initiaux portent tous le commit du clone superficiel **`8a13a33…`** ; ils ne suffisent donc pas à identifier le code exécuté. La provenance du 30 améliore nettement ce point pour N = 1000, sans transformer rétrospectivement le pilote en code gelé dans `bc2f838`.

### 5.3 Instructions exécutables

**MAJEUR — la commande de comparaison ne fonctionne pas après le run documenté.** `run.sh:43–54` appelle des runners qui écrivent **`cells.jsonl`** (`run.py:658`, `confirmatory.py:333`, `correlated.py:198`). Aucune compression n'est effectuée par `run.sh`. Or `scripts/compare_nh01.py:37` exige **`cells.jsonl.gz` dans les deux répertoires**. Le mode smoke a permis de reproduire le `FileNotFoundError` sur ce fichier ; les runners complets utilisent le même nom de sortie. Les instructions `README.md:84` et `code/README.md:41` ont donc une étape manquante. Correction minimale : `gzip -k results/nh01_confirmatory/cells.jsonl` avant comparaison, et analogue pour les autres runs ; meilleure interface : le comparateur accepte les deux formats.

**MAJEUR — le comparateur ne décide pas correctement du succès par son code de sortie.** Il écrit les différences mais ne retourne pas un code d'échec lorsque `keys_equal` ou `summary_equal_excl_run_meta` est faux, ou lorsque des cellules diffèrent (`compare_nh01.py:34–80`). Une simple commande ayant terminé sans erreur ne certifie donc pas une reproduction. Il écrase aussi silencieusement d'éventuelles clés dupliquées dans `load_cells()` ; aucune n'est présente dans les données auditées. Ajouter une vérification d'unicité et un statut de sortie défini rendrait le contrôle plus sûr.

**MINEUR** : `run.sh all` exécute confirmatoire puis corrélé, **sans pilote** (`run.sh:53–54`). C'est conforme à la description générale du wrapper, mais le nom `all` surprend. `--analyze-only` nécessite une décompression préalable des cellules distribuées, ainsi que `run_meta.json` si l'on veut conserver les métadonnées ; les instructions devraient donner cette commande. `scripts/rerun_nh01.sh` est correctement signalé comme spécifique au site ; son chemin Python est codé pour la machine d'origine (`:6`).

**MAJEUR — identité numérique et identité de fichier ne sont pas interchangeables.** `A:330–331`, `code/README.md:61–62`, `README.md:97` imposent une identité en octets des figures et de tous les champs des cellules. La régénération locale démontre que cet objectif dépasse la reproductibilité scientifique nécessaire, même avec NumPy/Matplotlib épinglés. Les PNG N = 1000 ont les mêmes pixels et des hash différents ; la nouvelle tâche N = 1000 conserve exactement ses statistiques et diffère d'environ 10⁻¹³ sur deux champs flottants. Distinguer **identité interne sur l'hôte d'origine** et **critère de comparaison entre plateformes**, avec tolérances annoncées et sans tolérance sur les classifications/clefs.

Les dépendances directes sont épinglées, mais pas Python au niveau patch ni toutes les dépendances de rendu/transitives ; des freezes sont fournis pour les re-runs. C'est suffisant pour une reproduction numérique raisonnable, pas une promesse de bit-exactness sur toute plateforme. Enfin, `c_spec: NaN` et certains ratios NaN sont acceptés par Python mais ne sont pas du JSON strict ; **MINEUR** pour les consommateurs hors Python.

### 5.4 Manifestes, archivage et preuves conservées

**OK** : dans chacun des trois `data/*/SHA256SUMS`, les cinq sommes sont exactes, y compris celle de `cells.jsonl` calculée sur le flux décompressé. Une vérification naïve avec `shasum -c SHA256SUMS` échoue sur ce seul fichier tant qu'il n'a pas été décompressé ; il faut le documenter.

**MINEUR — manifeste global périmé** : `data/MANIFEST.sha256` contient 33 entrées ; **32 passent et une échoue**. À la ligne **33**, `README.md` attend `6cac1e69b397584ed36a389df0c7bc2c8d48b4ecea1bb8752a59e5bff41b6a21`, alors que le fichier fourni vaut **`6b4ee40357cc9b5b65b3aace85bb9febd179b4686771789fcac53d3b1d76e242`**. Les cellules, résumés, figures et fichiers de provenance ne sont pas concernés. La phrase « covers every file » de `data/README.md:5` est à comprendre hors manifeste lui-même ; régénérer le manifeste après la dernière édition du README.

**OK — DOI et contenu de l'archive vérifiés.** L'API Zenodo retourne bien le record **23833431**, DOI **10.5281/zenodo.23833431**, publication le **31 octobre 2026**. J'ai téléchargé le ZIP **107 324 361 octets**, vérifié son MD5 **`59d698cf33f65f8e4c4486d373306f32`**, et comparé ses quinze fichiers `results/{nh01,nh01_confirmatory,nh01_correlated}/{cells.jsonl.gz,summary.json,figure.png,run_meta.json,SHA256SUMS}` au paquet : **15/15 identiques en octets**. [Record Zenodo](https://zenodo.org/records/23833431), [métadonnées API](https://zenodo.org/api/records/23833431).

**OK — Software Heritage** : les trois révisions complètes de `A:298–300` résolvent via l'API ; le snapshot **`01242c8b5873518a503b84a80ce3a302bb69b8a8`** contient aussi les trois références de tags annotés, comme objets release. Cela vérifie la disponibilité actuelle des références. La date précise de visite annoncée n'a pas été authentifiée ici indépendamment de la description de l'équipe. [Snapshot archivé](https://archive.softwareheritage.org/api/1/snapshot/01242c8b5873518a503b84a80ce3a302bb69b8a8/).

**MAJEUR, transparence plutôt que preuve contraire** : les dossiers `provenance-rerun-20261030/` ne contiennent ni les cellules recalculées ni les fichiers `github_tag_ref.json`, `github_tag_object.json`, `git_status_before.txt` ou `git_ls_files.txt` que produit le wrapper (`scripts/rerun_nh01.sh:31–48`). Les rapports `comparison.json` sont cohérents avec les résumés et hashes fournis ; leur comparaison complète de cellules et les contrôles pré-lancement ne peuvent pas être refaits avec ce seul paquet. Archiver ces pièces renforcerait l'affirmation de provenance. La phrase du README « every committed artefact » est trop large : les preuves de re-run portent sur les **deux séries N = 1000**, pas sur le pilote.

## 6. Rédaction, figures, longueur et bibliographie

**OK — longueur.** `article.md` contient environ **3247 mots bruts** selon `wc -w`, références et syntaxe incluses. La compilation de sa version courante, après régénération et Biber, donne **huit pages**, bibliographie comprise : dans la cible indicative de 4–8 pages mentionnée dans la demande. Je n'ai pas retrouvé de limite obligatoire de 4–8 pages sur la page officielle des consignes ; ce n'est donc pas un motif formel de rejet. Le bloc de provenance, long et rempli de chemins, peut être abrégé dans l'article et renvoyé à un supplément pour accueillir une discussion scientifique plus précise.

**MAJEUR — deux sources divergent.** `article/content.tex:22–25` contient encore le TODO demandant de vérifier les figures et tailles Monte Carlo, alors que `article.md:30–41` a été complété. Le diff de régénération confirme cette divergence. Le `Makefile:29–30` dépend de `content.tex`, mais ne contient **aucune règle qui le reconstruise à partir d'`article.md`**. Ainsi `make` peut compiler l'ancien texte sans erreur de dépendance. La version à évaluer doit être unique : régénérer le `.tex`, puis ajouter cette dépendance ou documenter une commande de build unique qui exécute d'abord `md2tex.sh`. Le fichier source Markdown modifié avant la revue n'a pas été écrasé.

**MAJEUR — mise en page réellement défectueuse.** La compilation avec bibliographie réussit, mais le log signale des `Overfull \\hbox` jusqu'à environ **274 pt**. L'inspection des pages confirme des chemins et de longues lignes mathématiques sortant des marges, notamment dans la description des pré-enregistrements, les listes de paramètres et la provenance (`A:134–142`, `A:288–327`, `content.tex:138–174` et `:398–479`). Les tableaux confirmatoire et corrélé sont lisibles, mais utilisent mal l'espace ; le tableau corrélé est coupé entre pages 4 et 5 et sa ligne m = 0,30 est très haute. Remplacer les longs chemins dans le corps par des identifiants courts reliés à une table de provenance, autoriser la coupure des URL/chemins et alléger les tableaux.

**MAJEUR — figure corrélée : la légende d'avertissement ne suffit pas.** La figure publiée à `A:236` montre en orange des ratios de l'ordre de 40–45 à T = 0 et 30–35 à T = 0,2, et son titre indique **m = 0.3: confirme ; C4 gain_increases**. Ce sont les informations visuelles dominantes, alors que le texte les neutralise. À T = 0,2, la courbe repose sur cinq dénominateurs définis ; à T = 0, sa valeur est finie mais très dépendante de la grille. Ce décalage n'est pas acceptable comme figure principale finale. Conserver intacte la figure brute dans `data/` est une bonne décision d'archivage ; produire une **figure de publication distincte**, par un petit script d'analyse traçable, ne falsifierait pas le pré-enregistrement. Masquer le ratio non interprétable à T = 0,2, afficher le nombre de graines définies, qualifier ou retirer la courbe T = 0 selon la règle retenue, et supprimer le titre automatique « confirmé » pour ce niveau. Conserver les capacités absolues à T = 0, informatives.

**OK / MINEUR — figure confirmatoire.** Les quatre panneaux et la légende décrivent correctement les courbes ; les IC sont bien des IC de moyenne, pas des dispersions de toutes les graines. Le titre « Spurious attractors » du panneau c doit devenir « States classified as spurious » : le panneau n'énumère pas les attracteurs. Les petits écarts du shrink à T = 0,2 sont peu visibles sur l'échelle générale ; un encart ou les valeurs du tableau suffisent. La figure du pilote est incluse dans les fichiers mais n'apparaît pas dans le corps ; la mentionner en supplément serait utile sans ajouter une page principale.

**MAJEUR — causalité et portée.** « removing the diagonal ... is responsible for the finite optimum » (`A:167`) n'est soutenu par aucune ablation avec/sans diagonale. « a finite-size effect » dans le résumé (`metadata.yaml:64`) n'est pas isolé d'un effet de définition de la capacité, du bruit du cue ou de la dynamique. La phrase sur la contraction des bassins (`A:276`) va aussi au-delà des mesures : une seule amplitude de bruit est testée au confirmatoire. Remplacer ces attributions par « observed under this protocol », et présenter les mécanismes comme hypothèses à tester.

**MINEUR — lisibilité.** Donner des noms distincts à l'overlap de récupération et au paramètre de l'ancêtre ; préciser « dernier croisement » et « maximum sur la grille » ; écrire les trois critères successifs avec leurs dates au lieu d'une liste apparemment commune à tous les runs. Remplacer les règles internes (« L1 », « rule 10 », « PI ruling », numéros d'issues) par leur contenu scientifique en une phrase, en conservant leur provenance dans le supplément. Employer « data/ » dans les chemins propres à cette soumission ; les références à `results/` sont des chemins amont.

**MINEUR — bibliographie.** Les cinq notices BibTeX sont présentes et bien formées. Biber ne rend cependant que **quatre références**, parce que `amit1985storing` n'est cité que dans la section Markdown `# References`, que `md2tex.sh:9` supprime avant conversion. Il faut ajouter `[@amit1985storing]` près de la valeur 0,138 (`A:26`). La mention « biber could not run » de `README.md:109–110` décrit le build interne, pas un PDF bibliographique final ; remplacer cette note après un build complet. Ajouter quelques travaux récents pertinents et la référence du paquet archivé, sans transformer cette réplication en revue générale.

Contrôle de fin de revue : le dépôt de soumission est passé au commit `dc19644024a1924c5904a31dfb93d35bc4dd9293` pendant l'examen ; le SHA-256 du Markdown examiné reste celui indiqué en tête, et les hashes de `content.tex`, du manifeste et du README des données sont inchangés. Les constats ci-dessus portent donc toujours sur les fichiers présents à la fin de cette revue.

## 7. Références 2024–2026 vérifiées et utiles (huit propositions)

Recherche ciblée effectuée le **31 octobre 2026**, suivant la compétence de revue bibliographique `scientific-thinking-literature-review`. Ce n'est pas une revue systématique exhaustive. Périmètre : dreaming/unlearning dans les Hopfield classiques, distinction avec les mémoires associatives denses, et exemples récents de réplication ReScience. Sources de découverte : moteur web ; vérification sur arXiv, versions éditeur en dépôt institutionnel et catalogue officiel de ReScience. Requêtes principales : `Hopfield dreaming unlearning 2024 2025 2026`, `Eigenvector Dreaming DOI`, `Daydreaming Serricchio 107216`, `dense associative memory capacity 2024`, puis titres exacts et catalogue 2025 de ReScience. Les doublons arXiv/article ont été fusionnés par titre et DOI. Sont exclus les résumés de blogs, les notices sans source primaire et les capacités non comparables utilisées comme validation de NH-01.

| Référence et statut vérifié | Usage précis dans la discussion ; limite |
|---|---|
| **Benedetti, M., Carillo, L., Marinari, E., Mézard, M. (2024). _Eigenvector dreaming_. J. Stat. Mech. 2024, 013302. DOI 10.1088/1742-5468/ad138e.** Publication vérifiée sur le PDF éditeur hébergé par Sapienza, p. 2 ; prépublication arXiv 2023. [Version publiée](https://iris.uniroma1.it/retrieve/f0d445de-f87b-4d9a-af21-8c6d0f9dbdce/Benedetti_Eigenvector-dreaming_2024.pdf), [arXiv](https://arxiv.org/abs/2308.13445). | **Prioritaire** : évolution du spectre et des vecteurs propres lors de l'unlearning ; explique pourquoi comparer une transformation spectrale à une simple échelle est pertinent. Ne pas identifier automatiquement leur algorithme au noyau fermé de 2019. |
| **Agliari, E., Alemanno, F., Aquaro, M., Fachechi, A. (version du 20 février 2024). _Regularization, early-stopping and dreaming: a Hopfield-like setup to address generalization and overfitting_. arXiv:2308.01421v2.** Version de prépublication 2024 vérifiée ; première version 2023. [Notice et historique](https://arxiv.org/abs/2308.01421). | Relier les couplages issus d'unlearning à la régularisation et à l'arrêt précoce. Utile pour discuter un t fini ; cette référence ne prouve pas que le t* = 7 de NH-01 soit causé par la taille finie. Aucune publication en revue n'est affirmée ici. |
| **Serricchio, L., Bocchi, D., Chilin, C., Marino, R., Negri, M., Cammarota, C., Ricci-Tersenghi, F. (2025). _Daydreaming Hopfield Networks and their surprising effectiveness on correlated data_. Neural Networks 186, 107216. DOI 10.1016/j.neunet.2025.107216.** Référence revue/DOI vérifiée sur arXiv ; texte intégral consulté. [Notice](https://arxiv.org/abs/2405.08777), [texte intégral](https://arxiv.org/html/2405.08777v1). | **Prioritaire** : renforcement et suppression conjoints, corrélations, cartographies de récupération et bassins. Les corrélations y viennent d'un modèle à caractéristiques aléatoires ; elles diffèrent du générateur à ancêtre unique de NH-01. |
| **Lucibello, C., Mézard, M. (2024). _The Exponential Capacity of Dense Associative Memories_. Phys. Rev. Lett. 132, 077301. DOI 10.1103/PhysRevLett.132.077301.** Publication et DOI vérifiés sur arXiv v4, texte intégral consulté. [Notice](https://arxiv.org/abs/2304.14964), [texte](https://arxiv.org/html/2304.14964v4). | Définir soigneusement capacité d'un motif typique, de tous les motifs et taille des bassins. **Le modèle et l'échelle P = exp(αN) diffèrent** du Hopfield pairwise de NH-01 ; aucune comparaison directe des α numériques n'est valide. |
| **Marinari, E., Rossi, S., Zamponi, F. (2026). _Dreaming improves memorization in a Hopfield model with bounded synaptic strength_. arXiv:2603.09384.** Prépublication du 10 mars 2026, notice primaire vérifiée. [arXiv](https://arxiv.org/abs/2603.09384). | Motiver les limites d'un contrôle de norme globale lorsque les poids sont bornés et que l'apprentissage est séquentiel. Ne constitue pas une réplication du noyau fermé ni une validation supplémentaire de ses ratios. |
| **Barra, A., Durante, F., Ladiana, A., Marra Solazzo, M. (2026). _Do Hopfield Networks Dream of Stored Patterns? A Statistical-Mechanical Theory of Dreaming in Multidirectional Associative Memories_. arXiv:2605.13721.** Prépublication du 13 mai 2026, auteurs/date/résumé vérifiés sur la notice primaire. [arXiv](https://arxiv.org/abs/2605.13721). | Situer le dreaming dans une architecture hétéroassociative à plusieurs couches. Discussion de portée uniquement : les résultats multilayers ne prouvent pas ceux de NH-01. La notice confirme que les deux références 2026 évoquées dans le pré-enregistrement pilote existent bien. |
| **Reynes, M., Aussel, A. (2025). _[Re] Model of thalamocortical slow-wave sleep oscillations and transitions to activated states_. ReScience C 10(1), #5. DOI 10.5281/zenodo.16529268.** Métadonnées, code et revue ouverts vérifiés dans le catalogue officiel ; texte intégral non évalué ici. [Catalogue ReScience](https://rescience.github.io/read/), [record](https://zenodo.org/records/16529268). | Exemple éditorial récent, proche du domaine sommeil/neurosciences numériques, pour organiser original, implémentation et pièces de reproduction. Pas une source de preuve sur les réseaux de Hopfield. |
| **Obadage, R. R., Thennakoon, K., Rajtmajer, S. M., Wu, J. (2025). _[Re] Network Deconvolution_. ReScience C 10(1), #4. DOI 10.5281/zenodo.15321683.** Publication et auteurs vérifiés sur le catalogue et le record Zenodo ; texte intégral non évalué ici. [Record primaire](https://zenodo.org/records/15321683). | Autre exemple de paquet de réplication Python et de lien avec une revue publique. À utiliser comme référence de présentation, sans lui attribuer de résultat sur la stabilité du noyau NH-01. |

Le noyau de discussion peut se limiter aux références 1, 3 et 4, puis à un exemple ReScience. Les prépublications 2026 sont utiles pour situer la portée actuelle, mais ne remplacent pas les comparaisons quantitatives à l'article de 2019.

## Corrections proposées — prêtes à appliquer

Les remplacements ci-dessous sont en anglais pour s'insérer directement dans le manuscrit. Ils ne changent aucun résultat ni fichier gelé. Les étapes de build et de manifeste sont des propositions ; elles n'ont pas été appliquées aux dépôts.

1. **Portée de la réplication — `A:43–46`.**
   - Ancien : « We replicate these qualitative claims with an independent NumPy implementation at finite size ... »
   - Nouveau : « We independently implement the published kernel and partially replicate its qualitative retrieval advantage at finite size (N ≤ 1,000). We use a new noisy-cue capacity estimator and do not reproduce the replica-symmetric capacity curve or the original Monte Carlo figures. Each study's design was registered before its main run; later registrations were informed by the preceding studies. »

2. **Dynamique originale — `A:30–37`.**
   - Ancien : « The original Monte Carlo checks ... use single-spin-flip Glauber dynamics ... »
   - Nouveau : « For the magnetisation curves (Figs. 7–8), the original study uses single-spin-flip Glauber dynamics and measures observables after equilibration. Its zero-noise field and basin analyses (Figs. 9–10) use the parallel sign update of Eq. (2.17), with N = 1,000 and P = 50. Fig. 9 reports 20 evolutions and 20 pattern realisations; Fig. 10 reports 200 evolutions for each of 200 realisations. »
   - Conserver ensuite les paramètres exacts N = 5000, M = 10, charges et temps des Figs. 7–8, déjà vérifiés.

3. **Test du projecteur — `A:81`.**
   - Ancien : « t = 10⁶ reproduces the projector »
   - Nouveau : « t = 10⁸ approximates the projector within the numerical tolerance tested ».
   - À `A:79–84`, préciser « 20 test functions, comprising 23 executed cases » et remplacer le chemin par `code/tests/test_nh01_hopfield_dream.py` pour le paquet de soumission.

4. **Bruit du signal — `A:97–98`.**
   - Ancien : « exactly round(0.10 N) bits flipped (overlap 0.80) »
   - Nouveau : « exactly round(0.10 N) bits flipped (overlap 0.80 at N = 1,000; small rounding differences occur at the pilot sizes) ».

5. **Estimateur — `A:101–105`.**
   - Ancien : « the load at which the piecewise-linear retrieval fraction ... crosses 0.5 ... flagged below_grid when r < 0.5 at the lowest load »
   - Nouveau : « the interpolated crossing immediately after the last grid load with retrieval fraction r ≥ 0.5. If no grid load reaches 0.5, the code records a below_grid flag and a zero sentinel; if the largest load reaches 0.5, it records a right-censored estimate at 0.95. »

6. **Théorème de shrink — `A:120–121`.**
   - Ancien : « ... is a heating and cannot raise capacity. »
   - Nouveau : « ... is equivalent to increasing the temperature to T/c. This transition-kernel identity does not impose a deterministic inequality on our finite-time capacity estimates; the effect at T = 0.2 is therefore measured empirically. »

7. **Cause du maximum et écarts — `A:165–167`.**
   - Ancien : « ... is responsible for the finite optimum in t reported below. »
   - Nouveau : « ... changes the update fields relative to the original parallel rule. We also replace that rule by asynchronous updates, use a fixed number of cue flips rather than independent bit flips, and apply an absolute overlap threshold. We did not isolate the causal contribution of these changes to the observed optimum over t. »

8. **Séquence des pré-enregistrements — `A:169` et `A:255`.**
   - Ancien : « Numbers fixed before any run » / « Under rules fixed before any run ».
   - Nouveau : « Parameters and decision rules were fixed before each respective main run. The confirmatory amendment changed the pilot's C2 and C3 criteria after observing the pilot; the correlated study was registered after the independent-pattern studies. »
   - Ajouter après la liste C1–C4 : « The pilot instead used the original C2 monotonicity rule with tolerance 0.05 and P4 at loads 0.10 and 0.14. »

9. **Forte corrélation à T = 0 — ligne m = 0,30 du tableau `A:211`.**
   - Ancien, colonne C1 : « not computable (denominator at the grid floor; the summary's value is not cited) ».
   - Nouveau : « 44.38 [42.56, 46.97] under the registered interpolation; all ten denominators are positive, but the magnitude is sensitive to the 0.01–0.02 load interval. »
   - Si l'auteur préfère ne pas mettre le nombre dans le tableau : « Computable but not retained for quantitative interpretation because the Hebbian crossing is poorly resolved by the load grid; the registered estimate is reported in the data. »

10. **Forte corrélation à T = 0,2 — `A:213–226`, résumé et README.**
    - Ancien : « a ratio whose denominator sits at the load-grid floor is reported as not computable ... since c(t) < 1 by construction the theorem gives S ≤ 1 ... ».
    - Nouveau : « At T = 0, all ten Hebbian crossings are bracketed by loads 0.01 and 0.02, so their ratios are defined but poorly resolved. At T = 0.2, five Hebbian estimates are below the grid and their ratios are undefined; the code's shrink estimate 0.6 [0.2, 1.0] uses only the five defined seeds. We therefore report the overall level as inconclusive after analysis, while retaining the registered labels in the raw outputs. The zero sentinels indicate censoring, not measured zero capacities. »
    - À `A:282` et dans `metadata.yaml:64`, remplacer « falls below the load grid » par « is close to the lower grid limit at T = 0 and falls below it on five seeds at T = 0.2 ».

11. **C4 — `A:228–230`.**
    - Ancien : « ... the direction, not the value, is the finding. »
    - Nouveau : « The registered C4 estimate is 40.6 [38.7, 43.2]. Its magnitude depends strongly on interpolation of the small Hebbian denominator at m = 0.30. We retain the increasing direction as a descriptive result and do not interpret this interval as accounting for load-grid uncertainty. »

12. **Stabilité — `A:261–262`.**
    - Ancien : « every stored pattern is a fixed point up to α = 0.95 for t ≥ 10 in the pilot's stability arm ».
    - Nouveau : « the pilot's f = 0 capacity estimate is right-censored at α = 0.95 for t ≥ 10. This is a 50%-retrieval criterion on at most 32 probed patterns, not a test that every stored pattern is a fixed point. »

13. **Conclusion générale et attracteurs — `A:255–260`.**
    - Ancien : « confirms the central qualitative claims ... removes spurious final states ... ».
    - Nouveau : « supports the published qualitative retrieval advantage of the dreaming kernel under our finite-size protocol. At loads 0.14 and 0.20, none of the tested dream t = 10 probes was classified as spurious; this does not establish the absence of spurious attractors throughout the state space. »

14. **Portée du contrôle — `A:267–270`.**
    - Ancien : « no uniform rescaling ... lowers capacity by 2–3 % ... as a heating must ».
    - Nouveau : « the Frobenius-matched rescalings tested here do not reproduce the dreaming gain. They are inert at T = 0 by scale invariance and reduce the mean empirical capacity by 2.52% at T = 0.2 (95% seed-bootstrap interval: 1.80–3.35%). »

15. **Bassins et théorie — `A:273–277`.**
    - Ancien : « ... concerns the stability of the stored patterns ... shows that basins of attraction shrink ... the original analysis does not quantify. »
    - Nouveau : « Our noisy-cue threshold differs from the original equilibrium retrieval boundary. We observe a lower empirical capacity at t = 100 than at the grid optimum t = 7, without measuring full basin sizes or identifying the cause. The original paper does quantify retrieval basins, at N = 1,000 and α = 0.05, under parallel zero-noise dynamics; that experiment does not cover our higher-load protocol. »

16. **Identité et périmètre des re-runs — `A:330–331`, `README.md:7–8`, `code/README.md:61–62`.**
    - Ancien : « Every committed artefact was reproduced bit-exactly ... figure.png must be byte-identical and every cell must match except task_seconds. »
    - Nouveau : « The two N = 1,000 studies were internally reproduced on the original host with exact non-timing cell values and identical figure files. On other platforms, compare cell keys and discrete outcomes exactly and floating-point diagnostics with a declared numerical tolerance; PNG byte identity is not required. The pilot is not covered by this internal provenance re-run claim. »

17. **Figure de publication — `A:236`.**
    - Ancien : « The figure is the unmodified output ... its ratio curve must not be read as a result. »
    - Nouveau, après production de la figure corrigée : « Publication view of the registered outputs. At m = 0.30, the T = 0 ratio is marked as sensitive to load-grid resolution, and T = 0.2 ratios are omitted because five Hebbian denominators are below the grid. Absolute T = 0 capacities are retained. Unmodified runner figures and automatic labels remain available in data/. »
    - Dans le panneau c confirmatoire, ancien « Spurious attractors » → nouveau « States classified as spurious ».

18. **Commandes et fichiers de publication.**
    - Ancien, après un run : `python -I scripts/compare_nh01.py ../data/nh01_confirmatory results/nh01_confirmatory cmp.json`.
    - Nouveau minimal : `gzip -k results/nh01_confirmatory/cells.jsonl`, puis la commande précédente ; analogue pour corrélé et pilote. Ajouter ensuite une lecture explicite des indicateurs de succès, tant que le comparateur n'a pas de statut de sortie d'échec.
    - Ancien : `cd article && make`.
    - Nouveau minimal : `cd article && bash md2tex.sh && make`, avec Python/PyYAML, pandoc, XeLaTeX et Biber disponibles ; idéalement ajouter une vraie règle de dépendance au Makefile.
    - Ancien : manifeste annonçant un contrôle global intégralement valide → nouveau : **régénérer `data/MANIFEST.sha256` après la dernière édition de `data/README.md`**, puis vérifier les 33 entrées. Ne pas modifier les cellules ni leurs hashes pour résoudre une erreur de README.
    - Ancien, `A:294` : « (to be created) » → supprimer : le dépôt public existe.
    - Ancien, `A:26` : valeur AGS sans clé de citation → ajouter `[@amit1985storing]` pour que la cinquième référence apparaisse réellement dans la bibliographie.
