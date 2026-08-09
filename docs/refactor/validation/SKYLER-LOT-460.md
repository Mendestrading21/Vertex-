# SKYLER LOT 460 — BILAN n°15 (tranche 450 → 459) : sept défauts affichés au lieu de cinq, mais le rang 1 reste au plancher — et la « chaîne de relais » qui a porté la tranche n'est pas de moi

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-460` (base : lot 459 fusionné,
1b23377)

Quinzième bilan. Fait **sur pièces** : les dix rapports relus, les chiffres
vérifiés dans le dépôt, **aucune trouvaille rejouée**. Aucun serveur DEMO, aucun
moteur rouvert. **Une seule mesure fraîche — les MD5 — et elle est dite comme
telle.**

## Ce que la tranche a déposé — mesuré

**Base résolue explicitement avant tout chiffre** (leçon 430/440/450) :

```text
base 3fc9045 = « lot 449 — la veine reason refermée »
tête 1b23377 = « lot 459 — les deux dettes de la tranche soldées »
commits dans l'intervalle : 10          ← vérifié avant publication
```

```text
fichiers modifiés                          12
   docs/refactor/validation                11   (10 rapports + SKYLER-INDEX.md)
   docs/skyler                              1   (STATUS.md)
fichiers HORS docs/                          0
lignes                        +2 893 / −0        (addition pure, rien supprimé)

terminal.py + vertex/** touchés               0 fichier
rapports 450→459 présents                    10 / 10
lignes d'index 450→459                       10 / 10
blocs STATUS par lot 450→459                 10 / 10
volume des dix rapports                 104 212 octets
MD5 des 8 pages remesurés                     8 / 8 identiques   ← mesure fraîche
SW enregistré dans system.py            td-shell-v187
```

### Une correction de référence que je publie : le SHA du lot 399 était faux

Les bilans précédents écrivaient « depuis le lot 399 (`29f4435`) ». **Mesuré :
`29f4435` n'est PAS un ancêtre de la tête.** C'est le commit côté branche,
remplacé par le squash `20a917f`, qui est le vrai point de fusion du lot 399 sur
l'intégration.

```text
29f4435   ancêtre de la tête ?  NON   (commit de branche, superseded)
20a917f   ancêtre de la tête ?  oui   (« Lot 399 … (#431) », squash sur l'intégration)

depuis 20a917f : 60 commits · 63 fichiers
   HORS docs/     1   tests/test_skyler_sweep_x1.py   (lot 401)
   PRODUCTION     0   — AUCUN
```

**Le chiffre publié ne change pas** — 0 fichier de production, 1 fichier hors
`docs/` — mais **la référence était fausse** et l'intervalle était calculé à
travers un point de fourche. Quatrième fois que « résoudre la base avant tout
chiffre » paie.

**Aucun octet de production n'a changé depuis le lot 399 — recompté, pas hérité.**

## Ce que les dix lots ont produit

Relu dans la section « Classement » de chaque rapport.

```text
450  BILAN n°14                                                          —
451  4 phrases `source` jamais produites · 269 lignes mortes testées     ✗ rang 4 + 3
452  85 modules injoignables · COLLISION /api/anomalies/<sym>            ✓ rang 1 (+2, +3)
453  contrats de route : 26 candidats, 25 faux — BORNE le 452            ✗ (+ rang 4)
454  6 phrases `action` jamais lues · 6 routes feeds.py sans citation    ✗ rang 4 + 3
455  veine des phrases REFERMÉE · synthèse pré-trade sans les INCONNUS   ✓ rang 2
456  fractions affichées · plafond 200 · camembert constant              ✓ rang 2 + 3
457  BORNE V1 FIGÉE sur /portfolio · veine des fractions REFERMÉE        ✓ rang 1
458  classeur `catOf` aveugle au type — BORNE le 457 (14 contre 1)       ✓ rang 2
459  deux dettes SOLDÉES : gex_scan rang 4 → rang 2 ; 458 resserré       ✓ rang 2

      2 rang 1 · 5 rang 2 · 4 rang 3 · 5 rang 4 · 2 veines refermées
      3 bornages · 1 retrait d'interprétation · 1 bilan
```

**Note d'instrument** : compter les occurrences du mot « rang 1 » dans les
rapports **ne mesure rien** — le 450, qui est un bilan, en contient 13 parce
qu'il cite d'autres dossiers. Le tableau ci-dessus est relu **verdict par
verdict**, pas compté par occurrence.

## Le rendement, recompté — et il faut deux lectures

```text
                        rang 1 PAR LOT      rang 1 PAR DOSSIER DISTINCT
tranche 420 → 429             4                        4
tranche 430 → 439             4                        3
tranche 440 → 449             3                        2
tranche 450 → 459             2                        2
```

**Le rang 1 reste au plancher : deux tranches de suite à 2.** Je ne l'enjolive
pas.

Mais l'autre compte monte :

```text
DÉFAUTS AFFICHÉS (rang 1 + rang 2, par dossier distinct)
tranche 430 → 439     5
tranche 440 → 449     5
tranche 450 → 459     7      ← +2
```

Les cinq rang 2 nés dans la tranche sont **distincts** : phrase `/opportunities`
(452), synthèse pré-trade (455), plafond de 200 (456), `symbols_usable` plafonné
(456 → requalifié au 459), classeur `catOf` (458).

**Lecture honnête : la cadence des rang 1 ne se redresse pas, mais le volume de
défauts affichés augmente.** La tranche a trouvé **plus** de choses fausses à
l'écran que les deux précédentes — simplement moins graves en moyenne. C'est
cohérent avec un dépôt dont les mensonges les plus lourds ont déjà été relevés.

## Le fait nouveau : une chaîne de relais — et je dis d'où elle vient

Cinq lots consécutifs se sont passé le relais **par la forme du défaut trouvé**,
et non par le sujet :

```text
455  « un dénominateur total avec des numérateurs partiels »
       ↓ désigne
456  LES FRACTIONS AFFICHÉES                    → rang 2 + rang 3, au premier essai
       ↓ désigne (un plafond présenté comme une population)
457  LES LITTÉRAUX PÉRIMÉS DE L'INTERFACE       → rang 1
       ↓ désigne (un littéral qui duplique la Constitution)
458  LES LITTÉRAUX QUI DUPLIQUENT LA CONFIG     → rang 2 + bornage du 457
       ↓ laisse deux dettes
459  SOLDE PAR EXÉCUTION                        → une requalification vers le haut
```

**Quatre passages de relais, quatre lots qui paient.** Est-ce une règle distincte
de celles déjà écrites ? Oui, et la distinction est nette :

- **416** (« trois lots de même forme → changer de famille ») est une règle
  d'**arrêt**.
- **425/446** (« partir de l'écran », « vérifier l'affichage avant de mesurer »)
  sont des règles de **sélection à l'intérieur d'une famille**.
- **Celle-ci est une règle de SUCCESSION** : elle dit **quelle famille ouvrir
  ensuite**, et elle la déduit du défaut qu'on vient de trouver.

### La réserve, et elle est sérieuse

**Les quatre relais ont été proposés dans les orientations de réveil, pas
découverts par la boucle.** Je les ai exécutés et ils ont payé, mais je ne peux
pas m'attribuer la sélection. Ce que la tranche établit, c'est que **la règle
fonctionne quand on l'applique** — pas que la boucle sait la trouver seule.
L'échantillon est de quatre, et la chaîne pourrait devoir autant au hasard des
veines qu'à la méthode.

## Mes comptes d'erreurs, recomptés — et il y en a un troisième

**Arrêtés avant publication : 25 → 26.** Recompte sur la tranche : 453 (**+4** —
couverture 32→72, fenêtre contaminée, enveloppes `allSettled`, classe `\s`
franchissant la ligne), 454 (**+1** — le zéro faux du détecteur à une seule
forme), **459 (+1)**.

Le +1 du 459 est **d'un genre nouveau et je le justifie** : sur la première
grille, la mesure rendait « delta max 0,684 → branche inatteignable ». C'était
faux, et cela aurait **enterré un défaut réel**. L'instrument n'était pas
bogué — il était **trop étroit**. Cela satisfait la définition d'un faux arrêté
avant publication : un résultat faux, prêt à être publié, attrapé avant. **Je le
compte. Total : 26.**

**Publiés puis corrigés : 3, inchangé** (439→441, 442→443, 443→444). Aucun fait
publié dans cette tranche n'a dû être démenti.

**Un troisième compte s'impose, et je l'ouvre : interprétations retirées = 1.**
Au 458 j'avais rangé « LEAPS → AUTRE » parmi les divergences ; le 459 a montré
que la Constitution **n'a aucune catégorie entre 0,60 et 0,70** et que « AUTRE »
y est la seule réponse honnête. **Le fait publié restait vrai ; l'insinuation
était de trop.** Ce n'est ni un faux arrêté ni un faux publié — c'est une
troisième chose, et la confondre avec l'une des deux fausserait les deux.

**Bornages publiés dans la tranche : 3.** 453 borne le 452 (le contrat rompu est
un cas, pas un genre) · 458 borne le 457 (14 concordances contre 1) · 459
requalifie le 456 vers le haut. **Trois fois, un lot a réduit ou déplacé la
portée du précédent.**

## Ce que les dix rapports NE prouvent PAS

- **Aucune trouvaille constatée sur des données réelles.** `scan_state['rows']`,
  `['options_board']`, `['detail']`, `['portfolio']`, `['recommendations']` vides
  ou `None` pendant toute la tranche. Tous les bancs tournent sur des entrées
  **fabriquées**.
- **Aucun navigateur ouvert de toute la tranche.** Dix lots, zéro rendu observé.
  Les chaînes d'affichage sont établies sur les **octets servis**.
- **Plusieurs formatages sont reproduits, pas exécutés** — le classeur `catOf`
  (458, 459), les gabarits de fraction (456). Les trois comparaisons sont
  recopiées à l'identique, mais la page n'est pas exécutée.
- Les bancs établissent le **comportement du code**, jamais la **fréquence** des
  cas réels — vrai pour le plafond de 200 (456), la fenêtre 10-15 (457), la
  troncature à 30 (459).
- **La distribution réelle d'IV n'est pas bornée** (459) : la borne 0,781 est une
  propriété de **ma grille**, pas du produit.
- Les pourcentages d'étiquetage du 459 (73,3 % de l'espace put) décrivent un
  **espace de grille**, pas un usage observé.

## Classement coût/risque — mis à jour avec 452, 455, 456, 457, 458

Ordre **par coût et risque croissants**. Le rang de gravité est rappelé ; **il ne
dicte pas l'ordre**.

```text
#   dossier                        geste                                       surface        risque
1   457 borne V1 figée             lire d.bounds.max — DÉJÀ REÇU par la page   1 expression   très faible   rang 1
2   455 synthèse pré-trade         ajouter statuses.count(UNKNOWN)             1 ligne        très faible   rang 2
3   434 renderAnomalies            copier la garde écrite 20 lignes plus haut  3 lignes JS    très faible
4   427 légende multi-indices      bâtir la légende depuis `sets`              1 ligne JS     très faible
5   428 entonnoir de sélection     accepter les deux vocabulaires              2 lignes JS    très faible
6   437 « Catalyseurs imminents »  retirer `|| Date.now()` (3 pages)           3 lignes JS    très faible
7   456 titre « 200 titres »       dire le plafond, ou lever la troncature     1 chaîne       très faible   rang 2
8   448+449 trois vidages          journaliser, rendre un motif écrit          3 blocs except très faible
9   425 « 4 maturités réelles »    compte dynamique `${pts.length}`            2 chaînes      très faible
10  458 classeur `catOf`           ajouter le type au prédicat                 3 lignes JS    faible        rang 2
11  447 max pain multi-échéances   filtrer sur l'échéance la plus proche       1 filtre       faible        rang 1
12  432+433 synthèses /portfolio   conditionner sur `allMarked` DÉJÀ CALCULÉ   3 branches     faible
13  442+443 les trois R:R          afficher `rr_res` + nommer chaque référence 4 rendus       faible
14  452 collision de route         retirer la règle masquée OU lire les clés   1 règle        faible        rang 1
15  424 thesis_health              UNKNOWN quand les 2 listes sont vides       1 branche      faible
16  422 expected-move muet         l'ajouter à la liste de limites             1 chaîne       faible
```

Trois remarques mesurées :

**Le n°1 est le rang 1 le moins cher que la boucle ait jamais classé.** La page
**reçoit déjà** `d.bounds` du moteur et **affiche déjà** « 8-15 lignes cibles »
trois cartes plus bas ; il s'agit de remplacer un littéral par une valeur en
main.

**Les neuf premiers ne touchent aucun moteur.** Ils vivent dans six fichiers de
page ou de JS statique.

Les dossiers lourds (406/407/408/409/411, 388, 417, 416, 436, 391/396) ne sont
**pas** classés : ils demandent une **décision de produit**. **Aucun GO n'est
demandé, rien n'est engagé.**

## Portée de ce bilan

Il mesure ce que la tranche a **déposé** et ce que les dix rapports
**affirment**. Il ne rejoue rien : **si un rapport s'est trompé sur un fait qu'il
présente comme mesuré, ce bilan reprend l'erreur.**

Le classement des rangs est **attribué par moi-même** — ce n'est pas une métrique
indépendante, et le recompte du rendement en dépend directement. Je donne les
deux conventions plutôt qu'un chiffre unique.

**La seule mesure fraîche prise ici est celle des MD5 : 8/8 identiques.** Tout le
reste est relecture et arithmétique sur le dépôt.

## Où en est la boucle

Soixante-troisième lot court, **quinzième bilan**.

La tranche 450-459 est la première à **refermer deux veines** (les phrases
composées au 455, les fractions affichées au 457) et la première où **trois lots
bornent leur prédécesseur**. C'est une tranche qui se corrige elle-même plus
qu'elle ne s'étend — et le compte des erreurs le montre : **26 faux arrêtés, 0
faux publié, 1 interprétation retirée**.

Et c'est la **quinzième tranche à se terminer sans qu'un seul des défauts prouvés
ait été corrigé**. Le classement en compte désormais **seize**, dont **neuf à
moins de trois lignes et sans moteur**, et dont le premier — un rang 1 — se
corrige en remplaçant un littéral par une valeur que la page reçoit déjà.

## Orientation pour le 461

Trois voies, et je tranche sur pièces.

**(a) Continuer les lots de mesure**, en désignant la famille suivante par la
forme du dernier défaut trouvé — la chaîne 455→459 a payé quatre fois.

**(b) Un lot « devis »** : chiffrer le coût de correction exact des rang 1 les
moins chers (fichiers, lignes, gardiens à écrire), sans rien corriger, pour
rendre la décision humaine possible.

**(c) S'arrêter et attendre.**

Le critère posé était : **(b) si et seulement si la cadence des trouvailles
baisse ; sinon (a)**. Elle ne baisse pas — **les défauts affichés passent de 5 à
7**, et huit lots de mesure sur neuf ont trouvé quelque chose. **Je recommande
donc (a).**

**Et je dis ce qui plaide contre.** Si l'on ne regardait que le **rang 1**, la
réponse serait (b) : deux tranches de suite au plancher, et **quinze tranches
sans une seule correction**. Je suis le critère posé plutôt que mon intuition,
mais je pose la bascule à voix haute : **au premier bilan où les défauts affichés
reculeront, (b) devient la bonne réponse.**

**Sept bilans — n°9, n°10, n°11, n°12, n°13, n°14 et n°15 — attendent une
réponse.**
