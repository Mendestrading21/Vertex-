# SKYLER LOT 450 — BILAN n°14 (tranche 440 → 449) : le tri par affichage paie, la cadence des rang 1 baisse, et mon compte d'erreurs publiées était trop flatteur

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-450` (base : lot 449 fusionné,
3fc9045)

Quatorzième bilan. Fait **sur pièces** : les dix rapports relus, les chiffres
vérifiés dans le dépôt, **aucune trouvaille rejouée**. Aucun serveur DEMO, aucun
moteur rouvert. Une seule mesure fraîche — les MD5 — et elle est dite comme
telle.

## Ce que la tranche a déposé — mesuré

**Base résolue explicitement avant tout chiffre** (leçon 430/440, deux fois
payée) : `d400bf2` **est** le lot 439 fusionné ; `3fc9045` **est** le lot 449.
L'intervalle donne bien **dix commits**, vérifié avant publication.

```text
base d400bf2 (lot 439 fusionné) → tête 3fc9045 (lot 449 fusionné)

commits                                    10
fichiers modifiés                          12
   docs/refactor/validation                11   (10 rapports + SKYLER-INDEX.md)
   docs/skyler                              1   (STATUS.md)
fichiers HORS docs/                          0
lignes                        +2 552 / −0        (addition pure, rien supprimé)

terminal.py + vertex/** touchés               0 fichier
rapports 440→449 présents                    10 / 10
lignes d'index 440→449                       10 / 10
blocs STATUS par lot 440→449                 10 / 10
volume des dix rapports                  98 591 octets
MD5 des 8 pages remesurés                     8 / 8 identiques
```

Depuis le lot 399 (`29f4435..3fc9045`) : **1 fichier hors `docs/`** —
`tests/test_skyler_sweep_x1.py`, lot 401 — et **0 fichier de production**.
**Aucun octet de production n'a changé depuis le lot 399.**

## Ce que les dix lots ont produit

```text
440  BILAN n°13                                                          —
441  piste /analysis refermée · corpus incomplet · unité corrigée        ✗
442  « R:R structurel » constant à 3, rr_res invisible                   ✓ rang 1 (+ rang 2 : MM 20/50/200)
443  TROIS R:R contradictoires — aggrave le 442                          ✓ rang 1 (+ rang 4 : stop_dist_atr)
444  recensement AST de 235 phrases + CORRECTION publiée du 443          ✗
445  6 phrases de `basis` TOUTES EXACTES — première famille saine        ✗
446  horizon « séance +N » sur séances OBSERVÉES, non affiché            ~ rang 4
447  max pain multi-échéances, TEXTE VISIBLE sur /portfolio              ✓ rang 1
448  exception Python affichée comme motif sur /options                  ✓ rang 2
449  veine `reason` refermée 7/7 — le rang 2 du 448 TRIPLE               ✓

      3 rang 1 · 2 rang 2 · 4 rang 4 · 3 bornages · 3 corrections publiées · 1 bilan
```

## Le fait nouveau : le tri par affichage

Le 446 a établi que **le rang dépend d'abord de l'écran**. Les 447, 448 et 449
l'ont appliqué : **trois lots de suite ont trouvé** — un rang 1, un rang 2, puis
un triplement de portée.

**Lecture A — c'est le 425 renommé.** « Partir de l'écran » disait déjà :
commencer par ce qui est rendu. « Vérifier l'affichage avant de mesurer » serait
la même instruction sous un autre nom.

**Lecture B — c'est une règle distincte, et plus forte.** Le 425 dit **où
chercher** ; le 446 dit **s'il vaut la peine de dépenser la mesure**. La
différence est opérationnelle et se lit dans les résultats : aux lots **435, 436
et 446**, la boucle a mesuré un défaut **entièrement**, puis a découvert que
personne ne l'affichait, et a dû le **descendre au rang 4** — trois mesures
dépensées pour trois rétrogradations. Aux lots **447, 448, 449**, l'ordre est
inversé : l'écran d'abord, la mesure ensuite — trois lots productifs d'affilée.

**Je tranche : règle distincte, et la plus rentable depuis le 425.** Le 425
choisit l'objet ; le 446 pose un **péage avant la dépense**. Trois
rétrogradations avant, trois trouvailles après.

**Avec une réserve que je pose franchement** : trois lots est un petit
échantillon, et le rendement des 447-449 doit une partie de son succès à la
**carte du 444** — qui avait déjà établi quels champs sont lus par combien
d'écrans. Sans ce recensement, le péage aurait coûté cher à chaque lot. La règle
est bonne **parce qu'une carte existait**.

## Le rendement, recompté — et il baisse

**Recompté, pas hérité** (leçon 440). Et il faut deux conventions, parce qu'un
même dossier peut occuper deux lots :

```text
                        rang 1 PAR LOT      rang 1 PAR DOSSIER DISTINCT
tranche 420 → 429             4                        4        (422, 425, 427, 428)
tranche 430 → 439             4                        3        (432+433 = même famille)
tranche 440 → 449             3                        2        (442+443 = même famille ; 447)
```

**La cadence baisse, dans les deux conventions.** Je ne l'enjolive pas.

Mais le compte des **défauts affichés** — rang 1 et rang 2 confondus — tient :

```text
tranche 430 → 439     4 rang 1 + 1 rang 2 = 5 défauts affichés
tranche 440 → 449     3 rang 1 + 2 rang 2 = 5 défauts affichés
```

**Lecture honnête : le volume tient, la gravité moyenne descend.** La tranche a
trouvé autant de choses affichées, mais deux d'entre elles ne sont pas des
mensonges — un message technique et une promesse de courbes. C'est cohérent avec
un dépôt dont les défauts les plus graves ont déjà été relevés dans les tranches
précédentes.

## Mes deux comptes d'erreurs — dont un était trop flatteur

**Arrêtés avant publication : 20.** Recompté sur la tranche : 441 (1 —
« `confirm` sans `invalidate` », démenti par la source), 443 (3 — `resistance`,
`setup_quality`, `stop_type`), 445 (1 — la boucle de `conflicts` qui semblait non
bornée), 446 (1 — la collision de nom sur `return_pct`). **+6**, ce qui porte le
total de 14 à **20**. Le chiffre hérité est confirmé par recompte.

**Publiés puis corrigés : 3, et non 1.** C'est le chiffre que je transportais
depuis le 444, et **le recompte le dément** :

```text
439  « 22 248 octets » pour /analysis         → CARACTÈRES, pas octets     corrigé au 441
442  « rr_res n'est affiché nulle part »      → visible en BLOCAGE < 2,0   corrigé au 443
443  « invalidation lu par 5 écrans »         → 2, et un AUTRE payload     corrigé au 444
     et « stop_type atteint un écran »        → RETIRÉ
```

**Trois affirmations publiées ont dû être corrigées, pas une.** Je ne comptais
que la troisième parce que c'est celle que le 444 avait nommée « la première fois
qu'un résultat faux m'échappe ». C'était déjà la deuxième, et il y en a eu une
troisième depuis.

**Ce que l'écart signifie** : 20 contre 3, c'est un filtre qui retient environ
sept erreurs sur huit. Ce n'est pas rien, et ce n'est pas parfait. Surtout, les
trois qui sont passées ont **toutes** la même cause — un chiffre ou une portée
annoncés sans que le payload soit identifié par sa forme. C'est la règle que le
448 a fini par écrire, et les trois échecs la précèdent.

## Ce que les dix rapports NE prouvent PAS

- **Aucune trouvaille constatée sur des données réelles.** Scan, board et
  `detail` vides au démarrage pendant toute la tranche. Tous les bancs tournent
  sur des entrées **fabriquées**.
- **Aucun navigateur ouvert de toute la tranche.** Les chaînes d'affichage sont
  établies sur les octets servis, jamais observées au rendu.
- **93 des 110 phrases concluantes du 444 restent fermées.** La carte est
  dressée ; le territoire ne l'est pas.
- **Plusieurs formatages sont recopiés, pas exécutés** (443 le R:R pré-trade, 448
  et 449 les vidages d'exception) : les exceptions sont réelles, la ligne qui les
  met en forme ne l'est pas.
- Les bancs établissent le **comportement du code**, jamais la **fréquence** des
  cas dans l'usage réel — vrai pour les 200 barres du 442, les trous de log du
  446, les échéances multiples du 447, les entrées mal typées du 449.

## Classement coût/risque — mis à jour avec 442+443, 447, 448+449

Ordre **par coût et risque croissants**. Le rang de gravité est rappelé, il ne
dicte pas l'ordre.

```text
#   dossier                        geste                                        surface        risque
1   434 renderAnomalies            copier la garde écrite 20 lignes plus haut   3 lignes JS    très faible
2   427 légende multi-indices      bâtir la légende depuis `sets`               1 ligne JS     très faible
3   428 entonnoir de sélection     accepter les deux vocabulaires               2 lignes JS    très faible
4   437 « Catalyseurs imminents »  retirer `|| Date.now()` (3 pages)            3 lignes JS    très faible
5   448+449 trois vidages          journaliser, rendre un motif écrit           3 blocs except très faible
6   425 « 4 maturités réelles »    compte dynamique `${pts.length}`             2 chaînes      très faible
7   447 max pain multi-échéances   filtrer sur l'échéance la plus proche        1 filtre       faible
8   432+433 synthèses /portfolio   conditionner sur `allMarked` DÉJÀ CALCULÉ    3 branches     faible
9   442+443 les trois R:R          afficher `rr_res` + nommer chaque référence  4 rendus       faible
10  424 thesis_health              UNKNOWN quand les 2 listes sont vides        1 branche      faible
11  422 expected-move muet         l'ajouter à la liste de limites              1 chaîne       faible
```

Trois remarques mesurées :

**Les six premiers ne touchent aucun moteur.** Ils vivent dans cinq fichiers —
`opportunities_page.py` (1, et une part de 4), `markets_page.py` (2, 3, 6, et une
part de 4), `briefing.py` (part de 4), `options_intel_api.py` et
`options_lab_api.py` (5).

**Le n°5 est nouveau et il est le moins risqué du lot** : trois blocs `except`,
et **le modèle est déjà écrit dans `horizon_scanners`**, sur la même page.

**Le n°7 aussi est petit** : un filtre sur l'échéance avant `max_pain`, dans
`vertex/options/gex.py` ou chez son appelant. C'est le seul rang 1 de la tranche
dont la correction tient en un geste.

Les dossiers lourds (406/407/408/409/411, 388, 417, 416, 436) ne sont **pas**
classés : ils demandent une **décision de produit**. **Aucun GO n'est demandé,
rien n'est engagé.**

## Portée de ce bilan

Il mesure ce que la tranche a **déposé** et ce que les dix rapports
**affirment**. Il ne rejoue rien : **si un rapport s'est trompé sur un fait qu'il
présente comme mesuré, ce bilan reprend l'erreur** — et la tranche vient
justement de montrer que cela arrive.

Le classement des rangs est **attribué par moi-même**, ce n'est pas une métrique
indépendante. Le recompte des rang 1 en dépend directement, et je donne les deux
conventions plutôt qu'un chiffre unique.

La seule mesure fraîche prise ici est celle des **MD5** : 8/8 identiques.

## Où en est la boucle

Cinquante-troisième lot court, **quatorzième bilan**.

La tranche 440-449 est la première où la boucle **change de méthode en cours de
route** et où le changement se voit dans les résultats : trois rétrogradations
avant le péage, trois trouvailles après. C'est le seul acquis de méthode de la
tranche, et il est net.

Elle est aussi la première où **je dois corriger mon propre compte d'erreurs** :
trois affirmations publiées ont été reprises, pas une. Le filtre retient sept
erreurs sur huit — pas huit sur huit.

Et c'est la quatorzième tranche à se terminer sans qu'un seul des défauts
prouvés — **onze désormais classés, dont six à moins de dix lignes et sans
moteur** — ait été corrigé.

**Six bilans — n°9, n°10, n°11, n°12, n°13 et n°14 — attendent une réponse.**
