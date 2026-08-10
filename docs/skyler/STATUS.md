# SKYLER V2 — EXECUTION STATUS

> Branche d’intégration : `integration/vertex-skyler-v2`  
> Base historique : `agent/vertex-neon-glass-graphs`  
> Statut : **Skyler V2 Core livré — phase Institutional+ ouverte**.

## BILAN — veille active, lots 490 → 499 (2026-08-10, bilan n°18)

Dix lots. Bilan **sur pièces** : les dix rapports relus, les chiffres vérifiés au
dépôt **et dans `git log`**, aucune trouvaille rejouée. Seule mesure fraîche :
les MD5. **Calibration : elle a arrêté ce lot DEUX FOIS** — motif sensible à la
casse (le 490 écrit « Arrêtés » en début de phrase), puis dernier nombre au lieu
du premier (le 499 écrit « 76 (+1) »). Sans elle, toute la série de ce bilan
aurait été fausse.

### Les chiffres

| | |
|---|---|
| suite | **2864 passed / 0 skipped** sur les dix |
| service worker | **`td-shell-v187`** sur les dix |
| MD5 des 8 pages | **8/8** déclaré dix fois, remesuré 8/8 aujourd'hui |
| production | **zéro fichier hors `docs/`** dans les dix commits — vérifié dans `git show --name-only` |
| gardiens | **zéro** ajouté |
| PR | **#522 (490) → #531 (499)** |

### Rendement : DEUX dossiers en dix lots

Feuille lue **dans les lignes d'index** : 480-482 **20** · 483 **21** ·
484-485 **23** · 486-489 **24** · 491-494 **24** · 495 **25** · 496-499 **26**.
**Tranche 480-489 : +4. Tranche 490-499 : +2. La production est divisée par
deux.** Les deux neufs : **495-A** (rang 1) et **496-A** (rang 2), plus la
**requalification du 442**.

### Auto-correction : de +3 à +1

« Publiés puis corrigés » : 480 **7** → 489 **10** ; 490 → 499 **11**. **Le taux
a baissé des deux tiers, et ce n'est pas nécessairement une amélioration** : la
tranche a publié moins de chiffres neufs. **Moins publier, c'est moins avoir à
corriger.**

### Faux arrêtés : +22, et la MOITIÉ sont mes propres instruments

479 **45** · 489 **54** · 499 **76** → tranche 480-489 **+9**, tranche 490-499
**+22**, taux **multiplié par 2,4**. Classement des 22 :

| | |
|---|---|
| **défaillance de mon instrument** | **11** — 490, 491, 492 ×2, 493 ×3, 496, 497 ×2, 498 |
| erreur de lecture du résultat | 10 — 491, 494 ×3, 495 ×2, 497 ×2, 498, 499 |
| sonde dangereuse évitée | 1 — 495 |

**Onze sur vingt-deux ne sont pas des faits sur le produit : ce sont des pannes
de mes propres bancs.** Un compteur qui monte n'est pas en soi une vertu — **il
mesure autant ma rigueur que ma maladresse.**

### Les règles de calibration servent-elles ? Un tiers

Sur les onze pannes : **3 attrapées par une calibration écrite d'avance** (493,
496, 498 — plus celle de ce lot), **8 attrapées en lisant la sortie**. Le **497**
est le contre-exemple : trois pannes, calibration muette — d'où la règle
« **témoin de CHARGE avant témoin de VARIÉTÉ** ».

### Fermer ou découvrir ? La boucle ferme

**4 veines closes** (493, 496, 498, 499) contre **1 ouverte** (495) et **5 lots
de bornage** (490, 491, 492, 494, 497). Travail réel — mais **une boucle qui
ferme quatre fois plus qu'elle n'ouvre approche la fin de ce qu'elle peut trouver
seule**.

### Le second contrôle : les chiffres du réveil

« feuille 24 → 26 » **confirmé** · « +21 » **faux, c'est +22** · « PR #521 →
#531 » : la plage propre à la tranche est **#522 → #531** · « 301 fichiers de
test » : **300** `test_*.py`, 301 `.py` avec `conftest.py`.

### Le stock

26 dossiers · quinze rang 1 · neuf rang 2 · trois rang 3 · dix lots A-J · 7 à
chiffrer · 7 arbitrages humains · 17+ observations · un devis de purge de 4 369
lignes. **Corrections engagées 0 · gardiens 0 · octets servis modifiés 0, sur
VINGT lots.** Je pose la question de la soutenabilité **sans y répondre à la
place de l'utilisateur**. Élément neuf : **le stock vieillit bien** — deux
dossiers ont été resserrés par des lots ultérieurs plutôt qu'abandonnés. **Il
reste inutilisable sans une décision.**

**Dix bilans — n°9 à n°18 — attendent une réponse.**

## BILAN — veille active, lots 480 → 489 (2026-08-09, bilan n°17)

Dix lots. Bilan fait **sur pièces** : les dix rapports relus, les chiffres
vérifiés dans le dépôt, **aucune trouvaille rejouée**. Seule mesure fraîche :
les MD5. Calibration écrite dans le code sur le compteur « publiés puis
corrigés » (487 = 10, 488 = 10) — les deux OK.

### Les chiffres

| | |
|---|---|
| suite | **2864 passed / 0 skipped** sur les dix, jamais rouge |
| service worker | **`td-shell-v187`** sur les dix |
| MD5 des 8 pages | **8/8** à chaque lot, remesuré 8/8 aujourd'hui |
| production touchée | **zéro fois** |
| gardiens ajoutés | **zéro** — aucun `tests/*lot48*`, total inchangé à 301 |
| PR | dix, **#512 → #521** (huit vérifiées au journal, #512 et #513 non re-vérifiées) |

### Le fil rouge — trois auto-corrections : force ou dérive ?

Incréments exacts du compteur : **469 · 471 · 477 · 479 · 481 · 485 · 487**.

```text
460-469 → 1        470-479 → 3        480-489 → 3
```

**Le taux n'a PAS monté entre les deux dernières tranches : il a plafonné.** Le
saut réel a eu lieu entre 460-469 et 470-479.

**La mesure confirme le 480** : il avait tranché que les révisions se groupent
dans les lots dont le travail est la **ré-examination**. Vérifié — les trois sont
**481** (ré-examen du 480), **485** (du 484), **487** (du 486), sans exception.

**Ce que je ne maquille pas** : 3 sur 10 = **30 % des lots corrigent un
prédécesseur**, contre 10 % avant. Le plateau est réel mais **haut**, et les
trois corrections portaient sur des **chiffres publiés** — 6 orphelins → 1,
plafond 35 → 29, rang 2 → rang 1.

### Le rendement, dit franchement

**Cinq lots ont mesuré la boucle** (480, 481, 482, 483, 488), **cinq le produit**
(484, 485, 486, 487, 489) — et sur ces cinq, **deux seulement ont trouvé du
neuf**. Défauts ajoutés : **484-A** (rang 1), **484-B** (rang 2), **486-A**
(rang 1 après le 487). **Dix lots pour trois défauts neufs.**

À sa décharge : les trois sont substantiels, et les cinq lots de vérification ont
**empêché trois publications fausses de survivre**.

### Ce que la tranche a coûté — question posée, pas tranchée

**0 correction engagée · 0 gardien · 0 octet servi modifié.** Feuille **20 → 24
dossiers (+4)**. Dettes : à chiffrer 6 · arbitrages humains 7 · observations non
classées 5 · barèmes non tracés 7 · rangs relatifs non re-vérifiés 8.

**La boucle produit des dossiers plus vite qu'elle n'en solde**, et n'en solde
aucun sans GO. **Est-ce soutenable ? Je pose la question et je ne réponds pas à
la place de l'utilisateur.** La valeur est réelle et mesurée — elle est
**entièrement immobilisée**.

### Deux chiffres du réveil corrigés

- « la feuille a grossi de **2** dossiers » → **FAUX, +4** (20 → 21 → 23 → 24).
- « PR **#513 → #521** » → **incomplet** : neuf numéros pour dix lots ; la
  tranche est **#512 → #521**, sous réserve des deux premières non re-vérifiées.

**Troisième réveil consécutif porteur d'une erreur factuelle** (480, 482, 490) :
**le brief est une source comme une autre et doit être vérifié comme telle.**

### Où va la boucle

Trois défauts et une méthode — et la méthode est devenue l'objet principal. Les
règles accumulées sont bonnes, toutes payées par une erreur réelle. **Mais une
boucle qui passe la moitié de son temps à s'auditer, qui ne peut rien corriger,
et dont la liste ne cesse de croître, a atteint la limite de ce qu'elle peut
apporter seule.** Ce n'est pas un échec : **il manque une décision.**

**Neuf bilans — n°9 à n°17 — attendent une réponse.**

## BILAN — veille active, lots 460 → 469 (2026-08-09, bilan n°16)

Dix lots. Bilan fait **sur pièces** : les dix rapports relus, les chiffres
vérifiés dans le dépôt, **aucune trouvaille rejouée**. Aucun serveur DEMO, aucun
moteur rouvert. **Une seule mesure fraîche — les MD5.**

### Ce que la tranche a déposé — mesuré

**Base résolue AVANT tout chiffre** (leçon 430/440/450/460, cinq fois payée) :
seul candidat « lot 459 » = `1b23377`, **ancêtre de la tête vérifié**, pas
supposé.

```text
base 1b23377 (lot 459) → tête c44ef80

commits                                    10
fichiers modifiés                          12
   docs/refactor/validation                11   (10 rapports + SKYLER-INDEX.md)
   docs/skyler                              1   (STATUS.md)
fichiers HORS docs/                          0
lignes                        +3 047 / −0        (addition pure)

terminal.py + vertex/** touchés               0 fichier
rapports / index / blocs STATUS          10/10, 10/10, 10/10
volume des dix rapports                 114 435 octets
MD5 des 8 pages remesurés                     8/8 identiques
SW                                      td-shell-v187

depuis 20a917f (lot 399) : 70 commits · 73 fichiers · 1 hors docs/ · 0 PRODUCTION
```

### Une correction de comptes que je publie contre mon propre réveil

L'orientation que j'avais rédigée au 469 annonçait « arrêtés avant publication
**32 → 40** ». **Faux sur deux points** : le départ était **26** (clôture du
bilan n°15), et l'énumération **omettait 465 et 467**.

```text
26 → 461 +3 → 29 → 462 +2 → 31 → 463 +1 → 32 → 464 +1 → 33 → 465 +1 → 34
   → 466 +3 → 37 → 467 +2 → 39 → 468 +1 → 40 → 469 +0 → 40      soit +14
```

La chaîne lot par lot est cohérente ; **c'est mon résumé qui ne l'était pas.**

### Ce que les dix lots ont produit

```text
460  BILAN n°15                                                          —
461  dominantRisk « aucun risque » dans 15-25 % · winnerRule type perdu  ✓ rang 2 + 3
462  phrases-seuil : 26/28 concordent — le 461 est un ACCIDENT ISOLÉ     ✗ bornage
463  gex_history journalise la démo 120 j sous « points réels »          ✓ rang 2
464  edge_ledger + 2 journaux sans provenance : le track record affiché  ✓ RANG 1
465  les deux dettes du 464 soldées — 0 nouvel accumulateur              ✗ bornage
466  28 orphelines sur 189 règles, publiées en INTERVALLE [22, 37]       ~ rang 4
467  l'intervalle RÉSOLU à 28 — 9 des 15 étaient des redirections        ✗ bornage
468  19 seuils concordants, 0 divergence neuve · 6 concepts sans loi     ~ rang 4
469  le board sélectionne SOUS le minimum absolu de la Constitution      ✓ rang 3

      1 rang 1 · 2 rang 2 · 2 rang 3 · 2 rang 4 · 6 lots sur 10 BORNENT
```

### Le rendement — et cette fois il baisse franchement

```text
                     rang 1 PAR LOT   PAR DOSSIER   DÉFAUTS AFFICHÉS
tranche 420 → 429          4               4               —
tranche 430 → 439          4               3               5
tranche 440 → 449          3               2               5
tranche 450 → 459          2               2               7
tranche 460 → 469          1               1               3      ← −4
```

**Les deux lectures vont dans le même sens pour la première fois depuis le
bilan n°12.** La tranche a consacré six lots sur dix à borner ou solder — c'est
sa qualité — **mais le critère porte sur le résultat, pas sur l'effort.**

### Le critère bascule, et je le suis

Le bilan n°15 écrivait : « **au premier bilan où les défauts affichés
reculeront, (b) devient la bonne réponse.** » **Ils reculent : 7 → 3.**

**Je recommande (b) : un lot DEVIS.** Première fois en sept bilans que la
recommandation change — **non parce que j'ai changé d'avis, mais parce que le
chiffre choisi d'avance a franchi le seuil fixé d'avance.**

### Le fait de méthode dominant, et il est dérangeant

**Dans huit des neuf lots de mesure, l'instrument était faux au premier jet** —
et la parade a changé de nature à chaque fois : le contrôle (461), la taille
(462), **la lecture de la liste** (463, 464, 466), **le contrôle lui-même faux**
(467), un chemin trop court (468), **une atteignabilité supposée** (469).
**Treize corrections d'instrument, deux erreurs de raisonnement.**

**La conclusion honnête n'est pas « la boucle s'améliore » : si l'instrument est
faux au premier jet presque à chaque fois, tout lot qui N'A PAS attrapé son
instrument est suspect.** Argument de plus pour (b) : **un devis se vérifie en le
lisant, une mesure ne se vérifie qu'en la refaisant.**

### L'atteignabilité — ce qu'elle a coûté

```text
462  « cible 1 »      inatteignable   VÉRIFIÉE    tient
465  alerte de démo   non servi       VÉRIFIÉE    tient
468  seuil DTE        « probable »    SUPPOSÉE    FAUX  (corrigé au 469)
```

**Deux sur trois mesurés, un supposé — et c'est celui-là qui était faux.** Le
filtre est excellent quand on le mesure, dangereux quand on l'invoque.

### Mes comptes

```text
arrêtés avant publication      26 → 40      +14
publiés puis corrigés           3 →  4       +1
interprétations retirées        1 →  2       +1
```

Le +1 de la deuxième ligne vient d'une phrase **hedgée et non classée**. Je
maintiens : *un lecteur qui repart avec une croyance fausse a été mal informé.*

### Classement coût/risque — 19 dossiers

Les cinq premiers : **457** borne V1 (rang 1, une expression) · **455** synthèse
pré-trade · **461** `dominantRisk` · **434** `renderAnomalies` · **427** légende.
Le **n°12** est le rang 1 le plus utile : **464**, passer `demo` à `record()` —
`DEMO_MODE` est **déjà en portée** et **`decision_memory` fait déjà exactement ce
qu'il faut**. **Les onze premiers ne touchent aucun moteur.** Les **trois
derniers** (469, 468, 466/467) **ne sont pas des correctifs** : ils demandent
qu'on **décide**.

### Portée

Le bilan reprend les erreurs des rapports s'il y en a — et la tranche vient de
démontrer que cela arrive. **Le classement des rangs est attribué par moi-même**
et le constat de baisse en dépend : en classant le DTE du 469 en rang 2, les
défauts affichés seraient **4 et non 3** — la conclusion tiendrait, moins
nettement. **Seule mesure fraîche : les MD5.**

### Orientation pour le 471

**(b) — le lot DEVIS.** Chiffrer sans rien corriger : fichier, ligne, nombre de
lignes, gardien à écrire, risque de régression ; et pour les trois dossiers qui
n'en sont pas, **la question à trancher**. **Ce qui plaide contre** : un devis ne
mesure rien de neuf, et quinze bilans n'ont pas obtenu une décision. **Mais
c'est le geste qui manque, et le seul jamais tenté.**

**Seizième tranche sans qu'un seul défaut prouvé ait été corrigé. Huit bilans —
n°9 à n°16 — attendent une réponse.**


## BILAN — veille active, lots 450 → 459 (2026-08-09, bilan n°15)

Dix lots. Bilan fait **sur pièces** : les dix rapports relus, les chiffres
vérifiés dans le dépôt, **aucune trouvaille rejouée**. Aucun serveur DEMO, aucun
moteur rouvert. **Une seule mesure fraîche — les MD5 — et elle est dite comme
telle.**

### Ce que la tranche a déposé — mesuré

**Base résolue explicitement avant tout chiffre** (leçon 430/440/450) :
`3fc9045` **est** le lot 449, `1b23377` **est** le lot 459, et l'intervalle donne
bien **dix commits** — vérifié avant publication.

```text
base 3fc9045 (lot 449 fusionné) → tête 1b23377 (lot 459 fusionné)

commits                                    10
fichiers modifiés                          12
   docs/refactor/validation                11   (10 rapports + SKYLER-INDEX.md)
   docs/skyler                              1   (STATUS.md)
fichiers HORS docs/                          0
lignes                        +2 893 / −0        (addition pure, rien supprimé)

terminal.py + vertex/** touchés               0 fichier
rapports / index / blocs STATUS          10/10, 10/10, 10/10
volume des dix rapports                 104 212 octets
MD5 des 8 pages remesurés                     8/8 identiques
SW enregistré                           td-shell-v187
```

### Une correction de référence que je publie : le SHA du lot 399 était faux

Les bilans précédents écrivaient « depuis le lot 399 (`29f4435`) ». **Mesuré :
`29f4435` n'est PAS un ancêtre de la tête** — c'est le commit côté branche,
remplacé par le squash `20a917f` (« Lot 399 … (#431) »), vrai point de fusion sur
l'intégration.

```text
depuis 20a917f : 60 commits · 63 fichiers
   HORS docs/     1   tests/test_skyler_sweep_x1.py   (lot 401)
   PRODUCTION     0   — AUCUN
```

**Le chiffre publié ne change pas** — 0 fichier de production, 1 hors `docs/` —
**mais la référence était fausse** et l'intervalle était calculé à travers un
point de fourche. Quatrième fois que « résoudre la base avant tout chiffre » paie.

### Ce que les dix lots ont produit

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
qu'il cite d'autres dossiers. Le tableau est relu **verdict par verdict**.

### Le rendement, recompté — et il faut deux lectures

```text
                        rang 1 PAR LOT      rang 1 PAR DOSSIER DISTINCT
tranche 420 → 429             4                        4
tranche 430 → 439             4                        3
tranche 440 → 449             3                        2
tranche 450 → 459             2                        2

DÉFAUTS AFFICHÉS (rang 1 + rang 2, par dossier distinct)
tranche 430 → 439     5
tranche 440 → 449     5
tranche 450 → 459     7      ← +2
```

**Le rang 1 reste au plancher : deux tranches de suite à 2.** Je ne l'enjolive
pas. Mais les cinq rang 2 de la tranche sont **distincts** — phrase
`/opportunities` (452), synthèse pré-trade (455), plafond de 200 (456),
`symbols_usable` plafonné (456 → requalifié au 459), classeur `catOf` (458).

**Lecture honnête : la cadence des rang 1 ne se redresse pas, mais le volume de
défauts affichés augmente.** La tranche a trouvé **plus** de choses fausses à
l'écran que les deux précédentes — simplement moins graves en moyenne.

### Le fait nouveau : une chaîne de relais — et je dis d'où elle vient

Cinq lots consécutifs se sont passé le relais **par la forme du défaut trouvé**,
non par le sujet :

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

C'est une règle **distincte** : **416** est une règle d'**arrêt**, **425/446**
sont des règles de **sélection à l'intérieur d'une famille**, celle-ci est une
règle de **SUCCESSION** — elle dit **quelle famille ouvrir ensuite**.

**La réserve, et elle est sérieuse : les quatre relais ont été proposés dans les
orientations de réveil, pas découverts par la boucle.** Je les ai exécutés et ils
ont payé, mais je ne peux pas m'attribuer la sélection. Ce que la tranche
établit, c'est que **la règle fonctionne quand on l'applique** — pas que la
boucle sait la trouver seule.

### Mes comptes d'erreurs, recomptés — et il y en a un troisième

**Arrêtés avant publication : 25 → 26.** Recompte sur la tranche : 453 (**+4**),
454 (**+1**), **459 (+1)**. Le +1 du 459 est d'un genre nouveau : sur la première
grille, la mesure rendait « delta max 0,684 → branche inatteignable ». C'était
faux, et cela aurait **enterré un défaut réel**. L'instrument n'était pas bogué —
il était **trop étroit**. **Je le compte. Total : 26.**

**Publiés puis corrigés : 3, inchangé.** Aucun fait publié dans cette tranche n'a
dû être démenti.

**Un troisième compte s'impose, et je l'ouvre : interprétations retirées = 1.**
Au 458 j'avais rangé « LEAPS → AUTRE » parmi les divergences ; le 459 a montré
que la Constitution **n'a aucune catégorie entre 0,60 et 0,70**. **Le fait publié
restait vrai ; l'insinuation était de trop.** Ce n'est ni un faux arrêté ni un
faux publié — c'est une troisième chose.

**Bornages publiés dans la tranche : 3** (453 borne le 452 · 458 borne le 457 ·
459 requalifie le 456 vers le haut).

### Ce que les dix rapports NE prouvent PAS

- **Aucune trouvaille constatée sur des données réelles** — tous les bancs sur
  entrées **fabriquées**.
- **Aucun navigateur ouvert de toute la tranche.** Dix lots, zéro rendu observé.
- **Plusieurs formatages sont reproduits, pas exécutés** (`catOf`, gabarits de
  fraction).
- Les bancs établissent le **comportement du code**, jamais la **fréquence** des
  cas réels.
- **La distribution réelle d'IV n'est pas bornée** : 0,781 est une propriété de
  **ma grille**, pas du produit.

### Classement coût/risque — 16 dossiers

Ordre **par coût et risque croissants** ; le rang de gravité est rappelé mais
**ne dicte pas l'ordre**.

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

**Le n°1 est le rang 1 le moins cher que la boucle ait jamais classé** : la page
**reçoit déjà** `d.bounds` et **affiche déjà** « 8-15 lignes cibles » trois
cartes plus bas. **Les neuf premiers ne touchent aucun moteur.** Les dossiers
lourds (406/407/408/409/411, 388, 417, 416, 436, 391/396) ne sont **pas**
classés : ils demandent une **décision de produit**. **Aucun GO n'est demandé,
rien n'est engagé.**

### Portée de ce bilan

Il mesure ce que la tranche a **déposé** et ce que les dix rapports
**affirment**. Il ne rejoue rien : **si un rapport s'est trompé sur un fait qu'il
présente comme mesuré, ce bilan reprend l'erreur.** Le classement des rangs est
**attribué par moi-même** — ce n'est pas une métrique indépendante. **La seule
mesure fraîche prise ici est celle des MD5 : 8/8 identiques.**

### Orientation pour le 461

Le critère posé était : **(b) un lot « devis » si et seulement si la cadence des
trouvailles baisse ; sinon (a) continuer les lots de mesure.** Elle ne baisse
pas — **les défauts affichés passent de 5 à 7** — **je recommande donc (a)**. Et
je dis ce qui plaide contre : si l'on ne regardait que le **rang 1**, la réponse
serait **(b)**, deux tranches au plancher et **quinze tranches sans une seule
correction**. **Au premier bilan où les défauts affichés reculeront, (b) devient
la bonne réponse.**

**Quinzième tranche à se terminer sans qu'un seul des défauts prouvés ait été
corrigé. Sept bilans — n°9 à n°15 — attendent une réponse.**


## BILAN — veille active, lots 440 → 449 (2026-08-09, bilan n°14)

Dix lots. Bilan fait **sur pièces** : les dix rapports relus, les chiffres
vérifiés dans le dépôt, **aucune trouvaille rejouée**. Aucun serveur DEMO, aucun
moteur rouvert. Une seule mesure fraîche — les MD5.

### Ce que la tranche a déposé — mesuré

**Base résolue explicitement avant tout chiffre** (leçon 430/440, deux fois
payée) : `d400bf2` **est** le lot 439, `3fc9045` **est** le lot 449, et
l'intervalle donne bien **dix commits** — vérifié avant publication.

```text
base d400bf2 (lot 439 fusionné) → tête 3fc9045 (lot 449 fusionné)

commits                                    10
fichiers modifiés                          12
   docs/refactor/validation                11   (10 rapports + SKYLER-INDEX.md)
   docs/skyler                              1   (STATUS.md)
fichiers HORS docs/                          0
lignes                        +2 552 / −0        (addition pure, rien supprimé)

terminal.py + vertex/** touchés               0 fichier
rapports / index / blocs STATUS          10/10, 10/10, 10/10
volume des dix rapports                  98 591 octets
MD5 des 8 pages remesurés                     8/8 identiques
```

Depuis le lot 399 : **1 fichier hors `docs/`** (`tests/test_skyler_sweep_x1.py`,
lot 401) et **0 fichier de production**.

### Ce que les dix lots ont produit

```text
440  BILAN n°13                                                          —
441  piste /analysis refermée · corpus incomplet · unité corrigée        ✗
442  « R:R structurel » constant à 3, rr_res invisible                   ✓ rang 1 (+ rang 2)
443  TROIS R:R contradictoires — aggrave le 442                          ✓ rang 1 (+ rang 4)
444  recensement AST de 235 phrases + CORRECTION publiée du 443          ✗
445  6 phrases de `basis` TOUTES EXACTES — première famille saine        ✗
446  horizon « séance +N » sur séances OBSERVÉES, non affiché            ~ rang 4
447  max pain multi-échéances, TEXTE VISIBLE sur /portfolio              ✓ rang 1
448  exception Python affichée comme motif sur /options                  ✓ rang 2
449  veine `reason` refermée 7/7 — le rang 2 du 448 TRIPLE               ✓

      3 rang 1 · 2 rang 2 · 4 rang 4 · 3 bornages · 3 corrections publiées
```

### Le fait nouveau : le tri par affichage

**Lecture A** — ce serait le **425 renommé** : « partir de l'écran » disait déjà
de commencer par le rendu.

**Lecture B** — c'est une **règle distincte et plus forte** : le 425 dit **où
chercher**, le 446 dit **s'il vaut la peine de dépenser la mesure**. Et la
différence se lit dans les résultats — aux lots **435, 436, 446**, la boucle a
mesuré entièrement puis découvert que personne n'affichait : **trois
rétrogradations au rang 4**. Aux lots **447, 448, 449**, l'ordre est inversé :
**trois lots productifs d'affilée**.

**Je tranche : règle distincte, la plus rentable depuis le 425.** Le 425 choisit
l'objet ; le 446 pose un **péage avant la dépense**.

**Réserve** : trois lots est un petit échantillon, et le rendement des 447-449
doit une part de son succès à **la carte du 444** — quels champs sont lus par
combien d'écrans. **La règle est bonne parce qu'une carte existait.**

### Le rendement, recompté — et il baisse

Recompté, pas hérité (leçon 440), et en **deux conventions**, car un même dossier
peut occuper deux lots :

```text
                        rang 1 PAR LOT      rang 1 PAR DOSSIER DISTINCT
tranche 420 → 429             4                     4     (422, 425, 427, 428)
tranche 430 → 439             4                     3     (432+433 = même famille)
tranche 440 → 449             3                     2     (442+443 = même famille ; 447)
```

**La cadence baisse dans les deux conventions — je ne l'enjolive pas.** Mais le
compte des **défauts affichés** (rang 1 + rang 2) **tient** : **5** au 430-439,
**5** au 440-449. **Le volume tient, la gravité moyenne descend** — deux des cinq
ne sont pas des mensonges (un message technique, une promesse de courbes).

### Mes deux comptes d'erreurs — dont un était trop flatteur

**Arrêtés avant publication : 20.** Recompté sur la tranche — 441 ×1, 443 ×3,
445 ×1, 446 ×1 = **+6**, de 14 à 20. Le chiffre hérité est **confirmé**.

**Publiés puis corrigés : 3, et non 1.** Le recompte dément le chiffre que je
transportais depuis le 444 :

```text
439  « 22 248 octets » pour /analysis      → CARACTÈRES, pas octets      corrigé au 441
442  « rr_res n'est affiché nulle part »   → visible en BLOCAGE < 2,0    corrigé au 443
443  « invalidation lu par 5 écrans »      → 2, et un AUTRE payload      corrigé au 444
     « stop_type atteint un écran »        → RETIRÉ
```

Je ne comptais que la troisième parce que le 444 l'avait nommée « la première
fois » — **c'était déjà la deuxième**. **Ce que l'écart signifie** : 20 contre 3,
un filtre qui retient **environ sept erreurs sur huit**. Et les trois qui sont
passées ont **toutes la même cause** — un chiffre ou une portée annoncés **sans
identifier le payload par sa forme**, la règle que le 448 a fini par écrire.

### Ce que les dix rapports NE prouvent PAS

- **Aucune trouvaille sur des données réelles** : scan, board et `detail` vides
  au démarrage pendant toute la tranche ; **tous les bancs sur entrées
  fabriquées**.
- **Aucun navigateur ouvert de toute la tranche.**
- **93 des 110 phrases concluantes du 444 restent fermées** — la carte est
  dressée, le territoire non.
- **Plusieurs formatages sont recopiés, pas exécutés** (443, 448, 449).
- Les bancs établissent le **comportement du code**, jamais la **fréquence** des
  cas réels (200 barres du 442, trous de log du 446, échéances du 447, entrées
  mal typées du 449).

### Classement coût/risque — mis à jour avec 442+443, 447, 448+449

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

**Les six premiers ne touchent aucun moteur** — cinq fichiers
(`opportunities_page.py`, `markets_page.py`, `briefing.py`,
`options_intel_api.py`, `options_lab_api.py`). **Le n°5 est le moins risqué du
lot** : trois blocs `except`, et **le modèle est déjà écrit dans
`horizon_scanners`, sur la même page**. **Le n°7 est le seul rang 1 de la tranche
dont la correction tient en un geste.** Les dossiers lourds (406/407/408/409/411,
388, 417, 416, 436) ne sont **pas** classés : décision de produit. **Aucun GO,
rien n'est engagé.**

**Portée** : ce bilan mesure ce que la tranche a déposé et ce que les rapports
affirment ; il ne rejoue rien — **si un rapport s'est trompé sur un fait présenté
comme mesuré, ce bilan reprend l'erreur**, et la tranche vient de montrer que
cela arrive. Le classement des rangs est **attribué par moi-même** : d'où les
deux conventions plutôt qu'un chiffre unique. Écart runtime final **aucun**.
Suite **2864 passed / 0 skipped**.

## BILAN — veille active, lots 430 → 439 (2026-08-09, bilan n°13)

Dix lots. Bilan fait **sur pièces** : les dix rapports relus, les chiffres
vérifiés dans le dépôt, **aucune trouvaille rejouée**. Aucun serveur DEMO, aucun
moteur rouvert. Une seule mesure fraîche a été prise — les MD5 — et elle est dite
comme telle.

### Ce que la tranche a déposé — mesuré

```text
base 1ac8446 (lot 429 fusionné) → tête d400bf2 (lot 439 fusionné)

commits                                    10
fichiers modifiés                          12
   docs/refactor/validation                11   (10 rapports + SKYLER-INDEX.md)
   docs/skyler                              1   (STATUS.md)
fichiers HORS docs/                          0
lignes                        +2 133 / −0        (addition pure, rien supprimé)

terminal.py + vertex/** touchés               0 fichier
rapports 430→439 présents                    10 / 10
lignes d'index 430→439                       10 / 10
blocs STATUS par lot 430→439                 10 / 10
volume des dix rapports                  80 011 octets
```

**La base a été résolue explicitement** (leçon du 430) : ma première tentative
prenait `e62fecb` comme base — mais `e62fecb` **est** le commit du lot 430, si
bien que l'intervalle ne couvrait que 431→439, **neuf commits**. Corrigé avant
publication. Contrôle refait depuis le lot 399 (`29f4435..d400bf2`) : **1 fichier
hors `docs/`** — `tests/test_skyler_sweep_x1.py`, lot 401 — et **0 fichier de
production**. **Aucun octet de production n'a changé depuis le lot 399.**

### Ce que les dix lots ont produit

```text
430  BILAN n°12 + correction d'une affirmation que je répétais           —
431  modeOf ne peut jamais rendre « Live » — J'ANNULE MON PROPRE RANG 1  ✗ rang 4
432  priorityAction range l'INCONNU avec le SAIN                         ✓ rang 1
433  bornage AGGRAVANT — les trois synthèses de /portfolio tombent       ✓ rang 1
434  renderAnomalies sans la garde écrite VINGT LIGNES PLUS HAUT         ✓ rang 1
435  la décision du jour, calculée sur zéro titre — et jamais lue        ~ rang 4 (+ rang 2)
436  /api/command : 2 champs lus sur 10, et la suite défend le reste     ~ rang 3
437  « Catalyseurs imminents » se déclare fraîche « à l'instant », TOUJOURS ✓ rang 1
438  bornage NÉGATIF — six contrats rompus, six faux positifs            ✗
439  trois pages ouvertes, aucun défaut nouveau, une métrique abandonnée ✗

      4 trouvailles de rang 1 · 1 de rang 2 · 1 de rang 3 · 2 de rang 4
      3 bornages (1 aggravant, 2 négatifs) · 1 annulation de soi-même · 1 bilan
```

### Le fait nouveau : quatorze instruments jetés en six lots

```text
430   git diff comparant la tête à elle-même (base vide)                        1
434   détecteur de garde v1 (page entière) puis v2 (mauvaise fonction)          2
435   motif sans DOTALL → « 0 appel » là où il y en a 16                        1
437   passe 1 (motif large) · passe 2 (0/4 invraisemblable) · passe 3 (bouillie) 3
438   trois lignes fausses issues d'une collision de noms de payloads           3
439   compteur de contrat de carte, v1 → v4, métrique abandonnée                4
                                                                             ─────
                                                                               14
```

**Tous arrêtés avant publication**, par trois contrôles seulement : **témoin
positif**, **invraisemblance**, **lecture de la sortie brute**.

**Et le chiffre-titre lui-même n'est pas homogène — je le corrige.** Sur les lots
437 et 439 l'unité comptée est une **version d'instrument écartée** ; sur le 438,
c'est une **ligne fausse produite par un seul et même instrument**. Par version :
**12**. Par résultat faux produit : **14**. Le « quatorze » publié au 439 mélange
les deux — il n'est faux dans aucune des deux conventions, il est **inconstant**.
Convention retenue pour la suite : **résultat faux produit, donc 14**. C'est la
règle du 437 (*ne jamais publier un total dont les lignes ne se comptent pas de la
même façon*) appliquée à ma propre comptabilité.

### Durcissement ou rendement décroissant — les deux lectures, puis la réponse

**Rendement décroissant** : quatorze instruments jetés en six lots, c'est plus
d'effort dépensé à se contrôler qu'à mesurer le produit ; deux des trois derniers
lots ne rendent **aucun défaut nouveau**, et le 439 finit sur un aveu.

**Méthode qui se durcit** : les quatorze ont **tous** été arrêtés **avant**
publication, par des contrôles qui coûtent quelques secondes. Et les questions ont
changé de nature — jusqu'au 433 la boucle lisait **une fonction** ; à partir du 434
elle balaie **3 829 722 octets servis**. Un balayage de corpus casse plus souvent
qu'une lecture de fonction : c'est attendu, pas dégradé.

**Ce qui tranche — le rendement, lui, n'a pas bougé :**

```text
tranche 420 → 429     4 trouvailles de rang 1 sur 10 lots
tranche 430 → 439     4 trouvailles de rang 1 sur 10 lots
```

**Identique**, et les quatre de cette tranche sont prouvées sur les octets servis,
dont une (437) affichée sur **trois pages** à la fois. **Réponse : durcissement,
pas rendement décroissant.** Le nombre d'instruments jetés monte parce que **la
portée des questions monte**, pas parce que les trouvailles se raréfient.

**Deux réserves.** *(1)* Le « quatorze en six lots » est **en partie un artefact
de comptage** : la boucle ne journalisait pas ses instruments écartés avant le 434.
On ne conclut pas à une **tendance** depuis une série qui commence quand on se met
à compter — des instruments fautifs, il y en avait avant (414, 415, 429), mais je
**n'ai pas** de recomptage rétrospectif à coût égal et je ne le fabrique pas.
*(2)* Cette lecture juge la boucle sur ce qu'elle **trouve**, pas sur ce qu'elle
**change** ; sur ce second critère le rendement est **nul depuis treize bilans**.

### Ce que les dix rapports NE prouvent PAS

- **Aucune trouvaille constatée sur des données réelles** : les lots 435 à 439
  mesurent tous **sur le scan vide du démarrage**. Le 438 l'a payé — deux de ses
  six faux positifs venaient de là.
- **Aucun navigateur ouvert** de toute la tranche ; rendus SVG non exécutés.
- **Vivier très peu ouvert** : 118 affirmations recensées, 47 phrases triées au
  433, **35 de `/options` recensées non vérifiées** ; phrases dynamiques toujours
  hors recensement.
- **Cinq routes sur huit non conclues** au test de consommation (437).
- **Aucun taux de couverture du contrat de carte** (439) — la métrique elle-même
  est mal définie, et c'est un aveu.

**Une limite du n°12 est levée** : il y listait « MD5 non remesurés — leur
constance est une **inférence** ». Les neuf rapports 431→439 les remesurent, et
je les ai remesurés pour ce bilan : **8/8 identiques**. C'est désormais **une
mesure**.

### Classement coût/risque — mis à jour avec 432+433, 434 et 437

Ordre **par coût et risque croissants**, comme au 430.

```text
#  dossier                          geste                                      surface        risque
1  434 renderAnomalies              copier la garde écrite 20 lignes plus haut 3 lignes JS    très faible
2  427 légende multi-indices        bâtir la légende depuis `sets`             1 ligne JS     très faible
3  428 entonnoir de sélection       accepter les deux vocabulaires             2 lignes JS    très faible
4  437 « Catalyseurs imminents »    retirer `|| Date.now()` (3 pages)          3 lignes JS    très faible
5  425 « 4 maturités réelles »      compte dynamique `${pts.length}`           2 chaînes      très faible
6  432+433 synthèses /portfolio     conditionner sur `allMarked` DÉJÀ CALCULÉ  3 branches     faible
7  424 thesis_health                UNKNOWN quand les 2 listes sont vides      1 branche      faible
8  422 expected-move muet           l'ajouter à la liste de limites            1 chaîne       faible
```

**Les six premiers ne touchent aucun moteur** — quatre fichiers de page
(`markets_page.py`, `opportunities_page.py`, `briefing.py`, `portfolio_page.py`) :
**un seul lot, un seul bump de service worker, une seule preuve navigateur**
suffiraient. Le **n°1 a son propre modèle dans son propre fichier** (la garde est
écrite vingt lignes plus haut, dans `renderRadar`) ; le **n°6 n'invente rien non
plus** — `allMarked` est déjà calculé, il sert une couleur et jamais une phrase.
Les dossiers lourds (406/407/408/409/411, 388, 417, 416, 436) ne sont **pas**
classés : ils demandent une **décision de produit**. **Aucun GO, rien n'est
engagé.**

**Portée** : ce bilan mesure ce que la tranche a déposé et ce que les dix rapports
affirment ; il ne rejoue rien — **si un rapport s'est trompé sur un fait qu'il
présente comme mesuré, ce bilan reprend l'erreur**. La comparaison de rendement
porte sur un **classement que j'attribue moi-même**, pas une métrique
indépendante : le 431 montre qu'il bouge. Écart runtime final **aucun**. Suite
**2864 passed / 0 skipped**.

## BILAN — veille active, lots 420 → 429 (2026-08-09, bilan n°12)

Dix lots. Bilan fait **sur pièces** : les dix rapports relus, les chiffres
vérifiés dans le dépôt, **aucune trouvaille rejouée**. Aucun serveur DEMO, aucun
moteur rouvert, aucun nouveau point de contrôle.

### Ce que la tranche a déposé — mesuré

```text
base 0676d78 (lot 419 fusionné) → tête 1ac8446 (lot 429 fusionné)

commits                                    10
fichiers modifiés                          12
   docs/refactor/validation                11   (10 rapports + SKYLER-INDEX.md)
   docs/skyler                              1   (STATUS.md)
fichiers HORS docs/                          0
lignes                        +2 231 / −0        (addition pure, rien supprimé)

terminal.py + vertex/** touchés               0 fichier
rapports 420→429 présents                    10 / 10
lignes d'index 420→429                       10 / 10
volume des dix rapports                  78 145 octets
```

### Une correction sur une affirmation que je répétais

La consigne de boucle porte depuis plusieurs lots la phrase « la production n'a
pas bougé depuis le lot 399 ». **Vérifiée : vraie sur le fond, fausse à la
lettre.** Entre le lot 399 (`29f4435`) et la tête : **31 commits**, **1 fichier
hors `docs/`** — `tests/test_skyler_sweep_x1.py`, corrigé au **lot 401** (un
gardien qui passait selon l'ordre d'exécution) — et **0 fichier de production**.
Formulation exacte substituée : **aucun octet de production n'a changé depuis le
lot 399**.

**Et comment je l'ai su** : ma première commande a rendu « aucun fichier », ce
qui confirmait commodément l'affirmation. Elle était **fausse** — le
`git log --grep` n'avait rien trouvé, la variable de base était vide, et
`git diff ..HEAD` comparait la tête à elle-même. *Une commande peut rendre une
ligne propre, alignée et fausse* (leçon 415). Contrôle refait avec le commit
résolu explicitement.

### Ce que les dix lots ont produit

```text
420  BILAN n°11 (tranche 410 → 419)
421  scoring.compose — hypothèse d'inversion RÉFUTÉE par la mesure          ✗
422  scenario_pricer — repli MUET de l'expected-move, absent des limites     ✓ rang 1
423  committee — « $None (structure) », chaîne remontée → inatteignable      ✗ rang 4
424  thesis_health — INTACT avec confiance 0.0, affichage NON PROUVÉ         ~ rang 2
425  « 4 maturités réelles » en dur, courbe tracée dès 2 points              ✓ rang 1
426  bornage — 6 affirmations de méthode sur 6 EXACTES                       ✗
427  vivier 17 → 118 ; légende multi-indices sur liste fixe                  ✓ rang 1
428  entonnoir de sélection PLAT PAR CONSTRUCTION                            ✓ rang 1
429  bornage — trois vocabulaires légitimes, 13 porteurs exacts sur 14       ✗

      4 trouvailles de rang 1 · 1 de rang 2 · 1 de rang 4
      3 bornages négatifs · 1 hypothèse réfutée · 1 bilan
```

### Trois acquis de méthode, qui comptent plus que le compte

**(1) Partir de l'écran** (425) : trois lots partis du moteur butaient sur des
branches inatteignables ; renverser l'ordre a produit une trouvaille en une seule
mesure. **(2) Exécuter les octets servis** (427/428) : extraction par appariement
d'accolades + Node — ce qui a permis d'affirmer « 60 → 60 → 60 → 0 quel que soit
le marché » comme une **mesure**. **(3) Le recensement lui-même peut être la
limite** (427) : le vivier était sept fois plus grand qu'annoncé.

### Ce que les dix rapports NE prouvent PAS

- **Aucune trouvaille constatée sur des données réelles** — scan et board vides
  au démarrage, aucun payload persisté avec `rows` ni `indices`. Les défauts sont
  démontrés par construction ou par exécution sur payloads fabriqués, avec leur
  porte d'entrée établie.
- **Aucun navigateur ouvert** ; rendus SVG non exécutés (valeurs passées aux
  graphiques, pas pixels).
- **116 des 118 affirmations rendues non vérifiées** ; phrases dynamiques
  toujours hors recensement.
- **MD5 des 8 pages non remesurés** depuis les lots 390/396 : leur constance est
  une **inférence**, pas une mesure fraîche.
- Le « 13 sur 14 » du 429 ne vaut que pour les vocabulaires MAJUSCULES comparés
  explicitement.

### La question, et un classement coût/risque

La boucle mesure de mieux en mieux et **ne corrige rien**. Les bilans n°9, n°10
et n°11 posaient déjà cette question et **ne sont pas reformulés ici** — s'y
reporter. Ce qui a changé depuis le n°11 : il y avait deux chiffres faux
affichés, il y a maintenant **quatre familles de défauts prouvés à l'écran**,
dont deux qui **égarent activement la lecture** — une carte qui explique comment
lire une platitude qu'elle fabrique, une légende qui nomme une courbe par le nom
d'une autre.

Options inchangées : **(a)** continuer à mesurer · **(b)** GO sur les rang 1 les
moins coûteux · **(c)** arrêter la boucle et attendre.

```text
#  dossier                     geste                                    surface       risque
1  427 légende multi-indices   bâtir la légende depuis `sets`           1 ligne JS    très faible
2  428 entonnoir               accepter les deux vocabulaires           2 lignes JS   très faible
3  425 « 4 maturités »         compte dynamique `${pts.length}`         2 chaînes     très faible
4  424 thesis_health           UNKNOWN quand les 2 listes sont vides    1 branche     faible
5  422 expected-move muet      l'ajouter à la liste de limites          1 chaîne      faible
```

**Les trois premiers touchent le MÊME fichier** (`vertex/ui/pages/markets_page.py`)
et **aucun moteur** : un seul lot, un seul bump de service worker, une seule
preuve navigateur. Les dossiers plus lourds (406/407/408/409/411, 388, 417, 416)
ne sont **pas** classés ici : ils demandent une décision de produit.

**Portée** : ce bilan mesure ce que la tranche a déposé dans le dépôt et ce que
les dix rapports affirment ; il ne rejoue pas les trouvailles. Écart runtime
final **aucun**. Suite **2864 passed / 0 skipped**.

## BILAN — veille active, lots 410 → 419 (2026-08-09, bilan n°11)

Dix lots. Bilan **sur pièces** : les dix rapports relus, les chiffres re-mesurés
dans le dépôt. Serveur DEMO non lancé.

**La tranche a deux moitiés nettes.**

```text
410        bilan n°10
411 → 415  LES OCTETS SERVIS   provenances · cache SW · chemins client
                               · boutons · identifiants dupliqués
416 → 419  LES MOTEURS         RSI · track_record · multiplicateur · bornage
```

**Première moitié — produit sain, filet court.** Zéro défaut produit sur cinq
contrôles : 59 provenances dont 25 littéraux exacts (411) · 156 chemins client,
aucun mort (413) · 167 boutons servis, aucun sans écouteur (414) · 288
identifiants, aucun doublon (415). Mais **trois fois sur cinq, le gardien censé
protéger l'invariant s'arrête avant la fin** : le 412 **détecte sans imposer**, le
414 couvre **149 boutons sur 167**, le 415 visite **3 pages sur 8**.

**Seconde moitié — quatre lots, quatre trouvailles** : RSI = 100 sur série plate
(416) · `track_record`, le N affiché n'est pas le N du calcul, jusqu'à une seule
observation (417) · multiplicateur d'option assumé à 100 et `MULTIPLIER_INVALID`
mort deux fois (418) · bornage — 4 sites de détection sur 22 replis, et un **RSI
de 0 effacé** (419).

**Le fait le plus important : le changement de famille a payé immédiatement.**

```text
veine « octets servis »   5 lots   0 défaut produit, 3 filets courts
veine « moteurs »         4 lots   4 défauts produit
```

La note de cadence du 416 — *si le lot rend une quatrième fois « produit sain,
gardien à périmètre court », changer de famille* — était **le bon appel**, et la
décision est **reproductible : quand trois lots d'affilée rendent le même
diagnostic de forme, changer de famille.**

**Le motif technique, vérifié quatre fois** : la bonne pratique est écrite **à
quelques lignes du défaut** — 416 `pos = 50.0` quand `hi == lo`, trois lignes plus
bas · 417 `tp1_resolved` dans le même dictionnaire · 418 le `is None` explicite de
`quantity`, deux lignes plus haut · 419 le `is not None` du coût moyen, quatre
lignes plus haut. Le défaut n'est jamais l'ignorance de la règle : c'est son
**application incomplète**. *Chercher la règle que le fichier respecte ailleurs,
puis l'endroit où il l'oublie* — méthode la plus rentable depuis le lot 398, et
désormais formulable comme une **procédure**.

**Le résultat le plus parlant — deux fautes opposées sur le même indicateur :**

```text
416   RSI FABRIQUÉ à 100   série plate → 0/0 indéfini, rendu comme l'extrême
419   RSI EFFACÉ à 0       `float(d.get('rsi') or 50)` → 0.0 est falsy → neutre 50
```

Une seule cause : **traiter une valeur extrême légitime comme une donnée
manquante**. Dans un cas on invente, dans l'autre on gomme, et les deux se lisent
comme des mesures.

**Les gravités, distinguées et non gonflées** : un NOMBRE FAUX (407, hors
tranche) ≠ un ÉCHANTILLON MAL PRÉSENTÉ (417) ≠ une HYPOTHÈSE DOCUMENTÉE NON
VÉRIFIÉE (418) ≠ un TEXTE D'EXPLICATION INCOMPLET (419). **Trois lots ont resserré
leur propre diagnostic quand la mesure les contredisait** (416, 418, 419).

**L'instrument pris en défaut : 7 fois sur 10 lots**, toujours attrapé **avant
publication** — 413 deux fois (`/static` hors corpus ; `fetch(` sans ses
enveloppes), 414 deux fois (55 faux « boutons morts » ; 231 comptés au lieu de
167), 415 deux fois (heuristique de proximité 9→1 ; test d'englobement rendant
des lignes propres, alignées et fausses), 417 une fois. **La leçon des enveloppes
a été refaite trois fois — 409 `emptyCard`, 413 `get(…)`, 414 `$(…)` :** une règle
écrite ne suffit pas, c'est le témoin qui l'attrape ; la parade est structurelle
— exiger la **proximité** d'un accesseur quelconque.

**Ce qui n'a pas bougé, mesuré :**

```console
$ git diff --name-only bbd5f86..HEAD | grep -v '^docs/'
  (aucun)
```

| | |
|---|---|
| Fichiers de production modifiés | **0** |
| Fichiers de test modifiés | **0** (la tranche précédente en avait 1) |
| Tests ajoutés | **0** — délibérément |
| Suite | **2 864 / 0 skipped**, identique aux dix lots |
| PR | **#442 → #451**, toutes fusionnées en squash |
| Service worker | `td-shell-v187`, servi et enregistré, inchangé |

MD5 des 8 pages : prouvé aux lots **390** et **396**, **pas re-mesuré depuis** —
aucun octet de production n'ayant bougé, il est réputé inchangé : **inférence,
pas mesure fraîche.**

**La question, plus pressante qu'au bilan n°10.** Le rang 1 contient maintenant
**six dossiers**, dont **deux chiffres faux affichés comme réels** : HHI d'un
facteur 170 avec alerte fabriquée (407) et RSI = 100 sur un titre immobile (416) ;
plus la consigne impossible (406/409), l'échantillon mal présenté sur la page qui
parle de confiance (417), les 7 points MSFT fabriqués (388) et les replis `0`
(378). **Aucun GO n'est arrivé depuis le lot 388 — trente-deux lots.**

- **(a)** continuer les lots courts. La veine des moteurs paie encore (4/4) — mais
  elle produit des **constats**, pas des corrections.
- **(b) GO groupé sur le rang 1, puis exécution. ← recommandé.** Purge des 7
  points MSFT (coût et risque quasi nuls), puis `myCapital`, puis le RSI (deux
  lignes, deux moteurs).
- **(c)** arrêter la boucle et attendre. Défendable : rien ne se dégrade, la
  production n'a pas bougé depuis le lot 399.

Les bilans n°9 et n°10 posaient déjà cette question et **ne sont pas reformulés
ici** — s'y reporter. La seule chose qui a changé depuis le n°10 et qui compte :
**il y a désormais deux chiffres faux affichés, pas un.**

**Portée** : ce bilan mesure ce que la tranche a **déposé dans le dépôt** et ce
que les dix rapports affirment ; il ne rejoue pas les trouvailles une à une.
Aucun serveur DEMO lancé, aucun moteur rouvert. Écart runtime final **aucun**.

## BILAN — veille active, lots 400 → 409 (2026-08-09, bilan n°10)

Dix lots. Bilan fait **sur pièces** : les dix rapports relus, les chiffres
re-mesurés dans le dépôt.

**Cette tranche n'est pas la précédente.** Le bilan n°9 disait de la 390-399
qu'« elle n'a rien construit ». Celle-ci a **trouvé deux défauts visibles par
l'utilisateur**, puis les a **bornés**.

```text
lots ayant TROUVÉ un défaut             3   (401, 406, 407)
lots ayant BORNÉ une trouvaille         3   (402, 408, 409)
lots revenus NÉGATIFS                   3   (403, 404, 405)
bilan                                   1   (400)
──────────────────────────────────────────
lots ayant modifié la PRODUCTION        0     ← mesuré
```

Un seul fichier non documentaire modifié en dix lots :
`tests/test_skyler_sweep_x1.py`, le correctif du 401.

| | |
|---|---|
| Suite | **2 864 / 0 skipped**, identique aux 10 lots |
| Tests ajoutés | **0** — délibérément (tranche précédente : +29) |
| PR | **#432 → #441**, toutes fusionnées en squash |
| Service worker | `td-shell-v187`, inchangé |

**Les trois trouvailles.** **401** — `test_sweep_route_and_no_journaling`
restaurait avec `if v is None: scan_state.pop(k)` ; or `market_ctx` est
initialisée à `None`, donc la clé **existe** et sa valeur légitime **est**
`None` : la remise en état la **supprimait** du dict partagé, et le gardien des
8 clés documentées tombait selon l'ordre d'exécution (repro à **deux fichiers**).
**406** — sur les 17 clés du contrat `DESK_KEYS`, **7 n'ont aucun écrivain** ;
deux sont **lues par `/portfolio`** (`myTradesEquity`, `myCapital`) → **courbe
d'équité et drawdown jamais affichables**, et l'état vide promet « *elle se
construit au fil des clôtures* » alors que clôturer n'écrit jamais cette clé.
Piège évité : élaguer `DESK_KEYS` serait une **perte de données** (last-writer-wins
total, mécanisme du 362). **407** — `cash: E().capital() || 0` envoyé avec
`simulated: false`, donc **déclaré réel** : `hhi` **0.5003 contre 0.0029** avec
un cash réel, **un facteur 170** ; et avec **une seule position** HHI = **1.0**,
donc le terminal affiche « **Concentration très élevée** » là où un portefeuille
réel n'aurait aucune alerte. Trois lignes plus bas, le fichier écrit la règle
qu'il enfreint : *« Manquant/insuffisant n'est jamais présenté comme zéro. »*

**Les trois bornages — aussi utiles que les trouvailles.** Savoir si un défaut
est isolé ou général **change la décision** :

```text
402   dépendance d'ordre     300 / 300 fichiers verts en isolation   → 401 était la seule
408   `|| 0` fautif          1 sur 25 charges utiles POST            → 407 est isolé
409   consigne impossible    1 sur 12 promesses (sur 88 états vides) → 406 est unique
```

Sans eux, la correction aurait pu passer pour une campagne. **Ce n'en est pas
une : une cause, un site, une carte.**

**Les trois lots négatifs** — 403 (2 tests sans assertion sur 2 563, tous deux
légitimes), 404 (0 assertion avalée sur 91 candidates), 405 (0 asset mort sur 54)
— sont des **résultats**, pas des échecs : dénominateur mesuré, instrument
prouvé. Mais ils **coûtent**, et leur rendement décroît ; trois d'affilée avaient
justifié de le dire au 405.

**LE POINT PRINCIPAL DE LA TRANCHE.** **L'instrument — ou son interprétation — a
été pris en défaut dans 6 lots sur 10**, dont **deux fois dans le même** (401),
et **chaque fois avant publication** :

```text
400   un `cd` oublié → j'ai cru six commandes durant que CLAUDE.md avait disparu
401   hook pytest mesurant AVANT les finalizers → 84 « fuites » dont 42 fausses
401   témoin `monkeypatch` écrivant une valeur DÉJÀ présente → idempotent, muet à tort
402   `nohup … &` → deux passes concurrentes, 195 fichiers couverts sur 300 annoncés
406   fichier exclu pour ce qu'il DÉCLARE → « 13 clés sans écrivain », dont `myTrades`
408   vivier trié par la FORME (53) pris pour une liste → le 1ᵉʳ candidat ouvert est sain
409   compter la DÉFINITION d'une aide au lieu de ses APPELS → le site du 406 introuvable
```

Ce n'est pas que la méthode soit mauvaise : c'est que **le contrôle de
l'instrument est la partie du travail qui rapporte le plus**. Chacune de ces
erreurs aurait produit un rapport faux, présenté avec les mêmes tableaux et la
même assurance.

**L'état du produit n'a pas bougé** : aucun fichier de production modifié sur la
tranche. Le MD5 des 8 pages a été re-prouvé identique aux lots **390** et
**396**, et **pas re-mesuré depuis** — c'est une inférence, pas une mesure
fraîche, et c'est écrit comme telle.

**LA QUESTION, PLUS COURTE QUE CELLE DU BILAN n°9.** Le rang 1 ne contient plus
seulement des inexactitudes discrètes. Il contient **un chiffre FAUX affiché
comme RÉEL** (HHI ×170, alerte de concentration fabriquée dès une seule
position), **une consigne que le trader ne peut pas suivre**, et depuis le 388
**7 points MSFT fabriqués** servis comme des mesures. La correction est **bornée
et petite** — une cause (`myCapital` jamais écrit), un site
(`portfolio_page.py:718`), une carte — et les lots 408 et 409 l'ont vérifié
exprès pour que la décision soit facile.
**Aucun GO depuis le lot 388 : vingt-deux lots.**
**(a)** continuer les lots courts — rendement décroissant, mesuré ;
**(b) GO groupé sur le rang 1, puis exécution — RECOMMANDÉ**, en commençant par
la purge des 7 points MSFT puis `myCapital` ;
**(c)** arrêter la boucle et attendre — défendable, rien ne se dégrade.
Ce qui ne serait pas honnête : continuer en (a) en laissant croire que le travail
avance sur ce qui compte. **Depuis le 406, il ne s'agit plus d'hygiène — un
chiffre faux est affiché comme réel.**

## BILAN — veille active, lots 390 → 399 (2026-08-09, bilan n°9)

Dix lots. Bilan fait **sur pièces** : les dix rapports relus, les chiffres
re-mesurés dans le dépôt, rien repris de mémoire.

**Ce qu'est cette tranche, sans enjoliver : elle n'a rien construit.** Elle a
vérifié, mesuré, et réparé quelques défauts de son propre outillage.

```text
lots ayant ajouté un gardien            3   (391, 392, 393 — 27 tests)
lots ayant réparé un fichier de test    3   (394, 398, 399)
lots n'ayant produit qu'une ligne       2   (390 bilan, 397)
lots n'ayant touché aucun fichier       2   (395, 396)
──────────────────────────────────────────
lots ayant modifié la PRODUCTION        0     ← mesuré, pas affirmé
```

| | |
|---|---|
| Suite | **2 835 / 2 skipped → 2 864 / 0 skipped** (+29, −2 skips) |
| Tests ajoutés | 27 gardiens + 2 réveillés = **29** — exactement le delta |
| PR | #422 → #431, toutes fusionnées en squash |
| Service worker | `td-shell-v187`, **inchangé sur les 10 lots** |
| `main` | jamais touchée |

Tranche précédente : **+81** tests. Le rythme est divisé par près de trois —
cohérent avec une tranche de vérification, et dit plutôt que caché.

**Les six trouvailles réelles.** **391** — un scan de DÉMO écrit dans
`breadth_history.json` : 16 points strictement identiques, site d'écriture
**inconditionnel** qui **écrase** le point du jour, servi sur `/markets` comme
« historique breadth RÉEL », et le point persisté ne porte **aucune provenance**
alors que `market_context_last.json` en porte une (reproduit au 396). **392** —
l'angle mort du 377 est **propre** : 30 routes, 12 refus, 12 motivés, 0 muet ;
et une sonde a **créé** un 22ᵉ fichier runtime. **394** — une docstring
**fausse** dans le gardien historique des clés desk, périmée depuis le lot 381.
**397** — un chiffre affirmé dans l'index **sans source** dans le rapport, que
rien d'autre n'aurait révélé. **398** — deux tests **morts depuis leur
création**, réveillés après preuve par mutation ; suite passée à **0 skipped**.
**399** — un test écrivait `desc_cache.json` **à la racine du dépôt de
l'utilisateur** ; doublement invisible, car le réseau échoue ici **et** parce que
l'écriture est conditionnée à la RÉUSSITE du fetch ; + un 23ᵉ fichier runtime
identifié (`constituents_cache.json`, gitignoré, vérifié).

**Six veines closes par la mesure** (392, 393, 394, 395, 396, 397). Une veine
close est un résultat honnête — **ce n'est pas une livraison.**

**Les leçons de méthode portent toutes sur l'INSTRUMENT, pas sur le code
mesuré** — c'est le motif dominant de la tranche : compter les occurrences avant
de muter (391) · un dénominateur non trié exagère le trou — 393 « angles morts »
dont 359 sont des aides internes (392) · quand un rapport réclame « un analyseur
d'un autre ordre », demander d'abord si l'**exécution** tranche (393) · *une
ancre absente n'est pas un résultat* (394) · *un énoncé faux se corrige
immédiatement là où c'est gratuit, et se verse aux dossiers là où cela coûte au
produit* (395) · *un détecteur qui ne connaît qu'UNE forme du document cherché
fabrique de faux manquants* (397) · *une écriture conditionnelle au réseau
échappe à un recensement fait hors ligne*, et *c'est le témoin positif qui donne
sa valeur à un « 0 »* (399) · **et aujourd'hui même, un `cd` oublié m'a fait
croire six commandes durant que `CLAUDE.md` avait disparu du dépôt : il n'avait
jamais bougé — l'instrument, cette fois, c'était le shell.**

**L'état du produit n'a pas bougé.** Vérifié dans le dépôt : depuis le correctif
XSS du lot **372** (4 fichiers de `vertex/ui/`), la seule modification hors tests
et documentation est **deux corrections de `CLAUDE.md`**, aux lots 381 et 382.
**Sur la tranche 390-399 : zéro.** MD5 des 8 pages servies re-prouvé identique
aux lots **390** et **396**. Dit franchement : **la boucle entretient et vérifie,
elle ne construit plus.**

**LA QUESTION DE FOND, REPOSÉE.** *Aucun GO n'est arrivé depuis le lot 388.* Les
dossiers du **rang 1** — ceux où l'utilisateur voit du faux dans son terminal —
sont tous à l'arrêt : 7 points MSFT fabriqués (388) · scan de démo dans
`breadth_history` (391) · `context()` sur univers vide (379) et « points réels du
scan » (363) · replis `0` de `_followed_count`/`_positions_count` (378) · badge
de provenance IBKR jamais affiché (386). Trois issues :
**(a)** continuer les lots courts — rendement décroissant, et c'est mesuré : deux
des six derniers n'ont trouvé strictement rien ;
**(b) un GO groupé sur le rang 1, puis exécution — RECOMMANDÉ**, en commençant
par la purge des 7 points MSFT (coût quasi nul, risque nul, seule ligne où un
chiffre inventé est aujourd'hui servi comme une mesure) ;
**(c)** arrêter la boucle et attendre — défendable, rien ne se dégrade.
Ce qui ne serait **pas** honnête, c'est de continuer indéfiniment en (a) en
laissant croire que le travail avance sur ce qui compte. Il n'avance pas :
**il attend une décision.**

## BILAN — veille active, lots 380 → 389 (2026-08-09, bilan n°8)

Dix lots. **Vérification refaite, pas rappelée** : **MD5 8/8 identiques** aux
références sur les 8 pages servies · navigateur réel, 8 pages hydratées,
**0 erreur console** · **les 7 gardiens de la tranche rejoués avec une faute
réelle : 7 sur 7 mordent encore**, témoin négatif muet.

### Les chiffres

Suite **2 754 → 2 835** (+81, soit exactement les 81 tests des 7 gardiens
ajoutés) · PR **#412 → #421** toutes fusionnées en squash · SW `td-shell-v187`
**inchangé sur les dix lots** · `main` jamais touchée · **zéro fichier de
production modifié**.

### Cinq trouvailles réelles

1. **381** — le repli de `deskKeys()` **servi** par `/system` n'était couvert par
   aucun test : y retirer une clé passait les 2 754 tests. Constat joint :
   `vx_kit.JS` (21 727 o) n'atteint aucune des 8 pages.
2. **382** — « aucun littéral couleur » était **faux** : 265 littéraux distincts
   dans `vertex/ui/**`, **53 atteignent une page servie**. La règle réellement
   tenue (aucun bleu non-marque) est la bonne ; la doc mentait.
3. **385** — le recensement des replis numériques s'arrêtait à `vertex/` :
   **31 % des handlers de production hors filet**, dont les 101 de `terminal.py`.
4. **387** — **un test pouvait effacer les notes du trader.** `myNotes` est une
   clé synchronisée ; le round-trip desk l'écrasait et restaurait **sans
   `finally`**. Une assertion en échec laissait `{"guard": "lot84-guard-…"}`
   **définitivement**.
5. **388** — **un point GEX fabriqué par jour sur MSFT**, un vrai titre, dans
   `gex_history_cache.json` que `/api/options/gex-radar` **sert**.

Les deux dernières sont d'une autre gravité : elles touchent les **données
réelles de l'utilisateur**, pas la documentation ni la couverture.

### Deux veines fermées par la mesure

**Audit des gardiens par mutation** (381-384) : 27 mutations, 2 trouvailles,
toutes deux dans les 2 premiers lots — fermée sur le rendement, pas la fatigue.
**Écritures runtime** (386-389) : 2 trouvailles ; 5 fichiers touchés au départ,
**4 à l'arrivée, tous sur un simple horodatage** (vérifié feuille à feuille).

### Le fil rouge — huit fois, la faute était dans MES instruments

Périmètre `vertex/` seulement (385) · chaîne présente 4× (386) · périmètre
4 → 15 → 17 fichiers **et un gardien accusant 2 fichiers sains** (387) ·
mutation portant sur le **message** de l'assertion (387) · exemption au fichier
(387) · détecteur rendant « ? », **8 sites comptés pour 12 réels** (388) ·
8 candidats pour **2 écrivains réels**, et **l'anti-vide creux REFAIT** (389) ·
mutation injectée dans une clé de nav jamais rendue (390).

**Avoir la règle écrite ne suffit pas à ne pas la re-violer** — le 389 a refait
mot pour mot la faute du 386. Ce qui l'attrape n'est pas la mémoire, **c'est la
preuve ROUGE**. Et le témoin a une valeur symétrique : au 389 il a mordu, et
c'était lui qui avait tort.

### Ce que la tranche n'a PAS prouvé

Les 81 tests sont **statiques** (ils lisent le code, n'observent pas
l'exécution) · les caractérisations sont **datées** · aucune couverture
exhaustive n'est démontrée · la **pollution historique n'est pas nettoyée**
(7 points MSFT, points SKYX/TSTQ) — donnée utilisateur, décision à prendre.

### Le vrai goulot — 18 dossiers, classés

**Rang 1, l'utilisateur voit du faux** : purge des points MSFT (388) ·
`context()` sur univers vide (379) + « points réels du scan » (363) · replis `0`
de `_followed_count`/`_positions_count` (378) · badge de provenance IBKR (386).
**Rang 2, risque de données** : filet desk option A (362).
**Rang 3, poids mort chiffré** : 604 Ko de `PAGE_*` (374, à trancher **avec** le
badge — elles contiennent son seul rendu) · `vx_kit.JS` (381) · purges É2/É3 et
fonctions de tête.
**Rang 4** : cosmétique, plus `vocab_js` (373) **déconseillé en l'état**.

**Si un seul GO : la purge des points MSFT** — coût quasi nul, risque nul, et
c'est la seule ligne où un chiffre inventé est aujourd'hui servi comme une
mesure.

## BILAN — veille active, lots 370 → 379 (2026-08-08, bilan n°7)

Dix lots de veille autonome sur la veine **sécurité & honnêteté des données**.
Vérifié au lot 380 : **MD5 8/8 identiques** aux références et **0 erreur console**
sur les 8 pages en navigateur réel — *les octets servis n'ont pas bougé d'un bit
sur toute la tranche*. Les **9 gardiens ajoutés ont été rejoués un par un avec une
faute réelle : les 9 mordent encore.**

### Ce que la tranche a apporté

- **Une vraie faille, sérieuse** (lot 372) : `/opportunities` laissait passer les
  valeurs de paramètres d'URL dans un bloc `<script>` via un `json.dumps` nu —
  XSS **déclenchable à distance par un simple lien**, dans une session ayant accès
  au desk local. Trouvée, corrigée, prouvée MD5-neutre, verrouillée.
- **Un danger latent verrouillé** (373) : `vocab_js`, `json.dumps` nu sur les
  8 pages, sûr seulement parce que son contenu est constant — désormais un
  invariant le garantit, sans durcissement inutile.
- **Une myopie de gardien corrigée** (377) : le gardien du 376 ne voyait que
  **13 refus sur 39** — il manquait tous les `return jsonify({...})`, c'est-à-dire
  les refus servis au navigateur. 33 % de couverture, au vert.
- **Deux pistes fermées par la mesure** (375, 376) plutôt que par un faux vert.
- **Chiffres** : suite **2610 → 2754** (+144 tests), jamais rouge · 9 gardiens ·
  **1 seul lot touchant la production** · SW `td-shell-v187` inchangé · 10 PR
  (#402→#411) · `main` jamais touchée.

### Le fil rouge — douze fois où l'outil était en cause, sous cinq formes

1. **L'outil accuse du code sain** (374 ×2, 375, 376) — *un gardien qui crie au
   loup finit désactivé*.
2. **Le périmètre de l'outil ment** (373 : `os.listdir` masquait le producteur
   HTML central ; 377 : `return <Dict>` manquait tous les `jsonify`) — *sous
   quelle ENVELOPPE la chose cherchée se présente-t-elle ?*
3. **L'outil empêche d'INNOCENTER** (378 : `s = 50.0` n'était pas le neutre, la
   fonction rend 76 à vide) — *le raisonnement élégant se vérifie sur valeurs
   réelles, dans les deux sens*.
4. **La borne trop lâche** (378) — *une borne qui absorbe la première régression
   n'est pas une borne*.
5. **La preuve elle-même est fautive** (379) — *un cas qui ne mord pas accuse
   d'abord la preuve*.

### Jugement franc — et il n'est pas flatteur partout

Après le lot 372, **sept lots n'ont trouvé aucune nouvelle faille exploitable** :
uniquement des dangers latents, des caractérisations et des « sain, rien touché ».
Sur la veine sécurité prise seule, **le rendement décroît nettement** — 1 faille
sur 6 lots, puis 0 sur 7. La creuser encore au même rythme donnerait des lots
honnêtes mais maigres.

Ce qui s'est révélé fertile, c'est le **méta-audit** : le lot 377 n'a pas audité
le code mais un **gardien déjà fusionné**. La suite compte **2 754 tests dont
personne n'a vérifié qu'ils voient ce qu'ils prétendent voir** ; un test au vert
qui ne mesure rien est plus dangereux qu'un test absent. C'est la piste
prioritaire de la tranche suivante.

### Le vrai goulot : quatorze dossiers attendent une décision humaine

Plusieurs sont chiffrés à l'unité — **604 Ko de HTML mort assemblés à chaque
import** (374), le **filet desk qui perd le travail de la journée** (362,
option A recommandée), et **deux questions d'honnêteté d'affichage jumelles**
(363 et 379 : sur univers vide, l'application affirme « NEUTRE » et
« participation 0 % » au lieu de dire qu'elle ne sait pas). Ce sont des décisions
produit : l'agent les a mesurées et documentées, il ne peut pas les trancher.
**Ce n'est plus le manque de pistes qui limite, c'est l'attente de ces GO.**

## BILAN — PROGRAMME 100 %, lots 71 → 75 (2026-08-06, bilan n°6)

Directive utilisateur : « Continue à tout développer et quand t'as tout à
100 tu me dis. » — exécuté en 5 lots prouvés, cadence resserrée.
**Le PROGRAMME 100 % est TERMINÉ : tout ce qui est prouvable est prouvé,
gardé par la suite, et vert. Déclaration 100 % faite à l'utilisateur.**

| Mesure | Avant (lot 70) | Après (lot 75) |
|---|---|---|
| Tests verts | 1 694 / 2 skipped | **1 706 / 2 skipped** (+12) |
| Service worker | v123 | **v124** |
| PR fusionnées | — | **5** (#104 → #108) |

### Les 5 lots et leurs verdicts

1. **Hygiène des références** (lot 71) : docstring du gateway IBKR
   citait un gardien INEXISTANT → corrigée (3 vrais gardiens READONLY)
   + contrat « toute référence tests/ citée existe » gardé à vie ;
2. **Performance** (lot 72) : mesures publiées — DCL < 300 ms, 0 doublon,
   vendor 160 kB lazy sur /analysis seul — SAIN + budgets 64 kB gardés ;
3. **Accessibilité** (lot 73) : 4 défauts réels — tickers cliquables
   inutilisables au clavier → tabindex+role + délégué clavier GLOBAL
   Enter/Espace ; re-balayage : 0 défaut sur 8 pages ;
4. **Robustesse** (lot 74) : entrées limites (injection, unicode, 120
   chars, POST malformés) → 0×5xx, 404 API JSON+nosniff, refus honnêtes
   live:false+ts — SAIN, contrat gardé ;
5. **RC FINALE** (lot 75) : suite + audit outillé + responsive + a11y
   re-prouvés sur base fraîche — 0 défaut partout.

Étapes humaines restantes : validation physique (TWS réel, iPhone —
vider le cache pour SW v124) ; merge vers `main` sur accord explicite.

## BILAN — programme AUDIT TOTAL, lots 66 → 70 (2026-08-06, bilan n°5)

Programme demandé par l'utilisateur (« audit totalement complet, tout
cohérent, tous les chiffres, chaque bouton, pousser au maximum ») —
exécuté en 5 volets prouvés. **L'audit total est TERMINÉ : l'application
est cohérente au maximum prouvable.**

| Mesure | Avant (lot 65) | Après (lot 70) |
|---|---|---|
| Tests verts | 1 688 / 2 skipped | **1 694 / 2 skipped** (+6, rouges d'abord) |
| Service worker | v121 | **v123** |
| PR fusionnées | — | **5** (#96 → #100) |

### Les 5 volets et leurs verdicts

1. **Routes** (lot 66) : 137 routes GET balayées — 0×5xx, un seul 400
   structuré ; **incohérence corrigée** : tuile Breadth du briefing sur
   `above50` non étiqueté vs Marchés `>MM200` → canonicalisée + étiquetée
   (preuve : 45 partout, nommé pareil) ;
2. **Vues profondes** (lot 67) : 30 vues × 2 viewports = 60 chargements —
   0 erreur, 0 débordement, 0 texte cassé (NaN/undefined) — SAIN ;
3. **IBKR lecture seule** (lot 68) : 4 verrous indépendants (readonly EN
   DUR, RequestTimeout=45, FORBIDDEN_TOOLS côté IA, config) + refus
   honnêtes prouvés route→UI (« aucun chiffre inventé ») + 34 gardiens —
   SAIN ;
4. **Cohérence fiche ↔ Opportunités** (lot 69) : divergence des moteurs
   DITE aux deux endroits (« un score ne déclenche jamais un ordre ») —
   SAIN ; **lacune corrigée** : scores shortlist sans échelle → « /100 »
   partout ;
5. **États dégradés** (lot 70) : /markets sans scan (10 états vides avec
   action), mémoire vide (branches honnêtes partout) — SAIN.

Invariants tenus sur tout le programme : READONLY absolu, données réelles
uniquement, moteur 0.9.0 jamais touché, `main` intacte. Retour aux RC
périodiques espacées (~30 min).

## BILAN — arc visuel & connexions, lots 51 → 60 (2026-08-05, bilan n°4)

Arc exécuté sur directive utilisateur (« visuel app 2026, esprit IBKR,
plus plus plus » puis « développe jusqu'au lot 60 et arrête-toi seule »).
Chaque chiffre est traçable vers son rapport `SKYLER-LOT-XX.md` et sa
ligne `SKYLER-INDEX.md`. **La boucle autonome est ARRÊTÉE après ce lot.**

| Mesure | Avant (lot 50) | Après (lot 60) |
|---|---|---|
| Tests verts | 1 627 / 2 skipped | **1 670 / 2 skipped** (+43, rouges d'abord) |
| Service worker | v107 | **v116** (9 bumps, 4 gardiens à chaque fois) |
| PR fusionnées | — | **10** (#78 → #87) |
| RC navigateur | — | **7 × GO — 0 défaut** (dont RC finale 8 pages × 3 viewports) |
| Moteur décisionnel | 0.9.0 | **0.9.0 — JAMAIS touché** |

### Livré sur l'arc

- **Signature graphique « app 2026 »** centrale (lots 51-54) : lissage
  monotone (jamais de faux extrêmes), dégradés riches, glow, pastille de
  dernier prix, crosshair de visée, chandeliers lisibles (défaut réel
  d'axe Y corrigé) — TOUT le tronc `chart-core.js` + prix d'Analyse ;
- **Connexions simplifiées** (lot 55) : fil d'Ariane cliquable (serveur
  + SPA, source unique), retour contextuel couvrant les 8 espaces ;
- **Polish prouvé page par page** (lots 56-59) : séries comparées
  contrastées (par la SOURCE palette.py), plus aucune info tronquée,
  ~75 fallbacks d'anciennes palettes purgés (dont 6 oranges bannis et
  2 tokens CSS inexistants qui rendaient RÉELLEMENT l'ancien thème),
  doc /design-system honnête, gardiens PROSPECTIFS transversaux ;
- **RC finale** (lot 60) : suite complète + audit outillé + responsive
  8×3 : 0 défaut ; cycle souverain re-prouvé une dernière fois.

Étapes restantes HUMAINES : validation physique (TWS réel, iPhone) ;
merge vers `main` sur accord explicite uniquement.

## BILAN — travail continu, lots 29 → 48 (2026-08-05, bilan n°3)

Synthèse des 20 lots + 3 RC périodiques livrés en mode continu (« go sans
validation humaine ») depuis la RC du lot 27, à l'intention de la
validation humaine. Remplace le bilan n°2 (lots 29-43) — chaque chiffre
reste traçable vers son rapport `SKYLER-LOT-XX.md` / `SKYLER-RC-…` et sa
ligne dans `SKYLER-INDEX.md`.

| Mesure | Avant (lot 28) | Après (lot 48) |
|---|---|---|
| Tests verts | 1 515 / 2 skipped | **1 627 / 2 skipped** (+112) |
| Moteur décisionnel | 0.8.0 | **0.9.0** (catalyst_kind émis + figé) |
| Service worker | v100 | **v107** (7 bumps, gardiens à jour) |
| RC navigateur | — | **6 × GO — 0 défaut** (dont 3 périodiques) |

### Capacités livrées

- **CYCLE SOUVERAIN COMPLET** (lots 29/42/45/46/47/48) : export intègre
  (`content_sha256` vérifiable hors ligne + `ledger_health` embarqué),
  RESTAURATION par rejeu append-only des TROIS magasins (l'historique
  local gagne toujours, empreinte vérifiée avant toute écriture),
  boutons Exporter/Importer côte à côte dans la carte Mémoire — et le
  cycle entier (export → altération refusée → restauration par le vrai
  bouton) est RE-PROUVÉ en navigateur À CHAQUE RC (lot 48) ;
- **Type de catalyseur figé** (lot 30) : `catalyst_kind` émis par le
  moteur + découpe `by_catalyst_type` en observation (non consommée) ;
- **Chaîne mémoire fermée** (lots 39/40) : badge → cellule (source
  unique d'appartenance) → décisions mesurées hit/miss → post-mortem —
  API JSON + vue HTML lisible (markupsafe prouvé sur contenu hostile) ;
- **Surfaçage UI** (lots 33/35/37) : badges contexte, `LEDGER :
  ANOMALIES` conditionnel, fraîcheur « dernière décision figée (J-N) » ;
- **Santé du ledger** (lot 35) : doublons/orphelins/mélanges de
  versions/corruption — DIT, jamais réparé en silence ;
- **RC courte outillée auto-prouvante** (lots 32/41/48) : 8 pages +
  parcours mémoire + cycle souverain à chaque exécution.

### Robustesse prouvée

- **11 crashs réels corrigés** en refus honnêtes (7 moteurs lot 31,
  4 HTTP 500 lot 34) ; couverture adversariale HTTP complète et exacte
  (lots 31/34/36/43) ;
- **2 défauts réels attrapés UNIQUEMENT par la preuve navigateur** :
  J-1 affiché pour une décision du jour (lot 37) et empreinte cassée au
  round-trip JS `100.0 → 100` (lot 47) — tous deux corrigés avec test
  rouge dédié ; **2 défauts d'outillage** corrigés et dits (lots 40/41).

### Invariants tenus sur les 20 lots

READONLY absolu · données réelles uniquement (absent → n/d) · `main`
jamais touchée · fichiers runtime jamais commités · gardiens prospectifs
· zéro aléatoire moteur · rouge d'abord quand le comportement change ·
preuve navigateur à chaque changement de shell · reports honnêtes dits.

### Étape suivante — dit franchement

Le cycle souverain est FERMÉ et auto-prouvé ; le backlog code est épuisé
en valeur réelle. **La validation humaine physique (TWS réel, pages,
iPhone — réserve n°1 de la RC du lot 27) est l'étape décisive du
programme.** Le mode continu bascule en RC périodiques espacées
(~30 min) — chaque RC re-prouvant suite complète, 8 pages, parcours
mémoire ET cycle souverain.


## Source de vérité

Skill : `.claude/skills/vertex-skyler-v2/SKILL.md`

Références avancées ajoutées :

- `references/DECISION_ENGINE.md`
- `references/ADVERSARIAL_COMMITTEE.md`
- `references/DECISION_PACKET_SCHEMA.md`
- `references/SCENARIO_CALIBRATION.md`
- `references/ANOMALY_INTELLIGENCE.md`

## Phase Core — historique validé

| Étape | Statut | Preuve principale |
|---|---|---|
| Audit convergence | ✅ GO | `docs/skyler/BRANCH_CONVERGENCE_AUDIT.md` |
| Lot 0 — Baseline | ✅ GO | `docs/skyler/BASELINE.md` |
| Lot 1 — Correctness options | ✅ GO | `docs/refactor/validation/SKYLER-LOT-01.md` |
| Lot 2 — Constitution V2 | ✅ GO | `docs/refactor/validation/SKYLER-LOT-02.md` |
| Lot 3 — Market Intelligence | ✅ GO | `docs/refactor/validation/SKYLER-LOT-03.md` |
| Lot 4 — News/catalyseurs/anomalies | ✅ GO | `docs/refactor/validation/SKYLER-LOT-04.md` |
| Lot 5 — Skyler Core | ✅ GO | `docs/refactor/validation/SKYLER-LOT-05.md` |
| Lot 6 — Options Intelligence | ✅ GO | `docs/refactor/validation/SKYLER-LOT-06.md` |
| Lot 7 — Portfolio Intelligence | ✅ GO | `docs/refactor/validation/SKYLER-LOT-07.md` |
| Lot 8 — Neon Glass | ✅ GO | `docs/refactor/validation/SKYLER-LOT-08A.md` à `08E.md` |
| Lot 9 — Calibration infrastructure | ✅ GO infrastructure | `docs/refactor/validation/SKYLER-LOT-09.md` |

État observé avant l’expansion : environ 1 300 tests verts, service worker v94, IBKR READONLY intact, `main` non modifiée.

## Phase Institutional+ — nouvelle expansion

### Gouvernance installée

- [x] moteur de décision institutionnel documenté ;
- [x] comité contradictoire de 12 rôles documenté ;
- [x] Président Skyler unique producteur du verdict final ;
- [x] avocat du diable obligatoire ;
- [x] red-team obligatoire pour S/S+ ;
- [x] schéma canonique `SkylerPacket` défini ;
- [x] scénarios/probabilités/calibration renforcés ;
- [x] intelligence des anomalies renforcée ;
- [x] agents spécialisés installés ;
- [x] runbook et checklist étendus.

### Lots Institutional+

| Étape | Statut | Objectif | Rapport attendu |
|---|---|---|---|
| Lot 10 — Mémoire et discipline décisionnelle | ✅ FAIT — validé (« go sans validation humaine ») et fusionné | décisions immuables, classification des erreurs, biais récurrents, amélioration humaine contrôlée | `docs/refactor/validation/SKYLER-LOT-10.md` |
| Lot 11 — Knowledge Graph institutionnel | ✅ FAIT — en attente de validation | relations sociétés/secteurs/catalyseurs/portefeuille prouvables, propagation explicable, questions de recherche | `docs/refactor/validation/SKYLER-LOT-11.md` |
| Lot 12 — Red-team et RC finale | ✅ FAIT — GO AVEC RÉSERVES (validation physique restante) | stress adversarial, audit math/données/sécurité, release candidate | `docs/refactor/validation/SKYLER-LOT-12.md` |

## Agents Institutional+

- `.claude/agents/skyler-chair.md`
- `.claude/agents/skyler-devils-advocate.md`
- `.claude/agents/skyler-market-regime.md`
- `.claude/agents/skyler-options-risk.md`
- `.claude/agents/skyler-data-auditor.md`
- `.claude/agents/skyler-portfolio-risk.md`

Aucun sous-agent ne peut publier `final_decision`. Le Président Skyler est l’unique source canonique.

## Décisions établies

- `main` ne bouge pas sans accord explicite.
- Neon Glass/Skyler reste la base fonctionnelle.
- Une invocation Claude = une mission ou un lot.
- Aucun lot Institutional+ ne commence sans validation du précédent.
- Les calculs et décisions canoniques restent déterministes.
- Claude rédige mais ne crée ni ne modifie les chiffres.
- IBKR reste strictement READONLY.
- Aucune note S/S+ sans red-team indépendante.
- Aucune recalibration ou modification de Constitution automatique.

## Lot 10 — livré (2026-08-05)

- moteur `vertex/engines/decision_memory.py` : ledger immuable par version de
  moteur (gel de 31 champs), anti-look-ahead par empreinte de série, résultats
  aux horizons déclarés (5/20/60 séances, catalyseur estimé étiqueté, thèse et
  option honnêtement NON_APPLICABLE), taxonomie d'erreurs déterministe,
  10 biais surveillés, recommandations `EN_ATTENTE_VALIDATION_HUMAINE` ;
- routes : gel fail-safe dans `/api/skyler/<sym>` + `GET /api/skyler/memory` ;
- persistance runtime `skyler_memory.json` (gitignorée, bornée) ;
- 1332 tests verts / 2 skipped (+32) ; SW inchangé v94 (aucune UI touchée) ;
- interdictions respectées : pas de Knowledge Graph, pas d'UI, pas de
  modification automatique des poids/Constitution, `main` intacte, aucun ordre.

## Lot 11 — livré (2026-08-05)

- moteur `vertex/engines/knowledge_graph.py` : 4 relations prouvables
  (secteur F1 sourcé, co-mouvement F2 fenêtré, catalyseur daté F1, détention
  desk F1), provenance obligatoire par arête, propagation explicable saut par
  saut, dépendances cachées ≥ 2 liens indépendants, questions de recherche
  `NON_DOCUMENTE` — fournisseurs/clients/concurrents JAMAIS inventés ;
- routes lecture seule : `GET /api/skyler/graph` + `GET /api/skyler/graph/<sym>` ;
- 1350 tests verts / 2 skipped (+18) ; SW inchangé v94 (aucune UI touchée).

## Lot 12 — livré (2026-08-05)

- règle red-team du comité appliquée par le moteur : S/S+ sans red-team
  complétée = plafonné à A — `ENGINE_VERSION` 0.1.0 → **0.2.0** (règle changée
  = version changée), historique 0.1.0 séparé en mémoire, Constitution
  intouchée (proposition de gate profil V3 documentée, en attente humaine) ;
- trouvaille adversariale corrigée : NaN/infini refusés par la mémoire ;
- batterie adversariale : séries hostiles, prix extrêmes, attaque look-ahead,
  déterminisme, labels hostiles, verbes d'ordre, fichiers runtime/secrets,
  performance bornée — 17 tests ;
- 1367 tests verts / 2 skipped (+17) ; SW v94 inchangé.

## Lot 13 — livré (2026-08-05, travail continu autorisé)

- moteur **0.3.0** : `operational_state` déterministe (8 états DECISION_ENGINE
  §2.2, base explicite, jamais une décision finale) + `confidence` factorisée
  §7 (4 facteurs bornés avec base, plafonds UNKNOWN ≤ 0,55 / conflit ≤ 0,50 /
  contradiction ≤ 0,60, calibration figée à 0,50 sans historique — jamais
  100 %) ;
- le ledger mémoire fige désormais ces champs (31/31 champs vivants) ;
- 1386 tests verts / 2 skipped (+19).

## Lot 14 — livré (2026-08-05, travail continu)

- moteur **0.4.0** + `vertex/engines/red_team.py` (1.0.0) : les 10 questions
  d'ADVERSARIAL_COMMITTEE §8 évaluées depuis les données réelles du packet —
  réponse fondée (F1/F2, données citées) ou UNANSWERED avec raison, jamais
  inventée ; `complete=True` seulement à 10/10 ; revue servie dans
  `/api/skyler/<sym>` (`red_team_review`) et injectée dans la décision ;
- le chemin S/S+ a désormais sa clé — mais reste fermé par les blocs
  insuffisants tant que les fondamentaux ne sont pas branchés (voulu) ;
- 1398 tests verts / 2 skipped (+12).

## Lot 15 — livré (2026-08-05, travail continu)

- `vertex/engines/session_log.py` : UNE clôture par symbole et par jour de
  scan RÉEL (date d'observation UTC, jamais inventée ; dédup par date ; borné ;
  NaN/dates malformées refusés) — `skyler_sessions.json` runtime gitignoré ;
- la mémoire fige `session_date` et les horizons 5/20/60 comptent des séances
  RÉELLES (log autoritaire, empreinte de série en secours pour les anciens
  records) — limite n° 1 du lot 10 levée ;
- 1410 tests verts / 2 skipped (+12).

## Lot 16 — livré (2026-08-05, travail continu)

- surfaçage UI : carte « Mémoire décisionnelle » sur Performance (ledger par
  version de moteur, biais badgés, propositions en attente humaine, état vide
  honnête) + section « Dépendances cachées » sur Portefeuille → Risque
  (paires ≥ 2 liens, questions de recherche) ;
- SW **v95** + 4 gardiens à jour ; preuve navigateur 390/1440 : 0 erreur
  console, 0 overflow, captures `docs/skyler/baseline/lot16-*.png` ;
- 1416 tests verts / 2 skipped (+6).

## Lot 17 — livré (2026-08-05, travail continu)

- co-mouvement du graphe en **corrélation partielle** (résidus OLS vs SPY,
  `method: residual_vs_SPY` + R² par titre) — le faux co-mouvement « les deux
  suivent le marché » est filtré (prouvé par test) ; sans SPY, fallback
  `method: raw` ÉTIQUETÉ + limite dite, jamais silencieux ; SPY exclu des
  paires ;
- `hidden_groups` : composantes connexes ≥ 3 titres synthétisées dans l'API
  et affichées sur Portefeuille → Risque ;
- SW **v96** + gardiens (lot 16 rendu prospectif ≥ 95) ; navigateur 390/1440 :
  0 erreur console, captures lot17-*.png ;
- 1427 tests verts / 2 skipped (+11).

## Lot 18 — livré (2026-08-05, travail continu)

- moteur **0.5.0** : `robustness` MESURÉE par analyse de perturbation — 11
  variations fixes documentées (score ±10, R:R ±0,5, régime ±0,2, un contexte
  retiré à la fois), fraction stable bornée, bascules listées, non applicable
  exclu (jamais compté stable) ; cœur de verdict partagé anti-divergence ;
  aucun aléatoire (gardien) ; prouvé : un ACHETER frontière bascule sous
  −10 points techniques (fragilité détectée) ;
- 1438 tests verts / 2 skipped (+11) ; SW v96 inchangé.

## Lot 19 — livré (2026-08-05, travail continu)

- moteur **0.6.0** : la boucle décision → mémoire → confiance est FERMÉE —
  `calibration_factor` = scenario hit rate des résultats MESURÉS de la mémoire
  pour la version courante uniquement (0,50 + 0,40 × hit rate, borné
  [0,50, 0,90], jamais 1,0) ; échantillon < 20 mesures → 0,50 « insuffisant »,
  jamais inventé ; route fail-safe ; versions jamais mélangées (testé) ;
- 1450 tests verts / 2 skipped (+12) ; SW v96 inchangé.

## Lot 20 — livré (2026-08-05, travail continu)

- drill-down `GET /api/skyler/memory/<decision_id>` : record figé complet +
  résultat mesuré + **post-mortem déterministe** (classification par horizon,
  scénario ayant contenu le résultat : HORS_FOURCHETTE_BASSE / PESSIMISTE /
  PROBABLE / EXCEPTIONNEL_ATTEINT, MFE/MAE, résumé) — honnête si rien n'est
  mesuré, discipline jamais devinée ; 404 structuré sur id inconnu ;
- carte Mémoire : tableau « Dernières décisions figées » avec lien détail ;
  SW **v97** + gardiens prospectifs ; navigateur 390/1440 : 0 erreur console ;
- 1463 tests verts / 2 skipped (+13).

## Lot 21 — livré (2026-08-05, travail continu)

- red-team **1.1.0** : Q05 chiffrée (repricing Black-Scholes CANONIQUE du
  candidat à IV −10 pts — en démo réelle : « IV 34 % → 24 % : −30,6 % », F3
  avec modèle et hypothèses) ; Q08 en grille stop/TP2/TP3 × IV −10/0/+10 avec
  convexité vs action ; fallbacks F2 et UNANSWERED intacts ; entrées invalides
  jamais chiffrées ; cas manuel BS gardé par test (ATM 1 an vol 20 % ≈ 7,97 %) ;
- 1472 tests verts / 2 skipped (+9) ; SW v97 inchangé.

## Lot 22 — livré (2026-08-05, travail continu)

- moteur **0.7.0** : calibration PAR CONTEXTE (§13) — découpe par niveau et
  par décision, chaque cellule avec son propre hit rate seulement si ≥ 20
  mesures (sinon INSUFFISANT dit, valeur None) ; sélection à portée explicite
  contextuel → global → 0,50 ; la route sert la cellule du niveau courant
  (prouvé bout en bout : cellule REFUS_WATCH 0,90 servie au moteur) ;
  `/api/skyler/memory` expose la découpe ; versions jamais mélangées ;
- 1481 tests verts / 2 skipped (+9) ; SW v97 inchangé.

## Lot 23 — livré (2026-08-05, travail continu)

- vue lisible `GET /memory/<decision_id>` : record figé, résultat mesuré et
  post-mortem rendus dans le shell produit — contenu de la mémoire ÉCHAPPÉ
  serveur (XSS testé avec script hostile), états honnêtes, 404 lisible ;
  lien de la carte Mémoire mis à jour ; SW **v98** ; parcours prouvé en
  navigateur (clic carte → vue, 0 erreur console) ;
- **`docs/refactor/validation/SKYLER-INDEX.md`** : index consolidé des lots
  10 → 23 (objectifs, versions moteur/SW, tests, verdicts) + architecture ;
- 1488 tests verts / 2 skipped (+7).

## Lot 24 — livré (2026-08-05, travail continu)

- `sector_exposure` dans le graphe : positions réelles agrégées par secteur
  déclaré, poids en % SEULEMENT si toutes les positions sont cotées (sinon
  None avec raison — jamais estimé), hors watchlist étiqueté ; groupes cachés
  mono-secteur flaggés **CONCENTRATION SECTORIELLE** ; affiché sur
  Portefeuille → Risque ; SW **v99** ; navigateur prouvé (0 erreur console) ;
- 1498 tests verts / 2 skipped (+10).

## Lot 25 — livré (2026-08-05, travail continu)

- revue de simplification SANS changement de comportement (suite identique
  1498/2, aucun test modifié) : docstrings resynchronisées sur 0.7.0,
  formule de calibration unique (`_hit_factor`), boucle de mesure réutilisée
  (`_measured_hits`), fallbacks red-team dédupliqués ; dette restante
  documentée et assumée.

## Lot 26 — livré (2026-08-05, travail continu)

- moteur **0.8.0** : calibration par RÉGIME — le record mémoire fige le label
  du régime au moment de la décision (None honnête, anciens records
  compatibles) ; découpe `by_regime` (mêmes règles d'échantillon, régime
  inconnu ≠ cellule) ; sélection prioritaire documentée niveau → régime →
  global avec portée explicite ; route passe le régime courant ; badges de
  calibration par contexte dans la carte Mémoire (masqués sans mesures —
  honnête) ; SW **v100** ;
- 1508 tests verts / 2 skipped (+10).

## Lot 27 — livré (2026-08-05, RC courte du travail continu)

- AUDIT complet des lots 13 → 26 (aucun code moteur) : 8 espaces en 200 aux
  deux tailles, 0 overflow, 0 erreur JS applicative (client-log = 0 ; les
  resets du tour = requêtes coupées par la navigation + Google Fonts
  injoignable dans la sandbox — investigué, documenté) ; 9 endpoints Skyler
  en 200 avec versions cohérentes (décision 0.8.0, red-team 1.1.0 complète,
  graphe 0.1.0 distinct) ; sécurité propre (no_orders, aucun runtime/secret
  suivi, aucun verbe d'ordre, readonly intact) ;
- verdict **GO AVEC RÉSERVES** — réserve n° 1 inchangée : validation humaine
  sur appareil physique ; bilan : +141 tests depuis le lot 12, moteur
  0.2.0 → 0.8.0, SW v94 → v100, 4/4 facteurs de confiance mesurés.

## Lot 28 — livré (2026-08-05, travail continu)

- `by_catalyst` dans la calibration par contexte : cellules avec/sans
  catalyseur dérivées du ledger existant, mêmes règles d'échantillon —
  découpe d'OBSERVATION uniquement, jamais consommée par la sélection
  (aucun bump moteur, prouvé par test) ;
- propagation du graphe 1–3 sauts (`?hops=`, clampé) avec garde de volume
  dure MAX_PATHS=200 — troncature déterministe et TOUJOURS DITE ;
- 1515 tests verts / 2 skipped (+7) ; SW v100 inchangé (API seulement).

## Lot 29 — livré (2026-08-05, travail continu)

- `GET /api/skyler/memory/export` : bundle JSON lecture seule (mémoire +
  séances + journal + versions moteur/schéma, horodatage UTC réel,
  `Content-Disposition` téléchargement) — l'historique décisionnel
  devient SOUVERAIN (les fichiers runtime sont gitignorés/périssables) ;
- lecture seule PROUVÉE (octets identiques avant/après l'appel) ;
  magasins vides → formes vides honnêtes ;
- bouton « Exporter → » dans la carte Mémoire (Performance) ; SW v101 ;
- 1522 tests verts / 2 skipped (+7) ; moteur 0.8.0 inchangé.

## Lot 30 — livré (2026-08-05, travail continu)

- `catalyst_kind` émis par le moteur (0.9.0) : le `kind` EXPLICITE
  (`earnings`/`macro`/`news`…) du même événement daté le plus proche qui
  produit `catalyst` — fait du moteur events, source unique, jamais
  re-parsé depuis le label ; figé au freeze (ancien record → None
  honnête, jamais rétroactif) ;
- découpe `by_catalyst_type` dans la calibration par contexte — mêmes
  règles d'échantillon, bucket `inconnu` honnête, OBSERVATION uniquement
  (non-consommation par la sélection prouvée par test) ;
- 1531 tests verts / 2 skipped (+9) ; SW v101 inchangé (moteur/API).

## Lot 31 — livré (2026-08-05, travail continu)

- batterie de fuzz DÉTERMINISTE (listes fixes, zéro aléatoire) sur les
  chemins des lots 26–30 : propagate, calibration (globale/contexte/
  sélection), freeze + catalyst_kind, export souverain ;
- **7 crashs réels trouvés** (TypeError unhashable, AttributeError sur
  magasins corrompus) et corrigés en REFUS HONNÊTES : nœud/contexte/kind
  non-chaîne → []/scope global/bucket `inconnu`, entrées de magasin
  non-dict ignorées, garde MAX_PATHS jamais désactivée ;
- aucun bump de version (aucune règle ne change sur données valides —
  prouvé par la suite inchangée) ; SW v101 inchangé ;
- 1543 tests verts / 2 skipped (+12).

## Lot 32 — livré (2026-08-05, travail continu)

- RC courte OUTILLÉE : `tools/rc_short_audit.js` (Playwright, versionné,
  ré-exécutable en périodique) — 8 espaces canoniques, 0 erreur console
  au repos, 0 pageerror, HTTP 200 partout, `/healthz` 200,
  `/api/client-log` à 0, SW `td-shell-v101` servi ;
- vérification live du chemin neuf : `/api/skyler/memory/export` → 200 +
  Content-Disposition téléchargement ;
- verdict **GO — 0 défaut produit** ; la validation sur appareil physique
  (TWS réel) reste l'étape humaine (réserve n°1 du lot 27, inchangée) ;
- 1543 tests verts / 2 skipped (inchangé — audit sans changement de
  comportement) ; SW v101 inchangé.

## Lot 33 — livré (2026-08-05, travail continu)

- carte Mémoire : les découpes d'OBSERVATION `by_catalyst` et
  `by_catalyst_type` rejoignent les badges de calibration par contexte —
  MÊME mécanique que niveau/régime/décision (une seule boucle, gardé par
  test), libellé explicite « catalyseur/type = observation, jamais
  consommés » ;
- SW v101 → v102 + 4 gardiens ; preuve navigateur : RC courte
  (tools/rc_short_audit.js) GO — 8 pages, 0 erreur console, client-log 0,
  v102 servi ; en démo 0 cellule mesurée → aucun badge (honnête, lot 26) ;
- 1547 tests verts / 2 skipped (+4) ; moteur 0.9.0 inchangé.

## Lot 34 — livré (2026-08-05, travail continu)

- batterie de fuzz HTTP à listes FIXES sur les routes graphe/mémoire :
  ?hops= dégénérés (clamp 1..3 toujours appliqué, troncature toujours
  dite), symboles/ids dégénérés (404 structuré, jamais nu), traversée
  (jamais un fichier système), XSS (id hostile jamais réfléchi brut) ;
- **4 crashs 500 réels trouvés** sur magasin mémoire corrompu (passe de
  mesure, find_decision/find_outcome, detect_patterns, aggregates) et
  corrigés : entrées non-dict ignorées, entrées valides toujours
  servies — refus honnête, jamais 500 ;
- aucun bump de version (données valides inchangées) ; SW v102 inchangé ;
- 1555 tests verts / 2 skipped (+8).

## Lot 35 — livré (2026-08-05, travail continu)

- `decision_memory.ledger_health` : contrôle de cohérence du ledger
  multi-versions — doublons d'id, outcomes orphelins, mélanges de
  versions décision/outcome, entrées corrompues ; statut SAIN/ANOMALIES
  avec basis chiffrée ; le contrôle DIT, ne répare JAMAIS (l'historique
  original gagne) ; robuste aux mémoires dégénérées d'entrée ;
- servi dans `/api/skyler/memory` (`ledger_health`) ; badge rouge
  « LEDGER : ANOMALIES » dans la carte Mémoire SEULEMENT si anomalie ;
- SW v102 → v103 + 4 gardiens ; RC courte GO (8 pages, 0 erreur,
  client-log 0, v103 servi) ; vérif live : status SAIN ;
- 1565 tests verts / 2 skipped (+10) ; moteur 0.9.0 inchangé.

## Lot 36 — livré (2026-08-05, travail continu)

- batterie de fuzz à listes FIXES sur `/api/skyler/<sym>` (le cœur
  décisionnel HTTP) : 14 symboles dégénérés, 6 corruptions de magasins
  (une par une puis simultanées, double appel dédupliqué), honnêteté du
  titre inconnu (blocs INSUFFISANTS, jamais un achat sans données),
  déterminisme, calibration fail-safe 0,50 — magasins réels jamais
  touchés (fixture isolée) ;
- **0 défaut produit** : la route était déjà robuste (gardes lots 31/34
  + hooks fail-safe) ; le contrat de réponse `{symbol, decision:{…},
  packet, red_team_review, demo}` est désormais DOCUMENTÉ par les tests ;
- couverture HTTP adversariale complète des chemins Skyler ;
- 1572 tests verts / 2 skipped (+7) ; moteur 0.9.0 et SW v103 inchangés.

## Lot 37 — livré (2026-08-05, travail continu)

- carte Mémoire : fraîcheur du ledger dans l'en-tête — « dernière
  décision figée : YYYY-MM-DD (J-N) », trois états honnêtes (ledger vide
  → « aucune décision figée », date absente → n/d, date réelle → J-N en
  différence de dates calendaires UTC, J-0 = aujourd'hui) ;
- **défaut réel attrapé par la preuve navigateur** : la première version
  affichait J-1 pour une décision d'aujourd'hui (arrondi d'heures) —
  corrigé en différence de minuits UTC, re-vérifié live « J-0 » ;
- SW v103 → v104 + 4 gardiens ; RC courte GO (8 pages, 0 erreur,
  client-log 0, v104 servi) ;
- 1576 tests verts / 2 skipped (+4) ; moteur 0.9.0 inchangé.

## Lot 39 — livré (2026-08-05, travail continu)

- drill-down cellule de calibration : `decision_memory.cell_decisions` —
  les décisions MESURÉES qui composent une cellule (id, titre, séance,
  contextes figés, hit/miss), avec la règle d'appartenance extraite en
  SOURCE UNIQUE (`_cell_key`, consommée par calibration_by_context ET le
  drill-down — anti-divergence prouvée sur toutes les cellules
  publiées) ;
- route `GET /api/skyler/memory/cell/<group>/<key>` : 404 structurés
  (groupe_inconnu avec liste des groupes, cellule_inconnue), résumé de
  cellule joint, jamais 500 ; badges de la carte Mémoire cliquables ;
- SW v104 → v105 + 4 gardiens ; RC courte GO (v105 servi) + 404 live
  vérifiés ; 1586 tests verts / 2 skipped (+10) ; moteur 0.9.0 inchangé.

## Lot 40 — livré (2026-08-05, travail continu)

- vue HTML lisible d'une cellule de calibration : `/memory/cell/<group>/
  <key>` — résumé (facteur, hit rate, n, basis), table des décisions
  MESURÉES avec hit/miss honnêtes et lien post-mortem par record,
  404 lisibles ; markupsafe PROUVÉ sur contenu hostile figé (affiché
  échappé, jamais exécuté ni caché) ; la vue lit `cell_decisions`
  (source unique lot 39), ne recalcule rien ;
- badges de la carte Mémoire → vue lisible (l'API JSON reste servie
  pour l'audit) ; boucle complète : badge → cellule → record →
  post-mortem ;
- SW v105 → v106 + 4 gardiens ; RC courte GO (v106 servi) + 404 live ;
- 1593 tests verts / 2 skipped (+7) ; moteur 0.9.0 inchangé.

## Lot 41 — livré (2026-08-05, travail continu)

- `tools/rc_short_audit.js` étendu au PARCOURS MÉMOIRE : après les
  8 pages, l'audit fige une décision démo (/api/skyler/AAPL), vérifie
  `/memory/<id>` en vrai navigateur (200, « Décision figée », 0 erreur
  console) puis la vue cellule — cellule existante → 200, sinon le 404
  LISIBLE est vérifié et DIT (démo : aucune cellule mesurée, honnête) ;
- défaut d'OUTIL trouvé et corrigé : innerText reflète la casse CSS
  (uppercase) → comparaison insensible à la casse, documentée ;
- RC courte GO — 0 défaut produit ; 1593 tests verts / 2 skipped
  (inchangé — outil seulement) ; moteur 0.9.0 et SW v106 inchangés.

## Lot 42 — livré (2026-08-05, travail continu)

- intégrité de l'export souverain : le bundle embarque `ledger_health`
  calculé AU MOMENT de l'export (l'archive dit elle-même si le ledger
  était cohérent — un magasin corrompu est fidèlement empreinté et son
  incohérence DITE, jamais maquillée) et `content_sha256` (sha256 du
  JSON canonique, clés triées — vérifiable HORS LIGNE sans le serveur,
  méthode documentée dans la note du fichier même) ;
- lecture seule stricte re-prouvée (octets identiques) ; gardiens de
  l'export lot 29 verts inchangés ; biais par type de catalyseur
  vérifié et REPORTÉ honnêtement (aucune information nouvelle sans
  échantillons mesurés réels) ;
- 1599 tests verts / 2 skipped (+6) ; moteur 0.9.0 et SW v106 inchangés.

## Lot 43 — livré (2026-08-05, travail continu)

- fuzz à listes FIXES des DEUX routes cellule (JSON + HTML, postérieures
  à la batterie du lot 34 — trou de couverture fermé) : traversée
  percent-encodée, 500 chars, XSS, unicode NFD, groupes dégénérés,
  traversée brute ; **0 défaut** — gardes des lots 31/34/39/40 déjà
  couvrantes ;
- non-interférence prouvée (cellule réelle servie entre deux salves
  hostiles) ; pas de normalisation cachée (clé NFD ≠ cellule NFC, 404) ;
- l'affirmation « couverture adversariale HTTP complète » (lot 36) est
  désormais exacte (lots 31/34/36/43) ;
- 1606 tests verts / 2 skipped (+7) ; moteur 0.9.0 et SW v106 inchangés.

## Lot 45 — livré (2026-08-05, développement repris sur directive utilisateur)

- restauration souveraine : `POST /api/skyler/memory/import` — l'export
  a désormais un chemin de retour ; `content_sha256` VÉRIFIÉ AVANT toute
  écriture (archive altérée → 400 dit, rien touché) ;
- `merge_memory` : REJEU APPEND-ONLY — un decision_id existant n'est
  JAMAIS remplacé (l'historique local gagne, prouvé contre archive
  falsifiée), outcomes monotones, entrées corrompues comptées ;
- périmètre honnête : ledger mémoire uniquement (séances/journal au
  backlog, dit dans la réponse) ; round-trip export→import prouvé ;
- 1615 tests verts / 2 skipped (+9) ; moteur 0.9.0 et SW v106 inchangés.

## Lot 46 — livré (2026-08-05, développement continu)

- restauration ÉTENDUE : le même bundle restaure désormais les TROIS
  magasins (mémoire + séances + journal) — périmètre partiel du lot 45
  complété, le mot « backlog » a disparu de la note (gardé par test) ;
- `session_log.merge_log` : seules les séances (symbole, date) absentes
  sont ajoutées — la clôture LOCALE n'est jamais remplacée (filtrage
  AVANT rejeu, car record_close seul aurait laissé l'archive écraser) ;
- `skyler_journal.merge_journal` : même triple de dédup que `record`
  (source unique), l'entrée locale gagne, borné MAX_ENTRIES ;
- empreinte vérifiée avant TOUTE écriture : falsification → 400 et
  AUCUN des trois magasins écrit (prouvé) ; stats par magasin ;
- 1622 tests verts / 2 skipped (+7) ; moteur 0.9.0 et SW v106 inchangés.

## Lot 47 — livré (2026-08-05, développement continu)

- bouton « Importer ← » à côté d'« Exporter → » dans la carte Mémoire :
  FileReader → POST import → affichage HONNÊTE des deux chemins (stats
  exactes par magasin avec « la donnée locale gagne », ou l'erreur
  serveur telle quelle — jamais maquillée) ; XSS échappé, apostrophes
  en entités ;
- **DÉFAUT RÉEL attrapé par la preuve navigateur** : JSON.stringify
  replie 100.0 → 100, l'empreinte canonique ne matchait plus au
  round-trip JS (invisible aux tests Python) — corrigé par
  `_canonical_bundle_json` (source unique export+import, flottants
  entiers normalisés, recette documentée dans le bundle), test rouge
  dédié simulant le round-trip ;
- SW v106 → v107 + 4 gardiens ; preuve navigateur : upload du VRAI
  fichier → « Restauration terminée … ledger : SAIN », 0 erreur
  console ; RC courte GO (v107 servi) ;
- 1627 tests verts / 2 skipped (+5) ; moteur 0.9.0 inchangé.

## Lot 48 — livré (2026-08-05, développement continu)

- CYCLE SOUVERAIN dans la RC outillée (`tools/rc_short_audit.js`) :
  chaque RC exporte le bundle, prouve le REFUS d'une copie altérée
  (400 empreinte_invalide exigé) puis la RESTAURATION via le VRAI
  bouton « Importer » (setInputFiles — le chemin utilisateur, pas un
  raccourci d'API), message « Restauration terminée … ledger SAIN »
  exigé ;
- rationale : le mécanisme le plus critique du desk (survie de
  l'historique) est re-prouvé à CHAQUE RC — 2 défauts réels n'avaient
  été visibles qu'en navigateur (J-1 lot 37, empreinte JS lot 47) ;
- exécuté : GO — 0 défaut ; 1627 tests verts / 2 skipped (inchangé —
  outil seulement) ; moteur 0.9.0 et SW v107 inchangés.

## Lot 50 — livré (2026-08-05, axe optimisation — demande utilisateur)

- profilage OUTILLÉ (`tools/profile_hot_routes.py`, reproductible) :
  p50/p95 des 5 routes chaudes + 8 pages — **toutes sous 15 ms p95**
  (seuil « RAS » fixé d'avance : 100 ms) ;
- hypothèse du double build_packet/score40 dans `/api/skyler/<sym>` :
  VÉRIFIÉE (0,667 ms/appel) puis RELATIVISÉE — 7,4 % d'un decide à
  9 ms dont l'essentiel est l'analyse de perturbation PAR CONSTRUCTION
  (robustesse mesurée, pas du gaspillage) ; route entière ~14 ms ;
- **décision documentée : NO-GO pour le lot d'optimisation** (gain ~1 ms
  imperceptible vs risque de toucher le cœur décisionnel) — l'axe
  optimisation est épuisé en valeur réelle, baseline chiffrée publiée
  pour re-mesurer si la latence réelle dégrade un jour ;
- 1627 tests verts / 2 skipped (inchangé) ; moteur 0.9.0 et SW v107
  inchangés ; retour aux RC périodiques espacées.

## Lot 51 — livré (2026-08-05, axe visuel — direction utilisateur)

- direction utilisateur : graphiques niveau app de courtage 2026 (esprit
  app IBKR) — livré CENTRALEMENT dans `chart-core.js` (`C.area`) : toutes
  les cartes `areaCard` upgradées d'un coup, zéro fork de renderer ;
- signature : lissage `cubicInterpolationMode 'monotone'` (ne dépasse
  JAMAIS les données réelles — pas de faux extrêmes), dégradé d'aire
  3 arrêts, glow subtil (`vxGlow`), pastille de dernier prix (`vxLastDot` :
  halo + point sur le dernier point RÉEL + pilule de prix au bord droit),
  ligne 2 px, survol mode index ;
- palette : AUCUN littéral couleur nouveau (gardien à inventaire exact) —
  `C.colors` + suffixes alpha sur la couleur reçue (idiome existant) ;
- preuves : 6 tests rouges→verts ; suite 1633/2 skipped ; RC outillée GO
  0 défaut sous SW v108 (cycle souverain inclus) ; preuve navigateur
  visuelle (capture /markets : pastille « 413,00 » rendue, roundRect
  supporté, 0 erreur console) ; moteur 0.9.0 inchangé.

## Lot 52 — livré (2026-08-05, axe visuel — suite)

- CROSSHAIR type app de courtage, central dans `chart-core.js` : plugin
  `vxCrosshair` (ligne de visée verticale pointillée suivant le point
  ACTIF du tooltip — jamais dessinée hors survol — + point surligné),
  câblé par défaut dans `C.area`, désactivable ;
- `C.multiLine` HARMONISÉ sur la signature 2026 du lot 51 : lissage
  monotone (jamais de faux extrêmes), ligne 2 px, crosshair ;
- palette : AUCUN littéral couleur nouveau (même gardien à inventaire
  exact que lot 51) ; le crosshair ne fait que POINTER un point réel ;
- preuves : 5 tests rouges→verts ; suite 1638/2 skipped ; RC outillée GO
  0 défaut sous SW v109 (cycle souverain inclus) ; preuve navigateur au
  SURVOL RÉEL (visée + point actif + tooltip + pastille lot 51 rendus,
  0 erreur console) ; moteur 0.9.0 inchangé.

## Lot 53 — livré (2026-08-05, axe visuel — suite)

- les trois primitives restantes de `chart-core.js` rejoignent la
  signature 2026 (livraison centrale, zéro fork) : `C.sparkline`
  (monotone + mini-aire dégradée, muette), `C.bars` (coins arrondis
  complets, translucides → pleines au survol, alpha appliqué SEULEMENT
  aux hex 6 digits — garde regex, jamais de couleur corrompue),
  `C.donut` (arcs arrondis espacés, hoverOffset, cutout 70 %) ;
- le tronc commun est maintenant ENTIÈREMENT sur la signature 2026
  (area/multiLine/sparkline/bars/donut + vxGlow/vxLastDot/vxCrosshair) ;
- preuves : 5 tests rouges→verts ; suite 1643/2 skipped ; RC outillée GO
  0 défaut sous SW v110 (cycle souverain inclus) ; l'état démo n'affiche
  ni donut ni bars (dit) → preuve par HARNAIS sur les primitives
  réellement servies dans la vraie page (capture, 0 erreur console) ;
  moteur 0.9.0 inchangé.

## Lot 54 — livré (2026-08-05, axe visuel — arc « jusqu'au lot 60 »)

- `price-chart.js` (graphique PRINCIPAL de la fiche Analyse) : signature
  2026 complète — monotone, 2 px, dégradé 3 arrêts, glow, visée,
  pastille de dernier prix ; plan moteur et earnings conservés ;
- `candlestick-chart.js` (repli honnête) : mèches 1 px, corps arrondis,
  visée ; DÉFAUT RÉEL attrapé en preuve navigateur — axe Y forcé à 0
  écrasait les bougies (échelle 0-150 pour des prix ~100) → corrigé
  (`beginAtZero:false` + grace 5 %), test rouge figé ;
- equity/drawdown héritent déjà via `C.area` (dit) ; candlestick-lwc
  (moteur LWC pro) inchangé (dit) ; aucun littéral hex nouveau ;
- preuves : 7 tests rouges→verts ; suite 1650/2 skipped ; RC outillée GO
  0 défaut sous SW v111 ; harnais navigateur : pastille « 110,40 »,
  bougies lisibles échelle 95-115, visée + tooltip OHLC (capture) ;
  moteur 0.9.0 inchangé.

## Lot 55 — livré (2026-08-05, arc « jusqu'au lot 60 » — connexions)

- audit honnête d'abord : l'infrastructure de connexions était déjà bonne
  (openAnalysis + délégation globale + contexte + tuiles KPI en liens) —
  deux trous RÉELS trouvés et fermés centralement ;
- fil d'Ariane CLIQUABLE : « Vertex » → `/`, segment d'espace → racine de
  l'espace — rendu serveur (`_topbar`, href depuis PRIMARY_NAV) ET crumb
  reconstruit par le routeur SPA (href dérivé du menu latéral rendu,
  zéro duplication) ; CSS survol discret ;
- retour contextuel §15 complété : les 8 espaces canoniques couverts
  (`/options` et `/journal` manquaient — chemin brut affiché avant) ;
- preuves : 5 tests rouges→verts ; suite 1655/2 skipped ; RC outillée GO
  0 défaut sous SW v112 ; parcours navigateur RÉEL : fiche AAPL → clic
  « Analyse » → /analysis ; crumb SPA (MSFT) garde ses liens ; 0 erreur
  console ; moteur 0.9.0 inchangé.

## Lot 56 — livré (2026-08-05, arc « jusqu'au lot 60 » — polish 1/4)

- inspection réelle d'abord (captures 1440+390, audit débordements : 0,
  0 erreur console) — deux défauts RÉELS corrigés, rien de gratuit ;
- séries comparées : les 3 premiers gris-blancs de SERIES étaient
  indistinguables sur « Indices — performance comparée » → réordonné
  marque/cyan technique/sable/violet/jaune/gris via la SOURCE
  (`palette.py`, constante TECHNICAL nommée) + miroirs thème JS et
  chart-core alignés — le gardien de cohérence a attrapé l'essai
  JS-seul, la source a été alignée, pas contournée ; zéro littéral
  nouveau ; non-bleu vérifié pour le garde-fou ;
- crumb mobile : slash orphelin (racine masquée, séparateur restant) →
  séparateur adjacent masqué avec elle ;
- preuves : 3 tests rouges→verts ; suite 1658/2 skipped ; RC outillée GO
  0 défaut sous SW v113 ; captures APRÈS (4 séries distinctes, crumb
  mobile propre vérifié programmatiquement) ; moteur 0.9.0 inchangé.

## Lot 57 — livré (2026-08-05, arc « jusqu'au lot 60 » — polish 2/4)

- inspection réelle (6 captures, audit : 0 débordement, 0 erreur
  console) — verdict honnête : pages SAINES (table mobile défile
  conformément, pairs déjà cliquables, états vides honnêtes) ;
- deux défauts réels de la fiche corrigés : libellés clé/valeur tronqués
  par ellipse (« Politique … ») → retour à la ligne, information jamais
  perdue (vérifié programmatiquement APRÈS) ; littéral hors palette
  `#FFD27A` (étoile favori) → token `var(--vx-warning)` — le littéral
  analogue de scorecard.py est côté MOTEUR, dit et non touché ;
- preuves : 3 tests rouges→verts ; suite 1661/2 skipped ; RC outillée GO
  0 défaut sous SW v114 ; moteur 0.9.0 inchangé.

## Lot 58 — livré (2026-08-05, arc « jusqu'au lot 60 » — polish 3/4)

- défaut ACTIF trouvé sur /options : le token `--vx-text-dim` n'existe
  pas dans tokens.css → son fallback `#8a837a` (ancienne palette chaude)
  se rendait réellement sur tous les textes atténués ; ~28 fallbacks
  périmés au total dont l'ORANGE BANNI `#cf6128` (tag démo) et le cuivre
  `#b9683d` — tous réalignés sur les tokens réels et leurs valeurs
  actuelles ; tag démo → var(--vx-warning) ;
- /portfolio : 4 fallbacks périmés réalignés + `title` sur le libellé de
  scénario ellipsé (info complète au survol, aria-label déjà présent) ;
- preuves : 5 tests rouges→verts ; suite 1666/2 skipped ; RC outillée GO
  0 défaut sous SW v115 ; balayage APRÈS des couleurs CALCULÉES (14
  valeurs périmées recherchées sur tout #vx-content) : « palette OK »
  sur les deux pages, 0 erreur console ; moteur 0.9.0 inchangé.

## Lot 59 — livré (2026-08-05, arc « jusqu'au lot 60 » — polish 4/4, transversal)

- balayage du lot 58 GÉNÉRALISÉ : ~45 fallbacks d'anciennes palettes
  purgés dans 7 pages (3 oranges bannis de plus sur Système, un
  `--vx-brand,#84aa31` vert aberrant sur /journal, tracking, analysis,
  markets, opportunities, design_system_demo) ;
- 2e token INEXISTANT : `--vx-neutral` (Opportunités — son fallback
  `#9d978e` se rendait) → `--vx-neutral-chart` ; gardien PROSPECTIF :
  tout token référencé avec fallback doit exister dans les CSS ;
- /design-system : étiquettes hex mensongères (valeurs de l'ancien
  design à côté de pastilles LIVE justes) réalignées sur les valeurs
  effectives, section retitrée honnêtement ; rrLadder : 3 fallbacks
  runtime réalignés ;
- vérifié SAIN (dit) : VX.states.empty/error sur les 8 pages ;
- preuves : 4 tests rouges→verts ; suite 1670/2 skipped ; RC outillée GO
  0 défaut sous SW v116 ; balayage APRÈS couleurs calculées : « palette
  OK » sur /journal, /system, /design-system ; moteur 0.9.0 inchangé.

## Lot 61 — livré (2026-08-06, reprise du travail continu)

- Catalyst Runway (briefing) : les étiquettes se chevauchaient sur les
  DTE proches (capture lot 56) — anti-collision DÉTERMINISTE à deux
  rangées par côté, place calculée sur la position bornée au viewBox ;
  le harnais de preuve (chevauchements MESURÉS par bounding boxes) a
  attrapé un défaut résiduel au premier essai, corrigé avant livraison :
  0 chevauchement, 0 hors-limites sur le calendrier dense ;
- gardien anti-palette du lot 59 ÉTENDU aux JS de charts : 25 fallbacks
  périmés purgés (chart-core, runway, anomaly-scan — `--vx-text-dim`
  actif —, regime-aura) + 3e token fantôme `--vx-bg-app` → `--vx-bg-0` ;
- preuves : 5 tests rouges→verts ; suite 1675/2 skipped ; RC outillée GO
  0 défaut sous SW v117 ; moteur 0.9.0 inchangé.

## Lot 62 — livré (2026-08-06, travail continu)

- dernier angle mort de la classe « ancienne palette » fermé :
  19 fallbacks périmés dans `js/pages/` (options-gex — orange banni +
  `--vx-text-dim` ACTIF —, options-intel, options-structure) + 2
  littéraux runtime de tracking.js réalignés ;
- gardien prospectif ÉTENDU à TOUT `vertex/static/vertex/js/`
  récursivement (vendor exclu) : fallback ∈ valeurs actuelles + token
  existant + zéro orange banni — la classe de défauts est FERMÉE sur
  tout le dépôt UI (pages Python lot 59, charts lot 61, reste lot 62) ;
- preuves : 4 tests rouges→verts ; suite 1679/2 skipped ; RC outillée GO
  0 défaut sous SW v118 ; balayage couleurs calculées « palette OK » sur
  /options structure+gex et /tracking ; moteur 0.9.0 inchangé.

## Lot 63 — livré (2026-08-06, travail continu)

- écart de cohérence réel (capture lot 56) : mini-aires des cartes
  d'indices en POLYLIGNES anguleuses au-dessus du grand C.area lissé →
  `sparkArea` trace désormais un chemin lissé MONOTONE Fritsch-Carlson
  (jamais de dépassement des données, points exacts, déterministe),
  dégradé + point actif conservés ; le langage visuel 2026 est uniforme
  sur tous les graphiques (Chart.js + SVG locaux) ;
- `sparkSvg` : zéro consommateur (grep) — code mort supprimé ;
- preuves : 5 tests rouges→verts ; suite 1684/2 skipped ; RC outillée GO
  0 défaut sous SW v119 ; navigateur : 4/4 mini-aires en courbes
  cubiques, zéro polyligne, 0 erreur console ; moteur 0.9.0 inchangé.

## Lot 64 — livré (2026-08-06, travail continu — tour d'inspection)

- audit élargi 8 pages × 2 viewports (débordements 0, boutons sans nom
  0, erreurs console 0) + nouveau critère : éléments RÉELLEMENT tronqués
  sans `title` → 3 occurrences vues en navigateur, 8 points d'appel
  `vx-truncate` sans title au grep (6 fichiers) — tous corrigés, le
  texte entier reste lisible au survol (même échappement esc()) ;
- gardien PROSPECTIF « vx-truncate ⇒ title » : classe fermée ;
- preuves : 2 tests rouges→verts ; suite 1686/2 skipped ; RC outillée GO
  0 défaut sous SW v120 ; re-balayage APRÈS : 0 élément tronqué sans
  title (desktop + mobile) ; moteur 0.9.0 inchangé.

## Lot 65 — livré (2026-08-06, travail continu — bascule RC espacées)

- angles NEUFS audités en navigateur : doublons d'id 0, liens internes
  morts 0/13, focus clavier visible 8/8 sur chaque page, SVG informatifs
  sans aria → 1 seul cas réel : le Catalyst Runway (le Regime Aura était
  déjà couvert) — corrigé en une ligne (role img + aria-label reprenant
  le verdict réel, échappé) ; re-balayage APRÈS : 0 restant ;
- CONSTAT HONNÊTE : 7 tours de qualité consécutifs (58→65) ont fermé
  toutes les classes par gardiens ; ce tour n'a produit qu'un
  micro-défaut → BASCULE en RC périodiques espacées (~30 min), dit ;
- preuves : 2 tests rouges→verts ; suite 1688/2 skipped ; RC outillée GO
  0 défaut sous SW v121 ; moteur 0.9.0 inchangé.

## RC périodique n°5 — GO (2026-08-06, surveillance espacée)

- première RC du mode espacé acté au lot 65 : suite 1688/2 skipped,
  compileall exit 0, audit outillé GO 0 défaut sous SW v121 (8 pages,
  client-log 0, parcours mémoire, CYCLE SOUVERAIN re-prouvé : altération
  refusée + restauration bouton), responsive 8×3 : 0 débordement,
  0 erreur console ; moteur 0.9.0 et main intacts ; prochaine RC ~30 min.

## RC périodique n°6 — GO (2026-08-06, surveillance espacée)

- suite 1688/2 skipped, compileall exit 0, audit outillé GO 0 défaut
  sous SW v121 (cycle souverain re-prouvé), responsive 8×3 :
  0 débordement, 0 erreur console ; moteur 0.9.0 et main intacts ;
  prochaine RC ~30 min.

## RC périodique n°7 — GO (2026-08-06, surveillance espacée)

- suite 1688/2 skipped, compileall exit 0, audit outillé GO 0 défaut
  sous SW v121 (cycle souverain re-prouvé), responsive 8×3 :
  0 débordement, 0 erreur console ; moteur 0.9.0 et main intacts ;
  prochaine RC ~30 min.

## Lot 66 — livré (2026-08-06, AUDIT TOTAL relancé par l'utilisateur)

- programme utilisateur « audit totalement complet, tout cohérent,
  pousser au maximum » traduit en volets PROUVABLES ; RC espacées
  suspendues, développement continu relancé ;
- volet routes : 137 routes GET balayées — 94×200, 41 redirections
  voulues, un seul 400 STRUCTURÉ, AUCUN 5xx ;
- volet cohérence : VIX et meilleure opportunité cohérents partout ;
  UNE incohérence réelle — tuile Breadth du briefing sur `above50`
  (50 %) NON étiquetée vs Marchés `>MM200` (45 %), et diff interne sur
  above200 → canonicalisée >MM200 + ÉTIQUETTE de métrique sur la tuile ;
  preuve APRÈS : 45 partout, nommé pareil ;
- volet boutons/console : 0 non câblé, 0 erreur ;
- preuves : 4 tests rouges→verts ; suite 1692/2 skipped ; RC outillée GO
  0 défaut sous SW v122 ; moteur 0.9.0 inchangé ;
- volets suivants (67+) : vues profondes (tous les onglets), couverture
  IBKR lecture seule, cohérence fiche ↔ opportunités, états dégradés.

## Lot 67 — livré (2026-08-06, AUDIT TOTAL volet 2 — vues profondes)

- inventaire COMPLET des vues depuis les registres `_VIEWS` (source de
  vérité) : 30 vues (Marchés ×5, Opportunités ×5, Options ×9 dont
  3 legacy servies, Journal ×5, + 6 pages/fiches) × 2 viewports =
  60 chargements ;
- critères : 0 erreur console, 0 débordement, AUCUN texte cassé
  (NaN/undefined/[object]/null — proxy de donnée mal branchée) ;
- résultat : **0 défaut sur 60 chargements** — constat honnête, aucun
  correctif requis (effet des gardiens des lots 51→66) ; lot
  documentaire, pas de bump SW ;
- suite 1692/2 skipped tenue ; moteur 0.9.0 inchangé.

## Lot 68 — livré (2026-08-06, AUDIT TOTAL volet 3 — IBKR lecture seule)

- les 4 verrous READONLY en place : `readonly=True` EN DUR dans le
  gateway (non paramétrable), `RequestTimeout=45` (gateway + scheduler),
  registre IA `FORBIDDEN_TOOLS` (tous les verbes d'ordre bloqués),
  `READONLY=True` config — aucun verbe d'ordre actif dans vertex/ ;
- refus honnêtes prouvés sous NO_IBKR : /api/ibkr/positions ok:false +
  erreur claire (jamais de position inventée), /api/pos-quotes
  live:false + ts (fraîcheur toujours portée, cache borné purgé) ;
- UI dégradée exemplaire : « P&L latent indisponible (marques IBKR hors
  ligne — aucun chiffre inventé) », n/d partout, 0 erreur console ;
- 34 gardiens dédiés verts (no_orders, ibkr_honesty, order_ticket) ;
  note doc : la docstring du gateway cite un nom de fichier de test
  obsolète (divergence documentaire, dite) ;
- verdict : SAIN, aucun correctif — lot documentaire, suite 1692/2
  skipped tenue, SW v122, moteur 0.9.0.

## Lot 69 — livré (2026-08-06, AUDIT TOTAL volet 4 — fiche ↔ Opportunités)

- croisement réel ACN/AOS/MMM (endpoints ↔ Opportunités ↔ fiche) : les
  deux moteurs divergent LÉGITIMEMENT (command ACHETER/RENFORCER vs
  Skyler canonique REFUSER 18-19/40 — gates honnêtes) et la hiérarchie
  est DITE aux deux endroits (« un score ne déclenche jamais un ordre » ;
  « la décision finale unique reste REFUSER — les verdicts techniques
  sont des entrées du moteur exécutif ») ; aucun même champ à deux
  valeurs — SAIN, vérifié ;
- UNE lacune de traçabilité corrigée : score shortlist nu → « /100 »
  (preuve APRÈS : 81 /100, 74 /100, 73 /100) — tout score affiché porte
  son échelle, partout ;
- preuves : 2 tests rouges→verts ; suite 1694/2 skipped ; RC outillée GO
  0 défaut sous SW v123 ; moteur 0.9.0 inchangé.

## RC périodique n°8 — GO (2026-08-06, surveillance espacée)

- première RC après la clôture de l'AUDIT TOTAL (bilan n°5) : suite
  1694/2 skipped tenue, compileall exit 0, audit outillé GO 0 défaut
  (8 pages, client-log 0, SW v123 servi, 404 lisible, cycle souverain :
  altération refusée 400 + restauration bouton), responsive 8×3 = 24
  chargements 0 débordement 0 erreur ;
- aucune bascule en lot corrélatif — baseline intacte, moteur 0.9.0,
  `main` intacte ; RC n°9 armée (~30 min).

## RC périodique n°9 — GO (2026-08-06, surveillance espacée)

- suite 1694/2 skipped tenue, compileall exit 0, audit outillé GO 0
  défaut (8 pages, client-log 0, SW v123 servi, 404 lisible, cycle
  souverain : altération refusée 400 + restauration bouton), responsive
  8×3 = 24 chargements 0 débordement 0 erreur ;
- aucune bascule en lot corrélatif — baseline intacte, moteur 0.9.0,
  `main` intacte ; RC n°10 armée (~30 min).

## RC périodique n°10 — GO (2026-08-06, surveillance espacée)

- suite 1694/2 skipped tenue, compileall exit 0, audit outillé GO 0
  défaut (8 pages, client-log 0, SW v123 servi, 404 lisible, cycle
  souverain : altération refusée 400 + restauration bouton), responsive
  8×3 = 24 chargements 0 débordement 0 erreur ;
- aucune bascule en lot corrélatif — baseline intacte, moteur 0.9.0,
  `main` intacte ; RC n°11 armée (~30 min).

## PROGRAMME 100 % — TERMINÉ (lots 71 → 75, voir bilan n°6 en tête)

Directive utilisateur : « Continue à tout développer et quand t'as tout à
100 tu me dis. » → sortie de la surveillance espacée, cadence resserrée
(~2 min entre lots), clôture prévue au lot 75 (RC finale + BILAN n°6 +
déclaration 100 % à l'utilisateur).

- **Lot 71 — livré** : hygiène des références. Docstring du gateway IBKR
  citait un gardien inexistant (`test_readonly_gateway`) → corrigée (cite
  les 3 vrais gardiens READONLY) + gardien prospectif « toute référence
  `tests/test_*.py` citée dans vertex/ doit exister » (balayage complet :
  1 seule vraie divergence, le reste = faux positifs chemins d'URL).
  Suite 1696/2 skipped (+2 rouges d'abord), RC outillée GO, SW v123
  (pas de bump — rien de visible).
- **Lot 72 — livré** : audit PERFORMANCE. Mesures réelles 8 pages (cache
  froid) : DCL < 300 ms en régime établi, 0 doublon, 0 ressource en
  erreur, vendor 160 kB lazy sur /analysis seul, plus gros fichiers 39-46
  kB — SAIN. 3 gardiens prospectifs de budget (64 kB/fichier, vendor
  jamais dans le shell). Suite 1699/2 skipped.
- **Lot 73 — livré** : accessibilité, angles restants. Balayage outillé
  8 pages (noms accessibles, labels, focusabilité) : 4 défauts réels sur
  /opportunities — tickers cliquables non focusables au clavier et
  délégation limitée au clic → tabindex+role sur les 3 gabarits +
  délégué clavier global Enter/Espace (vx-entities.js, prospectif).
  Balayage APRÈS : 0 défaut. Suite 1702/2 skipped, SW v124 + 4 gardiens.
- **Lot 74 — livré** : robustesse données limites. Sondes réelles :
  symboles invalides/injection/unicode/120 chars sur analysis+skyler,
  vues inconnues sur 8 pages, POST malformés sur pos-quotes — 0×5xx
  partout, 404 API JSON+nosniff (faux positif XSS de ma sonde vérifié
  aux en-têtes, dit), refus honnêtes live:false+ts. SAIN — 4 gardiens
  prospectifs. Suite 1706/2 skipped, SW v124.
- **Lot 75 — livré** : RC FINALE sur base fraîche (suite 1706/2, audit
  outillé GO, responsive 0 défaut, a11y 0 défaut) + BILAN n°6 en tête +
  déclaration 100 % faite à l'utilisateur. Retour RC espacées (~30 min).

## BOUCLE CONTINUE — EN COURS (ré-ouverte au lot 76, 2026-08-06)

Directive utilisateur : « Continue encore et encore ne t'arrête pas. »
Cadence resserrée (~2 min), tournée d'inspection perpétuelle : chaque lot
mesure un angle, corrige les défauts réels trouvés, garde la classe.

- **Lot 76 — livré** : hygiène JS/HTML. Débogage/duplications/TODO : 0
  partout ; 1 défaut réel — onglets démo design-system en `href="#"`
  (saut en haut de page) → ancres non-navigantes + gardien « plus jamais
  de href=# ». Suite 1708/2 skipped, SW v125 + 4 gardiens.
- **Lot 77 — livré** : sécurité en-têtes/contenu servi. 4 en-têtes
  présents partout (pages, API, statiques), contenu 0 email/secret/
  chemin/nom ; 1 défaut réel — `/api/desk` (données personnelles) sans
  Cache-Control → `no-store` par le middleware + gardiens. Suite 1710/2
  skipped, SW v125 (pas de bump — serveur).
- **Lot 78 — livré** : libellés français. Texte affiché 8 pages +
  sources : 0 anglais d'interface, 0 accent manquant, ponctuation
  conforme (l'espace avant « ; » est la norme FR — faux positif de la
  sonde, dit). SAIN — 2 gardiens prospectifs. Suite 1712/2 skipped.
- **Lot 79 — livré** : fraîcheur des données affichées. 2 passes
  navigateur : aucun chiffre marché sans fraîcheur accessible — les 5
  signalements stricts étaient des faux positifs (héritage de
  l'indicateur d'en-tête « Il y a X min · source » + troncature de
  sonde), vérifiés un à un. SAIN — 2 gardiens. Suite 1714/2 skipped.
- **Lot 80 — livré** : 5 parcours bout-en-bout « du réveil à la
  décision » : 14 étapes, 0 échec (outil versionné
  `tools/user_journeys.js`). Constat réel : polices sur CDN Google
  (offline + vie privée) → lot 81 = auto-hébergement. Mini-bilan
  76-80 : 2 défauts corrigés, 8 gardiens, suite 1706→1714.
- **Lot 81 — livré** : polices AUTO-HÉBERGÉES. 2 woff2 variables locaux
  (78 kB, dédupliqués aux empreintes), fonts.css local, 7 blocs CDN
  remplacés (shell + legacy), SW v126 précache les polices. Preuves :
  0 requête externe sur 8 pages, Inter/JBM chargées localement,
  parcours 14/14 avec 0 erreur console. Suite 1718/2 skipped.
- **Lot 82 — livré** : offline RÉEL. Défaut majeur — le shell canonique
  n'enregistrait JAMAIS le service worker (0 précache, offline = page
  d'erreur sur les 8 espaces) → enregistrement dans vx-shell.js (pas
  d'inline : gardien anti-reflet du fuzz 43, attrapé et dit). Preuve
  APRÈS : reload OFFLINE rendu depuis le cache, Inter offline, états
  honnêtes. Suite 1720/2 skipped, SW v127 + 4 gardiens.
- **Lot 83 — livré** : contrôles interactifs. 26 tris/onglets/selects
  cliqués en vrai sur 8 vues : l'ordre change, les vues basculent avec
  leur état visuel, 0 inerte, 0 erreur console. SAIN — outil
  tools/controls_audit.js versionné. Suite 1720/2 skipped.
- **Lot 84 — livré** : cycle desk bout-en-bout. 6/6 en navigateur :
  push (17 clés) → serveur porte le marqueur → pull restitue → 3
  backups listés → restore PAR LA ROUTE → remise en état
  last-writer-wins. Aucune perte possible constatée ; 4 listes de clés
  alignées (gardien vert). 2 gardiens API. Suite 1722/2 skipped.
- **Lot 85 — livré** : alertes + flux live. Cycle alerte 4/4 (création
  API client → localStorage → sync serveur → suppression propre) ; SSE
  sain — mes 2 sondes initiales étaient des faux positifs (pipe
  bufferisé ; onmessage vs événements nommés), vérifiés au socket brut
  puis addEventListener, dits. 3 gardiens. Suite 1725/2 skipped.

- **Lot 86 — livré** : cas limites du decision stack. 10 branches non
  couvertes identifiées (lecture complète du moteur vs 21 tests
  existants) et FIGÉES par caractérisation, nées vertes : detail=None
  honnête, score illisible jamais inventé, bornes exactes 56/66/80,
  verdict inconnu → WAIT, frontière rassis 900 s, CHOP, distribution,
  démo étiquetée, R:R absent ne punit pas, véhicule ACTION hors achat.
  Moteur 0.9.0 INTACT (diff = tests + docs). Suite 1735/2 skipped.

- **Lot 87 — livré** : façade recommendation + __VXVOCAB figées. La
  façade unique (212 lignes) n'avait AUCUN test dédié (homonyme testé
  ailleurs) → 10 caractérisations nées vertes : vocabulaire client sans
  trou (9 décisions + 7 verdicts de gestion), normalize honnête,
  discipline -20 % action / -25 % option exacte, thêta ≤14 j, cible,
  ADD/TRIM selon sous-jacent, board vide honnête. Moteur intact.
  Suite 1745/2 skipped.

- **Lot 88 — livré** : evidence + reasoning figés. 24 tests dédiés
  existants (nominal) + 10 caractérisations nées vertes sur les
  limites : gather(None) honnête, analystes sans entrée → [], force
  bornée 0-100, bornes catalyseur exactes, fondamental 0 = absent
  (jamais puni), UNKNOWN prime, contradiction CHAOS+empilées exposée,
  scénarios sans prix jamais un % inventé, comité absent sans biais,
  invalidations plafonnées. Moteurs intacts. Suite 1755/2 skipped.

- **Lot 89 — livré** : track_record figé. Le moteur d'auto-notation
  (181 lignes) n'avait aucun test dédié → 6 caractérisations nées
  vertes (ledger simulé, fichiers runtime jamais touchés) : record sans
  lignes → 0, bords _fwd/_hit_tp1 honnêtes, ledger vide → zéros,
  n<5 jamais publié, division par zéro impossible, mémo 30 min.
  Moteur intact. Suite 1761/2 skipped.

- **Lot 90 — livré** : persist + connections figés (10 tests — persist
  tolérant/fidèle sans toucher au runtime ; connections « configuré ≠
  connecté », jamais LIVE sans preuve, READONLY dit même en LIVE,
  démo étiquetée partout). Suite 1771/2 skipped.

- **Lot 91 — livré** : decide.py figé (9 caractérisations — un seul
  test existait, le gate R:R). {} → None refus honnête (hypothèse de ma
  sonde corrigée, dit), hard gates stop/régime/R:R borne 2.0 exacte,
  CHOP jamais d'achat, sur-étendu → « attendre un repli », IV-crush
  ≤ 14 j cité. Moteur intact. Suite 1780/2 skipped.

- **Lot 92 — livré** : committee.py — DÉFAUT RÉEL trouvé par la
  caractérisation : la branche « DANS LA ZONE D'ACHAT » était du code
  mort (le garde `ez < price` contredisait `in_zone`) — la fenêtre
  promise par la note ne s'ouvrait JAMAIS au repli. Corrigé
  minimalement (nominal inchangé, prouvé : 110 → ATTENDRE avec zone ;
  100 → ACHETER « DANS LA ZONE »). skyler_core 0.9.0 non touché.
  9 tests (le rouge + 8 caractérisations). Suite 1789/2 skipped.

- **Lot 93 — livré** : pivots/structure figé (8 caractérisations — il
  nourrit committee et la zone d'achat du lot 92, aucun test dédié
  n'existait). Cassure fraîche confirmée avec measured move exact,
  cassure étendue jamais poursuivie, rebond baissier = piège refusé,
  repli repris confirmé, ATR 0 sans division par zéro. Moteur intact.
  Suite 1797/2 skipped.

- **Lot 94 — livré** : contrat des routes POST figé. 12 routes sondées
  avec payloads limites : 0×5xx, refus structurés honnêtes partout
  (« symbol requis », « question vide », « scan pas encore prêt ») ;
  télémétrie client bornée (troncatures 120/300/160 exactes, line
  non-entier → None, tampon circulaire plafonné à 100). 4 tests.
  Suite 1801/2 skipped.

- **Lot 95 — livré** : filtres durs options figés (6 caractérisations
  directes — bornes DTE inclusives, delta inconnu jamais classé, refus
  documentés, PUT hors périmètre, annotations _liquidity/_anomalies).
  Repérage honnête : indicators/anomaly/events/call_selector déjà
  couverts (dit). Suite 1807/2 skipped.

- **Lot 96 — livré** : socle math du lab options figé (7 tests —
  _ncdf CDF de table, _bs dégénéré → intrinsèque jamais NaN, PARITÉ
  PUT-CALL exacte à 1e-9, golden BS 10,19 recalculé à la main : mon
  premier golden mémoire 10,27 était faux, LE MOTEUR AVAIT RAISON,
  dit ; _pct jamais de division par zéro, _star qualité d'abord, _rr
  jamais inventé). Moteur intact. Suite 1814/2 skipped.

- **Lot 97 — livré** : scoring pur figé (8 tests — tous les sous-scores
  bornés 0-100, neutres exacts sur dict vide, ROC borné ±25, fondamental
  réel vs proxy figés avec drapeau d'honnêteté, options_score(None) →
  None jamais 0 inventé, −10 IV-crush exact, double peine court+IV
  chère, confiance auto-cohérente). Moteur intact. Suite 1822/2 skipped.

- **Lot 98 — livré** : earnings + barème stratégie figés (8 tests —
  date inconnue honnête, réaction ≤2 j vs drift, run-up avec sortie
  avant annonce, refus avec chaque exigence NOMMÉE, langage de
  certitude neutralisé, bornes grade exactes, CHOP jamais un BUY,
  poids = 100). option_anomalies déjà couvert (21 tests, dit).
  Moteurs intacts. Suite 1830/2 skipped.
- **Lot 99 — livré** : broker SSE + états système figés (9 tests —
  live_stream n'avait AUCUN test direct : canal inconnu reclassé
  system, replay Last-Event-ID exact, tampon circulaire borné, client
  lent jamais bloquant (501 événements), unsubscribe idempotent,
  framing SSE nommé exact (leçon lot 85) ; status_service :
  ok/warming/degraded, rassis = avertissement pas panne, pas de
  timestamp → unknown honnête, mode demo>ibkr>cloud). Moteurs
  intacts. Suite 1839/2 skipped.

### BILAN CONSOLIDÉ n°7 — tournée « continue encore et encore » (76-100)

24 lots, PR #109 → #132 (une par lot, squash, `main` intacte),
suite **1706 → 1839 passed / 2 skipped** (+133 tests), SW v124 → v127,
skyler_core 0.9.0 JAMAIS touché, RC outillée GO à chaque lot.

- **4 défauts réels corrigés** : onglets démo `href="#"` (76) ·
  `/api/desk` sans Cache-Control → `no-store` (77) · **DÉFAUT MAJEUR :
  le shell n'enregistrait JAMAIS le service worker** — zéro offline
  depuis toujours → enregistrement vx-shell.js + précache, reload
  hors-ligne prouvé (82) · code mort « DANS LA ZONE D'ACHAT » de
  committee — seule modification moteur de la tournée (92).
- **2 chantiers** : polices auto-hébergées, 0 requête externe (81) ·
  PWA offline réel (82).
- **Programme « moteurs blindés » 86-99 : 114 caractérisations** figeant
  toute la chaîne — decision_stack, recommendation/__VXVOCAB, evidence,
  track_record, persist/connections, decide, committee, pivots, routes
  POST, contract_filter, math Black-Scholes du lab, scoring,
  earnings+barème, broker SSE + états système.
- Leçons encodées : couverture réelle = grep du NOM de module ; golden
  recalculés à la main ; sondes SSE au socket brut + événements nommés ;
  aucun `<script>` inline (fuzz anti-XSS).

Détail complet : `docs/refactor/validation/SKYLER-LOT-100.md`. Étapes
humaines restantes : validation physique TWS réel + iPhone (cache vidé,
SW v127) ; merge vers `main` sur accord explicite uniquement.

- **Lot 101 — livré** : entonnoir de chaîne options figé (8 tests —
  chain_loader n'avait qu'UN test indirect : bornes DTE constitution
  INCLUSIVES, préférées d'abord triées par distance au centre 150,
  _dist jamais fui, fenêtre strikes ±35 % exacte, spot ≤ 0 → [],
  échantillonnage à 14 pile gardant les 2 extrêmes, expiration sans
  strike plausible jamais envoyée au broker, contrat d'entrée du
  plan). market_clock déjà figé (dit). Moteur intact. Suite 1847/2
  skipped.
- **Lot 102 — livré** : gardien XSS des news figé (9 tests — la règle
  n°5 n'était testée qu'au point de sortie d'une route : balises
  retirées PUIS échappement complet, balise jamais fermée inerte,
  javascript:/data: supprimés, http(s) seul (insensible casse),
  quotes pourcent-encodées ; sentiment lexical FR/EN ; parse_rss sans
  exception + suffixe éditeur retiré ; dedupe titre normalisé/lien
  premier conservé). Moteur intact. Suite 1856/2 skipped.
- **Lot 103 — livré** : barème de liquidité figé (8 tests —
  liquidity.assess n'avait qu'un test superficiel : refus bid/ask
  nommé score 0, contrat parfait 100 zéro grief, pénalité dégressive
  4-10 % exacte sans grief, spread > 10 % jamais traitable même à
  score ≥ 40, mid absent = prudence 100 %, OI inconnu (−15) < OI
  faible (−30), volume None silencieux vs faible nommé, cumul exact
  100−45−30−10=15). expected_move/event_risk déjà figés (dit).
  Moteur intact. Suite 1864/2 skipped.
- **Lot 104 — livré** : environnement options figé (8 tests —
  score_environment n'avait que 3 tests de surface : formules exactes
  des 5 dimensions (IV médiane 20 %→100/60 %→0, IV rank inversé
  borné, spread 1 %→100/8 %→0, event risk fraction ≤7 j), IV
  textuelle jamais convertie en silence, verdict 66/45 exact,
  dimension inconnue EXCLUE de la moyenne (jamais zéro) et NOMMÉE en
  incertitude, confiance = connues/5 ; 1 sonde corrigée (valeur non
  parsable = connue mais jamais imminente — réalité figée, dite).
  Moteur intact. Suite 1872/2 skipped.
- **Lot 105 — livré** : séquence de démarrage figée (8 tests — ordre
  §10 EXACT des 8 étapes, _step jamais bloquant (ERROR + détail 200 +
  ms), ibkr jamais CONNECTED sans preuve, tradingview MISSING « 503
  honnête » vs CONFIGURED, rapport readonly/disabled-by-design,
  startup_report copie infalsifiable, ran False avant séquence).
  interpretation/overview/pulse déjà couverts (dit). Moteur intact.
  Suite 1880/2 skipped.

### MINI-BILAN tournée 101-105

5 lots, 41 tests, suite **1839 → 1880 passed / 2 skipped**, 0 défaut
moteur trouvé (les moteurs tiennent), 2 sondes à moi corrigées (dites),
SW v127 stable, skyler_core 0.9.0 intact, PR #134 → #138 : chain_loader
(entonnoir §14 — jamais toute la chaîne au broker) · news_plus (gardien
XSS règle n°5 enfin figé en direct) · liquidity (barème complet — OI
inconnu < OI faible) · environment (5 dimensions exactes — inconnue ≠
zéro) · startup (ordre §10, démarrage jamais bloquant).

- **Lot 106 — livré** : score contextuel des contrats figé (8 tests —
  contract_scorer §20 n'avait qu'une assertion de constante : score
  MULTIPLICATIF (aucun facteur ne rachète un défaut fatal), R:R < 2
  plafonné à 10, non calculable plancher 5, liquidité multiplicateur
  ≤ 1, DTE hors fenêtre ×0.75 nommé, IV rank ≥ 85 taxée ×0.6 « DTE
  long ou pas », ULTRA_CONVEX score 0 sans setup EXCEPTIONAL et
  moitié si convexité < 80 %, prime < 0.10 ×0.3). Moteur intact.
  Suite 1888/2 skipped.
- **Lot 107 — livré** : courbe de taux figée (8 tests — RateCurve
  servait de fixture partout sans test direct : repli plat 0.045 qui
  SE DIT (jamais présenté comme du marché), interpolation linéaire
  exacte, clamp aux extrémités sans extrapolation, points désordonnés
  triés, tenor exact → taux exact, contrat to_dict, rate_sensitivity
  ±50 bp exacte avec plancher 0 et None honnête). double_prob déjà
  figé (dit). Moteur intact. Suite 1896/2 skipped.
- **Lot 108 — livré** : surface de volatilité figée (8 tests —
  vol_surface n'avait que 3 tests d'intégration : realized_vol 0
  exact sur prix constants et None sur série courte, spot invalide →
  surface vide + note, IV pourries filtrées, ATM = strike le plus
  proche du spot, skew jamais inventé sans put ~10 % OTM,
  STRIKE_IV_DISLOCATION + SMILE_DISCONTINUITY nommées, IV
  rank/percentile exacts, IV_SPIKE > 1.3× médiane récente, historique
  plat → rank None jamais 0). horizon_scanners déjà couvert (dit).
  Moteur intact. Suite 1904/2 skipped.
- **Lot 109 — livré** : registre des jobs figé (8 tests —
  scheduler/registry §24 n'avait aucun test direct : snapshot ordonné
  par priorité produit (positions avant univers), jamais exécuté →
  aucune ETA inventée, job non canonique enregistré mais jamais
  exposé en UI, beat ok/erreur tronquée à 200, ETA bornée jamais
  négative (boucle en retard → 0), façade = délégation pure, snapshot
  copie infalsifiable). Moteur intact. Suite 1912/2 skipped.
- **Lot 110 — livré** : cas limites du flux figés (8 tests — repli
  mid×100 avec cost prioritaire, clé volume alternative, NaN/inf
  rejetés, OI absent → jamais un badge « frais », frontières skew
  60/40 exactes, top borne l'affichage jamais le décompte, type
  inconnu → CALL, non-dicts filtrés). Moteur intact. Suite 1920/2
  skipped.

### MINI-BILAN tournée 106-110

5 lots, 40 tests, suite **1880 → 1920 passed / 2 skipped**, 0 défaut
moteur trouvé, 2 sondes à moi ajustées (dites), SW v127 stable,
skyler_core 0.9.0 intact, PR #139 → #143 : contract_scorer (score
multiplicatif — rien ne rachète un défaut fatal) · rates (fallback
documenté, jamais d'extrapolation) · vol_surface (ATM au plus proche,
skew jamais inventé, dislocations nommées) · scheduler/registry
(priorité produit, ETA jamais négative) · flow edges (jamais « frais »
sans OI). Note d'exploitation : lot 108 livré en avance sur
« Continue » utilisateur ; renommage MCP absorbé.

- **Lot 111 — livré** : validation de configuration figée (8 tests —
  config_validation §11 n'avait aucun test direct : MISSING avec
  conséquence exacte nommée, INVALID nommé, AUCUN secret jamais exposé
  dans le rapport, alias historique TRADINGVIEW_SECRET accepté,
  espaces = MISSING, enum broker insensible à la casse, compteurs
  _summary exacts, aucune variable obligatoire — l'app démarre
  toujours en mode sûr READONLY). Moteur intact. Suite 1928/2
  skipped.
- **Lot 112 — livré** : santé du runtime IA figée (8 tests —
  ai/health §10 n'avait qu'un usage superficiel : sans clé MISSING
  avec note honnête exacte, clé ≠ preuve (CONFIGURED jamais CONNECTED
  sans appel réel), succès → CONNECTED, échec après succès → DEGRADED
  tronqué 200, le dernier appel réel fait foi, modèle défaut
  claude-sonnet-5 + override strip, clé espaces non configurée, la
  valeur de la clé jamais dans le rapport). Moteur intact. Suite
  1936/2 skipped.
- **Lot 113 — livré** : types de provenance figés (8 tests —
  data_sources/models n'avait aucun test direct : missing() honnête
  par défaut, usable exige valeur ET qualité vivante (STALE reste
  utilisable, EXPIRED/MISSING non, None jamais), 0.0/False = vraies
  valeurs (piège falsy évité), to_dict complet, warnings jamais
  partagés entre instances, AnalyticsPacket 5 familles + as_of ISO
  auto, set_source stocke un snapshot dict, aucun état partagé entre
  paquets). engines/backtest déjà couvert (dit). Moteur intact.
  Suite 1944/2 skipped.
- **Lot 114 — livré** : frontière d'unités IV figée (8 tests —
  iv_units (né du grand défaut IV %/décimal) n'avait que 4
  assertions : unité inconnue = ValueError (une unité devinée est un
  bug), NaN/inf/≤0 → None dans les deux unités, conversions exactes,
  porte legacy DÉTECTÉE ET ÉTIQUETÉE jamais muette, seuil 1.5 exact
  (1.5 pile = décimal, 1.51 = pourcentage averti), ordure → triple
  None, exports limités aux deux portes). Moteur intact. Suite
  1952/2 skipped.
- **Lot 115 — livré** : backtest recherche figé (8 tests —
  research/backtest §29 + factory.apply_costs n'avaient aucun test
  direct : rotation 0 = coût 0, chaque aller-retour se paie
  (formule exacte (spread+slippage)/100 × rotation), position 0 =
  équité plate, vide = None honnête, avertissement « walk-forward
  requis » sur CHAQUE résultat, longueurs tronquées au plus court,
  demi-position = moitié d'exposition). Moteur intact. Suite 1960/2
  skipped.

### MINI-BILAN tournée 111-115

5 lots, 40 tests, suite **1928 → 1960 passed / 2 skipped**, 0 défaut
moteur trouvé, 0 sonde corrigée (premier passage partout), SW v127
stable, skyler_core 0.9.0 intact, PR #144 → #148 : config_validation
(conséquence exacte par absence, secrets jamais exposés) · ai/health
(clé ≠ preuve — jamais CONNECTED sans appel réel) · provenance models
(STALE utilisable, 0/False vraies valeurs) · iv_units (unité devinée =
bug, legacy étiquetée) · research/backtest (un backtest n'est jamais
une preuve). Note d'exploitation : le serveur MCP des réveils a changé
deux fois de nom — absorbé, repli encodé au canevas.

- **Lot 116 — livré** : catalyseurs non-earnings figés (8 tests —
  event_engine §21/§23 n'avait aucun test : non confirmé JAMAIS dans
  l'horizon actionnable même à 5 j, type inconnu reclassé OTHER et
  dénoncé, horizon 0-30 j bornes incluses trié par proximité, fenêtre
  earnings 45 j incluse/46 exclue/passé exclu, next_events cap 3,
  avertissement nommé avec compte exact « jamais utilisés pour tenir
  une position à travers un événement »). Moteur intact. Suite
  1968/2 skipped.
- **Lot 117 — livré** : Research Factory figée (8 tests —
  factory §29 n'avait que 2 tests nominaux : transitions interdites
  refusées (IDEA ne saute jamais DEFINED, APPROVED ne redevient
  jamais une idée, RETIRED terminal), REJECTED renaît en IDEA, état
  inconnu nommé, DEFINED exige 11 champs nommés, APPROVED exige les
  12 contrôles de biais nommés + walk-forward (« un beau backtest ne
  suffit jamais »), transitions historisées, embargo réel des splits
  avec bornes exactes, passed ≥ max(2, n−1) folds positifs).
  Moteur intact. Suite 1976/2 skipped.
- **Lot 118 — livré** : lecture graphique figée (8 tests —
  chart_read (169 lignes) n'avait aucun test direct : {} → None
  honnête (sonde corrigée, dite), hiérarchie de tendance, seuils RSI
  78/60/48 exacts, indices chiffrés, accumulation prime sur
  distribution, chart_verdict 4 issues, thesis où la MÉFIANCE prime
  (distribution avant cassure), plays par profil + R:R + vent MTF).
  Moteur intact. Suite 1984/2 skipped.
  NOUVELLE DIRECTIVE reçue : lots 119+ orientés amélioration
  visuelle des graphiques page par page (« plus propres, plus beaux,
  plus développés »), en alternance avec les caractérisations.
- **Lot 119 — livré** : amélioration graphique n°1 (Aujourd'hui) —
  Catalyst Runway développé : zone d'imminence ≤ 5 j teintée
  (l'urgence se voit avant de se lire), points dimensionnés par
  impact avec halo doux, anneau de focalisation sur le prochain
  catalyseur, graduations hebdomadaires, bornes « aujourd'hui /
  horizon » nommées, étiquettes élargies, anti-collision conservé,
  tokens uniquement. SW v127 → v128 + 4 gardiens. Captures 1440
  avant/après envoyées à l'utilisateur. Suite 1984/2 skipped, RC GO.
  DIRECTIVE ESTHÉTIQUE renforcée reçue : priorité aux dégradés
  propres, traits fins, points propres, moins de chiffres empilés,
  lecture éducative et efficace — chaque page développée au max.
- **Lot 120 — livré** : amélioration graphique n°2 (Marchés) —
  lignes ultra propres au CŒUR des charts (chart-core.js) :
  endDotsPlugin (chaque série finit par un point net + son nom dans
  sa couleur — fini l'aller-retour vers la légende), softGlowPlugin
  (halo néon doux), traits affinés 1.6, dégradé area 4 arrêts.
  Bénéfice transversal : toutes les pages qui utilisent
  multiLine/area héritent de la finition. Gardien lot 52 mis à jour
  vers la nouvelle signature (délibéré). SW v128 → v129 + 4
  gardiens. Captures avant/après envoyées. Suite 1984/2, RC GO.

### MINI-BILAN tournée 116-120

5 lots (3 caractérisations + 2 graphiques), 24 tests, suite
**1960 → 1984 passed / 2 skipped**, 0 défaut moteur, PR #149 → #153,
SW v127 → v129 : event_engine (non confirmé jamais actionnable) ·
factory (un beau backtest ne suffit jamais) · chart_read (la méfiance
prime) · GRAPHIQUE Aujourd'hui (Catalyst Runway développé) · GRAPHIQUE
Marchés (lignes ultra propres transversales). Pivot de la boucle vers
l'esthétique sur directive utilisateur — chaque page au maximum,
sans autorisation demandée.

- **Lot 121 — livré** : amélioration graphique n°3 (Opportunités) —
  entonnoir « ultra propre » dans chart-core (un seul ton de marque
  en dégradé vertical brand → cyan, opacité qui décroît avec la
  profondeur, UN chiffre par étage — les % doublés supprimés —, la
  plus forte perte marquée −N discret) + zone actionnable du scatter
  teintée en dégradé positif léger. Aucun littéral couleur nouveau.
  SW v129 → v130 + 4 gardiens. Captures avant/après envoyées.
  Suite 1984/2, RC GO.
- **Lot 122 — livré** : amélioration graphique n°4 (Analyse) —
  radar en dégradé RADIAL dans chart-core (centre quasi transparent
  → bord de marque : la surface respire), points sommets nets avec
  halo, grille en opacité dégressive (l'extérieur guide, l'intérieur
  murmure), trait 1.6 jointures arrondies, id de dégradé unique par
  hôte. Bénéficiaires : scorecard des fiches Analyse + dossier
  analyste. SW v130 → v131 + 4 gardiens. Captures fiche ACN
  avant/après envoyées. Suite 1984/2, RC GO. (Démarré sur « Go »
  utilisateur sans attendre le réveil.)
- **Lot 123 — livré** : amélioration graphique n°5 (Portefeuille) —
  treemap matière VERRE dans chart-core : dégradé diagonal par tuile
  (dense → doux ; même le neutre honnête des marques hors ligne
  gagne de la profondeur), liseré fin de la couleur de la tuile au
  lieu du trait noir épais, coins arrondis, part du TOTAL (%) sur
  les grandes tuiles (le chiffre éducatif du treemap, aussi dans
  l'aria). SW v131 → v132 + 4 gardiens. Captures avant/après
  envoyées. Suite 1984/2, RC GO.
- **Lot 124 — livré** : amélioration graphique n°6 (Options) —
  payoff éducatif : le BREAKEVEN est enfin tracé (ligne warning
  « BE $X » — le chiffre éducatif d'un payoff), le SPOT aussi (ligne
  info), zones gain/perte migrées des hex en dur vers les tokens,
  trait 1.6 + halo doux (softGlowPlugin réutilisé). Arithmétique du
  contrat inchangée. SW v132 → v133 + 4 gardiens. Captures
  avant/après envoyées. Suite 1984/2, RC GO. (12 captures desktop
  de toutes les pages envoyées entre-temps sur demande.)
- **Lot 125 — livré** : amélioration graphique n°7 (Journal) —
  barres matière VERRE dans chart-core (chaque barre = dégradé de sa
  propre couleur, dense à l'extrémité de la valeur → doux vers la
  base, liseré fin, pleine au survol — TOUS les graphiques à barres
  de Vertex héritent) ; famille `.vx-stat` enfin stylée dans
  cockpit.css (les stats du Post-mortem s'affichaient COLLÉES —
  « Trades3 » — car les classes utilisées par 5 pages n'avaient
  aucun CSS : tuiles de verre, chiffres mono tabulaires, halo
  positif/négatif) ; hex en dur du track record → tokens. Aucun
  littéral couleur nouveau. SW v133 → v134 + 4 gardiens. Captures
  avant/après + preuve barres verre envoyées. Suite 1984/2, RC GO.

- **Lot 524 — livré** : **la borne du 523 est levée — 62 % → 81 % des
  chargeurs peignent — et les dix-sept libérés n'apportent AUCUN défaut.**
  Choix (b) : le 523 mesurait 55 chargeurs sur 89, 34 muets, cause dominante
  **mienne** (le résolveur reprenait les fonctions voisines mais pas les
  déclarations de module). **Extracteur calibré avant tout usage, quatre
  étages** : `SCAN_ACTION` rendue **caractère pour caractère** (retrouver le nom
  ne suffit pas, c'est la valeur qui compte — 516-A) · une constante fabriquée
  ne rend rien · 5/5 déclarations sont du JS valide chargé par node · variété
  des formes (chaîne, tableau, objet). **Gain mesuré à charge identique : 55/89
  → 72/89, +17, aucun perdu** ; 67 reprises sur 10 noms distincts ; texte peint
  7 553 → 11 410 caractères (× 1,5). **Les dix-sept apportent 0 défaut et 1
  seule occasion F1.** Accord numérique : **six occasions au total, six accords
  justes** — une de plus qu'au 523 ; l'élargissement n'a presque pas épaissi la
  preuve, **le français à compteur est rare dans ce produit** et la preuve reste
  mince. Fuite technique : **les trois mêmes fonctions qu'au 523, déjà réfutées
  comme artefacts**, reproduites à l'identique. **L'arrêt du lot** : en
  recopiant la charge du 523 j'avais **perdu l'alias `entries`** ; sans lui
  `loadTrack` cessait de peindre `[object Object]` et j'aurais annoncé que le
  résolveur avait fait disparaître un défaut — **deux choses changeaient à la
  fois**. Charge réalignée, balayage refait. **125 → 126.** **Second contrôle
  (famille 521-B)** : 2 977 déclarations en début de ligne, **729 ambiguës**
  (`el` ×25, `t` ×14…), mais **sur les 10 noms réellement repris, zéro
  ambigu** — le risque est réel et chiffré, il ne s'est pas réalisé ; et le
  résolveur n'est piloté par aucune liste de noms. Précision honnête : mon motif
  accepte l'indentation, les 2 977 ne sont donc pas toutes « de premier
  niveau ». **Troisième contrôle : le résidu a changé de propriétaire** — sur
  les 34 muets du 523, **17 parlent, 2 relèvent encore du résolveur** (`PARAMS`,
  déclarée en seconde instruction d'une ligne) **et 15 relèvent de ma charge ou
  de mes stubs**. **Les quatre chargeurs silencieux, vérifiés durement, ne
  donnent aucun dossier** : `loadBreadthInternals` **masque** son conteneur
  (honnête) ; les trois autres font un **retour sec**, mais
  `/api/opportunities/funnel` rend 7 étages et une clé
  `zero_actionable_is_valid` — le cas zéro est **explicitement traité** — et
  `vx-calendar` est servi **vide sans squelette**, donc pas de barre de
  chargement éternelle. Candidat nommé, non promu. Ce que le dépôt fait bien :
  masquer plutôt que laisser un rectangle vide, et traiter « zéro opportunité »
  comme un cas pensé. Portée : 19 % des chargeurs restent muets ; six occasions
  F1 seulement ; deux familles seulement ; charges fabriquées. Aucun code,
  aucun gardien, aucun test, aucun fichier de production touché ; rien supprimé.
  MD5 8/8 · snapshot 22 fichiers écart AUCUN · SW `td-shell-v187` · 2864 passed
  / 0 skipped. Feuille inchangée : 37 dossiers. Série 1, 2, 2, 3, 3, 0, 0, 4, 4,
  4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0. Quatre règles neuves : **524-A une seule
  chose doit changer entre deux passages** · **524-B un risque quantifié n'est
  pas un risque réalisé** · **524-C mesurer le résidu par cause, pas par
  nombre** · **524-D un `id` du HTML servi peut vivre dans un gabarit JS**.
  Rapport : `docs/refactor/validation/SKYLER-LOT-524.md`.
- **Lot 523 — livré** : **le français que le produit PEINT, mesuré par
  EXÉCUTION et non par motif.** Choix (b), dette du 516 ouverte depuis sept lots
  — « le français construit en JavaScript », 336 occurrences mal discriminées.
  La raison de l'immobilité est nommable : le seul instrument d'alors était un
  **grep**, la famille que le 522 vient de disqualifier. Le harnais node du 520
  extrait une fonction du **JS SERVI**, l'exécute, et **capture le texte
  réellement écrit dans le DOM**. **Réparation préalable du harnais** : le 520
  **stubait** `VX.states` et `Vf`, or les deux sont **servis** (`vx-core.js`
  L42/L85) — il mesurait son propre balisage. Les deux objets sont ici extraits
  du JS servi (1 814 et 2 918 car.) et évalués. **Crible calibré avant tout** :
  F1 accord numérique brisé (« 1 jours ») et F2 fuite technique (`undefined`,
  `NaN`, `[object Object]`) ; POSITIF 7/7 bien formées passent, NÉGATIF 6/6
  fautives signalées ; harnais et appareil calibrés eux aussi. **Balayage : 105
  fonctions inventoriées, 89 ciblées, 267 exécutions (3 régimes), 161 peignent,
  55 fonctions sur 89.** Aucun réseau : `VX.fetch` stubé, `globalThis.fetch`
  lève « RESEAU INTERDIT ». **F1 : zéro faute — sur CINQ occasions seulement**
  (« 1 titre », « 1 PUT » ×2, « 1 erreur », « 1 Fondamental ») ; zéro défaut sur
  cinq tirages est une preuve **mince**, pas un quitus. **F2 : trois candidats,
  TROIS RÉFUTÉS** — `loadTrack` (j'avais aliasé `entries` sur un tableau, le
  moteur rend un nombre), `loadPostmortem` (`trades_n` toujours rendu),
  `renderDiscipline` (`/api/portfolio/context` rend `available: False`, branche
  honnête ; `bounds` et `n_positions` toujours fournis sinon). **Les trois
  venaient de MA charge. 121 → 125.** **Le chiffre du 520 recompté avec
  l'appareil réel** : `/system?view=automations` A 2208 → 2031 o, B 329 →
  1987 o, C 182 → 734 o — **l'état vide réel est six fois plus gros** que
  mesuré. Les conclusions du 520 tiennent (les messages sont bien du produit) ;
  **ce sont les octets qui étaient à moi. Publiés puis corrigés : 16 → 17.** Ce
  que le dépôt fait bien et que le 520 ne pouvait pas voir : l'état vide réel
  **nomme la situation** avant d'en donner la raison, et la bannière d'erreur
  **offre une sortie** (« Réessayer », « Ouvrir Système ») ; **zéro défaut sur
  les 37 URL servies** (25 454 caractères) ; les registres relus par AST donnent
  exactement **35 vues**, confirmant le 518 par un chemin indépendant. **Second
  contrôle** : mes slugs de vues étaient **faux**, écrits de mémoire — une vue
  inexistante retombe silencieusement sur la vue par défaut ; corrigé en lisant
  les registres par AST (arrêt n° 125). Et **34 chargeurs sur 89 (38 %) n'ont
  jamais peint**, cause dominante mienne (constantes de module absentes).
  Portée : deux familles seulement ; charges fabriquées ; 38 % non mesurés.
  Aucun code, aucun gardien, aucun test, aucun fichier de production touché ;
  rien supprimé. MD5 8/8 · snapshot 22 fichiers écart AUCUN · SW
  `td-shell-v187` · 2864 passed / 0 skipped. Feuille inchangée : 37 dossiers.
  Série 1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0. Quatre
  règles neuves : **523-A ne pas stuber ce qui est servi** · **523-B un crible
  sans occasion ne prouve rien** · **523-C lire les slugs dans le registre** ·
  **523-D une fuite sous charge fabriquée n'est pas un défaut**. Rapport :
  `docs/refactor/validation/SKYLER-LOT-523.md`.
- **Lot 522 — livré** : **audit de mes propres chiffres, par la MÉTHODE et
  non par la prose.** Choix (a), dette du 515 — deux lots consécutifs ont montré
  que mes chiffres issus de motifs textuels sont faux avec régularité : le 515
  en a corrigé trois (253→38, 82→16, 44→1), le 521 trois autres. **Six chiffres
  faux en deux lots, dont un publié.** Chercher la réponse dans la PROSE des
  rapports aurait rejoué le travers audité : **la méthode d'un chiffre est dans
  le SCRIPT qui l'a produit**, et tous mes bancs sont encore là. Classement des
  115 bancs par nature de mesure (AST / ROUTE / NODE / MOTIF), calibré sur deux
  réponses connues (`l515_divent.py` doit ressortir AST — OK ;
  `l514_controle2.py`, qui a produit le 253 faux, doit ressortir MOTIF — OK) :
  **23 purement immunes · 31 mixtes · 13 reposant UNIQUEMENT sur un motif**, sur
  huit lots dont **quatre sans aucune autre mesure : 490, 491, 500, 509**. Les
  490 et 500 sont des bilans ; restent deux affirmations vérifiables sur le
  code. **Le chiffre du 509 recompté par AST** — « `_strat_tilt` est une copie
  quasi mot pour mot de `climate` », affirmation qui avait **doublé la portée du
  dossier 508-A** : identité 100 % / témoin négatif 27 % / **mesure 54 % de
  squelette, 69 % de constantes, 46 % de texte brut**. **Verdict PARTIEL.** Ce
  qui tient : **34 constantes communes sur 54** — mêmes seuils, mêmes étiquettes,
  mêmes clés ; **le défaut du 508-A est bien dupliqué et sa portée doublée reste
  juste**. Ce qui ne tient pas : « quasi mot pour mot » — `_strat_tilt` fait
  presque le double et ajoute ses propres playbooks ; c'est un **noyau de scoring
  partagé dans une fonction plus large**. **Le dossier survit, le qualificatif
  était gonflé. Publiés puis corrigés : 15 → 16.** Le « 7 barèmes » du 491 n'est
  **pas re-vérifiable** (sortie non conservée ; rejouer un banc à motif ne
  confirme rien — règle 503) : laissé ouvert plutôt que blanchi. **Second
  contrôle** : la classification porte sur des SCRIPTS, pas sur des CHIFFRES —
  **31 scripts mixtes sur 16 lots**, donc **« quatre lots » est une BORNE BASSE
  de l'exposition**. Ce que la boucle fait bien : **23 bancs sur 115 purement
  immunes**, et **quatre des huit lots à motif doublaient déjà leur mesure** —
  le réflexe du second contrôle jouait la moitié du temps avant même la règle
  515-A. Portée : **un seul chiffre recompté** ; la classification dit quels
  chiffres sont **exposés**, pas lesquels sont faux ; un motif n'est pas faux
  par principe (515-C). Aucun code, aucun gardien, aucun test, aucun fichier de
  production touché ; rien supprimé. MD5 8/8 · snapshot 22 fichiers écart AUCUN
  · SW `td-shell-v187` · 2864 passed / 0 skipped. Feuille inchangée : 37
  dossiers. Série 1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0.
  **Je n'incrémente pas le compteur d'arrêts : je n'ai arrêté aucun résultat
  faux ce lot-ci, j'en ai corrigé un déjà publié — gonfler ce compteur serait
  exactement le travers que le lot dénonce.** Rapport :
  `docs/refactor/validation/SKYLER-LOT-522.md`.
- **Lot 521 — livré** : **trois instruments, trois échecs de calibration sur le
  MÊME témoin — on ne prouve pas statiquement qu'une route ne sort pas sur le
  réseau. Voilà pourquoi cette dette dort depuis NEUF lots. Alors j'ai construit
  et VALIDÉ le verrou qui la débloquera. Aucun dossier (rang 0). AUCUNE des 23
  routes appelée.** Choix (a), la dette du 512, la plus ancienne non entamée ; son
  blocage a toujours été le même — plusieurs routes **hors liste sûre**, donc une
  innocuité réseau à établir d'abord. Chaque crible calibré sur **deux réponses
  connues** : `/api/correlations/<sym>` doit ressortir RÉSEAU, `/api/system/status`
  HORS RÉSEAU. **I · graphe d'appel par NOM** : positif OK, **négatif échoue** —
  résolution par nom partout dans le dépôt, un homonyme et le graphe explose (284
  modules). **II · graphe des IMPORTS** : **négatif échoue encore** — **importer un
  module n'est pas exécuter son réseau**, la fermeture transitive est trop
  grossière. **III · délégation vers la liste sûre** : **16 « mesurables » →  2**
  après nettoyage, parce que j'avais mis **`get`** dans la liste sûre, or il
  collisionne avec `dict.get`, `args.get`, `repo.get` — presque toute ligne de
  Python. **118 → 121**, trois arrêts dans un lot, **tous attrapés par leur propre
  témoin négatif**. **Ce que ces échecs établissent** : la limite est
  **méthodologique**, pas un défaut de soin — et c'est **la réponse à une question
  que je ne m'étais jamais posée : pourquoi cette dette ne bouge-t-elle pas ?**
  **Je la recommandais lot après lot sans voir que je recommandais une impasse.**
  **La sortie par le haut** : au lieu de prouver qu'une route ne sortira pas,
  **empêcher toute sortie** — un verrou de processus faisant lever
  `socket.socket`. La sûreté devient vraie **par construction**, et **l'échec
  devient l'information**. **Verrou construit et validé** : il **bloque** · il
  **n'abîme pas le sûr, 5/5 routes sûres répondent 200 verrou posé** · il est
  **réversible**. **Je ne l'applique à AUCUNE des 23 : outil prêt, pas
  autorisation.** **Ce que le dépôt fait bien** : les cinq routes sûres répondent
  **sans aucune sortie réseau possible** — liste empirique **confirmée par
  construction** pour elles ; et `/api/system/status` répond verrou posé alors que
  **trois cribles l'accusaient de sortir** : **c'est le produit qui avait raison,
  pas mes instruments**. Portée : **la dette du 512 reste ENTIÈRE**, ce lot mesure
  pourquoi elle résiste et fabrique l'outil ; verrou validé sur cinq routes
  seulement. Aucun fichier de production touché. MD5 8/8 · snapshot 22 fichiers
  écart AUCUN · SW `td-shell-v187` · **2864 passed / 0 skipped**. Feuille
  **inchangée : 37 dossiers**. Série **1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0,
  4, 4, 0, 0**. **Le collisionneur récurrent a un nom : `get` — troisième forme de
  la famille homonyme dans un seul lot, après le nom de FONCTION et le nom de
  MODULE. Question posée à l'humain : m'autorisez-vous à appeler les 23 routes,
  verrou réseau posé ?**

- **Lot 520 — livré** : **première mesure de ce que l'utilisateur VOIT — les
  chargeurs exécutés se comportent CORRECTEMENT, états vides honnêtes compris.
  Et j'ai failli publier un FAUX dossier de rang 2 : l'erreur JavaScript brute
  venait de MON BANC, pas du produit. Aucun dossier (rang 0).** Choix (b), dette
  du 519 : « câblée » n'est pas « peinte ». Instrument validé aux 504-511 —
  extraire la fonction du JS servi, l'exécuter sous node, capturer ce qu'elle
  écrit, **`VX.fetch` stubé, aucun appel ne sort** ; ajout de ce lot, une
  **résolution automatique des voisines** pour ne pas conclure « vue cassée »
  quand seul mon stub manque. **Résultat** : `/system?view=automations` est
  **exemplaire** — charge riche → tableau des jobs (2208 o) · charge vide `{}` →
  « Registre de jobs vide. » et « Rapport non généré (serveur fraîchement
  démarré ?) » (329 o) · fetch en échec → « Registre indisponible : HTTP 500 »
  (182 o). `/portfolio?view=options` et `/journal?view=progression` peignent
  identiquement aux trois régimes, ce qui est **normal** : elles lisent les
  données du poste, pas la charge réseau ; leur état vide est honnête.
  **J'ai failli publier un faux dossier** : mon premier régime faisait rendre
  `null` à `VX.fetch`, et la vue peignait **« Cannot read properties of null
  (reading 'jobs') »** — un message JavaScript brut dans l'interface, soit un
  dossier VISIBLE, le premier depuis le 514. Vérification dans `vx-core.js` :
  **`VX.fetch` LÈVE, elle ne rend jamais null**. Mon régime n'existe pas. Refait
  avec les deux dégradations réelles (charge `{}` — le 512 a mesuré que
  `/api/weekly` rend cela — et exception propagée), le produit répond
  honnêtement dans les deux cas. **116 → 118.** **Deux vues sur cinq non
  exécutées, et je ne les exécuterai pas** : elles appellent `/api/options/*`,
  dont l'innocuité réseau **n'est pas établie** ; lues, elles montrent un état
  vide honnête (« Saisis un symbole. »), qui est leur état d'arrivée. **Ce que le
  lot ne trouve pas est le résultat** : aucun chiffre faux, aucun squelette
  perpétuel, aucune fuite technique ; les états vides distinguent « vide » de
  « indisponible ». Après quatre lots sur l'axe du produit servi : **la surface
  visible se tient** — ce qui manque, ce sont des tests (518-A) et des portes
  d'entrée (519-A), pas de la correction. **Second contrôle** : mes stubs ne sont
  pas un navigateur ; **la charge riche est fabriquée par moi** ; **ma calibration
  de variété est mal écrite** (compare des paires, ne peut aboutir avec trois
  régimes) — publiée telle quelle (509-A), la variété étant démontrée par les
  2208/329/182 octets. **Ce que le dépôt fait bien** : `VX.fetch` lève au lieu de
  rendre null — **c'est ce qui empêche le message technique que je croyais avoir
  trouvé** ; deux tentatives de reprise avant de lever. Aucun fichier de
  production touché. MD5 8/8 · snapshot 22 fichiers écart AUCUN · SW
  `td-shell-v187` · **2864 passed / 0 skipped**. Feuille **inchangée : 37
  dossiers**. Série **1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0**.
  **Ce lot rapporte quelque chose de plus rare qu'un dossier : la preuve qu'un
  défaut que je croyais tenir n'existait pas. Première fois que l'arrêt portait
  sur un défaut VISIBLE — la catégorie que j'avais le plus envie de trouver. Le
  dossier le plus désirable est celui qu'il faut vérifier le plus durement.**

- **Lot 519 — livré** : **les 7 vues sans test FONCTIONNENT toutes. Mais 3 vues
  servies sur 35 ne sont liées depuis AUCUNE barre d'onglets — trois écrans
  complets, câblés, au contenu ENTIÈREMENT DISTINCT, qu'on n'atteint qu'en tapant
  l'URL. Dossier 519-A, rang 4.** Choix (b), suite directe du 518 : il avait
  mesuré une absence de garde, pas un contenu — **répondre 200 n'est pas afficher
  quelque chose**. **Premier résultat** : bloc propre extrait pour chaque vue,
  conteneurs recensés, chargeurs vérifiés dans le JS servi → **7 examinées, 0 au
  bloc vide, 0 sans conteneur, 0 ORPHELINE**. L'exposition du 518 est aujourd'hui
  **théorique**. **Ma calibration de variété a ÉCHOUÉ** (aucune orpheline parmi
  les sept) : la discrimination du crible reste **non démontrée sur ce lot**, et
  je le publie (509-A). **Le second contrôle a corrigé un chiffre que j'allais
  publier** : les **7 conteneurs « non visés »** sont **7 sur 7 des ENVELOPPES**
  dont le jumeau `…-body` est visé — motif « carte + corps hydraté », code normal ;
  mon crible comparait le mauvais niveau de l'arbre. **Orphelins réels : 0.
  115 → 116.** **Le dossier** : « branchée » n'est pas « atteignable ». Sur les 35
  vues servies, **32 sont liées** et **3 ne le sont depuis aucune barre** — les
  trois `_LEGACY_VIEWS` d'`options_intel_page` (`overview`, `radar`, `scenarios`).
  **Contrôle interne solide** : sur la même page, les six vues de `_VIEWS`
  ressortent liées et les trois legacy non. **Et ce ne sont pas des doublons** :
  Jaccard **0,00**, **zéro conteneur partagé** avec les vues visibles. Famille du
  **512-A** transposée du niveau route au niveau **vue**, du côté **occasion
  manquée** plutôt que déchet. **Ce que les deux lots disent ensemble** : **deux
  des trois vues inatteignables sont parmi les sept sans test** — ce qui **réduit
  la portée du 518-A à cinq vues**. Un lot qui rétrécit sa thèse de la veille en
  vaut un qui en ouvre une (507-C). **Rang 4** : rien de faux n'est montré, c'est
  **une surface de produit sans porte d'entrée** ; ce qui le distingue d'une
  curiosité, c'est que ces vues sont **maintenues et servies à chaque requête**.
  Correction pressentie : **décider entre les LIER et les retirer** — le contenu
  étant unique, **les lier est au moins aussi défendable**. **Aucun GO, ne rien
  supprimer.** **Ce que le dépôt fait bien** : les 7 vues fonctionnent ; le motif
  enveloppe/corps est propre et systématique ; 32 vues sur 35 correctement liées ;
  et les trois legacy sont **explicitement rangées** dans `_LEGACY_VIEWS` — le
  dépôt ne les cache pas. Portée : **« câblée » n'est pas « peinte »** (chargeurs
  non exécutés — dette neuve) ; le test « liée » cherche `?view=` littéral ;
  mesuré en DÉMO. Aucun fichier de production touché. MD5 8/8 · snapshot 22
  fichiers écart AUCUN · SW `td-shell-v187` · **2864 passed / 0 skipped**. Feuille
  **37 dossiers · cinq rang 4**. Série **1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0,
  4, 4**. **Deux lots de suite sur l'axe du produit servi, deux dossiers : le
  changement d'axe tient ses promesses — modestement, mais deux constats que
  personne n'avait mesurés.**

- **Lot 518 — livré** : **la dette la plus ancienne, enfin mesurée — ce ne sont
  pas « 29 vues sans empreinte » mais 27 VUES SERVIES SUR 35 dont aucun test ne
  regarde le contenu. Et mon premier banc disait le contraire. Dossier 518-A,
  rang 4.** Choix (a), dette portée depuis le lot 505 et **jamais entamée**,
  seule restante à porter sur le **produit servi**. **Deux corrections d'entrée**
  : ce ne sont **pas 37 vues mais 35** (`/` et `/analysis` n'ont **aucun
  registre** ; `/options` en a 9 dont 3 legacy) ; et **« sans empreinte » n'était
  pas la bonne question** — une empreinte publiée dans un rapport ne protège
  rien, **ce qui protège un rendu c'est un test**. **Le premier banc rassurait** :
  35 empreintes **distinctes**, repli **8/8** sur une vue fabriquée, **29 vues
  requêtées par un test** — j'allais conclure que la dette était un mythe.
  **Le second contrôle l'a renversé** : « requêtée » n'est pas « gardée ». Sur les
  35 paires réelles — **8** vues dont un test regarde le CONTENU · **16** testées
  **uniquement par un code de statut** · **11** dont aucun test ne nomme l'URL.
  **27 sur 35, soit 77 % de la surface servie, n'ont aucun test qui regarde ce
  qu'elles affichent**, et l'essentiel du « 29 » vient d'**un seul test** qui
  parcourt 21 vues sans rien vérifier d'autre que le statut. Parmi les 11 : 4
  vues par défaut (atteintes par l'URL nue, testée) et **7 non-défauts sans
  aucune trace** (`/journal?view=progression`, `/options?view=events|overview|
  radar|volatility`, `/portfolio?view=options`, `/system?view=automations`).
  **Rang 4** : rien de faux n'est montré, les 35 répondent 200 et le repli marche
  — **ce n'est pas un défaut du produit mais un défaut de protection** ; ce qui le
  distingue d'une curiosité est **l'échelle**, 77 % de la surface visible pouvant
  se vider sans que 2 864 tests bronchent. **Trouvaille secondaire** :
  `analysis_page.render_index(view)` accepte un paramètre dont le corps contient
  **zéro occurrence** — `/analysis?view=…` rend toujours la même page. **Deux
  arrêts avant publication, les deux sur mon banc** : j'ai agrégé la couverture
  **par nom de vue en perdant la page** (mélangeant les vues d'`intelligence_page`,
  page morte, et les noms fabriqués des tests négatifs) ; et j'allais publier
  « 10 vues affichent une bannière d'erreur » alors que je comptais des **classes
  présentes dans les gabarits JS inertes** — piège 495, lecture **retirée**.
  **113 → 115.** **Ce que le dépôt fait bien** : 35 empreintes distinctes, repli
  conforme au code sur 8/8 pages, zéro HTTP ≠ 200, et un test dédié protège déjà
  le repli. Portée : « sans test de contenu » n'est **pas** « cassée » — c'est une
  **exposition**, pas une panne ; le crible cherche l'URL littérale et 236 boucles
  paramétrées existent, donc **le 27 est une borne haute** ; mesuré en DÉMO.
  Aucun fichier de production touché. MD5 8/8 — **et c'était la calibration
  positive du banc** · snapshot 22 fichiers écart AUCUN · SW `td-shell-v187` ·
  **2864 passed / 0 skipped**. Feuille **36 dossiers · quatre rang 4**. Série
  **1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4**. **Le 517 disait la veine
  épuisée : c'était vrai de l'axe des INSTRUMENTS. En changeant d'axe — le produit
  servi — la première mesure rend un dossier. Leçon : une dette portée douze lots
  sans être mesurée finit par être mal énoncée ; celle-ci l'était sur le nombre,
  la nature et la conclusion.**

- **Lot 517 — livré** : **l'instrument du 516 est RÉPARÉ — il retrouve enfin son
  propre cas de référence. La zone aveugle contenait EXACTEMENT UN cas, et c'est
  le 513-A déjà connu. Le « 8 » du 516 devient 9. Aucun dossier neuf (rang 0).**
  Choix (a), la dette la plus embarrassante du 516 : mon recensement ratait **mon
  propre dossier 513-A**, `context._headline` s'assemblant morceau par morceau
  (plus long fragment « de l'univers », 13 caractères, sous le seuil). Règle
  516-A : le 516 a borné, **le 517 répare**. **Instrument neuf — l'unité n'est
  plus l'expression mais la FONCTION** : repérer les assembleuses
  (`x.append(…)` / `x += …` puis `join`), agréger tous leurs fragments et tester
  la prose sur l'**agrégat**. **La réparation a échoué au premier jet** :
  `parts.append(A if cond else B)` — l'argument est un **ternaire (`ast.IfExp`)
  qui contient** le `%`, et mon extracteur n'y descendait pas. Corrigé par
  récursion dans `IfExp`/`BoolOp`/arguments d'appel. **Sans la calibration à
  réponse connue je publiais « la famille assemblée ne contient rien » avec un
  extracteur cassé** — deuxième fois en quatre lots qu'un crible rate le défaut
  dont il est né. **112 → 113.** **Résultat, modeste et dit comme tel** : 38
  fonctions assembleuses, **11 atteignent l'écran**, **1 seule porte un nombre
  construit — le 513-A**. Total corrigé : **8 + 1 = 9**. Le « 8 » était une borne
  basse **d'exactement un**, et ce un n'est pas une découverte. **Second contrôle**
  : l'assemblage **entre fonctions** (7 jointures) et surtout les **tables de
  libellés au niveau module** — ~30 tables, **380 libellés français** hors de
  toute fonction, **mais un seul des 380 porte un gabarit, et c'est du balisage**.
  **Point décisif** : un libellé sans gabarit ne peut pas porter un nombre
  construit — **l'angle mort est réel pour le comptage des phrases et VIDE pour
  celui qui m'intéresse. Le 9 tient.** Compter 380 échappées et conclure « mon
  chiffre est très sous-estimé » aurait été faux d'un **raisonnement**, pas d'une
  mesure. **Ce que le dépôt fait bien** : les 380 libellés en tables sont un bon
  schéma (texte utilisateur regroupé, séparé de la logique), et c'est parce qu'il
  est bien rangé qu'il est statique donc sans risque ; sur les 11 phrases
  assemblées atteintes, **dix ne portent aucun nombre**. Portée : aucun dossier
  neuf ; « atteint » = octets servis **ou** charge d'une route appelée, **peint
  reste distinct** ; crible Python, le JS non traité ; scan DÉMO, **20 titres
  interrogés**. Aucun fichier de production touché. MD5 8/8 · snapshot 22 fichiers
  écart AUCUN · SW `td-shell-v187` · **2864 passed / 0 skipped**. Feuille
  **inchangée : 35 dossiers**. Série **1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0**.
  **Trois lots consécutifs sans dossier neuf, et je ne l'habille pas** : 515, 516
  et 517 ont tous servi à **réparer ou borner mon propre appareil de mesure**.
  L'hygiène était nécessaire (quinze chiffres publiés puis corrigés), mais trois
  lots de suite à mesurer mes instruments plutôt que le produit méritent d'être
  dits sans détour : **la veine d'audit sur cet axe est épuisée**. Je ne décide
  pas seule de changer de registre — je constate.

- **Lot 516 — livré** : **recensement — 457 phrases calculées, 75 atteignent
  l'écran (16 %), 8 portent un nombre construit. Et une correction du 514 : la
  liste est COUPÉE À CINQ, si bien que la phrase « top X % » que j'avais montrée
  est ÉVINCÉE dans 2 cas sur 2 sur données réelles. Aucun dossier neuf (rang 0).**
  Choix (a), recommandé deux fois et jamais pris ; crible par **AST**, pas par
  motif textuel (leçon 515-A). **Le recensement** : 457 phrases françaises
  interpolées dans les sources Python → **75 atteignent l'écran**, dont **7 via
  les octets servis** et **68 via la charge utile d'une route appelée**, et **8
  portent un nombre construit**. **Le chemin dominant n'est pas la page mais la
  charge utile — 68 sur 75, dix fois plus large que le rendu serveur direct** :
  c'est la voie par laquelle le 514-A est devenu visible. **Aucune des 8 n'est un
  dossier** : trois utilisent `int()` (troncature, « note 74 » pour 74,9) mais
  l'écart est **borné à un point sur cent** — convention d'affichage, pas
  destruction d'information (515-C) ; les cinq autres arrondissent correctement.
  **La correction du 514** : `decision_stack._result` coupe `pros` et `cons` à
  cinq. Le 514 avait mesuré sur une carte **fabriquée** aux facteurs concurrents
  rares. Sur le scan **réel** : 20 titres, **5 produisent la phrase**, **2 seulement
  la voient survivre (40 %)** — et **les DEUX cas « leader » sont évincés**
  (ACN « top 2% », AFL « top 8% »), tandis que la forme qui survit est
  **« bas X % » dans les facteurs NÉGATIFS**. **Le dossier 514-A tient** — la
  phrase atteint bien l'écran et écrira « bas 0 % » à l'échelle de production —
  **mais l'illustration que j'avais publiée était précisément la forme que les
  données réelles évincent**. Rang 2 maintenu, vitrine fausse. **Publiés puis
  corrigés : 14 → 15.** **Second contrôle : mon recensement rate son propre cas de
  référence** — `context._headline` assemble par `' · '.join(parts)` et son plus
  long fragment littéral est « de l'univers », 13 caractères, sous le seuil de
  prose : **mon dossier 513-A échappe à mon propre crible**. Mesuré : **98
  interpolées écartées pour fragment trop court**, 227 comme balisage — le « 8 »
  est une **borne basse**, publiée comme telle. Troisième angle mort, le français
  **assemblé en JavaScript** : 336 occurrences, **mais mal discriminées** (surtout
  du balisage à libellés français) — **majorant grossier, pas mesure**. **Deux
  arrêts avant publication, les deux sur mon banc** : j'interrogeais
  `/api/decision/AAPL` alors qu'**AAPL n'est pas dans le scan DÉMO** ; puis je ne
  visais que le meilleur titre, **dont la phrase est justement évincée** —
  j'allais réfuter le 514-A à tort. **110 → 112.** **Ce que le dépôt fait bien** :
  cinq des huit phrases arrondissent juste, la coupe à cinq est une **hygiène
  d'affichage délibérée**, et les 382 phrases non atteintes ne sont pas du gâchis
  (erreurs, journal, diagnostic). Portée : « atteint l'écran » = fragment présent
  dans les octets servis **ou** dans une charge appelée — qu'il soit **peint** est
  une question distincte ; crible Python et littéral ; mesuré sur le scan DÉMO.
  Aucun fichier de production touché. MD5 8/8 · snapshot 22 fichiers écart AUCUN ·
  SW `td-shell-v187` · **2864 passed / 0 skipped**. Feuille **inchangée : 35
  dossiers**. Série **1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0**. **Enseignement : un
  instrument doit retrouver son propre cas de référence. Le 514 avait échoué
  là-dessus et je l'avais réparé ; le 516 échoue à son tour, et cette fois je
  publie la BORNE plutôt que de réparer.**

- **Lot 515 — livré** : **la dette du 514 est close par un ZÉRO MESURÉ — les 38
  divisions entières du dépôt sont toutes légitimes. Mais le 514 avait publié
  253, faux d'un facteur 6,7, et j'ai attrapé TROIS artefacts de banc dans ce
  seul lot. Aucun dossier neuf (rang 0).** Choix (a), la dette créée par le 514.
  **Le chiffre du 514 était faux** : son `grep -rnE '[^/]//[^/]'` tournait **sans
  `--include=*.py`** — 253 lignes dont 17 avec « :// » (URLs) et 129 seulement
  dans un .py, le reste étant du **JS et du CSS où « // » est un COMMENTAIRE** ;
  et même dans les .py l'essentiel vit **dans des chaînes Python qui construisent
  du JavaScript**. Compté par **AST** : **`//` 253 → 38**, **`%` numérique
  82 → 16**, plus **688 formatages `'%d' % x` écartés**. **Publiés puis corrigés :
  13 → 14.** **Résultat : zéro défaut.** Les 38 classées — **19 médiane/index**
  (un index doit être entier), **9 seuil de tranche**, **5 quantité de contrats**
  (plancher **conservateur pour le risque**), **3 libellé de durée**, 2 autres.
  **Deux cas examinés et écartés** : le **libellé de durée** tronque toujours dans
  le sens « plus frais qu'en réalité », mais c'est la **convention** de tous les
  formateurs de temps relatifs et surtout **l'état `ok`/`stale`/`offline` est
  calculé sur `age_s` brut, pas sur le libellé** ; le **« tiers supérieur »** de
  `market_lens.py:46` vaut 27 % à 11 secteurs et 100 % à 1 secteur, mais
  **`market_lens` apparaît 0 fois dans le corpus servi** (seul lecteur :
  `intelligence_page.py`, **page non servie**) — **nouvelle instance de 512-A, pas
  un dossier neuf**. **Second contrôle, et deux artefacts de plus** : le JS servi
  donnait 103 `Math.floor(`, 15 `parseInt(`, 44 `| 0` ; ma séparation du vendor
  **ratait `chart.umd.min.js`** (205 ko de Chart.js, sans « vendor » dans le
  chemin) — refaite **par attribution fichier par fichier** : vendor **101 floor**,
  code applicatif servi **2**, les 9 pages **0**. Et **le `| 0` était un
  homonyme** : il capture la fin de `|| 0`, la coalescence — **43 des 44**.
  **Trentième récurrence de la famille homonyme.** Les **6** vraies troncatures du
  code servi, lues une par une, sont toutes innocentes (libellé tronqué à la
  largeur en pixels, numéro de mois, couleur hexadécimale, n° de ligne d'erreur).
  **Trois arrêts avant publication : 107 → 110**, tous dus à mes propres bancs.
  **Ce que le lot vaut, franchement** : troisième rang 0 de la veine — il **ferme**
  la dette par un zéro **mesuré**, **corrige un chiffre que j'avais publié**, et
  établit que **le dépôt fait juste** sur toute cette famille. Portée : le crible
  ne couvre que Python, les 6 sites JS ont été **lus** et non criblés ; aucun scan
  de production, aucun navigateur, aucun POST. Aucun fichier de production touché.
  MD5 8/8 · snapshot 22 fichiers écart AUCUN · SW `td-shell-v187` · **2864 passed
  / 0 skipped**. Feuille **inchangée : 35 dossiers**. Série **1, 2, 2, 3, 3, 0, 0,
  4, 4, 4, 2, 0**. **L'enseignement : trois de mes propres chiffres faux dans un
  seul lot, tous par la même cause — un motif TEXTUEL appliqué sans vérifier ce
  qu'il capture. L'AST n'a commis aucune de ces erreurs.**

- **Lot 514 — livré** : **le schéma du 513-A a une COPIE, et elle est SERVIE —
  sur la fiche d'un titre, en facteur positif d'un ACHAT FORT : « Parmi les
  meilleurs de l'univers scanné (top 0 %) ». Dossier 514-A, RANG 2, premier
  dossier VISIBLE depuis le 508.** Choix (c), règle 509-B (« chercher la copie »)
  appliquée au dossier du 513. **L'instrument et sa première calibration
  ÉCHOUÉE** : 1 140 arrondis dans le dépôt, donc crible **AST** à trois étages
  (imbriqué / variable locale / CHAMP). Calibration obligatoire — le 513-A doit
  être retrouvé : **premier jet NON**, parce que je définissais un « producteur
  d'arrondi » comme une fonction dont TOUS les `return` sont arrondis, alors que
  `_pct_rank` commence par `return None`, la garde d'absence honnête — **ma
  définition excluait exactement les producteurs bien écrits**. Corrigée :
  calibration 4/4. **Résultat** : 155 sites signalés sur 1 140 → **F1 « 100 - X »
  : 4** (dont 2 le même site de `demo.py` compté deux fois, complément légitime),
  F2 : **0**, F3 : 24, reste 127. **Deux vrais sites** : `context.py:98` (le
  513-A) et **`evidence.py:151`**. **Piège d'homonyme, 29ᵉ récurrence, sur un nom
  de MODULE** : j'ai d'abord cru la copie servie via `/api/evidence/<sym>` —
  **faux**, cette route utilise `evidence_lab`, un autre module. La vraie chaîne :
  `relative_analyst` ← `evidence.gather` ← `decision_stack.evaluate(context=…)` ←
  **`/api/decision/<sym>`** ← page **`/analysis/<sym>`** (route citée, établie au
  511). **Mesuré de bout en bout** sur une carte de 517 titres fabriquée en
  mémoire : n=20 → « top 2 % » sensé · **n=100 → bascule** · **n=517 → « top
  0 % »** ; décision complète **STRONG_BUY, grade A, `blocks_decision` False**, et
  les `pros` contiennent la phrase — **ce n'est pas un état dégradé** ; la page
  peint bien ces lignes sous « Facteurs positifs ». **Rang 2** : chiffre absurde
  peint sur une page servie dans une ligne d'aide à la décision ; **pas rang 1**
  car l'affirmation qualitative reste vraie et aucune décision ne bascule ; **pas
  rang 3/4** car ce n'est pas latent. **Second contrôle** : mon crible est
  **Python** et ne voit rien du JS — mesuré, 154 `Math.round(` et 213 `toFixed(`
  dans les octets servis, **24 contextes adjacents à une arithmétique, tous
  l'idiome de précision `Math.round(x*p)/p`, presque tous vendor : aucun n'est le
  schéma destructeur**. Angle mort mesuré et vide, mais **253 `//` et 82 `%`
  jamais criblés** — le « 4 en F1 » est un compte PYTHON, pas du dépôt (510-B).
  **Le crible a aussi retrouvé le 507-A tout seul** (conversions IV) : confirmation
  faible mais réelle, non recomptée. **Deux arrêts avant publication** : sans la
  calibration à réponse connue je publiais « le 513-A est isolé » (faux) ; et
  j'allais donner une fausse raison au caractère servi de la copie. Correction
  pressentie : la même qu'au 513 — **deux sites à traiter ensemble, pas un**.
  **Aucun GO, rien supprimé.** Portée : aucun scan de production lancé ; la
  condition `k ≤ n/100` reste non vérifiée sur données réelles ; en DÉMO la phrase
  est correcte, **le défaut est invisible dans le seul environnement exécutable** ;
  `_standing`, les percentiles bruts et « Leader de son secteur » restent corrects
  à toutes les tailles (509-C). Aucun fichier de production touché. MD5 8/8 ·
  snapshot 22 fichiers écart AUCUN · SW `td-shell-v187` · **2864 passed /
  0 skipped**. Arrêtés avant publication **105 → 107**. Feuille **35 dossiers ·
  douze rang 2**. Série **1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2** — **la veine repart** :
  trois lots latents m'avaient fait écrire que la chasse ne rendait plus rien,
  c'était vrai de l'instrument, pas du dépôt. **Le 513-A était la moitié du
  dossier.**

- **Lot 513 — livré** : **la règle 507-A retournée contre mon propre dossier
  d'hier — 512-A survit (phrase non vide 100 % du temps), mais à l'échelle de
  production elle annonce « Top 0 % de l'univers » au meilleur titre du scan.
  Dossier 513-A, rang 4.** Choix (c) : le 512 proposait d'afficher
  `context.headline` ; ma propre règle exige de mesurer l'atteignabilité avant de
  classer. **Premier résultat — 512-A tient, et mieux que publié** : sur les 20
  titres du scan DÉMO, **20 phrases non vides (100 %)**, 0 vide, **19 phrases
  distinctes sur 20** (pas une tautologie, règle 496) ; la partie secteur manque
  une fois sur deux uniquement parce que le DÉMO éparpille 20 titres sur 10
  secteurs — à n = 50, 100 et 517 elle est présente **100 %** du temps, mon 50 %
  est une **borne basse**. **Second contrôle (règle 481)** : `terminal.py:368`
  scanne `UNIVERSE[:20]` en DÉMO mais **UNIVERSE entier — 517 titres** en
  production, soit un univers **26 fois plus grand**. `_pct_rank` étant un
  mid-rank, `pct(max) = round(100 − 50k/n)` : dès que `50k/n < 0,5` l'arrondi rend
  100 et la phrase écrit **« Top 0 % »**. Mesuré : n=20 → Top 2 % (le chiffre cité
  par le 512) · **n=100 → bascule** · **n=517 → Top 0 % / Bas 0 %**. **Troisième
  contrôle — il réfute partiellement le second, et je le publie** : mon 2ᵉ banc
  imposait des scores tous distincts, or les vrais scores sont des **entiers**
  (20 scores, 17 valeurs distinctes) ; avec des ex aequo l'absurdité peut
  disparaître. **Le « Top 0 % » n'est PAS systématique** — condition exacte
  vérifiée point par point : **k ≤ 5 (= n/100) → Top 0 % ; k ≥ 6 → Top 1 %**. Et
  **ma « distribution réelle étirée » est elle-même un artefact** (étirer 20
  valeurs sur 517 fentes multiplie chaque ex aequo par 26). Ce que je peux
  affirmer : dans le scan DÉMO le score max (84) est **unique**, `k = 1`, et un
  sommet unique est le cas ordinaire. Ce que je ne peux pas affirmer : que la
  production ait `k ≤ 5` — il faudrait un scan réel de 517 titres, donc du réseau
  interdit. **Deux arrêts avant publication** : j'allais écrire « absurdité
  systématique » (faux) ; et ma première vérification de la condition était
  **fausse** (`range(0, n-k)` fabriquait des valeurs > 100, donc « le maximum »
  n'en était pas un). **Ce que cela fait au 512-A** : sa correction pressentie
  — afficher la phrase — n'est **pas applicable en l'état**, elle livrerait
  « Top 0 % de l'univers » au meilleur titre, contre l'invariant « données réelles
  uniquement ». **Le 512 avait raison sur le fond et tort sur la marche à
  suivre.** **Rang 4** parce que rien de faux n'est montré aujourd'hui et que le
  seul environnement exécutable (DÉMO, n=20) rend « Top 2 % », sensé — **le défaut
  est invisible partout où je peux le faire tourner** ; mais le jour où la phrase
  est affichée il devient un chiffre faux peint, soit rang 2 : **dossier
  conditionné à sa propre correction, cas nouveau**. **Quand le dépôt fait bien,
  le dire (509-C)** : `_standing` utilise le même percentile et reste correct à
  toutes les tailles ; les `pct_universe`/`pct_sector` sérialisés sont justes —
  seul le `100 - pct` de `_headline` détruit l'information. Correction pressentie
  : plancher « Top 1 % » ou ordinal « 1ᵉʳ sur 517 ». **Aucun GO, rien supprimé.**
  Portée : **aucun scan de production lancé**, tout ce qui concerne n=517 vient de
  cartes fabriquées en mémoire ; aucun navigateur, aucun POST, aucune route
  interdite. Aucun fichier de production touché. MD5 8/8 · snapshot 22 fichiers
  écart AUCUN · SW `td-shell-v187` · **2864 passed / 0 skipped**. Arrêtés avant
  publication **103 → 105**. Feuille **34 dossiers · trois rang 4**. Série
  **1, 2, 2, 3, 3, 0, 0, 4, 4, 4** — trois rangs 4 d'affilée, mais celui-ci
  **corrige la correction proposée par le lot précédent**.

- **Lot 512 — livré** : **les 41 routes muettes lues une par une — le brief se
  trompait : `/api/comite` ne cache rien (0 chaîne inédite sur 67). Mais un
  MOTEUR ENTIER, `context.py`, n'atteint l'écran sous AUCUNE formulation. Dossier
  512-A, rang 4.** Choix (a), la dette créée par le 511 (« je n'ai pas classé les
  41 par intention »). **Mesure, charge décodée, scan peuplé, sur les 9 routes de
  la liste SÛRE** — chaînes ≥ 8 caractères réparties entre *déjà dans les octets
  servis* / *déjà reçues par une route appelée* / *introuvables ailleurs* :
  `/api/committee-review` 44 → 15/1/**28** · `/api/brief` 30 → 17/1/**12** ·
  `/api/system/status` 20 → 15/1/4 · `/api/cockpit` 35 → 5/29/1 · `/news-feed`
  2 → 1/0/1 · **`/api/comite` 67 → 9/58/0** · **`/api/strategie` 19 → 5/14/0** ·
  **`/api/watchlist` 118 → 14/104/0** · `/api/weekly` charge vide, alimentée par
  `_weekly_loop()` jamais démarrée ici — **non jugée**. **Le brief et le 511 se
  trompaient** : ils annonçaient trois routes portant un raisonnement de comité
  invisible, il y en a **deux**. **Dossier 512-A** : les phrases introuvables
  (« Top 2% de l'univers · #1/3 dans Technology ») viennent de
  `vertex/engines/context.py:52 context_for` — percentile d'univers, percentile
  sectoriel, rang sectoriel, pairs nommés, phrase `_headline` **déjà rédigée** ;
  **un seul consommateur**, `decision_api.py:46 _ctx_for`, qui alimente
  **exactement trois routes, les trois muettes**. Corpus servi (9 pages dont la
  page détail + 33 scripts) : « de l'univers » 0 · « percentile » 0 · « #1/ » 0 ·
  « quartile » 0. **Classement des 41** : 9 exploitation · 9 appelables mesurées ·
  **23 lues mais non appelées** (drill-down par entité 12, suivi hypothétique 3,
  autonomes 8). **Trois arrêts avant publication dans un seul lot** : (1) charge
  mesurée **sans scan** — j'allais publier « `/api/comite` est vide », alors que
  ces routes lisent `scan_state` et sont vides par construction sans scan (après
  scan : 11 648 et 52 153 octets) ; (2) classe « redondant » bâtie sur des **noms
  de clé** — **28ᵉ récurrence de l'homonyme**, `/api/brief` classé dans la case
  exactement opposée à la mesure sur contenus ; (3) mon banc comparait des
  **échappements** (`March\u00e9` contre `Marché`) : recompté après décodage,
  31 → 28 et 13 → 12 — **artefact réel mais petit, aucune conclusion renversée, et
  je publie l'écart plutôt que le seul chiffre corrigé**. **Second contrôle (règle
  481)** : le cas exclu — une information à l'écran sous une autre formulation —
  écarté **par lecture** (seul producteur du dépôt, un seul consommateur, quatre
  vocabulaires absents) ; témoin positif : « régime » ressort sous **quatre**
  formulations, l'instrument sait donc voir une reformulation quand elle existe.
  **Rang 4** (étalon 454/511-A : rien de faux n'est montré) ; ce qui le distingue
  de son parent est la **précision** — un moteur, un fichier, une fonction, une
  phrase utilisateur déjà écrite : **premier élément de la veine directement
  actionnable en produit sans rien réécrire**. Correction pressentie : afficher
  `context.headline` sur la fiche d'un titre. **Aucun GO, ne rien supprimer.**
  Portée : « déjà reçue par une route appelée » n'est **pas** « affichée » ;
  **seules 9 des 41 sont mesurées**, les 23 autres classées par lecture ;
  `/api/weekly` non jugée ; les 32 routes hors liste sûre **n'ont pas été
  appelées**. Aucun fichier de production touché, rien supprimé. MD5 8/8 ·
  snapshot 22 fichiers écart AUCUN · SW `td-shell-v187` · **2864 passed /
  0 skipped**. Arrêtés avant publication **100 → 103**. Feuille **33 dossiers ·
  deux rang 4**. Série des rangs **1, 2, 2, 3, 3, 0, 0, 4, 4** : la veine rend
  désormais des **occasions manquées** plutôt que des défauts — changement de
  nature, et premier lot dont la suite naturelle est d'**ajouter** quelque chose
  à l'écran.

- **Lot 511 — livré** : **instrument NEUF « producteur sans consommateur » —
  quarante et une routes de données sur cent trois (39,8 %) ne sont demandées par
  aucun octet servi. Et j'ai corrigé mon propre chiffre TROIS FOIS. Dossier 511-A,
  rang 4.** Choix (b), la dette créée par le 510. Question jamais posée en
  transversal : **quelle part de ce que le serveur calcule n'atteint jamais
  l'écran ?** **Réponse au niveau ROUTE** (immune à l'angle mort des noms de clé) :
  `app.url_map` GET hors `/static` → **103 routes de données, 62 citées, 41 jamais
  citées**. **Nuance non masquée** : 9 des 41 sont des routes d'**exploitation**
  (`/api/rescan`, `/api/system/jobs`, `/api/validator`, `/api/healthz`, les trois
  `/api/positions/*`, les deux `/api/live/*`) — ce n'est pas du gâchis. **La part
  produit est 32/103 = 31 %**, et 39,8 % est une borne haute. **Trois corrections
  de mon propre chiffre** : (1) **49,4 % FAUX** — mon collecteur comptait les
  **clés de MAP** comme des noms de champ (les 133 « muettes » de `/scan` étaient
  des **tickers**) ; (2) 46,5 % encore fragile ; (3) au niveau route **47,6 %
  FAUX** — mon corpus n'avait pas **`/analysis/<sym>`**, pourtant établi comme
  servi dès le 502, et **8 routes en dépendaient** ; (4) **39,8 %** corpus complet.
  **Le second contrôle borne ET disqualifie le crible par clé** : le JS lit sans
  nommer — `Object.entries` 20, `Object.keys` 55, `Object.values` 6,
  destructuration 126, accès calculé `d[k]` **705** = **912 constructions**. Le
  « 173 champs jamais lus » est une **borne supérieure** ; **c'est pourquoi je
  publie le chiffre des routes**. **Piège d'homonyme, 27ᵉ récurrence, forme neuve —
  collision de préfixe** : `/api/brief` apparaît deux fois… **dans
  `/api/briefing/editorial`, une autre route** ; c'est mon compteur strict qui
  avait raison et ma vérification « plus large » qui produisait le faux positif.
  **Ce que le résultat éclaire ailleurs** : `/news-feed` n'est **jamais appelé**,
  alors que `CLAUDE.md` en fait la règle critique n°5 et qu'un gardien la protège —
  **le gardien protège une sortie que personne ne demande**, écart du même genre
  que le 381 sur `vx_kit`. **Rang 4**, étalon 454 : rien de faux n'est montré, ces
  routes ne peignent rien — c'est du **poids mort d'API** ; ce qui le distingue
  d'une curiosité, c'est l'échelle mesurée et le fait que chaque route reste un
  contrat à maintenir. **Correction pressentie : décider route par route entre
  RETIRER et BRANCHER** — `/api/comite`, `/api/committee-review`, `/api/brief`
  portent des raisonnements de comité que le produit n'affiche nulle part,
  peut-être une occasion manquée plutôt qu'un déchet. **AUCUN GO, NE RIEN
  SUPPRIMER.** **Portée : « jamais cité » n'est pas « jamais appelé » ; les 41 ne
  sont pas classées une par une par intention ; le comptage par clé est abandonné
  au profit du comptage par route ; POST hors périmètre ; aucun navigateur, aucune
  route interdite.** Aucun code, aucun test, aucun fichier de production touché,
  rien supprimé. MD5 **8/8** · snapshot 22 fichiers écart **AUCUN** · SW
  `td-shell-v187` · **2864 passed / 0 skipped**. Arrêtés avant publication
  **97 → 100**. Feuille **31 → 32 dossiers · un rang 4**. **L'instrument neuf a
  rendu un chiffre, ce que les deux lots précédents n'avaient pas fait — mais sans
  le second contrôle j'aurais publié 49,4 %, faux d'un quart.**
- **Lot 510 — livré** : **la chasse aux copies rend ZÉRO copie — et trouve les
  versions CORRECTES, écrites trois fois dans le dépôt. Puis le second contrôle
  établit que les trois sont dans du CODE MORT.** Choix (c), la règle 509-B
  appliquée aux quatre dossiers ouverts. Cinq signatures (des **formes de code**,
  pas des mots), chacune devant retrouver son site d'origine ; le témoin
  `(a50 if a50 is not None else 50)` rend **exactement les deux sites du 509**.
  **Aucune copie d'aucun des quatre défauts** : le 505-A est unique, le 506-A n'a
  qu'un second site en **vendor minifié** (coïncidence). **Le crible rend les
  versions correctes** : `vx_kit.py:92` et `candlestick-lwc.js:18` gardent `null`
  **et** `''` avant de convertir — ce que `performance_page.py:192` ne fait pas ;
  `journal.py:157` porte la version **direction-aware** qui manque au 504-A.
  **Le second contrôle les tue** : j'allais publier « la version correcte est déjà
  servie » (supposition qu'un fichier JS statique est chargé). Mesuré, avec les
  deux témoins du 381 qui se reproduisent (`vx-entities.js` **8/8**, `vx_kit`
  **0/8**) : les **trois précédents sont à 0/8 pages**, aucun n'atteint le
  navigateur. Deuxième fois en deux lots qu'une supposition de « servi » me trompe.
  **Observation avec son n** : sur **trois** idiomes, la version correcte est dans
  le code mort et la fautive dans le code servi — trois cas, pas une loi.
  **Le contrôle borne aussi mon propre crible** : la famille « inconnu aplati en
  zéro » compte **55** occurrences hors vendor (`x()||0` 1 · `?? 0` 13 ·
  `Number(x)||0` 7 · `float(x or 0)` 4 · `(x or 0)` 30) et **mon motif en couvre 1
  sur 55** — la **forme exacte** du 506-A est isolée, **pas la famille** ;
  conclure « cas unique » aurait été abusif d'un facteur cinquante-cinq.
  **Ce que le lot établit** : les quatre dossiers n'ont pas de copie littérale
  (la feuille est plus solide qu'elle aurait pu l'être) ; le **508-A reste le seul
  dossier dupliqué** ; et **la règle 509-C ne s'applique pas ici** — « le dépôt
  sait déjà faire » était vrai au 509 avec `scorecard.verdict` vivant et servi,
  c'est faux ici puisque les précédents sont morts. **Portée : crible LITTÉRAL,
  angle mort chiffré à 54/55 pour une seule famille — les « zéro copie » sont des
  zéros DE FORME ; une à deux signatures par dossier ; le 507-A n'a PAS été criblé
  (son défaut est une absence de consommateur, qu'un grep de formule ne capture
  pas) et je le dis plutôt que de le compter sans copie ; aucun navigateur, aucun
  POST.** Aucun code, aucun test, aucun fichier de production touché, rien
  supprimé, rien corrigé. MD5 **8/8** · snapshot 22 fichiers écart **AUCUN** · SW
  `td-shell-v187` · **2864 passed / 0 skipped**. Arrêtés avant publication
  **95 → 97**. Feuille **inchangée : 31 dossiers**. **Deuxième lot consécutif sans
  nouveau dossier ; la série des rangs est 1, 2, 2, 3, 3, 0, 0 — la chasse aux
  défauts ne rend plus rien de neuf, et les trois pistes restantes sont toutes de
  l'audit, aucune du produit.**
- **Lot 509 — livré** : **le cas dégradé intermédiaire, en transversal — AUCUN
  NOUVEAU DOSSIER. Trois candidats retirés sur atteignabilité, et deux résultats
  qui valent mieux.** Choix (b), la veine neuve née de la règle du 508. Question
  posée d'avance : *combien de fonctions de synthèse rendent un verdict sur une
  entrée PARTIELLE, et combien s'abstiennent ?* Six producteurs recensés **par
  leur forme**, testés sur PLEIN / PARTIEL / VIDE. **(1) Le 508-A est DEUX FOIS
  plus large que publié** : `strategy_fit._strat_tilt` est une **copie quasi mot
  pour mot** de `market_lens.climate` — mêmes poids, **même substitution
  `else 50`**, même garde limitée à l'absence totale, même **46 sans marqueur**
  sur une entrée partielle. Le rang ne change pas (c'est l'atteignabilité non
  démontrée qui le plafonne), **la portée double** : corriger `market_lens` seul
  laisserait le second exemplaire intact. **(2) Le dépôt SAIT dégrader honnêtement,
  deux modules sur quatre** : `scorecard.verdict` rend **REFUSÉ avec le marqueur
  « insuffisant »**, `context_for` expose ses **`dimensions`**. Ce n'est donc pas
  une limite d'architecture mais une **incohérence entre modules** — et la
  correction pressentie du 508 n'est pas une invention, c'est ce que `scorecard`
  fait déjà. **(3) Trois retraits sur atteignabilité (règle 507-A)** : `decide()`
  plante bien sur `clé: None` (le défaut de `.get` ne s'applique qu'à une clé
  ABSENTE) **mais sur 20 détails réels les cinq clés qu'il lit sont 20/20 présentes
  avec valeur → 20 verdicts, 0 plantage** ; `compose({})` rend `grade D ·
  confidence 58` sans garde **mais son unique appelant construit un littéral à 12
  clés toujours présentes** ; et ma thèse « les synthèses fabriquent » était **trop
  large** (2/4 portent un marqueur) → retirée. **Le contrôle négatif a ÉCHOUÉ et je
  le dis** : zéro producteur sur quatre ne s'abstient sur le partiel, donc mon banc
  n'a **aucun contre-exemple** sur cet axe ; ce qu'il montre, c'est que deux d'entre
  elles **marquent** leur incomplétude — une honnêteté différente de l'abstention.
  Conclusion plus faible que visée, publiée telle quelle. **Portée : entrées
  partielles fabriquées (le scan DEMO, lui, est réel et c'est lui qui tue le
  candidat `decide`) ; six producteurs recensés par la forme, un autre peut
  m'échapper ; 4 lignes complètes sur 6 ; aucun navigateur, aucun POST ; la
  duplication de `_strat_tilt` est établie sur le CODE, sa visibilité à l'écran ne
  l'est pas.** Aucun code, aucun test, aucun fichier de production touché, rien
  supprimé, rien corrigé. MD5 **8/8** · snapshot 22 fichiers écart **AUCUN** · SW
  `td-shell-v187` · **2864 passed / 0 skipped**. Arrêtés avant publication
  **92 → 95** ; interprétations retirées **3 → 4**. Feuille **inchangée : 31
  dossiers**, mais **508-A voit sa portée doubler**. **Premier lot sans nouveau
  dossier depuis le 503 : la règle 507-A a coûté TROIS dossiers en trois lots, et
  la veine des défauts d'affichage a un rendement mesurablement décroissant
  (1, 2, 2, 3, 3, puis zéro).**
- **Lot 508 — livré** : **`/markets`, dernière page jamais auditée — `climate()`
  note l'ABSENCE de donnée comme une donnée MOYENNE : un objet marché avec une
  seule clé non pertinente rend un verdict complet, score 46 « NEUTRE ». Dossier
  508-A, rang 3.** Avec ce lot, **les huit pages produit ont toutes été auditées
  au moins une fois**. **Le barème** : régime CHOP **6** mais **ABSENT 14** ; roro
  RISK-OFF **2** mais **ABSENT 12** ; vix stress **2** mais **ABSENT 8** ;
  `above50` absente → **50 substitué**. **L'absence est notée au-dessus de la pire
  réalité mesurable, sur la même échelle** : `climate({'foo':1})` → **46
  « NEUTRE »** quand le pire marché réel score **11 « DANGEREUX »** et le meilleur
  99. Seul `climate({})` est honnête (`None`). C'est l'invariant « donnée absente →
  n/d honnête ». **Atteignabilité** : `market_context._num()` documente rendre
  **None** pour une donnée manquante — `None` est la forme CHOISIE de l'absence,
  et c'est celle que `climate()` note moyenne ; **mais je n'ai pas observé l'état
  dégradé** (le scan DEMO remplit ses dix clés) et je le dis. **Le gardien teste
  exactement le cas qui marche** : `test_market_lens.py:20 assert climate(None) is
  None`. **Trois de mes quatre pistes se sont effondrées sous leurs propres
  contrôles**, et chacune aurait fait un dossier faux : (1) **le waterfall
  réconcilie** — poids et noms de clés identiques au moteur, et le clamp ne peut
  jamais mordre puisque les poids somment à 1,00 → retiré ; (2) **les deux seuils
  pour la même étiquette** (62 chez `climate`, 65 à l'endpoint) sont
  **invisibles** — « climate » a zéro occurrence dans 473 509 caractères servis et
  `label` n'est pas dans la réponse → retiré ; (3) **la jauge « > MM50 » qui
  affiche `above200`** est réelle et spectaculaire (71 sous l'étiquette MM50 avec
  « Participation SAINE » pendant que le détail juste en dessous écrit « Titres >
  MM200 : 71 % » — **le même écran se contredit**), **mais `above50` est toujours
  présente** dans la charge utile mesurée : **ma propre règle 507-A l'interdit** →
  ancré, non classé. Contrôle 504 appliqué : le repli **n'est pas orienté**
  (rassure 42→71, accuse 78→22). **Rang 3**, entre le 432 (rang 1) et le 454
  (rang 4) : au-dessus du 454 parce que **quelque chose de faux est montré** ; pas
  plus haut parce que l'état dégradé n'est **pas démontré en production** — la
  limite même qui m'a fait refuser un dossier au 507 — et parce que le cas vide est
  honnête. **Ce que `/markets` fait bien, mesuré** : le waterfall réconcilie ; la
  carte de détail étiquette correctement et n'affiche que les lignes fournies ;
  elle écrit sa limite (« non affichés plutôt qu'inventés ») ; `climate({})` rend
  `None`. **Portée : état dégradé non observé ; charges utiles fabriquées ; aucun
  navigateur (`loadBreadth` extraite des octets servis et exécutée sous node) ;
  aucun POST ; quatre sous-vues de `/markets` non auditées.** Aucun code, aucun
  test, aucun fichier de production touché, rien supprimé, rien corrigé. MD5
  **8/8** · snapshot 22 fichiers écart **AUCUN** · SW `td-shell-v187` · **2864
  passed / 0 skipped**. Arrêtés avant publication **89 → 92** ; publiés puis
  corrigés **13**. Feuille **30 → 31 dossiers · cinq rang 3**. **Le tour des huit
  pages est fini ; les rangs décroissent (1, 2, 2, 3, 3) — la veine des surfaces
  vierges s'épuise, et il faudra décider de changer de registre.**
- **Lot 507 — livré** : **`/options`, desk jamais audité — `iv_units` promet une
  détection d'unité « JAMAIS MUETTE » et le moteur tient parole, mais l'interface
  n'en lit AUCUN champ. Dossier 507-A, rang 3.** Choix (a)/`options`.
  **Correction d'un chiffre publié au 506** : « 30 vues servies » est **faux** —
  `/options` sert via `_ALL_VIEWS` (6 visibles **+ 3 legacy** : `overview`,
  `radar`, `scenarios`) et `/opportunities` a **cinq** vues comptées pour une.
  Total réel **37 vues servies, 8 empreintées → vingt-neuf hors empreinte**.
  Deuxième fois en deux lots que `_VIEWS`/`VIEWS` me piège. **Le contrat** :
  `iv_units.py` énonce trois fois « plus JAMAIS d'heuristique silencieuse »,
  « UNIQUE frontière tolérée », « l'appelant **DOIT** propager l'unité détectée et
  l'avertissement ». **Mesuré** (moteur en processus, board DEMO, GOOGL) :
  `iv=0.468`, `iv_detected_from='PERCENT'`, `iv_unit='DECIMAL'`, `warnings=['IV du
  board détectée en POURCENTAGE (46.8) — convertie…']`. **Le moteur propage
  exactement ce qui est exigé.** Puis sur **223 890 caractères servis** (6 vues +
  2 JS) : `iv_warning`, `iv_unit`, `POURCENTAGE`, `from_legacy_board` **tous
  absents** — et la mesure qui tranche, car un littéral absent ne prouverait rien
  si le JS rendait le tableau à l'exécution : **`.warnings` a ZÉRO occurrence**
  dans les trois scripts servis, **alors que `limitations` est rendue deux fois**.
  La page a une place pour les réserves et s'en sert ; le canal où atterrit la
  détection d'unité n'a aucun lecteur. **Le second contrôle a retiré deux tiers du
  brouillon** : (I) les sept sites de conversion hors frontière existent bien et
  le seuil documenté **1.5** diverge des quatre heuristiques inline à **3** sur la
  bande `]1.5, 3]`, **mais le board DEMO ne l'atteint jamais** (51 contrats, iv min
  28,1 · médiane 46,8 · max 61,9, zéro dans la bande) → divergence théorique, pas
  de dossier ; (II) le couple `vol_charts` (÷100) ↔ JS (×100) **se compense** →
  retiré ; (III) les deux conventions du JS **ne sont pas une incohérence**, chaque
  site respectant le contrat de SON endpoint → retiré. **Aucun gardien sur la
  propagation** : « warnings » a zéro occurrence dans les quatre tests qui gardent
  la frontière. **Rang 3**, un cran au-dessus de l'étalon **454** (rang 4, « rien
  de faux n'est montré ») sur deux critères absolus : un contrat explicite rompu
  **au dernier mètre**, et **la place existe et sert déjà**. **Pas rang 2** : aucun
  chiffre ni phrase faux, la valeur manquante est une **provenance**. **Fait ancré
  non classé** : sept sites contredisent « UNIQUE frontière », deux seuils
  incompatibles, trois divisions sans détection — le jour où un producteur émettra
  du décimal, elles rendront des IV cent fois trop petites en silence. **Portée :
  board DEMO seulement (pourcentage), je ne peux pas savoir d'ici pour le board
  réel ; aucune route `/api/options/*`, aucun POST, `/options/<sym>` jamais
  touché ; aucun navigateur ; `terminal.scan()` DEMO exécuté puis snapshot
  restauré.** Aucun code, aucun test, aucun fichier de production touché, rien
  supprimé, rien corrigé. MD5 **8/8** · snapshot 22 fichiers écart **AUCUN** · SW
  `td-shell-v187` · **2864 passed / 0 skipped**. Arrêtés avant publication
  **86 → 89** ; publiés puis corrigés **12 → 13**. Feuille **29 → 30 dossiers ·
  quatre rang 3**.
- **Lot 506 — livré** : **`/portfolio` calcule le risque affiché sur un capital de
  ZÉRO, en permanence — `myCapital` est dans le contrat de synchronisation mais
  AUCUNE ligne du dépôt ne l'écrit. Dossier 506-A, rang 2.** Choix (a)/`system`,
  la règle critique n°1. Le gardien du 381 couvre déjà liste-à-liste et
  liste-à-contrat ; reproduire n'aurait rien prouvé (**règle 503-A**), j'ai pris
  ce qu'il EXCLUT : **les listes correspondent-elles aux ÉCRITURES RÉELLES ?** Le
  chemin a mené ailleurs que prévu. **La chaîne** : `capital()` rend `null` faute
  d'écrivain (la clé n'apparaît que dans les 4 listes DESK_KEYS et dans
  l'accesseur — **aucune interface ne permet de saisir un capital**) →
  `portfolio_page.py:718` envoie `cash: E().capital()||0` = **0, toujours** →
  `PortfolioSnapshot(cash=0, provenance='REAL')` → la page peint « Risques
  priorisés ». **Mesuré en appelant les moteurs en processus, AUCUN POST** : HHI
  **0.279 → 0.009**, bêta **1.05 → 0.37**, pire stress **−10,46 % → −1,77 %**
  quand le cash monte. **Le zéro est l'hypothèse la plus alarmiste possible.**
  **Et les phrases basculent** : les trois messages sont à seuil ; sur 1 ligne à
  cash=0 la page affiche « Concentration très élevée (HHI 1.000) » et « Pire
  scénario −15,00 % », **les deux disparaissent avec 30 % de cash**. Sur un
  portefeuille diversifié aucun seuil n'est franchi — **visibilité conditionnelle,
  dite explicitement**. **Le second contrôle a fait tomber DEUX de mes propres
  résultats** : (1) mon contrôle négatif sur le bêta était **VACUEUX** — je
  comparais `None` à `None` ; refait avec des bêtas, **le bêta bouge, mon modèle
  était faux**, et la correction AGRANDIT le défaut ; (2) **accusation retirée** —
  `vxTodayBaseline` et `vxPortfolioBaseline`, non synchronisées, ont un **repli
  honnête** (« Depuis ta dernière visite », état vide explicite) : ce n'est pas un
  défaut (499, 501) ; (3) et un **zéro produit par mon propre banc** — « `/system`
  0 sous-vue » venait de ce que je cherchais `_VIEWS` au lieu de `VIEWS` ; il y en
  a **cinq**, et le brief du réveil se trompait aussi. **Sens inverse cherché
  (504)** : le défaut sur-alerte et ne peut pas sous-estimer, mais un `myCapital`
  hérité serait **figé à jamais**. **Fait ancré sans être classé** : cinq des 17
  clés synchronisées (`myRecosClosed`, `simCash`, `simClosed`, `simStart`,
  `simTrades`) ne sont **ni écrites ni lues** — poids mort, rien de faux affiché.
  **Sous-produit majeur** : `/journal` 5 vues, `/portfolio` 6, `/markets` 5,
  `/options` 6, `/system` 5, plus 3 pages sans sous-vue = **30 vues servies, 8
  empreintées — VINGT-DEUX hors de toute empreinte** ; le « MD5 8/8 » est exact
  mais couvre huit trentièmes (18 empreintes nouvelles au rapport). **Aucun
  gardien** : le seul test touchant ce cash poste `simulated:True` avec
  `cash:5000` ; le chemin réel n'est couvert par rien. **Rang 2** : pas la vue par
  défaut, le défaut **sur-alerte** (étalon **478**), visibilité conditionnelle ;
  **pas rang 3** car c'est peint, ça concerne le risque, et la cause ne se résorbe
  pas seule. **Portée : `desk_data.json` jamais ouvert ; aucun POST (reconstitution
  fidèle du handler) ; positions et cash fabriqués, seuils lus dans les octets
  servis ; aucun navigateur ; inventaire d'écritures = une borne (clés littérales
  seulement).** Aucun code, aucun test, aucun fichier de production touché, rien
  supprimé, rien corrigé. MD5 **8/8** · snapshot 22 fichiers écart **AUCUN** · SW
  `td-shell-v187` · **2864 passed / 0 skipped**. Arrêtés avant publication
  **83 → 86** ; publiés puis corrigés **12**. Feuille **28 → 29 dossiers · onze
  rang 2**.
- **Lot 505 — livré** : **`/journal?view=progression`, sous-vue jamais auditée —
  sous « Mes erreurs récurrentes diminuent-elles ? », la page écrit « la
  discipline progresse » sur une série STRICTEMENT PLATE, et « Vigilance » après
  DIX MOIS SANS UNE SEULE ERREUR. Dossier 505-A, rang 2.** Choix (b), le candidat
  désigné par le 504. **Sous-produit : les quatre empreintes qui manquaient à la
  boucle** — `journal` `87b254ef362f` · `learnings` `6a7e51204b30` ·
  `progression` `3c02ad9be276` · `track-record` `d9d406cc9135` (la référence
  connue `243699ace2d5` ne couvrait que `overview`). **La phrase** compare les
  DEUX BORNES de la série (`byMonth[dernier] <= byMonth[premier]`) : ce n'est pas
  une tendance, et le `<=` annonce l'égalité comme un progrès. **Cinq formes
  fausses sur sept** : plate 5→5→5, V inversé 2→20→2, creux puis pic 9→1→9, deux
  mois égaux 3→3 → « progresse » ; **pic puis chute 1→20→2 → « Vigilance » alors
  que c'est une amélioration massive**. **Règle 504 appliquée d'avance : le défaut
  n'est pas orienté, il flatte ET accuse.** Sur une série monotone la phrase est
  juste — les deux témoins le montrent et le dossier ne l'accuse pas là. **Le
  second contrôle (481) trouve le pire, deuxième lot d'affilée où il produit le
  résultat principal** : `byMonth` n'est incrémenté que si `e.mistake` est non
  vide, donc **un mois sans erreur n'existe pas dans la série**. Mesuré : 206
  décisions, 12 mois d'activité, **dix mois parfaits (200 décisions, zéro erreur)
  → l'axe ne porte que 2 mois sur 12**, valeurs [3,3] → « progresse » ; avec des
  bornes 5 puis 6, « Vigilance » malgré les mêmes dix mois parfaits. **Ce que le
  contrôle a fait retirer** : j'allais accuser l'axe de masquer les trous — les
  étiquettes NOMMENT les mois, accusation retirée. **Un point où la page a raison,
  mesuré et dit** : sous deux mois porteurs d'erreur, `VXCharts.card` n'est pas
  appelée et la page écrit « Aucune progression fabriquée avant d'avoir des
  faits ». **« Servi mais jamais pris » écarté** : `loadProgression()` extraite des
  octets servis et exécutée sous node, `card` appelée sur `vx-pf-prog-chart`, 857
  caractères écrits dans `#vx-pf-prog`. **Aucun gardien** : les trois assertions
  qui nomment `progression` vérifient que la vue existe, que la fonction existe et
  que la route rend 200. **Rang 2 et pas rang 1** : ce n'est pas la vue par défaut,
  le graphique est affiché à côté avec les vraies étiquettes (motif du 461), et la
  page s'abstient honnêtement quand les faits manquent. **Portée : `desk_data.json`
  jamais ouvert, journaux fabriqués en mémoire, la « vérité » de chaque ligne est
  mon jugement (les témoins monotones fixent les bornes indiscutables), aucun
  navigateur, trois sous-vues encore non auditées.** Aucun code, aucun test, aucun
  fichier de production touché, rien supprimé, rien corrigé. MD5 **8/8** · snapshot
  22 fichiers écart **AUCUN** · SW `td-shell-v187` · **2864 passed / 0 skipped**.
  Arrêtés avant publication **82 → 83** ; publiés puis corrigés **12**. Feuille
  **27 → 28 dossiers · dix rang 2**.
- **Lot 504 — livré** : **retour au PRODUIT après vingt lots de moteurs — sur
  `/journal`, page jamais auditée, le KPI « Respect des invalidations » affiche
  100 % EN VERT sur des entrées qui ne portent AUCUN stop, et 0 % EN ROUGE sur une
  petite position bien gérée. DOSSIER 504-A, rang 1.** Choix (b), la
  recommandation du 503. **Instrument : rien n'est transcrit** — `behavioral()` et
  `loadDiscipline()` sont **extraites des OCTETS SERVIS** par `/journal` (md5
  `243699ace2d5`, celui de la référence) et exécutées telles quelles sous node ;
  journaux **fabriqués en mémoire**, `desk_data.json` ni lu ni écrit. Résultat sur
  la vue par défaut : manuel LONG bien formé **50 % neutre (conforme)** · manuel
  SHORT deux stops sautés **100 % VERT** (vérité 0 %) · auto stop VIDE **100 %
  VERT** (vérité n/d) · auto stop=prix / exit=total $ **100 % VERT** (n/d) · auto
  PETITE position bien gérée **0 % ROUGE** (n/d). **Trois causes racines qui
  co-occurrent (497)** : (A) `num('')` **et** `num(null)` valent **0, pas null** —
  or `vx-entities.js:145` crée `entrySnap: {}` et `:177` écrit `stop:
  t.entrySnap?.stop ?? ''`, donc le stop vide est la **forme normale** de l'entrée
  automatique ; (B) aucune lecture de `e.dir` alors que le modal propose SHORT — le
  test est **inversé** pour un short ; (C) **unités mêlées** — l'auto écrit
  `entry`/`exit` en TOTAUX $ pendant que `stop` est un PRIX unitaire. **Du même
  défaut racine, une tautologie d'affichage : « Respect de la méthode » et
  « Qualité des entrées », affichés côte à côte, ont un écart de 0 sur les cinq
  formes que le code peut produire** — deux libellés, un seul nombre. **Second
  contrôle (481) en trois volets, et le troisième a changé la conclusion** :
  (I) « servi mais jamais pris » écarté en exécutant `loadDiscipline()` sur un DOM
  bouchonné et en lisant le HTML produit ; (II) pivot vérifié par témoin direct sur
  `num` ; (III) **j'allais publier « le défaut rassure » — c'est faux** : il rend
  aussi 0 % en rouge et accuse un trader irréprochable. **Le défaut n'est pas
  rassurant, il est ARBITRAIRE : le chiffre suit la TAILLE de la position, pas la
  discipline.** **Aucun gardien** — `test_journal_system_07.py:39` n'assert que la
  présence des identifiants, et `test_postmortem.py:29` couvre `postmortem.build()`,
  le moteur serveur : **« behavioral » désigne deux objets, vingt-sixième récurrence
  du piège des homonymes**. Rang 1 parce que le chiffre est affiché, colorié, sur la
  vue par défaut, faux **dans les deux sens**, sans gardien, et que **la phrase
  d'en-tête porte le même nombre** (motif du 433) ; pas plus haut car aucun ordre
  n'est passé et READONLY est intact. **Portée dite : `desk_data.json` jamais
  ouvert (je montre que le code PRODUIT ces formes, pas leur fréquence) ; formes
  fabriquées ; aucun navigateur ; les quatre autres sous-vues de `/journal` non
  auditées — et la référence MD5 ne couvre que la vue par défaut, donc quatre vues
  servies ne sont dans aucune empreinte de la boucle.** Aucun code, aucun test,
  aucun fichier de production touché, rien supprimé, rien corrigé. MD5 **8/8** ·
  snapshot 22 fichiers écart **AUCUN** · SW `td-shell-v187` · **2864 passed /
  0 skipped**. Arrêtés avant publication **81 → 82** ; publiés puis corrigés **12**.
  Feuille **26 → 27 dossiers · seize rang 1**.
- **Lot 503 — livré** : **la dette des huit rangs relatifs payée — aucun ne tient
  SEUL par comparaison, et le « NEUF sur vingt-quatre » du 480 est FAUX : il y en a
  QUINZE.** Choix (a) : la plus ancienne dette de fond encore ouverte (nommée au
  481), et la seule où le **bilan n°18 avait publié une affirmation non mesurée**
  (« le stock vieillit bien »). **Réponse à la question posée : 15 / 15 des sections
  comparatives portent un critère ABSOLU dans la même section — zéro exception.**
  **Trouvaille non cherchée** : mon premier banc a **reproduit le neuf du 480 à
  l'identique**, ce qui aurait dû alerter — deux instruments écrits à trois lots
  d'écart peuvent partager la même erreur. Le second banc (règle 481, sur ce que le
  premier EXCLUT) a rendu dix, puis quinze. Deux défauts, **tous deux dans mon
  camp** : (1) découpage en phrases AVANT la jonction des lignes markdown — le 433
  écrit « la conséquence est plus\nlourde qu'au 432 » ; (2) lexique exigeant
  `famille DE/DU/DES`, ratant « **la famille** 411/424/… » (454), « **au-dessus du
  463** » (464), « **comme celle du 457** » (461), « **ni le 422 … ni le 421/423 …
  entre les deux** » (424), « **différent du 407** » (417). **Le 424 est le plus
  embarrassant : le rang le plus purement relatif de la veine — son rang 2 est
  construit en encadrant deux dossiers — et c'est celui que le 480 a manqué.**
  Population **9 → 15 (62,5 %), six ajoutés, ZÉRO perdu** (sur-ensemble strict).
  **CALIB 3 est le vrai test** — élargir un lexique fait monter un compte trop
  facilement : les cinq sections citant un lot pour une MÉTHODE (437, 446, 457,
  458, 478), exclues explicitement par le 480, **restent non comparatives, 0 / 5**.
  Le zéro de la dette **contrôlé et non publié tel quel** (leçon 501) : densité des
  marqueurs absolus **4,17 / 1 000 car.** en « Classement » contre **0,00 sur 24/24**
  en « Vérifications du cycle » témoin — puis **les quinze sections lues en entier**,
  parce que le régime compte aussi les occurrences NIÉES. **Correction publiée : la
  phrase du 480 « 37,5 % des rangs sont JUSTIFIÉS par comparaison » se trompe deux
  fois**, sur le chiffre et sur le verbe — dans 12 / 15 la comparaison NOMME la
  famille pendant qu'un critère absolu porte le rang ; dans 3 seulement (424, 461,
  464) elle est porteuse, et même là un critère absolu l'accompagne. **Second
  contrôle : le bornage du 480 re-croisé sur les quinze, et il TIENT** — seul ajout
  concerné le 417, qui ne casse rien car sa comparaison **différencie** au lieu
  d'**ordonner**. « Un seul rang relatif affecté » **CONFIRMÉ sur une population
  67 % plus grande**. Limites dites : le 417 satisfait la LETTRE du 480 mais pas son
  ESPRIT (**sans lui, quatorze**) ; ce lot contrôle la **FORME** des justifications,
  **pas la VÉRITÉ** des défauts ; **la règle 491 n'est appliquée à aucun des
  quinze** ; étalons mobiles repris du 480, non re-mesurés ; **quinze est un
  plancher**. Aucun code, aucun test, aucun fichier de production touché, rien
  supprimé. MD5 **8/8** · snapshot 22 fichiers écart **AUCUN** · SW `td-shell-v187`
  · **2864 passed / 0 skipped**. Arrêtés avant publication **80 → 81** ; publiés
  puis corrigés **11 → 12**. Feuille inchangée : 26 dossiers. **Dette des huit rangs
  relatifs CLOSE** ; restent l'espion au troisième niveau et un retour au produit
  sur une surface jamais auditée.
- **Lot 502 — livré** : **la dette du coût de démarrage payée — les 4 369 lignes
  mortes coûtent NEUF MILLISECONDES et 1,49 Mo. Le devis de purge gagne son
  dernier chiffre, et ce chiffre lui RETIRE un argument.**
- **Choix (a)**, sans hésiter : dette nommée au 498, non payée au 499, 500, 501.
  **Trois reports, c'est le seuil où le 498 avait décidé d'arrêter de reporter.**
  (b) l'espion au 3ᵉ niveau et (c) les huit rangs relatifs **restent nommées**.
  **Rien supprimé.**
- **La réponse** : compilation **3,8 – 4,3 ms** · allocation à l'exécution
  **0,00 ms** · injections sur 1,43 Mo **4,50 ms** (borne inférieure) → **total
  ≈ 8 – 9 ms**, **1,49 Mo résident**, **0,7 % de l'exec de `terminal.py`**.
  **La performance n'est pas une raison de purger.**
- **La compilation est payée à CHAQUE démarrage** : `CLAUDE.md` documente
  `python terminal.py`, et le module **principal** n'est jamais mis en cache
  bytecode — **vérifié par exécution** (2 lancements comme `__main__` → aucun
  `__pycache__` ; 1 import → un `.pyc`). Deux mesures indépendantes concordent
  (écart 4,3 ms · sous-ensemble seul 3,77 ms), l'écart étant **significatif mais
  du même ordre que le bruit** (3,3 ms).
- **Le zéro de l'allocation a été VÉRIFIÉ, pas publié tel quel** (leçon 501) :
  témoin — copier 650 000 o prend 0,3 µs, donc le chronomètre voit la
  microseconde ; les littéraux sont des **constantes du code compilé**. **Le zéro
  est physique. 79 → 80.**
- **La tentative ratée a rapporté plus que la mesure réussie** : exécuter
  `terminal.py` neutralisé en mémoire **échoue** sur `terminal.py:5884` —
  le fichier **s'auto-vérifie sur le contenu de `PAGE_ENTREPRISES`** dont il
  extrait le Morning Opportunity Brief. **Une purge ferait échouer le module au
  démarrage tant que cette assertion n'est pas traitée** : ligne ajoutée au devis,
  que le 498 n'avait pas vue.
- **Second contrôle** : le coût **par requête est nul et c'est structurel** ; le
  **démarrage de processus complet** vaut **1,44 – 2,20 s**, donc la part morte y
  tombe à **0,4 – 0,6 %** — **le 0,7 % est la borne HAUTE** ; savoir si 1,49 Mo
  comptent sur la machine cible est **un arbitrage humain**, pas une mesure.
- Feuille **inchangée : 26 dossiers**.
- Cycle : aucun fichier de production touché · SW `td-shell-v187` · **MD5 8/8** ·
  `persist` redirigé **et vérifié dans chaque sous-processus** · runtime
  **22 fichiers, écart AUCUN** · suite **2864 passed / 0 skipped**.

- **Lot 501 — livré** : **l'espion d'exécution étendu aux HUIT sous-objets du
  détail — ZÉRO clé absente. Le bornage du 499 tient un niveau plus bas ; les deux
  « manques » apparents sont, l'un mon propre banc, l'autre un garde qui
  fonctionne.**
- **Choix (b)** : l'espion est l'instrument le plus fiable construit ici, et son
  périmètre était **explicitement borné à un niveau** par le 499 lui-même.
  **(a) le coût de démarrage — TROISIÈME report — et (c) les huit rangs relatifs
  restent des dettes nommées.**
- **Calibration à trois étages** : CHARGE (20 titres · **160 sous-objets
  espionnés** · 20 positions) · POSITIF DU MÊME GENRE (on retire `plan['stop']`,
  l'espion l'enregistre **8 fois**) · NÉGATIF (`plan['entry']` → 0). Bras desk :
  position **maximalement remplie** avec les 30 clés que les modèles lisent, sans
  quoi une absence serait ininterprétable.
- **Résultat : rien.** `plan` 1 620 lectures / **0 absente** · `trade` 1 520 / 0 ·
  `signals` 436 / 0 · `structure` 216 / 0 · `physics` 136 / 0 · `vertex` 72 / 0 ·
  `mtf` 68 / 0 · `series` 16 / 0. **La famille est bien un phénomène du PREMIER
  NIVEAU du détail, et de lui seul.**
- **Les deux « manques », refusés à la lecture** : `entrySnap['thesis']` 40× est
  **mon propre banc** (le second bras retire la thèse) ; `sub['options']` 68× est
  **gardé** (`decision_stack.py:176`, `isinstance(...)`, site localisé **par
  capture de pile**) et la clé **n'existe légitimement pas** — `analysis.py:203`
  appelle `compose()` sans `opt`, et la note affichée annonce **quatre**
  sous-scores. **Une clé morte suivie d'un garde qui marche n'est pas un défaut**
  (règle 499, deuxième occurrence). **77 → 79.**
- **Second contrôle** : l'espion est **aveugle à l'itération** — mesuré, **zéro**
  `.items()`/`.keys()`/`.values()` sur les huit sous-objets dans tout le code
  serveur : **l'angle mort existe et il est vide, par comptage**. Et surtout :
  `series`, `structure`, `vertex` affichaient d'abord **0 lecture** — pas
  « propre », **« jamais exercé »**. Exercices ciblés ajoutés → 16, 216 et 72
  lectures, toujours zéro absence. **Un zéro de couverture et un zéro de propreté
  sont indiscernables tant qu'on ne compte pas les lectures réussies.**
- **Trouvaille latérale** : `decision_stack._decomposition` (sous-scores,
  ajustements, note) sort à **0 occurrence** dans les octets servis — le moteur
  dont la confiance et l'accord sont affichés calcule une **traçabilité que
  personne ne peint**. Nommé, non classé.
- **Portée** : les sous-objets de **troisième niveau** ne sont pas espionnés — la
  frontière a bougé d'un cran, elle n'a pas disparu.
- Feuille **inchangée : 26 dossiers**.
- Cycle : aucun fichier de production touché · SW `td-shell-v187` · **MD5 8/8** ·
  runtime **22 fichiers, écart AUCUN** · suite **2864 passed / 0 skipped**.

- **Lot 499 — livré** : **la famille du 495 bornée par un ESPION D'EXÉCUTION à
  zéro faux positif — SEPT clés manquent sur le DÉTAIL, et ZÉRO sur tous les
  autres objets de `scan_state`. La symétrie inverse nommée au 498 N'EXISTE PAS.**
- **Choix (a)** : la veine du dernier rang 1, question décidable par la mesure.
  **(b), le coût de démarrage en millisecondes, reste une dette nommée.**
- **Changement d'instrument, et c'est le point du lot** : le 495 cherchait par
  regex (33 sorties, **29 faux positifs**) ; ici chaque objet de `scan_state` est
  une sous-classe de `dict` qui **enregistre les clés demandées et absentes**.
  **Une absence enregistrée est réelle par construction — zéro faux positif.**
- **Calibration** : charge (scan 20/20) · positif (`detail.st_fund` absent
  **132 fois**) · négatif (`detail.score` jamais absent). **32 exercices, toutes
  réponses 200**, aucune route réseau sortante.
- **Résultat** : DÉTAIL **7 clés** (`earnings_dte` 212× · `st_fund` 132× ·
  `fund_score` 132× · `rr` 92× · `st_timing` 92× · `atr` 80× · `rvol` 80×) ;
  **ROW 0** ; `portfolio`, `daily`, `market_ctx`, `committee`, `strategy`,
  `recommendations` : **0**. **Le défaut est confiné à UN objet.** Témoin de vie :
  le détail a servi `sector` 3 616 fois, `score` 1 892 — les objets ont bien été lus.
- **Le tri qui compte** : **`rr` a un repli qui FONCTIONNE** (`or plan.get('rr')`)
  → sans conséquence, et j'allais le compter comme un cinquième défaut. **Une clé
  morte suivie d'un repli qui marche n'est pas un défaut.** **`atr`** et **`rvol`**
  n'ont **aucun repli** → `stop_distance_atr = None` et `rel_volume = None`, alors
  que les valeurs existent (`plan['atr']`, `volx`/`rvol`). **0 occurrence dans les
  octets servis** → nommés, non classés. **75 → 76.**
- **Second contrôle, chiffré contre l'ancien instrument** : la regex du 495 voit
  **89 clés**, l'espion **7** ; **`atr` est INVISIBLE à la regex par construction**
  (forme parenthésée `(detail or {}).get(`), et **83 clés signalées par la regex
  n'ont jamais été vues par l'espion** (chemins non exécutés ou faux positifs).
  **Les deux instruments ne se remplacent pas — chacun voit ce que l'autre ne peut
  pas voir.**
- Feuille **inchangée : 26 dossiers**. Dernier lot de la tranche 490-499 ; **le
  lot 500 est le bilan n°18**.
- Cycle : aucun fichier de production touché · SW `td-shell-v187` · **MD5 8/8** ·
  runtime **22 fichiers, écart AUCUN** · suite **2864 passed / 0 skipped**.

- **Lot 498 — livré** : **la famille `PAGE_*` auditée — les DOUZE constantes sont
  mortes, zéro atteint une surface servie ; 61,1 % de `terminal.py` est du HTML
  jamais servi, et 1,43 Mo est reconstruit en mémoire à chaque démarrage.**
  **AUCUNE SUPPRESSION — audit, pas purge.**
- **Choix (a)** : dette nommée au 495, reportée au 496 et au 497 — **une dette
  reportée trois fois devient un évitement**. La symétrie ROW/DÉTAIL **reste une
  dette nommée**.
- **Le brief avait raison sur le point qu'il demandait de re-vérifier** :
  `PAGE_ME` commence bien à **L4741**.
- **Première calibration ÉCHOUÉE, et c'est ce qui sauve le lot** : le témoin
  positif `gnavFresh` (`terminal.py:2574`) a rendu **0** et le script s'est
  arrêté. Un instrument qui n'a jamais démontré qu'il sait voir un « présent » ne
  peut rien conclure d'un « absent ». Témoin remplacé par **le même test appliqué
  aux constantes de `vertex/ui/pages/*.py`** (règle 485) : **10 trouvées** jusqu'à
  6/6, **5 non trouvées** — exactement les modules d'interface déjà connus comme
  morts. **L'instrument distingue servi et non-servi sur le même genre d'objet.**
- **Résultat : ZÉRO sur DOUZE.** `PAGE_DAILY` 368 428 o / 1 486 lignes ·
  `PAGE_ENTREPRISES` 683 · `PAGE_ME` 449 · `PAGE_OPTIONS_DESK` 443 ·
  `PAGE_WATCHLIST` 333, plus sept construites par `_vpage` —
  **1 431 362 octets, 3 394 lignes de définition**. Aucune route n'en retourne
  aucune ; les seuls usages sont les boucles `globals()[_pg] = …` qui recopient
  d'une constante morte vers une autre.
- **Le faux positif que j'ai failli publier** : quatre constantes sont sorties
  « 1/6 fragments · SERVIE » et j'allais écrire « quatre des douze sont servies ».
  **Un fragment sur six est la signature d'un morceau PARTAGÉ** : les quatre sont
  des extraits du dictionnaire `__VXVOCAB`, injecté partout. **Tri à la lecture.**
- **Second contrôle — une constante morte peut être la SOURCE d'octets servis** :
  le fichier contient ce cas (`_NAV_CSS_CANON`/`_NAV_BUILD_CANON`/`_VXSCATTER_JS`
  extraits de `PAGE_DAILY`). Mesuré : **0/6 servis** pour les trois — **la chaîne
  d'extraction reste interne à la famille morte**. Le contrôle **confirme au lieu
  d'infirmer**, et je le dis.
- **Trouvaille latérale** : `_SCATTER_HELP_JS` vaut **la chaîne vide** —
  `_extract` n'a pas trouvé son marqueur et a rendu `''` **en silence**. Sans
  conséquence (code mort), mais c'est un **mode d'échec muet**.
- **Mesure large** (même test sur toutes les constantes chaîne > 400 o) :
  **19 constantes, toutes absentes des octets servis, 4 369 lignes / 7 153 =
  61,1 %.**
- **Aucun dossier** : c'est du code mort, pas un défaut affiché. `CLAUDE.md` dit
  déjà que la purge É1 a laissé des reliques — **ce lot ne les découvre pas, il
  les chiffre**. Le coût de démarrage est donné **en octets, pas en
  millisecondes** : non chiffré en temps. **Rien n'est supprimé** : c'est **le
  devis d'une purge éventuelle**, pas la purge.
- Feuille **inchangée : 26 dossiers**. Comptes : arrêtés avant publication
  **75 (+2)**.
- Cycle : aucun fichier de production touché · SW `td-shell-v187` · **MD5 8/8** ·
  runtime **22 fichiers, écart AUCUN** · suite **2864 passed / 0 skipped**.

- **Lot 497 — livré** : **le 495-A borné — il atteint bien `/portfolio`, mais par
  un chemin ÉTROIT et CONDITIONNEL : il n'y arrive que si la position n'a PAS de
  thèse.** Quatre faux arrêtés, dont **trois branches d'échec de mon propre banc**.
- **Choix (c)** : borner un rang 1 déjà posé plutôt qu'ouvrir une famille neuve.
  **(b), l'audit `PAGE_*`, reste une dette nommée.**
- **Règle 491 d'abord** : chaîne établie sur pièces jusqu'à la colonne
  **« Verdict moteur »** (`portfolio_page.py:460`), et `/portfolio` fetche bien
  `/api/positions/state`.
- **La condition qui change tout** (positions fabriquées en mémoire,
  `desk_data.json` jamais touché) : **sans thèse et en gain → 20 lignes, verdict
  changé 4/20** · **avec thèse et en gain → 0 ligne, la carte n'est pas rendue**
  (tout tombe en `P3_LOW`) · **sous invalidation, avec ou sans thèse → 0/20**
  (le verdict est dominé par `thesis_invalidated`). **Je refuse de publier
  « 4/20 sur /portfolio » : vrai du banc, faux du produit.**
- **Les deux défauts CO-OCCURRENT** : la carte n'apparaît que quand quelque chose
  ne va pas, et quand ce qui ne va pas est « thèse absente », le moteur est
  **aussi** aveugle au fondamental.
- **Second contrôle — les trois autres clés mortes** : `st_fund` **4/20** ·
  `earnings_dte` **2/20** · `st_timing` **0/20** · les deux premières ensemble
  **4/20, pas 6** · les trois **4/20**. **L'effet n'est PAS additif** :
  **l'effet conjoint des quatre clés égale celui de `st_fund` seule.**
- **Nommé, non classé** : avec une thèse renseignée, `thesis_health` change
  **20/20** et son échelle **s'effondre de cinq états à deux** — mais
  `thesis_health`/`overall_status` sortent à **0 occurrence** dans les octets
  servis (règles 486/491/492).
- **Quatre faux arrêtés** : (1) mon blob n'était pas lu (`blob['data']['myTrades']`
  et non `blob['myTrades']`) → « 0 changement sur 0 position », **un non-résultat
  lisible comme « aucun impact »**, et **ma calibration ne couvrait pas le cas
  zéro** ; (2) `thesis_health.assess()` sortait en retour anticipé faute de
  `thesis_text` → « inchangé 0/20 » au lieu de 20/20 ; (3) **`thesisState` de
  `/portfolio` est un homonyme client** de `thesis_health` (**24ᵉ récurrence**) ;
  (4) j'allais publier « 4/20 sur /portfolio » sans la condition d'affichage.
  **69 → 73.**
- **Leçon de méthode, chèrement payée** : trois des quatre faux étaient des
  **branches d'échec de mon banc**, et la règle « calibrer le banc sur sa propre
  validité » (492) **n'en a attrapé aucun** — elle testait la mauvaise chose.
  **Une calibration doit vérifier que le banc CHARGE quelque chose, pas seulement
  qu'il REND quelque chose de varié.**
- **Le rang 1 du 495-A n'est pas modifié** (il tient sur `/analysis`,
  inconditionnel). Ce lot ajoute une seconde surface **conditionnelle** et
  **aucun dossier neuf**. Feuille **inchangée : 26 dossiers**.
- Cycle : aucun fichier de production touché · SW `td-shell-v187` · **MD5 8/8** ·
  runtime **22 fichiers, écart AUCUN** · suite **2864 passed / 0 skipped**.

- **Lot 496 — livré** : **la veine des barèmes définitivement close — `edge /100`
  est SAIN (il atteint 100 et S+) ; mais le second contrôle montre que le R:R du
  moteur est une TAUTOLOGIE, et que « R:R visé » affiche un score /100 sous une
  étiquette de ratio.** **Dixième dette nommée payée d'affilée.**
- **Règle 491 d'abord** : chaîne établie avant tout banc, `vx_edge` non nul
  **20/20** sur le scan DEMO — l'objet mesuré est bien celui qui est peint.
- **Un dimensionnement jeté** : ma première grille faisait **1 119 744
  combinaisons × un Monte-Carlo à 1 200 chemins**. Tuée, restructurée en deux
  passes (16,5 s puis 3,7 s sur 1 604 configurations ciblées). Rien de faux
  publié, mais **j'ai dimensionné avant de mesurer le coût**.
- **Résultat — le barème est sain** : `edge` atteint **100/100**, et **les cinq
  paliers du verdict sont atteignables**, y compris `VERTEX S+` (edge ≥ 82), la
  quatrième échelle S+ du dépôt. Aucun plafond, aucun bloc bridé, aucune borne
  morte.
- **Un faux arrêté par la calibration (B)** : `institutionality` s'arrêtait à
  **99** et j'allais publier « un cinquième terme plafonné ».
  `_clamp((volx−0.8)×12, 0, 15)` donne 14,4 pour `volx = 2,0` (ma grille) et 15
  pour `volx = 2,5` → **inst 100**. **C'était ma grille, pas le moteur.**
  **68 → 69.**
- **Second contrôle** : les 16 champs lus par les cinq termes sont présents
  **20/20** (rien de mort, contrairement au 495) — mais sur les 20 détails réels,
  **`rr1/rr2/rr3` n'a qu'UNE valeur distincte : (1.0, 2.0, 3.0)**.
- **DOSSIER 442 ÉTENDU — le R:R du moteur est une tautologie** :
  `analysis.py:260-262` pose `tp1 = last + risk`, `tp2 = last + 2·risk`,
  `tp3 = last + 3·risk`, `'rr': 3.0` ; `quant_engine.rr_score` **recalcule
  `(tp_k − entry)/risk` sur des cibles qu'il a lui-même définies ainsi**. Résultat
  (1, 2, 3) **par construction, pour tout titre, toujours** — structurel, pas un
  artefact de démo. Le 442 disait « un littéral constant » : **c'est toute
  l'échelle de cibles qui est figée**. **Requalifié, pas dupliqué.** Conséquence :
  `rr_score` ne varie que par le plafonnement par la résistance — **il mesure où
  est la résistance, pas le rendement/risque.**
- **DOSSIER 496-A, RANG 2** : sur `/opportunities`, **quatre sites** affichent
  `vx_rr` — c'est-à-dire `rr_score`, une **note de 0 à 100** — sous l'étiquette
  **« R:R visé »**, qui désigne un rapport. « Edge composite » porte `/100` sur la
  même carte ; « R:R visé » ne porte rien. Le vrai rapport (`rr_detail`) sort à
  **0 occurrence** dans les octets servis. **Pas d'atténuation** : le
  « R:R structurel 3 » d'`/analysis` est sur une **autre page** (règle 487), et il
  aggrave — 3 ici, 64 là. **Rang 2 et pas rang 1** : le chiffre est ambigu, pas
  faux (règle 492).
- **Bilan de la veine** : sur les sept barèmes annoncés au 486, **deux étaient des
  homonymes, deux n'étaient pas des barèmes, un était un doublon, et les deux
  vrais sont sains.** Bornage complet, coût cinq lots.
- Feuille : **25 → 26 dossiers · quinze rang 1 · neuf rang 2 · trois rang 3.**
- Cycle : aucun fichier de production touché · SW `td-shell-v187` · **MD5 8/8** ·
  runtime **22 fichiers, écart AUCUN** · suite **2864 passed / 0 skipped**.

- **Lot 495 — livré** : **la veine des barèmes close — les « cinq » n'étaient
  que DEUX ; et en la fermant, la mesure trouve un DOSSIER RANG 1 : le moteur
  exécutif décide en aveugle sur QUATRE de ses entrées, dont le score
  fondamental.** **Premier dossier neuf depuis cinq lots**, et ce n'était pas la
  cible.
- **Choix (a)** : dette de MESURE nommée depuis le 491. L'audit `PAGE_*` reste
  une dette nommée.
- **La liste était sale, pour la deuxième fois** (après le 491) : `best.score` et
  `r.score` sont **le MÊME producteur** (`row.score`, deux sites de rendu) ;
  `rating_mean/5` est le **consensus analystes yfinance**, échelle EXTERNE ;
  `count / 10 max` est un **compte contre un plafond de portefeuille**.
  **Cinq entrées → deux barèmes réels.**
- **Le barème mesuré** : 691 200 combinaisons × 3 jeux de fondamentaux,
  calibration écrite dans le banc (`technical_score` tout allumé = 100, tout
  éteint = 0). **`risk_score` plafonne à 72** sur une échelle documentée
  « 0-100 » ; `compose()['global']` plafonne à **95**, et la borne analytique
  coïncide exactement — **cause unique : `risk ≤ 72`**.
- **Mais le chiffre AFFICHÉ n'est pas plafonné** : `analysis.py:228` ajoute
  `struct_adj ∈ [−12,+10]`, donc 100 est atteint — **jamais par la composition,
  seulement par le bonus**. → **observation, pas dossier** (règle 492). Garde
  mort de plus : `min(8, …)` dans `score_adjust` ne mord jamais (max +7).
- **DOSSIER 495-A, RANG 1** : `terminal.py:440` pose `st_fund` **sur la ROW** ;
  le DÉTAIL ne le porte pas (il porte `sub.fundamental`). Quatre lecteurs le
  cherchent pourtant sur un DÉTAIL (`strategy_os_api.py:56`,
  `recalculator.py:99`, `thesis_health.py:37`, `analysis_page.py:432`).
  **Vérifié à l'exécution** : `detail.st_fund = None` quand
  `detail.sub.fundamental = 83` **dans le même objet** ; `st_timing` écrit
  **nulle part** ; `earnings_dte` jamais posé sur le détail ; `fund_score`
  inexistant. **Quatre entrées du paquet exécutif nulles en permanence.**
- **Mesuré par A/B sur les 20 titres DEMO** : en remplissant **la seule clé
  `st_fund`**, « fundamental » quitte `unknowns` **20/20** et **la décision
  affichée en tête d'`/analysis` change 4 fois sur 20** (ACN, ALL, AOS, LNT —
  toutes **REFUSER → ATTENDRE**). **Aucune atténuation** : le champ `unknowns`
  du paquet exécutif **n'est affiché nulle part**.
- **Ce que je ne dis pas** : les 20 % viennent du scan DEMO — **taux de
  démonstration, pas fréquence de production**. Le mécanisme, lui, est certain
  (AST + exécution), et la direction est **restrictive**.
- **Second contrôle** : généralisation à toutes les lectures `detail.get('X')`,
  calibrée (positif `st_fund`, négatif `score`). 33 lectures sortent — **je n'en
  publie pas 33** : dans `decision_memory`/`skyler_journal`/`skyler_sweep` le `d`
  est un dict de décision. **Tri à la lecture → quatre certaines.** Le contrôle a
  **élargi le défaut de un à quatre** et **failli faire publier 29 faux**.
- **Trois faux arrêtés** : les 33 lectures brutes ; **`dec.unknowns` qui vient du
  `decision_stack`, pas du moteur exécutif — 23ᵉ homonyme**, le piège même du
  491 ; et l'ouverture du navigateur sur `/analysis`, annulée parce que la page
  fetche `/api/ticker/<sym>` → `options_pack` → `yf.Ticker` **sans garde DEMO**.
  **65 → 68.**
- **Le brief était incomplet, 3ᵉ fois** (490, 492, 495) : sa liste réseau **omet
  `/api/ticker/<sym>`**.
- **Dette nommée** : `edge /100` **non mesuré** — la veine est close **à un
  barème près**.
- Feuille : **24 → 25 dossiers · quinze rang 1** · huit rang 2 · trois rang 3.
- Cycle : aucun fichier de production touché · SW `td-shell-v187` · **MD5 8/8** ·
  runtime **22 fichiers, écart AUCUN** · suite **2864 passed / 0 skipped**.

- **Lot 494 — livré** : **la dette du 493 soldée aux DEUX bouts — le second
  score /40 monte à 40/40 et atteint S+, mais il n'est affiché NULLE PART ;
  le /40 qu'on VOIT plafonne à 29 et n'atteint jamais S ni S+.**
- **Ordre imposé par la règle 491** : la surface servie **d'abord**, le plafond
  ensuite. Cet ordre change le lot : la réponse à (1) interdit tout classement,
  mais elle rend (2) beaucoup plus parlant.
- **(1) Surface servie — mesuré : NON.** Corpus **42 objets · 841 916
  caractères**. Calibration écrite dans le détecteur : positif `.detail`
  (4 objets), négatif `zzz_inexistant` (0). `.pack` **0** · `score40` **0** ·
  `no_chase` **0** · `optfit` **0** · `api/cockpit` **0**. **Les deux chemins de
  production sont morts côté client** : `/api/cockpit` n'a **aucun
  consommateur**, et les **sept** lecteurs de `r.score40` vivent dans
  **`PAGE_DAILY` et `PAGE_WATCHLIST`**, que **nulle route ne retourne** ;
  `/analysis` fetche bien `/api/ticker` mais ne lit que `t.detail` et
  `t.company`. **Le second /40 est calculé pour chaque titre à chaque scan, et
  jeté.**
- **(2) Plafond — 40/40, S+ atteignable.** Deux calibrations avec sortie
  programmée : entrée vide → **18** exactement (composantes neutres calculées à
  la main), et **aucune composante restée neutre** sur l'entrée parfaite —
  **le contrôle qui manquait au 493**. Balayage **2 099 520 combinaisons** :
  MIN 8 · **MAX 40** · **S+ 3 597 fois (0,17 %)**.
- **Le contraste, résultat du lot** : `skyler_core.score40` = **29/40**, S et S+
  **inatteignables** (484-A, 485), **affiché** sur `/analysis` ;
  `scorecard.score40` = **40/40**, S+ atteignable, **affiché nulle part**.
  **Deux échelles /40 exactement à l'envers l'une de l'autre.** **Nommé, non
  classé** (règles 486/491/492).
- **Second contrôle (I) — plafond PAR SITE D'APPEL** : `terminal.py:591`
  **38/40** avec **`cata` plafonné à 4/6**, parce que l'`opt` construit en
  588-590 ne porte **jamais** `earnings_dte` ; `terminal.py:1597` **40/40**.
  **Le motif du 485 reproduit sur l'autre moteur.**
- **Second contrôle (II) — conclure par ABSENCE** : sur les **34 clés** posées
  par `options_pack`, **18 noms apparaissent** dans les octets servis, dont
  `ibkr` — qui est en réalité `data_sources.ibkr`, l'état du courtier.
  **L'absence d'un nom est une preuve forte, sa présence ne prouve rien :
  18 faux positifs sur 34, taux enfin chiffré.**
- **Trois faux arrêtés** : le motif `ibkr` nu (19 occurrences, toutes le
  courtier — **21ᵉ homonyme**) ; `d.recommendations` sur `/journal`, qui vient
  de `decision_memory` (**22ᵉ homonyme**) ; « le vocabulaire servi est
  orphelin », **réfuté** (`decision_stack.py:110` le produit). **62 → 65.**
- **Une erreur à moi, publiée hier, corrigée ici** : la ligne d'index du 493 dit
  « runtime 21 fichiers, écart AUCUN » alors que son rapport dit qu'un fichier
  **est apparu** et que le compte passe à **22**. **Publiés puis corrigés :
  10 → 11.**
- **Quatrième lot consécutif sans nouveau dossier** — feuille inchangée à
  **24**. Mais le 494 **ferme une question ouverte la veille, aux deux bouts**.
  Phrase du lot : **il y a deux scores /40 dans Vertex, et c'est le mauvais qui
  est branché.**
- Cycle : aucun fichier de production touché · SW `td-shell-v187` · **MD5 8/8** ·
  runtime **22 fichiers, écart AUCUN** · suite **2864 passed / 0 skipped**.

- **Lot 493 — livré** : **la famille « producteur constant » balayée sur tout le
  code serveur — elle ne rend RIEN de neuf ; mais le balayage découvre un SECOND
  score /40, importé en production sous l'alias `ibkr`.**
- **Choix assumé** : (b) rouvrir la famille qui a donné deux rangs 1, plutôt que
  (a) finir la veine des barèmes — **(a) reste une dette nommée**, chiffrée à un
  seul traçage pour trois cibles.
- **Calibration ÉCHOUÉE du premier coup, et c'est ce qui sauve le lot** : témoin
  positif `'rr'` ressorti **non constant**, arrêt immédiat. Diagnostic : **`'rr'`
  a 12 sites dans 8 modules, tous calculés sauf `analysis.py:262`** — **j'agrégeais
  par nom de clé sur tout le dépôt : l'homonyme au niveau du CHAMP**. Corrigé en
  **(fichier, clé)**.
- **Résultat** : onze champs numériques constants dont le nom est lu dans les
  octets servis — **dix légitimes** (TTL, prix de démo, poids, table de points)
  et **un déjà classé** (`rr 3.0`, dossier 442). **La famille est close par la
  mesure : aucun défaut neuf sous cette forme.**
- **Trouvaille latérale** : `scorecard.py:178` déclare `'max': 40` — **un second
  score /40**, appelé en production (`terminal.py:591`, `:1597`) via
  `from vertex.engines import scorecard as **ibkr**`. **Vingtième homonyme, par
  alias d'import : en 493 lots la boucle n'avait jamais vu qu'il existe DEUX
  scores /40.**
- **Et je n'ai pas établi son plafond** : mon banc rendait « 25/40 », **non
  publié comme plafond** — les composantes montrent les branches **neutres**
  (`Fondamentaux 5/8`, `Option Fit 4/6`), donc l'entrée fabriquée n'est pas lue.
  **Dette nommée.**
- **Second contrôle — le détecteur ne voit que les dicts littéraux** : ni
  `out['k']=5`, ni un `return`, **ni un argument par défaut**. Or le 492 a trouvé
  exactement cela (`_num(…, 55)`) : **mon recensement aurait manqué la trouvaille
  du lot précédent.** La famille est vide **sous cette forme**, pas en général.
- **Trois faux arrêtés** : l'agrégation par nom de clé (stoppée par la
  calibration), l'extraction sur `score` au lieu de `score40` (« −1 » lisible
  comme « rien trouvé »), et le banc tombé dans les branches neutres. **59 → 62.**
- **Troisième lot consécutif sans nouveau dossier** — les veines ouvertes sont
  mesurées et ne rendent plus. Le lot apporte néanmoins **la preuve qu'une
  famille peut être close par la mesure**.
- Feuille **inchangée** : 24 dossiers · quatorze rang 1 · huit rang 2 · trois rang 3.
- **Un fichier runtime est APPARU** : `desk_backup_20260810.json`, créé par la
  suite au basculement de date. **Comportement caractérisé au 388**, pas une
  pollution. **Non supprimé** — effacer une sauvegarde du desk serait destructeur
  et l'invariant l'interdit ; **gitignoré** (vérifié), contenu **copie fidèle**
  du desk, `desk_data.json` **restauré à l'octet**. Compte runtime **21 → 22**.
- Cycle : aucun fichier de production touché · SW `td-shell-v187` · **MD5 8/8** ·
  suite **2864 passed / 0 skipped**.

- **Lot 492 — livré** : **les deux barèmes réellement peints, tracés jusqu'au
  producteur — « accord /100 » est SAIN, « confiance /100 » plafonne à 95, et les
  DEUX bornes du garde-fou du comité sont MORTES.**
- **Vérification d'abord** (leçon 491, appliquée **au début**) : la chaîne
  `analysis_page:735` → `/api/decision/<sym>` → `decision_stack` est établie
  **avant** de mesurer. Module **sans aucune écriture**, vérifié.
- **Le brief était incomplet deux fois** : il omettait `- dq.confidence_penalty`
  et le garde-fou propre du comité `max(20, min(95, …))` ; **c'est justement le
  garde-fou omis qui porte la trouvaille**.
- **Trouvaille** : `agreement ∈ [0,1]` par construction, donc
  `45 + agreement×45 − 15×contradiction` parcourt **[30, 90]**. Énumération
  **complète** : **`max(20,…)` et `min(95,…)` ne mordent JAMAIS.** Le code
  exprime une échelle 20-95 **qui n'existe pas**.
- **Le chiffre affiché ne peut jamais atteindre 100** : maximum absolu **95**.
  Banc réel : `d.confidence` absent → **72** · `=90` → **90** · `=100` → **95**.
  **« accord 100/100 » atteint : témoin POSITIF du lot.**
- **Hypothèse à moi réfutée** : je croyais `base_conf` toujours à la constante
  55 — **faux**, `quant/scoring.py:139` le produit vraiment ([40,100] par
  formule, **[40,73] sur ma grille** — propriété de la grille, dite comme telle).
- **Je refuse de gonfler : aucun rang posé.** Cinq points inatteignables sur cent
  sur une grandeur heuristique n'est pas du même ordre que le 484-B (27,5 % hors
  d'atteinte sur la carte de décision) → **observation**. Les bornes mortes sont
  **internes**, donc **nommées, non classées** (règle 486/491).
- **Second contrôle** (cas exclu : la pénalité de qualité) : scan rassis →
  **38/100 contre 72**. **Une pénalité de 15 fait chuter de 34 points**, car
  `stale` modifie aussi les preuves — **l'effet n'est pas additif et rien ne le
  dit**. Et **la borne basse `max(0,…)`, elle, EST atteignable** : un garde-fou
  mort en haut, un vivant en bas, dans la même expression.
- **Deux faux arrêtés** : (1) mon premier banc mesurait la branche
  `DATA_INSUFFICIENT` et rendait 0 trois fois — **diagnostiqué, pas conclu** ;
  (2) mon scan AST disait que `compose()` ne renvoie pas `confidence`, **l'exécution
  a répondu l'inverse**. **57 → 59.**
- **Deuxième lot consécutif sans nouveau dossier — ce n'est pas une panne, c'est
  une veine correctement mesurée qui se vide.**
- Feuille **inchangée** : 24 dossiers · quatorze rang 1 · huit rang 2 · trois rang 3.
- Cycle : aucun fichier de production touché · SW `td-shell-v187` · **MD5 8/8** ·
  runtime 21 fichiers, écart **AUCUN** · suite **2864 passed / 0 skipped**.

- **Lot 491 — livré** : **les 7 barèmes non tracés — la liste du 486 confondait
  TROIS échelles homonymes, et la confiance plafonnée à 50/100 que j'ai mesurée
  n'est affichée NULLE PART.**
- **Calibration** : `score40` du paquet parfait = 29 (485), facteur `calibration`
  = 0,50 (docstring) — les deux OK.
- **Le banc** : `confidence()` = `1.0 × 1.0 × 0.875 × 0.5` = **0,438 → 44/100**.
  Le plafond **n'est pas structurel** : 100/100 est atteint **si** une
  calibration réelle est fournie.
- **Est-elle fournie ? Non** : le fichier runtime porte **29 décisions et 0
  résultat mesuré** ; `calibration_factor_for` rend **0,50** partout, base
  « échantillon insuffisant (**0/20** mesures) ». Et le balayage
  `/opportunities` **ne passe aucune calibration**.
- **Le retournement** : ce chiffre **n'atteint aucune surface servie**. Sur les
  **15 occurrences** de `confidence` dans `vertex/ui/` + `static/`, **aucune** ne
  lit celle de `skyler_core` ; le balayage n'expose même pas le champ.
  **Famille du 486 : exact, produit, jamais peint. Je le nomme, je ne le classe
  pas** — un chiffre non affiché ne trompe personne.
- **Le vrai résultat** : `agreement` existe en **facteur [0,1] non servi**
  (`skyler_core:100`) **et** en `×100` affiché (`decision_stack:251`) ;
  `confidence` de même. **Dix-neuvième récurrence de l'homonyme, et la plus
  coûteuse — j'ai benché un objet qui n'est pas celui qu'on voit.** Le 484 avait
  signalé le même piège ; **la leçon existait, je ne l'ai pas appliquée avant de
  choisir ma cible.**
- **Second contrôle** : distinguer un `/100` barème d'un `/100` pourcentage.
  Trouvé — `briefing.py:402` « Confiance données … % » est un **pourcentage de
  fraîcheur**, pas un barème. **La liste des « 7 » n'était pas une population
  propre.**
- **Deux faux arrêtés** : (1) sonde **mal étiquetée** — elle annonçait « plafonné
  à 0,50 » et ne testait que `plafonn` ; vérifié, **« 0,50 » est ABSENT des
  octets servis** ; (2) j'allais attribuer le plafond au chiffre affiché, qui
  vient du **decision_stack**. **55 → 57.**
- **Portée** : **aucun rang posé** — le lot **nettoie une population et empêche
  une fausse publication**. `decision_stack.confidence` et `.agreement`, **les
  deux barèmes réellement peints, restent non tracés** : dette nommée. Le
  « 0/20 » est un **état**, pas une propriété permanente. **Aucun navigateur.**
- Feuille **inchangée** : 24 dossiers · quatorze rang 1 · huit rang 2 · trois
  rang 3.
- Cycle : aucun fichier de production touché · SW `td-shell-v187` · **MD5 8/8** ·
  runtime 21 fichiers, écart **AUCUN** · suite **2864 passed / 0 skipped**.

- **Lot 490 — livré** : **BILAN n°17 de la tranche 480-489** (voir le bloc de
  bilan en tête). **Le taux d'auto-correction n'a pas monté — il a plafonné à 3**
  (460-469 : 1 · 470-479 : 3 · 480-489 : 3), et **les trois auto-corrections sont
  des lots de RÉ-EXAMINATION**, ce qui confirme la thèse du 480 avec dix lots de
  plus. **La moitié de la tranche a mesuré la boucle, pas le produit** : dix lots
  pour **trois défauts neufs**. **0 correction engagée, 0 gardien, 0 octet servi
  modifié**, feuille **20 → 24**. **Deux chiffres du réveil corrigés** : la
  feuille a grossi de **+4** et non +2 ; la tranche couvre **#512 → #521** et non
  #513 → #521. **Troisième réveil consécutif fautif (480, 482, 490) — le brief
  est une source comme une autre.** **Défaut de mon instrument** : je cherchais
  « N dossiers » dans les rapports alors que le chiffre vit dans les **lignes
  d'index**. **Arrêtés avant publication 54 → 55.** Cycle : aucun fichier de
  production touché · SW `td-shell-v187` · **MD5 8/8** · runtime 21 fichiers,
  écart **AUCUN** · suite **2864 passed / 0 skipped**.

- **Lot 489 — livré** : **la dette du 488 soldée en MOBILE — les trois
  atténuations survivent à 390 × 844, mais la mesure trouve autre chose : un
  genre neuf, l'ATTÉNUATION CONDITIONNELLE, qui tombe sous ~730 px de hauteur
  d'écran.**
- **Banc calibré par construction** : les deux viewports dans le même script, la
  calibration étant le 1440 lui-même — « même carte = OUI » retrouvé trois fois.
  À 390 × 844 les trois survivent (`display:block`, `visibility:visible`, taille
  non nulle, aucun rognage).
- **Mon instrument était incomplet, attrapé en lisant sa sortie** : le premier
  banc mesurait la position de **l'atténuation seule** et allait me faire publier
  « en mobile l'atténuation du 455 sort de l'écran » — **vrai et sans intérêt**,
  car au 1440 elle en sort aussi, et le défaut est tout aussi bas. **La quantité
  qui décide est la DISTANCE entre le défaut et son atténuation. 53 → 54.**
- **Mesure refaite — distance défaut ↔ atténuation** : 1440 → 510 / 81 / 620 px
  (écran 1400) : 3 co-visibles · 390×844 → 406 / 119 / **681** : 3 co-visibles ·
  **375×667 → 455 : NON** · **360×640 → 455 : NON**. **La distance du 455 se fige
  à 681 px** sur les trois largeurs : seule la **hauteur** décide (règle 459, la
  réponse a cessé de bouger).
- **456 et 484-B tiennent partout** (484-B le plus robuste : 81 à 137 px).
  **Le 455 tient sur un grand téléphone et tombe sur un petit** — il faut alors
  **défiler entre le défaut et ce qui le corrige**.
- **Ce que j'en fais** : **je ne promeus PAS le 455 au rang 1** — au 487 le
  486-A a été promu parce que son atténuation était sur une **autre vue**, jamais
  simultanée sur **aucun** appareil ; ici elle l'est sur l'appareil le plus
  probable, et promouvoir sans savoir serait une **aggravation non fondée**.
  **Mais je ne le confirme pas sans réserve** : son rang 2 devient
  **CONDITIONNEL**, condition écrite — *hauteur de viewport ≥ ~730 px*.
  **Je ne sais pas de quel côté de la borne se trouve l'utilisateur** et je ne
  l'invente pas.
- **Genre neuf** : *une atténuation peut être **conditionnelle** — vraie sur un
  appareil, fausse sur un autre ; un rang qui en dépend doit **porter sa
  condition**.* Troisième affinement consécutif : le 487 a exigé la même **vue**,
  le 488 la même **carte**, le 489 ajoute la **distance** et l'**écran**.
- **Second contrôle** : `innerText` ignore `display:none` mais **pas** un texte
  rogné par `overflow:hidden`. Mesuré sur les six cas — **rien trouvé**. **Ce
  n'est pas la même chose que de l'avoir validé sur un cas positif**, et je le
  dis plutôt que de compter le contrôle comme concluant.
- **Portée** : trois atténuations, quatre viewports — **pas la matrice complète** ;
  la distance du 455 vaut pour **AAPL et 2 000 $** ; le seuil ~730 px est
  **déduit**, non dichotomisé ; **aucune capture d'écran** — verdicts issus de
  `getBoundingClientRect`, un texte visible mais illisible échapperait.
- **Fait de méthode** : **mon premier banc posait la mauvaise question.** *Une
  mesure exacte peut répondre à côté — seule la lecture de sa sortie le révèle.*
- Feuille : **rangs inchangés (24 · 14 · 8 · 3)**, avec **une condition neuve
  inscrite au rang 2 du 455**.
- Cycle : aucun fichier de production touché · SW `td-shell-v187` · **MD5 8/8** ·
  serveur DEMO **arrêté et vérifié** · runtime 21 fichiers, écart **AUCUN** ·
  suite **2864 passed / 0 skipped**.

- **Lot 488 — livré** : **la règle du 487 appliquée à TOUTES les atténuations
  qui ont fait descendre un rang — les trois autres TIENNENT, vérifiées à
  l'écran, aucun rang ne bouge ; et la boucle avait déjà la méthode aux lots 442
  et 471 avant de la perdre au 486.**
- **Recensement** : 490 rapports balayés sur le vocabulaire d'atténuation ;
  calibration dans le code (le 486, réfuté au 487, **doit** sortir — trouvé).
  **Population brute 30**, et **la lecture corrige l'instrument** : **douze ne
  portent « note honnête » qu'au sens d'un état vide**. **Quatre atténuations
  ont réellement fait descendre un rang** : 455, 456 (i), 484-B, 486-A (réfutée).
- **Une lecture qui tranche avant le navigateur** : la note du 456 passe au Chart
  Shell comme `limits`. Le 442 avait établi que le **tiroir** ne rend que
  `shows/why/confirm/invalidate`. Mesuré : `chart-core.js` **L161 rend `limits`
  dans `vx-chart-foot`, le pied VISIBLE de la carte** (L174 n'en est qu'une
  répétition dans le tiroir). **Le pied, pas le tiroir.**
- **Au navigateur, les trois tiennent** (test : une même carte rendue contient-elle
  le défaut ET l'atténuation ?). **456** `/system?view=data` : la note « qualité
  au niveau scan (source unique)… » est dans le pied de la carte, **sans clic** →
  même carte. **455** : les six contrôles, avec icônes de statut et détail de ce
  qui manque, sont dans la **même carte** que la narration. **484-B** : « REFUSER
  8/40 … Fondamentaux 0/5 Catalyseurs 2/5 … » → même carte.
- **Deux mesures antérieures confirmées à l'écran, sans être recomptées** :
  « Catalyseurs 2/5 » et « Flux/anomalies 0/4 » (blocs bridés du 485) ;
  « Dominante : DEMO (20 / 20) » (camembert à une seule part du 456 (ii)).
- **Un faux arrêté en chemin** : mon premier passage a rendu « CARTE ABSENTE »
  sur `/system` nu — **j'allais conclure l'atténuation invérifiable** ; la carte
  vit sur **`/system?view=data`**, une vue **serveur** distincte. **Diagnostiqué,
  pas conclu. 52 → 53.**
- **Second contrôle — un cas exclu par le recensement** : le **442**, dont le
  rang 2 est justifié autrement. Il écrit « atténué par une légende honnête **non
  co-visible** » et repose sur une **accessibilité non établie**. **Exclusion
  justifiée, pour la bonne raison.**
- **Fait de méthode** : le **442** distinguait déjà co-visible et non co-visible ;
  le **471** mesurait la co-visibilité **vue par vue** (« sur `risque`, et là
  seulement ») — **exactement la règle du 487** ; le **486** l'a affirmée sans
  vérifier la vue. **Une règle peut être appliquée avant d'être nommée, et
  oubliée après l'avoir été.** Le 487 croyait poser du neuf ; **il redécouvrait**.
- **Résultat de bornage, publié tel quel** : le 487 avait trouvé une atténuation
  fausse ; combien d'autres ? **Aucune.** La feuille est **inchangée**.
- **Portée** : les défauts eux-mêmes **non rejoués**, seules leurs atténuations ;
  **le plafond de 200 du 456 ne mordait pas** (scan DEMO à 20 titres) — **le cas
  fautif n'a pas été observé à l'écran** ; **un seul viewport**, pas de mobile ;
  douze rapports écartés par lecture, comptés dans aucun total ;
  `/analysis/AAPL` **écrit** — su, assumé, **restauré à l'octet**.
- Cycle : aucun fichier de production touché · SW `td-shell-v187` · **MD5 8/8** ·
  serveur DEMO **arrêté et vérifié** · runtime 21 fichiers, écart **AUCUN** ·
  suite **2864 passed / 0 skipped**.

- **Lot 487 — livré** : **la dette du 486 soldée AU NAVIGATEUR — le défaut est
  confirmé à l'écran, le mécanisme s'allume dès qu'on remplit le champ, et
  l'atténuation qui maintenait le rang 2 est RÉFUTÉE : l'alerte et la barre ne
  sont jamais sur la même vue. 486-A passe au RANG 1.**
- **Banc** : Chromium préinstallé lancé par `executable_path` (1194 sur disque,
  Playwright réclamait 1228 — **`playwright install` non lancé**) ; **synchro
  desk coupée en lecture ET en écriture** au niveau réseau ; positions semées en
  `localStorage` avant hydratation (poids 40/30/30 %).
- **Deux calibrations, la première a ÉCHOUÉ** : en ne bloquant que le POST,
  l'alerte affichait « ACN = 65 % » — **un symbole non semé** : la page
  s'hydratait depuis le desk serveur. **Aucun résultat de ce passage n'a été lu.**
  Corrigé en coupant le GET → « AAA = 40 % », le poids exact. Seconde
  calibration (les 3 symboles semés dans le tableau) : passée.
- **Découverte de structure** : le tableau des poids **n'est pas sur la vue par
  défaut**. `/portfolio` ouvre sur **Synthèse** (0 cellule Poids) ; le tableau
  vit sur **Positions**. Sans ce clic, le banc mesurait une page sans l'objet.
- **CONFIRMÉ par exécution** : `AAA 40,0 %` → **barre verte**, tick absent,
  suffixe absent, `vx-warn` false, Conviction « — ». Une position à 40 % du
  portefeuille affiche une barre verte. Le repli « — » de `convOf` est **honnête**.
- **Second contrôle — un cas que le produit n'exerce jamais** : avec
  `entrySnap.score = 30` injecté, la même ligne donne `40,0 % / 5 %`, barre
  **rouge**, tick **présent**, suffixe **présent**, `vx-warn` **true**,
  « A · 30 ». **Le mécanisme fonctionne : le code n'est pas cassé, il attend une
  donnée que personne n'écrit.** Le contrôle confirme la **cause**, pas seulement
  le symptôme.
- **RÉFUTÉ — mon propre classement** : Synthèse → alerte présente, **0 cellule
  Poids** ; Positions → 3 barres vertes, **« Concentration élevée » absente**.
  **Jamais à l'écran en même temps.** Ma « co-visibilité » venait des **octets
  servis**, pas du **rendu** — la leçon que le 486 avait lui-même publiée, que
  j'avais appliquée au défaut **et pas à mon atténuation**.
- **Contrepoids donné** : l'alerte est sur la vue **par défaut**, donc vue en
  premier. Cela ne restaure pas le rang 2 : la vue Positions est celle dont le
  métier est le risque **ligne par ligne**, et rien n'y signale le plafond.
  **486-A : rang 2 → RANG 1.** **Publiés puis corrigés 9 → 10.**
- **Fait de méthode** : **le test d'accessibilité doit être appliqué à
  l'ATTÉNUATION autant qu'au DÉFAUT.** J'ai cru mon atténuation sur parole parce
  qu'elle m'arrangeait — elle faisait descendre un rang.
- **Portée** : exclusivité des onglets établie sur **deux passages**, pas une
  seule session (deux bascules en session ont échoué ; **la mesure inutilisable a
  été écartée, non lue**). Poids **semés**, un seul viewport, pas de mobile.
  **`/api/client-log` = 0 erreur** ; l'unique erreur console est **mon propre
  blocage de `/api/desk`**, non comptée. Le **latent** du 486 reste latent — le
  banc l'a contourné en injectant un score déjà sur /40.
- **Le contrôle d'apparition a attrapé ma propre pollution** : `l487_res.json`
  écrit à la racine du dépôt par un script du banc. Supprimé, restauration
  revérifiée : **21 fichiers, écart AUCUN**. `breadth_history` et `daily_prev`
  touchés par le serveur DEMO (reproduction du 391), **restaurés à l'octet**.
- Feuille : **24 dossiers · quatorze rang 1 · huit rang 2 · trois rang 3**.
- Cycle : aucun fichier de production touché · SW `td-shell-v187` · **MD5 8/8** ·
  serveur DEMO **arrêté et vérifié** · suite **2864 passed / 0 skipped**.

- **Lot 486 — livré** : **le test du 485 appliqué à TOUS les barèmes — le score
  /40 est affiché sur DEUX pages et non une, et la trouvaille vient du cas que
  mon recensement EXCLUAIT : la barre de poids de `/portfolio` est TOUJOURS
  VERTE, quel que soit le poids.**
- **Instrument** : population construite **depuis l'écran** — 42 objets servis,
  841 916 caractères, six motifs. **Calibration sur les deux réponses connues**
  (LEAPS sain, score /40 bridé à 29), sortie si l'une manque : les deux trouvées.
  **66 relevés sur 15 objets.**
- **Un second SITE, pas un second défaut** : `/opportunities` sert « Classement
  Skyler — score canonique /40 », tracé jusqu'à `skyler_sweep.py:50`
  `_sk.decide(...)` — **le moteur plafonné à 29**. Conséquences neuves : la barre
  **ne peut jamais dépasser 72,5 %** de son rail, le seuil vert `>=28` est une
  **fenêtre de deux points**, la colonne `Niveau` ne peut afficher ni S ni S+.
  **Le dossier 484/485 passe de 1 à 2 pages servies** — chiffrage changé, rang
  inchangé.
- **Le second contrôle est celui qui trouve.** Mon recensement exige un maximum
  **déclaré** : il exclut les **jauges muettes**. Contrôle sur `wgtBar`, appelée
  une seule fois avec `tr = tierOf(t)`, et `tierOf` lit **`entrySnap.score`**.
  Mesuré dans les octets servis : **18 occurrences — 15 lectures, 3 écritures**,
  toutes dans `vx-entities.js`, **aucune n'écrivant `score`** ; le seul site qui
  le pourrait est `vx_kit.py:185`, **mort** (lot 381).
- **Donc `tierOf` rend `null` pour toute position** : tick de plafond jamais
  dessiné, suffixe « / cap % » jamais écrit, `over`/`near` toujours faux →
  **barre toujours verte**, et `vx-warn` jamais déclenchée. **Les trois chemins
  sont bien servis — vérifié — ils ne sont jamais pris. Exact, servi,
  inatteignable.**
- **Ce qui atténue** : `dominantRisk` (`:221`) alerte bien sur Top1 > 25 %, et
  c'est **servi**. Le risque est signalé au niveau du portefeuille ; c'est la
  barre **par ligne** qui ne le signale pas. → **486-A rang 2**, et c'est ce
  seul point qui l'empêche d'être rang 1.
- **Défaut LATENT nommé sans être classé** : `n = sc<=40 ? sc : round(sc/2.5)` —
  un score /100 ≤ 40 est lu comme un /40, donc `40/100` (faible) donne **S+ /
  15 %** quand `78/100` (bon) donne **S / 10 %** ; et `roleOf:111` lit **le même
  champ à l'autre échelle** (`>= 78`). **Rien n'écrivant `score`, c'est latent :
  aucun rang, pas compté dans la feuille.**
- **Mutualisation réelle, la première depuis le 478** : 486-A et le latent ont
  **une seule cause**, `entrySnap.score` jamais écrit — **un seul correctif**.
  Famille du 406/407, **pas le même site** : je ne fusionne pas.
- **Deux faux arrêtés avant publication** : (1) le recensement allait conclure
  « rien de neuf » — sa restriction excluait précisément la jauge fautive ;
  (2) ma sonde a rendu « ABSENT » sur une chaîne mal recopiée — revérifiée,
  **PRÉSENT** : j'allais affaiblir mon propre constat. **49 → 51.**
- **Portée** : **aucune exécution de moteur** — c'est du JS client ;
  l'inatteignabilité vient du recensement des écritures servies, pas d'un rendu.
  **Dette nommée : un navigateur la solderait.** Six motifs littéraux ;
  **7 barèmes nommés non tracés** ; « `vx_kit.py` mort » repris du 381.
- **Fait de méthode** : trois lots de suite, **le résultat est venu du BORD de
  l'instrument, pas de son centre**. *Le défaut se loge là où la définition de la
  population s'arrête.*
- Feuille : **+1 dossier → 24 · treize rang 1 · neuf rang 2 · trois rang 3**.
- Cycle : aucun fichier de production touché · SW `td-shell-v187` · **MD5 8/8** ·
  runtime 21 fichiers restaurés, écart **aucun** · suite **2864 passed / 0 skipped**.

- **Lot 485 — livré** : **la dette du 484 soldée PAR EXÉCUTION — le rang 1 est
  confirmé (0 niveau S ou S+ sur 3 072 combinaisons) et mon propre chiffre publié
  la veille est FAUX : le plafond n'est pas 35/40, il est 29/40.**
- **Sûreté d'abord** : `skyler_core` ne contient **aucune écriture** (vérifié) ;
  les écrivains cités au 484 sont appelés par `analysis_api.py`, pas par le
  moteur. `persist` redirigé **et vérifié** malgré tout.
- **Calibration écrite dans le banc** : paquet vide → 0 / `REFUS_WATCH` ; score
  technique 100→0 → **−6 exactement**, le poids du bloc. Sortie si échec.
- **Paquet parfait** : `0/5 · 2/5 · 6/6 · 1/4 · 4/4 · 6/6 · 6/6 · 4/4` →
  **TOTAL 29/40, level A**. **648 combinaisons : la borne ne bouge pas.**
- **CONFIRMÉ** : sur **3 072 combinaisons**, `REFUS_WATCH 2952 · B 112 · A 8 ·
  S 0 · S_PLUS 0`. **Jamais un niveau S ou S+.** Le rang 1 passe de « par
  lecture » à **« par exécution »**. Et **pire que prévu** : A n'apparaît que
  **8 fois sur 3 072 (0,26 %)** — **A tient sur deux points de marge**.
- **RÉFUTÉ** : **11 points inatteignables, pas 5** ; **trois blocs bridés, pas
  un** — `fundamentals_quality` 0/5, `catalysts` 2/5, `institutions_flow…` 1/4.
  Les deux manqués **ne sont pas figés à zéro**, et c'est pourquoi l'AST du 484
  les a laissés passer : il testait « ce bloc marque-t-il **quelque chose** ? »,
  pas « atteint-il **son propre maximum** ? ».
- **Fait de méthode — j'avais posé la bonne question la veille, à un autre
  objet** : dans le MÊME lot 484, sur le barème LEAPS, j'ai vérifié que chaque
  dimension atteint son maximum — puis j'ai découvert le barème du score /40 et
  **je ne lui ai pas appliqué le test que je venais d'appliquer**. **Un test
  appliqué à un objet de l'enquête doit l'être à tous les objets de même genre,
  y compris à celui qu'on vient de trouver.** **Publiés puis corrigés 8 → 9.**
- **Second contrôle, trois cas exclus par le banc** : (a) V1 **n'a aucun
  `skyler_score.blocks`** — sous V1 le score entier serait 0/40 ; V2 est le
  profil actif, **conclusion bornée à V2 et je le dis** ; (b) `decide()` vérifié
  ligne à ligne — il ne fait que **lire** `total` et `level`, aucune réécriture ;
  (c) **les deux blocs bridés déclarent leur propre plafond** dans leur `basis`
  (« plafonné 2/5 », « plafonné 1/4 »), rendu en `title` — **au survol, pas
  affiché** ; la puce visible montre « Catalyseurs 2/5 », **qui invite à croire
  que 3 points restent à gagner**.
- **Rangs** : **484-A rang 1 CONFIRMÉ** par exécution ; **484-B reste rang 2**
  avec ses chiffres corrigés — le défaut est plus grave, mais l'atténuation est
  plus forte aussi, et **une aggravation est aussi fragile qu'une atténuation**.
- **Observation non classée** : `red_team.required` est **toujours `False`**
  (`level` est déjà rabattu à l'intérieur de `score40`) — drapeau mort, et
  `red_team` n'atteint aucune surface servie.
- **Portée** : paquet **fabriqué à la main**, `build_packet()` non exercé — le
  banc établit ce que `score40` **peut** rendre, pas la distribution en usage ;
  neuf axes discrétisés ; **aucun navigateur**.
- Cycle : aucun fichier de production touché · SW `td-shell-v187` · **MD5 8/8** ·
  runtime 21 fichiers restaurés, écart **aucun** · suite **2864 passed / 0 skipped**.

- **Lot 484 — livré** : **retour au produit, et il paie au premier lot — la carte
  de décision de `/analysis` affiche un score « /40 » dont 5 points sont
  STRUCTURELLEMENT inatteignables, et les deux plus hauts niveaux de conviction
  de la Constitution, S et S+, ne peuvent être atteints par AUCUN titre.**
  **Direction choisie** : tracer les 7 gabarits de fraction que le 456 avait
  nommés mais laissés « ni comptés, ni conclus » — **et y inclure les trois qu'il
  avait pré-classés « barèmes » PAR LECTURE**, puisque la leçon 481 dit qu'une
  restriction qui écarte des faux positifs fabrique des faux négatifs. **C'est
  exactement là que la trouvaille était.**
- **Deux contrôles** : le premier calibré dans le code du détecteur (un site sain
  connu, un site plafonné connu) — passé ; le second sur **l'angle mort que le 456
  avait lui-même nommé** (fractions construites par un helper) — exclusion
  **justifiée cette fois**, et bornée à quatre formes cherchées.
- **Deux témoins positifs** : G4 `p.v/p.max` (maxima 30+25+20+15+10 = 100, chacun
  atteint par la branche haute de son ternaire) et G6 `favorable / pts.length`
  (numérateur filtré du dénominateur lui-même).
- **La trouvaille, établie par AST après un premier détecteur FAUX** : mon `grep`
  rendait huit blocs figés à zéro — sept avaient un zéro dans une *branche*.
  Refait par AST : **un seul bloc, `fundamentals_quality`, un site d'appel,
  littéral `0`, hors condition, statut `INSUFFICIENT` en dur**. Les 8 poids somment
  à 40, le dénominateur est écrit en dur → **plafond réel 35/40**. Et
  `skyler_core.py:333-334` rabat S/S+ vers A **dès qu'un bloc est insuffisant** :
  **S et S+ sont donc inatteignables pour tous les symboles**, avec leurs bandes
  d'allocation 7-10 % et 10-15 %.
- **Vérifié dans les octets servis** (`/analysis/AAPL`, 75 216 o) : « Score /40 »
  présent, `/40` présent, puce `b.points/b.max` présente, **`insufficient_blocks`
  ABSENT**, **mention d'un plafond de NIVEAU ABSENTE**. **Faux positif arrêté sur
  place** : le mot `plafonn` est bien là, mais c'est `capped_by_gate` — le plafond
  de hard gate, pas celui des blocs. **Arrêté avant publication 48 → 49.**
- **Ce qui atténue** : la puce « Fondamentaux 0/5 » EST affichée, grisée, avec son
  motif en `title`. Co-visible sur le bloc, muette sur le reste.
- **Classement, critères absolus** : **(A) S et S+ inatteignables en silence →
  rang 1** (servi, conséquence sur une décision, **aucune information co-visible**) ;
  **(B) « /40 » dont le plafond est 35 → rang 2** (la puce 0/5 est co-visible —
  exactement ce qui a maintenu le 456 (i) au rang 2).
- **Les trois autres, non gonflés** : G1 — la fraction est défendable mais
  **`avg = acc/total` divise des surprises CONNUES par TOUS les trimestres** →
  moyenne diluée ; **accessibilité non établie → rang 3**. G2 — `deque(maxlen=200)` :
  dénominateur = fenêtre glissante, pas un cumul → observation. G5 — **le dépôt
  n'encode nulle part le sens de `recommendationMean`** ; je **ne** conclus **pas**
  que l'échelle est inversée, faute de source → observation. G7 — « 1 max » ne
  concerne que les puts alors que la chaîne couvre calls et puts → observation.
- **Mutualisation cherchée, partiellement trouvée** : deux plafonds de même genre,
  **trois fichiers, aucun correctif commun** — la famille est réelle, la
  mutualisation ne l'est pas.
- **Portée** : **aucun banc sur `skyler_core`** — établi par lecture de deux lignes
  et par AST ; `decide()` non exécuté, et ce banc monterait la preuve d'un cran.
  Profil V2 seul. **Aucun navigateur** : présence établie sur les octets servis.
- **Fait de méthode, prolongement de la 481** : *un lot qui écarte une catégorie
  « par nature » sans la tracer ne l'a pas mesurée — il l'a supposée.* Le 456 a eu
  raison sur deux barèmes sur trois, et **tort sur celui qui portait le défaut le
  plus grave**.
- Feuille : **+2 dossiers → 23 · treize rang 1 · huit rang 2 · trois rang 3**.
- Cycle : aucun fichier de production touché · SW `td-shell-v187` · **MD5 8/8** ·
  runtime 21 fichiers restaurés, écart **aucun** · suite **2864 passed / 0 skipped**.

- **Lot 483 — livré** : **les six dernières entrées « à classer » lues une par
  une — UNE SEULE l'était encore, deux étaient déjà classées et mal rangées,
  quatre ne portent aucun défaut propre, et AUCUNE des six n'est une
  correction.** Suite directe du 482, avec **deux épreuves** : ce que le rapport
  DIT être, **et** si son site de code existe encore aujourd'hui (leçon 473).
  **Les deux contrôles du 481** : le premier calibré **dans le code du
  détecteur** — passé ; **le second sur un cas que l'instrument EXCLUT** — mon
  instrument lit la liste **par ses étiquettes**, et « 388 (MSFT) » masque le
  second volet du 388 (SKYX/TSTQ dans `skyler_sessions.json`) ; mesuré,
  **3 sources touchent le journal de sessions et les 3 redirigent — 0 sans
  redirection, volet SOLDÉ**. Je l'écris « sans conséquence *cette fois* », pas
  « justifiée » : l'exclusion l'a été par chance, pas par construction.
  **Les six** : **363** « points réels du scan » → **non-dossier**, le rapport
  titre lui-même « Une observation, pas un défaut » (le mot qualifie une
  *méthode*, pas une provenance) ; **386** marqueur `src='ibkr'` →
  **non-dossier, décision produit** — `indices_live` et `['src']` à **0
  occurrence** dans `vertex/ui/` + `static/js`, et les trois rendus « TEMPS RÉEL
  IBKR » tombent **tous** dans des constantes `PAGE_*` **mortes** ; son second
  volet `bret=0.0` est une caractérisation déjà gelée ; **388** les 7 points
  MSFT fabriqués sont **encore là** mais la cause de code est corrigée depuis le
  388 — reste une **purge de données utilisateur** ; **396** → **recoupement**
  du 391 (« Aucun code. Aucun gardien. Aucun test ajouté. ») ; **391** →
  dossier réel portant **déjà un rang 1** (classement du 390), site vérifié
  `terminal.py:503-512`, **aucune garde DEMO** ; **456+459** → dossier portant
  **déjà un rang 2 établi par exécution** au 459 — **il n'était pas à classer,
  il était à CHIFFRER**. **379** (`context()` sur univers vide) est **le seul
  encore à classer**, et le seul comportement **réexécuté** : verdict
  « MARCHÉ · NEUTRE · participation 0 % » sur zéro donnée, **identique
  64 lots plus tard** ; et ce lot ajoute ce que le 379 n'avait pas établi —
  **la chaîne jusqu'à l'écran** : `terminal.py:558` (scan vivant) → `:612`
  `scan_state['market_ctx']` → **trois pages servies** le lisent (`briefing`,
  `markets`, `intelligence`). **Rang 3**, sur trois critères **absolus** et
  aucune comparaison : sortie servie (établi), affirmation au lieu d'abstention
  contre l'invariant n°4 (établi), **cas déclencheur non établi** — ce
  troisième point, et lui seul, l'empêche de monter. **Dossiers en attente de
  classement : 6 → 0, la liste est close.** **Résultat le plus net : tout ce qui
  survit est une DÉCISION** — conception (391), moteur (379), produit (386),
  données (388), style (363) : la liste « à classer » n'attendait pas un
  classement, elle attendait **sept arbitrages humains et un chiffrage**.
  **Mutualisation cherchée et absente, et c'est une trouvaille** : le 379 se dit
  « jumeau du 363 », le 386 « jumelle du `context()` du 379 » — mesuré, la
  parenté est de **famille**, pas de **site** (trois fichiers, trois mécanismes,
  **aucun correctif commun**) ; fusionner sur le mot « jumeau », comme le 478
  l'a fait **à raison** pour 406+407 qui partageaient une *cause*, serait ici
  une erreur. **Fait de méthode : « jumeau » dans un rapport affirme une
  FAMILLE, pas un SITE** — dix-septième récurrence de l'homonyme, sous une forme
  neuve : un même mot désignant tantôt une ressemblance, tantôt une identité.
  **Défaut de mon propre instrument attrapé en lisant sa sortie** : le
  localisateur de constantes `PAGE_*` indexait les intervalles **par nom**, et
  les **huit** affectations `PAGE_DAILY` s'écrasaient — la ligne 3807 ressortait
  « hors constante » ; corrigé en liste de triplets (18 → **18 intervalles
  distincts**) et recalibré sur une réponse connue. **Écraser n'est pas
  accumuler, troisième récurrence après 464 et 465. Arrêté avant publication
  47 → 48.** **Portée** : mesures internes des six **non rejouées** (deux
  épreuves, pas trois) ; seul `context()` réexécuté ; **les numéros de ligne des
  386 et 456 sont périmés** (L621 → 2249, L165-168 → 167) — sites retrouvés par
  **motif**, confirmation directe de la leçon 473 ; « `PAGE_*` mortes » **repris
  du 374** ; **aucun navigateur**. **Feuille : le 379 entre au rang 3 → 21
  dossiers · douze rang 1 · sept rang 2 · deux rang 3 ; lignes et gardiens
  inchangés (55-63 · 20), le 379 étant une décision non chiffrée ; dix lots A à
  J inchangés.** Cycle : aucun fichier de production touché · SW
  `td-shell-v187` · **MD5 8/8** · `persist` redirigé **et vérifié** · runtime
  21 fichiers restaurés, écart **aucun** · suite **2864 passed / 0 skipped**
  lancée **après** les trois documents.

- **Lot 482 — livré** : **retour au produit — QUATRE des dix « dossiers en
  attente » ne sont pas des dossiers ; la liste tombe de dix à six.** Le 481 avait
  fixé la consigne, ce lot mesure l'inventaire réel des défauts de Vertex.
  **Les deux contrôles de la règle neuve du 481** : le premier sur un cas connu du
  478 **passé** ; **le second sur un cas que la restriction du réveil exclurait —
  et il montre que le réveil est FAUX** : `drawdownCard` est à
  `portfolio_page.py:614`, **pas** dans `performance_page.py`. **La règle a payé
  dès son premier emploi.** **Mesuré, et chaque rapport le dit lui-même** : le
  **408** BORNE le 407 (« isolé, pas une famille », 25 POST examinés), le **409**
  BORNE le 406 (« unique sur les 8 pages servies »), le **411** est un RECOUPEMENT
  qui **atténue** de lui-même, et le **426** se déclare mot pour mot
  « recoupement, pas trouvaille » — **cinquante-six lots avant que je ne le lui
  demande**. **Six numéros de rapport, un seul dossier** : le 478 en avait fusionné
  deux, ce lot en rattache quatre de plus, et le tout est **déjà classé rang 2 et
  chiffré à 4 lignes**. **Aucun classement à poser, et c'est le résultat** —
  aucune des quatre ne prétend à un défaut. **Précision de produit appliquant la
  leçon 477** : le littéral « clôtures déclarées (myTradesEquity) » est **servi
  mais jamais peint** (garde `eq.length>=2` en `:604`), donc la formulation des
  411/426 est exacte ; et la garde est **honnête** — sans série, la page rend un
  état vide motivé. **Portée** : les mesures des quatre lots **n'ont pas été
  rejouées**, leurs chiffres sont les leurs ; **je ne les retire pas de
  l'historique**, seulement de la liste des dossiers en attente — un bornage qui
  empêche une campagne inutile reste un résultat. **Fait de méthode : une liste de
  dossiers en attente n'est pas une liste de défauts — elle accumule des numéros
  de lot, et un lot peut n'avoir rien trouvé.** Les compter comme des dossiers,
  c'était confondre le travail et son objet, et cela durait depuis soixante-dix
  lots. Aucun fichier de production touché · SW `td-shell-v187` · **MD5 8/8** ·
  suite **2864 passed / 0 skipped** · **feuille INCHANGÉE**. Comptes :
  **47 (+1)** · 8 · 3 · 0 · 0 · 8.
- **Lot 481 — livré** : **les six rangs orphelins du 480 sont UN SEUL, et il était
  déjà soldé — mon détecteur d'hier gagnait en précision et perdait en rappel, et
  le lot qui l'a posé n'a mesuré que le premier effet.** Lot de soldes, **et il
  travaille contre le lot précédent**. Portée : aucune conclusion ne porte sur
  Vertex. Contrôle sur réponse connue du 480 (le 407 n'a aucune section
  « Classement ») : **passé** — et c'est ce contrôle réussi qui rend la suite
  embarrassante, car **le fait du 480 est exact mais sa conclusion ne l'est pas**.
  **Mesuré : cinq des six déclarent bien leur rang**, mais partout sauf dans une
  section nommée « Classement » — dans un titre de sous-section (455), une puce
  (456), un bilan de veine, une phrase liminaire (406, 407, 463). **Seul orphelin
  réel : le 378**, et il était **déjà soldé au 477** (rang 2, trois critères
  absolus). **Rangs sans justification : 6 → 0.** **Publiés puis corrigés 7 → 8 —
  et cette fois ce n'est pas un compte du réveil, c'est la trouvaille principale
  de mon propre lot d'hier.** **Genre neuf : une restriction qui supprime des faux
  positifs en créant des faux négatifs, et le lot qui la pose ne mesure que le
  bénéfice.** Corollaire sévère : **un contrôle choisi parmi les cas que
  l'instrument voit ne teste jamais ce qu'il ne voit pas** — la règle du 467 est
  insuffisante, il faut y ajouter « et un cas que la restriction exclut ».
  **Corollaire qui corrige une phrase du 480** : le tableau du plan **a repris** ce
  que les rapports disaient, il ne l'a pas inventé. **Et un fait qui renforce le
  479** : le 407 se déclarait bien rang 1 lui-même, donc le 478 l'a fait descendre
  **contre une déclaration explicite**, pas contre une case de tableau. **Les six
  portent un critère absolu ; aucun rang ne bouge.** **Seconde dette résolue** : le
  418 tient sur trois critères propres, la comparaison n'y est qu'un appoint —
  **c'est une phrase qui est périmée, pas un classement** ; **incohérences de
  rang 1 → 0**. **Dette neuve, ouverte plutôt que masquée** : **huit rangs relatifs
  non re-vérifiés**. **Observation de cadence** : trois lots d'introspection
  d'affilée ont chacun corrigé le précédent — ce n'est pas une dérive, mais **cela
  fixe une limite que j'écris : le prochain lot doit revenir au produit.** Aucun
  fichier de production touché · SW `td-shell-v187` · **MD5 8/8** · suite **2864
  passed / 0 skipped** · **feuille INCHANGÉE**. Comptes : 46 · **8 (+1)** · 3 · 0 ·
  0 · **8 (dette neuve)**.
- **Lot 480 — livré** : **l'audit des rangs relatifs — NEUF sur vingt-quatre, UN
  SEUL est affecté, et il n'est pas dans le plan ; mais l'audit trouve autre
  chose : CINQ des vingt dossiers du plan portent un rang que leur propre rapport
  n'a jamais déclaré.** Réponse à la question posée sans réponse au 479. **Portée
  posée d'emblée : aucune conclusion ne porte sur Vertex, toutes portent sur mes
  propres rapports.** Calibration écrite **dans le code** ; contrôle sur cas connu
  (le 416) **passé**. **Population** : 482 rapports, 81 déclarent un rang, **371
  déclarations** — l'instrument comptait les rangs **cités**, pas **posés**. Puis
  deux défauts de plus, vus en lisant : **« Classement coût/risque » est le tableau
  du plan, pas un rang propre** (seizième récurrence des homonymes), et **le regex
  prenait le premier rang, donc « pourquoi pas rang 1 » l'emportait sur le
  verdict**. Corrigé : **24 rangs propres**, dont **9 relatifs (37,5 %)**, formant
  une **chaîne de sept dossiers** suspendus à un seul étalon. **Mouvements de rang
  mesurés indépendamment** : 459 → 456 (**hausse**, rang 4 → 2), 478 → 407
  (baisse), 479 → 416 (baisse). **Le réveil se trompe une quatrième fois** : il
  listait 469, 465 et 462 qui ne sont pas des mouvements, et **omettait la
  requalification 459 → 456**. **Croisement : seul le 418 est affecté** — rang 2
  « moins grave que le 416 », or le 416 est passé à rang 3 : **inversion**. Je le
  **nomme sans le reclasser** : il n'est pas dans le plan. **Bornage : la feuille
  de décision ne change pas — c'est le résultat de l'audit, pas son absence.**
  **Raison mesurée à cette robustesse : le 422 s'était explicitement dissocié de
  son étalon (« famille du 417, pas du 407 »), cinquante-sept lots avant que le
  problème n'existe.** **Trouvaille non cherchée et plus grave que la question** :
  **six rangs orphelins de justification** (378, 406, 407, 455, 456, 463) — leur
  classement vient du tableau des bilans, jamais d'un rapport ; **et le 407 est
  l'étalon du 416**. **Règle posée parce que la mesure la porte : un rang doit
  porter au moins un critère absolu ; la comparaison est un appoint, jamais le
  seul.** **L'autre question du 479 tranchée** : trois révisions, deux baisses une
  hausse, **et les trois dans des lots de ré-examination** — ni calibrage ni
  fatigue, **un changement de tâche** ; mais **trois est trop peu pour exclure un
  biais faible, et je le dis**. **Portée** : le détecteur de mouvements est une
  heuristique — **il a trouvé le 459 que j'ignorais mais raté le 478**, donc les
  trois mouvements ne sont **pas** un total exhaustif. Aucun fichier de production
  touché · SW `td-shell-v187` · **MD5 8/8** · suite **2864 passed / 0 skipped**.
  Comptes : **46 (+1)** · 7 · 3 · **incohérences de rang 1** · **rangs sans
  justification 6**.
- **Lot 479 — livré** : **le 416 DESCEND de rang 1 à rang 3, par transitivité avec
  ma propre mesure du 478 — et « les quinze jamais classés » est un compte FAUX.**
  Contrôle sur réponse connue du 478 : **passé**. **Premier résultat** : mesuré
  rapport par rapport, **trois des quatorze portent déjà un rang** (416 et 422
  rang 1, 431 rang 4) ; « jamais classés » confondait **ne pas être rangé** et
  **ne pas être chiffré**. Le travail restant est **onze classements et quatorze
  devis**, pas quinze classements — le chiffre venait de **mon propre réveil**.
  **Choix du 416** : seul candidat dont le rang peut être **testé par
  transitivité**, puisqu'il se compare explicitement au 407 que je viens de
  re-mesurer. **Deux formes syntaxiques** du même choix (`.fillna(100)` et
  `if avg_l > 0 else 100.0`) — **quinzième récurrence du détecteur à une seule
  forme**, mon premier grep n'en voyait qu'une. **Atteignabilité prouvée par
  exécution et plus précise que le rapport** : `kv('RSI'` est absent de
  `/analysis` et présent dans `/analysis/AAPL`. **Témoin positif treize lignes
  plus haut** : la série de RSI mappe `NaN → None`, le scalaire non ; réserve
  honnête, **je n'ai pas mesuré si cette garde tire jamais**. **Rang 3** : le 416
  se déclarait « nettement moins grave que le 407 », et le 478 a mesuré le 407 en
  rang 2 — **le 416 n'a pas changé, c'est son étalon qui a bougé** ; la mesure
  directe concorde (cas de bord strict, convention de Wilder correcte dans le cas
  dominant). **Pas rang 4** : affiché, servi, indiscernable d'une mesure.
  **Chiffrage : 3 lignes, 2 fichiers, aucune ligne de rendu** — mais **premier
  dossier du plan dont la correction touche un vrai calcul de moteur**, donc à
  traiter seul. Régression **moyenne** : cinq fichiers de test touchent les
  indicateurs, et le 416 signale lui-même un gardien à relire avant. Mutualisation
  **absente**, mesurée. **Feuille : 20 dossiers · 55 à 63 lignes · 20 gardiens ·
  douze rang 1 · sept rang 2 · un rang 3**, avec un nouveau lot J isolé.
  **Fait de méthode neuf : un rang est RELATIF — quand une référence bouge, tout
  ce qui s'est classé par rapport à elle doit bouger aussi.** Question posée et
  **non résolue** : combien d'autres rangs ont été posés par comparaison à un
  dossier dont le rang a bougé depuis ? Je la nomme plutôt que de la taire.
  **Et une observation à ma charge : les deux derniers lots ont réduit un dossier
  après vingt lots où la mesure aggravait — instrument qui se calibre ou juge qui
  se fatigue, je ne sais pas encore, et je préfère l'écrire.** Aucun fichier de
  production touché · SW `td-shell-v187` · **MD5 8/8** · suite **2864 passed /
  0 skipped**. Comptes : **45 (+1)** · **7 (+1)** · 3 · 0.
- **Lot 478 — livré** : **406 et 407 sont UN SEUL dossier, classé RANG 2 — deux
  clés du contrat de synchronisation que le produit LIT sans que rien ne les
  ÉCRIVE.** Contrôle sur réponse connue du 477 : **passé**. **Le lot en absorbe
  deux** : les non classés passent de 16 à 15 pendant que le plan ne gagne qu'un
  dossier — la fusion est un gain de lisibilité, pas une perte de contenu.
  **Cause prouvée** : `myCapital` et `myTradesEquity` sont déclarées dans
  `DESK_KEYS`, lues par `capital()` et `equity()` (`vx-entities.js:235-236`), et
  **aucune ligne du dépôt ne les écrit** — `capital()` rend **toujours `null`**,
  en permanence. **Le compte de sites triple le dossier** : le 407 citait un
  `||0` (`:718`), il y en a **trois** — `:200` et `:208` dans `computeMetrics`,
  plus en amont que le site publié. **Témoin positif dix lignes plus bas** :
  `:604` se tait honnêtement quand `myTradesEquity` manque, alors que `myCapital`
  absent devient `0`. **Atteignabilité prouvée par exécution** : les deux
  accesseurs sont dans les octets servis de `/portfolio`. **Rang 2, et les trois
  arguments contre le rang 1 jouent tous contre moi** : l'erreur va dans le sens
  **prudent** (elle sur-alerte), `myCapital` **n'est écrivable par personne**, et
  une **lecture alternative** rend le calcul correct avec un libellé fautif —
  **je ne tranche pas, et le rang 2 survit aux deux lectures**. **Mutualisation
  forte** : `computeMetrics` (`:194-208`) est appelée juste avant `dominantRisk`
  (`:298`) — **les quatre dossiers du lot C tiennent dans une quinzaine de lignes
  consécutives**. **Chiffrage : 4 lignes, 1 fichier, aucun moteur** ; régression
  **faible**, la plus basse des dix-neuf. La variante ambitieuse (ouvrir un champ
  « capital » dans le desk) est **nommée et non chiffrée** : c'est une
  fonctionnalité, versée aux dossiers de décision. **Feuille : 19 dossiers · 52 à
  60 lignes · 19 gardiens · douze rang 1 · sept rang 2**, lot C porté à 14 lignes.
  Portée : **les bancs des 406 et 407 n'ont pas été rejoués** ; le « ×170 » est
  leur chiffre, sur des positions fabriquées. **Premier dossier classé dont le
  rapport d'origine ne contient aucune atténuation à démentir — à son crédit.**
  **Fait de méthode : un dossier peut être RÉDUIT par la mesure autant
  qu'aggravé.** J'ai commencé en pensant tenir un rang 1 ; trois mesures l'ont
  ramené à un rang 2. Pendant exact de l'observation du 477 : **la boucle doit se
  méfier autant des phrases par lesquelles elle aggrave que de celles par
  lesquelles elle minimise.** Aucun fichier de production touché · SW
  `td-shell-v187` · **MD5 8/8** · suite **2864 passed / 0 skipped**. Comptes :
  **44 (+1)** · 6 · 3 · 0.
- **Lot 477 — livré** : **le 378 classé RANG 2 — deux replis `0` atteignent bien
  l'entonnoir de `/opportunities`, et l'atténuation que le 378 avait publiée est
  RÉFUTÉE.** Contrôle sur réponse connue du lot précédent : **passé**. **Choix
  motivé** : le 378 est **le seul des dix-sept qui contredit une règle écrite**
  (« donnée absente → `—` honnête »), il s'était **arrêté à mi-chemin** (verdict
  « caractérisation, pas de faute prouvée »), et sa forme est **neuve** dans le
  classement. **Chaîne remontée jusqu'à l'écran** : `opportunities_api.py:22`
  et `:34` (`except Exception: return 0`) → `funnel.py:102-103` (étages
  « Suivis » et « Positions ») → `opportunities_page.py:194` puis `:220`.
  **Atteignabilité prouvée par exécution dans les deux sens** : une seule page
  servie cite la route, et `GET /api/opportunities/funnel` rend **200, sept zéros,
  aucune clé `error`**. **L'atténuation est réfutée** : le `try/except` interne
  capture **avant** celui de la route, donc le `500 + error` protège tout **sauf**
  les deux fonctions que le 378 prétendait couvrir par lui. **Publiés puis
  corrigés : 5 → 6.** **Témoin positif dans le même objet** : `funnel.py:111-113`
  marque explicitement un zéro légitime — **pour un étage sur sept**. **Rang 2** :
  affiché, servi, contraire à une règle écrite, et la marque était possible ;
  **mais** le chemin fautif est celui de l'**exception** (sur le chemin normal, `0`
  est exact), **la fréquence n'a pas été mesurée**, et l'entonnoir décrit sans
  prescrire. **Mutualisation cherchée et absente** — le dossier est isolé.
  **Chiffrage** : (a) recommandée, **3 lignes, 2 fichiers** (`return None` +
  marqueur d'étage) ; (b) 2 lignes, un drapeau `degraded`, **mais le « 0 » reste à
  l'écran**. **Régression la plus élevée des dix-huit** : changer le type d'un
  champ consommé par **au moins quatre fichiers de test** — moyen à élevé, à
  relire avant correction. Aucun octet servi, donc aucun bump. **Feuille : 18
  dossiers · 48 à 56 lignes · 18 gardiens · douze rang 1 · six rang 2**, avec un
  nouveau lot I « l'entonnoir ». Hors devis, en plus des seize non classés : **les
  dix autres replis numériques du 378**, ni tracés ni classés — nommés, non
  comptés. **Genre neuf : une protection qui existe, mais pas sur le chemin qu'on
  croit couvert** — pendant de la leçon 471. **Observation notée sans en faire une
  règle : sur les six derniers lots, cinq atténuations publiées ont été démenties
  par la vérification, alors que les défauts tiennent presque toujours ; ce que la
  boucle publie de plus fragile, ce sont les phrases par lesquelles elle minimise.**
  Aucun fichier de production touché · SW `td-shell-v187` · **MD5 8/8** · suite
  **2864 passed / 0 skipped**. Comptes : 43 · **6 (+1)** · 3 · 0.
- **Lot 476 — livré** : **le devis clos, la mesure reprend — le 417 est CLASSÉ
  RANG 1 et chiffré à 5 lignes.** Contrôle sur cas connu (`track_record.py:52-59`)
  **passé**. **Choix motivé** : la forme « un dénominateur qui n'est pas le
  dénominateur » est **déjà calibrée** par les 456 et 457, donc j'ai un étalon ; le
  devis avait déjà ouvert `track_record.py` ; et l'enjeu est le plus élevé des
  dix-huit — c'est la page qui dit **à quel point le moteur est fiable**. **Écarté
  sciemment : le 416**, trop proche du genre que je viens de nommer au 475 — se
  méfier d'aller rechercher ce qu'on vient d'inventer (leçon 463). **Le
  mécanisme** : `n` compte les entrées résolues à **au moins un** horizon, `f20` ne
  se remplit que si +20 séances existent, et le filtre `n >= 5` protège **le
  paquet, pas chaque nombre**. **Et `agg()` (`:163-166`) n'expose pas les vrais
  dénominateurs** — le moteur sait, et ne dit pas. **Témoin positif dans la même
  ligne** : quatre colonnes chiffrées, **une seule** (`TP1 avant stop`, `:450`)
  affiche son dénominateur — motif exact du 457. **Atteignabilité mesurée par
  exécution, et elle a failli me tromper** : `GET /performance` rend **301**, mais
  `redesign.py:108-111` monte `/journal` sur `performance_page.render()`, et
  `GET /journal` contient bien « Rdt +20 séances » et « tp1_resolved ».
  **Quatorzième récurrence des homonymes, forme neuve : `vertex/ui/journal.py` est
  MORT et `/journal` est rendu par `performance_page.py`** — le fichier qui porte
  le nom est mort, celui qui rend la page porte un autre nom. **Rang 1** : page
  servie, biais **structurel** (51 % de `N` sur 40 séances, mesuré au 417), et la
  page sait faire mieux une colonne sur quatre ; **pas plus** car aucun nombre
  n'est fabriqué — c'est une **attribution de dénominateur**, même famille que le
  447, rang 1 lui aussi. **Chiffrage : 5 lignes, 2 fichiers** (`agg()` +2 clés, la
  page +3 suffixes) ; **ne pas** durcir `n>=5`, ce serait cacher au lieu de
  qualifier. Régression **faible à moyen** — un `assert set(d.keys())` casserait,
  **à vérifier avant correction, je le nomme comme un point et non comme un fait**.
  **Mutualisation avec le lot B mesurée et partielle** : même fichier, deux
  fonctions, deux gestes ; à faire ensemble quand même, **mais le lot B perd son
  « aucun bump »**. **Feuille : 17 dossiers · 45 à 53 lignes · 17 gardiens · douze
  rang 1.** Portée : **le banc du 417 n'a pas été rejoué**, ses chiffres sont cités
  comme siens ; ce lot mesure que **les sites tiennent** et que **les dénominateurs
  ne sont pas exposés**. **Fait de méthode** : *quand une question porte sur ce que
  le produit FAIT, l'exécution tranche et la lecture propose* — deuxième fois en
  trois lots. Aucun fichier de production touché · SW `td-shell-v187` · **MD5 8/8**
  · suite **2864 passed / 0 skipped**. Comptes : **43 (+1)** · 5 · 3 · 0.
- **Lot 475 — livré** : **LE DERNIER DOSSIER — seize fichiers cachaient SIX
  sources, dont deux fonctions homonymes `_rr` et surtout UNE CONSTANTE.**
  Contrôle sur réponse connue mot pour mot (`pretrade.py:161`) : **passé**.
  **442+443 (rang 1) TIENT, et plus fort que ses deux rapports ne le disaient.**
  **Six sources** mesurées, pas seize : `analysis.py:262` `'rr': 3.0`
  **constante** · `:264` `rr_res` · `scenario_pricer.py:173` `gain/abs(loss)` ·
  `order_ticket.py:92 _rr()` · `options_lab.py:70 _rr()` · `terminal.py:432`
  `vx_rr`. **Treizième récurrence des homonymes sous une forme neuve : deux
  FONCTIONS du même nom dans deux modules**, dont l'une calcule un potentiel
  rapporté à une prime — unité différente. **Trois sources seulement atteignent
  l'écran**, toutes trois sous le libellé « R:R » ; la cinquième vit dans une page
  morte, donc **l'homonyme le plus dangereux est inatteignable**. **Le cœur** :
  `tp3` est défini comme `last + 3*risk`, donc « R:R structurel 3.0 » vaut **3 par
  construction, pour tout titre, dans tout régime** — le nombre est exact et
  n'informe de rien. **Genre neuf : UNE TAUTOLOGIE AFFICHÉE COMME UN RÉSULTAT.**
  **Chiffrage : 4 lignes, 1 fichier, aucun moteur** — et il ne faut **pas** toucher
  `analysis.py:262`, cohérent avec `tp3`. Deux variantes à coût identique ; la
  recommandée **(b)** remplace la tautologie par `rr_res`, **déjà calculée et déjà
  transmise dans le même dictionnaire**. Zéro gardien existant ; risque faible.
  **Deux sites retirés du dossier** : `ai/fallback.py:24` (non atteignable, mesuré
  au 455) et la source en page morte. **LE DEVIS EST CLOS — feuille de décision
  finale : seize dossiers · 40 à 48 lignes · 16 gardiens · onze de rang 1 · un
  seul bump · `_EMPREINTE` une seule fois.** **Huit lots de travail**, dont quatre
  ne touchant qu'un fichier chacun ; **quatorze des seize tiennent dans six
  emplacements**. Restent explicitement hors devis les trois dossiers de
  **décision** (469, 468, 466/467) et dix-huit dossiers jamais classés — **seize
  sur une trentaine**. **Fait de méthode qui clôt la série** : *un défaut peut être
  exact, servi, et vide ; la veine a passé cinquante lots à chercher des nombres
  FAUX, celui-ci est VRAI et n'informe de rien.* Aucun fichier de production
  touché · SW `td-shell-v187` · **MD5 8/8** · snapshot runtime 21 fichiers, écart
  final aucun · suite **2864 passed / 0 skipped**. Comptes : 42 · 5 · 3 ·
  **re-localisation 1 → 0**.
- **Lot 474 — livré** : **RE-LOCALISATION — trois dossiers sur quatre retrouvés
  et chiffrés, la collision de route du 452 prouvée par le routeur lui-même, et le
  433 tombe dans la fonction que le devis du 461 vise déjà.** Contrôle sur réponse
  déjà connue : **passé** (`analysis_page.py:856`). **447 (rang 1) retrouvé,
  tient, chiffré** : producteur `gex.py:232` (aucun filtre d'échéance), site du
  dossier `positions_api.py:206-215`, cinq consommateurs ; **le 447 citait
  `portfolio_page.py:484` et il avait raison — `:484` rend `g.detail`, chaîne
  construite trois fichiers plus loin.** **Fait de méthode neuf : un site de rendu
  générique ne porte pas le vocabulaire du défaut qu'il affiche** — le 473 en avait
  conclu « site introuvable » là où il fallait conclure « référence indirecte ».
  **1 à 2 lignes, chez l'appelant** ; ne surtout pas toucher `gex.max_pain()`, dont
  quatre autres consommateurs dépendent. **Seul dossier du devis déjà couvert par
  des tests** (4 + 4) → risque moyen. **452 (rang 1) retrouvé, tient, chiffré** :
  la collision est **prouvée par `app.url_map`** — deux règles vivantes pour
  `/api/anomalies/<sym>` (`analysis_api.py:59` et `strategy_os_api.py:104`), la
  seconde inatteignable, **et c'est la route morte qui porte l'avertissement
  d'honnêteté sur ses propres limites**. 1 ligne, mais une **décision de produit**
  préalable : laquelle doit vivre. **Gardien le plus rentable des quinze** —
  « aucune URL deux fois dans le routeur » protège les 189 règles, et c'est **le
  seul du devis dont l'échec est établi par exécution**. **432+433 (rang 1)
  retrouvé, tient** : les trois phrases sont `:231`, `:244`, `:398` (+ `:742`,
  `:744`), à conditionner à `allMarked` déjà calculé en `:197` — **3 lignes (+2)**,
  zéro gardien existant. **Mutualisation la plus forte du devis : le 461 (`:221`)
  et le 433 (`:231`) sont dans la MÊME fonction `dominantRisk`**, à dix lignes
  d'écart ; aucun des deux rapports ne pouvait le savoir, écrits à trente lots
  d'écart — **seul le devis, qui regarde les lignes et non les défauts, pouvait le
  voir**. **442+443 borné et renvoyé au 475** (onzième bornage). **Feuille de
  décision : quinze dossiers · 36 à 44 lignes · 15 gardiens · dix rang 1 · un seul
  bump.** Treize des quinze tiennent dans cinq emplacements ; **sept lots de
  travail**, dont le nouveau **F « les routes » (447+452+456, 4 lignes, 2 rang 1,
  aucun octet servi)** — avec sa réserve : seul lot touchant un site déjà testé et
  seul exigeant une décision de produit. Aucun fichier de production touché · SW
  `td-shell-v187` · **MD5 8/8** · snapshot runtime 21 fichiers, écart final aucun ·
  suite **2864 passed / 0 skipped**. Comptes : 42 · 5 · 3 · **re-localisation
  4 → 1**.
- **Lot 473 — livré** : **LE DEVIS, TROISIÈME TRANCHE — le rang 1 le plus utile
  chiffré à 6 lignes, mais QUATRE dossiers sur cinq ne sont pas devisables en
  l'état**, et c'est le résultat du lot : leurs sites publiés ne contiennent plus
  ce qu'ils annoncent, et chiffrer par-dessus aurait produit un devis **propre et
  faux**. **Le contrôle échoue au premier jet** (2ᵉ fois de la veine, après 467) :
  le témoin du 464 annoncé en `decision_memory.py:54` est un `return None` ; le
  vrai est en **`:111`** — la référence venait de **mon propre réveil**, pas du
  rapport. Et il rend mieux que prévu : `:71-73` montre que le drapeau `demo`
  entre **dans le hash d'identité** de la décision. **464 (rang 1) chiffré :
  6 lignes, 3 fichiers** — `skyler_journal` 2 l. (aucun test ne l'appelle),
  `session_log` 2 l. avec **mot-clé à défaut obligatoire** (huit appels de test à
  quatre positionnels), `track_record` 2 l. **sans changement de signature mais
  avec un import**, car `scan_state` ne porte ni `source` ni `demo`. **Aucun octet
  servi, aucun bump.** N'achète que l'avenir (`edge_ledger` est append-only).
  **Atteignabilité failli publiée fausse** : mon grep donnait « aucun appelant en
  production » pour `track_record.record()` — l'appel existe **sous un alias
  d'import** (`terminal.py:66` puis `:1430`) ; **quatorzième récurrence du piège
  du détecteur à une seule forme, cette fois sur la forme d'un APPEL**.
  **Non devisables** : **447** (le mot `max_pain` n'apparaît dans aucun des deux
  fichiers cités), **452** (`:929` est l'invocation, le corps est en **`:856`**),
  **432+433** (les lignes citées sont les mécanismes, pas les phrases),
  **442+443** (seize fichiers, deux rapports croisés — un lot entier). **Feuille
  de décision : douze dossiers · 31 à 37 lignes · 12 gardiens · sept rang 1 · un
  seul bump · `_EMPREINTE` une seule fois.** `markets_page.py` porte **4 dossiers
  dont 3 rang 1 pour 6 lignes** ; **dix des douze tiennent dans quatre fichiers**.
  **Six lots de travail autonomes (A à F)**, le A (« /markets », 427+428+425) étant
  le meilleur rapport valeur/risque. Nommé et non chiffré : les quatre dossiers
  ci-dessus et **dix-huit dossiers jamais classés** — douze sur une trentaine
  ouverts. **Fait de méthode** : *un rapport de mesure établit qu'un défaut
  EXISTE ; il n'établit pas OÙ il est d'une façon qui survive au temps* — et
  quarante-neuf lots de veille n'avaient produit que le premier. Aucun fichier de
  production touché · SW `td-shell-v187` · **MD5 8/8** · snapshot runtime 21
  fichiers, écart final aucun · suite **2864 passed / 0 skipped**. Comptes :
  arrêtés avant publication **42 (+2)** · publiés puis corrigés **5** ·
  interprétations retirées **3** · **nouveau compteur : 4 dossiers en attente de
  re-localisation**.
- **Lot 472 — livré** : **LE DEVIS, SECONDE TRANCHE — six dossiers chiffrés (6 à
  11 du classement), et le résultat structurant n'est aucun des six.** Contrôle
  sur un cas **doublement** connu (`catOf`, publié au 458 puis remesuré au 461) :
  retrouvé à `opportunities_page.py:475-477`, quatre `return` collés, rendu
  `:489` — **passé avant tout chiffrage**. **428 (rang 1)** : `markets_page.py:786-787`,
  **2 lignes**, et un piège que le correctif naturel aurait déclenché — mettre le
  prédicat « en anglais » est **faux**, le repli `|| r.decision` est alimenté en
  français par `terminal.py:596` ; **les deux vocabulaires doivent coexister**.
  **437 (rang 1)** : **trois clients** (`briefing.py:351`, `markets_page.py:637`,
  `opportunities_page.py:634`) et **deux producteurs** (`terminal.py:1200`, `:1220`) ;
  `content.py:40` sert `{**cal_state}`, donc **une clé ajoutée est servie sans
  toucher la route** ; variante (a) 3 lignes supprime l'affirmation **et** la
  fraîcheur, variante **(b) 5 lignes** la rend réelle — **seul des onze dossiers
  où la variante chère est la bonne**. **456 (rang 2)** : le plafond tient en
  **une ligne**, `strategy_os_api.py:167` `[:200]` — personne ne ment, un seul
  tronque ; deux correctifs, et **le choix est une décision**. **463 (rang 2)** :
  `record()` prend **un seul paramètre** et **quatre tests l'appellent ainsi** —
  un second paramètre **positionnel** les casserait ; il faut `demo=False`,
  mot-clé à valeur par défaut. **4 lignes**, moteur touché mais sur une **garde
  d'entrée** ; et **le correctif n'achète que l'avenir** (`_MAX_DAYS=120`, quatre
  mois de rétention). **Découverte de cadrage : la conclusion « `_EMPREINTE`
  jamais » du 471 n'était vraie que de ses cinq dossiers** — `options-gex.js` vit
  sous `vertex/static/vertex/js/pages/`, donc `_EMPREINTE` **et** `_SW_VERSION`
  seraient à mettre à jour ; je restreins la conclusion du 471 explicitement.
  **425 (rang 1)** : **trois sites, pas un** (`:93-94` HTML statique, `:598`
  `limits`, `:580` commentaire) alors que `:586` trace dès 2 points — la leçon
  « compter les sites » **double le chiffrage** ; contrainte : `:93-94` ne peut
  pas lire `pts`. **458 (rang 2)** : **seul dossier des onze dont le correctif
  complet est impossible** — les catégories de la Constitution se chevauchent sur
  le delta ; le devis recommande de **renommer** la colonne (1 ligne) plutôt que
  de prétendre la résoudre (4 à 6 lignes). **Total seconde tranche : 6 fichiers ·
  15 à 18 lignes · 6 gardiens · 3 rangs 1. Total des onze : 25 à 30 lignes · 10
  gardiens · 6 rangs 1 · un seul bump SW.** **Mutualisation plus forte qu'au
  471** : `markets_page.py` porte **trois** dossiers dont deux rang 1, et sur les
  deux tranches **sept des onze tiennent dans trois fichiers**. Gardiens existants
  sur les six sites : quasi nuls. **Fait de méthode** : au 471 la relecture
  corrigeait des **faits**, ici elle révèle des **contraintes d'exécution** — qui
  ne se lisent dans aucun rapport de mesure et n'apparaissent qu'en préparant le
  geste. Aucun fichier de production touché · SW `td-shell-v187` · **MD5 8/8** ·
  snapshot runtime 21 fichiers, écart final aucun · suite **2864 passed /
  0 skipped**. Comptes **inchangés** : 40 · 5 · 3 — les quatre pièges sont des
  contraintes découvertes, pas des erreurs corrigées.
- **Lot 471 — livré** : **LE DEVIS — cinq dossiers chiffrés ligne par ligne, et
  l'exercice invalide DEUX affirmations publiées.** Premier lot de la tranche
  470-479 et premier lot d'un genre nouveau : le bilan n°16 ayant constaté le
  recul des défauts affichés (7 → 3) et le critère posé d'avance au n°15 étant
  rempli, ce lot exécute la recommandation **(b)** — chiffrer le coût de
  correction **sans rien corriger**. **Contrôle sur un cas dont la réponse était
  DÉJÀ connue (leçon 467), passé AVANT tout chiffrage** : le devis retrouve
  `portfolio_page.py:266`, littéral `' / 10'`, exactement là où le 457 l'avait
  publié. **Parade posée avant la première mesure** — relire chaque ligne citée
  dans le fichier réel avant de la chiffrer ; **elle a servi quatre fois**.
  **457 (rang 1)** : trois lignes portent le 10 (`:266`, `:267`, `:268`) ; la
  correction pressentie du 457 est **RÉFUTÉE** — `renderSummary` (l.248) ne
  reçoit que `rich`, les 2 seules occurrences de `bounds` (l.961-962) vivent dans
  `renderDiscipline` (l.950) ; co-visibilité mesurée **sur 1 vue / 4** (le KPI est
  sur quatre vues, la carte des bornes sur la seule vue Risque, et sur la Synthèse
  le KPI n'apparaît pas) ; **troisième récurrence de la leçon 468 en direct** —
  `portfolio_target_positions` **n'existe pas** sur l'objet, c'est
  `portfolio_max_positions` (15), `portfolio_min_positions` (8),
  `max_stock_weight_pct` (15.0), et la V1 donne bien **10** ; trois chemins
  chiffrés, **(a) injection serveur ≈ 5 lignes retenu** car le mécanisme est déjà
  dans le fichier (`json_for_script`, `%%VIEW%%` l.1005). **455 (rang 2)** :
  `pretrade.py:161-166`, gabarit à trois `%d`, **2 lignes** — et correction de
  l'attendu du réveil, **un des cinq touche bien un moteur** (`vertex/engines/`),
  mais sur une f-string ; **seul des cinq à ne pas exiger de bump**. **461
  (rang 2)** : `:221`, **1 à 2 lignes**, et un piège que seule la relecture
  montre — **deux littéraux `>25` dans la même fonction** (l.221 concentration,
  l.228 options), douzième récurrence des homonymes. **434 (rang 1)** : 1 ligne,
  et **le chiffre du 434 est faux** — la garde n'est pas « vingt lignes plus
  haut » mais **362** (l.237 vs l.599) ; la substance tient. **427 (rang 1)** :
  1 ligne, `legend:wanted.map` → `sets`, et le même geste corrige les deux
  défauts. **Total : 4 fichiers · 10 à 12 lignes · 4 gardiens à écrire · 3 rangs 1
  · UN SEUL bump SW · `_EMPREINTE` jamais** (mesuré : elle n'agrège que
  `vertex/static`, qu'aucun des cinq ne touche). **Gardiens existants sur les cinq
  sites : ZÉRO.** Le fait le plus utile est la **mutualisation** : 457 et 461
  partagent fichier et profil — faits ensemble, le second ne coûte plus qu'une
  ligne. **Quatre relectures, quatre écarts**, dont trois qui auraient envoyé un
  correcteur au mauvais endroit et un droit dans une exception ; aucun ne renverse
  un classement. **Genre neuf : une correction pressentie qui désigne une variable
  hors de portée — juste au niveau de la PAGE, faux au niveau de la FONCTION.**
  Les trois dossiers qui ne sont pas des correctifs (469, 468, 466/467) sont
  nommés et **laissés hors de tout devis** : on ne devise pas ce que personne n'a
  décidé de corriger. Aucun fichier de production touché · SW `td-shell-v187` ·
  **MD5 8/8** · snapshot runtime 21 fichiers, écart final aucun · suite **2864
  passed / 0 skipped**. Comptes : arrêtés avant publication **40** · publiés puis
  corrigés **5** (+1) · interprétations retirées **3** (+1).
- **Lot 470 — livré** : **BILAN n°16 (tranche 460 → 469) — la cadence baisse
  pour la première fois de façon nette, le critère que j'avais posé bascule, et
  il faut le suivre.** Seizième bilan, **sur pièces**, aucune trouvaille rejouée,
  **une seule mesure fraîche (les MD5)**.
  **Base résolue AVANT tout chiffre** : `1b23377` **ancêtre vérifié** → `c44ef80`,
  **10 commits** ; **12 fichiers**, **0 hors `docs/`**, **+3 047 / −0**, **0
  fichier de production** ; 10/10 partout ; **114 435 octets** ; **MD5 8/8**.
  Depuis `20a917f` : 70 commits, 73 fichiers, 1 hors docs, **0 production**.
  **Correction publiée contre mon propre réveil** : il annonçait « arrêtés
  32 → 40 » — **faux**, le départ était **26** et l'énumération omettait 465 et
  467. **Mesuré : 26 → 40, +14.**
  **Bilan des dix lots** : **1 rang 1 · 2 rang 2 · 2 rang 3 · 2 rang 4 · six
  lots sur dix qui BORNENT**.

  ```text
                       rang 1 PAR LOT   PAR DOSSIER   DÉFAUTS AFFICHÉS
  420-429                    4               4               —
  430-439                    4               3               5
  440-449                    3               2               5
  450-459                    2               2               7
  460-469                    1               1               3      ← −4
  ```

  **LE CRITÈRE BASCULE.** Le bilan n°15 avait écrit : « au premier bilan où les
  défauts affichés reculeront, (b) devient la bonne réponse ». **Ils reculent,
  7 → 3. Je recommande (b), le lot DEVIS** — première fois en sept bilans que la
  recommandation change, **non parce que j'ai changé d'avis mais parce que le
  chiffre choisi d'avance a franchi le seuil fixé d'avance**.
  **Fait de méthode dominant, et il dérange : dans HUIT des NEUF lots de mesure,
  l'instrument était FAUX au premier jet** — contrôle (461), taille (462),
  **lecture de la liste** (463/464/466), **contrôle lui-même faux** (467), chemin
  trop court (468), **atteignabilité supposée** (469). Treize corrections
  d'instrument, deux erreurs de raisonnement. **La conclusion honnête n'est pas
  « la boucle s'améliore » : tout lot qui n'a pas attrapé son instrument est
  SUSPECT.** Argument de plus pour (b) — **un devis se vérifie en le lisant, une
  mesure ne se vérifie qu'en la refaisant.**
  **L'atteignabilité** : trois candidats tués, **deux vérifiés (tiennent), un
  SUPPOSÉ (faux, corrigé au 469)**. Excellent quand on le mesure, dangereux
  quand on l'invoque.
  **Comptes** : arrêtés **26 → 40 (+14)** · publiés puis corrigés **3 → 4** ·
  interprétations retirées **1 → 2**. Le +1 vient d'une phrase **hedgée et non
  classée** — je maintiens qu'elle comptait.
  **Classement à 19 dossiers** ; le **n°12** est le rang 1 le plus utile (**464**,
  passer `demo` à `record()` : `DEMO_MODE` **déjà en portée**, et
  `decision_memory` **fait déjà exactement ce qu'il faut**) ; **les onze premiers
  ne touchent aucun moteur** ; **les trois derniers ne sont pas des correctifs**,
  ils demandent qu'on **décide**.
  **Portée** : le bilan reprend les erreurs des rapports, et la tranche vient de
  démontrer que cela arrive ; **le classement est attribué par moi-même** — en
  classant le DTE du 469 en rang 2, les défauts affichés seraient 4 et non 3, la
  conclusion tiendrait mais **moins nettement** ; **seule mesure fraîche, les
  MD5**.
  **Seizième tranche sans qu'un seul défaut prouvé ait été corrigé.**
  **Aucun code, aucun gardien, aucun test ; aucun GO demandé, rien d'engagé.**
  Suite **2864 passed / 0 skipped** ; écart runtime **aucun**.
- **Lot 469 — livré** : **les deux dettes du 468 soldées, et l'une CONTRE ma
  propre inclinaison — le board sélectionne bien des contrats sous le minimum
  absolu de la Constitution, par une SECONDE source de configuration qui la
  contredit.** 49ᵉ lot, **dernier de la tranche 460-469** : un dernier lot solde
  et n'ouvre pas de front.
  **Dette (a) — ATTEIGNABLE, je m'étais trompé.** Le 468 écrivait qu'un contrat
  sous 60 jours « n'atteint probablement jamais le board ». **Faux.** Chaîne
  remontée jusqu'au bout : `best_for_symbol` va chercher sa chaîne **lui-même**
  chez le fournisseur (`yf.Ticker().option_chain()`) — **il ne passe ni par
  `chain_loader`, ni par `contract_filter`**, les deux modules qui appliquent
  `dte_within_constitution` (ils servent `call_selector` et `bearish_tactical`,
  pas le board).

  ```text
  OPTION_BUCKETS (vertex/strategy/config.py:31)
     court  min  25 · CIBLE  45 · max  75      ← sous le plancher
     moyen  min  75 · cible  90 · max 135
     long   min 150 · cible 210 · max 400
  Constitution  options_profile.dte.absolute_minimum = 60
  computeVerdict  n'avertit qu'en dessous de 20

  les QUATRE écrivains du board passent buckets=('court', …) :
     terminal.py:1073 · terminal.py:1586 · legacy_engine.py:336 · weekly.py:222
  ```

  **La cible du bucket court est 45 : ce n'est pas un cas limite, c'est la zone
  visée.** **Mais la borne de 60 n'est affichée NULLE PART** (« DTE absolu »,
  « absolute_minimum », « 60-540 » → aucun objet servi ; le seul rendu qui
  l'affiche appartient à un module non servi). **Aucun nombre faux à l'écran.**
  **Rang 3** — pas plus, rien de faux à l'écran ; pas moins, la politique de
  sélection réelle diffère du document que le reste de l'app traite comme
  faisant autorité. Le commentaire de `config.py:29` **assume** le choix, mais
  **il est dans un commentaire, pas dans la Constitution**, qui pose 60 **sans
  exception** et est verrouillée par `test_constitution_v2.py`.
  **Genre neuf : DEUX SOURCES DE CONFIGURATION QUI SE CONTREDISENT, ET LE CODE
  SUIT CELLE QUI N'EST PAS LA CONSTITUTION.** Fait net : **le dépôt a un
  sélecteur qui respecte la Constitution et un qui l'ignore — c'est le second
  qui remplit le board.**
  **Dette (b) — RÉFUTÉE.** `analysis.py:228` rend un score **/100** ;
  `skyler_score.blocks` somme **40** et `conviction_levels` est en **/40**.
  **Deux moteurs, deux grandeurs** : les 72/66/56 de `bucketOf` et les 36/32/28
  de la Constitution ne mesurent pas la même chose. **L'insinuation du 468 est
  retirée**, et la conversion `sc<=40?sc:round(sc/2.5)` confirme que le dépôt
  connaît la dualité. **Onzième récurrence des homonymes, forme nouvelle : un
  même NOM DE CHAMP (`score`) pour deux grandeurs de deux moteurs.**
  **Mes comptes, et celui-ci n'est pas confortable** : le 468 a **publié**,
  hedgé et non classé, que la branche était « probablement inatteignable » — **un
  lecteur en serait reparti avec une croyance fausse. Je le compte : publiés
  puis corrigés 3 → 4.** Ne pas l'avoir classé **n'efface pas de l'avoir
  écrit** ; ce qui a sauvé le dossier, c'est d'avoir écrit « non tranché » **dans
  le verdict**.
  **Portée** : chaîne établie **par lecture**, **aucun réseau appelé** ;
  proportion réelle de contrats courts **non mesurée** (board vide) ; **je ne
  juge pas le choix du bucket**, je mesure qu'il contredit la Constitution ;
  **aucun navigateur**.
  **Fait de méthode, écrit à la veille du bilan : l'atteignabilité a tué trois
  candidats dans cette tranche (462, 465, 468) et j'en ai fait un RÉFLEXE. Le
  quatrième cas en montre le prix — j'ai SUPPOSÉ l'inatteignabilité au lieu de
  la MESURER. L'atteignabilité est un TEST, pas une intuition ; une chaîne
  « probablement filtrée » qui n'a pas été remontée jusqu'au fournisseur n'est
  pas filtrée du tout.**
  **Aucun code, aucun gardien, aucun test ; aucun GO demandé, rien d'engagé.**
  Anti-doublon `total 100 · actifs 0` ; aucun fichier touché ; MD5 **8/8** ;
  snapshot runtime 21 fichiers, écart final **aucun** ; suite **2864 passed /
  0 skipped**. Comptes : arrêtés **40**, publiés puis corrigés **4**,
  interprétations retirées **2**.
- **Lot 468 — livré** : **les seuils décisionnels contre la Constitution —
  dix-neuf valeurs concordent, aucune divergence NEUVE, et la vraie trouvaille
  est que la moitié des seuils des classeurs n'a AUCUNE source de
  configuration.** 48ᵉ lot, huitième et **dernier lot d'ouverture** de la
  tranche (le 469 solde, le 470 est le bilan n°16). Seule piste de la liste
  jamais ouverte : les seuils en dur des 13 classeurs du 461.
  **Calibrage** : le 462 avait tranché les **phrases** qui citent un seuil ; ici
  **les seuils eux-mêmes**. Critère décisif — **seuil de STRATÉGIE** (décide un
  verdict produit → devrait venir de la Constitution) contre **seuil de
  PRÉSENTATION** (exclu, nommé). **Deux passes** : config → code, et code →
  config.
  **Deux contrôles sur des cas connus (leçon 467)** : le **457** (« Actions / 10 »
  contre `maximum = 15`) ressort **SOURCÉ DIVERGENT** ; le **458** (échelle de
  conviction) ressort **SOURCÉ CONCORDANT**. Les deux passent.
  **Correction d'instrument attrapée par la passe A** : elle a déclaré
  `max_simultaneous_bearish_positions` et `target_call_share_pct` « clé absente »
  alors qu'elles vivent sous `.options_profile.` — **un « absent » qui n'était
  qu'un chemin trop court**. Faux arrêtés : **39 → 40**.

  ```text
  SOURCÉ CONCORDANT                                   19 valeurs
     échelle de conviction  8   ·  bandes de delta   6
     paliers de gain        4   ·  plancher OI 500   1
  SOURCÉ DIVERGENT                                     2 — TOUS DÉJÀ CONNUS
     « Actions n / 10 » vs 15 (457) · dominantRisk >25 vs 15 (461)
  ```

  **Aucune divergence NEUVE. Dixième bornage consécutif.**
  **Fait neuf** : sur les **cinq** paliers de gain servis, **quatre concordent**
  avec `review_thresholds_gain_pct = [30, 50, 75, 100]` — **le palier +20 % n'a
  aucune source**.
  **La vraie trouvaille — SIX concepts n'ont AUCUNE clé dans tout le profil** :
  la **liste de 6 tickers défensifs** de `roleOf` · la **prime « > 12 % du
  notionnel »** · la **proximité du stop × 1,04** · l'**asymétrie 3 / 1,8 / 1,2**
  · les **gradations de spread 3 / 6 / 10** · le **palier +20 %**. **Pour ces six,
  le littéral EST la Constitution** : ils décident « Défense / gardien »,
  « Structure intéressante mais chère », « Fragilisée », « Asymétrie
  excellente », « Liquidité acceptable » — **et rien ne les gouverne, ni version,
  ni test**. Pas un mensonge à l'écran : une **surface de décision hors
  Constitution**. **Rang 4**, la valeur du lot est la mesure.
  **Le contraste rend le résultat lisible : là où une clé existe, le code la
  respecte 19 fois sur 21. Le problème n'est pas la désobéissance, c'est
  l'absence de loi sur la moitié du terrain.**
  **Deux candidats NON classés** : `liqState` tolère 6 % de spread quand
  `LEAPS.spread_pct_max = 5.0` — **portées différentes** (clé par catégorie,
  classeur générique), leçon 458, **nommé non classé** ; et `computeVerdict` ne
  signale une échéance courte qu'**en dessous de 20 j** quand le minimum absolu
  est **60** — **mais `chain_loader.py:24` et `contract_filter.py:18` filtrent
  déjà sur [60, 540]**, chaîne non établie de bout en bout → **règle 442/445,
  non classé**. **Troisième candidat sérieux de la tranche tué par
  l'atteignabilité** (après 462 et 465) : c'est le filtre dominant.
  **Portée** : liste de limites **fermée** (six clés) · passe B héritant du
  périmètre des 13 classeurs · `bucketOf`/`tierOf` en **/100** contre une
  Constitution en **/40** — équivalence **non prouvée, non comptée** ·
  « aucune clé » établi par balayage sur mots-clés · **aucun banc, aucun
  navigateur**.
  **Genre neuf : UN SEUIL QUI DÉCIDE SANS LOI.**
  **Aucun code, aucun gardien, aucun test ; aucun GO demandé, rien d'engagé.**
  Anti-doublon `total 100 · actifs 0` ; aucun fichier touché ; MD5 **8/8** ;
  snapshot runtime 21 fichiers, écart final **aucun** ; suite **2864 passed /
  0 skipped**. Comptes : arrêtés **40**, publiés puis corrigés **3**,
  interprétations retirées **1**.
- **Lot 467 — livré** : **l'intervalle [22, 37] du 466 se résout à 28 — neuf des
  quinze suspectes étaient des redirections de compatibilité, et mon CONTRÔLE
  obligatoire était lui-même mal spécifié : il rejetait un instrument juste.**
  47ᵉ lot, septième de la tranche. Le 466 avait publié un intervalle faute
  d'avoir tranché quinze routes citées uniquement depuis `terminal.py`.
  **Calibrage** : chaque citation classée par sa **position syntaxique** (`ast`)
  — **A** déclaration (`@…route`) · **B** appel Python (`redirect`, `url_for`,
  `client.get`…) · **C** texte client. **Une seule citation B suffit à déclarer
  la route consommée.**
  **LE FAIT DE MÉTHODE — mon contrôle était faux** : il a rendu « 0 citation B →
  AVEUGLE AUX APPELS, VERDICT NUL ». **Le classeur n'était pas aveugle** : le
  contrôle cherchait un B **parmi les suspectes**, or c'est **le résultat
  cherché**, pas une preuve. Refait en deux volets :

  ```text
  V1 fixture synthétique  route→A · redirect→B · href→C · client.get→B   SAIN
  V2 témoin réel /analysis/   A=1 B=2 C=2
     B → redesign.py:256  redirect(f'/analysis/{sym}', code=301)      VOYANT
  ```

  **Jusqu'ici mes contrôles n'attrapaient que des faux POSITIFS ; celui-ci a
  produit un faux NÉGATIF. Le contrôle peut être faux dans les DEUX sens.**
  **Cinquième correction** : le témoin V2 a révélé que `/titre/<sym>` est une
  **redirection 301** — le 466 avait bâti K4 depuis le **dictionnaire**
  `LEGACY_REDIRECTS` et ne voyait pas celles **déclarées par décorateur**.
  Reclassement **par le corps de la vue** → **9 redirections** parmi les 37.
  **Verdict des quinze : 9 redirections · 6 orphelines confirmées · 0
  consommée.** Aucune n'était un appel serveur — mais **neuf n'étaient pas
  mortes pour autant**.

  ```text
  189 règles = 98 K1 + 28 K2 + 9 K3 + 21 K4 + 5 E3 + 28 ORPHELINES
                                            28 / 189 = 14,8 %
  ```

  **L'intervalle se résout à 28 ; le plafond de 37 était gonflé de NEUF.**
  **Deux corrections d'unité** : les « 53 citations de `/titre/<sym>` » du 466
  étaient des **occurrences de sous-chaîne**, pas des sites — **12 littéraux
  distincts** par nœud `ast` ; et ces douze pointent vers une redirection **qui
  fonctionne**, donc **pas des liens cassés**.
  **Lignes mortes de `terminal.py`** : `/desc/<sym>` 30 · `/api/correlations/`
  26 · `/weekly-regen` 13 · `/api/company/` 6 · `/api/rescan` 5 ·
  `/api/alerts/status` 3 → **83 sur 7 154, soit 1,2 %**. **Limite** : ne couvre
  que les handlers ; les 18 citations « texte client » vivent **au niveau
  module** et **ne sont pas dans les 83 lignes**.
  **Portée** : classe B sur **liste fermée d'appelants** — un dispatch dynamique
  gonflerait le compte · le test K4 (« contient `redirect(` et rien d'autre »)
  est **grossier**, même si les neuf ont un corps identique · **compte exact
  pour la méthode, pas absolu** · **aucune route appelée** · **aucun navigateur**.
  **Neuvième bornage consécutif**, et le neuvième **réduit** encore ce que la
  boucle croyait avoir trouvé.
  **Règle : un contrôle doit porter sur un cas dont on connaît DÉJÀ la réponse ;
  un contrôle qui porte sur la question posée ne contrôle rien.**
  **Aucun code, aucun gardien, aucun test ; aucun GO demandé, rien d'engagé.**
  Anti-doublon `total 100 · actifs 0` ; aucun fichier touché ; MD5 **8/8** ;
  snapshot runtime 21 fichiers, écart final **aucun** ; suite **2864 passed /
  0 skipped**. Comptes : arrêtés **39**, publiés puis corrigés **3**,
  interprétations retirées **1**, + **une correction d'unité** sur un chiffre
  du 466.
- **Lot 466 — livré** : **les routes qui travaillent pour personne — entre 22 et
  37 des 189 règles déclarées n'ont aucun consommateur atteignable, et 15
  d'entre elles ne sont citées que depuis du JS de `terminal.py` qui n'atteint
  plus aucune page.** 46ᵉ lot, sixième de la tranche. Le 465 a nommé « du code
  complet et correct qui n'est pas servi » ; ce lot attaque la classe entière.
  **Calibrage** : trois classes posées d'avance (**K1** cité dans les 42 objets
  servis · **K2** appelé par un module serveur · **K3** page de navigation), et
  **la règle qui décide de tout — appariement sur le PRÉFIXE STATIQUE**, une
  route paramétrée n'apparaissant jamais littéralement dans les octets servis.
  **Trois corrections d'instrument, et les trois sur LA MÊME confusion : du
  texte destiné au CLIENT, écrit dans un fichier PYTHON, n'est pas du code
  SERVEUR.**

  ```text
  1  vertex/ui/**.py dans le corpus K2  → LE CONTRÔLE A ÉCHOUÉ au premier tir
     (/api/alerts/status, orpheline connue du 465, ressortait « interne »)
  2  aucune classe pour les redirect(…, 301) → 12 fausses orphelines
     leur NON-CITATION est leur RAISON D'ÊTRE  → K4
  3  les chaînes JS de terminal.py encore dans K2 — révélé par /news-feed
  ```

  Faux arrêtés : **34 → 37**.

  ```text
  189 règles déclarées (hors static)
     98  K1 consommée par un objet SERVI
     43  K2 « serveur interne »            ← borne HAUTE
      9  K3 navigation
     12  K4 redirection 301
      5  E3 infrastructure
     22  ORPHELINES
  ```

  **K2 est contaminée et je la BORNE au lieu de la réparer** : **15 des 43** sont
  citées **uniquement depuis `terminal.py`** et **absentes des octets servis** —
  `/titre/<sym>` **53 citations**, `/settings` **22**, `/bordel` **20**,
  `/catalysts` 15, `/entreprises` 13, `/ma-page` 11. **Cinquante-trois citations
  et pas un octet servi** : c'est la mesure des pages mortes du monolithe.
  **Le compte est donc un INTERVALLE : 22 plancher ferme, 37 plafond — 12 % à
  20 % de la surface HTTP.** Les quinze **ne sont pas tranchées une par une**.
  **Le coût est faible** : **1 écrit** (`/desc/<sym>`), **2 coûtent du réseau**
  (`/desc/<sym>`, `/api/correlations/<sym>`), **20 sont inertes**. Surface de
  maintenance, **aucun mensonge à l'écran → rang 4** : la valeur du lot est la
  **mesure**.
  **Fait nommé** : le CLAUDE.md justifie l'assainissement de trois sorties
  « car leurs consommateurs injectent le titre brut en innerHTML » ; mesuré,
  **`/api/skyler/` est citée par 4 objets, `/api/events/` et `/news-feed` par
  AUCUN**. L'assainissement reste **juste et utile** (sûreté gratuite, gardien
  vert) ; **c'est la JUSTIFICATION consignée qui est inexacte** — même famille
  que la correction du SHA du lot 399 au 460. **Nommé, non classé.**
  **Homonymes, dixième récurrence, évitée par construction** : `/api/live/events`
  EST servi, `/api/events/` non — une recherche naïve du mot « events »
  (27 occurrences) aurait conclu l'inverse.
  **Portée** : intervalle et non nombre · K1 par **préfixe** — une URL assemblée
  autrement serait faussement orpheline (**non quantifié**) · « écrit »/« réseau »
  par **motifs dans la source de la vue**, donc **coût sous-estimé** ·
  **aucune route appelée** · **aucun navigateur**.
  **Huitième bornage consécutif.** Genre confirmé : **UNE ROUTE QUI TRAVAILLE
  POUR PERSONNE**, variante **UNE CITATION QUI NE SORT JAMAIS DU DÉPÔT**.
  **Aucun code, aucun gardien, aucun test ; aucun GO demandé, rien d'engagé.**
  Anti-doublon `total 100 · actifs 0` ; aucun fichier touché ; MD5 **8/8** ;
  snapshot runtime 21 fichiers, écart final **aucun** ; suite **2864 passed /
  0 skipped**. Comptes : arrêtés **37**, publiés puis corrigés **3**,
  interprétations retirées **1**.
- **Lot 465 — livré** : **les deux dettes du 464 soldées, toutes deux en
  NÉGATIF — l'élargissement du détecteur ne trouve AUCUN nouvel accumulateur, et
  l'alerte déclenchée par un prix de démo n'atteint aucun écran parce que son
  consommateur n'est pas servi.** 45ᵉ lot, cinquième de la tranche. Un lot qui
  solde vaut un lot qui ouvre (modèle 449/455/457/459).
  **Calibrage** : les deux critères du 464 reposés (**donnée de marché** ·
  **écraser n'est pas accumuler**) ; huit mécanismes d'écriture nommés d'avance ;
  **`persist.py` exclu — c'est la PRIMITIVE, pas un écrivain**.
  **Dette (ii)** : détecteur du 464 **28 sites** → élargi **46 sites, +18**.
  Contrôle double passé dès la première exécution : `track_record.record`
  retrouvé **par ses deux mécanismes** (`open(…,'a')` ET `save_json`),
  `gex_history.record` retrouvé.

  ```text
  les 18 sites manqués = 11 écrivains distincts, lus un par un
     1  déjà trouvé au 464      track_record.record
     3  SANS OBJET              .vertex_secret · backup desk · Constitution
     4  CACHES (écrasent)       company · constituents · analyst_deep · desc_ep
     1  FENÊTRE 2 JOURS         daily.save_state (cur + prev)
     1  ÉCRASE (os.replace)     weekly.save_snapshot
     1  JAMAIS INSTANCIÉ        strategy/memory/store
     ──
     0 NOUVEL ACCUMULATEUR DE DONNÉE DE MARCHÉ
  ```

  **Le compte du 464 — sept accumulateurs — TIENT.** C'est le meilleur résultat
  qu'une dette d'instrument puisse rendre : la mesure précédente était
  **complète pour ce qu'elle prétendait mesurer**.
  **Deux faits nommés** : `strategy/memory/store` **n'est instancié nulle part en
  production** (aucun `MemoryStore(` hors tests) — écrivain **mort** — et il porte
  pourtant une **garde exemplaire** (`add()` refuse l'actif sans
  `confirmed_by_human=True`, `active()` ne rend que `CONFIRMED`) : **second témoin
  positif, mais de CONCEPTION et sur l'ACTIVATION, pas la provenance — non
  compté** ; `daily.save_state` garde `prev`, donc un jour de démo survit **un
  jour** dans le Diff de `/` — borné, **pas de la perpétuation, non classé**.
  **Dette (i)** — `alerts_fired.json` : `_alert_price` retombe sur
  `scan_state['detail']`, donc **un prix synthétique en DEMO** ; l'entrée écrite
  n'a **aucun champ de provenance** ; le fichier **accumule** (200, sans
  expiration) ; et `if aid in _ALERTS_FIRED: continue` fait qu'**une alerte
  déclenchée n'est plus jamais réévaluée**. **Sur le papier, un rang 1** :
  `vx_kit.py:292` écrit `al.fired=true; al.active=false; al.firedPrice=f.price`.
  **Et c'est faux** — recherche de l'**URL littérale** dans les 42 objets servis :
  `/api/alerts/status` **AUCUN OBJET SERVI**, `firedPrice` **aucun**, `al.fired`
  **aucun** ; seules `/api/alerts/active` et `/api/positions/alerts` sont citées.
  `vx_kit.py` est le module qui **n'atteint aucune des 8 pages**. **NON GARDÉ,
  mais la conséquence n'atteint aucun écran — règle 442/445, non classé.**
  **Le faux arrêté à une inférence de la publication** : j'avais la chaîne
  complète et la ligne du client ; **il ne manquait que la vérification de l'URL
  servie**. La règle 454/455 a payé, **contre moi**. Faux arrêtés : **33 → 34**.
  **Portée** : classement **par lecture**, pas par cycle réel ; huit mécanismes
  seulement — un neuvième échapperait (**non quantifié**, mais la marge se
  réduit) ; **aucun fichier runtime ouvert** ; **aucun navigateur**.
  **Fait de méthode, le plus inconfortable de la tranche, et il porte sur MOI :
  le détecteur était juste du premier coup, c'est le RAISONNEMENT qui allait
  publier. Une chaîne causale complète DANS LE CODE n'est pas une chaîne causale
  DANS LE PRODUIT tant qu'on n'a pas prouvé que le consommateur est SERVI.**
  **Septième bornage consécutif.**
  **Aucun code, aucun gardien, aucun test ; aucun GO demandé, rien d'engagé.**
  Anti-doublon `total 100 · actifs 0` ; aucun fichier touché ; MD5 **8/8** ;
  snapshot runtime 21 fichiers, écart final **aucun** ; suite **2864 passed /
  0 skipped**. Comptes : arrêtés **34**, publiés puis corrigés **3**,
  interprétations retirées **1**.
- **Lot 464 — livré** : **le ledger qui produit le track record affiché ne peut
  pas distinguer un verdict de DÉMO d'un verdict réel — trois écrivains
  append-only sur quatre ont perdu la provenance, et le quatrième la garde.**
  44ᵉ lot, quatrième de la tranche. Le 463 a nommé « une promesse de provenance
  que le journal perpétue » ; ce lot attaque **les écrivains de fichiers runtime
  et leur garde de provenance**.
  **Calibrage, DEUX critères posés avant la première mesure** : **(1)** seul ce
  qui est **dérivé d'une donnée de marché** entre dans la population (utilisateur
  / config / méta : exclus, nommés) ; **(2)** trouvé en lisant la liste —
  **ÉCRASER N'EST PAS ACCUMULER** : un cache réécrit à chaque cycle **ne
  perpétue rien**, un journal accumule. **Ce critère BORNE rétroactivement le
  463.**

  ```text
  28 sites d'écriture · 21 fichiers runtime distincts
     14 ÉCRASENT (caches)          un mensonge de démo n'y survit pas
      3 SANS OBJET                 desk_data ×2 · track_meta
      7 ACCUMULENT du marché       ← la population
  ```

  **Correction d'instrument, quatrième de la série et d'une forme neuve** : le
  détecteur AST cherchait `save_json` et **a manqué `track_record.record()`, qui
  écrit par un `open(…, 'a')` brut** — piège du détecteur à une seule forme
  **transposé aux écritures**. Révélé par la **lecture**, pas par la taille.
  Faux arrêtés : **32 → 33**.
  **Les sept accumulateurs** : `breadth_history` (**connu 391/396**) ·
  `gex_history_cache` (**connu 463**) · **`skyler_memory` → `'demo'` STOCKÉ,
  GARDÉ ← témoin** · **`edge_ledger.jsonl` NON GARDÉ** · **`skyler_decisions`
  provenance PERDUE** · **`skyler_sessions` provenance IMPOSSIBLE** ·
  `alerts_fired` (pressenti au 462, nommé non tranché).
  **Le témoin positif** : `decision_memory.freeze()` stocke `'demo'` comme champ
  **lisible** et le fait entrer dans le hachage de `decision_id` — deux décisions
  identiques, l'une démo l'autre réelle, **coexistent séparément**. **Sur le même
  chemin de code, dans les mêmes `try`, quatre écritures append-only : une seule
  retient la provenance que la route a calculée.**
  **La trouvaille** : `analysis_api.py:102` lit `DEMO_MODE` et le passe aux
  moteurs — **la décision SAIT qu'elle est de démo** — puis
  `skyler_journal.record()` écrit 8 champs et **mesuré, `'demo' in entrée` →
  False : le drapeau est reçu puis JETÉ** ; `session_log.record_close(log, sym,
  date, close)` **n'a aucun paramètre de provenance** ; et
  `track_record.record(state)` écrit en **append-only** 12 champs **sans aucune
  provenance**. **Banc** (persist redirigé, `cache_path` vérifié) : 2 lignes
  écrites, aucun champ de provenance, `evaluate()` lit le ledger et **ne filtre
  pas**. **L'appelant ne garde pas** : `terminal.py:1430`, toutes les 6 h, **sans
  condition sur `DEMO_MODE`** — alors que le fichier le teste **seize** fois
  ailleurs.
  **Ce que l'écran en fait** : `/journal` affiche « moyenne réelle des verdicts
  résolus (n≥5) — **mesure, pas une promesse** », calculée sur ce ledger.
  **RANG 1, et je dis sur quel critère : le CONSOMMATEUR.** Une frise GEX fausse
  désinforme ; un track record contaminé **change ce que l'utilisateur croit que
  le moteur vaut**. Trois aggravations : **append-only** (aucune purge),
  **indétectable** (aucun champ), **définitive** (« Ledger immuable » affiché).
  **Précondition dite franchement** : il faut avoir tourné en DEMO — mais la
  démo est le **défaut dès que `NO_IBKR=1`**, donc à tout lancement sans TWS.
  Correction pressentie : passer `demo` à `record()`, **déjà dans la portée de
  l'appelant**, comme `decision_memory` le fait. **Aucun gardien** ; le dossier
  417 porte sur les **dénominateurs**, pas la provenance — **pas de recoupement**.
  **Portée** : banc sur état **fabriqué** — établit **l'absence de garde**, pas
  la proportion réelle ; **`edge_ledger.jsonl` n'a pas été ouvert** ; DEMO établi
  **par lecture** ; **une écriture par un chemin encore différent échapperait —
  c'est arrivé une fois dans ce lot même**, reste **non quantifié** ;
  `alerts_fired` **non tranché** ; **aucun navigateur**.
  **Premier rang 1 depuis le 457, et rendu en BORNANT : sixième bornage
  consécutif.** Fait de méthode confirmé : **c'est en LISANT la liste, pas en la
  comptant, que le défaut de l'instrument se voit** — quatrième détecteur
  consécutif faux à la première écriture.
  **Aucun code, aucun gardien, aucun test ; aucun GO demandé, rien d'engagé.**
  Anti-doublon `total 100 · actifs 0` ; aucun fichier touché ; MD5 **8/8** ;
  snapshot runtime 21 fichiers, écart final **aucun** ; suite **2864 passed /
  0 skipped**. Comptes : arrêtés **33**, publiés puis corrigés **3**,
  interprétations retirées **1**.
- **Lot 463 — livré** : **les promesses de provenance — l'historique GEX
  journalise les profils de DÉMO dans un fichier de 120 jours et les ressert sous
  la légende « points réels uniquement », la seule promesse qui SURVIT au retour
  en mode réel.** 43ᵉ lot, troisième de la tranche. Le 462 avait signalé hors
  calibrage une phrase affirmant une propriété qu'un repli dément ; ce lot prend
  la piste.
  **Calibrage posé AVANT la première mesure** : une promesse de provenance porte
  du texte visible, contient un marqueur d'une **liste fermée**, et **AFFIRME**
  au lieu de **NOMMER** — « Connexions (IBKR, …) » nomme, « points réels
  uniquement » affirme.
  **Correction d'instrument, troisième de la série 461-462-463** : première
  mesure **88 phrases**, **le contrôle passait**, et c'est la **lecture de la
  liste** qui a trahi l'instrument (`live` appariait `live-updates.js` et
  `connected-live` ; `ibkr` appariait `vx-conn-ibkr-badge` et
  `/api/ibkr/positions`) — **le critère « affirmer, pas nommer » était posé dans
  le calibrage mais imposé nulle part dans le code**. **88 → 31.** Faux arrêtés :
  **31 → 32**. **Leçon : la taille détecte le bavardage GROSSIER ; le bavardage
  MODÉRÉ ne se voit qu'en lisant la liste.**
  **Ce que la famille contient — elle re-surface surtout du connu** : 31
  promesses, **22 tranchées**, **9 nommées non tracées** (exclues de tout total).

  ```text
  branches d'ABSENCE (« rien d’inventé »)      11   promesse TENUE
  CONDITIONNELLES (`demo ? … : …`)              5   honnêtes par construction
  dossiers DÉJÀ OUVERTS                         4   425 · 363 · 407 · 386/431
  vérifiée au 462 (« moyenne réelle … n≥5 »)    1   concorde
  NOUVELLE TROUVAILLE                           1
  ```

  **Le bornage demandé est rendu : la famille ne creuse pas de terrain neuf.**
  **La trouvaille** — `gex_history.py` promet dans sa docstring « QUE des profils
  **réels** **non vides** » ; **la garde n'en couvre qu'UNE**. Mesuré :
  `record(profile)`, **aucun paramètre de provenance** ; seule garde = non vide.
  **Banc** (persist redirigé vers un tempdir) : `record()` sur un profil
  synthétique → **True**, fichier écrit, `series()` le relit et le sert.
  L'appelant ne garde pas non plus — son commentaire dit « réel seulement » et la
  **même fonction** sert `'demo': bool(DEMO_MODE)` dans la même réponse.
  **Et la légende est inconditionnelle** : `options-gex.js:32` écrit
  `d.demo ? '…DÉMO…' : ''` — **la page SAIT** — et **75 lignes plus bas**,
  `:107`, elle affirme « points réels uniquement » sans consulter ce drapeau.
  Famille 433/457 portée à son degré le plus net : l'information honnête est
  **déjà utilisée soixante-quinze lignes plus haut**.
  **Ce qui en fait un défaut DISTINCT et non le 391/396 redit** : en DEMO tout
  l'affichage du scan est synthétique — **compter chaque phrase « réelle » comme
  un défaut séparé gonflerait le résultat de quinze cas imaginaires, je ne le
  fais pas**. Ce qui distingue celui-ci : **il PERSISTE**. Le point écrit en démo
  au jour D−30 reste **120 jours** ; au jour D en réel, `d.demo` vaut `false`,
  **l'étiquette DÉMO disparaît**, et la frise mêle démo et réel sous « points
  réels uniquement », **sans aucun signal**. **Second site du genre 391/396**
  (qui porte, lui, sur `breadth_history.json`). **Rang 2** — il faut avoir tourné
  en DEMO, et cela n'inverse pas une décision d'entrée comme au 457.
  **Le gardien existe et couvre l'AUTRE promesse** : `test_gex_history.py`
  verrouille « non vides » ; **rien ne verrouille « réels »**. Une garde sur la
  bonne fonction, **sur la mauvaise propriété**.
  **Portée** : 9 promesses non tracées ; liste de tournures **fermée**
  (**non quantifié**) ; le banc établit **l'absence de garde**, pas la fréquence
  réelle ; **`gex_history_cache.json` n'a PAS été ouvert** ; atteignabilité du
  mode DEMO **par lecture** ; **aucun navigateur**.
  **Fait de méthode** : troisième détecteur consécutif faux à la première
  écriture — **la seule parade efficace trois fois sur trois est de LIRE la liste
  avant de la compter**. **Un mensonge affiché se corrige en rafraîchissant ; un
  mensonge JOURNALISÉ se corrige en purgeant un fichier.**
  **Genre neuf : UNE PROMESSE DE PROVENANCE QUE LE JOURNAL PERPÉTUE.**
  **Cinquième bornage consécutif.**
  **Aucun code, aucun gardien, aucun test ; aucun GO demandé, rien d'engagé.**
  Anti-doublon `total 100 · actifs 0` ; aucun fichier touché ; MD5 **8/8** ;
  snapshot runtime 21 fichiers, écart final **aucun** ; suite **2864 passed /
  0 skipped**. Comptes : arrêtés **32**, publiés puis corrigés **3**,
  interprétations retirées **1**.
- **Lot 462 — livré** : **les phrases-seuil servies — 26 sur 28 citent EXACTEMENT
  le seuil que le code applique, le défaut du 461 est un accident isolé, et la
  seule autre divergence porte sur une branche INATTEIGNABLE.** 42ᵉ lot, deuxième
  de la tranche. Le 461 a nommé le genre « un classeur qui cite un seuil et en
  applique un autre » ; ce lot attaque **la classe entière** : les phrases
  servies qui citent un nombre à côté d'un prédicat.
  **Calibrage posé AVANT la première mesure** : une phrase-seuil est destinée à
  l'affichage, contient un nombre, **et porte elle-même un mot de comparaison**
  (`plafond`, `repère`, `seuil`, `au-delà`, `≥`, `≤`, chevron + chiffre…).
  **Le critère du mot de comparaison est le cœur du calibrage** — sans lui,
  contamination par homonymes (leçon des 28 valeurs exclues du 458).
  **DEUX corrections d'instrument, et le contrôle du 461 PASSAIT dans les deux
  versions fausses** :

  ```text
  1  la regex `'…'` appariait le guillemet FERMANT d'un littéral avec
     l'OUVRANT du suivant → elle capturait le CODE entre les deux
     (`,opp.actionable>0?`)  — même famille que le 453
  2  `<` et `>` NUS dans la liste des mots de comparaison → tout le
     BALISAGE HTML entrait dans la population
                              186 phrases  →  30   (facteur SIX)
  ```

  **Un contrôle qui passe ne prouve pas que l'instrument est juste ; il prouve
  seulement qu'il n'est pas aveugle.** Faux arrêtés : **29 → 31**.
  **Population** : 42 objets servis, 841 916 caractères → **30 phrases-seuil**
  (279 E1 habillage, 319 E2 descriptif, 1 E3 interpolé) ; **2 écartées à la
  lecture** (en-têtes de tableau) → **28 tranchées**.
  **Résultat : 26 CONCORDENT** — « 3 clôtures datées » ← `length < 3` ·
  « minimum 5 par verdict » et « n≥5 » ← `n >= 5` · « <-20 » et « >+50 » ←
  bornes de bucket · « breadth > 55 % » ← 55 appliqué deux fois sur la page ·
  « max 5 catégories » ← `slice(0,5)` · les **5 paliers** « Gain ≥ +N % » de
  `winnerRule` **et** les **5** d'`optNextAction` · « ≤ 7 j » ← `<= 7` (deux
  sites) · « max 3, dont 1 PUT » ← Constitution 3 et 1 · « plafond 15 % par
  titre » ← `> 15` · « /40 » ← 8 blocs sommant 40 · « zone ≤ 5 j » ←
  `xOf(min(5, horizon))` · « >12 % du notionnel » ← `> 0.12` ·
  « P(valeur terminale ≥ 2× coût) » ← `S_T ≥ K + 2×prime`, **la même condition
  sous une autre forme** · « toutes les 60 s » ← `time.sleep(60)`.
  **1 DIVERGE** : « ~15 % pour un titre » ← `> 25`, le cas du 461.
  **1 BORNÉE** : `analysis_page.py:788` — « cible 1 » peut afficher `tp2`, et si
  `tp1` et `tp3` manquaient ensemble les cartes « Probable » et « Exceptionnel »
  montreraient le **même** chiffre ; **mais la branche est INATTEIGNABLE** :
  `analysis.py:261`, unique producteur de `dec.targets`, écrit les trois cibles
  **dans la même expression**. **Règle 442/445 — je ne la classe pas.**
  **Le défaut du 461 n'est pas la pointe d'un massif : c'est un accident isolé.
  Quatrième bornage consécutif — 453 sur 452, 458 sur 457, 461 sur 458, 462 sur
  461.**
  **Deux observations nommées, non classées** : le libellé `>+50` couvre
  `[50, 1e9]` (un trade à +50 % pile y est compté — cosmétique) ; et, **hors
  calibrage**, la bulle qui porte le « 60 s » exact affirme aussi « sur données
  réelles » alors que `_alert_price` retombe sur le détail du scan, synthétique
  en DEMO — genre du dossier ouvert 391/396, **nommé, non compté**.
  **Portée** : liste de mots de comparaison **fermée** (une phrase sans mot de
  comparaison échapperait — **non quantifié**) ; les **319 E2 n'ont pas été
  relues une par une**, elles sont écartées **par construction** ; concordances
  établies **par lecture**, **aucun banc monté** ; **aucun navigateur**.
  **Fait de méthode — corollaire de la règle du 461 : le contrôle par un cas
  connu détecte la CÉCITÉ de l'instrument, jamais son BAVARDAGE ; pour le
  bavardage, le signal est la TAILLE de la population.**
  **Lot à résultat NÉGATIF, et c'est son utilité : le défaut d'hier tient, mais
  il ne se généralise pas — le dire borne le dossier au lieu de l'enfler.**
  **Aucun code, aucun gardien, aucun test ; aucun GO demandé, rien d'engagé.**
  Anti-doublon `total 100 · actifs 0` ; aucun fichier touché ; MD5 **8/8** ;
  snapshot runtime 21 fichiers, écart final **aucun** ; suite **2864 passed /
  0 skipped**. Comptes : arrêtés **31**, publiés puis corrigés **3**,
  interprétations retirées **1**.
- **Lot 461 — livré** : **la carte « Risque dominant » de `/portfolio` déclare
  « Aucun risque critique détecté » entre 15 % et 25 % de concentration — alors
  qu'elle cite elle-même le repère de 15 % et que deux cartes voisines sont déjà
  en alerte.** 41ᵉ lot, premier de la tranche 460-469. Le bilan n°15 recommandait
  **(a)** : désigner la famille suivante par la forme du dernier défaut. Le
  458/459 avait nommé une **taxonomie amputée et aveugle à une dimension** → ce
  lot attaque **la classe entière des CLASSEURS SERVIS**.
  **Calibrage posé AVANT la première mesure** : un classeur servi rend **≥ 2
  étiquettes textuelles** à partir d'**≥ 1 comparaison numérique** ; **quatre
  formes** reconnues ; exclus et nommés — couleur/classe CSS, nombre, table de
  correspondance, classeur sur chaîne.
  **TROIS corrections d'instrument, toutes révélées par le même contrôle —
  exiger que le détecteur retrouve le cas CONNU du 458 (`catOf`)** :

  ```text
  1  `return\s+` exigeait un ESPACE ; les octets servis écrivent
     `return'BALANCED'`            → le cas du 458 INTROUVABLE : ZÉRO FAUX
  2  les `return` des fonctions IMBRIQUÉES attribués à la PARENTE (piège 453)
  3  plafond de 44 puis 60 caractères par étiquette → `winnerRule` (~78 c.)
     SILENCIEUSEMENT absent de la population
  ```

  **Le n°3 répète la leçon du 459 : une BORNE D'INSTRUMENT décidait de la
  population mesurée.** Trois faux arrêtés : **26 → 29**.
  **Population** : 42 objets servis, 841 916 caractères → **28 candidats**,
  **13 retenus**, **15 exclus nommés**.
  **Verdict, et il BORNE le 458** : **9 classeurs sains sur 13** — `bucketOf`,
  `tierOf` ×2, `roleOf`, `thesisState`, `nextAction`, `liqState`,
  `computeVerdict`, `optNextAction` ; **2 aveugles au type** (`catOf` et
  **`catOf2`**) ; **1 rang 3** (`winnerRule`) ; **1 rang 2** (`dominantRisk`).
  **L'aveuglement du 458 touche DEUX SITES — le même prédicat dupliqué — pas une
  pratique générale.** Fait neuf : **`catOf2`**, copie conforme dans
  `window.__opCompare`, **que le 458 n'avait pas signalée**.
  **La trouvaille** — `portfolio_page.py:216-226`, rendu en **KPI de tête**
  (`:324-326`) : le prédicat se déclenche à **25** et le repère que **sa propre
  phrase invoque est 15** ; la Constitution chargée pose
  `max_stock_weight_pct = 15.0`. Reproduction des trois prédicats servis
  (règle 443) :

  ```text
  poids Top 1 | KPI Concentration | carte Discipline V2 | carte RISQUE DOMINANT
      14,9 %  | POSITIVE          | sous le plafond     | Aucun risque critique
      15,0 %  | WARNING           | sous le plafond     | Aucun risque  ← CONTRA.
      20,0 %  | WARNING           | > plafond 15 % rouge| Aucun risque  ← CONTRA.
      25,0 %  | WARNING           | > plafond 15 % rouge| Aucun risque  ← CONTRA.
      25,1 %  | NEGATIVE (halo)   | > plafond 15 % rouge| Concentration élevée
  ```

  **Fenêtre exacte au pas de 0,1 point : 15,0 % → 25,0 %**, les deux cas sains
  encadrant juste. **Ce qui rend le résultat serré : le KPI (`:349`) et la carte
  (`:222`) lisent LA MÊME expression `m.top1.w`** — aucune question de
  dénominateur. La carte « Discipline V2 » (`:964-969`, `> 15` → rouge)
  **corrobore sans prouver** : grandeur **serveur** distincte, leçon 458.
  **Rang 2, et je dis pourquoi pas rang 1** : c'est un KPI de tête qui énonce une
  absence de risque fausse, mais **l'utilisateur n'est pas sans signal** (KPI
  voisin jaune, carte Discipline rouge) — **fausse quiétude**, pas consigne
  d'action fausse comme au 457. Correction pressentie : lire
  `max_stock_weight_pct`, **déjà calculé** (`portfolio_context.py:64`).
  **Aucun gardien** : `dominantRisk` dans aucun test ; le plafond est vérifié
  côté profil et côté moteur (**qui avertit dès 15 %**), jamais contre le
  littéral de la page — motif 381/385/414/415/457.
  **Rang 3** : `/portfolio` délègue à **`winnerRule(t.pl)` qui ne reçoit qu'un
  NOMBRE**, le type étant perdu à l'appel, alors que `/options` a un frère
  conscient du type ; à +60 % la page dit « **relever le stop sous le prix** »
  pour une **option**. **Les cinq paliers sont identiques : rien n'est faux.**
  **Portée** : prédicats **reproduits, pas exécutés** ; la branche concentration
  est la **deuxième** (les invalidations passent avant) ; la contradiction
  prouvée est **intra-page** ; les 13 valent **pour les quatre formes**, un
  classeur bâti par helper échapperait (**non quantifié**) ; `roleOf` porte une
  **liste de 6 tickers défensifs en dur sans source de configuration** — nommé,
  **non classé** ; **aucun navigateur**.
  **Fait de méthode, et il devient une règle : une BORNE D'INSTRUMENT décide de
  la POPULATION mesurée — un détecteur qui ne retrouve pas le défaut d'hier ne
  mesure rien aujourd'hui.** Genre neuf : **UN CLASSEUR QUI CITE UN SEUIL ET EN
  APPLIQUE UN AUTRE**. Chaîne de relais : **cinquième fois**, réserve du bilan
  n°15 rappelée (la famille a été **proposée**, pas trouvée seule).
  **Aucun code, aucun gardien, aucun test ; aucun GO demandé, rien d'engagé.**
  Anti-doublon `total 100 · actifs 0` ; aucun fichier touché ; MD5 **8/8** ;
  snapshot runtime 21 fichiers, écart final **aucun** ; suite **2864 passed /
  0 skipped**. Comptes : arrêtés **29**, publiés puis corrigés **3**,
  interprétations retirées **1**.
- **Lot 460 — livré** : **BILAN n°15 (tranche 450 → 459) — sept défauts affichés
  au lieu de cinq, mais le rang 1 reste au plancher, et la « chaîne de relais »
  qui a porté la tranche n'est pas de moi.** Quinzième bilan, fait **sur
  pièces** : dix rapports relus, chiffres vérifiés dans le dépôt, **aucune
  trouvaille rejouée**, aucun serveur DEMO, aucun moteur rouvert ; **une seule
  mesure fraîche, les MD5**. **Base résolue avant tout chiffre** : `3fc9045`
  (lot 449) → `1b23377` (lot 459), **10 commits** ; **12 fichiers**, 11 dans
  `docs/refactor/validation`, 1 dans `docs/skyler`, **0 hors `docs/`**,
  **+2 893 / −0**, **0 fichier de production** ; rapports/index/STATUS
  **10/10** ; **104 212 octets** ; MD5 **8/8** ; SW `td-shell-v187`.
  **Correction de référence publiée : le SHA du lot 399 était faux** —
  **`29f4435` n'est PAS un ancêtre de la tête**, c'est le commit côté branche,
  remplacé par le squash **`20a917f`** ; depuis `20a917f` : 60 commits, 63
  fichiers, **1 hors `docs/`** (`tests/test_skyler_sweep_x1.py`, lot 401),
  **0 production**. Le chiffre publié ne change pas, **la référence était
  fausse**. **Bilan des dix lots** : **2 rang 1 · 5 rang 2 · 4 rang 3 · 5 rang 4
  · 2 veines refermées · 3 bornages · 1 retrait d'interprétation**.
  **Rendement recompté, deux lectures** : rang 1 par lot 4 → 4 → 3 → **2** ; par
  dossier distinct 4 → 3 → 2 → **2** — **le rang 1 reste au plancher**. Mais les
  **défauts affichés** (rang 1 + rang 2, dossiers distincts) passent de **5 → 5
  → 7**. **Fait nouveau : une chaîne de relais** — 455 → 456 → 457 → 458 → 459
  se sont passé le relais **par la FORME du défaut**, quatre passages, quatre
  lots qui paient ; règle de **SUCCESSION**, distincte du 416 (arrêt) et du
  425/446 (sélection). **Réserve sérieuse : les quatre relais ont été proposés
  dans les orientations de réveil, pas découverts par la boucle** — la règle
  fonctionne quand on l'applique, ce n'est pas la preuve que la boucle sait la
  trouver seule. **Comptes d'erreurs** : arrêtés avant publication **25 → 26**
  (le +1 du 459 : la première grille aurait publié « inatteignable » et
  **enterré un défaut réel** — instrument non bogué mais **trop étroit**) ;
  publiés puis corrigés **3, inchangé** ; **troisième compte ouvert :
  interprétations retirées = 1** (le 459 retirant l'insinuation du 458 sur
  « AUTRE »). **Classement coût/risque à 16 dossiers**, le **n°1 étant le rang 1
  le moins cher jamais classé** (lire `d.bounds.max`, déjà reçu par la page) et
  **les neuf premiers ne touchant aucun moteur**. **Orientation 461 : (a)
  continuer les lots de mesure** — le critère posé (« (b) si la cadence baisse »)
  n'est pas rempli, les défauts affichés montent de 5 à 7 — **mais la bascule est
  posée à voix haute : au premier bilan où ils reculeront, (b), le lot devis,
  devient la bonne réponse**. **Aucun code, aucun gardien, aucun test ; aucun
  GO demandé, rien d'engagé.** Anti-doublon `total 100 · actifs 0` ; aucun
  fichier de production touché ; MD5 8/8 ; snapshot runtime 21 fichiers, écart
  final **aucun** ; suite **2864 passed / 0 skipped**.
- **Lot 459 — livré** : **les deux dettes de la tranche soldées PAR EXÉCUTION —
  le plafond du radar GEX monte au rang 2, la branche « AUTRE » est bel et bien
  atteignable, et ma borne d'atteignabilité a bougé trois fois avant que je la
  publie.** 40ᵉ lot, **dernier lot de mesure de la tranche**. Un dernier lot
  solde au lieu d'ouvrir (modèle 449) ; les deux dettes « établies par lecture »
  sont soldées **par exécution**, et elles vont **en sens opposés**.
  **Dette (i) — `gex_scan` du 456.** Cause des deux échecs, trouvée en lisant le
  moteur : **la clé du board est `sym`** (j'écrivais `symbol`) **et l'open
  interest se lit `oi`** (j'écrivais `open_interest`).

  ```text
  board |  sans cap   |  AVEC top=30 (valeur de la route)
     29 |  29/29      |  29/29     concordent
     30 |  30/30      |  30/30     concordent
     31 |  31/31      |  30/31   ← le plafond mord EXACTEMENT à 31
    120 | 120/120     |  30/120
  ```

  **Atteignable, et c'est le cas nominal** : `_publish_board()`
  (`terminal.py:1033-1044`) publie **FOCUS ∪ ROTATION** et annonce couvrir
  « tout l'univers optionable (~700 titres US) ». **Requalification : rang 4 par
  lecture → RANG 2 par exécution.**
  **Dette (ii) — la branche « AUTRE » du 458.** Le seul sélecteur du board est
  `best_for_symbol` (focus `:1073` et rotation `:1586`), filtrant par
  **moneyness** ; delta par `legacy_engine._greeks`. **Trois grilles, trois
  réponses, et je publie les trois** :

  ```text
  A. iv ≥ 0.20                        delta max 0,684   « inatteignable »
  B. iv ≥ 0.15, pas 0.004             delta max 0,715   atteignable, marginal
  C. iv ≥ 0.10, pas 0.001, 2 000 pts  delta max 0,781   ATTEIGNABLE (40,3 % de
                                                        la bande LEAPS)
  ```

  **La grille A m'aurait fait publier « inatteignable » — c'était faux.**
  **Leçon neuve : une borne d'atteignabilité mesurée sur une grille est une
  propriété de la GRILLE tant qu'on n'a pas borné les entrées réelles.**
  **Ce que « AUTRE » recouvre vraiment** (étiquetage de tout l'espace atteignable,
  reproduction du prédicat) :

  ```text
  CALL  |delta| 0,005–0,715   BALANCED 49,8 % · AUTRE 24,8 % · DYNAMIC 16,8 %
                              · ULTRA_CONVEX 8,6 %
  PUT   |delta| 0,000–0,569   DYNAMIC 34,2 % · ULTRA_CONVEX 28,6 % · AUTRE 26,7 %
                              · BALANCED 10,5 %
  ```

  **Deux conclusions qui RESSERRENT le 458** : **(1) « AUTRE » est largement
  HONNÊTE** — il couvre surtout des deltas que **la Constitution ne catégorise
  pas** (rien sous 0,18, **aucune catégorie entre 0,60 et 0,70**) ; **je retire
  l'insinuation que « AUTRE » serait en soi un défaut** ; **(2) ce qui tient
  entièrement, c'est l'aveuglement au TYPE** — **73,3 % de l'espace de put
  atteignable reçoit un badge de catégorie HAUSSIÈRE**, alors que `c.type` est
  dans le même objet. **Le rang 2 du 458 est confirmé sur UN front, pas deux, et
  désormais chiffré.** **Les deux dettes de la tranche sont CLOSES** : le bilan
  n°15 héritera de comptes nets, plus aucun « établi par lecture » en suspens.
  **Portée** : `catOf` **reproduit, pas exécuté** ; les pourcentages décrivent
  **l'espace que le sélecteur peut produire**, pas la fréquence réelle ; **la
  distribution d'IV n'est pas bornée**, donc **0,781 est le chiffre d'une grille,
  pas une borne du produit** ; le banc `gex_scan` fabrique un board synthétique ;
  **aucun navigateur**. **Le fait de méthode le plus utile de la tranche, et il
  est inconfortable** : la première grille m'aurait fait **enterrer un défaut
  réel** ; la parade est de **faire varier la grille jusqu'à ce que la réponse
  cesse de bouger** — ce qu'elle n'a pas encore fait ici, et je l'écris.
  Aucun fichier touché · SW `td-shell-v187` · **MD5 8/8 identiques** · écart
  runtime **aucun** · suite **2864 passed / 0 skipped** · rapport
  `docs/refactor/validation/SKYLER-LOT-459.md`.

- **Lot 458 — livré** : **les littéraux de l'interface contre la Constitution —
  l'échelle de conviction est copiée à la valeur près, mais le classeur de
  catégories d'options est aveugle au type et ne connaît que 3 des 5
  catégories.** 39ᵉ lot, 8ᵉ de la tranche. Règle 455 → 456 appliquée : **la
  famille suivante est désignée par la FORME du défaut du lot précédent**.
  **Calibrage posé AVANT la première mesure** — c'est lui qui rend le lot
  publiable :

  ```text
  valeurs numériques du profil V2                    126 · 49 distinctes
     à chemin UNIQUE, retenues                        21
     à chemins MULTIPLES, EXCLUES et nommées          28   (aucun total ne les inclut)
  présentes dans les octets servis                    19  ·  absentes 2
  coïncidences écartées après lecture du contexte      8   (7, 120, 150, 200, 240,
                                                            365, 500, -20, 31)
  valeurs DÉCIDABLES                                  11
  ```

  **Témoin positif n°1 — l'échelle de conviction est exacte**
  (`portfolio_page.py:185-189`) : seuils **36 / 32 / 28** = `score_min` du profil,
  plafonds **15 / 10 / 5 / 2** = `allocation_pct[1]` de S_PLUS / S / A / B —
  **8 valeurs sur 8 concordantes, sur la page même où le 457 a trouvé une borne
  périmée**. **Témoin n°2** : `0.40/0.60`, `0.28/0.45`, `0.18/0.30` sont
  **exactement** les bornes de BALANCED, DYNAMIC et ULTRA_CONVEX.
  **La trouvaille** — `opportunities_page.py:475-477`, rendu dans la colonne
  « Catégorie » du tableau options (`:489`) :

  ```text
  catégorie du profil   delta          étiquette rendue
  BALANCED              0.40–0.60      BALANCED                   CONCORDE
  DYNAMIC               0.28–0.45      BALANCED / DYNAMIC         DIVERGE
  ULTRA_CONVEX          0.18–0.30      DYNAMIC / ULTRA_CONVEX     DIVERGE
  LEAPS                 0.70–0.90      « AUTRE »                  DIVERGE
  BEARISH_TACTICAL      0.30–0.55      BALANCED / DYNAMIC         DIVERGE
  ```

  **Trois faits mesurés** : **(1)** les catégories du profil **se chevauchent**,
  donc un classeur fondé sur le **seul delta ne peut pas** reproduire la
  taxonomie — **grandeur insuffisante**, pas bug d'implémentation ; **(2)** le
  prédicat **ignore le type** alors que `c.type` **est dans le même objet**
  (`legacy_engine.py:291`) — `put −0.45 → « BALANCED »`, `call +0.45 →
  « BALANCED »`, `put −0.25 → « ULTRA_CONVEX »`, quand la Constitution pose
  `primary_direction: LONG_CALL`, `target_call_share_pct: 90` et une catégorie
  **BEARISH_TACTICAL** distincte (`RARE`, max 1) ; **(3)** le board **contient
  des puts** (`build_board()` → `sells` en AVOID → `best_for_symbol(..., 'put')`),
  la branche est donc **atteignable**. **Rang 2** : étiquette fausse **affichée**
  dans une colonne, alors que l'information qui la corrigerait est dans le même
  objet ; rien n'est inventé — c'est une **taxonomie amputée et aveugle à la
  direction**. **Aucun GO. Aucun gardien.** **Non établi** : qu'un delta ≥ 0.70
  atteigne ce board — `best_for_symbol` filtre par **moneyness** (calls
  0,98×–1,18× spot) et **exclut le deep-ITM**, donc « AUTRE » pourrait être rare
  ou inatteignable pour les calls ; **je ne le tranche pas** (442/445).
  **La réponse à la question du réveil — le 457 n'était pas isolé en GENRE, mais
  il l'est en GRAVITÉ** : **14 valeurs concordantes contre 1 divergente** (plus
  une taxonomie incomplète non chiffrée). **L'interface recopie la Constitution
  correctement dans 14 cas mesurés sur 15** — le rang 1 du 457 est un **relief
  isolé, pas la pointe d'un massif** ; ce lot **borne** le dossier au lieu de
  l'élargir. **Portée** : classeur **reproduit, pas exécuté** ; atteignabilité du
  put établie **par lecture** ; **aucun navigateur**. Aucun fichier touché · SW
  `td-shell-v187` · **MD5 8/8 identiques** · écart runtime **aucun** · suite
  **2864 passed / 0 skipped** · rapport
  `docs/refactor/validation/SKYLER-LOT-458.md`.

- **Lot 457 — livré** : **« Actions 10 / 10 — complet, remplacement obligatoire » :
  le portefeuille affiche la limite de la Constitution V1 alors que le produit
  tourne sur la V2, qui en autorise 15 — et la bonne borne est affichée trois
  cartes plus bas.** 38ᵉ lot, 7ᵉ de la tranche. Le 456 avait laissé **7 fractions
  sur 12 non tracées** ; ce lot **solde la dette** (modèle 449/455).
  **Six des sept sont saines**, pour la même raison : numérateur et dénominateur
  posés **dans le même objet** ou dérivés de **la même liste** — `sm.beats/total`,
  `diag.ai.ok/total`, `b.points/b.max` (profil : 8 blocs, **somme exactement 40**),
  `p.v/p.max` (barème), `rating_mean/5` (échelle yfinance 1-5),
  `favorable/pts.length`. **Nuance nommée et NON classée** : `total` compte chaque
  trimestre publié mais `beats` exige `surp is not None` — un trimestre à surprise
  inconnue compte au dénominateur seul ; c'est la forme du 455 mais **honnête**.
  **La trouvaille — trois dénominateurs sur une carte, deux exacts, un périmé** :

  ```text
  affiché      Constitution V2 réellement chargée (vertex_strategy_v2)   verdict
  « / 3 »      max_simultaneous_options            = 3                   EXACT
  « 1 max »    max_simultaneous_bearish_positions  = 1                   EXACT
  « / 10 »     portfolio_target_positions {min 8, max 15}                FAUX — c'est 15
  ```

  **D'où vient le 10** : `test_constitution_v2.py:24` → `load_profile(version=1)`
  donne **10** ; `:69` → `load_profile()` donne **15**. **C'est la borne de la V1,
  restée figée dans l'interface quand les moteurs sont passés en V2.**
  **Banc — les deux cartes se contredisent sur la même page** :

  ```text
   n | moteur in_bounds · libres | carte « Lignes »      | KPI « Actions »
   7 | False ·  8                | sous la cible         | places disponibles     d'accord
   9 | True  ·  6                | dans les bornes       | places disponibles     d'accord
  10 | True  ·  5                | dans les bornes       | COMPLET                CONTRADICTION
  12 | True  ·  3                | dans les bornes       | COMPLET                CONTRADICTION
  15 | True  ·  0                | dans les bornes       | COMPLET                CONTRADICTION
  16 | False ·  0                | au-dessus de la cible | COMPLET                d'accord
  ```

  **Les deux cas sains tombent juste** — la contradiction n'occupe que la fenêtre
  **10-15**, exactement l'écart entre les deux Constitutions. **Et la bonne borne
  est déjà à l'écran** : `portfolio_page.py:966` rend `${b.min}-${b.max} lignes
  cibles` avec `b = d.bounds` = **{min 8, max 15}** — la page affiche « 8-15
  lignes cibles » **trois cartes sous** un KPI qui déclare le book complet à 10.
  **Famille 433 aggravée : l'information honnête n'est pas seulement déjà
  calculée, elle est déjà AFFICHÉE.** **Rang 1** — ce n'est pas une étiquette
  approximative mais une **consigne d'action fausse** : à 10 lignes le terminal
  dit *pour acheter, vends d'abord*, alors que la stratégie autorise cinq lignes
  de plus. Correction pressentie : lire `d.bounds.max`, **déjà reçu par la page**.
  **Aucun GO.** **Le gardien est vert** — `test_constitution_v2.py:69` vérifie 15
  **côté profil** ; **aucun test ne compare le littéral de la page au profil**
  (périmètre qui s'arrête avant l'interface, motif 381/385/414/415). **Réserve** :
  le KPI compte les seules lignes `STK` quand le moteur compte tous les symboles
  ouverts — cela ne sauve pas le dénominateur, 10 n'étant la borne d'aucune des
  deux lectures sous la V2. **État de la veine : 12 / 12 tranchées, VEINE DES
  FRACTIONS AFFICHÉES REFERMÉE** — 1 rang 1, 1 rang 2, 1 rang 3, 1 rang 4 par
  lecture, **8 fractions saines**. **Portée** : la dette `gex_scan` du 456 **reste
  ouverte** (rang 4 par lecture) ; le banc établit le comportement du **code**,
  pas la taille réelle du book ; les limites options sont vérifiées **par lecture
  du profil chargé** ; **aucun navigateur**. Aucun fichier touché · SW
  `td-shell-v187` · **MD5 8/8 identiques** · écart runtime **aucun** · suite
  **2864 passed / 0 skipped** · rapport
  `docs/refactor/validation/SKYLER-LOT-457.md`.

- **Lot 456 — livré** : **les fractions affichées — la carte « Qualité des
  données » de `/system` plafonne son dénominateur à 200 pour un univers de 517,
  et son camembert ne peut afficher qu'une seule part à 100 %.** 37ᵉ lot, 6ᵉ de
  la tranche. La veine des phrases composées étant close, le 455 avait désigné la
  famille suivante — **un compte affiché dont les numérateurs ne couvrent pas tout
  le dénominateur** ; ce lot attaque la classe entière.
  **Instrument, partir de l'écran par construction** : balayage des **42 objets
  servis** (841 916 caractères) à la recherche des gabarits qui **affichent** une
  fraction. **12 relevés · 5 tracés (2 plafonnés, 3 sains) · 7 nommés et NON
  tracés**, donc comptés dans aucun total (règle 448) : `sm.beats/sm.total`,
  `diag.ai.ok/total`, `b.points/b.max`, `p.v/p.max`, `rating_mean/5` (**barèmes**),
  `favorable/pts.length`, `CALLS/1 max`.
  **Témoin positif — trois fractions saines** : `environment.py:122-123` et
  `risk_map.py:137-138` (`known = [x for x in L if x['known']]` → **même liste**)
  et `markets_page.py` (« X titre(s) sur `rows.length` », **même tableau**).
  **La trouvaille** — `strategy_os_api.py:165-168` construit les paquets sur
  `list(detail)[:200]` et `diagnostics.py:44` rend `'total': len(packets)` :

  ```text
  detail   5 → total   5      detail 150 → total 150     detail 200 → total 200
  detail 260 → total 200 ←    detail 517 → total 200 ←   le plafond mord dès 201
  by_quality : {'RECENT': 200} · {'DEMO': 200} · {'MISSING': 200}
  len(UNIVERSE) = 517
  ```

  Route **réellement exécutée en GET**, `scan_state['detail']` peuplé en mémoire
  **puis restauré** (0 → 0 entrée, `source` `None` → `None`, aucune écriture).
  **Deux défauts distincts sur la même carte** (`system_page.py:699-701`) :
  **(i)** le titre « Qualité des données (**200** titres) » présente un **plafond
  d'échantillon comme un compte de titres** — pas un chiffre faux, un
  **échantillon présenté comme la population** (famille 417), et **le plafond
  n'est mentionné nulle part à l'écran** → **rang 2** ; **(ii)** le camembert ne
  peut afficher **qu'une seule part, toujours à 100 %**, parce que la route
  calcule **une seule** qualité au niveau du scan puis l'estampille sur chaque
  symbole — `by_quality` n'a **jamais qu'une clé**, la conclusion est **toujours**
  « Dominante : X (200 / 200) », **une répartition qui ne peut pas se répartir**
  (constant par construction, famille 442) → **rang 3**. **Ce qui atténue, et que
  je dis** : la note servie à côté est **honnête et co-visible** — « qualité au
  niveau scan (source unique) … » — elle **avoue le point (ii)** mais **ne dit
  rien du plafond de 200**, d'où (i) en rang 2 et (ii) en rang 3.
  **Seconde fraction plafonnée, établie par LECTURE et non par exécution** :
  `gex_scan.py:53-55` tronque `rows` à `top` **trois lignes avant**
  `'symbols_usable': len(rows)`, et la route passe **`top=30`**
  (`options_intel_api.py:133`) ; `options-gex.js` rend « … X/Y **titres
  exploitables** » — au-delà de 30 exploitables, **le numérateur est le plafond
  d'affichage, pas une mesure d'exploitabilité**. **Deux bancs ont échoué** (le
  premier fabriquait la clé `symbol` alors que le module lit **`sym`** ; le
  second, corrigé, rend `symbols_scanned` mais `symbols_usable = 0` car
  `gex.compute` rejette mes contrats) → **rang 4 en l'état, à requalifier si un
  banc l'exécute**. Je préfère le dire que gonfler le résultat.
  **Genre nouveau : UN PLAFOND D'ÉCHANTILLON AFFICHÉ COMME UNE POPULATION.**
  **Portée** : 7 fractions non tracées, nommées, hors total ; les fractions
  construites par un helper ou par déstructuration **échappent** (436), non
  quantifiées ; le banc établit le comportement du **code**, pas la taille réelle
  du scan en usage ; **aucun navigateur**. Aucun fichier touché · SW
  `td-shell-v187` · **MD5 8/8 identiques** · écart runtime **aucun** · suite
  **2864 passed / 0 skipped** · rapport
  `docs/refactor/validation/SKYLER-LOT-456.md`.

- **Lot 455 — livré** : **la veine des phrases composées refermée — 11 dernières
  phrases tranchées, et la toute dernière cache un défaut affiché : « 0 contrôle
  défavorable, 1 à surveiller, sur 6 » quand 5 des 6 sont INCONNUS.** 36ᵉ lot,
  5ᵉ de la tranche. Le 454 avait conclu que la veine rendait surtout du poids
  mort ; ce lot la **solde** en un balayage, avec l'instrument déjà validé
  (détecteur AST **aux quatre formes dès la 1ʳᵉ passe**, corpus des **42 objets
  servis**, payload identifié par sa **forme**).

  ```text
  impact     options_lab.py:788                  NON AFFICHÉE — /api/options-lab citée nulle part
  summary    ai/fallback.py:34                   JAMAIS PRODUITE — module non atteignable (452)
  summary    decide.py:128                       NON LUE — payload de l'`action` du 454
  summary    decision_memory.py:546              NON LUE
  summary    analysis_api.py:498, :501           NON ÉTABLIES (2) — branche MESURE non atteinte
  summary    widget_lab.py:1759                  AFFICHÉE — bandeau de /widget-lab
  question   knowledge_graph.py:355/360/366      AFFICHÉES (3) — carte de /portfolio
  narrative  pretrade.py:163                     AFFICHÉE — carte pré-trade de /analysis
     11 tranchées · 5 affichées · 4 non affichées ou jamais produites · 2 non établies
  ```

  Les deux `summary` de `analysis_api` sont **non établies, pas absentes** : la
  route `/memory/cell/<g>/<k>` rend **404** au démarrage, mais son 404 est une
  **page honnête** ; les phrases vivent sur la branche `MESURE`. **Leçon 438 : je
  les nomme et je ne les compte pas.** **Neuvième récidive du piège de nom, et
  massive** : `.impact` lu 4 fois, `.summary` 4 fois, **`.question` 6 fois dont 5
  sont le contrat de carte VXCharts**, `.narrative` 6 fois — **une seule** lecture
  correspond à la forme de `knowledge_graph`. **C'est la forme qui tranche, jamais
  le nom.** **Les trois `question` sont exactes** : deux impriment littéralement
  leur garde (lecture, pas mesure — 447), la troisième est inconditionnelle et
  **vérifiée vraie** (aucune source de chaîne de valeur n'existe dans le dépôt).
  **La trouvaille** — `pretrade.py:163` fait `n_ko = statuses.count(KO)` et
  `n_warn = statuses.count(WARN)`, puis rend « … %d défavorable(s), %d à
  surveiller, **sur %d** » : **aucun `statuses.count(UNKNOWN)` n'existe**, le
  dénominateur est le total mais les numérateurs ne couvrent que **deux statuts
  sur quatre**. Rendue sur `/analysis/<sym>` par `analysis_page.py:850`. **Banc
  sur le moteur réel, cas dégradé et cas sain côte à côte** :

  ```text
  A. état du démarrage   inconnu 5 · attention 1   badge MITIGÉ
     phrase  « 0 contrôle(s) défavorable(s), 1 à surveiller, sur 6. »
     le lecteur soustrait 6 − 0 − 1 = 5 « qui vont bien »
     ils sont en réalité 5 IMPOSSIBLES À ÉVALUER

  C. tout branché        ok 3 · attention 2 · defavorable 1
     phrase  « 1 défavorable, 2 à surveiller, sur 6. »   → les 3 sont VRAIMENT ok
  ```

  Le cas sain **tombe juste** ; le même gabarit, dans le cas A, invite à conclure
  l'inverse. Et **le cas A n'est pas un cas de bord** : `scan_state` vide au
  démarrage rend comité, régime, GEX, résultats et concentration tous `inconnu`.
  **Rang 2, et je dis pourquoi pas rang 1** : famille 432/433 (l'inconnu rangé
  avec le sain, du côté qui rassure) qui y valait rang 1 — mais ici
  l'information honnête est **co-visible**, les six contrôles étant rendus juste
  au-dessus avec leur icône et un détail qui **nomme ce qui manque**.
  **L'atténuation n'efface pas** (442) : la phrase est la **conclusion** de la
  carte. `n_ko` et `n_warn` sont **exacts** — **c'est une omission, rien de faux
  n'est affiché**. Correction pressentie : **une ligne**, ajouter le compte des
  inconnus. **Aucun GO. Aucun gardien** ne compare la phrase aux statuts.
  **État de la veine** : **tous les champs annoncés à 3 écrans ou plus sont
  tranchés** ; restent `volume` et `spread_pct` (1 phrase, 1 écran chacun) ; **72
  des 110 phrases du 444 restent fermées**. Bilan des 8 champs ouverts : **2 rang
  1, 2 rang 2, 1 famille saine, le reste en poids mort** — la veine s'éteint sur
  un rang 2 trouvé au dernier lot. **Enseignement, qui contredit à moitié le
  454** : la veine rendait du poids mort **parce que les champs étaient choisis
  par leur nombre d'écrans ANNONCÉ**, un chiffre qui **compte des homonymes** — le
  défaut était dans le champ annoncé à 4 écrans dont 5 lectures sur 6 sont des
  homonymes. **Portée** : `/api/options-lab` non appelée (conclusion sur l'URL
  littérale dans les octets servis, méthode 454) ; le banc établit le
  comportement du **code**, mais le cas A **reproduit l'état effectif du
  démarrage** ; déstructuration et crochets **échappent** (436), non quantifiés ;
  **aucun navigateur**. Aucun fichier touché · SW `td-shell-v187` ·
  **`/options/<sym>`, `/api/analyst/`, `/api/correlations/` volontairement NON
  appelées** · **MD5 8/8 identiques** · écart runtime **aucun** · suite
  **2864 passed / 0 skipped** · rapport
  `docs/refactor/validation/SKYLER-LOT-455.md`.

- **Lot 454 — livré** : **les six phrases `action` sont des ordres d'entrée
  chiffrés, calculés à chaque scan, sérialisés, envoyés au navigateur — et lus
  par personne.** 35ᵉ lot, 4ᵉ de la tranche. Trois balayages structurels
  d'affilée, le dernier refermé négativement : **la règle du 416 s'applique,
  changer de famille** — retour aux moteurs et aux phrases.
  **Étape 0, un détecteur qui a failli mentir** : première passe AST sur les
  **dictionnaires littéraux** seuls → `action` **0 phrase composée**, 19 valeurs
  littérales (`'ATTAQUER'`, `'BUY'`, `'HOLD'`, `'DATA_REPAIR_REQUIRED'`…).
  **J'allais publier un zéro faux.** Élargi à quatre formes d'écriture :

  ```text
  action   6 composées   [dict 0 · d[k]= 0 · kwarg 0 · variable 6]
     engines/decide.py:115, :119                 f-string
     engines/scorecard.py:233, :235, :237, :239  f-string
  ```

  Les six sont des **affectations de variable nues**, la seule forme ignorée par
  la première passe — **neuvième récidive du piège « un détecteur qui ne connaît
  qu'UNE forme fabrique de faux manquants »**, arrêtée avant publication.
  **Faux arrêtés : 24 → 25.** **Le sens du champ, vérifié avant tout plan
  (leçon 451)** : ce sont des **consignes d'entrée chiffrées** — « Entrée vers
  $X, stop $Y ($stop_type), objectifs $tp1 / $tp2 / $tp3. » — la famille la plus
  engageante du dépôt sur un terminal en lecture seule ; et **`action` désigne au
  moins quatre charges utiles** (recommandation, réconciliation, note d'analyste,
  connexion) : **septième récidive du piège de nom**.
  **Étape 1, l'affichage d'abord** : les deux moteurs sont **atteignables**
  (instrument 452) ; corpus **42 objets servis**. Les deux seules lectures
  `.action` servies portent sur d'**autres** payloads (`portfolio_page.py:459`
  réconciliation, `analysis_page.py:714` note d'analyste) ; **`decision.action`,
  `dec.action`, `v.action` : cités nulle part**.
  **Étape 2, où vont les six phrases** : les quatre de `scorecard.verdict()`
  entrent dans `scan_state['recommendations']` (`terminal.py:591-598`, `:614`) et
  `/scan` transporte la clé — mais « recommendations » n'apparaît **qu'une fois**
  dans les 42 objets servis, sur `/journal`, et c'est un **autre payload**
  (`analysis_api.py:295`, lu comme `r.proposal`) : **huitième récidive**. Les deux
  de `decide.decide()` entrent dans `options_pack()` (`:1595`), servi par
  `/options/<sym>` et `/api/ticker/<sym>` ; `/api/ticker/` **est** consommé — l'un
  des 40 sites sains du 453 — mais il lit `company`, `detail`, `in_universe`,
  `risk_map`, **pas `decision`**. **Témoin positif** :

  ```text
  champ de la ligne `recs`   lu dans les octets servis
     niveau    OUI   markets · analysis · portfolio · journal · system · 6 builders
     raison    OUI   accueil · markets · opportunités · portefeuille · options · journal
     alloc     OUI   portefeuille
     action    NON   (les 2 occurrences sont d'autres payloads)
     score40   NON
  ```

  L'instrument distingue **dans le même dictionnaire** les champs lus des autres.
  **Classement : rang 4** — famille 411/424/435/436/446, *calculé, sérialisé,
  envoyé, jamais affiché*. **Rien de faux n'est montré. Ce que cela ne réveille
  PAS** : la phrase de `decide.py` fond `stop_type` et `resistance` dans son
  texte, **cela ne rétablit pas** le verdict retiré au 444 — la phrase n'atteint
  aucun écran. **Trouvaille annexe, rang 3** : dans `feeds.py`, **6 routes sur 9
  ne sont citées nulle part** dans les octets servis (`/api/cockpit`,
  `/api/watchlist`, `/api/search`, `/api/weekly`, `/api/strategie`,
  `/api/comite`), tandis que `/api/market/summary`, `/api/market/context` et
  `/api/options` le sont — **témoin positif dans le même fichier** ;
  `/api/cockpit` est **maintenue vivante par deux fichiers de tests**, dont un qui
  vérifie `'/api/cockpit' in rules` : **un gardien qui impose une route qu'aucun
  écran n'appelle** (motif 436/451). **Correction d'instrument** : le crible du
  453 aurait rangé `/api/options` parmi les non-consommées (appel en
  `.then(function (d){…})`, forme échappée) — la recherche de l'URL littérale dans
  les **octets servis** n'a pas cet angle mort. **Portée** : déstructuration,
  crochets et helpers à paramètre **échappent** (436), non quantifiés ; une route
  non citée reste **appelable à la main** ; `scan_state` vide au démarrage donc
  les six phrases ont été **lues à la source**, pas exécutées — **ce lot établit
  où va la valeur, pas ce qu'elle vaut**, et je n'ai pas fabriqué de banc pour
  faire nombre ; **aucun navigateur** ; **83 des 110 phrases du 444 restent
  fermées**. **Troisième lot d'affilée** (449, 451, 454) où la phrase examinée
  n'atteint aucun écran : la veine rend maintenant surtout du poids mort.
  Aucun fichier touché · SW `td-shell-v187` · **MD5 8/8 identiques** · écart
  runtime **aucun** · suite **2864 passed / 0 skipped** · rapport
  `docs/refactor/validation/SKYLER-LOT-454.md`.

- **Lot 453 — livré** : **j'ai tenté de généraliser le contrat rompu du 452 ; le
  balayage rend 26 candidats, tous faux sauf celui du 452, et il a fallu corriger
  l'instrument QUATRE fois pour pouvoir le dire.** 34ᵉ lot, 3ᵉ de la tranche.
  Question posée : le contrat rompu du 452 est-il **un genre ou un cas** ?
  **Réponse : un cas.** C'est un **bornage**, annoncé dès le titre.
  **Instrument** — combien de lectures `receveur.champ` dans le JS **servi**
  portent sur des clés que la route interrogée ne rend jamais :

  ```text
  corpus            58 sources servies (25 pages/ui inline + 33 JS statiques)
                    1 exclu : vendor minifié (leçon 437)
  appels VX.fetch                          87
  liaisons receveur ↔ URL reconnues        72   (83 %)
  lignes échappées, toutes nommées         15   (17 %)
  routes distinctes 47 · 200 JSON 46 · non concluante 1
  ```

  **Quatre corrections, chacune avec sa cause** : **(1)** couverture **32 → 72**
  — la première passe ratait l'affectation nue, `Promise.all` et
  `Promise.allSettled`, soit **37 % de l'usage** : huitième récidive du piège des
  enveloppes ; **(2)** **fenêtre de lecture contaminée** — 80 lignes après la
  liaison avalaient les lectures d'un **autre** receveur du même nom
  (`analysis_page.py:859` lie `d` à `/api/anomalies/`, `:869` rebinde
  `const d=r&&r.decision`), corrigé en arrêtant la fenêtre à **toute
  réaffectation** (médiane 34 lignes) ; **(3)** **les enveloppes
  `Promise.allSettled` ne sont pas la charge utile** — `.status`/`.value` sont
  les propriétés du wrapper : **17 couples** ; **(4)** **une classe de caractères
  contenant `\s` FRANCHIT le retour à la ligne** — mon extracteur d'imports a
  capturé `'series as _series\n    from vertex'` et **avalé l'instruction
  suivante** : **miroir exact de la leçon 435**. **Faux arrêtés avant
  publication : 20 → 24.** **Le crible** :

  ```text
  72 sites : 40 SAINS · 24 écart · 7 passe-plat · 1 non concluant
  78 couples (site, clé) en écart
     17 enveloppes allSettled            artefact
      2 clé écrite dans la vue           optionnelle
     26 chaîne de repli  X.a || X.b      lecture tolérante
     33 candidats → 7 expliqués par le module délégué → 26 SURVIVANTS
  ```

  **Les 40 sites sains sont le témoin positif intégré** — sans eux, un instrument
  rendant « tout est rompu » serait indistinguable d'un instrument juste.
  **Les 26 survivants, tranchés un par un — 25 sont faux** : **1**
  `/api/anomalies/` `a.anomalies` = **le défaut du 452, retrouvé** ; **7**
  `/api/analyst/` → `data_sources/analyst_deep.py` **les écrit 7/7**, route
  dépendante du **réseau** (yfinance), GET refusé par le proxy donc charge utile
  vide ; **5** `/api/evidence/` → `engines/evidence_lab.py:72-75` **les écrit
  5/5**, manqués par la correction n°4 ; **13** `/api/validator` → la vue rend
  `validator.build(eq)` **si** `scan_state['portfolio']` existe, or il vaut
  **None** au démarrage, donc la réponse servie est le repli **honnête**
  `{'ok': False, 'note': 'backtest indisponible (univers/historique
  insuffisant)'}` — **la leçon 438 dans sa forme pure** ; **1**
  `/api/ai/enrichment` `snap.as_of` → écrit par `ai/enrichment.py`.
  **Ce que le lot établit** : sur 72 sites couvrant 46 routes, **un seul** survit
  à quatre cribles et à l'examen à la main, et c'est celui déjà publié. **Cela
  BORNE le rang 1 du 452 au lieu de l'élargir.** **Le contrôle 443 et son coût** :
  la variante « écrivain n'importe où dans la **clôture d'imports** » classait
  `a.anomalies` comme optionnelle (car `analysis.py:314` et `skyler_core.py:173`
  portent une clé `'anomalies'` dans un **autre** dictionnaire) → **règle 443 non
  tenue, variante rejetée** ; la variante « clé littérale **dans la fonction de
  vue** + délégation à 1 niveau » la fait survivre. **Nouvelle règle : chercher un
  écrivain « quelque part dans la clôture d'imports » ne prouve rien — la clé doit
  être écrite dans LE dictionnaire RENDU ; la clôture d'imports, excellente pour
  l'ATTEIGNABILITÉ au 452, est le MAUVAIS OUTIL pour un CONTRAT DE CHARGE UTILE.**
  **Sous-produit rang 4** : **26 couples lus dans une chaîne de repli**
  (`ob.contracts||ob.list||ob.best`, `exec.blocking_anomalies||exec.blocking`) —
  **branches de repli mortes**, rien de faux à l'écran. **Portée** : 83 % mesurés,
  17 % nommés ; clés servies relevées **avec `scan_state` vide** — ce sont des
  **contrats observés au démarrage, pas prouvés** ; le GET sur `/api/analyst/AAPL`
  a **tenté un appel réseau sortant** refusé par le proxy, **aucune écriture** ;
  déstructuration et crochets **échappent** (436), non quantifiés ; **aucun
  navigateur**. Aucun fichier touché · SW `td-shell-v187` · écart runtime
  **aucun** · suite **2864 passed / 0 skipped** · rapport
  `docs/refactor/validation/SKYLER-LOT-453.md`.

- **Lot 452 — livré** : **85 modules sur 299 sont injoignables depuis
  `terminal.py`, et le balayage tombe sur une COLLISION DE ROUTE : la carte
  « Anomalies » de `/analysis` lit le contrat d'une route masquée, donc elle
  affiche « Aucune anomalie détectée » quoi qu'il arrive.** 33ᵉ lot, 2ᵉ de la
  tranche. Le 451 avait trouvé 269 lignes mortes **sans les chercher** ; ce lot
  généralise. **Instrument** : graphe d'imports par **AST** (299 modules
  `vertex/`, 609 fichiers `.py`, **0 échec de parse**) puis **clôture transitive
  depuis la seule vraie entrée produit, `terminal.py`** — le compte des
  importeurs directs ne suffit pas, un module mort qui en importe un autre le
  ferait passer pour vivant. **Cinq contrôles avant tout chiffre** :

  ```text
  14/14 modules de page servis          ATTEIGNABLES
  21/21 blueprints de app/routes        ATTEIGNABLES
   7/7  moteurs canoniques CLAUDE.md    ATTEIGNABLES
   5/5  reliques du lot 327             MORTS   (attendu)
   2/2  modules du lot 451              MORTS   (retrouvés SEULS — règle 443)
  ```

  **Ce qui échappe, mesuré** : deux fichiers seulement portent
  `importlib`/`__import__`, un seul en production — `vertex/data/company.py:231`
  `__import__('datetime')`, **bibliothèque standard**. **Aucun module `vertex/`
  n'est importé dynamiquement** : l'angle mort existe, il est vide.
  **Recensement** :

  ```text
  atteignables 214 · NON ATTEIGNABLES 85 · 6 192 lignes
     dont couverts par un test   55   4 869 lignes
     dont sans aucun test        30   1 323 lignes
  fichiers de tests concernés    33 / 301   (4 433 lignes)
  research 23 · data_sources 12 · options 9 · strategy 8 · ai 7 · ui 5 · autres 21
  ```

  **Le 451 n'était pas isolé** : ses 269 lignes sont **4,3 %** du total, et son
  motif — *du code mort figé par ses propres gardiens* — porte sur **55 modules
  et 33 fichiers de tests**. **Ce que le chiffre ne dit PAS** : non atteignable
  ≠ à supprimer (`research/` ressemble à une bibliothèque en attente) ; la
  mesure porte sur des **modules**, jamais sur des **fonctions**.
  **Où le balayage a mené (rang 2)** : `option_anomalies` et `vol_surface` sont
  **tous deux morts**, or `/opportunities` les nomme en **texte visible** —
  « ouvrir une analyse pour le détail (moteurs option_anomalies / vol_surface /
  portefeuille) ». Servi : **200, 67 278 o, md5 6a22a6abbd03 identique**, phrase
  présente 1 fois, **six** puces ; `Actions` et `Données` rendent proprement,
  **les quatre autres tombent dans le `else`**. **Témoin positif sur le même
  écran** : `Actions` est servie par `stock_anomalies`, **atteignable**
  (`terminal.py:38`). **La trouvaille (rang 1)** — en vérifiant cette promesse :

  ```text
  /api/anomalies/<sym>   2 règles GET
     analysis_api.api_anomalies    ← résolue par Flask (mesuré)
     strategy_os.anomalies_for     ← MASQUÉE

  gagnante  : as_of closes empty events extreme generator n_spikes narrative
              points reason series_source streak symbol vol_ratio
              → PAS de 'anomalies', PAS de 'note'
  masquée   : {'symbol', 'anomalies', 'note'}

  analysis_page.py:512-517 lit  a.anomalies  et  a.note
  ```

  Vérifié par lecture exhaustive : `engines/anomaly.py` n'a que **deux `return`**
  et **aucun** ne porte `anomalies` ; la route n'ajoute que
  `symbol`/`series_source`/`as_of`. La carte est dans `loadDossier()`, appelée au
  chargement (`:929`) et rafraîchie toutes les 180 s (`:937`). **Elle affiche donc
  EN TOUTES CIRCONSTANCES « Aucune anomalie détectée sur la série disponible. »**
  **Banc, cas sain et cas dégradé côte à côte** : 81 clôtures avec choc +16 % →
  `n_spikes 1`, `vol_ratio 11.84`, narratif « +16.0 %, z=8.4 … ×11.8 la normale »
  — **la carte dit « Aucune anomalie détectée »** ; 10 clôtures (sous
  `MIN_POINTS=21`) → `empty True` + `reason` honnête — **même texte**. La carte
  **confond trois états**. **Témoin positif sur la MÊME page** : `/analysis/<sym>`
  porte **deux** cartes servies par la **même requête** — `an-anomaly` (rendue par
  `charts/anomaly-scan.js`, lit `d.closes`/`d.events`/`d.narrative`/`d.reason`)
  est **honnête** ; `an-anomalies` lit deux clés jamais présentes. Les deux sont
  dans les octets servis de `/analysis/AAPL` (200, **75 829 o**). **Témoin négatif
  gratuit** : **4** URL portent deux règles, **une seule** oppose deux `GET` —
  `/api/client-log` (GET+POST), `/api/tracking` (GET+POST),
  `/api/tracking/<id>` (GET+PATCH) sont légitimes. **Les gardiens : deux verts, un
  de chaque côté de la collision** — `test_strategy_os_routes.py::test_anomalies_route`
  monte un **Flask nu** avec le seul blueprint `strategy_os` (**pas de collision**)
  et valide `isinstance(data['anomalies'], list)` ; `test_anomaly_engine.py::test_anomalies_route_reads_real_series`
  utilise `terminal.app` **réel** et valide `n_spikes >= 1`, **sans jamais
  comparer** ; `test_analysis_page_has_anomaly_card` n'assure que `'an-anomaly'`,
  la carte **singulier**, l'honnête. **Aucun des trois ne peut voir le défaut** —
  motif 381/385/414/415 dans sa forme la plus nette ; **aucun test ne compte les
  règles d'une même URL**. **Classement** : carte toujours vide → **rang 1**
  (affirmation fausse affichée, qui ment **du côté qui rassure**, famille
  432/433) ; **collision de route** → cause, **genre nouveau** : *deux routes GET
  sur la même URL, la consommatrice lisant le contrat de la perdante* ; phrase
  `/opportunities` → **rang 2** ; **85 modules / 6 192 lignes / 33 fichiers de
  tests** → **rang 3**. **Aucun GO, rien n'est engagé.** **Portée** :
  atteignabilité **statique** depuis `terminal.py` **seul** — `verifier_vertex.py`,
  `ib_reader.py`, `test_connection.py` volontairement exclus des entrées ; banc sur
  **moteur réel** et série **fabriquée** (comportement du code, pas fréquence
  réelle ; `scan_state['detail']` vide au démarrage) ; **aucun navigateur** ;
  **modules et non fonctions** ; **89 des 110 phrases du 444 restent fermées** —
  ce lot change de veine. Comptes inchangés : faux **arrêtés 20**, **publiés puis
  corrigés 3**. Aucun fichier touché · SW `td-shell-v187` · **MD5 8/8 identiques**
  · écart runtime **aucun** · suite **2864 passed / 0 skipped** · rapport
  `docs/refactor/validation/SKYLER-LOT-452.md`.

- **Lot 451 — livré** : **les quatre phrases `source` ne sont jamais produites —
  `build_surface` n'a aucun appelant, et la liste blanche d'outils de l'IA non
  plus.** 32ᵉ lot, premier de la tranche. **D'abord une erreur de plan, que je
  publie** : l'orientation supposait que `source` était une **étiquette de
  provenance** ; dans `vol_surface.py` c'est un **localisateur d'anomalie**
  (`f'{symbol} {exp} {k}'`). Le « 4 écrans » du 444 concerne un **autre**
  `source`. **Cinquième récidive du piège « un nom, plusieurs payloads »** — et
  **la première fois qu'il égare le PLAN, avant toute mesure**. **Le péage du 446
  a mordu à l'étape 1.** **Ces phrases n'atteignent aucun écran parce qu'elles ne
  sont JAMAIS PRODUITES** :

  ```text
  vol_surface.build_surface()          0 appelant hors module
  vol_surface.relative_value_zones()   0 appelant
  vertex/ai/tool_registry.py           0 appelant dans vertex/
  ```

  Les quatre `Anomaly(...)` sont toutes construites **dans** `build_surface()`.
  Les seules mentions hors module sont **une chaîne** dans une liste blanche et
  **le mot dans une phrase française**. **269 lignes** (210 + 59) qu'aucun chemin
  servi n'atteint. **Ce que cela ne veut PAS dire** : `FORBIDDEN_TOOLS` contient
  `place_order` — mais **l'invariant READONLY n'en dépend pas** : hors ce module,
  la recherche rend **une seule ligne**, `order_ticket.py:175`
  `'transmitted': False`. **Il n'existe aucun chemin d'ordre à garder.** **Les
  gardiens sont là, sur du code non appelé** — `test_ai_runtime.py`,
  `test_production_guards_canonical.py`, `test_vol_surface_lot108.py` : motif
  exact du **436**, un périmètre qui s'étend **au-delà du produit**. **Rang 4**
  pour les phrases jamais produites, **rang 3** pour les 269 lignes de poids mort
  figées par les tests. **Ce n'est pas un défaut de sécurité — mesuré, et répété
  pour que le classement ne soit pas sur-lu.** Correction = **décision de
  produit**. **Aucun GO.** **Portée** : appelants mesurés dans `vertex/` et
  `terminal.py` ; un dispatch **dynamique** échapperait (**non quantifié**, mais
  `register()` est lui-même sans appelant) ; **`realized_vol()` et `_median()` du
  même fichier ont 2 et 8 appelants** — le fichier n'est **pas entièrement mort**,
  et c'est le **témoin positif** de la mesure ; **aucun navigateur** ; **89 des
  110 phrases du 444 restent fermées**. Comptes inchangés : faux **arrêtés 20**,
  **publiés puis corrigés 3**. Aucun fichier touché · SW `td-shell-v187` · écart
  runtime **aucun** · suite **2864 passed / 0 skipped** · rapport
  `docs/refactor/validation/SKYLER-LOT-451.md`.

- **Lot 450 — livré** : **BILAN n°14 (tranche 440 → 449)** — voir le bilan en
  tête de ce document. Fait **sur pièces**, aucune trouvaille rejouée ; **une
  seule mesure fraîche**, les MD5 (**8/8 identiques**). **Base résolue
  explicitement** (leçon 430/440) : `d400bf2..3fc9045` = **10 commits, vérifié
  avant publication**. **Déposé** : 12 fichiers, **0 hors `docs/`**,
  **+2 552 / −0**, **0 fichier de production**, 10/10 partout, **98 591 octets**.
  **Bilan des dix lots** : **3 rang 1 · 2 rang 2 · 4 rang 4 · 3 bornages · 3
  corrections publiées**. **Le fait nouveau — le tri par affichage** : deux
  lectures (le 425 renommé / une règle distincte), et **je tranche pour la
  seconde** — le 425 dit **où chercher**, le 446 dit **s'il vaut la peine de
  dépenser la mesure** ; **trois rétrogradations au rang 4** (435, 436, 446)
  avant le péage, **trois lots productifs** (447, 448, 449) après. **Réserve** :
  petit échantillon, et le rendement doit une part à **la carte du 444** — la
  règle est bonne **parce qu'une carte existait**. **Le rendement, recompté — il
  BAISSE** : rang 1 **par lot** 4 / 4 / **3**, **par dossier distinct** 4 / 3 /
  **2** ; mais les **défauts affichés** (rang 1 + rang 2) **tiennent à 5** —
  **le volume tient, la gravité moyenne descend**. **Mes deux comptes d'erreurs,
  dont un était trop flatteur** : **arrêtés avant publication 20** (recompté,
  +6 dans la tranche, hérité **confirmé**) mais **publiés puis corrigés 3, et non
  1** — le 439 (« 22 248 octets » = caractères) corrigé au 441, le 442
  (« `rr_res` n'est affiché nulle part ») corrigé au 443, le 443
  (« `invalidation` lu par 5 écrans » + « `stop_type` atteint un écran »)
  corrigé au 444. **Je ne comptais que la troisième parce que le 444 l'avait
  nommée « la première fois » — c'était déjà la deuxième.** Le filtre retient
  **sept erreurs sur huit**, et **les trois qui sont passées ont toutes la même
  cause** : une portée annoncée **sans identifier le payload par sa forme**.
  **Ne prouvent pas** : aucune donnée réelle (bancs sur entrées **fabriquées**) ·
  **aucun navigateur de toute la tranche** · **93 des 110 phrases du 444 restent
  fermées** · plusieurs formatages **recopiés, pas exécutés** · comportement du
  **code**, jamais **fréquence** des cas réels. **Classement coût/risque mis à
  jour** avec **447** (7ᵉ — 1 filtre avant `max_pain`, **seul rang 1 de la
  tranche corrigible en un geste**), **448+449** (5ᵉ — 3 blocs `except`, **le
  modèle est déjà dans `horizon_scanners`, même page** : le moins risqué) et
  **442+443** (9ᵉ) ; **les six premiers ne touchent aucun moteur**. **Aucun GO.**
  **Quatorzième tranche sans qu'un seul des onze défauts classés — dont six à
  moins de dix lignes et sans moteur — ait été corrigé.** Aucun fichier de
  production touché · SW `td-shell-v187` · écart runtime **aucun** · suite
  **2864 passed / 0 skipped** · rapport
  `docs/refactor/validation/SKYLER-LOT-450.md`.

- **Lot 449 — livré** : **la veine `reason` refermée — 7 phrases sur 7 tranchées,
  le rang 2 du 448 passe d'une route à trois, et une phrase n'est jamais
  produite.** 31ᵉ lot, **dernier de la tranche 440-449** : il **solde la dette**
  du 448 (4 phrases non établies) au lieu d'ouvrir un front. **Étape A — route
  puis lecteur** : `options_lab_api:57` → `/api/options/strategies/<sym>` →
  `options-structure.js:101` (**ligne exacte** : le fetch est **quatre lignes plus
  haut**, `:97`) et `options-intel.js:468` (**niveau fichier**, les appels passent
  par un helper — **je ne prétends pas mieux**) · `options_lab_api:72` →
  `/api/options/analyze` → `options-structure.js:101` · `horizon_scanners:47` →
  `/api/options/scanner/<universe>` → `options-scanner.js:32` ·
  `tradingview_signal_store:52` → **aucune route**. **La quatrième n'est pas « non
  affichée » : elle n'est jamais produite** — `SIGNAL_STORE.record()` **n'a aucun
  appelant** dans tout `vertex/`. Chemin mort, **rang 4**. **Étape B — banc sur
  les moteurs réels** :

  ```text
  /api/options/strategies/<sym>   board mal typé → « AttributeError: 'str' object has no attribute 'get' »
  /api/options/analyze            leg mal typé   → « AttributeError: 'str' object has no attribute 'get' »
  /api/options/scanner/<univers>  « univers inconnu : 'INCONNU' (attendu ['LEAPS','SWING','TACTICAL']) »
                                  « aucun contrat SWING dans la fenêtre [60, 180] pour ce filtre »
  ```

  **Le rang 2 du 448 TRIPLE** : trois routes de `/options` rendent une
  `AttributeError` Python dans une carte d'état vide. **Et le témoin positif est
  sur la même page** : `horizon_scanners` rend, **même champ, même page, même
  chemin de rendu**, un refus qui **nomme la valeur reçue et l'ensemble attendu**.
  **Le défaut n'est donc une propriété ni de la page ni du champ — mais des blocs
  `except`.** **Veine refermée** : 7/7 tranchées · **6 affichées · 3 exactes · 3
  vidages · 1 morte** ; **aucune ligne « non établie »**. **Aucun GO. Aucun
  gardien** ; la correction pressentie est **écrite dans `horizon_scanners`**.
  **Portée** : exceptions **réelles** mais formatage **recopié**, pas exécuté ;
  **une seule famille d'entrées mal formées** ; **`board None` et `spot None` ne
  lèvent pas** — le vidage n'apparaît que sur une entrée **mal typée**, dont **la
  fréquence réelle n'est pas mesurée** ; **aucun navigateur** ; **93 des 110
  phrases du 444 restent fermées, ce lot n'en ouvre aucune**. Comptes séparés
  inchangés : faux **arrêtés 20**, **publiés puis corrigés 1**. Aucun fichier
  touché · SW `td-shell-v187` · écart runtime **aucun** · suite **2864 passed /
  0 skipped** · rapport `docs/refactor/validation/SKYLER-LOT-449.md`.

- **Lot 448 — livré** : **« simulation impossible : 'NoneType' object has no
  attribute 'spot' » — une exception Python s'affiche sur `/options` comme motif à
  l'utilisateur.** 30ᵉ lot. Dernier gros champ non ouvert : **`reason`**, 7
  phrases, **sept producteurs différents**. **Classées par nature** : **3 vidages
  d'exception** (`options_intel_api:113`, `options_lab_api:57` et `:72`), 1 refus
  de validation, 1 refus de config, **2 claims chiffrés** (`anomaly:56`,
  `evidence_lab:59`). **L'affichage d'abord** (leçon 447), payload identifié par
  sa forme : **établi** pour `evidence_lab:59` (route `/analysis` à paramètre),
  `anomaly:56` (`anomaly-scan.js:15`) et `options_intel_api:113`
  (**`options-intel.js:413`, page `/options`**) ; **non établi** pour les quatre
  autres — **nommées, non comptées**, et je ne conclus **ni** qu'elles sont
  affichées **ni** qu'elles ne le sont pas. **Les deux claims chiffrés sont
  exacts** :

  ```text
  clôtures    0    5   20   21   30   40   41   60
  annoncé     0    5   20   21   30   40    —    —      (= réel à chaque fois)
  available   F    F    F    F    F    F    T    T      (bascule EXACTE au seuil 41)
  ```

  **Point levé puis écarté** : la garde est un `or` — la forme qui au **418**
  testait le repli ; ici saine, `anomaly.scan` n'ayant **qu'une branche `empty`**
  (`< 21`), donc `empty` ⟹ `points < 41`. Les seuils **21** et **41** diffèrent
  volontairement et **chaque module affiche le sien**. **La trouvaille** :
  `options_intel_api:113` renvoie `'simulation impossible: %s' % e` et
  `options-intel.js:413` le rend en état vide. **Mesuré sur une exception réelle
  de `scenario_pricer.simulate`** : **« simulation impossible: 'NoneType' object
  has no attribute 'spot' »** — trois fois sur trois ; les deux autres routes
  donnent **« KeyError: 'x' »**. **Rang 2** : **pas** une affirmation fausse (donc
  pas rang 1), **pas** sans conséquence (affiché en texte visible, donc pas rang
  4), et **déroge à la norme du dépôt** — le contre-exemple est **le champ voisin
  du même corpus**. Correction : journaliser côté serveur, rendre un motif écrit.
  **Aucun GO. Aucun gardien.** **Ce que le lot dit du contraste** : les deux
  phrases qui **affirment un chiffre** sont **exactes** ; le défaut est d'une
  **autre nature** — **les moteurs disent vrai, ce sont les chemins d'exception
  qui ne disent rien d'utile**. **Portée** : 3 sur 7 établies ; l'exception est
  **réelle** mais son formatage est **la ligne de la route recopiée**, pas la
  route exécutée (**une reproduction n'est pas une exécution**) ; **je n'ai pas
  cherché** d'exceptions plus révélatrices ; **aucun navigateur** ; **93 des 110
  phrases du 444 restent fermées**. Comptes séparés inchangés : faux **arrêtés
  20**, **publiés puis corrigés 1**. Aucun fichier touché · SW `td-shell-v187` ·
  écart runtime **aucun** · suite **2864 passed / 0 skipped** · rapport
  `docs/refactor/validation/SKYLER-LOT-448.md`.

- **Lot 447 — livré** : **« max pain à J-3 de la plus proche échéance » — l'aimant
  annoncé est celui de TOUTES les échéances mélangées, et la phrase s'affiche en
  clair sur le portefeuille.** 29ᵉ lot. **L'affichage d'abord** (leçon 446) :
  trois phrases du champ `detail` viennent de `positions_api.py:202/213/219`,
  servies par `/api/positions/alerts` — route citée par `/portfolio`, dont
  `portfolio_page.py:484` lit `g.detail` sur `alerts.gamma` et `:488` le rend en
  **texte visible** dans la carte « Surveillance ». **Première fois de cette veine
  que des phrases serveur sont trouvées affichées en clair**, pas en infobulle.
  **Deux phrases sur trois** : l'inégalité imprimée **est** la condition testée
  (« Spot sous le mur put (%s < %s) », « Spot sous la bascule zero-gamma ») —
  **dit comme une lecture, pas comme une mesure**. **La troisième, mesurée** :
  `gex.max_pain(contracts)` **parcourt tous les contrats et ne groupe jamais par
  échéance**, quand sa docstring parle de « l'aimant d'expiration » au singulier.

  ```text
  A. cas sain — une seule échéance      max_pain(J-3) = 100.0 = max_pain(board)   ACCORD
  B. cas réel — deux échéances          max_pain(J-3) = 100.0   max_pain(board) = 130.0
  C. phrase rendue (spot 129,0)         « max pain (129.0 ~ 130.0) à J-3 … »
  ```

  **La phrase nomme une échéance et lui attribue une statistique qui n'est pas la
  sienne** — écart de 30 points sur le banc. **Ce n'est pas un cas de bord** : le
  board est **multi-échéances par conception** (LEAPS `dte >= 300`, buckets
  court/moyen/long), et la condition `min(dtes) <= 7` exige une échéance proche
  **pendant** que le board en porte de lointaines. **Rang 1** — texte visible, sur
  les **positions réelles**, et un trader qui lit « max pain 130 à J-3 » en déduit
  une force d'épinglage qui sur cette échéance **n'existe pas**. Correction
  pressentie : **filtrer sur l'échéance la plus proche avant `max_pain`** — ce que
  la docstring promet déjà. **Aucun GO. Aucun gardien.** **Détail relevé, non
  classé** : `int(min(dtes))` tronque (6,9 j → « J-6 »), une troncature n'est pas
  une affirmation fausse. **Portée** : banc sur board **fabriqué** — la
  **fréquence des divergences réelles n'est pas mesurée** ; **aucun navigateur** ;
  **3 phrases ouvertes sur les 19** des champs à quatre écrans, `reason`, `source`
  et `narrative` **non ouverts** ; **100 des 110 phrases du 444 restent fermées**.
  Comptes séparés inchangés : faux **arrêtés 20**, **publiés puis corrigés 1**.
  Aucun fichier touché · SW `td-shell-v187` · écart runtime **aucun** · suite
  **2864 passed / 0 skipped** · rapport
  `docs/refactor/validation/SKYLER-LOT-447.md`.

- **Lot 446 — livré** : **« clôture séance +5 » compte les séances OBSERVÉES, pas
  les séances de marché — le contraste moteurs/pages du 445 est nuancé, pas
  confirmé.** 28ᵉ lot, **bornage du 445**. Troisième producteur indépendant :
  `decision_memory`, 16 phrases jamais ouvertes. **Banc sur `measure()`**, log
  construit par le vrai producteur `record_close()` :

  ```text
  terminal ouvert tous les jours   10 séances   « séance +5 »   5.0 %   ← témoin positif, ACCORD
  4 jours sans scan                 6 séances   « séance +5 »   8.0 %   ← réel à +5 séances : 5.0 %
  ```

  **Le module le documente lui-même** : « aucun jour sans scan n'est comblé — un
  trou dans le log reste un trou ». Le log n'écrit qu'aux jours de scan, et
  `closes_after_date()` rend une liste **compactée**. **Le trou vient de l'usage,
  pas de la donnée** — `record_close()` et `series.closes()` refusent les entrées
  invalides. **Deux conventions dans la même fonction** : la branche EN_ATTENTE
  dit « séance(s) postérieure(s) **observée(s)** », la branche MESURE, **dix
  lignes plus bas**, dit « clôture séance **+5** » — famille **426** appliquée aux
  deux branches d'une seule fonction, contre-exemple compris. **Mais la
  conséquence n'atteint aucun écran** : `horizons`, `H5`/`H20`/`H60`,
  `sessions_observed`, `mfe_pct`/`mae_pct` → **0 écran** ; les deux lectures de
  `return_pct` appartiennent à **d'autres payloads** (une cible de scénario, une
  ligne de calibration). **Quatrième occurrence du piège « un nom, plusieurs
  payloads » — arrêtée avant publication : vingtième résultat faux arrêté.**
  **Rang 4** — défaut réel dans le moteur, sans conséquence à l'écran aujourd'hui.
  **Réserve** : si ces horizons sont un jour affichés, le défaut devient sérieux
  **et il flatte** (mesurer la 5ᵉ séance *observée* allonge la période réelle) ;
  correction déjà écrite dix lignes plus haut — dire « observée » des deux côtés.
  **Aucun gardien.** **Réponse au 445 : nuancée, pas confirmée** — le contraste
  moteurs/pages tient sur les **conséquences affichées**, pas sur la **justesse du
  vocabulaire** ; **mon échantillon du 445 était favorable sur cet axe, et je le
  dis**. **Portée** : **1 phrase ouverte sur 16**, **103 des 110 phrases du 444
  restent fermées** ; banc = log **fabriqué**, la **fréquence réelle des trous
  n'est pas mesurée** ; `H20`, `H60`, `CATALYSEUR` **non vérifiés** (même
  fonction, mesuré une seule fois) ; **aucun navigateur**. Comptes séparés : faux
  **arrêtés 20**, **publiés puis corrigés 1**. Aucun fichier touché · SW
  `td-shell-v187` · écart runtime **aucun** · suite **2864 passed / 0 skipped** ·
  rapport `docs/refactor/validation/SKYLER-LOT-446.md`.

- **Lot 445 — livré** : **j'ouvre les phrases que le serveur écrit, et elles sont
  justes — 15 accords sur 16, le seizième sur un état inatteignable.** 27ᵉ lot.
  Le 444 avait livré la carte (110 phrases, **aucune vérifiée**) ; ce lot ouvre
  les **28 phrases de `basis`**. **Banc** : `confidence()` appelée sur des paquets
  fabriqués, chaque `basis` confronté à la valeur du même appel.

  ```text
  dq_pts 0→4     « bloc data_quality N/4 du score »            0.0 → 1.0    5 accords
  n_contra 0→5   « N contradiction(s) — −0,20 chacune »        1.0 → 0.0    6 accords
  n_insuf 0/2/4/8 « N bloc(s) insuffisant(s) sur 8 »           1.0 → 0.0    4 accords
                                                        accord phrase/valeur : 15/16
  ```

  **Dénominateurs exacts** : `block(...)` est appelé sous **8 noms distincts** ;
  le profil servi donne bien `"data_quality": 4`. **Le seizième cas** : à
  `n_contra = 6` l'écrêtage rend le coût marginal 0,00 et la phrase serait fausse
  — **j'ai failli le publier**, car `skyler_core.py:197` est une **boucle**. En
  remontant, `market_context.py:107-114` n'a **qu'un seul `if`** : au plus **un**
  conflit, donc **4 contradictions maximum**, donc **l'écrêtage n'est jamais
  atteint**. *Une boucle n'est pas une preuve de multiplicité — il faut remonter
  à ce qu'elle parcourt.* **Dix-neuvième résultat faux arrêté avant
  publication.** **`knowledge_graph`** : **deux phrases pour deux méthodes**, le
  repli explicitement étiqueté « SPY absent, marché non contrôlé » (ce qui
  manquait au dossier **422**), **`L-1` points** — le compte exact, aucune
  inflation du n — et le seuil affiché ; les trois autres `basis` nomment leur
  provenance (« par la watchlist du code », « date déclarée », « position réelle
  déclarée »), chaque arête porte un `evidence_level`, et le fichier ajoute
  lui-même « relations jamais inventées ». **Aucun défaut — et c'est le
  résultat** : **six phrases ouvertes, six exactes**. **Première famille
  d'affirmations que la boucle mesure et trouve SAINE**, en contraste net avec
  427→443 côté interface : **les phrases écrites par les moteurs tiennent mieux
  que celles écrites dans les pages.** **Rang 4** à surveiller : le `4` en dur du
  dénominateur `data_quality`, **dans la phrase et dans le calcul**, alors que le
  bloc lit la valeur du profil — aucun écart aujourd'hui, un changement de profil
  en créerait un **des deux côtés à la fois**. **Portée** : **6 phrases sur 28**,
  **104 des 110 phrases concluantes du 444 restent fermées** ; banc = paquets
  fabriqués ; **je n'ai pas vérifié que `_pearson` calcule une vraie corrélation**
  — seulement que **la phrase dit ce que le code fait**, pas que le code fait ce
  qu'il faut ; **aucun navigateur**. Comptes séparés : faux **arrêtés 19**,
  **publiés puis corrigés 1**. Aucun fichier touché · SW `td-shell-v187` · écart
  runtime **aucun** · suite **2864 passed / 0 skipped** · rapport
  `docs/refactor/validation/SKYLER-LOT-445.md`.

- **Lot 444 — livré** : **235 phrases écrites par le serveur, jamais recensées
  depuis le 427 — et la première fois qu'un résultat faux m'a échappé jusqu'au
  rapport publié.** 26ᵉ lot. Le 443 avait ouvert la classe sans la quantifier ;
  ce lot la quantifie **et retire l'exemple sur lequel le 443 fondait sa règle**.
  **Instrument par AST** (pas par motif) : 299 fichiers Python, toute f-string ou
  `%`-format **interpolant une valeur** et rangée sous un nom de champ →
  **74 champs, 235 phrases**. Témoin positif : `invalidation`
  (`committee.py:133`) ressort bien. **125 phrases sur 235 sont NON CONCLUANTES**
  — 36 noms trop génériques pour être distingués dans du JS (`note` 31, `error`
  16, `src` 7, `label` 6…), leçon 437 généralisée aux noms communs : **je les
  nomme et je ne les compte pas**. **Périmètre concluant : 38 champs, 110
  phrases, 13 atteignent un écran** — `reason` 4 écrans · `detail` 4 · `source` 4
  · `narrative` 4 · `basis` 3 (28 phrases) · `action` 3 · `impact` 3 · … ; **25
  champs distinctifs lus par aucun écran**. **LA CORRECTION — mon 443 s'est
  trompé deux fois sur la même ligne.** Il publie « `invalidation` est lu par
  cinq écrans, 12 fois » : **(1)** le « cinq » comptait des **mots français** —
  `/portfolio` 9 occurrences, **0 lecture de champ** (« Cassée — invalidation
  atteinte » est un libellé) ; strictement, **2 écrans** ; **(2)** et ces deux-là
  lisent **un autre `invalidation`** — `skyler_core:433/627` émet
  `'invalidation': stop`, **un nombre**, formaté par `VX.fmt.num`. **La phrase du
  comité n'est lue par aucun écran.** **Troisième occurrence du piège « un nom,
  plusieurs payloads »** (438 `scan`, 441 `.decision`) — **et la première à ne pas
  avoir été arrêtée avant publication.** Les deux comptes restent séparés :
  **arrêtés avant publication 18** (inchangé), **publiés puis corrigés 1** (de 0).
  **Le verdict « `stop_type` atteint un écran » est RETIRÉ** ; le reste du 443
  (douze champs du plan, trois R:R, correction du 442) **n'est pas touché**.
  **La règle survit, avec un vrai exemple** : **`basis`**, 28 phrases composées
  (`decision_memory` 16, `knowledge_graph` 6, `skyler_core` 5, `red_team` 1), lu
  par `/portfolio`, `/journal`, la route `/analysis` à paramètre et
  `performance_page` — et **porteuses de chiffres** (« corrélation des résidus de
  marché = %.2f sur %d points », « %d contradiction(s) tracée(s) — −0,20
  chacune », « bloc data_quality %d/4 du score »). **Où elles s'affichent** :
  surtout en attributs **`title=`**, visibles au **survol** — ce qui explique
  qu'aucun recensement de la boucle (texte visible ou littéraux du client) ne les
  ait jamais croisées. **Aucun défaut de produit nouveau** ; **les 110 phrases
  concluantes sont recensées, NON OUVERTES** — vivier du lot suivant. **Portée** :
  une phrase composée sans nom échappe (**non quantifié**) ; les 125 génériques
  sont **hors mesure, pas hors existence** ; déstructuration et variable
  intermédiaire échappent (limite du 436) ; **aucun navigateur**, infobulles non
  observées. Aucun fichier touché · SW `td-shell-v187` · écart runtime **aucun** ·
  suite **2864 passed / 0 skipped** · rapport
  `docs/refactor/validation/SKYLER-LOT-444.md`.

- **Lot 443 — livré** : **trois R:R différents sur la même page, et le seul
  honnête n'apparaît que pour se plaindre — le test du 442 généralisé aux douze
  champs du plan.** 25ᵉ lot. **Instrument à deux témoins intégrés** : pour chacun
  des 12 champs, valeurs distinctes sur 6 marchés × occurrences servies ×
  moteurs — **il doit retrouver seul les deux trouvailles du 442, et il les
  retrouve** (`rr` → 1 valeur distincte, `rr_res` → 5 distinctes / 0 servi) ;
  **0 déstructuration, 0 accès par crochet**. **Sept champs sur douze atteignent
  un écran, un seul est totalement mort.** **Trois verdicts faux arrêtés avant
  publication** — mon premier tableau annonçait **six** « jamais servis » :
  **`resistance`** est lu par `price-chart.js:16` et rendu comme niveau
  « Résistance » — consommé **dans un builder** (*6ᵉ récidive* de « compter sans
  les enveloppes ») ; **`setup_quality`** existe à **deux niveaux** du payload
  (`analysis.py:264` et `:316`), les cinq moteurs lisent le second (leçon 438
  appliquée aux **niveaux** d'un même objet) ; **`stop_type`** est **fondu dans
  une phrase composée au serveur** — `committee.py:133` bâtit
  `invalidation = "clôture sous $X (structure)"`, et `invalidation` est lu par
  **cinq écrans**, **12 fois** sur la route `/analysis` à paramètre. **Règle
  nouvelle** : *un champ peut atteindre l'écran à l'intérieur d'une phrase
  composée au serveur — une recherche par nom de champ ne le verra jamais.*
  **Seul champ vraiment mort** : `stop_dist_atr`, aucun lecteur nulle part —
  **rang 4**. **Correction due à mon propre 442** : « `rr_res` n'est affiché nulle
  part » était **trop fort** — mesuré via `build_ticket()`, il apparaît en
  **message de blocage** (« R:R 0.4 < 2.0 (minimum stratégie) ») **uniquement
  sous 2,0** ; à 3,5 ou 4,7 il n'est montré nulle part. **Le R:R honnête
  n'apparaît que lorsqu'il est mauvais.** **Ce que le balayage a trouvé de
  neuf** : `pretrade.py:130` **recalcule un troisième R:R** depuis le prix live,
  et `/api/pretrade/check` est l'une des douze routes de la page :

  ```text
  cas                carte plan   rr_res   pré-trade au prix d'entrée   à +3 %
  haussier calme          3.0:1      0.4                        1.0:1    0.2:1
  baissier                3.0:1      1.1                        1.0:1    0.3:1
  court (120 barres)      3.0:1      4.7                        1.0:1        —
  ```

  Le pré-trade rend **1,0:1 au prix d'entrée pour tous les titres** — structurel
  (`tp1 = entrée + risque`) : **un second constant par construction**. **Et il est
  étiqueté comme une faute** (« (< 2:1 — Constitution) »). **La même page peut
  donc afficher, au même instant, « R:R structurel 3 » et « R:R 1.0:1 (< 2:1 —
  Constitution) »** — l'un dit que le plan est bon, l'autre qu'il viole le
  minimum de la stratégie ; **aucun des deux n'annonce contre quel objectif il
  compte**, et **aucun n'est celui que les neuf moteurs utilisent**. **Rang 1, et
  il AGGRAVE le 442.** Correction pressentie : nommer la référence de chaque R:R
  et afficher `rr_res`. **Aucun GO. Aucun gardien.** **Portée** : le R:R du
  pré-trade est **reproduit depuis la formule**, pas obtenu en appelant la route
  (POST exigeant un `scan_state` peuplé) ; banc **synthétique** ; **l'instrument
  est aveugle aux phrases composées au serveur** et je **n'ai pas quantifié**
  combien d'autres champs passent par là ; `atr` et `setup_quality` sont **« non
  observé », pas « absent »** ; **aucun navigateur**. Compte des résultats faux
  arrêtés : **dix-huit**. Aucun fichier touché · SW `td-shell-v187` · écart
  runtime **aucun** · suite **2864 passed / 0 skipped** · rapport
  `docs/refactor/validation/SKYLER-LOT-443.md`.

- **Lot 442 — livré** : **« R:R structurel 3 » — le seul R:R affiché sur la page
  d'analyse vaut 3 sur tous les marchés, et celui qui varie, lu par huit moteurs,
  n'est affiché nulle part.** 24ᵉ lot. Le 441 avait recensé 5 affirmations sur la
  route `/analysis` à paramètre **sans en ouvrir aucune** ; ce lot en ouvre une et
  en trouve une autre en chemin. **Ce que je cherchais** : `analysis_page.py:414`
  annonce « moyennes mobiles 20/50/200 » dans le tiroir, et `:389` les **filtre**
  — le moteur le documente (`analysis.py:266-268`). **Mesuré sur le moteur
  réel** :

  ```text
  barres    11    30    60   120   199   200   400
  MM tracées 1     1     2     2     2     3     3      (« 20/50/200 » annoncées à chaque fois)
  ```

  Seuil **exactement 200 barres**, carte tracée **dès 11**. Famille du **425**.
  **Atténuation réelle mais non co-visible** : la légende (`candlestick-lwc.js:69`)
  n'affiche que les courbes tracées, mais le tiroir (`chart-core.js:167-175`) ne
  rend **ni légende ni limites**. **Rang 2.** **Non établi** : aucun titre réel à
  moins de 200 barres observé — la **fréquence du cas n'est pas mesurée**.
  **Ce que j'ai trouvé en chemin** : `plan.rr` a **un seul écrivain**,
  `analysis.py:262` → `'rr': 3.0`, **un littéral** — le R:R affiché est la
  **définition de `tp3`** relue à l'envers. **Mesuré sur six marchés très
  différents** : entrée 113,51 → 30,28, stop 107,83 → 27,00, tp3 130,56 → 40,13
  (**témoin positif : le moteur réagit**) et **« R:R structurel » = 3.0 dans les
  six**, tandis que **`rr_res` prend [0.4, 0.7, 1.1, 3.5, 4.7]**. **Et `rr_res`
  n'est affiché nulle part** : lu par **huit moteurs** (`committee`,
  `decision_stack` ×2, `decide`, `evidence`, `skyler_core`, `chart_read`,
  `planning_api`→`order_ticket`), il compte **0 occurrence** dans les octets
  servis, quand `plan.rr` en compte **7** (4 rendus : conclusion de carte,
  `aria-label`, ligne de carte plan, libellé du cône). **Le R:R qui décide n'est
  jamais montré ; le R:R montré ne peut pas varier.** **Rang 1** — atténuation
  dite d'abord (« structurel » peut se lire « par construction », le chiffre
  **n'est pas faux**), mais la ligne siège **dans une liste de cinq valeurs par
  titre qui varient toutes**, rien ne signale la tautologie, et la vraie
  différence (0,4 contre 4,7) **n'atteint pas l'écran**. Croisement de **428** et
  **433** ; le contre-exemple est **une ligne plus bas**. Correction pressentie :
  afficher `rr_res`, déjà calculé et déjà servi. **Aucun GO.** **Aucun gardien.**
  **Une hypothèse écartée** : le repli `—` du stop (`vx-core.js:43`) **n'est pas
  atteignable** — `plan.stop` est toujours un nombre réel de 11 à 250 barres.
  **Portée** : moteur réel mais séries **synthétiques** — un **banc**, pas le
  marché ; **aucun navigateur** ; **4 des 5 affirmations restent non vérifiées**.
  Aucun fichier touché · SW `td-shell-v187` · écart runtime **aucun** · suite
  **2864 passed / 0 skipped** · rapport
  `docs/refactor/validation/SKYLER-LOT-442.md`.

- **Lot 441 — livré** : **la page d'analyse que la boucle n'avait jamais servie —
  `/analysis/<sym>` fait 75 829 octets, porte 20 graphiques et 12 routes, et aucun
  des zéros publiés ne bouge.** 23ᵉ lot, premier de la tranche. Le 439 laissait
  `/analysis` en **piste** ; ce lot l'ouvre. **`/analysis` est un LANCEUR** :

  ```text
                       octets   VXCharts   vx-card   routes /api
  /analysis (index)    22 359          0        17             1
  /analysis/AAPL       75 829         20        77            12
  ```

  **La piste est refermée dans le sens NÉGATIF** : l'index n'est pas une
  exception, c'est un écran de saisie ; le contenu vit à `/analysis/<sym>`.
  `render(sym)` est un **pur assembleur de chaînes** — `/analysis/AAPL` et
  `/analysis/MSFT` font **exactement la même taille**, tout est hydraté côté
  client. **Le corpus des 95 objets était incomplet** : aucune route à paramètre
  n'y figurait, il y en a **sept**, mais **une seule vraie page** (`+2 %` du
  corpus) — les autres sont deux redirections, deux fragments et deux 404.
  **Aucun zéro publié n'en est affecté** : les quatre jetons du 435 rendent **0**,
  et `/api/command` n'est **jamais appelé** depuis cette page (436). **Piège
  évité** : `.decision` ×8 sur cette page appartient à `/api/decision/` et
  `/api/strategy/decision/`, pas au champ du 436 — *un nom d'identifiant peut
  désigner plusieurs payloads* (438), appliquée **avant** la faute. **Une
  trouvaille qui n'en était pas — le quinzième instrument** : le recensement
  rendait `confirm` **sans `invalidate`** sur la page qui demande « méritent-elles
  du capital maintenant ? » — **faux**, `analysis_page.py:414` porte
  `invalidate:` en **littéral gabarit**, invisible à un motif à guillemets
  simples. Arrêté par la lecture de la source brute. **La zone d'ombre enfin
  chiffrée : 3,2 %** (90 simples · 0 doubles · **3 gabarits** · total **93**),
  témoin positif `/journal` = **8**, exactement le chiffre du 439 — **réelle et
  petite**, mais les trois rattrapées **interpolent une donnée vivante** et l'une
  d'elles **est le dossier 422** : *3,2 % en nombre, pas 3,2 % en risque*. **Un
  chiffre du 439 corrigé** : « 22 248 octets » pour `/analysis` est en fait
  **22 359 octets** — 22 248 est le nombre de **caractères** (md5 `113827718e99`
  inchangé) ; confirmé sur `/analysis/AAPL` (**75 829 o pour 75 216 caractères**).
  **Unité mal étiquetée, deuxième récidive après le « quatorze » du 440.**
  **Témoin positif involontaire** : la suite lancée **avant** l'insertion de la
  ligne d'index a fait **échouer**
  `test_skyler_index_integrity_lot228::test_tout_rapport_du_perimetre_a_sa_ligne_d_index`
  — exactement ce qu'il promet ; relancée après les trois documents : **2864
  passed**. Ce gardien mord réellement, ce qu'aucun lot n'avait vérifié.
  **Aucun défaut de produit nouveau** — rien à ajouter aux dossiers, rien à
  retirer. **Portée** : HTML de page seulement (les 35 affirmations du JS
  `/static` de `/options` **ne sont pas dans les 93**) · **aucune des 5
  affirmations de `/analysis/<sym>` ouverte** · mesure sur le **squelette servi**,
  12 routes non appelées · `/options/<sym>` classé **fragment** · **aucun
  navigateur ouvert**. Aucun fichier touché · SW `td-shell-v187` · écart runtime
  **aucun** · suite **2864 passed / 0 skipped** · rapport
  `docs/refactor/validation/SKYLER-LOT-441.md`.

- **Lot 440 — livré** : **BILAN n°13 (tranche 430 → 439)** — voir le bilan en
  tête de ce document. Traité **sur pièces** : dix rapports relus, chiffres
  vérifiés dans le dépôt, **aucune trouvaille rejouée**, aucun serveur DEMO, aucun
  moteur rouvert ; **une seule mesure fraîche**, les MD5. **Déposé
  (`1ac8446..d400bf2`)** : **10 commits · 12 fichiers · 0 hors `docs/` ·
  +2 133 / −0 · `terminal.py` + `vertex/**` : 0 fichier** ; 10/10 rapports, 10/10
  lignes d'index, 10/10 blocs STATUS, **80 011 octets**. **Base résolue
  explicitement** (leçon 430) : `e62fecb` **est** le lot 430, l'intervalle ne
  couvrait que 431→439 — corrigé avant publication. **Bilan des dix lots** : 4
  trouvailles de **rang 1** (432, 433, 434, 437) · 1 rang 2 · 1 rang 3 · 2 rang 4
  · 3 bornages · **1 annulation de mon propre rang 1** (431). **Le fait nouveau —
  quatorze instruments jetés en six lots** (430 ×1, 434 ×2, 435 ×1, 437 ×3, 438
  ×3, 439 ×4), **tous arrêtés avant publication** par trois contrôles : témoin
  positif, invraisemblance, lecture de la sortie brute. **Et je corrige le
  chiffre-titre lui-même** : sur 437 et 439 l'unité est une **version
  d'instrument**, sur 438 une **ligne fausse d'un seul instrument** → **12 par
  version, 14 par résultat faux** ; le « quatorze » du 439 mélange les deux — il
  n'est faux dans aucune convention, il est **inconstant**. Convention retenue :
  **résultat faux produit, 14**. **Durcissement ou rendement décroissant — les
  deux lectures, puis la réponse** : ce qui tranche, c'est que **le rendement n'a
  pas bougé — 4 rang 1 sur 10 lots au 420-429, 4 rang 1 sur 10 lots au 430-439** ;
  le nombre d'instruments jetés monte parce que **la portée des questions monte**
  (jusqu'au 433 la boucle lisait une fonction, depuis le 434 elle balaie 3 829 722
  octets servis). **Réponse : durcissement.** **Deux réserves assumées** : le
  « 14 en six lots » est **en partie un artefact de comptage** (la boucle ne
  journalisait pas ses instruments écartés avant le 434 — *on ne conclut pas à une
  tendance depuis une série qui commence quand on se met à compter*), et cette
  lecture juge la boucle sur ce qu'elle **trouve**, pas sur ce qu'elle **change**,
  où le rendement est **nul depuis treize bilans**. **Une limite du n°12 levée** :
  les MD5 des 8 pages, remesurés ici encore, sont **8/8 identiques** — leur
  constance est désormais **une mesure**, plus une inférence. **Classement
  coût/risque mis à jour** avec 432+433, 434 et 437 : 1 · 434 `renderAnomalies`
  (copier la garde écrite 20 lignes plus haut) · 2 · 427 légende multi-indices ·
  3 · 428 entonnoir · 4 · 437 « Catalyseurs imminents » (retirer `|| Date.now()`
  sur 3 pages) · 5 · 425 « 4 maturités » · 6 · 432+433 les trois synthèses
  `/portfolio` (conditionner sur `allMarked` **déjà calculé**) · 7 · 424
  `thesis_health` · 8 · 422 expected-move muet — **les six premiers ne touchent
  aucun moteur** (quatre fichiers de page : un lot, un bump SW, une preuve
  navigateur). **Aucun GO, rien n'est engagé.** **Portée** : le bilan ne rejoue
  rien — **si un rapport s'est trompé sur un fait présenté comme mesuré, ce bilan
  reprend l'erreur** ; la comparaison de rendement porte sur un **classement que
  j'attribue moi-même**. Aucun fichier de production touché · SW `td-shell-v187`
  inchangé · écart runtime **aucun** · suite **2864 passed / 0 skipped** ·
  rapport `docs/refactor/validation/SKYLER-LOT-440.md`.

- **Lot 439 — livré** : **les trois pages jamais ouvertes — `/journal` est
  exemplaire, `/options` cache ses affirmations dans son JS, `/analysis` n'en a
  aucune — et six instruments ont été jetés pour l'établir.** Vingt-deuxième lot,
  **dernier de la tranche**. **Phrases rassurantes** : `/journal` **7, toutes
  honnêtes** — chacune **nomme l'entrée manquante** (« Aucune erreur déclarée —
  renseigne le champ « erreur » à chaque sortie perdante », « Aucune leçon
  consignée… ») ; `/analysis` 1 ; `/options` 0. **`/journal` est le meilleur
  exemple du dépôt** : c'est exactement la garde qui manquait à `/portfolio`
  (432, 433) et à `renderAnomalies` (434). **Affirmations rendues** :

  ```text
                HTML de page   JS de page   TOTAL
  /journal            8            —           8   dont 2 chiffrées
  /analysis           0            0           0
  /options            0           35          35
  ```

  **`/options` ne cache rien, mes premiers comptages si.** **`/analysis` n'a
  aucune affirmation nulle part** : **22 248 octets** servis (la plus petite des
  huit), **0 `<canvas>`, 0 `VXCharts`, 0 vue**, 17 coques `vx-card`, un seul appel
  réseau (`/api/names`). **Je ne conclus pas** qu'elle n'affiche jamais de
  graphique — elle est pilotée à la demande ; ce qui est mesuré, c'est qu'**au
  chargement elle ne porte ni moteur de graphique ni contrat d'explication**.
  **Une confirmation, pas une trouvaille** : « moyenne réelle des verdicts résolus
  (n≥5) » est le **dossier 417**, désormais **confirmé servi sur `/journal`**.
  **Six instruments, six contrôles, et une mesure abandonnée** : je voulais
  mesurer la couverture du **contrat de carte** — v1 plafond `len(opts)>6000`
  (`/opportunities` 0 alors que le comptage littéral en trouve 7) · v2 JS de page
  non rattaché · v3 **`VC.card(...)`, un alias local — 4ᵉ récidive de « compter
  sans les enveloppes »** (409, 413, 414) · v4 la carte est rendue **par un
  builder** qui reçoit `question:` de son appelant. **La métrique elle-même est
  mal définie : aucun taux de couverture n'est annoncé.** Quatrième contrôle
  « invraisemblance » de la boucle — **il a mordu quatre fois sur quatre**.
  **Aucun défaut nouveau** : trois faits mesurés et un aveu ; `/analysis` reste
  une **piste**, pas un constat. **Portée** : littéraux de 10 à 200 caractères
  seulement, **phrases dynamiques toujours hors recensement** ; les 35
  affirmations de `/options` **recensées, non vérifiées** ; `/analysis` **non
  ouverte avec un symbole**. **Le compte des instruments fautifs atteint QUATORZE
  en six lots** (430, 434 ×2, 435, 437 ×3, 438 ×3, 439 ×4), tous arrêtés avant
  publication — **statistique la plus utile de la tranche : la boucle passe
  désormais plus d'effort à vérifier ses instruments qu'à mesurer le produit**, et
  le bilan n°13 devra la regarder en face. MD5 des 8 pages remesurés : **8/8
  identiques**. Aucun fichier touché, aucun bump, SW `td-shell-v187`. Suite
  **2864 passed / 0 skipped**.
  Rapport : `docs/refactor/validation/SKYLER-LOT-439.md`.

- **Lot 438 — livré** : **six contrats rompus, six faux positifs — trois objets
  différents s'appellent `scan`, et `cal.ts` reste seul.** Vingt et unième lot,
  **bornage du 437**. **Instrument** : la question du 437 inversée — pour chaque
  route à receveur **distinctif**, comparer les champs LUS aux champs SERVIS.

  ```text
  /api/command  cmd       2/10   aucun absent
  /scan         scan     18/24   SIX absents
  /cal-feed     cal       3/3    ts          ← témoin positif (trouvaille du 437)
  diagnostics   diag      4/5    aucun
  positions     posState  0/4    aucun
  ```

  **Les six sont faux. Tous les six.** Cause unique : **trois objets différents
  s'appellent `scan`** — `last_scan_ts`, `options_source`, `source` sont à
  **`diag.scan`** ; `symbols` est à **`st.scan`** (`/api/system-status`) ;
  `market` et `scan_ts` sont écrits dans `scan_state` (`terminal.py:520/522`,
  `:615/617`) et manquent **parce qu'aucun scan n'a tourné**. Et
  `system_page.py` écrit en toutes lettres le repli du seul cas ambigu :
  `if(_sym==null&&diag&&diag.scan)_sym=diag.scan.rows;` — **le code avait prévu
  l'absence, mon détecteur ne savait pas de quel `scan` il parlait**. Le piège de
  l'**état unique**, répété depuis le 425, m'a eu quand même. **Résultat : sur le
  périmètre mesurable, `cal.ts` reste le SEUL contrat rompu** — la veine du 437 ne
  s'étend pas. **Bornage négatif**, et utile : il empêche de transformer une
  trouvaille isolée en motif d'architecture sur la foi d'un compteur.
  **Une hypothèse, marquée comme telle** : `/api/system-status` émet bien un `ts`
  que `system_page.py` lit correctement ; il est **plausible** que le `cal.ts` du
  437 soit cette forme recopiée — **non testé** (règle 421). **Ce que le lot dit
  de l'instrument** : **dix lignes propres et fausses en cinq lots** (430,
  434 ×2, 435, 437 ×3, 438 ×3) ; cause nouvelle — une **collision de noms entre
  payloads**, qu'un instrument indexant par nom d'identifiant ne peut pas séparer.
  Ce qui les a arrêtées : **l'invraisemblance** (règle 414, 3ᵉ application, juste
  la 3ᵉ fois). **Aucun défaut nouveau, rien à classer.** **Portée** : 5 routes sur
  8, les trois à receveur d'une lettre **hors d'atteinte** ; champs de **premier
  niveau** seulement — un contrat rompu sur un sous-objet échappe et **n'a pas été
  quantifié** ; mesure sur le scan vide du démarrage. MD5 des 8 pages remesurés :
  **8/8 identiques**. Aucun fichier touché, aucun bump, SW `td-shell-v187`. Suite
  **2864 passed / 0 skipped**.
  Rapport : `docs/refactor/validation/SKYLER-LOT-438.md`.

- **Lot 437 — livré** : **le test de consommation ne se généralise pas (trois
  instruments, trois contrôles) — mais il a trouvé une carte qui se déclare
  fraîche « à l'instant », toujours.** Vingtième lot, **bornage du 436**.
  **Trois instruments, trois contrôles qui mordent** : **passe 1** (`.champ` sur
  tout le corpus) → 86 % de champs lus, **propre, aligné et FAUX** — le **témoin
  positif** annonçait `/api/command` 5/10 alors que le 436 avait établi 2/10 ;
  **passe 2** (`ident.champ`, `ident` recevant la réponse) → témoin **retombe
  juste**, mais `/api/positions/state` à **0/4** est invraisemblable (*un pool qui
  mord sur un objet sain accuse l'instrument*, 414) ; **passe 3** (payloads
  transmis **en bloc**) → trouve le vrai cas `actionListHtml(posState)` **et une
  bouillie** (`Bo`, `Number`, `fillText`), les receveurs d'une ou deux lettres
  étant indistinguables du Chart.js minifié.

  ```text
  /api/command             2/10   CONCLUANT      /api/positions/state  INCONCLUANT
  /api/system/diagnostics  4/5    CONCLUANT      /scan          12/24   BORNE BASSE
  /cal-feed                2/3    CONCLUANT      summary · regime · sweep  INUTILISABLES
  ```

  **3 routes sur 8 concluantes** ; `/api/command` à **20 %** se détache de
  `/api/system/diagnostics` (80 %) et `/cal-feed` (67 %). **Le 436 n'est pas
  généralisé, il est indiqué** — la méthode ne se déploie pas à coût constant.
  **La trouvaille, sortie du bornage** : `/cal-feed` sert `items`, `macro`,
  `updated` ; le client lit `timestamp: cal.ts || Date.now()` — **et `cal.ts`
  n'existe pas**. Le repli s'applique **toujours**, et `VX.updateIndicator` rend
  `VX.fmt.ago(ts)` : **la carte « Catalyseurs imminents » annonce en permanence
  que ses données datent de l'instant présent**, sur **trois pages**. **Le contrat
  n'a jamais existé des deux côtés** : `cal_state['updated']` est une **chaîne
  d'affichage** (`strftime('%H:%M %d/%m')`), inexploitable par un `ago()` — le
  serveur émet un libellé, le client attend un horodatage. **Rang 1** :
  affirmation de fraîcheur, affichée, toujours fausse, et penchant du côté qui
  **rassure**. **Aucun gardien.** **Aucun GO.** **Portée** : 5 routes sur 8 non
  conclues et **non comptées** ; le taux de 51 % de la passe 2 est **une borne
  basse contaminée, non publiée comme chiffre** ; carte non observée en
  navigateur. **Sept instruments fautifs en quatre lots** (430, 434 ×2, 435,
  437 ×3) — ici **les trois ont été arrêtés par leurs propres contrôles avant
  d'entrer dans le rapport**. MD5 des 8 pages remesurés : **8/8 identiques**.
  Aucun fichier touché, aucun bump, SW `td-shell-v187`. Suite **2864 passed / 0
  skipped**. Rapport : `docs/refactor/validation/SKYLER-LOT-437.md`.

- **Lot 436 — livré** : **`/api/command` sert dix champs, le produit en lit deux —
  95 % du payload ne va nulle part, et la suite en défend une partie.**
  Dix-neuvième lot de la veine. **Leçon du 435 appliquée d'abord** : la
  consommation avant le contenu, et **comptage littéral avant tout regex**.
  **Mesure**, accès `X.champ` dans les 3 829 722 octets servis :

  ```text
  top_stocks 12 LU · alerts 4 LU
  counts · decision · exposure · portfolio_score · regime · risk ·
  top_options · validation           →  0 accès, JAMAIS LUS
  → 2 champs sur 10 lus, 8 calculés/sérialisés/envoyés et jamais lus
  ```

  **Témoin positif** : l'instrument détecte les deux champs dont la lecture était
  établie au 435. **Durcissement** : déstructuration **0**, accès par crochet **6
  formes** (carte d'échappement + internes Chart.js), itération **2** (Chart.js +
  `/api/system/config`) → **rien n'échappe**. **Le poids** : 628 octets sur scan
  vide, **596 jamais lus (95 %)** ; et `risk` déclenche `portfolio_risk.build`
  (`:105`), `validation` déclenche `validator.build` (`:117`) — **deux moteurs
  tournent à chaque appel pour un résultat que personne ne lit**.
  **`exposure` n'est même pas un calcul** : `command.py:123` porte
  `{'actions':'70-90%','options':'10-20%','etf':'tampon / cash'}`, **un littéral
  inline**, invariant. Ma présomption d'entrée était **juste sur le fond et trop
  généreuse sur la forme** : pas un calcul discutable, une **constante** — et
  personne ne la lit. **Rang 4.** **Le point à signaler : la suite défend
  l'inutilisé** — `tests/test_command_routes.py:39`, `:47`, `:68` portent **trois
  assertions sur deux champs qu'aucun consommateur servi ne lit**. Ce n'est pas un
  gardien faux : c'est un gardien dont le **périmètre est AU-DELÀ du produit**,
  l'inverse du motif habituel (381/414/415). **Rang 3** : aucun mensonge à
  l'écran — c'est le problème, **rien n'atteint l'écran** ; ce qui reste est du
  **poids mort servi**. Correction pressentie : **décision de produit**, pas
  correction de deux lignes. **Aucun GO.** **Portée** : mesure sur les **octets
  servis uniquement** — un consommateur externe échapperait à l'instrument ; je
  considère la mesure représentative mais **c'est une appréciation, pas une
  preuve** ; le poids est mesuré sur le scan vide, **le rapport 2/10 ne dépend pas
  de l'état** ; le coût des deux moteurs est **constaté par lecture, pas
  chronométré**. **Deux lots de suite qui descendent leur propre trouvaille** —
  `/api/command` est une route dont le produit a cessé de se servir sans que
  personne l'écrive. MD5 des 8 pages remesurés : **8/8 identiques**. Aucun fichier
  touché, aucun bump, SW `td-shell-v187`. Suite **2864 passed / 0 skipped**.
  Rapport : `docs/refactor/validation/SKYLER-LOT-436.md`.

- **Lot 435 — livré** : **la décision du jour est calculée sur zéro titre, et
  personne ne la lit — je referme le point laissé « non conclu » au 434.**
  Dix-huitième lot de la veine. **Ce que `/api/command` rend quand rien n'a été
  scanné** (appel réel via `test_client`, lecture seule) :

  ```text
  top_stocks   []
  decision     {'action': 'ATTENDRE / SÉLECTIF',
                'msg': "Peu d'avantage statistique — n'acheter que l'exceptionnel, garder du cash."}
  risk         {'n': 0, 'note': 'panier trop petit pour une analyse de corrélation'}
  validation   {'ok': False, 'note': 'historique trop court pour valider'}
  ```

  **Trois champs, trois attitudes** : `risk` et `validation` **avouent** manquer
  de matière, chacun avec sa phrase écrite exprès ; `decision` **tranche** — une
  affirmation sur l'avantage statistique du marché produite à partir de **zéro
  observation**. `command.py:93-104` : scan vide → `n_act=0`, `score=None` → le
  `else` final ; **aucune branche « je ne peux pas décider »**, alors que les deux
  champs voisins en ont une. **Mais est-ce affiché ? — et la réponse renverse le
  lot** : « ATTENDRE / SÉLECTIF », « ATTAQUER », « RÉDUIRE / DÉFENSIF » et « Peu
  d'avantage statistique » → **aucun octet servi** ; `/api/command` est appelé
  depuis `/` sur **4 sites** qui lisent `cmd.top_stocks` et `cmd.alerts`, et
  **« decision » est absent de `paint`**. **Le champ n'est lu par aucun
  consommateur servi** — calculé, sérialisé, envoyé, **jamais rendu**. **Rang 4**,
  règle 411/424 appliquée contre moi-même sur la phrase la plus spectaculaire
  trouvée depuis plusieurs lots. **La question du 434 est refermée** : « Aucune
  opportunité retenue par le comité. » est rendue quand `top_stocks` est vide,
  donc **aussi sans scan** ; le voisinage de la carte ne porte **aucun compte de
  titres scannés** → **pas d'atténuation**, mais la phrase ne prétend pas qu'une
  détection a eu lieu → **rang 2**. **Un troisième instrument fautif en deux lots,
  et je le dis** : ma première mesure a rendu « 0 appel à `/api/command` » — faux,
  il y en a **16** ; cause, un motif `.{170}` **sans `DOTALL`**. Et **une fois de
  plus le faux résultat allait dans le sens de ma thèse**. **Aucun gardien.**
  **Aucun GO.** **Portée** : 39 des 47 phrases non vérifiées ; **un seul champ**
  de `/api/command` ouvert (`counts`, `exposure`, `regime`, `portfolio_score`,
  `alerts` servis et non vérifiés) ; la bascule vers `ATTAQUER` est **lue dans le
  code, pas exécutée**. MD5 des 8 pages remesurés : **8/8 identiques**. Aucun
  fichier touché, aucun bump, SW `td-shell-v187`. Suite **2864 passed / 0
  skipped**. Rapport : `docs/refactor/validation/SKYLER-LOT-435.md`.

- **Lot 434 — livré** : **« Aucune anomalie détectée sur le scan courant » quand
  il n'y a pas de scan — et la garde correcte est vingt lignes plus haut, dans le
  même fichier.** Dix-septième lot de la veine. Le 433 avait laissé 43 des 47
  phrases rassurantes non vérifiées ; ce lot ouvre les candidates nommées.
  **Un instrument écarté, et je le dis** : deux versions d'un détecteur de garde
  ont rendu des lignes **propres, alignées et fausses** — la première cherchait la
  garde dans **toute la page** au lieu de **la fonction**, la seconde remontait à
  la **mauvaise fonction englobante**. **Les deux confirmaient commodément ce que
  j'attendais.** Balayage jeté, mesure par **exécution**.
  **Mesure** (`renderAnomalies`, 3 523 o extraits du marquage servi, Node 22) :

  ```text
  3 titres, 2 anomalies              → tableau des anomalies          ← témoin positif
  2 titres RÉELS, aucune anomalie    → « Aucune anomalie action…»     ← phrase LÉGITIME
  AUCUN SCAN (rows vide)             → MÊME PHRASE
  /scan indisponible                 → idem
  ```

  **Trois états distincts, une seule phrase** — qui affirme qu'une **détection** a
  eu lieu et qu'il existe un **scan courant**. **La garde correcte est dans le même
  fichier** : `renderRadar` (7 652 o, même page, même source) porte
  `if(!rows.length){ … 'Aucun titre scanné — lancer un scan depuis Système.'; return; }`.
  Mesuré par extraction : garde **présente dans `renderRadar`, absente de
  `renderAnomalies`**. Ce n'est plus un contre-exemple sur une autre page (433) :
  **même fichier, même page, même donnée.** **Conséquence de bord qui réduit ma
  propre liste** : la vue radar étant protégée, « Aucune asymétrie exceptionnelle
  détectée » et « Aucun candidat en zone actionnable » sont **inatteignables sans
  scan** → **elles sortent du dossier**. **Un troisième comportement nuance** :
  `moversRows` (`/markets`) n'a pas de garde, mais son appelant affiche
  `${rows.length} titres scannés` **juste en dessous** — la confusion est dans la
  phrase, l'information honnête est **à côté** ; la vue anomalies, elle, n'affiche
  **aucun compte**. **Trois comportements sur la même donnée** : garde explicite ✓ ·
  pas de garde mais compte affiché ~ · pas de garde, aucun compte **✗**.
  **Autres candidates** : « Aucune alerte active » → données utilisateur, honnête ·
  « Aucun catalyseur imminent identifié » → `catch` distinct pour l'échec, honnête ·
  « Aucune opportunité retenue par le comité » → **non conclu, non compté**.
  **Rang 1**, famille 432/433, moins lourd (une carte, vue secondaire) mais **même
  sens : elle rassure**. Correction pressentie **déjà écrite vingt lignes plus
  haut**. **Aucun gardien.** **Aucun GO.** **Portée** : 7 candidates sur 47, **40
  non vérifiées** ; sur les 7 → **1 défaut, 1 atténuée, 2 retirées, 2 honnêtes, 1
  non conclue** ; application sans scan **non observée** en navigateur. **Bornage
  qui TRIE** — ni « exception » ni « motif de page » : la famille du 432 existe mais
  est **moins large que ce que le 433 pouvait laisser croire**. MD5 des 8 pages
  remesurés : **8/8 identiques**. Aucun fichier touché, aucun bump, SW
  `td-shell-v187`. Suite **2864 passed / 0 skipped**.
  Rapport : `docs/refactor/validation/SKYLER-LOT-434.md`.

- **Lot 433 — livré** : **le portefeuille calcule `allMarked`, s'en sert pour une
  classe CSS, et l'ignore dans les trois phrases qui rassurent.** Seizième lot de
  la veine, **bornage du 432**. **Pool** : sur le corpus servi, les littéraux
  commençant par *Aucun/Aucune/Rien/Pas de/Tout* → **47 phrases rassurantes**. La
  majorité décrit une **absence d'entrée** (honnête par construction) ; la classe
  dangereuse affirme une **absence de problème** après une évaluation qui n'a
  peut-être pas eu lieu — **trois vivent sur `/portfolio`**.
  **Mesure par exécution des octets servis** (Node 22) :

  ```text
  cas                        allMarked   risque dominant                     liste de décision
  TÉMOIN POSITIF, 1 cassée     true      « 1 position(s) sous invalidation » 1 position(s)
  4 positions SANS marque      false     « Aucun risque critique détecté —   « Aucune position urgente —
                                           concentration et invalidations      toutes les thèses sont intactes
                                           dans les repères »                  ou en surveillance normale. »
  1 seule position, sans marque false     « Concentration élevée : 100 % »   idem
  ```

  Le troisième cas **nuance mon propre constat** : la branche « concentration »
  mord quand même (les poids se replient sur le coût investi) — seule la partie
  « invalidations » est aveugle. **Ce qui rend ce lot différent du 432 :
  l'information EXISTE, calculée, à portée.** `computeMetrics` (`:197`, servi)
  calcule `allMarked` ; mesuré, elle apparaît **cinq fois** dans les octets
  servis — elle conditionne `plAbs`, elle est exportée dans `m`, elle pose **une
  classe `vx-warn`**, elle garde une écriture `localStorage` — **et elle ne
  conditionne aucune des trois phrases**, alors que `m` est le second argument de
  `dominantRisk`. Le fichier sait dire « je n'ai pas toutes les marques » : **il
  le dit avec une couleur, jamais avec une phrase.** **Contre-exemple mesuré** :
  `/system` distingue « Aucun titre scanné — **la qualité ne peut pas être
  mesurée** » de « Aucun titre en qualité dégradée — rien à signaler ». **Le dépôt
  sait faire la différence, et il l'écrit — sur une autre page.** **Compte du
  bornage** : 47 phrases · **3 ouvertes, toutes sur `/portfolio`** (`dominantRisk`,
  liste de décision, `priorityAction` du 432) · 1 contre-exemple · **43 non
  ouvertes**. **Le défaut du 432 n'était pas isolé : c'est un motif de page** — les
  trois synthèses tombent ensemble, sur le même déclencheur, et **aucun test ne
  mentionne `dominantRisk`**. **Rang 1**, identique au 432, mais conséquence plus
  lourde : les trois phrases occupent le **haut de la page** et disent la même
  chose **en chœur**. Correction pressentie, déjà écrite ailleurs dans le fichier :
  conditionner à `m.allMarked`. **Aucun GO.** **Portée** : 43 des 47 phrases non
  ouvertes, classées par leur **forme** et non vérifiées ; une phrase rassurante
  **construite dynamiquement** échappe toujours au recensement ; portefeuille réel
  sans cotations **non observé**. **Première fois qu'un bornage AGGRAVE** — les
  précédents disaient « exception, pas symptôme » (426, 429) ou levaient une
  alerte (431). MD5 des 8 pages remesurés : **8/8 identiques**. Aucun fichier
  touché, aucun bump, SW `td-shell-v187`. Suite **2864 passed / 0 skipped**.
  Rapport : `docs/refactor/validation/SKYLER-LOT-433.md`.

- **Lot 432 — livré** : **« Aucune décision urgente — laisser courir les thèses
  intactes », dit la carte, alors que le moteur vient de classer chaque position
  « Données insuffisantes ».** Quinzième lot de la veine. Point de contrôle : la
  **seconde piste ouverte au 429**, la lecture par **table `{…}[champ]`**, avec la
  bonne question — *le repli implicite est-il honnête ou invente-t-il ?*
  **Pool apparié** (accolades ET crochets, leçon 415) : **19 lectures** → 4 cartes
  d'échappement HTML, 2 internes Chart.js, **13 tables produit**. Classées par ce
  que leur repli **fait** : **9 honnêtes** (`d.bias`→`'—'`, `_ib`→`['IBKR état
  inconnu']`, `mode`→`''`, `t`→`'vx-muted'`, `st2.status`→`'frozen'`…), 3 sans
  objet, **1 qui range l'inconnu avec le sain**. **12 sur 13 sont honnêtes.**
  **La trouvaille** : `/portfolio`, `priorityAction` —

  ```javascript
  const rank = {cassee:3, fragilisee:2, surveiller:0,
                insuffisant:0, intacte:0, renforcee:0}[st.key] || 0;
  … .filter(x => x.rank > 0)
  ```

  **Le repli `|| 0` est inatteignable** (`thesisState` produit exactement six
  clés, la table les liste toutes) : **le défaut n'est pas une clé manquante,
  c'est la VALEUR donnée à `insuffisant`** — une position « Données
  insuffisantes » n'est pas classée bas, elle est **retirée du tri**.
  **Mesure par exécution des octets servis** (Node 22) :

  ```text
  témoin positif — 1 thèse cassée        → « AAA — Réévaluer la sortie, invalidation atteinte »
  4 positions SANS marque (IBKR off)     → « Aucune décision urgente — laisser courir les thèses INTACTES »
  3 sans marque + 1 réellement intacte   → idem
  ```

  **La règle est écrite trois lignes plus haut** : docstring de `thesisState`
  (`portfolio_page.py:130`) — *« Sans marque → « données insuffisantes » (jamais
  un verdict) »*. La couche d'état la tient ; la couche d'action la casse et
  prononce **exactement** le verdict interdit, en le nommant. Huitième instance du
  motif, et parente directe du 424 — mais cette fois **du côté affiché**.
  **Atteignable et pas au bord** : le producteur des cotations est un
  `try { fetch('/api/pos-quotes') } catch(e) { return {}; }` — un échec rend un
  objet vide, **aucune position n'a de marque**. **Prouvé affiché** : la carte
  « Action prioritaire » est rendue dans le marquage servi, `${esc(act.label)}`
  sans condition. **Rang 1** : aucune valeur n'est inventée, les états sont
  corrects un par un — c'est la **synthèse** qui est fausse, et dans le sens le
  plus coûteux : elle **rassure** quand elle devrait dire qu'elle ne sait pas.
  Correction pressentie : compter les `insuffisant` et rendre un libellé qui
  l'avoue. **Aucun gardien** ne mentionne `priorityAction`. **Aucun GO.**
  **Portée** : 13 tables ouvertes sur 19, les 6 autres écartées **par rôle** ; un
  `switch`/`case` échappe toujours ; portefeuille réel sans cotations **non
  observé**. **Leçon de rang** : le 431 avait annulé son rang 1 parce que
  l'étiquette était **conservatrice** ; ici elle **rassure** — même forme, sens
  inverse, **c'est le sens de l'erreur qui décide du rang**. MD5 des 8 pages
  remesurés : **8/8 identiques**. Aucun fichier touché, aucun bump, SW
  `td-shell-v187`. Suite **2864 passed / 0 skipped**.
  Rapport : `docs/refactor/validation/SKYLER-LOT-432.md`.

- **Lot 431 — livré** : **`modeOf` ne peut jamais rendre « Live » — le jeton
  `ibkr` n'existe nulle part dans le vocabulaire qu'il interroge, et j'annule mon
  propre rang 1.** Quatorzième lot de la veine, premier après le bilan n°12.
  Point de contrôle : la **piste ouverte au 429 et jamais consommée**, les
  vocabulaires en **minuscules**. **Pool trié par RÔLE** (leçon 419) sur le
  corpus servi : **53 porteurs · 119 couples** → **22 vocabulaires** (≥ 2 jetons)
  et **31 drapeaux** écartés d'emblée. **Alerte la plus prometteuse, levée par la
  chaîne** : `bias` comparé à `haussier`, `baissier` **et** `bearish` — forme
  exacte du 428 — mais ce sont **deux champs distincts**
  (`options-gex.js:139` ← `gex_scan.py:45` ; `options-structure.js:109` ←
  `multileg_lab.py:421`). **Troisième alerte levée** après 426 et 429.
  **La trouvaille** : `/markets`, octets servis —

  ```javascript
  function modeOf(scan){ return scan.data_source==='demo' ? 'fallback'
                       : (scan.source==='ibkr' ? 'live' : 'delayed'); }
  ```

  or `terminal.py:352`/`:373` ne produit que **quatre valeurs — `yfinance`,
  `stooq`, `yfinance+stooq`, `demo` — jamais `ibkr`** (même champ servi par
  `/healthz`). **Mesure par exécution des octets servis** : les quatre valeurs
  réelles rendent `delayed`/`fallback` ; **témoin positif `ibkr` → `live`**, la
  branche existe et fonctionne. Libellés de `vx-core.js` :
  `{live:'Live',delayed:'Différé',fallback:'Secours'}`. **Une des trois issues est
  inatteignable, et c'est « Live »** ; **16 cartes** de `markets_page.py` passent
  `mode:modeOf(scan)`. **Périmètre — le contrôle qui empêche de surestimer** :
  deux autres sites portent la même comparaison (`gnavFresh` « 🟢 LIVE IBKR »,
  `_srcb` « 🟢 IBKR live ») et **aucun n'est servi** (constantes `PAGE_*` mortes,
  dossier 374). **J'annule mon propre rang 1** : le libellé rendu n'est **pas
  faux** — `scan_state['source']` décrit la provenance des **séries de cours**,
  qui viennent réellement de yfinance/stooq. Restent : **(a)** une **branche
  morte** (rang 4, aucune conséquence à l'écran) ; **(b)** une **sous-estimation**
  — quand IBKR est connecté, `_apply_ibkr_indices()` écrase les prix des indices
  en place et le pied de carte annonce quand même « Différé » : l'étiquette est
  **conservatrice**, et l'invariant interdit d'annoncer MIEUX, pas moins.
  **Recoupement du dossier 386**, deuxième porte : 386 = champ jamais lu ; ici =
  champ lu, comparé **au mauvais niveau** (`scan.source` au lieu de
  `scan.indices_live.source`, écrit juste à côté en `terminal.py:2257`).
  **Verdict négatif au sens du produit**, rang 4. **Aucun GO.** **Portée** : 1
  porteur ouvert sur 22, **21 non confrontés** ; les 15 porteurs lus par table
  `{…}[champ]` toujours pas ouverts ; IBKR **non observé**, la sous-estimation est
  établie par lecture de la chaîne. **MD5 des 8 pages REMESURÉS : 8/8 identiques**
  aux références des lots 390/396 — **l'inférence devient une mesure**. Aucun
  fichier touché, aucun bump, SW `td-shell-v187`. Suite **2864 passed / 0
  skipped**. Rapport : `docs/refactor/validation/SKYLER-LOT-431.md`.

- **Lot 430 — livré** : **BILAN n°12 (tranche 420 → 429)** — voir le bilan en
  tête de ce fichier. Mesures du bilan : `0676d78..1ac8446` → **10 commits, 12
  fichiers, tous sous `docs/`, +2 231 / −0 lignes, 0 fichier de production** ;
  10/10 rapports, 10/10 lignes d'index, 78 145 octets. **Correction publiée** :
  la phrase « la production n'a pas bougé depuis le lot 399 » est vraie sur le
  fond mais fausse à la lettre — 1 fichier hors `docs/` a changé
  (`tests/test_skyler_sweep_x1.py`, lot 401), 0 fichier de production ; et ma
  **première commande de vérification était fausse** (variable de base vide,
  `git diff ..HEAD` comparant la tête à elle-même), refaite avec le commit
  résolu. Bilan des dix lots : **4 trouvailles de rang 1** (422, 425, 427, 428),
  1 de rang 2, 1 de rang 4, 3 bornages négatifs, 1 hypothèse réfutée. Trois
  acquis de méthode : partir de l'écran, exécuter les octets servis, le
  recensement lui-même peut être la limite. Classement coût/risque des rang 1 les
  moins chers publié — les trois premiers touchent le même fichier et aucun
  moteur. **Aucun GO demandé.** Aucun fichier de production touché, aucun bump,
  SW `td-shell-v187`. Suite **2864 passed / 0 skipped**.
  Rapport : `docs/refactor/validation/SKYLER-LOT-430.md`.

- **Lot 429 — livré** : **trois vocabulaires de décision coexistent
  légitimement — 13 porteurs sur 14 prennent le bon, un seul se trompe.**
  Treizième lot de la veine, **bornage du 428**, dernier lot de mesure de la
  tranche. **Instrument** : sur le corpus **servi** (95 objets, 3 829 722 o),
  toute comparaison d'un porteur à un **jeton de vocabulaire** (littéral
  MAJUSCULE). Le premier passage ne connaissait qu'une forme
  (`.champ === 'JETON'`) et **manquait `u !== 'ÉVITER'`, la moitié même du défaut
  du 428** — un second passage a été ajouté pour les **identifiants nus**
  (leçon 414). **27 + 17 = 44 couples · 18 porteurs.** Témoin positif : les deux
  moitiés du défaut du 428 apparaissent bien. **Découverte structurelle** : le
  dépôt n'a pas un vocabulaire de décision, il en a **trois**, tous légitimes —

  ```text
  lignes du scan     BUY · WATCH · WAIT · AVOID                strategy/config.py:51
  comité             ACHETER · RENFORCER · ATTENDRE · ÉVITER   engines/committee.py
  Skyler canonique   ACHETER · ATTENDRE · REFUSER              engines/skyler_core.py
  ```

  **Le défaut du 428 se re-décrit plus précisément** : ce n'est pas « du français
  contre de l'anglais », c'est **le vocabulaire du COMITÉ appliqué aux lignes du
  SCAN**. **Confrontation porteur par porteur**, chacun remonté à son producteur :
  `name` VIX/WTI, `verdict`/`v` (accepte les deux), `x = r.decision`
  (`skyler_core`, 2 jetons morts), `type`/`typ`/`kind`, `result` WIN/LOSS
  (`<option value>` servi), `status` ANOMALIES / MESURE / MISSING-OK, `state`
  ACTIVE/DISABLED, `label` HOSTILE/PORTEUR, `level` ACTIONABLE, `regime`
  UNKNOWN, `spy_regime` TREND → **14 confrontés · 13 exacts · 1 défectueux**
  (celui du 428). **Deux résultats fins** : **(a) une alerte LEVÉE par la
  chaîne** — `regime_engine` n'émet jamais `'TREND'` tout court, mais
  `spy_regime` a un **autre producteur** (`market/context.py:46` →
  TREND/CHOP/NEUTRAL) : deux champs, deux vocabulaires, chaque consommateur prend
  le bon ; **(b) un producteur plus riche que son consommateur, correctement
  traité** — `tradingview_signal_store` émet trois états, `system_page.py:538-540`
  les traite **tous les trois** par table avec repli : **le contre-exemple exact
  du 428**. **Ce qui échappe encore, quantifié** : jetons **minuscules**
  (44 couples · 27 porteurs) et lecture par **table `{…}[champ]`** (15 porteurs),
  **non confrontés** — le « 13 sur 14 » vaut pour les vocabulaires MAJUSCULES
  comparés explicitement, pas pour tout le dépôt. **Verdict : négatif, et c'est le
  bon résultat** — le défaut du 428 est une **exception**, pas un symptôme ; le
  bornage **renforce** le 428 : un seul site se trompe, et c'est celui qui
  affiche au trader comment interpréter son propre résultat. **Portée** : aucune
  exécution, aucune valeur calculée ni observée sur données réelles ;
  producteurs identifiés par lecture des énumérations, moteurs non exécutés.
  Runtime : 3 fichiers ré-horodatés **restaurés à l'octet près et revérifiés**,
  écart aucun. Aucun fichier touché, aucun bump, SW `td-shell-v187`. Suite
  **2864 passed / 0 skipped**.
  Rapport : `docs/refactor/validation/SKYLER-LOT-429.md`.

- **Lot 428 — livré** : **l'entonnoir du scan est plat par construction — il
  cherche des verdicts en français dans un moteur qui répond en anglais.**
  Douzième lot de la veine, quatrième mené depuis l'écran. **Affirmation
  ouverte, et elle est exacte** : `explain.shows:'Le décompte des verdicts
  moteur sur l'univers scanné (max 5 catégories)'` — le code tronque bien
  (`slice(0,5)`) et le vocabulaire moteur est **fermé à quatre valeurs**
  (`vertex/strategy/config.py:51` : BUY / WATCH / WAIT / AVOID) → **le `slice` ne
  coupe jamais : l'affirmation est vraie mais ne mord jamais**, dit tel quel.
  **Ce que la même mesure a révélé chez la voisine** : juste sous le donut,
  l'**entonnoir de sélection** —
  `isBuy = v=>['ACHETER','RENFORCER'].includes(v.toUpperCase())` et
  `isAct = v=>u && u!=='ÉVITER' && u!=='EVITER'`. **Les deux prédicats
  interrogent un vocabulaire FRANÇAIS ; le champ `verdict` des lignes du scan ne
  contient que de l'ANGLAIS.** Le repli `|| r.decision` ne rattrape rien (clé
  française portée par `recs`, `terminal.py:596`, pas par les `rows` du `/scan`,
  `:412`). **Mesure par exécution des octets servis** (bloc de 1 148 o, Node 22,
  `VXCharts.funnel` stubé) :

  ```text
  30 BUY · 20 WATCH · 10 AVOID     60 → 60 → 60 → 0
   2 BUY ·  8 WATCH · 50 AVOID     60 → 60 → 60 → 0
  100 % AVOID                      60 → 60 → 60 → 0
  TÉMOIN vocabulaire français      60 → 60 → 50 → 30
  ```

  **Le marché le plus porteur et l'univers entièrement rejeté produisent le même
  entonnoir** ; le témoin positif prouve que la logique fonctionne — c'est le
  vocabulaire qui ne se rencontre pas. Trois étages sur quatre sont constants.
  **Ce qui fait basculer le lot au rang 1 — la phrase rendue** : dans le marquage
  servi de `/markets?view=breadth`, sous l'entonnoir, *« Chaque étape resserre
  l'univers scanné jusqu'aux verdicts d'achat du comité. Aucune idée n'est
  forcée : un entonnoir plat = marché hostile. »* — **la phrase donne la clé de
  lecture d'un entonnoir plat, et l'entonnoir est plat par construction,
  toujours** : un décalage de vocabulaire présenté comme un signal de marché.
  Conteneur présent dans **1 vue sur les 8 mesurées**. **Bornage sur les octets
  servis** : `/opportunities` accepte les **deux** vocabulaires sur le même champ
  (3 fragments) — **le dépôt sait que le champ peut porter les deux** ;
  `/markets` est le seul site servi qui n'accepte que le français → **1
  défectueux sur 2**. `analysis_page.py:524` porte un regex acceptant les deux,
  mais **cette chaîne n'apparaît dans aucun octet servi** — mesuré, non
  interprété. **Le gardien existe et il est vert** :
  `tests/test_cockpit.py::test_breadth_selection_funnel_real_data` — son **nom**
  promet « alimenté par les données réelles du scan », ses **assertions**
  vérifient la présence de 4 chaînes dans le source ; il n'exerce **pas une seule
  ligne de scan** (motif des 416/417). **Ce que je n'ai pas observé** : scan vide
  au démarrage, aucun payload persisté avec `rows` — **pas d'entonnoir plat
  constaté sur un scan réel** ; vocabulaire lu dans la source de vérité et
  corroboré par 3 autres consommateurs (`terminal.py:445`, `:1460-1462`,
  `:5512`). **Rang 1**, famille des 422/425/427 : les valeurs du scan sont
  réelles, ce sont les **comptes dérivés** qui sont faux — « Achats » vaut 0 en
  permanence, « Dossiers actionnables » compte les titres rejetés. Correction
  pressentie : accepter les deux vocabulaires comme le fait déjà
  `/opportunities`. **Aucun GO.** **Portée** : 2 affirmations ouvertes sur 118,
  116 non vérifiées ; la phrase d'aide a été trouvée par **voisinage**, pas par le
  recensement ; `VXCharts.funnel` stubé, rendu SVG non exécuté. Runtime :
  snapshot **avec copie du contenu**, 3 fichiers ré-horodatés **restaurés à
  l'octet près et revérifiés** — écart final aucun. Aucun fichier touché, aucun
  bump, SW `td-shell-v187`. Suite **2864 passed / 0 skipped**.
  Rapport : `docs/refactor/validation/SKYLER-LOT-428.md`.

- **Lot 427 — livré** : **la légende annonce quatre indices, le graphique en
  trace trois — les couleurs glissent d'un cran.** Onzième lot de la veine,
  troisième mené **depuis l'écran**. Le 426 avait conclu que le vivier était
  quasi épuisé ; la consigne était de **l'élargir**. **Recensement élargi, même
  corpus servi** (52 pages et vues, 43 fichiers `/static`, 3 829 722 octets) : le
  filtre du 425 ne prenait que `limits:`/`conclusion:` de 15 à 150 caractères →
  **17** ; les huit familles donnent **118 affirmations distinctes**
  (`question` 32 · `why` 22 · `confirm` 15 · `invalidate` 15 · `shows` 14 ·
  `limits` 11 · `conclusion` 8 · `note` 1). **Le vivier était sept fois plus
  grand que ce qui avait été recensé**, dont 17 porteuses d'un chiffre.
  **Affirmation ouverte** : carte « Indices — performance comparée »
  (`/markets`, `vx-mk-multi`), `explain.shows:'Les mêmes séries d'indices que le
  bandeau, rebasées à 0 %…'` — une affirmation d'**identité** entre deux objets
  de la même page. **Mesure par EXÉCUTION des octets servis** : `loadMultiIndex`
  (1 432 o), `loadStrip`, `crossAsset`, `idxByName` extraits du **marquage
  servi** par appariement d'accolades, puis **exécutés sous Node 22** avec
  `VXCharts` stubé — ni lecture ni transcription. **Le défaut** :
  `legend: wanted.map((n,i)=>({label:n,color:series[i%6]}))` est bâti sur une
  **liste fixe de 4**, alors que les données sont
  `sets = wanted.map(…).filter(x=>x.spark.length>5)` — **filtrées** ; et
  `chart-core.js:526` colore chaque courbe par son **rang dans `sets`**.

  ```text
  nominal (4 indices)      0 courbe mal nommée   ← témoin positif
  Nasdaq absent            2
  Dow Jones absent         1
  S&P 500 absent           3
  Russell 2000 seul        1
  ```

  Cas « Nasdaq absent » : la pastille annonçant **« Nasdaq »** porte la courbe du
  **Dow Jones**, celle annonçant **« Dow Jones »** porte **Russell 2000**, et la
  légende annonce un **quatrième indice qui n'est pas tracé du tout**.
  **L'affirmation de départ est elle aussi conditionnelle** : bandeau et
  graphique n'appliquent pas le même filtre (`last != null` contre
  `spark.length > 5`) → bandeau 4 / graphique 3 puis 2. **Preuve d'affichage sur
  les octets servis** : `chart-core.js` rend `<div class="vx-chart-legend">` avec
  pastille `background:${l.color}` + libellé, et `charts.css` la rend visible.
  **Détail aggravant** : `multiLine` réactive par-dessus la légende native de
  Chart.js, construite **à partir des jeux de données** — la carte porte donc
  **deux légendes qui se contredisent**. **Ce que je n'ai pas observé, et que je
  dis** : aucun payload persisté ne contient de clé `indices`, le scan est vide
  au démarrage — **pas de graphique décalé constaté sur données réelles** ; la
  porte d'entrée est établie (`terminal.py:449-457`, `try/except: pass` par
  ticker → indice omis, mécanisme du 425). **Bornage** : 2 sites seulement
  construisent une `legend:` sur mesure dans `vertex/ui/**` — celui-ci, et la
  courbe des taux, dont les deux jeux viennent du même `pts`, jamais filtrés :
  **1 défectueux sur 2** ; **aucun test** ne mentionne `vx-mk-multi`,
  `loadMultiIndex` ni `vx-chart-legend` — **aucun gardien**. **Rang 1**, famille
  des 422/425 : les **valeurs** tracées sont réelles, c'est le **nom attaché à la
  couleur** qui devient faux, sur une carte dont le rôle est de comparer les
  indices entre eux. Correction pressentie : bâtir la légende depuis `sets` —
  corrige du même geste le décalage et l'indice fantôme. **Aucun GO.**
  **Portée** : 1 ouverte sur 118 ; le recensement reste borné aux littéraux de 10
  à 200 caractères, **les phrases dynamiques lui échappent toujours** ; Chart.js
  n'a pas été exécuté. **Runtime caractérisé au lieu d'être supposé** : suite
  lancée **deux fois** avec copie intermédiaire → `ai_enrichment.json` ne change
  que son `as_of`, `desk_data.json` que son `ts`, `weekly_snapshot.json` que son
  `generated_at` — **aucune donnée utilisateur modifiée** ; 21 fichiers runtime
  (rotation `desk_backup_*` sur 7 jours). Aucun fichier touché, aucun bump,
  SW `td-shell-v187`. Suite **2864 passed / 0 skipped**, deux fois.
  Rapport : `docs/refactor/validation/SKYLER-LOT-427.md`.

- **Lot 426 — livré** : **les affirmations de méthode confrontées à leur code —
  6 exactes sur 6, et une septième portée par une carte qui ne s'affiche
  jamais.** Dixième lot de la veine, deuxième mené **depuis l'écran**. Le 425
  avait recensé **17 affirmations littérales rendues** et n'en avait ouvert
  **qu'une** ; celui-ci en ouvre **six de plus** — les plus testables, celles qui
  énoncent une **formule** ou une **méthode**. **Aucun défaut : c'est un
  bornage.**
  ```text
  1. « σ = spot · IV_ATM · √(DTE/365) »          vol_charts.py:73    EXACTE terme pour terme
  2. « IV ATM = contrat le plus proche du spot »  vol_charts.py:52-55 EXACTE
  3. « moyenne des % par trade, pas composée »    portfolio_page:643  EXACTE
  4. « P&L latent absolu (valeur − coût) »        portfolio_page:104  EXACTE
  5. « force = score moyen · momentum = var. moy. » sectors.py:51/68  EXACTE (2 axes)
  6. « historique breadth partiel, pas tout le NYSE »                 EXACTE
  ```
  **Une vérification annexe aurait pu mordre** : le `iv / 100.0` de
  `vol_charts.py` est **inconditionnel** alors que `options_intel_api.py:105`
  normalise **conditionnellement** (`iv/100 if iv > 3`) — deux conventions pour
  le même champ. Chaîne remontée : le producteur du board écrit
  `round(float(mg.impliedVol) * 100, 1)` (`terminal.py:897`), donc **en
  pourcentage** ; la division inconditionnelle est **correcte**, et le second
  producteur est sur la même échelle. **L'alerte était légitime, la mesure l'a
  levée.**
  **La septième, seul point à signaler.** « Dérivé arithmétiquement de la courbe
  d'équité » et « dérivé de la série déclarée — pas un indicateur de marché »
  (`portfolio_page.py:616/618`) sont **justes sur le fond**. Mais le lot 406 a
  mesuré que `myTradesEquity` **n'a aucun écrivain**, et le 411 en a tiré que
  **cette carte n'est jamais rendue** : deux affirmations correctes portées par
  une carte que personne ne voit. **Recoupement du dossier 406/411, pas une
  trouvaille.**
  ```text
  affirmations littérales rendues (recensées au 425)        17
     ouvertes au 425                                         1   → FAUSSE
     ouvertes ici                                            6   → 6 EXACTES
     portée par une carte inatteignable                      1   → recoupement 406/411
     non ouvertes                                            9
  ```
  **Sur sept affirmations confrontées à leur code, six sont exactes et une est
  fausse.** Le contrat d'honnêteté des cartes tient donc largement, et le défaut
  du 425 en ressort mieux caractérisé : **une exception dans un ensemble
  rigoureux**, pas le symptôme d'un texte négligé.
  **Portée** : les neuf restantes ne sont **pas** vérifiées (conventions
  d'affichage, un conseil, périmètres déjà couverts) ; le recensement reste borné
  aux littéraux `limits:`/`conclusion:` de 15 à 150 caractères — `question:`,
  `explain.shows` et phrases dynamiques échappent et **n'ont pas été comptés** ;
  et pour la confrontation n°1 la mesure est **statique** (board vide au
  démarrage) — la formule a été comparée au **code**, pas à une sortie.
  **La méthode « partir de l'écran » reste la bonne** : une trouvaille (425) puis
  un bornage propre (426) en deux lots, là où trois lots partis du moteur
  butaient sur l'inatteignable.
  Suite **2864 passed / 0 skipped**, inchangée. **Aucun fichier touché** ; SW
  `td-shell-v187` ; écart runtime final aucun.

- **Lot 425 — livré** : **« 4 maturités réelles » — le compte est écrit en dur, la
  courbe se trace dès 2 points.** Neuvième lot de la veine, et le premier mené
  **dans l'autre sens** : partir d'une phrase **réellement rendue**, puis remonter
  au code. C'était la consigne, après trois lots dont la conséquence s'arrêtait
  avant l'écran.
  **Point de départ.** Les 8 pages et leurs scripts demandés au serveur (méthode
  du 413), puis extraction des **affirmations littérales** rendues par les cartes
  (`limits:` / `conclusion:`) → **17**, dont « σ = spot · IV_ATM · √(DTE/365) »,
  « moyenne des % par trade — pas une performance composée », « historique breadth
  de l'univers scanné (partiel) »… La seule **affirmation de compte** — donc
  vérifiable — a été ouverte.
  **Preuve d'affichage, sur les octets servis :**
  ```text
  vue          panneau statique dans le MARQUAGE   chaîne limits servie
  overview               non                              oui
  macro                  OUI                              oui
  sectors / breadth / volatility   non                    oui
  ```
  Sur `/markets?view=macro`, le marquage servi contient *« Courbe tracée sur les
  **4 maturités réelles** du scan (3M · 5A · 10A · 30A). Les maturités
  intermédiaires ne sont pas fournies par les moteurs — **non affichées plutôt
  qu'inventées**. »* Et sur **les cinq vues**, la carte porte
  `limits:'4 maturités réelles (3M/5A/10A/30A)'`. **Les deux sont des chaînes
  fixes : aucune n'est conditionnelle.**
  **Ce que le code fait réellement.** Client, `markets_page.py:584-586` : `mats`
  liste 4 tickers, `pts = mats.filter(… value != null)`, puis
  `if (pts.length < 2) { emptyCard(); return; }` — **la courbe se trace dès deux
  points**. Serveur, `terminal.py:478-480` : `if _v is None: continue` — **une
  maturité indisponible est omise du payload**. Le seuil `< 2` existe précisément
  parce que « moins de 4 » est un état prévu.
  **Une courbe tracée sur 2 ou 3 maturités porte donc, en toutes lettres,
  « 4 maturités réelles ».**
  **La règle est dans la même phrase.** Le panneau se déclare fier de « non
  affichées plutôt qu'inventées » **deux propositions plus loin** : jusqu'ici la
  bonne pratique et son oubli étaient à quelques lignes d'écart — ici ils
  partagent **la même phrase**.
  **Ce que je n'ai pas observé, et que je dis** : le payload `macro` présent au
  démarrage porte **4 maturités sur 4**. Le décalage est **démontré par
  construction, pas constaté sur des données réelles** — la différence est en
  faveur du produit.
  **Rang 1, famille du 422** : les **valeurs** affichées sont réelles, aucune
  maturité n'est inventée ; c'est le **compte** qui devient faux quand une source
  manque, dans une phrase qui se présente comme une déclaration de limites.
  Correction pressentie, minuscule : compte **dynamique** et formulation sans
  nombre fixe. **Aucun GO, rien d'engagé.**
  **Décision de veine : le critère durci du 424 est REMPLI** — la phrase a été
  extraite du **marquage servi**, pas d'un fichier source. La veine reste
  **ouverte**. Et le **changement d'ordre est validé** : partir de l'écran a
  produit en une mesure ce que trois lots partis du moteur n'avaient pas atteint.
  **Portée** : **une** affirmation ouverte sur 17 ; les seize autres sont
  **listées, non vérifiées** — notamment les deux affirmations de **méthode**. Le
  recensement ne couvre que les littéraux de 15 à 150 caractères ; une
  affirmation construite dynamiquement lui échappe.
  Suite **2864 passed / 0 skipped**, inchangée. **Aucun fichier touché** ; SW
  `td-shell-v187` ; écart runtime final aucun.

- **Lot 424 — livré** : **« Thèse INTACT, confiance 0.0 » — le titre médian reçoit
  un verdict sans une seule preuve.** Huitième lot dans la veine des moteurs,
  cible `vertex/positions/thesis_health.py`, choisi selon la consigne du 423 :
  **entrées utilisateur donc réellement variables**, et **chaîne vérifiée avant
  d'investir dans la mesure**.
  **La règle que le fichier respecte — et il la respecte beaucoup.** C'est l'un
  des modules les plus honnêtes du dépôt : compteur d'**inconnues** dimension par
  dimension, `confidence = connu / (connu + inconnues)`, docstring portant la
  correction du lot 365, et un statut `UNKNOWN` réellement utilisé.
  ```text
  thèse absente                          UNKNOWN         conf 0.0   unk 1
  thèse écrite, AUCUNE donnée            UNKNOWN         conf 0.0   unk 4
  preuves positives (fond 70, rs 65)     STRENGTHENING   conf 1.0   pos 2
  preuves négatives (fond 30, rs 20)     AT_RISK         conf 1.0   neg 2
  ```
  Quatre témoins, deux de chaque côté : **le moteur sait dire qu'il ne sait pas.**
  **L'endroit où il ne la tient pas.** Chaque dimension n'émet une preuve **qu'aux
  extrêmes** — fondamental ≥ 60 ou < 45 · force relative ≥ 60 ou < 40 · R:R restant
  ≥ 2 ou < 1 · résultats dans 0-30 jours. **Entre les deux : ni preuve, ni
  inconnue.** Le titre traverse les quatre dimensions sans laisser de trace et
  tombe dans le `else` final :
  ```text
  fond 52 · rs 50 · R:R 1.4 · earnings J+60   →   statut INTACT · conf 0.0
                                                  pos 0 · neg 0 · unk 0
  ```
  **Zéro preuve positive, zéro preuve négative, zéro inconnue — et le verdict est
  « thèse INTACTE ».** La contradiction est **dans le même dictionnaire** : le
  statut affirme, la confiance dit qu'il n'y a rien derrière. `UNKNOWN` est
  réservé aux données **manquantes**, jamais aux données **non concluantes**,
  alors que c'est le même aveu d'ignorance.
  **Ce n'est pas un cas de bord** : les quatre conditions décrivent **le titre
  médian**. Contrairement aux lots 421 et 423, les entrées sont **ordinaires et
  atteignables**.
  **Mais je m'applique la règle du 411 : est-ce affiché ?**
  ```text
  recalculator.py:76-78     p['thesis_health'] = assess(...)['overall_status']
  positions_api.py:54-62    /api/positions/state  → jsonify(state)        ← SERVI
  portfolio_page.py:478/538 posState → actionListHtml → colonne « Statut »
  recalculator.py:105       'thesis_invalidated': … == 'INVALIDATED'
  ```
  Le champ est **calculé et servi au client**, mais la seule consommation tracée
  dans les moteurs est un **booléen `INVALIDATED`**, pour lequel `INTACT` et
  `UNKNOWN` sont équivalents — et **je n'ai pas établi** que la colonne « Statut »
  rende `thesis_health` plutôt que le statut de cycle de vie. **Défaut réel, sur
  des entrées ordinaires, servi — affichage non prouvé, et je l'écris ainsi
  plutôt que de le supposer.**
  **Rang 2** : ni le 422 (affiché, rang 1) ni les 421/423 (inatteignables, rang 4).
  Correction pressentie, dans l'esprit du fichier : quand `pos_ev` **et** `neg_ev`
  sont vides, rendre `UNKNOWN` — le statut existe déjà, et `confidence` vaut déjà
  0.0. **Aucun GO, rien d'engagé.**
  **Décision de veine, prise.** Le critère « troisième défaut inatteignable »
  **n'est pas rempli** — le cas mesuré ici est parfaitement atteignable. Mais la
  pente est nette : **422 affiché · 423 inatteignable · 424 servi, affichage non
  prouvé** — la conséquence s'amincit à chaque lot. **Critère durci pour le 425 :
  si le lot suivant ne produit pas un défaut dont la valeur est PROUVÉE AFFICHÉE,
  la veine des moteurs sera déclarée épuisée et la famille changera au 426.** Le
  compteur ne porte plus sur « trouver », mais sur « atteindre l'écran ».
  **Portée** : une seule fonction (`assess`) ; la colonne « Statut »
  d'`actionListHtml` n'a pas été suivie jusqu'à sa source — c'est la limite
  déclarée ; le gardien `test_thesis_health_dimensions_lot365.py` n'a pas été
  ouvert.
  Suite **2864 passed / 0 skipped**, inchangée. **Aucun fichier touché** ; SW
  `td-shell-v187` ; écart runtime final aucun.

- **Lot 423 — livré** : **« clôture sous $None (structure) » — le comité sait dire
  « — », sauf sur son invalidation ; et la chaîne referme le dossier.** Septième
  lot dans la veine des moteurs, cible `vertex/engines/committee.py` (verdicts
  ACHETER/RENFORCER/ATTENDRE/ÉVITER, thèse, plan et **invalidation**, affichés sur
  « Aujourd'hui »). **Aucun défaut produit — c'est le résultat, pour la deuxième
  fois dans cette veine.**
  **La règle que le fichier respecte** : il sait déjà remplacer une donnée absente
  par un tiret — mesuré, `grade=None` → *« score 70, — »*, `rs` absent → *« force
  rel. — »*.
  **L'endroit où il ne la tient pas**, une ligne plus bas — la phrase qui dit au
  trader à quel prix sa thèse est morte :
  ```python
  invalidation = f"clôture sous ${plan.get('stop')} ({plan.get('stop_type', 'structure')})"
  ```
  ```text
  plan complet (stop 92, type ATR)     « clôture sous $92.0 (ATR) »
  stop_type ABSENT                     « clôture sous $92.0 (structure) »   ← type INVENTÉ
  stop ABSENT / plan VIDE / plan absent « clôture sous $None (structure) »
  ```
  Deux choses distinctes : le prix devient le mot **`None`** à l'écran, et le
  **type de stop est affirmé** alors qu'il n'a jamais été calculé. *Le second est
  plus grave que le premier : `$None` se voit, « structure » se croit.*
  **Le détail le plus fin — dans une seule ligne.** Mon témoin a révélé mieux que
  ce que je cherchais :
  ```text
  d.get('mom', '—')  avec mom = None   →  « momentum None/100 »
  d.get('rs',  '—')  avec rs  ABSENT   →  « force rel. — »
  ```
  **Même f-string, même forme, deux comportements** : `d.get(clé, '—')` ne protège
  que de la **clé absente**, jamais d'une **valeur présente valant `None`**.
  C'est l'instance la plus resserrée du motif de la veine — la bonne pratique et
  sa faille sur la même ligne.
  **La chaîne referme le dossier.** Le seul producteur du `detail`
  (`analysis.py:260-263` et `:304`) remplit `plan.stop`, `plan.stop_type` et `mom`
  **inconditionnellement et jamais `None`** ; unique appelant `terminal.py:608`.
  **Les cas mesurés sont inatteignables aujourd'hui.** **Rang 4** — pièges
  latents, aucune conséquence actuelle, même nature qu'au 421. **Aucun GO.**
  **Cadence, dit sans arrondir.** Séquence de la veine : **416 ✓ · 417 ✓ · 418 ✓ ·
  419 ✓ · 421 ✗ · 422 ✓ · 423 ✗**. Ce n'est **pas** deux négatifs d'affilée, le
  compteur repart de 1. Mais le signal utile n'est pas le compteur : **les deux
  lots négatifs ont la même forme** — un défaut réel dans le code, rendu inoffensif
  par un producteur unique qui remplit tout. Les moteurs sont honnêtes **sur leurs
  entrées réelles** ; ce qui reste est dans des branches que rien n'atteint. **Si
  le 424 rend une troisième fois ce verdict, la veine devra être déclarée
  épuisée** — non parce qu'elle ne trouve rien, mais parce qu'elle ne trouve plus
  que de l'inatteignable.
  **Portée** : une seule fonction (`_evaluate_one`) et son unique chaîne
  d'alimentation ; les branches de verdict n'ont pas été rejouées une par une —
  celle du RSI l'avait été au 416.
  Suite **2864 passed / 0 skipped**, inchangée. **Aucun fichier touché** ; SW
  `td-shell-v187` ; écart runtime final aucun.

- **Lot 422 — livré** : **le R:R affiché repose sur un mouvement attendu que le
  moteur s'invente, et c'est le seul repli qu'il n'étiquette pas.** Sixième lot
  dans la veine des moteurs. Cible : `vertex/options/scenario_pricer.py`, qui
  produit le **R:R du plan** et le **gain attendu** affichés sur `/options`,
  `/analysis` et `/opportunities`.
  **La règle est écrite partout dans ce fichier.** Le docstring l'annonce
  (*« honnêteté §6.8 : … ESTIMATION … étiquetée MODEL_ESTIMATE, jamais présentée
  comme vérité broker »*) et le corps la tient **trois fois** : données
  insuffisantes → **simulation refusée** (« pas de chiffre inventé ») · IV
  absente → recalculée **et** `limitations.append('IV recalculée depuis le mid
  (FALLBACK_ESTIMATE)')` **et** `model_source = 'FALLBACK_ESTIMATE'` ·
  `worst_planned_loss_pct` calculé **seulement** `if stop:`, jamais sur un stop
  inventé.
  **Trois lignes au-dessus du repli IV étiqueté, un quatrième repli — muet :**
  ```python
  em_pct = setup.expected_move_pct
  if em_pct is None:
      em_pct = iv * math.sqrt(holding_days / 365.0) * 100     # aucune limitation ajoutée
  ```
  **Ce n'est pas un cas de bord : c'est le seul chemin.** Les **deux**
  constructeurs d'`UnderlyingSetup` du dépôt (`options_intel_api.py:107` et
  `redesign.py:226`) **omettent le champ** — `expected_move_pct` vaut donc `None`
  **à chaque simulation**, et le mouvement attendu est **toujours fabriqué par le
  moteur lui-même**.
  **Mesuré**, contrat identique, seul le mouvement varie :
  ```text
                                      gain BASE    pire perte    R:R
  expected_move_pct = None (PROD)       145.7 %      -40.8 %     3.57
  expected_move_pct =  3.0 %            104.7 %      -40.8 %     2.57
  expected_move_pct =  8.0 %            213.7 %      -40.8 %     5.24
  expected_move_pct = 12.0 %            309.6 %      -40.8 %     7.59
  ```
  Le moteur fabrique **4,97 %**, d'où le R:R de **3,57**. Le même contrat
  afficherait **2,57** ou **7,59** selon l'hypothèse : **le R:R du plan est
  entièrement déterminé par une hypothèse que le moteur prend pour lui-même.**
  Et les limitations servies sont exactement les trois constantes du fichier (BS
  européen, dividendes, smile) — **aucune ne mentionne le mouvement attendu**,
  vérifié sur la liste servie.
  **Où ça s'affiche** : `analysis_page.py:631` (« R:R ») ·
  `opportunities_page.py:553` (« R:R simulé … perte planifiée ») ·
  `options-intel.js:439` (« R:R du plan »). Et `options-intel.js:431` **rend la
  liste « Limites méthodologiques »** : **la carte affiche ses limites, et
  celle-là n'y figure pas.** Le trader lit une méthodologie qui se présente comme
  complète.
  **Classement — famille du 417, pas du 407.** Ce n'est **pas un chiffre faux** :
  un mouvement attendu déduit de l'IV est l'estimation standard, probablement la
  meilleure disponible. Ce qui manque, c'est **l'étiquette** — dans un fichier
  dont c'est le sujet, à trois lignes d'un repli qui, lui, est étiqueté et dégrade
  `model_source`. **Rang 1** ; correction pressentie minuscule et déjà écrite
  juste au-dessus : une ligne de limitation, et au choix la dégradation de
  `model_source`. **Aucun GO, rien d'engagé.**
  **Portée** : la question de ce lot est l'**étiquetage**, pas la formule — je n'ai
  pas vérifié que le mouvement déduit de l'IV soit numériquement le bon
  estimateur. `capital_free_analysis` n'a pas été ouvert au-delà d'un constat : il
  applique lui aussi un **multiplicateur 100 en dur** (`mid * 100`), même
  hypothèse qu'au lot 418 dans un autre fichier — **signalé, non mesuré ici**.
  **Motif de la veine vérifié une cinquième fois, sous sa forme la plus nette** :
  le fichier étiquette un repli, refuse une simulation faute de données, garde un
  calcul derrière un vrai stop — **et laisse passer le seul repli qui s'exécute à
  chaque appel**. Le compteur annoncé au 421 (deux négatifs d'affilée → le dire ;
  trois → changer de famille) **repart à zéro**.
  Suite **2864 passed / 0 skipped**, inchangée. **Aucun fichier touché** ; SW
  `td-shell-v187` ; écart runtime final aucun.

- **Lot 421 — livré** : **le scoring note un dict vide « D, confiance 58 » — mais
  la mesure a réfuté mon hypothèse, et la chaîne a fermé le dossier.** Cinquième
  lot dans la veine des moteurs, cible `vertex/quant/scoring.py` (score global,
  note, confiance). **Lot négatif sur le produit, et c'est le résultat.**
  **La règle que le fichier respecte, et où il ne la tient qu'à moitié.** Ligne
  136 : `out['fundamental_is_proxy'] = not fund_real  # honnêteté : signale si le
  fondamental est un proxy`. Le fichier **sait** qu'un sous-score peut être une
  hypothèse plutôt qu'une mesure, et il le **déclare** — **pour un sous-score sur
  quatre**. Les trois autres prennent des défauts silencieux (`rsi=50`,
  `volx=1.0`, `atr_pct=2.0`) sans aucun drapeau.
  **Mesuré :**
  ```text
  compose({})   global=40  grade=D  confidence=58
                technical=18  momentum=50  fundamental=45  risk=64
                fundamental_is_proxy=True     ← le seul drapeau, et il est correct
  ```
  Un verdict complet, noté et chiffré, **sur rien du tout**. Points gagnés par
  les seules valeurs par défaut : `technical_score({}) = 18` (rsi 50 → +12 dans
  la bande 45-70 · volx 1.0 → +6), contre **0.0** avec les mêmes clés fournies au
  pire réel. Booléens tous `False` dans les deux cas :
  ```text
  mesures RÉELLES au pire (rsi 10, roc −25, rs 0, atr 10 %)   global=11  tech=0   mom=0   risk=42
  mesures ABSENTES (clés retirées)                            global=40  tech=18  mom=50  risk=64
  ```
  **L'absence de mesure vaut 29 points de plus que la pire mesure réelle.**
  **Mon hypothèse était que la confiance s'inversait. La mesure l'a réfutée.**
  Je supposais que `confidence = 100 − min(std × 2.5, 60)` serait **maximale** sur
  un dict vide, les défauts étant peu dispersés. Mesuré : **aucune donnée 58 ·
  cas réel cohérent 66 · cas réel contradictoire 40**. La confiance se comporte
  **correctement**. **Je ne publie donc pas ce défaut, parce qu'il n'existe pas.**
  *Une hypothèse d'explication doit être testée, pas narrée* — la règle a coûté
  ici une trouvaille annoncée.
  **La chaîne ferme le dossier.** Un **seul appelant** dans tout le dépôt,
  `vertex/engines/analysis.py:203`, et le `ind` construit deux lignes plus haut
  porte **les douze clés, toujours**, calculées inconditionnellement depuis la
  série de prix. **Les valeurs par défaut de `scoring.py` ne sont jamais utilisées
  en production** : le comportement mesuré est **inatteignable aujourd'hui**.
  **Ce qui reste est une caractérisation, pas un défaut.** Le module se présente
  comme **pur et réutilisable** (« Pures = testables », liste des clés attendues
  en tête) — une invitation à un second appelant, qui recevrait une note sans
  savoir qu'elle repose sur des défauts. **Classé rang 4**, piège latent, aucune
  conséquence actuelle. **Aucun GO, rien d'engagé.**
  **Portée** : la vérification de chaîne établit que les douze clés sont
  **toujours présentes**, pas qu'elles soient **numériquement saines** ;
  `options_score` n'a pas été ouvert (il reçoit `None` sur ce chemin).
  **Troisième fois d'affilée dans cette veine que la mesure RÉDUIT ce que j'allais
  écrire (416, 418, 419) — et la première où elle l'ANNULE.**
  Suite **2864 passed / 0 skipped**, inchangée. **Aucun fichier touché** ; SW
  `td-shell-v187` ; écart runtime final aucun.

- **Lot 419 — livré** : **la forme du 418 bornée — 22 replis, 18 légitimes, 4
  aveuglants, et un RSI de 0 effacé.** Dernier lot de mesure de la tranche : il
  **borne** au lieu d'ouvrir. Le 418 avait trouvé une condition de validation qui
  teste son propre repli ; **ce site est-il isolé ?**
  **Recensement par AST** (`vertex/**/*.py` + `terminal.py`) :
  ```text
  comparaisons de `if` contenant un repli `or CONSTANTE`      25
     dont SANS garde `is None` dans la même condition         22
  ```
  **Témoins, les trois passent** : le site du 418 est retrouvé · la ligne
  `quantity` du même fichier est vue par le détecteur · **et écartée** grâce à
  son `is None`. Le détecteur distingue la forme fautive de la forme correcte
  écrite deux lignes plus haut.
  **Les 22 ouverts un par un, triés par RÔLE et non par forme** : **18 =
  sélection/classement, repli honnête** (« absent → 0 » veut dire « ne qualifie
  pas » : `(fund.get('score') or 0) >= 65`, `(c.get('quality') or 0) > (best…)`,
  comparaisons de chaînes, `or 'UNKNOWN'` volontaire…) ; **4 =
  détection/validation**, où le repli masque ce qu'on cherche.
  **La trouvaille — `vertex/scanner/daily.py:62`, un RSI de 0 est EFFACÉ.**
  `if float(d.get('rsi') or 50) < 45: bits.append('momentum faible')` — `0.0` est
  *falsy*, donc la valeur la plus baissière qui existe devient le neutre **50**.
  Mesuré sur `_avoid_reason`, toutes autres entrées identiques :
  ```text
  rsi = 40  (momentum faible)      → « … · momentum faible »
  rsi = 1   (quasi extrême bas)    → « … · momentum faible »
  rsi = 0   (extrême bas RÉEL)     → « … »        ← la raison DISPARAÎT
  rsi ABSENT                       → « … »        ← même sortie que rsi = 0
  ```
  Le trader reçoit **la même explication** pour « je n'ai pas la donnée » et pour
  « le momentum est au plus bas possible » — et la fonction est **non monotone à
  sa propre frontière** (listée à 1, absente à 0). **Ironie avec le 416** : le
  même indicateur y était **fabriqué à 100** là où il est indéfini ; il est ici
  **effacé à 0** là où il est réel. Deux fautes opposées, une seule cause :
  traiter un extrême légitime comme une donnée manquante.
  **Les deux autres.** `reconciler.py:82` compare
  `(loc.get('multiplier') or 100)` à `(b.get('multiplier') or 100)` ; le 418
  ayant mesuré que le côté courtier ne porte **jamais** de multiplicateur, la
  comparaison oppose toujours le local à un **100 fabriqué** — cohérent avec le
  418, pas un dossier neuf. Le contraste est **quatre lignes plus haut, même
  bloc** : le coût moyen est gardé par `is not None` **et** un dénominateur non
  nul. `portfolio_guard.py:19` compte une exposition **inconnue** comme **zéro**,
  donc `MAX_OPTIONS_REACHED` ne se déclenche pas — **lu, pas mesuré**, et dit
  comme tel.
  **Ce que le lot établit** : la forme du 418 est **rare et le plus souvent
  inoffensive** — 4 sites de détection sur 22 replis, dont 1 défaut réel nouveau,
  1 déjà connu, 1 conséquence d'un défaut connu, 1 signalé sans mesure. **Aucune
  campagne à lancer, et c'était la question.**
  Le nouveau défaut est **rang 2** : la conséquence est un **texte d'explication
  incomplet**, pas un chiffre faux, et seulement sur un RSI exactement nul —
  lequel, mesuré au 416, demande une baisse sans un seul jour de hausse. Rare,
  mais c'est le cas où l'avertissement compte le plus. **Aucun GO.**
  **Portée** : le détecteur ne voit que les replis **littéraux dans une
  comparaison de `if`** ; un repli passé par une variable intermédiaire lui
  échappe et **n'a pas été quantifié**. Les 18 « légitimes » sont classés par
  lecture du rôle, pas par exécution.
  Suite **2864 passed / 0 skipped**, inchangée. **Aucun fichier touché** ; SW
  `td-shell-v187` ; écart runtime final aucun.

- **Lot 418 — livré** : **le multiplicateur d'option vaut 100 partout, et le seul
  contrôle qui le surveille ne peut pas mordre.** Troisième lot dans la veine des
  moteurs. Cible : `vertex/positions/calculator.py`, dont le docstring pose une
  règle testable — *« donnée absente → None (jamais 0) »*.
  **La règle est tenue partout, sauf sur un champ.** Moteur exécuté en mémoire,
  mêmes entrées, seul le multiplicateur change :
  ```text
  multiplicateur          market_value   P&L      delta   theta   data_quality  issues
  ABSENT / = 100 / = 0       1000.0     +100.0   110.0   -16.0        OK          []
  = 10  (mini-option)         100.0     -800.0    11.0    -1.6        OK          []
  = 22  (ajusté après split)  220.0     -680.0    24.2    -3.52       OK          []
  ```
  Même position : **P&L +100 avec l'hypothèse 100, −800 avec le vrai
  multiplicateur** — changement de signe sur l'argent, Greeks divisés par dix, et
  `data_quality` reste **OK** sans la moindre alerte. **Témoins dans le même
  fichier** : Greeks absents → `delta = None` · `cost_basis = 0` →
  `unrealized_pnl_pct = None` · `mark` absent → `market_value = None` +
  `MISSING_MARK`. **La règle est appliquée partout sauf sur le seul champ qui
  multiplie tout le reste.**
  **Mais la chaîne resserre le diagnostic.**
  ```text
  ibkr_positions.fetch_positions   ne lit QUE symbol, position, avgCost, secType, currency
                                   → `contract.multiplier` n'est JAMAIS demandé à IBKR
  repository.load_positions        construit le dict IBKR sans clé `multiplier`
  models.option_position           `_f(trade.get('multiplier')) or 100.0`  ← le vrai défaut
  calculator.enrich_option         `p.get('multiplier') or 100.0`          ← repli sur un défaut
  ```
  Toute position arrivant au calculateur porte **déjà** 100 : ce n'est pas
  improvisé, c'est une **convention produit assumée**, écrite dans le docstring
  d'`option_position` (« cost = qty × prime × 100 »). Ce que la chaîne montre
  vraiment : **le multiplicateur réel n'est jamais demandé au courtier**. Pour un
  contrat non standard — mini-option, contrat ajusté après un split — le coût
  moyen, la valeur, le P&L et les quatre Greeks sont faux, **sans signal**. Or le
  système **connaît** ce risque : `reconciliation.py:134` lève
  `MULTIPLIER_MISMATCH` (sévérité 3) dès qu'un contrat annonce autre chose que
  100 — mais ce détecteur travaille sur les **contrats**, jamais sur les
  **positions**.
  **Le contrôle qui ne peut pas mordre.** `audit.py:30` :
  `if (p.get('multiplier') or 100) <= 0: errs.append('MULTIPLIER_INVALID')`.
  Exécuté sur toutes les valeurs invalides :
  ```text
  ABSENT → rien · None → rien · 0 → rien (la valeur même que « <= 0 » vise)
  0.0 → rien · -100 → MULTIPLIER_INVALID   ← seul cas qui mord
  ```
  Cause : `or 100` remplace `None` **et** `0` (tous deux falsy) **avant** la
  comparaison — **le contrôle teste son propre repli, pas la donnée**. **Le
  témoin est deux lignes plus haut** : `if p.get('quantity') is None or
  (p.get('quantity') or 0) <= 0` — le `is None` explicite y est, et
  `QUANTITY_INVALID` **mord** (vérifié par exécution), comme `STRIKE_MISSING` et
  `COST_BASIS_INVALID`. **Deux lignes d'écart, la même forme, une seule écrite
  correctement.** Et `MULTIPLIER_INVALID` **n'apparaît dans aucun test** — zéro
  occurrence sur `tests/**`.
  **Classement calibré, pas gonflé — moins grave que le 416 et le 417** :
  l'hypothèse « multiplicateur = 100 » est **juste pour l'écrasante majorité** des
  contrats américains, et elle est **documentée**. **Rang 2** : le multiplicateur
  réel n'est jamais lu chez le courtier alors que le système sait le contrôler
  ailleurs — erreur **silencieuse et multiplicative**, bornée aux contrats non
  standard. **Rang 4** : `MULTIPLIER_INVALID` ne détecte ni l'absence ni le zéro,
  et ne peut de toute façon jamais se déclencher puisque la valeur est fixée à
  100 en amont — **contrôle mort, deux fois**. **Aucun GO, rien d'engagé.**
  **Portée** : un seul moteur, plus la chaîne d'alimentation nécessaire pour
  savoir si le défaut est atteignable — ce parcours a **réduit** le diagnostic.
  `fetch_positions` ne transmet ni `right`, ni `strike`, ni `exp` ; ce qui en
  résulte n'a **pas** été mesuré ici.
  **Motif confirmé sur trois lots** : la bonne pratique est écrite **à quelques
  lignes du défaut** — 416 `pos = 50.0` quand `hi == lo` ; 417 `tp1_resolved` dans
  le même dictionnaire ; 418 le `is None` explicite deux lignes au-dessus.
  *Chercher la règle que le fichier respecte ailleurs, puis l'endroit où il
  l'oublie* est la méthode la plus rentable trouvée depuis le lot 398.
  Suite **2864 passed / 0 skipped**, inchangée. **Aucun fichier touché** ; SW
  `td-shell-v187` ; écart runtime final aucun.

- **Lot 417 — livré** : **« Rendement +20 séances » — le N affiché n'est pas le N
  du calcul.** Deuxième lot dans la veine des moteurs. Cible :
  `vertex/engines/track_record.py`, **le moteur qui note Vertex lui-même**, dont
  le docstring annonce *« Aucune promesse, que du mesuré »* — d'où la question :
  le mesuré est-il présenté avec son échantillon ?
  **Le mécanisme.** `evaluate()` ne publie un paquet que si `b['n'] >= 5`, mais
  `n` compte les entrées résolues **à au moins un horizon**, alors que chaque
  statistique se calcule sur sa propre liste. Un verdict émis il y a 6 séances
  alimente `n` et `f5`, **pas** `f20`. Le filtre protège le **paquet**, pas
  chaque **nombre publié**.
  **Mesuré — moteur exécuté en mémoire** (ledger fabriqué, `persist._BASE_DIR`
  redirigé, mémo réinitialisé) :
  ```text
  TÉMOIN −  4 entrées                        AUCUN PAQUET (filtre n≥5)   ✔
  TÉMOIN +  5 entrées anciennes              n=5 win_1j=100 win_5j=100 win_20j=100 avg_20j=15.73
  CAS       1 ancienne + 4 à horizon court   n=5 win_1j=20  win_5j=20  win_20j=100 avg_20j=20.0
  ```
  Troisième ligne : le terminal annonce **N = 5**, **20 % de gagnants à 1 et 5
  séances**, et dans la même ligne **100 % de gagnants et +20,0 % de rendement
  moyen à 20 séances** — **assis sur une seule observation**.
  **Ce n'est pas un cas de bord : c'est l'état normal du registre.** Un registre
  qui tourne contient toujours des verdicts trop récents pour +20. Sur un cas
  réaliste — un verdict par séance sur les 40 dernières :
  ```text
  N annoncé                                     39
  observations derrière « +1 séance »           39   (100 % de N)
  observations derrière « +5 séances »          35   ( 90 % de N)
  observations derrière « +20 séances »         20   ( 51 % de N)
  ```
  La colonne « +20 séances » repose **structurellement** sur un sous-ensemble
  strict de `N`, proportion **jamais affichée**. Le cas à une observation est
  l'extrême ; le biais est **permanent**.
  **Où ça s'affiche, et la phrase qui promet ce que le chiffre n'a pas.** Dans la
  **même ligne** de `performance_page.py:443`, `TP1 avant stop` **affiche son
  dénominateur entre parenthèses** (`tp1_resolved`) tandis que `Rdt +20 s`
  n'expose rien et se lit sous le `N` de la ligne — **la bonne pratique existe
  déjà, appliquée à une métrique sur quatre**. Et la légende du graphique dont
  c'est le sujet (L459) déclare *« moyenne réelle des verdicts résolus **(n≥5)**
  — mesure, pas une promesse »* : **faux pour ce chiffre**, `n≥5` filtre le
  paquet, pas l'échantillon de la moyenne à 20 séances. **La phrase promet
  exactement la garantie qui manque.**
  **Le gardien.** `test_evaluate_min_sample_and_no_division_by_zero` (lot 89)
  vérifie le minimum **du paquet** ; sa fixture n'a que **7 cours**, donc `f5` et
  `f20` valent `None` partout et **le cas « un horizon a moins d'observations que
  n » n'est jamais exercé**. À son crédit, il assert `tp1_resolved == 0` : le
  dénominateur est surveillé **là où il est exposé**.
  **Rang 1, sans le gonfler.** Contrairement au 407, **le nombre n'est pas faux**
  — c'est une moyenne réelle d'observations réelles. Ce qui est faux, c'est
  l'**échantillon suggéré** et la **légende**. Défaut d'**honnêteté de
  présentation**, sur la page dont le sujet est la confiance accordée au moteur.
  Correction pressentie, petite : publier le compte par horizon comme le moteur
  le fait **déjà** pour TP1, l'afficher entre parenthèses comme le fait **déjà**
  la colonne TP1, corriger la légende. **Aucun GO, rien d'engagé.**
  **Portée** : un seul moteur, une seule fonction. **`edge_ledger.jsonl` n'existe
  pas sur ce poste** — rien n'est dit de l'ampleur sur les données réelles de
  l'utilisateur ; les proportions viennent d'un registre fabriqué, réaliste mais
  fabriqué.
  **Motif des deux lots de la veine** : dans les deux cas, le code contenait
  **déjà la bonne pratique à côté du défaut** — 416, `pos = 50.0` quand
  `hi == lo` trois lignes plus bas ; 417, `tp1_resolved` dans le même
  dictionnaire. Le défaut n'est pas l'ignorance de la règle, c'est son
  **application incomplète**.
  Suite **2864 passed / 0 skipped**, inchangée. **Aucun fichier touché** ; SW
  `td-shell-v187` ; écart runtime final aucun.

- **Lot 416 — livré** : **un titre qui n'a pas bougé affiche « RSI 100 », et le
  gardien qui dit « neutre » accepte l'extrême.** **Changement de famille
  assumé** : après trois lots sur la couverture des gardiens (413-415), descente
  dans les **moteurs de calcul**.
  **La prémisse, mesurée et fausse.** Le docstring de
  `vertex/engines/indicators.py:13` justifie son choix : *« dn==0 → 100, jamais
  NaN (casserait le JSON) »*. Or :
  ```text
  jsonify({'x': float('nan'), 'y': float('inf')})  →  {"x":null,"y":null}
  ```
  **Flask assainit déjà** — `null` est du JSON valide, que le client rend en
  `—`/`n/d`. *Le témoin a fermé la sonde prévue avant même la mesure.*
  **Ce que rend le moteur, en mémoire** :
  ```text
  série NORMALE (marche aléatoire)            RSI  63.1
  baisse MONOTONE                             RSI   0.0
  hausse MONOTONE (aucune baisse)             RSI 100.0   ← Wilder, CORRECT
  série PLATE (aucun mouvement)               RSI 100.0   ← 0/0 rendu comme l'extrême
  ```
  Deux situations opposées, **même valeur** : un titre halté ou illiquide est
  présenté aussi suracheté qu'une envolée sans un jour de repli. Même choix dans
  la seconde implémentation, `vertex/market/indicators.py:85` (`else 100.0`).
  **Où la valeur arrive** : `analysis.py:40` calcule, L304 place `'rsi':
  round(r)`, `analysis_page.py:472` affiche `kv('RSI', d.rsi)` — **le 100 est
  montré tel quel**.
  **Ce que la mesure a corrigé dans mon propre diagnostic.** `committee.py:97`
  produit la phrase « *Timing défavorable : RSI 100 (suracheté). On patiente.* ».
  Mesuré, elle **est** atteignable sur un plateau de 3 à 45 jours (`dernier >
  MM50` vrai, RSI 100) — **mais dans ces séries il n'y a aucun jour de baisse
  depuis le début**, et « aucune baisse ⇒ 100 » **est** la définition de Wilder :
  contre-intuitif, pas faux. Sonde : neutraliser le seul cas `up == 0 ET dn == 0`
  laisse le plateau-après-hausse à 100, la moyenne des hausses gardant la mémoire
  de la montée. **Le défaut est donc plus étroit que je ne l'ai cru** — titre
  **plat depuis toujours** : RSI indéfini rendu **100**, faux et **affiché** ;
  plateau après hausse : **correct**. Et sur une série parfaitement plate
  `dernier > MM50` est faux, donc la phrase dit « sous la MM50 » : **le nombre
  ment à l'écran, la phrase non.**
  **Le gardien.** `tests/test_calculations_golden.py:193` s'appelle
  `test_rsi_flat_series_is_neutral_not_zero` et assert `30 <= val <= 100` : le
  **nom** promet la neutralité, l'**assertion** admet l'extrême. Il garde contre
  le `0` (baissier extrême), pas contre le `100`. **Il ne bloque pas la
  correction** : sonde rendant `50.0` sur le cas sans mouvement → **31 tests
  golden passent**.
  **Classé rang 1**, mais **nettement moins grave que le 407** : là le HHI était
  faux d'un facteur 170 dans le cas *nominal* ; ici la valeur est juste dans le
  cas dominant et fausse au bord. Correction pressentie : rendre `None` quand il
  n'y a **ni hausse ni baisse** sur la fenêtre — 2 lignes, 2 moteurs, plus le nom
  du gardien à accorder à son assertion. **Aucun GO, rien d'engagé.**
  **Portée** : **un seul** indicateur ouvert. Le recensement statique donne
  **641 divisions dans `vertex/**` hors UI, dont 481 à dénominateur non constant
  et non protégé** — c'est un **vivier trié par la forme**, pas une liste de
  défauts (leçon du 408) ; **aucune campagne lancée**, rien mesuré sur les 480
  autres.
  **Note de cadence tranchée** : la veine « couverture des gardiens sur les
  octets servis » reste **close en rendement** ; celle des **moteurs de calcul**
  vient de s'ouvrir et paie mieux.
  Suite **2864 passed / 0 skipped**, inchangée. Sonde **restaurée à l'octet** et
  moteur ré-interrogé après restauration ; SW `td-shell-v187` ; écart runtime
  final aucun.

- **Lot 415 — livré** : **288 identifiants servis, aucun doublon ; le gardien
  n'en surveille que 3 pages sur 8.** Deux éléments qui portent le même `id`,
  c'est un défaut **silencieux** : `getElementById` rend **le premier**, le
  second n'est jamais mis à jour — carte figée, aucune erreur en console. Le
  trader voit une donnée qui ne bouge plus et n'a aucun moyen de le savoir.
  Périmètre : les octets servis (8 pages + 26 scripts), `<script>` **retirés du
  marquage** — une chaîne dans du JS n'est pas un nœud.
  ```text
  1. doublon dans le marquage servi        288 identifiants → 0 doublon
  2. collision marquage × gabarit JS       1 candidat  → ouvert
  3. id littéral émis DANS une répétition  1 sur 113   → ouvert
  ```
  **Le candidat n°2** (`#op-compare`, `/opportunities`) : les deux porteurs sont
  dans des **vues mutuellement exclusives** — `renderRadar()` (L240) émet
  `<div id="op-compare">`, `renderOptions()` (L509) émet
  `<button id="op-compare">`, et **les deux écrasent le même
  `$('op-body').innerHTML`**. Ils ne coexistent jamais. Mieux : `renderCompare()`
  n'a **qu'un seul appelant**, L256, dans `renderRadar` — la fonction qui vient
  de créer le `div`. **Aucune conséquence.** (L'`id` du bouton n'est cherché par
  personne, son handler est un `onclick` inline : nom en double sans effet,
  rang 4.)
  **Le candidat n°3** est la forme qui fabrique vraiment des doublons — un `id`
  fixe dans un gabarit passé à `.map()`. Ouvert : `'<div id="strat-pf-' + i + '"'`,
  relu par `getElementById('strat-pf-' + i)` — **interpolé avec l'indice de
  boucle**, unique par élément, code correct ; mon extracteur tronquait au `+`.
  **Zéro doublon réel sur les trois classes.**
  **L'instrument, deux fois.** Une heuristique de proximité (« un `.map(` dans
  les 700 caractères précédents ») donnait **9 candidats** ; remplacée par un
  vrai **appariement de parenthèses** — le `.map(` doit se **fermer** après
  l'identifiant → **1**. Témoins des deux côtés : un `id` dans un `.map()`
  fabriqué est détecté, un `id` hors `.map()` ne l'est pas. Et une version
  intermédiaire du test d'englobement remontait jusqu'au premier guillemet
  rencontré : elle tombait sur `class="` et jugeait le mauvais contexte. Elle
  produisait des lignes propres, alignées, et fausses. Jetée.
  **Ce que le filet couvre, mesuré par mutation.** `test_no_duplicate_ids` ne
  visite que **3 pages sur 8** (`/`, `/portfolio`, `/system`) :
  ```text
  doublon posé sur /markets  (page NON visitée)  →  suite complète : 2864 passed
  doublon posé sur /         (page visitée)      →  test_no_duplicate_ids : FAILED
  ```
  **Le gardien mord — là où il regarde.** Sur `/markets`, `/opportunities`,
  `/analysis`, `/options`, `/journal`, un identifiant dupliqué serait servi au
  navigateur sans qu'aucun des 2 864 tests ne le signale. **Non comblé**
  (invariant non violé, mesuré 8/8 ; gardien-pour-faire-un-lot interdit depuis le
  384) — **rang 3**. **Avertissement pour qui étendra** : la regex du gardien,
  `id="([^"]+)"`, **ne retire pas les `<script>`** et compte donc les
  identifiants des gabarits JS comme des nœuds ; élargir sans corriger ce point
  ferait remonter des doublons qui n'existent pas dans le DOM — exactement le
  `#op-compare` ci-dessus.
  **Portée** : identifiants **statiquement observables** ; un `id` entièrement
  calculé échapperait, et le DOM final n'a pas été rejoué en navigateur — la
  classe 3 est une **borne statique**, pas une observation.
  Suite **2864 passed / 0 skipped**, inchangée. Sondes **restaurées à l'octet**
  (`git status` vide, suite de référence rejouée après restauration) ; SW
  `td-shell-v187` ; écart runtime final aucun.

- **Lot 414 — livré** : **les 167 boutons servis sont tous câblés ; un bouton
  mort fabriqué par le JS servi ne serait vu par aucun test.** Un bouton qui ne
  fait rien est le défaut le plus banal d'une interface, et le plus humiliant :
  le trader clique, rien ne se passe, il ne sait pas si c'est l'application ou
  lui. Trois tests déclarent l'invariant ; personne n'avait mesuré ce qu'ils
  couvrent **des octets servis**.
  ```text
  boutons dans le HTML rendu (scripts retirés)   85
  boutons fabriqués par le JS servi              82   (inline de page 64 · /static 18)
  total                                         167
  ```
  **Correction de cohérence interne** : une première passe annonçait **231** — 
  elle comptait deux fois les boutons vivant dans un `<script>` inline.
  **Verdict, avec un critère durci** (l'id doit être un **littéral cité** ET à
  moins de 70 caractères d'un accesseur) : **inline 18 · id 87 · `data-*` 62 ·
  SANS ÉCOUTEUR 0**. Les 62 `data-*` ont été **ouverts** : 16 attributs
  distincts, chacun avec son site de consommation nommé (`data-open-analysis` 53,
  `data-entity-menu` 10, `data-close-drawer`/`data-close-modal`,
  `data-filter-key`, `data-i` → `btns.forEach(b => b.addEventListener(…))`).
  **Cinq témoins** : bouton nu, `data-zzz-lot414` inconnu, id inexistant → morts ;
  `onclick` réel et `id="vx-collapse-btn"` (accroché via l'aide `$()`) → câblés.
  **L'instrument s'est encore trompé, et c'est la même faute.** Un premier
  durcissement exigeant `getElementById('id')` donnait **55 boutons « morts »**,
  dont `vx-collapse-btn` et `vx-notifs-btn` — manifestement vivants. Cause :
  `vx-shell.js` accroche par une **aide locale**, `$('vx-collapse-btn')`.
  **Troisième répétition** (409 `emptyCard`, 413 `get(…)`, 414 `$(…)`) → le
  critère est devenu agnostique à l'accesseur.
  **Ce que les trois gardiens couvrent, mesuré par mutation.** Un bouton mort
  déposé **dans le shell** : `test_every_button_has_handler` **MORD** ;
  `test_ui_v3::test_no_dead_buttons` **passe**, car il **court-circuite** dès
  qu'un attribut `data-` existe — ce qui **exempte 62 des 167 boutons** ; le
  troisième passe aussi. Le même bouton déposé **dans un fichier JS servi**
  (`vx-entities.js`) : **les trois passent**, et la suite complète ne rend
  **qu'un** échec — **l'empreinte `/static` du 361**, qui ne dit rien du bouton.
  Empreinte mise à jour comme le flux de travail l'impose de toute façon :
  ```text
  octet /static modifié · empreinte mise à jour · bouton mort servi
  suite complète →  2864 passed
  ```
  **Entièrement verte, avec un bouton inerte servi sur les 8 pages.** Raison :
  `test_every_button_has_handler` balaie `vertex/ui/pages/*.py` et le shell,
  **pas `vertex/static/**/*.js`** — où vivent **18 des 167** boutons. Même défaut
  de périmètre que le **385** (recensement s'arrêtant à `vertex/`) et le **381**
  (liste gardée qui n'est pas celle qui est servie), sur un troisième objet.
  **Bilan : le produit est sain (0 mort sur 167), le filet ne couvre que
  149/167.** Trou **non comblé** : livrer un gardien « parce qu'un trou existe »
  est interdit depuis le 384, et l'invariant n'est pas violé aujourd'hui.
  **Classé rang 3** — élargir le périmètre demande d'accepter la délégation
  inter-fichiers, c'est une décision de conception.
  **Portée** : le contrôle établit qu'un écouteur **existe**, pas que le clic
  produise le bon effet ; l'analyse est statique, et un attribut calculé au vol
  échapperait — mesuré à **0** occurrence dans le corpus servi.
  Suite **2864 passed / 0 skipped**, inchangée. Sondes **restaurées à l'octet**
  et vérifiées **par l'instrument lui-même** (361 → 5 passed, `git status`
  vide) ; SW `td-shell-v187` ; écart runtime final aucun.

- **Lot 413 — livré** : **les 156 chemins que le client peut demander — aucun ne
  pointe dans le vide.** Un chemin d'API mal écrit côté client ne casse rien de
  visible : la requête part, le serveur répond 404, la carte reste sur son état
  vide — **honnête en apparence, mais pour une mauvaise raison**. Personne
  n'avait vérifié la correspondance.
  **Périmètre = les octets servis**, pas les sources : les 8 pages demandées au
  serveur en mémoire (8 × HTTP 200), puis **chaque `<script src>` demandé au
  serveur à son tour**.
  ```text
  pages 8 · scripts externes servis 26 · blocs inline 15 · corpus 1 243 931 octets
  résolution par app.url_map.match() → les 190 routes réellement enregistrées
  ```
  **L'instrument s'est trompé deux fois, et c'est mesuré.** (1) Les 26 fichiers
  `/static` n'étaient pas dans le corpus — recherche disque avec un chemin faux :
  `515 108` octets / 42 chemins, contre `798 881` / 52 une fois **demandés au
  serveur**. (2) Le détecteur ne connaissait que `fetch(`, alors que
  `options-intel.js:466` appelle `get('/api/options/strategies/'+sym)` via une
  **aide locale** — **répétition exacte de la leçon du lot 409**, avec une autre
  enveloppe. (3) Trois faux morts par normalisation : la concaténation **en
  queue** (`'/api/options/gex/' + encodeURIComponent(sym)`) est désormais
  reconnue comme segment dynamique.
  **Témoins** : route réelle → OK · route inventée → `NotFound` · segment
  dynamique → OK ; et **de bout en bout** sur les trois formes d'écriture (appel
  direct, aide locale, concaténation en queue), les trois chemins sont retrouvés.
  Un `fetch('/api/reco-inexistante-413')` déposé dans un fichier servi **serait**
  rapporté.
  ```text
  chemins distincts confrontés à l'url_map     156
     résolvent                                 149   (dont 8 par segment dynamique)
     ne résolvent pas                            7   ← ouverts un par un
  appels /api distincts                          55   tous résolus
  ```
  **Les 7 sont 7 faux positifs de l'extracteur, aucune requête** : `/1%IV` et
  `/100` (unités affichées), `/api` et `/static` (tests de préfixe,
  `vx-router.js:42`), `/api/ibkr`, `/api/positions`, `/api/account` (préfixes de
  politique de cache, `vx-core.js:228/272`). **Zéro chemin mort**, et le zéro est
  **substantiel** : 156 littéraux confrontés à un `url_map` exécuté, les 7
  restants lus dans leur ligne.
  **Trouvaille annexe, triviale — dite comme telle.** `/api/account` figure dans
  **les deux** listes de cache du client (`PERSIST_DENY`, `LIVE_TTL`) alors que
  **0 route sur 190**, **0 appel sur 55** et **0 occurrence ailleurs dans le
  dépôt** ne lui correspondent : **entrée morte**, elle ne dénie rien et ne
  raccourcit aucun TTL. **Aucune conséquence visible pour le trader** — classée
  **rang 4**, non corrigée : ce serait exactement le « changement gratuit » que la
  boucle s'interdit. Les 5 autres préfixes **mordent**, ce qui rend le `0` lisible.
  **Portée mesurée, pas affirmée** : l'extraction est statique, donc un chemin
  entièrement calculé lui échapperait — sur **91** appels `fetch(` du corpus
  servi, **85** ont un littéral en premier argument et **6** une variable
  (`url`, `u`, `href`) ; les 6 sont ouverts : ce sont **les tuyaux eux-mêmes**
  (implémentation de `VX.fetch`, `fetch` de fragment du routeur), qui reçoivent
  les URL construites aux 85 sites littéraux — **aucun endpoint distinct ne s'y
  cache**. Le lot établit que les routes **existent**, pas ce qu'elles renvoient.
  Suite **2864 passed / 0 skipped**, inchangée. **Aucun fichier touché** (la
  sonde vit dans le scratchpad) ; SW `td-shell-v187` ; écart runtime final aucun.

- **Lot 412 — livré** : **le gardien de la règle n°3 détecte le changement
  d'asset, mais n'impose pas le bump.** La règle critique n°3 protège le **repli
  hors-ligne** : si un octet de `/static` change sans bump du service worker, un
  visiteur déjà venu et hors ligne garde l'ancienne copie. Le gardien du lot 361
  est censé l'imposer — **personne n'avait vérifié qu'il l'impose vraiment**.
  **D'abord la concordance** : version SERVIE (`system.py`) `v187` = version
  ENREGISTRÉE (`test_sw_cache_scope_lot361.py`) `v187`, et l'empreinte
  enregistrée `f83645b51509…` **égale** celle recalculée sur les 54 fichiers de
  `/static`. Le contrat décrit bien l'état servi.
  **L'expérience — le scénario du développeur pressé.** Le message d'aide du
  gardien demande deux choses : *« 1. bumper `const CACHE='td-shell-vN'` … ;
  2. remettre à jour `_EMPREINTE` et `_SW_VERSION` »*. Simulé exactement : un
  octet ajouté à `vertex/static/vertex/css/tokens.css`, `_EMPREINTE` mise à jour
  **comme demandé**, `CACHE='td-shell-v187'` **laissé tel quel**.
  ```text
  asset modifié · empreinte mise à jour · CACHE inchangé (v187)
  suite complète →  2864 passed
  ```
  **Verte.** Un fichier servi a changé, le repli hors-ligne n'a pas été purgé, et
  rien dans les 2 864 tests ne le signale. Pourquoi :
  `test_les_assets_servis_correspondent_a_la_version_enregistree` compare
  l'empreinte — satisfaite dès qu'on la réécrit ; et
  `test_la_version_enregistree_n_est_jamais_en_avance_sur_le_service_worker`
  n'exige que `_SW_VERSION <= _version()`, soit `187 <= 187`. **Aucun test
  n'exige que la version AUGMENTE quand l'empreinte change.**
  **Ce qui atténue, et qu'il faut dire** : le trou n'est **pas silencieux**.
  Seconde sonde : sans réécrire l'empreinte, le gardien **échoue d'abord**, avec
  l'instruction en toutes lettres (`E   1. bumper \`const CACHE='td-shell-vN'\`
  …`). Il faut donc **obéir à la moitié de la consigne** pour produire le défaut,
  pas simplement l'oublier. Le gardien **informe**, il n'**automatise** pas.
  **Pourquoi je ne corrige pas** : « exiger que `_SW_VERSION` augmente quand
  `_EMPREINTE` change » **n'est pas implémentable dans le fichier lui-même** —
  les deux constantes sont éditées par le commit qu'on veut contrôler, donc
  l'ancienne valeur a déjà disparu à l'exécution du test. Un registre append-only
  déplace le problème sans le fermer. **La seule vérification robuste lit
  l'historique git** (aucun test ne lit git aujourd'hui) : instrument d'un autre
  ordre, **décision de conception**, pas réparation d'agent. **Classé rang 3.**
  *Un contrat écrit dans le fichier qu'il contrôle ne peut pas s'imposer à qui
  édite ce fichier.*
  **Portée** : ce lot teste **une** faille précise — mettre à jour l'empreinte
  sans bumper. Il ne dit pas le gardien faible ailleurs : le lot 394 avait rejoué
  la règle n°3 avec une faute réelle (fichier `/static` modifié, rien d'autre
  touché) et **elle mordait**. Le gardien **détecte** le changement d'asset ; il
  **n'impose pas** la conséquence.
  Suite **2864 passed / 0 skipped**, inchangée. Sondes **restaurées à l'octet**
  (`git status` vide, empreinte recalculée = enregistrée, v187 = v187) ; SW
  `td-shell-v187` ; écart runtime final aucun.

- **Lot 411 — livré** : **les 59 provenances déclarées — 2 nomment une origine
  sans producteur, et elles ne s'affichent jamais.** Chaque carte de Vertex
  déclare sa provenance (`source:`) : c'est le contrat d'honnêteté visible par le
  trader — *d'où vient ce que je regarde ?* Personne n'avait vérifié que
  l'étiquette corresponde à la donnée réellement tracée.
  ```text
  champs `source:`                          59   (dans 26 fichiers)
     EXPRESSION (variable, ternaire)        32   ← propage la provenance réelle
     LITTÉRAL (chaîne fixe)                 27   ← peut dériver
  ```
  Les 32 expressions sont **honnêtes par construction** : elles transportent ce
  que le serveur a déclaré. Seuls les 27 littéraux peuvent mentir. **Témoin de
  l'instrument** : les deux étiquettes connues du 407 sont bien retrouvées parmi
  eux.
  **Les 27 confrontés un par un** à l'existence **et** au producteur de l'origine
  nommée : `scenario_pricer` ×6 (module présent) · `SCAN` ×5 — l'étiquette du
  client **duplique la déclaration du serveur** (`source='SCAN'`, 3 sites) au
  lieu d'en inventer une · `board options` · `calendrier moteur` ×3 (`/cal-feed`,
  7 réf.) · `moteur track-record` · `Moteur de régimes` · `journal local` ×2
  (`set('vxJournal')` ×2) · « clôtures déclarées » L642 (`set('myTradesClosed')`,
  carte **rendue**, étiquette exacte). **→ 25 sur 27 exactes**, et les **2**
  seules sans producteur sont celles du dossier 406/407.
  **Le détail qui change la description du dossier.** Trois cartes de
  `/portfolio` portent « clôtures déclarées », et elles ne se valent pas :
  ```text
  L610  equityCard    ← E().equity() → myTradesEquity → 0 écrivain → JAMAIS rendue
  L617  drawdownCard  ← même série                                 → JAMAIS rendue
  L642  heatmapCard   ← withPl (myTradesClosed)                    → RENDUE, exacte
  ```
  Donc **ces deux étiquettes ne sont jamais affichées** : elles vivent sur une
  branche inatteignable. Le préjudice du 406/407 est bien **le graphique absent
  et la consigne impossible**, *pas* une provenance mensongère à l'écran. C'est
  une précision, pas une atténuation — **le HHI faux du 407, lui, est affiché**.
  **Quatrième bornage consécutif** (402, 408, 409, 411). Le zéro est
  **substantiel** : 27 littéraux confrontés un par un, pas comptés.
  **Portée** : le contrôle porte sur la correspondance étiquette ↔ origine
  nommée (existe-t-elle, produit-elle) ; il ne dit rien de la **justesse de la
  valeur** tracée. Et les 32 expressions n'ont pas été suivies jusqu'à leur
  source : elles sont réputées honnêtes parce qu'elles propagent — raisonnement
  de conception, pas mesure.
  Suite **2864 passed / 0 skipped**, inchangée. **Aucun fichier touché** ; SW
  `td-shell-v187` ; écart runtime final aucun.

- **Lot 409 — livré** : **les 8 pages balayées — une seule consigne impossible,
  celle du 406.** Le lot 406 avait trouvé **un** état vide qui donne au trader une
  consigne que le code ne peut pas honorer ; les 8 pages n'avaient pas été
  balayées.
  **L'instrument s'est trompé, et le témoin l'a montré.** Premier détecteur :
  compter les appels `states.empty(` → 85 trouvés, **mais pas le site du 406**.
  Raison : `portfolio_page.py` et `performance_page.py` passent par une **aide
  locale** (`emptyCard(host, reason, action)`) et mon détecteur comptait la
  **définition** de l'aide, jamais ses appels. *Compter les appels d'une fonction
  sans compter ceux de ses enveloppes, c'est mesurer la mécanique et rater
  l'usage.* Corrigé :
  ```text
  sites d'état vide réellement affichés   88   (direct 83 · via une aide 5)
  ```
  Témoin après correction : `portfolio_page.py:623` **est retrouvé**.
  **Le filtre** : un état vide qui **décrit** une absence (« VIX non fourni par le
  dernier scan ») n'est pas un état vide qui **promet**. Le défaut du 406 a une
  forme précise — *le message dit de faire quelque chose, et le faire ne produira
  pas le résultat annoncé*. Sur tournures d'instruction (« se construit »,
  « renseigne », « marque une », « ajoutez », « créez », « lancer un scan », « au
  fil des »…) : **12 / 88**.
  **Les 12 vérifiés un par un**, mécanisme cherché dans le code et non supposé :
  ```text
  « lancer un scan depuis Système » ×3     /api/rescan (7 réf.)            TENABLE
  « Marque une idée Suivre »               followStock() + bouton servi    TENABLE
  « créez un suivi depuis une analyse »    followStock(entry/stop/tgt)     TENABLE
  « ajoutez les titres à surveiller »      set('vxWatchlist') ×2           TENABLE
  « ouvrir une analyse pour le détail »    route /analysis                 TENABLE
  « le flux se remplit au rythme… »        flux d'événements live          TENABLE
  « renseigne le champ erreur »            j-mistake → e.mistake           TENABLE
  « renseigne le champ leçon »             j-lesson  → e.lesson            TENABLE
  « renseigne état émotionnel »            j-emo     → e.emo               TENABLE
  « elle se construit au fil des clôtures » set('myTradesEquity') → 0 site ★ IMPOSSIBLE
  ```
  Les trois consignes du Journal méritaient l'examen car elles nomment des champs
  précis : vérifié, `performance_page.py` L338-341 construit `j-lesson`,
  `j-mistake`, `j-emo` **et** L355 les écrit dans l'entrée. Le trader peut les
  renseigner ; les cartes se rempliront.
  **Une seule consigne est impossible sur les 8 pages : celle du 406.** Comme le
  408 pour le `|| 0` du 407, ce lot **borne** le dossier au lieu de l'élargir —
  la correction reste **un texte ou un mécanisme, sur une seule carte**. Le zéro
  est **substantiel** : 12 promesses examinées une par une, pas un comptage
  global.
  **Portée** : le filtre repose sur une liste de tournures françaises, écrite
  dans le rapport pour qu'elle soit contestable ; une consigne formulée
  autrement passerait au travers. Et « TENABLE » signifie *le mécanisme existe et
  écrit la donnée lue* — pas que le parcours soit ergonomique.
  Suite **2864 passed / 0 skipped**, inchangée. **Aucun fichier touché** ; SW
  `td-shell-v187` ; écart runtime final aucun. **Prochaine échéance : bilan n°10
  au lot 410.**

- **Lot 408 — livré** : **le `|| 0` du lot 407 est isolé, pas une famille.**
  Question laissée ouverte par le 407 : cas isolé ou premier d'une famille ? La
  réponse change la **taille du dossier de rang 1**, donc la décision.
  **Recensement brut** — périmètre servi (`vertex/**` `.py`+`.js` et
  `terminal.py`, les six modules reliques exclus) :
  ```text
  lignes portant `|| 0` / `?? 0` / `or 0`      440   (dans 70 fichiers)
  occurrences (plusieurs par ligne possible)   606
     dont terminal.py                          206
  ```
  Instrument validé : le site du 407 est retrouvé, un fichier sans motif ne rend
  rien. **Ce chiffre ne prouve rien et n'est pas présenté comme un problème** :
  `(r.get('change') or 0)` dans une somme est un choix de modélisation. Un
  `|| 0` n'est un défaut que si l'opérande peut être **absent** *et* que le zéro
  est ensuite **présenté comme une mesure**.
  **Le filtre décisif — les charges utiles envoyées aux moteurs.** C'est
  exactement la forme du 407 : un `null` transformé en `0`, transmis à une API et
  **déclaré réel**.
  ```text
  appels POST sur chemin servi                          25
     dont un `|| 0` / `?? 0` dans la charge utile        1
  ```
  **Un seul — celui du 407.** Aucune autre page n'envoie une absence maquillée en
  zéro à un moteur. **Le défaut est isolé** : le dossier reste un site, une page,
  une décision.
  **Le filtre de forme, et ce qu'il vaut vraiment.** Un `|| 0` sur un **appel**
  dont le résultat est, ailleurs dans le même fichier, comparé à `null` : 128
  appels, **53 candidats**. **Ce ne sont pas des trouvailles, c'est un vivier
  d'hypothèses** — montré plutôt qu'affirmé en ouvrant le candidat le plus
  sensible, celui qui toucherait le P&L d'une position IBKR :
  `positions/repository.py:63` — `'cost': (raw.get('avgCost') or 0) * (qty or 0)
  if raw.get('avgCost') is not None and qty else None`. **Il est sain** : le
  `or 0` est gardé, `cost` vaut `None` quand `avgCost` manque. Faux positif de
  forme, résolu en le lisant. *Un vivier trié par la forme ne devient une liste
  de défauts qu'après lecture, un par un ; publier les 53 comme des trouvailles
  aurait été malhonnête.*
  **Conséquence pratique pour la décision** : corriger 406/407 ne demande **pas
  une campagne** — un seul site à changer, une seule cause (`myCapital` jamais
  écrit).
  **Portée** : le filtre décisif ne voit que les payloads construits à moins de
  12 lignes d'un `method:'POST'` ; une charge utile assemblée plus loin
  échapperait au comptage. Le recensement large est purement textuel : il ne
  distingue pas un opérande qui peut manquer d'un compteur qui vaut réellement
  zéro. C'est dit, pas contourné.
  Suite **2864 passed / 0 skipped**, inchangée. **Aucun fichier touché** ; SW
  `td-shell-v187` ; écart runtime final aucun.

- **Lot 407 — livré** : **le `|| 0` qui fabrique une alerte de concentration.**
  Le lot 406 avait trouvé deux clés lues mais jamais écrites, et suivi **une**
  conséquence (la courbe d'équité qui ne s'affiche jamais). Ce lot suit **la
  seconde — et elle est plus grave**.
  **D'abord borner.** `vx-entities.js` lit **11** clés et en écrit **9** :
  **exactement deux orphelines**, `myCapital` et `myTradesEquity`, pas une de
  plus. Et sur les 8 pages servies, **un seul module** les consomme —
  `portfolio_page.py` (L296, L586, L718). Le périmètre du dossier 406 est
  **confirmé et clos** : 2 accesseurs, 1 page.
  **La conséquence non suivie.** L718 envoie
  `cash: E().capital() || 0` avec `simulated: false`. Or `capital()` vaut
  **toujours `null`** : le `|| 0` **convertit silencieusement une donnée absente
  en un zéro**, transmis à `/api/portfolio/team` et **déclaré réel**
  (`provenance='REAL'`). Trois lignes plus bas, le fichier écrit lui-même la
  règle qu'il enfreint : *« Manquant/insuffisant n'est jamais présenté comme
  zéro. »*
  **Ce que ce zéro change, mesuré** — moteur exécuté deux fois sur les **mêmes**
  positions :
  ```text
  mesure          cash = 0        cash = 50 000    verdict
  equity          4 100           54 100           DIFFÈRE
  hhi             0.5003          0.0029           DIFFÈRE  (×170)
  issue_gardien   True            False            DIFFÈRE
  ```
  `hhi` est calculé sur l'équité **cash compris** ; envoyer 0 gonfle la
  concentration de deux ordres de grandeur. Et la page **affiche** ce chiffre :
  `if (risk.hhi >= 0.66) → « Concentration très élevée (HHI …) »`.
  **Le seuil est-il franchi ? Oui, mesuré** :
  ```text
  1 position    HHI cash=0  1.0     → ALERTE       | cash=50k 0.0015 → aucune   ★ FABRIQUÉE
  2 positions   HHI cash=0  0.5003  → aucune       | cash=50k 0.0029 → aucune
  4 positions   HHI cash=0  0.3019  → aucune       | cash=50k 0.0073 → aucune
  ```
  **Avec une seule position déclarée, le terminal affiche « Concentration très
  élevée (HHI 1) » — un artefact du `|| 0`, pas une lecture du portefeuille.**
  Le blob actuel porte 2 positions, donc l'alerte ne part pas aujourd'hui ; mais
  **le HHI affiché reste faux d'un facteur ~170** et servi comme mesure réelle.
  **Une conséquence qui, elle, n'atteint pas l'écran — dite quand même.**
  `team_view` conclut **toujours** « pas de gardien (cash/monétaire) »
  (`ROLE_TARGETS[GOALKEEPER] = (1,1)`, `if snapshot.cash > 0` jamais vrai). Mais
  la page **ne consomme pas** `d.team` — `team` n'y désigne que le nom de la vue
  « Synthèse ». Vérifié : calculé, **pas affiché**. Je le dis plutôt que de
  grossir le dossier.
  **Trois issues, aucune engagée** (toutes touchent un octet servi ou un moteur) :
  (1) ne pas envoyer un zéro pour une absence ; (2) **alimenter `myCapital`** —
  même décision que le volet 1 du 406, elle règle les deux d'un coup,
  **RECOMMANDÉ** ; (3) a minima masquer le HHI et son alerte quand le cash est
  inconnu.
  **Portée** : les chiffres viennent d'une exécution directe de `risk_engine` et
  `stress_tests` sur des positions **fabriquées pour la mesure** — c'est la
  méthode qui est démontrée, pas le portefeuille du trader ; `beta` et
  `pire_stress` ressortent `None` faute d'entrées, leur sensibilité au cash
  **n'est pas affirmée**.
  Suite **2864 passed / 0 skipped**, inchangée. **Aucun fichier touché** ;
  moteurs exécutés en mémoire, sans serveur ; SW `td-shell-v187` ; écart runtime
  final aucun.

- **Lot 406 — livré** : **sept clés synchronisées que rien n'écrit, et une
  promesse intenable sur `/portfolio`.** Après trois lots négatifs (403, 404,
  405), celui-ci trouve — et c'est **visible par l'utilisateur**.
  **La question** : le contrat `DESK_KEYS` (règle critique n°1) liste **17 clés**
  synchronisées. Jamais posée : ces 17 clés sont-elles réellement **produites**
  par le client ? Une clé listée que rien n'écrit, c'est la synchronisation d'un
  fantôme.
  **L'instrument s'est trompé d'abord.** Première passe : « 13 clés sur 17 sans
  écrivain », dont `myTrades` — la clé des positions du trader. Absurde. J'avais
  exclu `vx-entities.js` du corpus parce qu'il porte la **liste** `DESK_KEYS`,
  sans voir qu'il porte aussi **les écrivains** (`set('myTrades', list)` et
  quinze autres). *Exclure un fichier pour ce qu'il déclare, c'est se priver de
  ce qu'il fait.* Corrigé : exclusion des **lignes** de déclaration, pas des
  fichiers. Témoin négatif : une clé inventée ne trouve aucun site.
  ```text
  clés du contrat DESK_KEYS                              17
     avec au moins un site d'écriture en production      10
     SANS aucun site d'écriture                           7
  ```
  Les sept : `myTradesEquity` · `myRecosClosed` · `myCapital` · `simCash` ·
  `simStart` · `simTrades` · `simClosed`. Vérification exhaustive des écritures
  littérales sur tout `vertex/**` et `terminal.py` : **aucune** ne les vise.
  Blob desk **réel** : **6 clés sur 17** portent des données, **aucune des sept**
  n'y figure, et aucune clé hors contrat.
  **LE DÉFAUT VISIBLE.** `portfolio_page.py` L296/L586/L718 lisent
  `E().capital()` et `E().equity()`, soit `myCapital` et `myTradesEquity` —
  **jamais écrits**. Donc `eq` vaut **toujours `[]`** : la branche
  `if(eq.length>=2…)` est **inatteignable**, la **courbe d'équité** et le
  **drawdown** ne peuvent **jamais** s'afficher, et `cash` vaut toujours
  `null`/`0`.
  **Le problème n'est pas la carte vide — c'est ce qu'elle promet** : « *Courbe
  d'équité indisponible — elle se construit au fil des clôtures de positions
  déclarées.* » Or clôturer une position exécute `set('myTrades', list);
  set('myTradesClosed', closed);` (`vx-entities.js:171`) — **jamais**
  `myTradesEquity`. Le trader peut déclarer autant de clôtures qu'il veut : la
  courbe n'apparaîtra pas. **L'état vide donne une consigne qui ne peut pas
  aboutir** — pas un chiffre inventé, mais son cousin : une promesse que le code
  ne peut pas tenir.
  **L'« évidence » à NE SURTOUT PAS FAIRE.** Élaguer `DESK_KEYS` de 17 à 10
  serait une **perte de données**, pas un nettoyage : le push desk est
  **last-writer-wins total** (mécanisme du lot 362), et un profil de navigateur
  détenant encore `simCash`/`simTrades`/`simClosed` (l'ère du simulateur) les
  verrait **cesser d'être synchronisées puis disparaître du serveur** au premier
  push suivant. Le blob mesuré ici ne les contient pas — mais il ne dit rien des
  autres profils, et il n'y a pas de retour en arrière.
  **Dossier de rang 1, deux volets, aucun engagé** : (1) **la promesse de
  `/portfolio`** — soit alimenter `myTradesEquity` à la clôture (le comportement
  que le texte promet), soit réécrire l'état vide ; **les deux touchent un octet
  servi** (bump SW, MD5, gardiens), c'est une décision. (2) **Les 7 clés** —
  recommandation : **les garder** (coût nul, le push n'envoie que les clés
  réellement présentes ; le retrait, lui, est irréversible).
  **Portée** : la recherche porte sur les écritures **littérales** ; les 53 sites
  `set(<variable>, …)` du dépôt ont été vérifiés — aucun ne concerne le magasin
  desk. Et « présente dans le blob » vaut pour **un** profil, celui de cette
  machine — c'est précisément pourquoi l'élagage est déconseillé.
  Suite **2864 passed / 0 skipped**, inchangée. **Aucun fichier touché** ;
  `desk_data.json` **lu seulement**, jamais écrit ; SW `td-shell-v187` ; écart
  runtime final aucun.

- **Lot 405 — livré** : **aucun octet mort dans `/static` — 54 sur 54 réellement
  référencés.** Balayage textuel, quelques secondes.
  **Pourquoi ça compte** : le service worker met en cache **tout `/static`**
  (règle n°3). Un fichier statique mort n'est donc pas du poids de dépôt — ce
  sont des **octets téléchargés et conservés sur l'appareil de l'utilisateur**,
  plus une entrée de plus dans l'empreinte que le gardien du lot 361 doit
  suivre. Périmètre : **54 fichiers · 824 Ko** (34 `.js`, 17 `.css`, 2 `.woff2`,
  1 `.md`).
  **Instrument validé avant emploi** : recherche du **nom de base** dans tout le
  texte du dépôt (1 218 fichiers), volontairement **large** — `<script src>`,
  `url()` CSS, `@import`, chaîne Python composant le chemin ; chercher un chemin
  exact aurait fabriqué de faux morts. **Témoin positif** :
  `zz-temoin-mort-405.css` déposé dans `vertex/static/vertex/css/` → **seul
  signalé**, aucun des 54 fichiers réels. Témoin supprimé aussitôt, arbre
  vérifié propre.
  **Le zéro rendu substantiel plutôt que décoratif — trois filtres** :
  ```text
  fichiers statiques                                        54
     cités depuis la PRODUCTION (vertex/**, terminal.py)    54
     cités seulement depuis un AUTRE fichier static          0
     cités seulement dans docs/ ou tests/                    0
     cités NULLE PART                                        0
  ```
  Puis le **contrôle de second ordre**, celui qui distingue vraiment : un fichier
  référencé uniquement par un module lui-même mort est mort par transitivité.
  `CLAUDE.md` et les lots 327/381 nomment six modules `vertex/ui/` sans aucun
  consommateur en production. Sur **302 modules de production examinés (dont 6
  connus morts)** : **0 fichier statique n'est cité que par un module mort**.
  Les 54 sont donc tous atteints depuis du code vivant.
  **Ce que ce lot dit du dossier « code mort »** : le poids mort est **dans le
  monolithe Python** — 604 Ko de `PAGE_*` jamais servis (374), `vx_kit.JS` qui
  n'atteint aucune page (381), cinq modules reliques (327) — **pas dans les
  octets servis**. `/static` est propre ; inutile d'y chercher un gain de poids
  en arbitrant les dossiers de rang 3.
  **Portée** : recherche **textuelle par nom de base**. Elle prouve qu'un nom
  apparaît dans du code vivant, pas que la ligne qui le contient soit
  **exécutée**. Aller plus loin supposerait de relever les requêtes réelles d'un
  navigateur sur les 8 pages — donc de lancer le serveur DEMO, donc de fabriquer
  un point dans `breadth_history.json` : coût non justifié pour confirmer un
  zéro déjà filtré trois fois.
  Suite **2864 passed / 0 skipped**, inchangée. **Aucun fichier touché** — le
  témoin créé par la sonde a été supprimé par la sonde, `git status` vide de
  bout en bout ; empreinte SW inchangée ; SW `td-shell-v187` ; écart runtime
  final aucun.

- **Lot 404 — livré** : **les assertions avalées par un `except` — zéro, et le
  zéro est substantiel.** Symétrique exact du lot 403 : celui-ci cherchait les
  tests qui **n'affirment rien**, celui-là ceux qui **affirment, mais dont
  l'affirmation ne peut pas les faire tomber** parce qu'un `except` l'attrape
  (`try: assert … except Exception: pass`). Balayage AST, quelques secondes.
  **Le détecteur** ne signale un `assert` que si les trois conditions tiennent :
  il est dans le **`body`** d'un `try` ; un handler attrape `AssertionError`
  (`except:` nu, `Exception`, `BaseException`, `AssertionError`, ou un tuple en
  contenant un) ; ce handler ne **relance pas** et n'appelle pas `pytest.fail`.
  Exclus à dessein : `except ValueError`, handler qui relance, `try/finally`
  sans handler, `assert` situé **dans** le handler. **Témoin avant emploi** :
  3 fautes plantées signalées, **6 cas légitimes muets**.
  ```text
                          assert au total   dans un `try`   AVALÉS
  tests/                          5 663             91         0
  vertex/                             2              0         0
  terminal.py                         1              0         0
  ```
  **Côté tests, le zéro est substantiel** : 91 assertions vivent réellement dans
  un `try`, et la répartition est sans exception — **91 en `try/finally` SANS
  handler**, le motif de remise en état imposé depuis le lot 387, **0** sous un
  handler attrapant `AssertionError`. Aucun `except` de la suite n'est en
  position de bâillonner une assertion.
  **Côté production, le zéro est trivial — et il faut le dire** : `vertex/`
  contient **2** `assert` en tout, `terminal.py` **1**. Un « 0 avalé » sur
  3 assertions ne prouve presque rien ; le présenter comme un succès serait un
  zéro décoratif.
  **Ce que font ces 3 assertions**, puisqu'on les a comptées : extraction de
  l'Opportunity Brief JS vérifiée à l'import (`terminal.py:5887`) · précondition
  direction LONG (`call_selector.py:21`) · **`assert decision in
  FINAL_DECISIONS`** (`executive_engine.py:161`), qui garde le **vocabulaire
  canonique du verdict final**. Or un `assert` **disparaît** sous `python -O`.
  Vérifié plutôt que supposé : **aucun lanceur n'utilise `-O`** et
  `PYTHONOPTIMIZE` n'apparaît nulle part dans le dépôt — les trois sont actives
  sur tous les chemins de lancement documentés. Ce n'est pas un défaut mais une
  **fragilité latente** ; **classée rang 4**, non corrigée : ajouter une garde
  ici serait le changement gratuit que la boucle s'interdit depuis le 384.
  **Portée** : le détecteur raisonne sur la structure syntaxique — une assertion
  neutralisée par un `xfail`, un `contextlib.suppress` ou une aide capturant
  l'exception ne serait pas vue ; et rien n'est dit de la **justesse** des
  5 663 assertions, seulement qu'aucune n'est muselée.
  Avec le 403, la question « la suite peut-elle échouer ? » est traitée sous ses
  deux angles — assertions **absentes** et assertions **muselées** — les deux
  réponses négatives, les deux dénominateurs mesurés.
  Suite **2864 passed / 0 skipped**, inchangée. **Aucun fichier touché** — ni
  production, ni test, `git status` vide de bout en bout ; SW `td-shell-v187` ;
  écart runtime final aucun.

- **Lot 403 — livré** : **les tests qui n'affirment rien — deux, et tous deux
  légitimes.** Point de contrôle **peu coûteux** délibérément choisi après les
  35 minutes du lot 402 : un balayage AST, quelques secondes. Question : la
  suite contient-elle des tests qui **ne peuvent pas échouer** ?
  Trois familles cherchées : **A** test sans aucune assertion (ni `assert`, ni
  `pytest.raises`, ni appel à une aide locale qui assère) · **B** `assert` sur un
  littéral toujours vrai (`assert True`, `assert 1`) · **C** `assert (cond,
  'message')` — **le tuple**. Un tuple non vide est toujours vrai : la
  parenthèse de trop **annule l'assertion**, et le code se lit comme correct.
  C'est la plus dangereuse des trois.
  **Instrument validé avant emploi** : quatre fautes plantées, toutes détectées ;
  **trois témoins légitimes muets** — un `assert` normal, un test qui délègue à
  une aide assérante, un test à `pytest.raises`. Le détecteur suit **un niveau
  d'indirection**, sans quoi tout test délégant sa vérification aurait été
  faussement accusé.
  ```text
  fonctions test_* analysées                    2 563
     A. sans AUCUNE assertion                       2
     B. assert sur un littéral toujours vrai        0
     C. assert sur un TUPLE                         0
  ```
  **Zéro `assert True`, zéro assertion annulée par une parenthèse.** Résultat
  négatif, mais dénominateur mesuré et instrument prouvé.
  *Note de dénominateur* : 2 563 fonctions pour **2 864** tests collectés —
  l'écart vient des **55 fonctions paramétrées** (59 décorateurs `parametrize`,
  33 à liste littérale soit 152 cas, et **26 dont les cas sont calculés**, non
  énumérables sans exécuter). Je ne prétends pas reconstituer 2 864 par
  l'analyse statique ; je dis d'où vient l'écart.
  **Les deux tests sans assertion** — `test_save_failure_is_silent` et
  `test_save_failure_is_silent_by_contract` — vérifient que `persist.save_json`
  **ne lève pas** quand l'écriture échoue. L'assertion est implicite et
  légitime. Mais ils ont un **angle mort** : ils passeraient aussi si
  `save_json` devenait un **no-op**. Plutôt que de l'affirmer, mesuré —
  `save_json` remplacé par un `return` nu : les **2 tests passent** (aveugles,
  confirmé) tandis que **leurs voisins de fichier tombent**
  (`test_round_trip`, `test_save_load_roundtrip_faithful`). L'angle mort est
  **réel et couvert dans le même fichier** : les durcir n'ajouterait aucune
  protection que la suite n'ait déjà. *Un test sans assertion n'est pas
  nécessairement creux — encore faut-il vérifier qui couvre ce qu'il ne voit
  pas.* Production restaurée à l'octet.
  **Portée** : le détecteur voit les assertions écrites dans le fichier, avec un
  seul niveau d'indirection ; et « 0 littéral toujours vrai » ne dit rien des
  assertions fausses mais non littérales — `assert x == x` passerait au travers.
  Suite **2864 passed / 0 skipped**, inchangée. Aucun fichier touché — ni
  production, ni test ; SW `td-shell-v187` ; écart runtime final aucun.

- **Lot 402 — livré** : **les 300 fichiers rejoués seuls — la suite ne dépend
  pas de son ordre.** Le lot 401 avait prouvé qu'**une** dépendance d'ordre
  existait et l'avait corrigée ; il n'avait pas dit s'il y en avait d'autres.
  Ce lot balaie le périmètre entier : **chaque fichier de test rejoué seul**,
  dans un interpréteur neuf. Aucun code, aucun gardien, aucun test — résultat
  **négatif et mesuré**.
  ```text
  fichiers rejoués SEULS                    300 / 300
     échecs                                   0
     skips                                    0
     tests exécutés en isolation          2 864
     tests de la suite complète           2 864   ← identique
  ```
  L'égalité des deux totaux est le contrôle qui compte : elle prouve qu'aucun
  test n'a été **perdu** en chemin (fichier non collecté, import silencieusement
  cassé). Chaque test a tourné dans les deux régimes, même verdict.
  **L'instrument a échoué une fois — et je l'ai vu avant de conclure.** Le
  premier balayage, lancé en `nohup … &`, n'était **pas mort** quand j'ai cru
  l'avoir arrêté ; un second a écrit dans le même fichier de sortie →
  **339 lignes pour 195 fichiers distincts sur 300**. Un rapport écrit à ce
  moment-là aurait annoncé « 0 échec » sur un périmètre **incomplet de 35 %**,
  en le présentant comme complet. Ce qui l'a révélé n'est pas une intuition mais
  un **contrôle de cohérence interne** : lignes, fichiers distincts et
  dénominateur attendu devaient coïncider — ils ne coïncidaient pas.
  *Un « 0 » n'a de valeur que si le dénominateur est vérifié, pas supposé.*
  Bénéfice secondaire de l'incident : les 202 fichiers passés deux fois donnent
  une mesure gratuite de reproductibilité — **202 verdicts identiques sur 202**.
  Harnais validé avant emploi par un **témoin positif** (fichier délibérément
  faux → `1 failed`).
  **Portée assumée** : ce balayage teste UNE direction — *un fichier a-t-il
  besoin des autres pour passer ?* Il ne teste pas l'inverse (*un fichier
  casse-t-il les suivants ?*, celle du 401, trouvée par un autre chemin), ni les
  ordres intermédiaires. Établi exactement : **isolation complète → vert
  partout**, **ordre nominal → vert**.
  **Un chiffre trouvé en chemin.** Les 300 exécutions isolées tournent avec un
  `persist._BASE_DIR` **réel** — la redirection accidentelle du lot 392 ne
  s'applique pas hors de son module. Effet mesuré :
  `skyler_decisions.json` **11 → 18 entrées**, soit **7 décisions journalisées
  dans le journal réel de l'utilisateur** pour une passe isolée complète ;
  `skyler_memory.json` réécrit, taille stable. Ce n'est pas une piste nouvelle :
  c'est le **dossier de rang 2 du lot 401, désormais chiffré**. Restauré à
  l'octet.
  Suite **2864 passed / 0 skipped**, inchangée. Aucun fichier touché — ni
  production, ni test ; SW `td-shell-v187` ; écart runtime final aucun.

- **Lot 401 — livré** : **un gardien qui passait selon l'ordre d'exécution.**
  Point de contrôle **jamais balayé** : les tests qui mutent un état global sans
  le remettre en état. Le lot 387 en avait trouvé **un**, par hasard ; le
  périmètre entier n'avait jamais été mesuré.
  **Deux instruments, tous deux corrigés avant de servir.** Statique (AST) :
  3 034 fonctions, 50 mutent un global, 36 protégées (`monkeypatch`/`finally`/
  teardown), **14 nues** — mais ce ne sont que des **hypothèses**, une fonction
  d'aide mutante pouvant être appelée depuis un test protégé. Exécution :
  empreinte de l'état global avant/après **chaque** test. Première version :
  **84 « fuites » dont 42 fausses**, parce que `pytest_runtest_teardown`
  s'exécute **avant** les finalizers de `monkeypatch` — corrigé en enveloppant
  `pytest_runtest_protocol`. Témoin négatif qui mordait aussi :
  `PYTEST_CURRENT_TEST` est réécrit à chaque phase, exclu de l'empreinte. Et le
  premier témoin « monkeypatch » écrivait une **valeur déjà présente** —
  écriture idempotente, donc invisible, donc concluante à tort (leçon du 389) :
  rejoué avec une valeur réellement différente et une assertion prouvant la
  mutation effective. **84 → 8 fuites réelles sur 2 864 tests.**
  **La trouvaille.** `test_skyler_sweep_x1.py::test_sweep_route_and_no_journaling`
  restaurait avec `if v is None: scan_state.pop(k, None)`. Or
  `vertex/app/state.py` initialise `'market_ctx': None` : **la clé existe et sa
  valeur légitime EST `None`**. La remise en état la **supprimait** donc du dict
  partagé, pour tout le reste de la session. Prouvé par la plus petite
  reproduction possible — **deux fichiers** : `pytest test_skyler_sweep_x1.py
  test_state.py` → **1 failed**, chacun seul → vert ; idem sur la queue de
  66 fichiers (1 failed / 664 passed). Le test qui tombe est
  `test_scan_state_has_expected_keys` — **le gardien dont le métier est
  exactement de vérifier que les 8 clés documentées existent**. Son verdict
  dépendait de l'ordre d'exécution.
  *Une hypothèse testée et écartée* : j'ai cru que la suite complète passait
  grâce à une seconde fuite laissant `market_ctx` non-`None` ; placer ce fichier
  devant laisse l'échec. Je ne sais pas quel test recrée la clé dans la suite
  complète, et je le dis plutôt que de l'inventer.
  **Corrigé** en mémorisant la **présence** de la clé et non sa vérité. Rouge →
  vert sur les deux périmètres ; **témoin** : ancienne logique remise → rouge à
  nouveau, c'est bien elle qui décidait.
  **Les 7 autres fuites** (gamma_surveillance ×3, market_context, options_routes,
  portfolio_stress, pretrade) : vérifié qu'**aucune ne retire une clé
  documentée** — rejouées ensemble puis suivies du gardien, `72 passed`.
  Pollutions **latentes**, pas défauts actifs ; les corriger à l'aveugle
  changerait ce qu'elles mesurent. **Classées.**
  **Un dossier ouvert, non exécuté (rang 2).** La fixture de portée module de
  `test_refus_variable_lot392.py` — mon propre lot 392 — assigne
  `persist._BASE_DIR = tempfile.mkdtemp(...)` **sans restaurer** : la
  persistance est redirigée pour **678 tests**, 24 % de la suite. Et ce défaut
  **protège** aujourd'hui : rejouée seule avec un `_BASE_DIR` réel, cette queue
  écrit dans `skyler_decisions.json` et `skyler_memory.json`. **Restaurer
  naïvement réintroduirait des écritures réelles dans le stockage de
  l'utilisateur.** Le bon correctif est de décider **où** la persistance doit
  pointer pendant la suite — et ce n'est pas neutre :
  `test_funnel_positions_match_desk` lit délibérément le **vrai**
  `desk_data.json`. Décision, pas réparation.
  Suite **2864 passed / 0 skipped**, inchangée — aucun test ajouté, délibérément.
  Un seul fichier de test modifié ; aucune production ; SW `td-shell-v187` ;
  écart runtime final aucun.

- **Lot 399 — livré** : **qui, dans la suite, sort sur Internet ?** Le lot 398
  avait neutralisé deux sorties réseau au passage, sans savoir s'il en restait.
  Ce lot mesure au lieu de supposer.
  **L'instrument, validé avant emploi.** Plugin pytest à deux capteurs : un
  **faux proxy local** — `HTTPS_PROXY` pointe dessus pendant la session, donc
  tout `CONNECT` y atterrit, **y compris ceux de libcurl/`curl_cffi`**, le
  transport de yfinance, qu'un patch de `socket` **ne verrait pas** — plus un
  patch de `socket.connect` pour les connexions directes. Réponse `502`, aucun
  blocage : la sortie échoue comme hors ligne, le verdict des tests ne change
  pas. **Témoin positif obligatoire** : yfinance capté, `requests` capté, test
  sans réseau muet. *Sans ce contrôle, un « 0 sortie » n'aurait rien valu.*
  **Mesure : 3 sorties sur 2 864 tests.** Test le plus lent : 1,52 s, aucun
  au-delà — mais c'est parce que le proxy échoue vite ; sur une machine
  connectée, les trois aboutissent.
  **(1) `en.wikipedia.org`, à l'IMPORT** — `vertex/data/universe.py` L16 appelle
  `get_index_members()` au niveau module ; sans cache frais, `constituents.py`
  va chercher 3 listes d'indices (**15 s de timeout par requête**) et écrit
  `constituents_cache.json`, soit un **23ᵉ fichier runtime**. Vérifié : couvert
  par `*_cache.json` dans `.gitignore`, **aucun risque de commit**. C'est un
  comportement de **produit**, voulu et documenté — mais il s'applique aussi à
  `pytest`. Je ne touche pas à la production de ma propre initiative :
  **classé en dossier (rang 4)**.
  **(2) `test_company_twin_never_invents`** → yfinance via `_fetch_profile`,
  **qui n'entre dans aucune de ses assertions**. Sortie inutile : neutralisée,
  verdict identique (hors ligne le fetch échouait déjà).
  **(3) `/desc` — le test écrivait dans le dépôt de l'utilisateur.** Et c'est un
  test que **j'ai écrit moi-même au lot 392**. `terminal.py` L1983 : quand le
  fetch yfinance **réussit**, la route écrit `desc_cache.json` **à la racine du
  dépôt** ; le test appelle cette route à chaque passe. Le défaut était
  **doublement invisible** — le réseau échoue ici, et le recensement du lot 389
  ne pouvait pas le voir parce que **l'écriture est conditionnée à la RÉUSSITE
  du fetch** : un recensement statique fait hors ligne ne pouvait pas la relier
  à ce test. *Une écriture conditionnelle au réseau échappe à un recensement
  fait hors ligne.* **Preuve directe sans réseau** (`yf.Ticker` remplacé par un
  faux qui réussit) : sans isolation → racine écrite ; avec l'isolation du
  399 → tmp seulement, racine intacte ; le fichier créé par la sonde a été
  supprimé par la sonde.
  **Corrigé** : `_DESC_PATH` et `_desc_cache` isolés dans ce seul test — la
  route reste la vraie, seule sa destination change. La sortie réseau est
  **conservée délibérément** : ce test existe pour vérifier qu'une réponse
  yfinance réelle sur un symbole inexistant ne remplit aucun champ ; la
  supprimer le réduirait à sa branche hors ligne.
  **Résultat : sorties réseau 3 → 2, écritures dans le dépôt depuis la suite
  1 → 0.** Suite **2864 passed / 0 skipped**, inchangée — aucun test ajouté, et
  c'est délibéré. Aucun fichier de production touché ; SW `td-shell-v187` ;
  écart runtime final aucun.

- **Lot 398 — livré** : **les 2 tests skippés étaient morts depuis leur
  naissance.** Quatrième lot court. Point de contrôle **jamais examiné en
  26 lots** : la suite affiche `2 skipped` depuis des dizaines de rapports —
  personne n'a jamais regardé **lesquels**.
  Ce sont les deux tests de `tests/test_cross_page_consistency.py`, créé le
  **2026-07-12** (`fa234ca`) et **jamais modifié depuis**. Leurs skips sont
  **structurels, pas environnementaux** : `/scan` sérialise `scan_state`, vide
  sous pytest parce qu'**aucun test de la suite ne déclenche de scan** —
  mesure : ce fichier est le **seul des 300** à appeler `/scan`, et ses deux
  appels sont dans le test skippé lui-même. Même mécanique pour
  `options_board`. **Ces deux tests n'ont jamais tourné une seule fois** ; ils
  étaient comptés dans la suite et ne protégeaient rien.
  **Valaient-ils d'être réveillés ?** Mesuré avant de toucher quoi que ce soit,
  par trois mutations de **production** + un témoin, rejouées dans
  l'environnement pytest réel sur le fichier final : filtre `CALL → CALLS` de
  `pulse.py` — le filtre est écrit **deux fois**, `overview.py` L42 et
  `pulse.py` L34, sur le même board → **T2 mord** ; `/api/ticker` servant un
  prix autre que le `detail` du scan → **T1 mord (A)** ; `/scan` transformant
  `rows` sans transformer `detail` → **T1 mord (B)** ; témoin (docstring
  reformulée) → muet. Production restaurée à l'octet entre chaque.
  **Réparés** : une fixture alimente `scan_state` **en place** puis restaure
  dans un `finally` (convention de `test_options_intelligence_lot6.py`, leçon
  du 387) ; les `pytest.skip` conditionnels deviennent des **assertions** — une
  entrée manquante est désormais un échec, plus un silence. Deux effets de bord
  neutralisés dans T1 par `monkeypatch` : `options_pack` (**sortie réseau**) et
  `_company.get` (**écriture de `company_cache.json` depuis la suite**) —
  aucun des deux ne participe à l'invariant, et les laisser aurait réintroduit
  le défaut fermé au lot 389.
  **Résultat : 2862 passed / 2 skipped → 2864 passed / 0 skipped.** La suite
  n'a plus un seul test inerte. Aucun fichier de production touché ; snapshot
  runtime 22 fichiers, écart final aucun ; SW `td-shell-v187`.
  *Limite assumée : T1 tourne sur une entrée injectée — il prouve que les
  routes ne déforment pas ce que le scan produit, pas que le scan produise des
  prix justes.*

- **Lot 397 — livré** : **le registre confronté à lui-même.** Troisième lot
  court — aucun code, aucun gardien, aucun test ; une seule ligne corrigée dans
  un rapport.
  **Point de contrôle jamais fait en 25 lots** : la mémoire de la boucle
  elle-même. Rien ne vérifie le registre, et c'est pourtant lui qu'on relit
  pour décider — une omission y serait **invisible autrement**.
  **Présence : 25 sur 25.** Chaque lot 372→396 a son rapport, sa ligne d'index
  et son bloc STATUS. Mon premier détecteur en signalait **deux manquants** —
  **faux** : les lots 380 et 390 sont des **bilans**, dont le bloc prend la
  forme `## BILAN — veille active, lots N → M` et non `**Lot N — livré**`. Le
  détecteur ne connaissait qu'une forme. *Encore l'instrument avant le
  document.*
  **Exactitude : un écart réel.** La présence ne dit rien de la justesse. La
  chaîne des 25 comptes de suite est **strictement monotone et exacte** — 2645
  au lot 372, 2862 aujourd'hui — sans une seule erreur de transcription en
  25 lots de tenue de registre ; c'est la première fois que c'est vérifié
  plutôt que supposé. Mais **le lot 394 : l'index affirme `v187` alors que le
  rapport ne l'écrit nulle part**, quand les 24 autres l'enregistrent dans
  leurs « Vérifications du cycle ». L'assertion du registre n'était **adossée à
  rien** — vraie par ailleurs, puisque le lot n'a touché aucun octet servi,
  mais invérifiable depuis sa source. **Cette fois ce n'était pas le
  détecteur** : la ligne manquait réellement. Corrigée → **0 écart sur 25**.
  L'écart trouvé est du genre le plus discret qui soit : *un chiffre affirmé
  dans le registre sans source dans le rapport*. Ni la suite, ni les gardiens,
  ni une relecture ne l'auraient révélé, puisque la valeur était juste.
  **Portée** : deux des quatre colonnes confrontées (suite, SW) ; la version du
  cœur est constante et le verdict est déclaratif. Et le contrôle porte sur la
  **concordance interne** du registre, pas sur sa fidélité aux faits.
  Aucun fichier de production touché, écart runtime aucun. Suite **2862 /
  2 skipped, inchangée**. SW v187.

- **Lot 396 — livré** : **les octets servis n'ont pas bougé.** Deuxième lot
  court consécutif — aucun code, aucun gardien, aucun test — et c'est encore
  le bon résultat.
  **Point de contrôle différent de celui du 395**, conformément à la règle
  *un constat se vérifie, il ne se répète pas* : la preuve la plus forte de la
  boucle, non refaite depuis le **lot 390** — le MD5 des 8 pages servies.
  **8/8 IDENTIQUES.** Six lots plus tard, dont deux ayant modifié des fichiers
  de test et un ayant corrigé une docstring, **pas un octet servi n'a bougé**.
  La discipline « aucun fichier de production touché depuis le lot 372 » est
  désormais vérifiée par la mesure, pas seulement affirmée.
  **La sonde a reproduit le dossier de rang 1 du 391 à l'identique** : lancer
  le serveur DEMO pour ce contrôle a ajouté un **17ᵉ point** à
  `breadth_history.json` — `2026-08-09`, `a50 50 · a200 45 · net −4 ·
  health 37`, mêmes valeurs que les seize précédentes. **Le dossier n'est pas
  théorique : il se reproduit à chaque démarrage en mode démo**, y compris
  celui de l'agent. Restauré à l'octet (retour à 16 points).
  Trois fichiers runtime touchés cette fois contre huit au lot 390 — l'écart
  tient à la durée du scan, pas à un changement de comportement ; je ne
  l'interprète pas plus loin.
  **Portée** : le MD5 prouve que le HTML servi est identique, il ne dit rien
  des fichiers `/static` (couverts par l'empreinte du gardien SW, rejouée au
  394), et il vaut pour l'état du dépôt, pas pour ce qu'un utilisateur a en
  cache.
  Serveur arrêté (port 5002 fermé), écart runtime final aucun, arbre propre.
  Suite **2862 / 2 skipped, inchangée**. SW v187.

- **Lot 395 — livré** : **rien à faire, vérifié.** Aucun code, aucun gardien,
  aucun test ajouté — **c'est le résultat, pas un défaut d'exécution**.
  Le 393 a constaté l'épuisement des pistes fines, le 394 l'a confirmé en
  allant vérifier ailleurs. Toutes les veines sont closes **par la mesure** :
  audit des gardiens par mutation (384, 27 mutations → 2 trouvailles) ·
  écritures runtime par la suite (389, 2 trouvailles) · refus API littéraux
  (377, 39 refus / 39 motivés) et construits en variable (392, 30 routes,
  0 muet) · promesses de retour littérales (375) et imbriquées (393, 0 fausse)
  · rejeu des gardiens anciens (394, 7/8 mordent, l'écart était une docstring).
  Un gardien de plus serait le changement gratuit que la boucle s'interdit
  depuis le 384.
  **Mais un constat se vérifie, il ne se répète pas.** Reprendre la liste des
  pistes sans la contrôler serait exactement la faute commise huit fois dans
  cette tranche : faire confiance à ce qu'on transporte. Les deux items
  restants ont donc été re-mesurés. Le commentaire
  « MIROIR EXACT de `__DESK_KEYS` (terminal.py) » est **toujours présent**
  (`vx-entities.js:18`) et **toujours faux** — `__DESK_KEYS` n'existe plus
  depuis la purge É1. Les sites de concaténation sont **conformes** au
  décompte du 374 (4 appels `_extract(PAGE_DAILY, …)`, dont 3 à constantes).
  Aucune dérive entre la mémoire de la boucle et le dépôt.
  **Une asymétrie assumée plutôt que cachée.** Le lot 394 vient de corriger une
  docstring fausse dans un fichier de test ; ce commentaire-ci, du même genre,
  reste différé. La raison n'est pas le coût d'édition mais **l'invalidation de
  cache** : `vx-entities.js` est SERVI, donc le corriger impose un bump de
  service worker, la mise à jour de `_EMPREINTE`, et purge la copie hors-ligne
  de l'utilisateur. Pour un commentaire, c'est disproportionné — et c'est une
  décision, pas un effet de bord de lot. **Règle qui en sort : un énoncé faux
  se corrige immédiatement là où c'est gratuit, et se verse aux dossiers là où
  cela coûte au produit.**
  Arbre propre, **aucun fichier touché** (ni production ni test), écart runtime
  aucun. Suite **2862 / 2 skipped, inchangée**. SW v187.
  **La matière utile n'est plus technique, elle est décisionnelle** : purge des
  7 points MSFT (388) et scan de démo dans `breadth_history` (391) en tête.

- **Lot 394 — livré** : **les gardiens anciens, jamais rejoués — 7 sur 8
  mordent encore.** Une vérification plutôt qu'une piste : le lot 393 ayant
  constaté l'épuisement des pistes fines, ce lot répond à une question laissée
  ouverte par le **bilan n°8** — *« les gardiens non ciblés restent non
  vérifiés »*. **Aucun gardien ajouté**, une seule correction, dans un fichier
  de test.
  **Le dénominateur** : sur 300 fichiers de test, **290 n'ont jamais été
  confrontés à une faute réelle** (179 estampillés d'un lot < 380, 111 sans
  numéro) ; seuls les 10 de la tranche 380-393 l'avaient été au lot 390.
  **L'échantillon, choisi par un critère et non au hasard** : les gardiens que
  `CLAUDE.md` désigne nommément pour ses règles critiques — si l'un d'eux a
  pourri, c'est une règle du produit qui n'est plus tenue. **Mordent** : clé
  retirée de l'ancre `vx_kit` · JS servi rendu syntaxiquement invalide ·
  fichier `/static` modifié sans bump d'empreinte · `sanitize_news` retiré de
  la sortie IBKR · filtre d'URL de la sortie IA neutralisé · rotation des
  sauvegardes desk à 0 · bleu non-marque injecté dans un octet servi. Témoin
  muet, état runtime sans écart.
  **Le huitième ne mord pas — et ce n'est pas un gardien pourri.**
  `test_desk_sync_keys_single_source_of_truth` compare `vx_kit.JS` et
  `journal.JS` et **n'a jamais regardé le fichier statique servi**. Le lot 381
  avait déjà comblé ce trou de couverture avec
  `test_desk_keys_servies_lot381.py`. Ce qu'il n'avait **pas** corrigé, c'est
  la **docstring**, qui affirmait « la source de vérité servie est vx_kit (kit
  global, présent sur toutes les pages) » — **faux depuis le 381**, qui a
  mesuré que ces 21 727 o n'atteignent aucune des 8 pages et que `journal.py`
  est un module mort. Un lecteur ouvrant ce test pour comprendre la règle n°1 y
  lisait le contraire de ce que le dépôt fait. **Corrigée** : elle dit
  désormais ce que le test couvre, ce qu'il ne couvre pas, et renvoie au
  gardien du 381 — les deux sont complémentaires, l'un verrouille l'ancre de
  comparaison, l'autre ce que le navigateur reçoit.
  **Deux ancres fautives corrigées avant de conclure** : `--vx-radius`
  n'existe pas dans `tokens.css`, la première tentative sur la règle n°3 n'a
  donc rien mesuré ; rejouée sur `--vx-canvas`, elle mord. *Une ancre absente
  n'est pas un résultat : c'est une mesure qui n'a pas eu lieu.* Sans cette
  reprise j'aurais annoncé un trou sur le service worker.
  **Portée** : 8 gardiens sur 290, c'est un **sondage**. Ce que le lot établit
  précisément : les gardiens des règles critiques n'ont pas pourri, et le seul
  écart trouvé est une **documentation périmée**, pas une protection perdue.
  Suite **2862 / 2 skipped, inchangée** — aucun test ajouté, délibérément.
  SW v187.

- **Lot 393 — livré** : **les promesses de retour imbriquées — il ne fallait
  pas d'analyseur.** Dernier angle mort déclaré du lot 375, qui écrivait :
  *« vérifier les formes IMBRIQUÉES demanderait un analyseur d'un autre
  ordre »*. **C'était chercher du mauvais côté** : une promesse de retour se
  vérifie en **appelant** la fonction — l'exécution tranche ce que l'analyse
  statique ne sait pas suivre. C'est la vraie trouvaille du lot, et elle porte
  sur la méthode plutôt que sur le code.
  **Dénominateur** : 7 fonctions portent une promesse « Retourne {…} », dont
  **5 couvertes par le 375** (au moins un retour littéral) et **2 déléguées**.
  Le trou déclaré était réel mais **étroit** — le dire évite de faire passer un
  lot mince pour une percée.
  **Verdict, prouvé par exécution** avec les fixtures de la suite et non des
  entrées fabriquées : `grade_packet` promet `{overall, warnings,
  actionable_allowed}` et les rend toutes · `select_calls` promet
  `{per_category, primary, rejected, notes}` et les rend toutes. **Zéro clé
  manquante.**
  **Troisième cas, déjà connu, re-mesuré** : `options_for_position` énumère
  **12 identifiants nus** et son `pack()` interne en rend **13** — `delta` non
  déclaré : **sous-déclaration, pas promesse fausse**. Identique au 375.
  Détail de méthode : ma première extraction cherchait des clés **entre
  quotes** alors que la docstring les écrit **nues** — l'instrument avant le
  code, encore.
  Gardien `tests/test_promesses_imbriquees_lot393.py` (6 tests) : dénominateur
  (si une promesse perdait son retour littéral, elle basculerait dans l'angle
  mort du 375 sans signal) · les deux déléguées **par exécution** · la
  troisième **statiquement** · anti-péremption de la sous-déclaration. ROUGE
  ×3, et **le témoin vaut plus que les trois** : déclarer `delta` — la
  correction que quelqu'un fera un jour — **ne casse pas le gardien**. *Un
  gardien qui punit la correction est pire qu'aucun gardien.*
  **Portée** : lot mince, assumé. Il ne prouve rien sur les promesses formulées
  autrement, et la vérification par exécution ne couvre **qu'un chemin par
  fonction**.
  **Les pistes fines sont épuisées** : refus API littéraux (377) et en variable
  (392), écritures runtime par la suite (389), promesses de retour littérales
  (375) et imbriquées (393) — toutes closes. Ne restent que la concaténation à
  constantes (374, sans enjeu d'honnêteté) et le commentaire périmé de
  `vx-entities.js` (différé : un octet servi pour un gain nul). **Aucune ne
  mérite un lot** ; la matière utile est dans les dossiers du rang 1, en
  attente de décision.
  Suite 2856 → **2862** / 2 skipped. SW v187.

- **Lot 392 — livré** : **les refus construits en variable — l'angle mort
  déclaré du lot 377, mesuré, et PROPRE.** Le détecteur du 377 déballe
  `jsonify(...)` puis exige un dict **littéral** : une réponse assemblée dans
  une variable lui échappe. Il le disait ; ce lot le mesure.
  **Dénominateur resserré par la mesure.** 417 retours littéraux couverts par
  le 377 · **393 par variable** dans l'angle mort — mais **359 sont des aides
  internes** : seuls **34 sont dans une route**, **31 servis**, soit **30
  routes**. *Un dénominateur non trié aurait fait croire à un trou deux fois
  plus grand qu'il n'est.*
  **Verdict prouvé à l'exécution.** Les 30 routes sollicitées avec des entrées
  que le serveur doit refuser — symbole inexistant, corps vide, identifiant
  inconnu — et c'est la **réponse réellement servie** qui est lue, pas le
  code : **12 refus, 12 motivés, 0 MUET**. Les motifs prennent plusieurs
  formes honnêtes (`reason`, `error`, `available: false`, `empty` +
  `generator`, `audit_trail`). Trois réponses sans clé de motif ne sont **pas**
  des refus et n'inventent rien : `/desc` rend des chaînes vides et
  `employees: null`, `/api/positions/state` des zéros avec la note « jamais
  estimés en agrégat », `/api/desk` un `{}`. Une absence rendue comme une
  absence.
  **Deux fois l'instrument en cause.** (a) Ma sonde accusait
  `run_startup_sequence` d'être un refus muet — son motif vit **entièrement
  dans `steps`**, chaque étape portant son statut et son message ; ma liste de
  clés ne contenait pas `steps`. Neuvième fois de la tranche. (b) **Trois
  mutations fautives** sur la preuve ROUGE : `greeks_note` vit dans
  `recalculator.py` et non `positions_api`, `reason` ne vient pas
  d'`analysis_api`, et pour `/desc` j'avais muté une branche **non atteinte**
  — sans réseau, `yf.Ticker` échoue et le chemin servi est l'initialisation du
  dict.
  **Et la mutation corrigée a sali un cache.** Elle a écrit une description
  inventée dans `desc_cache.json`, que le code restauré relisait ensuite : la
  suite restait rouge après restauration. *Restaurer le code ne suffit pas
  quand la mutation a écrit sur disque — il faut vérifier l'état runtime, pas
  seulement l'arbre git.* Fichier supprimé (il n'existait pas avant), écart
  final aucun.
  **Un 22ᵉ fichier runtime découvert par cet incident** : `desc_cache.json`
  n'apparaît qu'après une récupération réussie et manquait aux 21 inventoriés
  depuis le 388. Le gardien livré ne l'écrit pas (avec le code sain, `summary`
  reste vide). Versé aux dossiers.
  Gardien `tests/test_refus_variable_lot392.py` (14 tests) : dénominateur ·
  anti-double-emploi avec le 377 · **LA propriété vérifiée à l'exécution sur la
  réponse servie**, avec une liste large de clés de motif pour ne pas accuser
  un simple renommage (leçon du 383) · rien n'est inventé. ROUGE ×4.
  **Portée** : les 10 routes testées sont celles **prouvées refuser
  aujourd'hui** ; les 20 autres ne sont couvertes que par le dénominateur. Et
  « 0 muet » vaut pour les entrées invalides choisies — un refus déclenché par
  une panne réseau ou l'absence d'IBKR n'a pas été sollicité.
  Suite 2842 → **2856** / 2 skipped. SW v187.

- **Lot 391 — livré** : **un scan de démo écrit dans l'historique breadth
  réel, et servi.** Piste ouverte par une observation non engagée du lot 390.
  **Les données parlaient avant toute manipulation** : `breadth_history.json`
  portait **16 points strictement identiques** — `a50 50 · a200 45 · net −4 ·
  health 37` — du 21/07 au 08/08. La participation réelle d'un marché ne
  reste pas figée seize séances de suite : **signature exacte de la pollution
  GEX du lot 388**, sur un autre fichier.
  **Lien causal prouvé** : scan DEMO → 16 puis 17 points, date ajoutée
  `2026-08-09`, valeurs identiques aux seize précédentes. Le site d'écriture
  est **inconditionnel** — aucun test de `DEMO_MODE` — et il ne fait pas
  qu'ajouter : `if _bh[-1]['d'] == _today: _bh[-1] = _snap` **écrase** le
  point du jour. Une démo lancée après un scan réel **remplace la mesure du
  jour**.
  **Et c'est servi** : `/scan` rend 17 points dans `internals.history`, que
  `markets_page.py` consomme pour « Tendance de participation » — dont le
  commentaire du code dit « historique breadth **RÉEL** ». Pendant une
  session de démo l'utilisateur est prévenu (`vx-demo-banner`,
  `source = 'demo'`), **mais le point persisté ne porte aucune provenance** :
  lors d'une session réelle ultérieure, sans bannière, les points de démo
  sont servis au milieu des vrais, indistinguables. Le contre-exemple honnête
  existe dans le dépôt : `market_context_last.json` **est** écrit avec un
  champ `demo`.
  **Aucun fichier de production modifié, délibérément.** Mesuré : **aucune**
  persistance du dépôt ne garde `DEMO_MODE`. Ajouter ce garde serait une
  **décision de conception** — ne pas persister en démo, marquer le point, ou
  assumer que la démo peuple l'historique — pas la réparation d'une
  incohérence. Le dossier part au **rang 1**. La purge des 16 points déjà
  accumulés relève de la même décision.
  **Une part de cette pollution vient de la boucle** : ses vérifications de
  tranche lancent le serveur DEMO. Le rituel de copie de sûreté et de
  restauration adopté aux lots 388-390 **a arrêté cette contribution** — le
  point du 09/08 créé par la mesure a été restauré, retour à 16 points. Ce qui
  demeure n'en dépend pas.
  Gardien `tests/test_persistance_demo_lot391.py` (7 tests) : il verrouille
  les **mécanismes de distinction qui existent** — jamais le défaut, car un
  gardien figeant l'absence de marqueur accuserait la correction future
  (leçon du 383). ROUGE ×6, et **le témoin est le test le plus important du
  lot** : ajouter `'demo': DEMO_MODE` au point persisté — *la correction
  probable* — **ne casse pas le gardien**. Une ancre a dû être corrigée
  (`vx-demo-banner` apparaît 4×).
  **Portée** : le gardien est statique ; les autres caches touchés par une
  démo (`daily_prev`, `skyler_memory`) **n'ont pas été analysés** — ce lot
  traite le cas le plus grave, pas la famille.
  Suite 2835 → **2842** / 2 skipped. SW v187.

- **Lot 389 — livré** : **les deux dernières écritures de test, et une
  mesure qui piégeait.** Deux questions laissées ouvertes au 388.
  **(1) Vérifier mon propre énoncé.** J'avais écrit que les 3 fichiers
  restants « ne changent qu'un horodatage » — contrôlé seulement au
  **premier niveau de clés**. Diff **feuille à feuille** (aplatissement
  récursif) après la suite complète : **exactement une feuille modifiée
  par fichier** — `.as_of`, `.ts`, `.age_s`, `.generated_at` — aucune
  perdue, aucune ajoutée. L'énoncé tient ; il repose désormais sur la
  bonne mesure.
  **(2) Le piège.** `skyler_sessions.json` **n'a pas bougé** de
  l'exécution. Conclusion tentante : « personne n'écrit ». **Fausse.** Le
  point du jour existait déjà : l'écriture est **idempotente**, et la
  croissance est d'un point **par JOUR**, pas par exécution. En retirant
  le point du jour avant chaque essai, elle redevient observable — la
  règle du 387 appliquée à l'envers : *« rien ne bouge » ne vaut que si
  l'on s'assure qu'il y avait quelque chose à observer.*
  **Le périmètre était encore quatre fois trop large** : 8 fichiers
  mentionnent SKYX/TSTQ, **2 seulement écrivent** — `test_skyler_core` et
  `test_xss_exits_lot177`, tous deux via `/api/skyler/<sym>` qui
  journalise une séance. Corriger les 8 aurait été six changements
  gratuits.
  **Correction** : redirection de `persist._BASE_DIR` dans les deux tests
  concernés. **Aucune production touchée.** Effet vérifié : **5 → 4
  fichiers runtime touchés**, `skyler_sessions.json` sort de la liste ; les
  4 restants sont exactement ceux dont le diff récursif prouve qu'ils ne
  changent qu'un horodatage.
  **Gardien étendu, pas dupliqué** : `test_caches_runtime_lot388.py`
  passe de 5 à **9 tests** — même propriété qu'au 388, un fichier jumeau
  aurait été du bruit. Ajouts : les 2 entrées au recensement, un anti-vide
  sur la journalisation de séance, et la borne `MAX_SESSIONS = 400`.
  ROUGE ×4 + témoin muet.
  **Deux fois l'outil en cause.** (a) **Mon témoin a mordu** : je
  renommais `SESSIONS_FILE` en croyant faire un changement anodin — c'est
  une `AttributeError` en production, et le recensement l'a signalée comme
  un **13ᵉ site**. Le gardien avait raison, le témoin était faux. (b)
  **Mon anti-vide était creux — la faute du lot 386, refaite** :
  `'SESSIONS_FILE' in src` alors que la chaîne apparaît **6 fois** pour
  **2 sites** d'écriture ; en retirer un laissait le test vert. Réécrit
  par AST. *Avoir la règle écrite ne suffit pas à ne pas la re-violer ;
  c'est la preuve ROUGE qui l'attrape.*
  **Portée** : les 4 fichiers encore touchés le sont **aujourd'hui** sur un
  horodatage — caractérisation datée, rien ne l'impose au code. La
  pollution historique (7 points MSFT, points SKYX/TSTQ déjà accumulés)
  n'est **pas** nettoyée : donnée runtime de l'utilisateur, sa purge est
  une décision.
  **La veine « écritures runtime par la suite » est close** : ouverte au
  386, mesurée au 387, élargie au 388, terminée ici — deux trouvailles
  réelles sur trois lots. Suite 2831 → **2835** / 2 skipped. SW v187.

- **Lot 388 — livré** : **la suite écrivait un point fabriqué par jour dans
  l'historique GEX réel.** Le lot 387 avait traité `desk_data.json` et
  n'avait regardé que celui-là. Ce lot applique la même méthode aux **vingt**
  fichiers runtime du dépôt — pas aux quatre supposés.
  **Mesure : 7 sur 20 touchés par la suite.** Trois horodatages seuls
  (`ai_enrichment`, `session_digest_cache`, `weekly_snapshot`) ·
  `desk_data.json` (connu du 387, `data` byte-identique) ·
  **`desk_backup_20260809.json` CRÉÉ** — ce que le 387 n'avait qu'annoncé
  (« la suite consomme le créneau quotidien ») est désormais **mesuré** ·
  `skyler_sessions.json` (tickers synthétiques) · et
  **`gex_history_cache.json`, sur MSFT — un VRAI titre**.
  **La faute.** `test_options_gex_route_real_numbers` sème un board
  d'options **fabriqué** (MSFT, strikes 460/420, spot 440) puis appelle
  `/api/options/gex/MSFT` ; la route **journalise le profil** via
  `gex_history.record()` dans le vrai fichier, la fixture ne redirigeant
  rien. Mesuré : **8 points MSFT strictement identiques** (net_gex
  36 784 000, spot 440.0, zero_gamma 429.6), un par exécution de la suite —
  alors qu'ACN et ADBE portent des valeurs variées et n'ont pas bougé. La
  comparaison interne au fichier suffit à distinguer le fabriqué du mesuré.
  **Ce fichier est SERVI** : `options_intel_api.py` le lit pour
  `/api/options/gex-radar`. Des chiffres de test étaient donc rendus comme un
  historique mesuré, **sur un titre réellement détenu** — invariant n°4, cette
  fois sur un vrai symbole et non un ticker de test.
  **Correction** : redirection de `persist._BASE_DIR` vers un dossier
  temporaire dans **le seul test concerné** — périmètre établi en rejouant
  les 19 tests du fichier **un par un** depuis un état restauré à l'octet,
  pas par intuition. **Aucune production touchée.**
  **Effet vérifié : 7 → 5 fichiers runtime touchés, MSFT 7 → 7 points.**
  Gardien `tests/test_caches_runtime_lot388.py` (5 tests) : anti-vide sur la
  journalisation (sinon la redirection n'a plus d'objet), bornes
  anti-croissance (`_MAX_SYMBOLS` évince les plus anciens : un symbole
  réinjecté en boucle chasserait un vrai symbole), propriété de redirection,
  anti-péremption, **recensement des 12 sites de production**. ROUGE ×4 +
  témoin muet.
  **Un recensement opaque ne recense rien** : mon premier détecteur rendait
  « ? » pour toute cible non triviale et comptait **8** sites ; rendu
  explicite il en trouve **12**, et surtout il nomme `SESSIONS_FILE` — le
  fichier même qui accumule les tickers de test. Borne fixée sur la vraie
  mesure. Même leçon qu'aux 385 et 387 : *un dénominateur mesuré par un outil
  myope est un faux dénominateur.*
  **Non corrigé, versé aux dossiers** : SKYX/TSTQ dans `skyler_sessions.json`
  (8 fichiers, tickers synthétiques non confondables, bornés à 400 — dégât
  d'une autre nature) et la **purge des 7 points MSFT pollués**, qui est une
  décision de l'utilisateur et non un effet de bord de lot.
  Suite 2826 → **2831** / 2 skipped. SW v187.

- **Lot 387 — livré** : **un test pouvait effacer les notes du trader.**
  Le 16ᵉ dossier ouvert au lot 386 est traité — et son verdict prudent
  (« la suite réécrit `desk_data.json` mais sans perte ») était incomplet.
  **Le dénominateur a été trois fois trop étroit avant d'être juste** :
  `grep desk/push` → 4 fichiers, `grep desk_data` → 15, et c'est **mon
  propre gardien** qui en a trouvé **17** (les deux manquants postent sur
  `/api/desk` sans jamais nommer `desk_data`). Mesure empirique, chaque
  fichier rejoué depuis un état de référence restauré à l'octet :
  **16 sur 17 n'écrivent pas** dans le vrai desk — 12 redirigent
  (`persist.cache_path` **ou** `persist._BASE_DIR`), 1 pousse 3 Mo rejetés
  en 413 avant la route, 3 ne font que lire — et **un seul écrit**.
  **La faute.** `test_desk_roundtrip_is_faithful` lit le desk réel,
  **écrase `myNotes`** par un marqueur, pousse, vérifie, puis restaure.
  `myNotes` n'est pas une clé de test : c'est une **clé synchronisée**,
  `{"NVDA": "note"}`, les **notes par titre du trader**, présente dans les
  trois listes de sync avec ses accesseurs. La restauration n'était **pas**
  protégée. Prouvé par mutation, l'assertion de fidélité inversée :
  `note rendue = False`, contenu laissé `{"guard": "lot84-guard-…"}` —
  **définitivement**, et le filet ne rattraperait rien puisque le lot 362 a
  établi que le snapshot quotidien est pris avant la première écriture,
  créneau que la suite consomme.
  **Pourquoi le lot 386 n'avait rien vu** : l'utilisateur n'a **aujourd'hui
  aucune note** (6 clés, `myNotes` absente). Le chemin de perte existait
  sans matière à perdre. *Un « aucune perte constatée » ne vaut que si l'on
  vérifie qu'il y avait quelque chose à perdre* — le pendant exact de la
  règle du dénominateur.
  **Correction** : un `try/finally` dans `tests/test_desk_cycle_lot84.py`
  — **fichier de test, aucune production touchée**.
  Gardien `tests/test_desk_ecritures_lot387.py` (9 tests) : dénominateur ·
  aucune écriture du vrai desk sans redirection · anti-péremption ·
  **`finally` verrouillé par AST** et remise en état devant repousser `d0` ·
  exemption **vérifiable et bornée au nombre de sites** · `myNotes` doit
  rester une clé servie. Preuve ROUGE ×4 + témoin muet.
  **Trois fois l'outil était en cause.** (a) Ma première mutation ne mordait
  pas : `assert cond, ('msg' and False)` — le `and False` portait sur le
  **message**, pas la condition. (b) Mon premier gardien **accusait deux
  fichiers sains** — `test_desk_routes.py` redirige par `_BASE_DIR`, un
  second mécanisme valide que mon détecteur ignorait, et
  `test_production.py` est rejeté en 413 avant la route ; *un gardien qui
  accuse du code sain finit désactivé*. (c) Mon exemption portait sur le
  **fichier** : la preuve ROUGE a montré qu'un écrivain ajouté après coup y
  passait — resserrée au **nombre de sites**, gelé à la mesure.
  **Portée** : le risque était conditionnel (assertion en échec **et**
  utilisateur ayant des notes) ; aucune perte réelle n'a eu lieu. Ce lot
  supprime le **chemin**, pas un dégât constaté. Le gardien est **statique**
  — il lit le code des tests, il n'observe pas leurs écritures.
  Desk vérifié après la suite : `data` **identique à la référence**, seul
  `ts` diffère. Suite 2817 → **2826** / 2 skipped. SW v187.

- **Lot 386 — livré** : **les 38 `except: pass` de `terminal.py`, lus un
  par un** — le lot 379 l'avait fait pour les 46 de `vertex/`, le 385 avait
  montré que le recensement s'arrêtait à cette frontière. Classement par ce
  que le `try` ENTOURE : nettoyage/fermeture 6 · journal/persistance 10 ·
  import/config optionnel 2 · infra thread 2 · **absence honnête 16** ·
  examinés de près 2. Les trente-six premiers sont sans danger pour
  l'invariant n°4 : un échec y produit une **absence**, jamais une valeur
  inventée.
  **L621 — l'overlay IBKR : honnête au moteur, muet au produit.**
  `_apply_ibkr_indices()` écrase les indices différés yfinance par les
  valeurs temps réel et marque chaque entrée `src = 'ibkr'` — le
  commentaire dit même « provenance temps réel (honnêteté §4) ». Le
  mécanisme est complet et correct. **Mais il n'atteint aucune surface
  servie** : mesuré, `markets_page.py` et `briefing.py` lisent
  `.price/.change/.spark` et **jamais `.src`** ; le seul rendu de « TEMPS
  RÉEL IBKR » vs « yfinance différé » du dépôt est dans `PAGE_ME`,
  **l'une des 7 constantes `PAGE_*` MORTES du lot 374** ; et
  `indices_live` part au client via `/scan` mais **aucun code ne le lit**.
  Ce n'est pas une malhonnêteté — un cours différé reste un cours réel —
  c'est la catégorie du lot 382 : **un énoncé du code plus large que ce
  que le produit délivre**. La pièce réellement fragile est **la fenêtre
  de fraîcheur de 75 s** : l'élargir servirait des valeurs périmées comme
  du temps réel. Verrouillée, avec le marqueur, pour qu'un affichage
  futur ait quelque chose de vrai à lire.
  **L1342 — `bret = 0.0` : mesuré, pas excusé.** J'allais l'innocenter en
  disant que 0 est le neutre. `analysis.py:54` dit le contraire :
  `rs = clip(50 + (sym_ret − bench_ret) × 200, 0, 100)` → 40 devient 70,
  16 devient 40, 50 devient 90. **La force RELATIVE devient une
  performance ABSOLUE** — exactement le piège du lot 378 avec
  `entry_quality`. Trois faits l'empêchent d'être une faute : `0.0` est le
  défaut **déclaré** (atteint aussi sans exception si `bi <= 63`), le
  chemin de scan **vivant** passe un `bench_ret` réel, et aucune page
  servie ne lit `scan_state['edge']`. **Caractérisation, pas correction**
  — jumelle du dossier `context()` du 379.
  Gardien `tests/test_pass_terminal_lot386.py` (11 tests) ; preuve
  ROUGE ×5. **Un test creux démasqué par sa propre preuve ROUGE** : mon
  anti-dérive testait `'< 75' in src`, or la chaîne apparaît **4 fois**
  dans `terminal.py` — élargir la fenêtre à une heure laissait le test
  vert. Réécrit pour lire la constante **dans le corps de la fonction,
  par AST**.
  **Trouvaille adjacente — la suite de tests écrit dans les données du
  desk.** Mesuré : `desk_data.json` est **réécrit** par la suite complète
  (md5 f30f5d7da49a → c6beebcf97f0). **Aucune donnée perdue** — 6 clés
  avant et après, `data` byte-identique, seul `ts` change. Mais le lot 362
  a montré qu'un push **partiel** remplace le blob entier et qu'un push
  `data: {}` est **accepté** : un futur test effacerait des clés en
  silence, et le filet ne rendrait que l'état d'avant la première écriture
  du jour. **16ᵉ dossier**, non engagé — et piste recommandée pour le 387.
  Aucun fichier de production touché. Suite 2806 → **2817** / 2 skipped.
  SW v187.

- **Lot 385 — livré** : **le recensement des replis s'arrêtait à
  `vertex/`**. Parti compter les 38 `except: pass` « autres » du lot 379,
  je suis tombé sur la frontière avant de tomber sur les handlers. Le
  gardien 378 tient l'invariant n°4 — *un `except` qui renvoie un nombre
  substitue une valeur plausible à une donnée manquante* — avec un
  `RACINE = 'vertex'` en dur. **Mesure : 254 handlers dans `vertex/`,
  113 hors, dont 101 dans `terminal.py`** : **31 % des handlers de
  production hors du filet**, dont tout le monolithe qui sert encore des
  routes.
  **Trou prouvé, et distingué d'un gardien inutile.** Un
  `except: return 50` NEUF dans `terminal.py` — exactement ce que la
  propriété 378 interdit — passe les 2 793 tests. Le témoin seul ne
  suffisait pas (deux « AUCUN » côte à côte pourraient vouloir dire que
  le gardien ne sert à rien) : **contrôle décisif**, le même défaut mot
  pour mot dans `vertex/engines/stats.py` **MORD**. Le gardien fait donc
  précisément ce que son code dit — **ce n'est pas une myopie, c'est sa
  frontière**, la catégorie exacte du trou du lot 381.
  **Les trois replis existants de `terminal.py` sont honnêtes, pour deux
  raisons différentes.** `_seed_fund_from_company` → `0` est un compteur
  exact (le nombre EST la mesure). `_i` → `0` et `_f` → `0.0` sont de
  vrais substituts — vérifié sur valeurs réelles,
  `_i(None) = _i('abc') = _i(NaN) = 0` — mais **le site d'appel les
  écarte** : `if iv <= 0 or oi <= 0: continue`. **C'est ce garde-fou, et
  non la coercition, qui tient l'invariant** ; s'il disparaissait, un
  repli entrerait dans la médiane d'IV ATM et le GEX **servis**. C'est la
  seule pièce fragile des trois, désormais verrouillée — ainsi que le
  fait que les coercitions n'aient pas essaimé, puisque toute la
  démonstration repose là-dessus.
  Gardien `tests/test_replis_racine_lot385.py` (13 tests) : dénominateur
  d'abord, LA propriété portée hors `vertex/`, anti-péremption, borne de
  dérive **fixée À la mesure** (38), **anti-rot du périmètre** forçant la
  décision sur tout nouveau module racine, exclusions vérifiées non
  importées par la production. Preuve ROUGE ×3, toutes sur le **vrai
  fichier de production** — la faute du lot 383 ne s'est pas reproduite.
  **Un risque de test évité** : ma première version appelait
  `_seed_fund_from_company()`, sans écriture ici *parce que le cache est
  plein sur cette machine* ; sur un cache incomplet elle aurait sauvegardé
  un fichier runtime depuis un test. `_save_json` est interceptée et le
  test échoue si une écriture est tentée.
  Aucun fichier de production touché, aucun fichier runtime muté
  (`fund_cache.json` inchangé, vérifié par `mtime`). Suite 2793 →
  **2806** / 2 skipped. SW v187. Suite : les 38 `except: pass` de
  `terminal.py` lus un par un, seule piste fine portant encore une
  question d'honnêteté non tranchée.

- **Lot 384 — livré** : audit des gardiens par mutation, **quatrième et
  dernière passe — 6 sur 6, aucun trou**, et la veine se ferme sur ce
  résultat. **Mordent** : snapshot quotidien du desk désactivé ·
  garde-fou de taille du snapshot neutralisé · redirection héritée
  `/heatmap` supprimée · entrée Options retirée de `PRIMARY_NAV` ·
  `/healthz` vidé de son contenu réel · collecte de `/api/client-log`
  neutralisée. Le **témoin négatif** (commentaire reformulé) reste muet,
  ce qui donne son sens au 6/6.
  **Bilan honnête de la veine, quatre lots, ~27 mutations utiles** :
  381 → 1 trou + 1 constat · 382 → 1 écart · 383 → 0 · 384 → 0. **Les
  deux trouvailles sont concentrées dans les deux premiers lots**, avec
  un protocole pourtant plus rigoureux à chaque passe : c'est le signal
  convenu au 383, **la veine est épuisée, je la ferme plutôt que de m'y
  acharner**.
  **L'actif réel** : dix-sept invariants sont désormais **prouvés tenus
  par mutation**, non plus supposés — READONLY, service worker (recul de
  version ET fichier `static` sans bump), les trois listes de clés de
  sync, `sanitize_news` sur deux sorties, filet desk (rotation, snapshot,
  garde-fou), navigation (redirection héritée, registre), observabilité
  (`/healthz`, `/api/client-log`), vocabulaire des verdicts, apostrophes
  françaises servies, nom personnel, `scan_state`, plancher de version du
  cœur. Avant cette tranche, aucun de ces énoncés n'avait été vérifié
  autrement que par la présence d'un test au vert — **et un test au vert
  qui ne mesure rien est plus dangereux qu'un test absent**.
  **Rien touché, délibérément** : aucun fichier de production, **aucun
  test ajouté** — il n'y a rien à corriger, et ajouter un gardien là où
  6 mutations sur 6 sont déjà attrapées serait le changement gratuit que
  la boucle s'interdit. Un seul item mineur **volontairement différé** :
  le commentaire « MIROIR EXACT de `__DESK_KEYS` (terminal.py) » en tête
  de `vx-entities.js`, faux depuis la purge É1 — le corriger changerait
  un octet **servi**, donc imposerait bump SW, invalidation de cache,
  `_EMPREINTE` et preuve MD5 complète. Disproportionné pour un
  commentaire.
  **Portée** : 27 mutations sur 2 793 tests restent un **sondage**.
  « MORD » = « attrape CETTE faute-là ». Ce que je conclus, c'est que
  *cibler les invariants critiques ne rend plus rien*, pas que la suite
  entière est saine. Suite **2793 / 2 skipped inchangée**. SW v187.
  **Le vrai goulot reste les quinze dossiers en attente de décision
  humaine** — 604 Ko de HTML mort assemblés à chaque import, le filet
  desk qui perd le travail de la journée, les deux questions d'honnêteté
  jumelles (363 et 379), `vx_kit.JS` servi nulle part.

- **Lot 383 — livré** : audit des gardiens par mutation, **troisième
  passe** — et cette fois **aucun trou**. C'est un résultat, pas une
  absence de résultat. **Mordent** : apostrophes déséchappées dans un
  bloc JS **servi** · nom personnel injecté dans une page servie ·
  `scan_state` réassigné dans un **consommateur** · **recul** de version
  du cœur (0.9.0 → 0.8.0). Le **témoin négatif** ne mord pas, comme
  attendu.
  **Deux « AUCUN GARDIEN » qui accusaient à tort.** (a) Ma première
  mutation `scan_state` visait `vertex/app/state.py` — or c'est le
  `HOME` déclaré du gardien, **exclu du scan par conception** puisque
  c'est le domicile légitime de l'affectation ; rejouée dans un
  consommateur, la violation tombe immédiatement. (b) Passer
  `demo_mode=DEMO_MODE` à `False` ne change **aucun octet servi** —
  `/system` rend le même MD5 (73e917c0f2d0, 82 837 o) — alors que
  `DEMO_MODE` vaut bien `True` au runtime : la mutation était effective
  dans la source mais n'atteint pas la page. Mutation invalide, pas un
  trou. Deux fois sur trois le « AUCUN » initial était faux : *un cas
  qui ne mord pas accuse d'abord la mutation*.
  **Seul écart relevé : un PLANCHER, pas une égalité.** « skyler_core
  0.9.0 intact » suggère l'égalité ; le gardien impose `>= (0, 9, 0)` —
  un recul échoue, un bond en avant passe. C'est la catégorie « gardien
  plus étroit que l'énoncé » du lot 383, **mais ici la règle réelle est
  la bonne** : monter est légitime, régresser ne l'est pas. Rien à
  corriger dans le code ; l'énoncé gagne à être dit précisément, et le
  gardien le fixe.
  **Un faux gardien écarté avant livraison.** Ma première version
  testait la parité des quotes simples dans le JS servi : elle échouait
  sur **5 pages sur 8** alors que le code est sain (les quotes vivent
  aussi dans des chaînes doubles, des regex, des commentaires). Un
  gardien qui accuse du code sain finit désactivé — remplacé par la
  vérification que le vrai parseur `node --check` couvre encore les
  8 pages servies. Le bon outil existait déjà.
  Gardien `tests/test_invariants_reellement_imposes_lot383.py`
  (14 tests) ; preuve ROUGE ×3, dont un cas d'abord **non mordant parce
  que j'avais muté mon propre fichier de test** au lieu du gardien
  historique. Aucun fichier de production touché. Suite 2779 → **2793** /
  2 skipped. SW v187. **Bilan de la veine : deux écarts sur trois lots,
  et zéro ici — si un lot de plus ne trouve rien, changer de veine.**

- **Lot 382 — livré** : audit des gardiens par mutation, **seconde
  passe**, protocole durci après les trois mutations fautives du 381
  (ancre unique, mutation vérifiée effective, code muté vérifié SERVI).
  J'ai ajouté un **témoin négatif** — une modification anodine qui ne
  doit PAS faire tomber la suite — pour que les « MORD » veuillent dire
  quelque chose : il se comporte comme attendu.
  **Quatre protections lourdes tiennent** : `sanitize_news` retiré de
  `/news-feed` **et** de la construction des événements, rotation des
  sauvegardes desk ramenée à 0, et un fichier `vertex/static` modifié
  **sans bump d'empreinte** — tous mordent.
  **Un trou** : un `#ff00ff` en dur dans le shell **servi** passe les
  2 767 tests. Tentation immédiate d'accuser le gardien couleur de
  myopie — **vérifié avant d'accuser**, par mutation ciblée : `#1e6fd9`
  (bleu non-marque) MORD, `#ff00ff` et `#c0392b` passent. Le gardien
  balaie bien `vertex/ui/**`, shell compris, et fait **exactement ce que
  son nom annonce**. Ce n'est pas lui qui ment : c'est `CLAUDE.md` qui
  annonçait « tokens/VXChartTheme uniquement, **aucun littéral
  couleur** ».
  **Mesure : 265 littéraux `#RRGGBB` distincts dans `vertex/ui/**`, dont
  53 atteignent une page SERVIE** (répartis sur une dizaine de modules).
  L'énoncé était donc faux depuis longtemps, et exiger zéro casserait la
  suite sans rien améliorer. **Verdict : le code respecte la règle
  réelle — c'est l'énoncé qui était faux, et le contrat qui n'était
  verrouillé nulle part.**
  Livré : gardien `tests/test_litteraux_couleur_servis_lot382.py`
  (12 tests — anti-vide avec dénominateur, **borne de dérive fixée À la
  mesure** (55 pour 53), règle réelle vérifiée sur les **octets servis**
  là où le gardien historique lit les sources, anti-péremption du
  périmètre) ; plus une section « Couleurs — la règle réellement tenue »
  dans `CLAUDE.md`, chiffres à l'appui. Preuve ROUGE ×4 — les quatre
  fautes passaient toutes la suite avant ce lot. Aucun fichier de
  production touché. Suite 2767 → **2779** / 2 skipped. SW v187.
  **Deux lots, deux écarts doc/réalité au même endroit** : les
  invariants annoncés dans `CLAUDE.md`. La piste suivante s'impose —
  vérifier systématiquement chaque règle critique contre ce qu'un
  gardien impose vraiment.

- **Lot 381 — livré** : ouverture de la veine décidée au bilan 380 —
  **auditer les GARDIENS eux-mêmes, par mutation**. 291 fichiers de test,
  2 756 tests dont nul n'avait vérifié qu'ils voient ce qu'ils prétendent.
  Protocole : muter le code protégé puis lancer **toute la suite** — la
  question n'est pas « ce gardien-ci mord-il ? » mais « **un** gardien
  mord-il ? ». Sept sondages sur les gardiens que `CLAUDE.md` nomme comme
  protégeant les règles critiques.
  **Bonne nouvelle d'abord** : **READONLY**, le **service worker**, le
  **vocabulaire des verdicts** et **DESK_KEYS de vx_kit** mordent tous.
  Les invariants lourds sont réellement tenus, et ce n'était pas acquis.
  **Mais un trou, sur la règle critique n°1** — celle dont `CLAUDE.md`
  dit « sinon un push l'efface côté serveur » : retirer `vxAlerts` du
  **repli servi** de `/system` passe **les 2 754 tests**.
  **Et en cherchant pourquoi, le constat le plus grave.** Mesure page par
  page : **`vx_kit.JS` (21 727 octets) n'est servi sur AUCUNE des
  8 pages**, alors que la doc le décrivait comme « kit global présent sur
  toutes les pages » et **source de vérité** des clés. Tableau réel : sur
  les **deux listes réellement servies** — `vx-entities.js` (statique,
  32 464 o, chargé par les 8 pages) et le repli inline de `/system` —
  **une seule était gardée** ; les deux autres listes gardées (`vx_kit`,
  `journal`) n'atteignent pas le navigateur. La chaîne tient encore par
  comparaison, mais elle est **ancrée sur un module candidat à la
  purge** : le jour où il part, la référence s'en va et la liste servie
  non gardée reste.
  **Trois fausses pistes en chemin, toutes de mon fait** : `.replace(…,1)`
  a frappé la mauvaise occurrence deux fois, et une mutation visait un
  bloc **servi nulle part**. Dans un lot dont le sujet est « les gardiens
  mentent-ils ? », c'est l'outil qui a menti trois fois — *un cas qui ne
  mord pas accuse d'abord la mutation*. La passe corrigée exige une ancre
  **unique** et vérifie que la ligne visée a changé.
  **Livré** : gardien `tests/test_desk_keys_servies_lot381.py` (13 tests)
  qui garde les listes **par ce qu'elles SERVENT** (contrat complet et
  aucune clé inventée dans le repli, `vx-entities.js` vérifié tel que
  servi, les 8 pages le chargent, les deux listes servies identiques, et
  le fait `vx_kit` non servi **ancré**) ; plus la **correction de la
  règle n°1 de `CLAUDE.md`**, qui annonçait trois listes servies dont
  deux ne le sont pas. Preuve ROUGE ×4 — les quatre fautes passaient
  toutes la suite avant ce lot ; un cas d'abord **sauté** (espaces après
  virgules), signalé puis corrigé. Aucun fichier de production touché
  (`CLAUDE.md` est de la documentation, non servie) : pas de preuve MD5
  requise, pas de bump. Suite 2754 → **2767** / 2 skipped. SW v187.

- **Lot 379 — livré** : les 46 `except: pass` **jugés** — le lot 378 les
  avait comptés en déclarant explicitement ne pas les juger — **plus les
  matériaux du bilan 380**. Classement par ce que le `try` ENTOURE :
  3 nettoyage, 5 journal/persistance, 38 lus un par un (imports
  optionnels, lecture du `.env`, écritures de cache, calculs métier).
  Mon classificateur automatique en laissait 38 sur 46 « à lire » : il
  n'a pas fait le travail, et je le dis plutôt que de maquiller le
  résultat. Les cinq blocs de `market/context.py` n'écrivent que dans
  `out[...]` et des locales → un échec produit une **absence**, jamais
  une valeur périmée servie.
  **Hypothèse sérieuse formée, puis RÉFUTÉE par la mesure.**
  `analysis.py:229` recalcule `grade` après que `score` a été ajusté,
  sous `except: pass` : en cas d'échec, un grade calculé sur l'ANCIEN
  score serait servi à côté du NOUVEAU — deux champs incohérents, qu'aucun
  gardien existant n'attraperait. Vérification : `config.grade` ne lève
  pour **aucun** nombre (0, 1, 50, 99, 100, −5, 105, 50.5, NaN, ∞) et la
  ligne 228 garantit un `int` : **le handler est inatteignable**,
  l'incohérence ne peut pas se produire.
  **Et la sonde a trouvé à côté ce qui vaut plus que la piste.** En
  vérifiant que `context()` dégrade bien par absence, j'ai mesuré son
  comportement sur univers vide : il est **mixte**. `vix`, `vix_band`,
  `vix_chg`, `spy_regime`, `spy_adx`, `spy_trend_txt` valent `None` —
  honnête. Mais `roro` affirme **'NEUTRE'**, `roro_gap` vaut **0**,
  `breadth` sort tout à zéro et `verdict` annonce « MARCHÉ · NEUTRE ·
  participation 0% au-dessus MM50 ». Ce n'est PAS un `except` qui
  avale : le bloc **réussit**, parce que ses propres défauts
  (`ro = np.mean(…) if any(…) else 50`) le font aboutir sur zéro donnée.
  Sur un univers vide, l'application **affirme** donc un régime au lieu
  de dire qu'elle ne sait pas. **Caractérisation GELÉE, pas corrigée** —
  toucher au moteur de contexte sans accord serait le changement gratuit
  que la boucle s'interdit, et la question est **jumelle du dossier
  ouvert au lot 363**. Versée aux dossiers en attente.
  **Verdict : sain, rien touché.** Gardien
  `tests/test_pass_et_contexte_lot379.py` (24 tests : périmètre,
  anti-vide et borne de dérive, écriture dans `out[...]` seulement,
  `config.grade` total sur 10 valeurs, anti-dérive de la garantie `int`,
  6 champs honnêtes en `None`, 4 champs affirmatifs gelés) ; preuve
  ROUGE ×4 — le premier cas d'abord **non mordant**, mais c'était **ma
  mutation** qui était inopérante (définition écrasée par la vraie), pas
  le gardien : *un cas qui ne mord pas accuse d'abord la preuve*.
  Aucun fichier de production touché. Suite 2730 → **2754** / 2 skipped.
  SW v187 inchangé. **Matériaux du bilan 380 consignés** : tableau des
  dix lots, +144 tests sur la tranche, 9 gardiens, 1 seule faille réelle
  (372) et 1 seul lot touchant la production (MD5 0/8), SW v187 sur les
  dix lots, et le fil rouge des **douze fois où l'outil était en cause**.

- **Lot 378 — livré** : les **exceptions comme convention de refus**,
  angle mort déclaré au lot 377. Risque produit : un `except` qui avale
  une erreur transforme une donnée manquante en **blanc muet**, ou pire
  en **chiffre plausible**. Mesure : **254 handlers** — 124 replis nus
  (48,8 %), 66 autres, **46 `except: pass`**, 17 marqués, 1 avec trace.
  Le chiffre de 124 fait peur mais mon classement confondait deux choses
  opposées : ce que le handler **renvoie** tranche — **`None` 70**
  (contrat « valeur ou None » : parfaitement HONNÊTE, l'appelant affiche
  `—`), et seulement **12 NOMBRES**, seule famille qui menace
  l'invariant n°4.
  **Première correction, et elle est d'un genre nouveau.** Deux des
  douze renvoient **50** (`quant_engine.entry_quality`). J'allais les
  innocenter : 50 est le point de départ de la fonction (`s = 50.0`) et
  le défaut de ses entrées, donc « le neutre déclaré de l'échelle ».
  **Exécution faite, c'est FAUX** : à entrée vide la fonction rend
  **76**, pas 50. `s = 50.0` est un point de départ interne, pas une
  sortie naturelle — le repli est bien un score plausible,
  **indiscernable d'une mesure**. C'est la **première fois de la boucle
  que la vérification sur valeurs réelles m'empêche d'INNOCENTER du
  code** ; d'habitude elle m'empêche d'en accuser.
  **Verdict : CARACTÉRISATION, pas de faute prouvée.** Le chemin est
  défensif (il exige un `d` non-dict, alors que les appelants passent
  des lignes de scan) et je n'ai trouvé aucune entrée réelle qui
  l'atteigne — modifier un moteur de scoring sur un défaut non démontré
  serait le changement gratuit que la boucle s'interdit. Ce que le lot
  livre, c'est le **recensement gelé** : aucun nouveau repli numérique
  ne pourra apparaître en silence.
  **Seconde correction, sur mon propre gardien.** La preuve ROUGE a
  d'abord répondu **NE MORD PAS** au cas « `raise` privé de son
  message » : ma tolérance de 3 muets reposait sur un chiffre annoncé de
  2, quand la mesure au critère du gardien donne **39 `raise`, 1 seul
  muet**. Borne ramenée à la mesure. **Une borne qui absorbe la première
  régression n'est pas une borne** — c'est la même illusion de confort
  que la myopie découverte au lot 377.
  Observation versée aux dossiers : `opportunities_api._followed_count`
  et `_positions_count` renvoient `0` sur exception, rendant « desk
  illisible » et « desk vide » indiscernables (portée limitée : la route
  consommatrice marque bien ses propres erreurs, 500 + `error`).
  Gardien `tests/test_replis_exception_lot378.py` (9 tests : périmètre,
  anti-vide, recensement gelé et justifié, anti-péremption, bornes de
  dérive qui rendent visible sans juger, caractérisation vérifiée **en
  exécution**, `raise` muets ≤ 1) ; preuve ROUGE ×5, restauration
  identique à l'octet — deux cas d'abord **sautés** puis corrigés sur
  les vraies lignes, un troisième d'abord **non mordant**, ce qui a
  révélé la borne trop lâche. Aucun fichier de production touché, donc
  pas de preuve MD5 requise. Suite 2721 → **2730** / 2 skipped. SW v187
  inchangé.

- **Lot 377 — livré** : les autres conventions de refus — **et la
  découverte que le gardien du lot 376 n'en voyait qu'un TIERS.**
  Volume mesuré sur 1321 fonctions : `return None` **242** (absence de
  valeur ordinaire, PAS un refus — non décidable, et je ne prétends pas
  le trancher), `return []` 28, `return {}` 13,
  `{available: False}` 13, `{ok: False}` 4.
  **Le vrai défaut n'était pas dans le code mais dans le PÉRIMÈTRE du
  gardien précédent.** Il ne regardait que `return <Dict>` ; or la
  majorité des refus d'API sont **enveloppés** —
  `return jsonify({...})`, souvent `jsonify({...}), 400` — donc portés
  par un `Call` ou un `Tuple`, jamais un `Dict`. Ils étaient **tous**
  invisibles : **13 vus sur 39 réels, soit 33 % de couverture**. Et les
  26 manquants sont précisément **les plus exposés** : les refus servis
  en JSON au navigateur, ceux que l'interface montre à l'utilisateur.
  **12ᵉ fois de la boucle que le périmètre de l'outil ment, et la
  première où c'est un gardien DÉJÀ FUSIONNÉ qui se révèle myope** — le
  code était sain, le test au vert, et le vert ne voulait pas dire ce
  qu'on croyait. Un gardien myope est plus dangereux qu'une absence de
  gardien, puisqu'il rassure. Périmètre corrigé : **39 refus,
  39 motivés, 0 muet**, confirmé sur les réponses réellement servies
  (`error='question vide'`, `err='nom invalide'`). Cas voisin vérifié
  avant de crier au loup : `/api/skyler/<sym>` répond 200 sans clé
  d'état pour un symbole inconnu, mais sert une décision complète avec
  un `audit_trail` énumérant ce qui manquait — **la traçabilité EST le
  motif**, pas un refus muet. Discipline des contrats à deux visages
  mesurée avec son dénominateur : **37 fonctions mixtes existent, 0 ne
  porte de clé d'état** dans sa branche riche. **Verdict : sain, rien
  touché** — ce que ce lot corrige, c'est la **couverture**. Gardien
  `tests/test_refus_api_lot377.py` (9 tests, dont celui qui verrouille
  la leçon : **le déballage doit voir strictement plus que le détecteur
  naïf, écart ≥ 10** — si l'écart tombe, c'est le gardien qui est
  redevenu myope, pas le code qui a changé) ; preuve ROUGE ×5,
  restauration identique à l'octet, dont **la myopie elle-même rejouée**
  en retirant le déballage. Aucun fichier de production touché, donc pas
  de preuve MD5 requise. Suite 2712 → **2721** / 2 skipped. SW v187
  inchangé.

- **Lot 376 — livré** : les docstrings qui décrivent leur retour **en
  prose** — angle mort déclaré au lot 375. Consigne appliquée :
  **mesurer le volume AVANT de promettre un verdict**, précisément parce
  que le lot 375 s'était fait piéger par un « 0 » sans dénominateur.
  Mesure : 1321 fonctions, 674 avec docstring, 51 parlant de retour,
  6 structurées (lot 375), **45 en prose**, dont **2 seulement**
  mécaniquement vérifiables — et **les deux sont de faux positifs** :
  `premium`, `model`, `iv` sont des **paramètres d'entrée**, `cost` un
  champ du board ; mon heuristique prenait tout mot entre backticks pour
  une clé de retour. **11ᵉ fois de la boucle que l'outil est le premier
  suspect, et 4ᵉ d'affilée où mon détecteur accuse du code sain.** Une
  docstring en prose ne marque pas ce qu'elle décrit : **piste close par
  la mesure**, pas par un vert de complaisance.
  **Mais la lecture a exhibé un contrat autrement plus utile, et lui
  parfaitement décidable** : `analyze_strategy` promet « entrée
  insuffisante ou invalide => `{'available': False, 'reason',
  'refusals': [{field, value, why}]}` ». C'est **l'invariant produit n°4
  de Vertex sous sa forme code** — donnée absente → motif honnête,
  jamais un blanc. Un `available: False` sans motif est un refus
  **muet** : l'interface affiche un vide que l'utilisateur risque de
  lire « rien à signaler » au lieu de « je ne sais pas ». Mesuré :
  **13 refus dans le paquet, 13 motivés, 0 muet**, et confirmé sur
  **valeurs réelles** (leçon du lot 374) — motifs français explicites,
  dont « prime manquante sur une jambe — pas de P&L inventé ».
  **Verdict : sain, rien touché** ; ce que le lot ajoute, c'est
  l'invariant : aucun refus futur ne pourra être muet. Gardien
  `tests/test_refus_honnete_lot376.py` (9 tests : périmètre, anti-vide
  avec dénominateur explicite, la propriété avec un message d'échec qui
  dit POURQUOI c'est grave, 4 refus provoqués en réel avec exigence d'un
  motif d'au moins 12 caractères et non numérique, anti-dérive de la
  docstring qui fait de ce comportement une promesse, pas-trop-strict
  avec anti-péremption) ; preuve ROUGE ×4, restauration identique à
  l'octet — le cas décisif étant le **motif vidé en chaîne vide**, qui
  passe un contrôle de présence de clé et n'est attrapé que par le test
  sur valeurs réelles. Aucun fichier de production touché, donc pas de
  preuve MD5 requise. Suite 2703 → **2712** / 2 skipped. SW v187
  inchangé.

- **Lot 375 — livré** : les promesses des docstrings de **FONCTIONS** —
  le gardien du lot 366 ne couvrait que celles des **modules**. Même
  veine que les lots 365 (PORTFOLIO_FIT annoncé, jamais évalué) et 368
  (promesse d'échappement fausse). **Deux volets, deux résultats
  différents — et le second est le plus instructif.**
  **Volet 1, les promesses de forme de retour : SAINES, prouvé.** Six
  fonctions portent un contrat `Retourne {…}` ; sur **toutes** leurs
  branches `return {littéral}` — 14 au total — **aucune clé annoncée ne
  manque**. La collecte statique de CHAQUE branche s'est révélée plus
  forte qu'un test d'exécution : `assess` a une **sortie anticipée**
  (bid/ask absent) qui renvoie 3 clés là où le chemin normal en renvoie
  4 — un appel unique n'aurait jamais visité cette branche, et c'est
  précisément elle que la preuve ROUGE fait échouer. Trois
  sous-déclarations relevées (`spread_pct`, `entry`, et `delta` dans la
  forme imbriquée de `pack()`) et **volontairement non corrigées** : ce
  sont des enrichissements, pas des promesses fausses. Le gardien
  n'exige donc PAS l'égalité exacte — l'imposer le rendrait intenable
  dès qu'une branche d'erreur renvoie le socle minimal, et un gardien
  qui crie au loup finit désactivé (leçon du lot 374).
  **Volet 2, les promesses en un seul mot majuscule : NON DÉCIDABLES.**
  359 mots majuscules distincts cités en docstring de fonction, **0
  introuvable** dans le paquet — mais ce zéro est **vide de sens** :
  l'échantillon (`ACHETER`, `ATTENDRE`, `ATTAQUE`, `ARBITRAIRE`) montre
  que sans underscore, un mot majuscule dans une docstring française est
  presque toujours une **emphase**, pas un identifiant, et le filet les
  déclare tous « trouvés ». Le lot 366 avait heurté le même mur dans
  l'autre sens (139 faux positifs). Annoncer « 0 problème » ici serait
  un faux vert : **piste close par la mesure**, pas par un vert.
  **10ᵉ correction de méthode, et 3ᵉ d'affilée où c'est MON détecteur
  qui accuse du code sain** : `ast.walk` descendait dans la fonction
  imbriquée `pack()` et attribuait ses 13 clés à
  `options_for_position`, qui en annonce 4 — une violation de trois clés
  entièrement imaginaire. Règle retenue : quand un audit signale une
  faute grossière dans du code mûr, **l'outil est le premier suspect**.
  Gardien `tests/test_promesses_retour_lot375.py` (10 tests : périmètre,
  2 anti-vide, la propriété, pas-trop-strict avec anti-péremption,
  **anti-ré-attribution verrouillant ma propre faute**, 4 contrats
  épinglés nommément contre la dérive silencieuse d'une docstring) ;
  preuve ROUGE ×4, restauration identique à l'octet — le premier cas
  d'abord **sauté** faute de motif, signalé par le script puis corrigé
  sur la vraie ligne. Aucun fichier de production touché, donc pas de
  preuve MD5 requise. Suite 2693 → **2703** / 2 skipped. SW v187
  inchangé.

- **Lot 374 — livré** : les blocs `<script>` **assemblés par
  concaténation** — l'angle mort que le lot 373 avait lui-même déclaré.
  **Il existe bel et bien** : 15 chaînes littérales déséquilibrées, soit
  4 points de concaténation. Trois n'assemblent que des constantes de
  module (`_OPP_BRIEF_JS`, `_sync_ui.JS`, `_VX_JS_FULL`, `ART_JS`) ; le
  quatrième — `terminal.py::_vpage`, qui fait
  `'…</div><script>' + js + '</script>…'` — est le seul à recevoir un
  **paramètre**. **Verdict : sain, rien touché — mais pour une raison de
  ROUTAGE, pas de code.** Ses 7 appelants passent tous une constante
  évaluée à l'import, et surtout **les 7 pages ainsi construites ne sont
  plus servies** : `/bordel`, `/review`, `/research`, `/heatmap`,
  `/equipe`, `/settings`, `/health` renvoient un **301** vers les pages
  du redesign (table `_LEGACY` de `redesign.py`). Contrôle croisé sur
  les octets servis : balises équilibrées sur les 8 pages (10 à
  18 paires). Comme la sûreté dépend d'un fait de routage et non d'une
  propriété du code, le gardien **ancre explicitement ce fait**.
  **Deux corrections de méthode, et les deux portaient sur MON PROPRE
  GARDIEN** (8ᵉ et 9ᵉ de la boucle). Ma première version exigeait que
  `js` soit un littéral : elle accusait `_BORDEL_JS`, qui concatène en
  fait trois constantes de module — détecteur trop étroit, corrigé en
  résolution transitive. Toujours rouge : deux de ces constantes sont
  produites par `_extract(PAGE_DAILY, …)`, donc constantes **à
  l'import** mais pas littérales au sens statique. J'ai alors compris
  que l'invariant syntaxique était le **mauvais outil** — la propriété
  qui protège n'est pas « `js` est un littéral » mais « **la valeur de
  `js` ne contient pas de balise fermante** », vérifiée sur les valeurs
  réelles. Les deux fois, mon gardien accusait du code sain : l'erreur
  **symétrique** de celle qu'on redoute d'habitude, et tout aussi
  coûteuse — un gardien qui crie au loup finit désactivé. **Constat de
  poids mort, mesuré et NON engagé** : ces 7 constantes représentent
  **618 527 octets (604 Ko) de HTML assemblés à chaque import** de
  `terminal.py` pour n'être jamais renvoyés (import : 1,91 s) —
  candidat naturel pour les purges É2/É3, **dossier en attente de GO**.
  Gardien `tests/test_script_concatene_lot374.py` (21 tests : 3
  anti-vide, la vraie propriété sur les valeurs réelles, complément
  statique interdisant un `js` calculé par requête, équilibre des
  balises sur les 8 pages servies avec exigence de ≥ 8 blocs, le fait de
  routage dont dépend le verdict, anti-péremption si la purge a lieu) ;
  preuve ROUGE ×4, restauration identique à l'octet — avec la précision
  honnête que le cas 2 remonte en **erreur de collecte**, pas en échec
  d'assertion. Aucun fichier de production touché, donc pas de preuve
  MD5 requise. Suite 2672 → **2693** / 2 skipped. SW v187 inchangé.

- **Lot 373 — livré** : la faute du lot 372 sous ses **autres habillages**
  — f-strings, `%`-format, et tous les producteurs de HTML, pas seulement
  les gabarits `%%…%%` de trois pages. **Verdict : aucune faille
  exploitable, rien touché — mais un danger latent trouvé et verrouillé.**
  **7ᵉ correction de méthode de la boucle, et la plus instructive** : ma
  première passe listait les fichiers avec `os.listdir`, qui **ne descend
  pas dans les sous-dossiers**. `vertex/ui/shell/__init__.py` — le
  producteur HTML **central**, celui qui assemble les 8 pages — n'a
  jamais été lu, et c'est exactement là que se trouvait la trouvaille.
  Première fois que c'est mon **périmètre de balayage**, et non ma
  logique, qui mentait. Passe corrigée en `os.walk` :
  `vertex.engines.recommendation.vocab_js()` est un `json.dumps` **nu**
  injecté dans `<script id="vx-vocab">window.__VXVOCAB={…}</script>`,
  donc **sur les 8 pages** — l'endroit le plus exposé de l'application.
  Il ne tient aujourd'hui que parce que `_labels_map()` n'assemble que
  des tables littérales du module (`DECISIONS`, `HELD`, `_ALIAS`) : les
  3 689 octets servis ne contiennent **ni `<`, ni `>`, ni `&`**, et
  **rien ne le vérifiait**. Une seule étiquette future avec un `<`
  ferait sortir le script sur les huit pages à la fois. **Durcissement
  mesuré puis écarté avec raison** : `vocab_js` sérialise en
  `ensure_ascii=False` alors que `json_for_script` laisse la valeur par
  défaut — l'appliquer transformerait tous les accents en `\uXXXX`,
  changerait les octets servis sur les 8 pages et imposerait un bump SW,
  pour **zéro gain** puisque le contenu n'a aucun caractère de balise.
  C'est l'**invariant** qui protège ici, pas le durcissement. Les deux
  `%%VIEW%%` restés bruts (`markets_page`, `performance_page`) vivent
  dans `const VIEW='%%VIEW%%'` — une chaîne JS entre apostrophes, dont
  une charge s'échapperait — mais tiennent par la **liste blanche
  appliquée avant la substitution** ; sondés 4 charges × 2 routes sur
  des rendus réels de 55-70 Ko : 0 fuite, `VIEW='overview'` partout.
  Gardien `tests/test_contexte_js_lot373.py` (27 tests : anti-vide,
  **anti-angle-mort verrouillant la faute de mon propre outil**,
  exceptions justifiées **et** anti-péremption, invariant vocab sur les
  8 pages, gardien pas-trop-strict) ; preuve ROUGE ×3 (étiquette avec
  `<`, liste blanche retirée, `json_for_script` remplacé par un
  `json.dumps` nu), restauration identique à l'octet — le 1ᵉʳ cas a
  d'abord été **sauté** faute de motif correspondant, signalé plutôt que
  tu. Aucun fichier de production touché, donc pas de preuve MD5
  requise. Suite 2645 → **2672** / 2 skipped. SW v187 inchangé.

- **Lot 372 — livré** : les **interpolations serveur** dans le `page_js`
  des pages, dernière grande surface non auditée de la veine sécurité.
  **VRAIE FAILLE XSS TROUVÉE ET CORRIGÉE — la plus grave de la boucle.**
  Audit AST : 35 interpolations dans les `render*`, dont 4 envoient du
  JSON dans un bloc `<script>`. `/opportunities` reçoit
  `params=request.args` et n'en filtre que les **CLÉS** (`sym`, `sector`,
  `setup`, `decision`) ; les **VALEURS** partaient nues dans
  `json.dumps`, qui échappe `"` et `\` mais **ni `<` ni `/`**. Donc
  `?sym=</script><img src=x onerror=…>` **ferme le script et injecte du
  HTML actif** : 8 injections confirmées sur un rendu réel (4 clés ×
  2 charges, HTTP 200, pages de 66 Ko). Contrairement à la faille du
  lot 368 — qui exigeait que le moteur produise un symbole hostile —
  celle-ci est **déclenchable à distance par un simple lien**, dans une
  session qui a accès au desk local. Les 6 autres pages recevant des
  paramètres d'URL : aucune fuite. Corrigé par
  `vertex.ui.shell.json_for_script` (`<`, `>`, `&` → `\uXXXX`, relus à
  l'identique par un moteur JS, donc comportement client inchangé),
  appliqué aux **4** sites pour rendre le contrat vérifiable
  statiquement ; sonde rejouée **16/16 saines**. **6ᵉ correction de
  méthode** de la boucle : mon premier détecteur comptait comme
  « actif » un `<img>` resté **à l'intérieur** d'un `<script>` non
  refermé — où il est inerte — et gonflait le résultat. Gardien
  `tests/test_json_script_lot372.py` (35 tests : anti-vide, charges ×
  clés, préservation du comportement, gardien pas-trop-strict, contrat
  statique dont un test qui vérifie que le détecteur mord) ; preuve
  ROUGE ×2 (faute historique rejouée, correctif affaibli), restauration
  identique à l'octet. **MD5 0/8 divergence** malgré 3 fichiers de
  production touchés ; navigateur réel 0 erreur console sur filtre
  légitime, filtre secteur et charge hostile. Tranché au passage : les
  plages « smoke » de ces scripts mesurent le **DOM hydraté** (4662 pour
  `/opportunities`) alors que le script mesure le **HTML brut** (410) —
  deux grandeurs sans rapport ; ce smoke n'a jamais rien prouvé, seul le
  MD5 porte la preuve. Suite 2610 → **2645** / 2 skipped. SW v187
  inchangé.

- **Lot 371 — livré** : `/memory/cell/<group>/<key>`, la **route sœur**
  de la faille du lot 368 — même fichier, même auteur, même motif de
  rendu, donc forte probabilité du même défaut. **Verdict : SAINE, et
  prouvé sur des cellules réelles.** **Correction de méthode d'abord
  (la 5ᵉ de la boucle)** : ma première sonde écrivait les résultats sous
  la forme `{'hit': bool}` → **aucune cellule formée**, 404 partout,
  donc des « non » rassurants et **vides** — exactement le piège du
  lot 368. La vraie forme d'un résultat mesuré est
  `{'horizons': {'H5'|'H20'|'H60': {'status': 'MESURE', 'return_pct'}}}`
  (cf. `_measured_class`) ; sans horizon MESURE, aucune cellule n'existe.
  Sonde corrigée : **4 cellules rendues en 200 (~19 Ko)** avec des
  records hostiles, dont `by_regime` **dont la clé EST la charge**
  — elle traverse alors **à la fois l'URL et la donnée** : 0 charge
  brute, 0 balise active, `<title>` unique et clos, version échappée
  présente. **Pourquoi cette route tient là où l'autre a cédé** : son
  `title=` est une **constante** (`'Cellule de calibration'`) alors que
  la faille du lot 368 venait d'un titre nourri par la donnée, et chaque
  valeur du corps passe par `markupsafe.escape`, y compris la clé
  reconstruite. **Rien touché.** Gardien
  `tests/test_memoire_cellule_lot371.py` (5 tests) sur une mémoire
  **temporaire** — dont un **anti-vide** qui exige ≥4 cellules formées,
  pour que la fixture ne puisse plus tourner à vide en silence — et un
  test qui exige que le titre **reste** une constante. Preuve ROUGE ×2,
  dont la faute du lot 368 **transplantée** dans cette route (titre
  nourri par la donnée → 3 tests rouges). Aucun fichier de production
  touché → pas de preuve MD5 requise, pas de bump (`td-shell-v187`).
  Suite 2605 → **2610 / 2 skipped** verte (+5). Piste (a) — les
  interpolations serveur dans le `content=` de chaque page — reste
  ouverte et demande son propre lot.

- **Lot 370 — livré** : CHECKPOINT de la tranche 360-369. Serveur DEMO
  (`/scan` 20 lignes, `source=demo`) : **les 8 MD5 sont identiques aux
  références** — aucun octet servi n'a bougé de toute la tranche,
  cohérent avec dix lots dont **un seul** a touché un fichier de
  production (lot 368, une ligne d'échappement, dans une route hors des
  8 pages). Navigateur réel (Chromium 1194, 1440×900, après
  hydratation) : **0 erreur console, 0 `pageerror`** sur les 8 pages.
  **Unique écart, et c'est ma plage qui était fausse** : `/markets`
  mesure **2794**, soit exactement la **référence historique** — la
  plage `2795-2835` que j'avais construite autour des 2814 du lot 360
  excluait la référence elle-même. Erreur de construction, pas une
  régression (le MD5 identique le prouve) ; plage corrigée en
  **2790-2835**. Au passage, cela reconfirme la conclusion du lot 360 :
  le smoke dépend du jeu DEMO régénéré par session (2814 puis 2794 pour
  des octets identiques). **Bilan de tranche** : **1 vraie faille XSS
  trouvée et corrigée** (368 — titre du post-mortem non échappé), 3 trous
  (361 périmètre du SW, 364 gardiens emportés par la purge É1, 367 liste
  blanche non gardée), 1 divergence doc-vs-code (365 PORTFOLIO_FIT), et
  **3 verdicts « sain » étayés** (363 règle n°4 prouvée en navigateur,
  366 isolée sur 110 moteurs, 369 18/18 étiquettes sûres).
  **9 gardiens neufs**, suite **2530 → 2605 / 2 skipped (+75)**,
  **10 PR fusionnées** (#392 → #401), SW **`td-shell-v187` inchangé**
  toute la tranche, `main` jamais touchée. **Leçon dominante** :
  vérifier l'outil avant de conclure a changé le résultat **quatre
  fois** (367 le diff, 368 les charges avec `/` bloquées en 404
  Werkzeug, 369 la page d'erreur au même MD5, et ce lot-ci la plage mal
  construite).

- **Lot 369 — livré** : ÉTIQUETTES DU SHELL — suite directe de la faille
  du lot 368. Audit de **tous** les appels `render_shell` : **44
  étiquettes constantes** (sûres par construction) et **18
  interpolées**, tracées **une par une** jusqu'à leur source →
  **18/18 sûres** : `analysis_page` filtre explicitement les caractères
  (`safe = ''.join(ch for ch in sym if ch.isalnum() or ch in '.-')`),
  toutes les autres lisent `label`/`sub` dans un **dict de vues** après
  normalisation, et `options_intel` normalise `view` dès la première
  ligne. **La faille du lot 368 était isolée.** Asymétrie structurelle
  documentée : le chemin **fragment** échappe les 4 étiquettes
  (`escape(…, quote=True)`), le chemin **page complète** n'en échappe
  **aucune** — `<title>{title}`, `<b>{space_label}</b>`,
  `<span>{sub_label}</span>` et surtout
  `data-page-label="{page_label or space_label}"`, **dans un attribut**,
  où un simple guillemet suffirait à sortir. Cause identifiée :
  `from html import escape` est un import **local à
  `_render_fragment`** — l'échappement n'existe que là où l'import
  existe. **Le dossier en attente de GO est désormais CHIFFRÉ** :
  durcissement appliqué temporairement puis restauré (MD5 du fichier
  vérifié) → **7 pages sur 8 inchangées à l'octet près**, seule `/`
  bouge parce que son titre est `"Aujourd'hui"` et que l'apostrophe
  devient `&#x27;` — **visuellement identique**, coût réel = un bump SW
  + une nouvelle référence MD5 pour `/`. **Rien engagé** : la décision
  reste vôtre, mais avec le chiffre. **Correction de méthode (encore
  une)** : ma première mesure annonçait « 8/8 pages changeraient » avec
  le **même MD5 sur les 8** — absurde pour 8 pages différentes ; c'était
  une page d'erreur (`NameError`, `escape` hors de la portée de son
  import local). Sans ce doute, j'aurais rapporté un chiffre faux et
  peut-être fait renoncer à un durcissement quasi gratuit. Gardien
  `tests/test_etiquettes_shell_lot369.py` (**27 tests**) : 3 charges ×
  7 routes via `?view=` et via le segment, `<title>` reste unique et
  clos, aucun `data-page-label` ne contient `"` ni `<`, plus deux tests
  de contrat (le fragment échappe ; la page complète reste le seul
  chemin non échappé — à mettre à jour le jour du durcissement). Aucun
  fichier de production touché → pas de preuve MD5 requise, pas de bump
  (`td-shell-v187`). Suite 2578 → **2605 / 2 skipped** verte (+27).

- **Lot 368 — livré** : SEGMENTS DE CHEMIN — **une vraie faille XSS
  trouvée et corrigée**. Jumelle du lot 367, mais sur les segments
  (`/analysis/<sym>`, `/memory/<id>`), du texte libre donc plus exposé.
  **Correction de méthode d'abord** : ma première sonde envoyait des
  charges contenant `/` — Werkzeug refuse `%2F` dans un segment et rend
  son 404 par défaut (701 octets), la charge n'atteignait **jamais** le
  rendu ; 28 lignes de « non » rassurants et vides. Refaite sans barre
  oblique : 18 requêtes sur 42 rendent alors une vraie page.
  **(1) Le symbole est sain, doublement protégé** :
  `/analysis/"><img src=x onerror=alert(1)>` → 200, 75 216 octets,
  `const SYM="IMGS"` (non-alphanumériques **retirés** avant injection JS)
  et texte **échappé** (`&lt;`, `&quot;`, `&gt;`) ; redirections
  `/titre/` et `/company/` **relatives** (pas de redirection ouverte) ;
  CRLF refusé par Werkzeug. 0 fuite sur 6 charges × 7 gabarits.
  **(2) `/memory/<decision_id>` : FAILLE RÉELLE.** La page (200,
  19 371 o, 1 bloc inline qui parse, 35 `id` sans doublon) est celle que
  le lot 359 signalait comme non couverte. Sa docstring promet « TOUT
  contenu de la mémoire est ÉCHAPPÉ (XSS) » — **c'était faux pour le
  titre** : le corps utilisait bien `markupsafe.escape`, l'argument
  `title=` de `render_shell` l'avait oublié. Mesuré : un symbole
  `</title><script>alert(1)</script>` **sort de la balise** et injecte
  un **`<script>` actif dans le `<head>`**. **Portée dite franchement** :
  le `symbol` vient du moteur de décision (univers contrôlé), pas d'une
  saisie utilisateur ; l'exploitation suppose d'écrire dans
  `skyler_memory.json`, fichier local — **pas exploitable à distance**,
  mais défense en profondeur absente et **promesse fausse dans la doc du
  code**. **Corrigé en une ligne** (`_e(rec.get('symbol'))` dans le
  titre) : ce n'est pas implémenter une fonctionnalité manquante
  (règle du lot 365), c'est faire tenir au code une promesse qu'il
  affichait déjà. Gardien `tests/test_segments_url_lot368.py`
  (**12 tests**, record hostile injecté dans une mémoire **temporaire** —
  le vrai `skyler_memory.json` jamais touché) ; **une assertion du
  gardien était elle-même trop stricte** (elle refusait `onerror=alert`
  même échappé, donc inerte) → corrigée pour ne viser que la forme
  exécutable. Preuve ROUGE sur la faute réelle (correctif retiré →
  2 tests rouges). Fichier de production modifié → preuve exigée :
  **MD5 des 8 pages, 0 écart / 8** → pas de bump (`td-shell-v187`).
  Suite 2566 → **2578 / 2 skipped** verte (+12). Piste ouverte : auditer
  **tous** les `render_shell(title=…)`, même classe de défaut ; le
  durcissement de fond (échapper le titre dans `render_shell`) toucherait
  toutes les pages servies — en attente de GO.

- **Lot 367 — livré** : VARIANTES `?view=` — les gardiens JS ne balayent
  que les routes **nues** ; les variantes servent-elles du JS jamais
  parsé (le trou du lot 359, en plus grand) ? **37 variantes découvertes
  en lisant les onglets du HTML servi** — ma liste tirée d'un grep du
  code n'en voyait que **25** (elle manquait `?view=learnings`,
  `progression`, `events`, `positioning`, `impacts`, `macro`) :
  première correction de méthode, **découvrir depuis le servi, pas
  depuis la source**. Ces variantes servent **16 blocs `<script>`
  inline absents des routes nues** — soit un trou 4× celui du lot 359.
  **Puis le diff a démenti la piste** : entre une route nue et sa
  variante, **2 lignes d'écart** — `const VIEW="team"` → `const
  VIEW="risk"` — le JavaScript est identique au reste près. Une faute de
  syntaxe s'y verrait sur la route nue, déjà balayée par le lot 182.
  **Il n'y a pas de trou** ; un gardien qui reparse 16 quasi-doublons
  aurait coûté du temps pour rien. (`/intelligence`, `/system`,
  `/options` servent même des blocs strictement identiques entre leurs
  vues.) **Le constat utile est ailleurs** : ce paramètre d'URL atteint
  les octets servis — constante `const VIEW=…` dans le JS de 4 pages,
  attribut `data-view` sur 2 autres — et sa sûreté ne tient qu'à une
  **liste blanche serveur que rien ne testait**. Sondée avec 3 charges
  hostiles (sortie de chaîne JS, sortie d'attribut, fermeture de
  `<script>`) × 8 routes : **aucune fuite**, la valeur inconnue retombe
  partout sur la vue par défaut. Livré : gardien
  `tests/test_vues_parametre_lot367.py` (**33 tests**, dont un anti-vide
  exigeant qu'une vue légitime change bien la page), preuve ROUGE en
  retirant la liste blanche de Portefeuille. Aucune vulnérabilité
  trouvée : le lot ferme une **fenêtre de non-détection sur un chemin
  d'injection**, il ne répare rien. Aucun fichier de production touché →
  pas de preuve MD5 requise, pas de bump (`td-shell-v187`). Suite
  2533 → **2566 / 2 skipped** verte (+33). **La conclusion la plus utile
  est négative** : sans le diff, ce lot aurait posé un gardien inutile
  et annoncé une faille imaginaire.

- **Lot 366 — livré** : GÉNÉRALISATION DU LOT 365 — la trouvaille
  (`thesis_health` annonçant PORTFOLIO_FIT sans le calculer) était-elle
  isolée ou un motif ? Les **110 modules** de `vertex/engines`,
  `positions`, `options`, `scanner`, `strategy` et `ai` passés à la même
  question. **Verdict : ISOLÉE**, aucune autre promesse non tenue. Les
  10 candidats triés : contrats de gouvernance (`SKYLER_ARCHITECTURE`,
  `ADVERSARIAL_COMMITTEE`, `OPTIONS_CORRECTNESS` — vérifiés présents
  dans le SKILL et les rapports), notation mathématique (`S_T`),
  constantes produites par un **module frère** (`ULTRA_CONVEX` et
  `MODEL_ESTIMATE` viennent d'`options/models.py`, via `CALL_CATEGORIES`
  et `GREEKS_MODEL`), et la note du lot 365 elle-même. **Deux erreurs de
  méthode payées comptant et signalées** : (1) un premier filtre « tout
  jeton majuscule ≥4 lettres » a produit **139 faux suspects** noyés
  dans les mots français en capitales — corrigé en exigeant un
  **souligné** (identifiant machine, pas prose) : 139 → 10 ; (2) chercher
  l'identifiant dans le **seul module** qui l'annonce produit des faux
  positifs — la recherche doit couvrir le **paquet**. **Rien touché**
  (« sain » est un verdict, pas un aveu). Ce qui manquait n'était pas un
  correctif mais la **permanence** de la vérification, deux lots l'ayant
  posée avec un script jetable : gardien
  `tests/test_promesses_docstrings_lot366.py` (3 tests, dont « une
  tolérance de gouvernance sans justification dans le SKILL ou les
  rapports est un trou »), dont le message d'échec rappelle la règle du
  lot 365 — corriger la DOC, jamais implémenter à la volée. Preuve ROUGE
  ×2, dont la faute du lot 365 **transplantée dans `anomaly.py`**
  (anomalie `GAP_RUPTURE` annoncée, jamais produite) : attrapée.
  Limite dite : une promesse en un seul mot majuscule échappe au filtre,
  et les docstrings de fonctions ne sont pas balayées. Aucun fichier de
  production touché → pas de preuve MD5 requise, pas de bump
  (`td-shell-v187`). Suite 2530 → **2533 / 2 skipped** verte.

- **Lot 365 — livré** : IDENTIFIANTS CITÉS EN PROSE (piste (a) laissée
  ouverte par le lot 364). Extraction depuis les docstrings/commentaires
  de `vertex/` + `terminal.py` de deux formes calibrées (constantes
  `CAPS_SNAKE`, appels `nom()`), confrontées au code réel du dépôt :
  **23 appels cités, 0 mort** ; 117 constantes citées dont 16
  « introuvables » — examinées **une par une** et toutes légitimes :
  noms de contrats de gouvernance (`SKYLER_ARCHITECTURE`,
  `ADVERSARIAL_COMMITTEE`, `OPTIONS_CORRECTNESS`,
  `SCENARIO_CALIBRATION`, présents dans le SKILL et les rapports),
  notation mathématique (`S_T`), nom de document
  (`VERTEX_WIDGET_LIBRARY.md`, qui **existe** — ma première vérification
  cherchait la chaîne dans le CONTENU des docs, pas dans les noms de
  fichiers ; faux positif corrigé en cours de lot et signalé), et codes
  d'anomalie écrits en majuscules alors que le moteur émet
  `'vol_shift'` (convention, pas divergence). **UNE divergence réelle** :
  `vertex/positions/thesis_health.py` annonçait **7 dimensions** dont
  **PORTFOLIO_FIT**, alors que son code (97 lignes, vérification
  exhaustive) n'a que **5 sections** — `# FUNDAMENTAL`, `# CATALYST`,
  `# TECHNICAL`, `# SENTIMENT`, `# RISK / DATA_QUALITY` : **aucune ligne
  ne regarde l'adéquation au portefeuille**. Piège aggravant :
  `portfolio_fit` existe vraiment ailleurs (`scanner/stages.py`,
  `strategy/executive_engine.py`), donc on pouvait croire que la santé
  de thèse — qui alimente l'état de thèse affiché sur Portefeuille — en
  tenait compte. Correctif : la docstring dit désormais ce que le module
  évalue ET ce qu'il n'évalue pas, avec le renvoi vers les modules qui
  produisent réellement `portfolio_fit`. **Aucune dimension ajoutée** :
  implémenter à la volée une adéquation au portefeuille aurait mis un
  chiffre inventé dans un verdict de santé — c'est une décision produit,
  en attente de GO. Gardien `tests/test_thesis_health_dimensions_lot365.py`
  (3 tests, dont « PORTFOLIO_FIT reste écrit comme non évalué » qui
  réclamera sa mise à jour le jour où il sera implémenté) ; preuve ROUGE
  ×2 dont **la faute rejouée**. Un fichier de production ayant changé
  (docstring seule), preuve exigée : serveur DEMO + **MD5 des 8 pages,
  0 écart / 8** → pas de bump (`td-shell-v187`). Suite 2527 →
  **2530 / 2 skipped** verte.

- **Lot 364 — livré** : AUTO-RÉFÉRENCES — « ce que le projet dit de
  lui-même est-il vrai ? », suite du lot 71 (qui avait trouvé une
  docstring citant un gardien inexistant et posé le contrat pour
  `vertex/`). Deux angles morts restaient : `terminal.py` et les
  documents. Mesure : **0** chemin de module `vertex/**.py` mort,
  **0** route sur les **29** routes `/api/…` citées en commentaire
  (toutes dans l'`url_map`), mais **7 références de tests inexistants,
  toutes dans `docs/`**. Enquête git : trois gardiens créés aux
  lots 183/184/185 ont été **supprimés par la purge É1 du lot 323**
  (`80a1729`, PR #355) — comme le plan le prévoyait, sa catégorie B
  s'appelant littéralement « retrait avec leurs tests » — mais **rien
  ne l'écrivait**. `ANNEXE-E1-RETRAITS.md`, qui est le document de
  PREUVE de la purge, laissait donc sa piste de vérification rompue :
  un lecteur cherchant ces gardiens ne les trouvait pas et ignorait
  pourquoi. **C'est mon propre travail (lot 323) qui a créé l'écart.**
  La 7ᵉ référence est la citation historique du défaut du lot 71
  lui-même, légitime. Livré : **statut d'exécution** ajouté à l'annexe
  (commit, PR, ampleur, les 3 gardiens marqués RETIRÉ avec leur lot de
  création) — les rapports `SKYLER-LOT-183/184/185.md` ne sont PAS
  touchés, ce sont des archives et les réécrire falsifierait
  l'histoire ; et gardien `tests/test_references_vivantes_lot364.py`
  (7 tests) : contrat du lot 71 **étendu à `terminal.py`**, même
  contrat sur les chemins de modules, et pour les **documents vivants**
  — citer un gardien disparu est permis **à condition de dire qu'il a
  été retiré** sur la ligne qui le nomme. Preuve ROUGE ×2, dont la
  faute historique du lot 71 rejouée dans le fichier que son gardien ne
  regardait pas ; fichiers restaurés MD5 identique. Aucun code n'était
  faux : le défaut était une piste de preuve rompue. Aucun octet servi
  → pas de bump (`td-shell-v187`). Suite 2520 → **2527 / 2 skipped**
  verte.

- **Lot 363 — livré** : RÈGLE N°4 (« données RÉELLES uniquement ; le mot
  démo ne s'affiche que si le serveur le confirme ») — **SAINE, et
  prouvé plutôt que supposé**. (1) Les données DEMO sont bien
  synthétiques et le serveur le dit (`_demo_universe`,
  `scan_state['source']='demo'` ; mesuré : taux 3 mois à **35,6 %**,
  manifestement fabriqué). (2) Les **8 pages préviennent** en navigateur
  réel après hydratation : « DÉMO — Données synthétiques clairement
  identifiées, jamais présentées comme réelles » sur `/`, `/markets`,
  `/opportunities`, `/portfolio`, `/journal` ; « board démo » sur
  `/options` (correctif du lot 296, toujours en place) ; « Mode global
  demo » sur `/system`. `/analysis` n'a que le chip de nav — c'est une
  page de **recherche** sans donnée de marché, cohérent. (3) Recensement
  des couples `source:`/`mode:` servis, seul endroit où une chaîne peut
  mentir sur la réalité d'un chiffre : **31 dérivés du serveur,
  59 constants, 0 affirmant réel/live** — les constants valent `delayed`
  / `index` ou nomment un moteur. Mais la règle s'était **déjà perdue
  deux fois** (lot 296 « board réel » en dur, lot 297 chip « Live » en
  dur) et rien n'empêchait une troisième : gardien neuf
  `tests/test_honnetete_provenance_lot363.py` (4 tests, dont un
  anti-vide). **Preuve ROUGE : les deux fautes historiques rejouées sont
  attrapées**, fichiers restaurés MD5 identique. Observation laissée
  telle quelle : « 4 maturités réelles » / « points réels du scan » sur
  `/markets` parlent de méthode, pas de provenance — ambigu à côté d'un
  badge démo, mais pas faux ; reformuler serait un octet servi modifié
  pour du style, décision humaine. Aucun octet servi → pas de bump
  (`td-shell-v187`). Suite 2516 → **2520 / 2 skipped** verte.
  **Bilan des 5 règles passées à la question : 4 trouvailles** (n°2, n°3,
  n°5 = trous ; n°6 = promesse plus étroite ; n°4 = saine).

- **Lot 362 — livré** : RÈGLE N°6 (celle qui protège les données réelles
  de l'utilisateur) passée à la même question. **Sain** : la chaîne de
  sauvegarde tient (snapshot quotidien avant écrasement, rotation à 7,
  restore au nom strictement validé — traversée refusée, `ts` neuf pour
  que tous les appareils re-tirent), et le client se protège bien
  (`vx_kit.py` ne pousse qu'après hydratation réussie, s'abstient si
  `bootSync` échoue, re-remplit toute clé absente). **Trois faits
  mesurés** que la règle ne disait pas, sonde isolée dans un dossier
  temporaire (le vrai `desk_data.json` jamais touché) : (1) un push
  `data: {}` est **accepté en 200** et vide le blob — la validation
  porte sur le TYPE, `{}` est un dict, donc l'écrasement n'a pas besoin
  d'être « à la main » ; (2) le last-writer-wins est **total**, un push
  partiel efface les clés absentes ; (3) **aucun snapshot
  supplémentaire** n'est pris à ce moment-là → un restore rend l'état
  d'**avant la 1ʳᵉ sync du jour** et **perd le travail de la journée**,
  avec au plus **7 jours** de profondeur. Scénario résiduel réaliste :
  navigateur dont l'écriture localStorage échoue en silence (navigation
  privée, quota). Livré : gardien de **caractérisation**
  `tests/test_desk_perte_lot362.py` (5 tests, messages d'échec = « mettre
  à jour ce gardien ») + règle n°6 corrigée dans `CLAUDE.md`. Preuve que
  le gardien ALERTE : durcissement simulé (refus du push vide) → ROUGE,
  fichier restauré MD5 identique, 5 verts après restauration.
  **Rien durci** — refuser un push vide changerait le contrat de sync
  assumé ; 3 options en attente de GO humain (A : snapshot
  supplémentaire avant perte, **recommandée**, purement additive ;
  B : refus 409 ; C : fusion par clé). Aucun octet servi modifié → pas
  de bump (`td-shell-v187`). Suite 2511 → **2516 / 2 skipped** verte.

- **Lot 361 — livré** : RÈGLE N°3 passée à la question qui a donné les
  lots 358 et 359. La règle disait « tout changement de **shell visible
  utilisateur** → bump `td-shell-vN` ». Le service worker, lui, met en
  cache **tout `/static`** (54 fichiers servis : 34 JS, 17 CSS,
  2 polices) **plus** les navigations et le manifeste ; il est
  *network-first* (`Promise.race([fetch, timeout 4500])`), le cache ne
  sert qu'en repli ; `activate` supprime tous les caches dont la clé
  diffère. Deux vérités absentes de la règle : le périmètre est **plus
  large que « le shell »**, et le bump ne sert pas à « faire voir » la
  nouvelle interface (le network-first s'en charge) mais à **purger la
  copie de repli hors-ligne**. Fenêtre d'exposition : visiteur déjà
  venu, hors-ligne ou réseau > 4,5 s, servi depuis un cache assemblé au
  fil de visites différentes. Mesure de l'historique : **27 commits sur
  144** touchant `vertex/static` sans bump — **conformes à la règle
  écrite**, donc le défaut est dans la règle, pas dans la discipline.
  Livré : gardien `tests/test_sw_cache_scope_lot361.py` (5 tests —
  sémantique du SW figée + contrat empreinte SHA-256 des assets ↔
  version enregistrée, daté d'aujourd'hui, ne juge pas l'historique) et
  règle n°3 corrigée dans `CLAUDE.md`. Preuve ROUGE sur les 4
  propriétés, fichiers restaurés MD5 identique. Aucun bug utilisateur
  observé (en ligne le frais gagne toujours) : le lot rend la règle
  exacte et applicable, au prix d'une **friction assumée** (tout
  changement d'asset exigera un bump + 2 constantes). Solution de fond
  non engagée : empreinte dans les URL d'assets — demande un GO humain.
  Aucun octet servi modifié → pas de bump (`td-shell-v187`). Suite
  2506 → **2511 / 2 skipped** verte.

- **Lot 360 — livré** : CHECKPOINT de la tranche 350-359. Serveur DEMO
  (`/scan` 20 lignes) : **les 8 MD5 sont identiques aux références** —
  aucun octet servi n'a bougé depuis le lot 350. Navigateur réel
  (Chromium, 1440×900, après hydratation) : **0 erreur console** sur les
  8 pages. Toutes les tailles smoke sauf `/analysis` (923, exact)
  s'écartaient : deux vérifications avant de conclure. (a) La mesure hors
  navigateur n'est pas comparable (les pages s'hydratent côté client :
  `/` 510 en HTML brut). (b) **À MD5 identique, le smoke bouge** — deux
  passes à 90 s d'écart : `/` 3367 → 3385 (**+18 caractères, MD5
  stable**), les 5 autres pages à delta 0. Les libellés de fraîcheur
  changent de longueur. Conclusion d'instrument : **le MD5 est la seule
  preuve stricte inter-sessions ; le smoke mesure le contenu hydraté**
  (horloge, jeu DEMO régénéré par session, `desk_data.json` local) et
  est donc requalifié en **plage indicative**, jamais opposable au MD5.
  Chaque écart tracé dans le rapport : `/markets` +20 et
  `/opportunities` −93 = jeu DEMO de la session (stables en session) ;
  `/system` +2/+3 = plage du lot 340 structurellement trop étroite pour
  une page qui imprime des âges ; `/journal` +1010 = sondes locales du
  lot 305 (documenté depuis le lot 330). Bilan de tranche : 8 lots
  « sain, rien touché », 2 trouvailles (358 : 2ᵉ famille de sorties de
  news ; 359 : `/analysis` hors gardiens JS) — les deux nées de la même
  question, « la règle écrite décrit-elle vraiment le code servi ? ».
  Suite 2501 → **2506 / 2 skipped**, SW `td-shell-v187` inchangé sur
  toute la tranche, 10 PR fusionnées (#382 → #391), `main` intacte.

- **Lot 359 — livré** : GARDIENS JS — même question qu'au lot 358 appliquée
  à la règle critique n°2 (« tout JS généré doit être syntaxiquement
  valide ») : ses gardiens (lots 182 et 186) travaillent sur une **liste
  de routes figée**. Inventaire complet de l'`url_map` (chaque règle GET
  appelée sans suivre les redirections) : les 40 routes hors liste sont
  des **301** vers des pages canoniques, mais **`/analysis`** (index,
  `analysis_page.render_index` — fonction distincte de `render(sym)` qui
  sert `/analysis/<sym>`) est une **page HTML 200 servie, 22 248 o,
  2 blocs `<script>` inline**, absente des DEUX gardiens. Sa syntaxe JS
  et ses liens d'assets n'ont jamais été vérifiés — alors qu'elle est
  l'une des 8 pages de la référence smoke. Ajoutée aux deux listes.
  Preuve ROUGE en rejouant le bug historique de la règle n°2 (apostrophe
  française non échappée dans une chaîne JS simple) : **ancienne liste
  0 erreur — totalement aveugle ; nouvelle liste attrape**, fichier
  restauré MD5 identique. Aucune faute n'existait : le lot ferme une
  fenêtre de non-détection, il ne répare rien. Aucun octet servi modifié
  → pas de bump (`td-shell-v187`). Suite **2506 / 2 skipped** verte.

- **Lot 358 — livré** : SORTIES DE NEWS — la règle critique n°5 décrivait
  UNE famille de sorties ; il y en a **deux**. `/api/ai/enrichment`
  (cerveau Claude+web) sert le titre d'actualité **non neutralisé**
  (mesuré : `<script>alert(1)</script>Titre`) et n'était couvert par
  aucun gardien. Ce n'est pas un trou — son unique rendu
  (`system_page.py::loadBrain`) échappe via `esc()`, les citations sont
  filtrées http(s), la forme est reconstruite et bornée — mais rien ne
  figeait ces trois propriétés, et y ajouter `sanitize_news`
  **double-échapperait** les titres légitimes. Livré : gardien neuf
  `tests/test_ai_news_exit_lot358.py` (5 tests, preuve ROUGE sur les
  3 défenses, fichiers restaurés MD5 identique) + règle n°5 de
  `CLAUDE.md` corrigée (deux familles, deux contrats, leurs gardiens).
  Première rédaction du gardien `esc()` **ne mordait pas** (fenêtre de
  30 caractères) → refaite en analyse des appels englobants, re-prouvée.
  Aucun octet servi modifié → pas de bump (`td-shell-v187`).
  Suite **2501 → 2506 / 2 skipped** verte.

- **Lot 357 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour e19305a, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 350). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 356 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 63b9559, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 350). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 355 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 91b0d6c, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 350). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 354 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 92eec8f, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 350). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 353 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 6aadd19, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 350). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 352 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 51ff1ec, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 350). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 351 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 843b21a, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (le lot 350 vient de tout mesurer, aucun octet n'a bougé).
  Docs seulement, pas de bump. Quatre dossiers toujours en attente de
  décision humaine.

- **Lot 350 — livré** : **ÉCHÉANCE PÉRIODIQUE (10e mesure) + BILAN
  340-349**. Smoke complet : **8×200, 0 erreur console/pageerror,
  client-log 0** — et pour la première fois **les 8 tailles de texte
  tombent TOUTES dans leurs références**, y compris les deux qui avaient
  demandé une explication au lot 340 : `/journal` 3 690 (desk local de
  la session) et **`/system` 4 123**, qui confirme par une seconde
  observation la fourchette rebasée (4 122-4 124). Le rebasage du lot
  340 n'était pas un ajustement de confort : il décrivait la réalité.
  **Les 8 MD5 conformes** ; `/sw.js` sert `td-shell-v187` ; suite
  **2501 / 2**.
  **BILAN de la tranche — « la croisière tenue »** : dix lots, **zéro
  changement produit, zéro défaut détecté**, et c'est le résultat
  correct, pas un aveu d'inaction — les filons « code mort » et « textes
  périmés » ont été épuisés dans la tranche précédente, et fabriquer du
  travail pour remplir un rapport aurait été la seule vraie faute
  possible. 340 = échéance 9e mesure + bilan 330-339 avec le **rebasage
  de la fourchette `/system`** (le lot 328 avait retiré deux caractères,
  la référence ne l'avait jamais enregistré) ; 341-349 = neuf cycles de
  veille, règle appliquée sans exception : **ne pas re-mesurer ce qui
  n'a pas bougé**. Chiffres : suite **2501 constante sur les 10 lots**,
  SW **v187 constant**, terminal.py **inchangé à 7 153 l.**, **10 PR
  fusionnées (#372 → #381)**. Prochaine échéance ~lot 360. Pas de bump.

- **Lot 349 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 30f62ec, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (la 10e mesure est pour le lot 350). Docs seulement, pas de
  bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 348 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 09246b2, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 340). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 347 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 72c13c7, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 340). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 346 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 26e1910, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 340). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 345 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 59dcdf6, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 340). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 344 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 985db84, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 340). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 343 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 593208a, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 340). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 342 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 5498b86, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 340). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 341 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 0b37527, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (le lot 340 vient de tout mesurer, aucun octet n'a bougé).
  Docs seulement, pas de bump. Quatre dossiers toujours en attente de
  décision humaine.

- **Lot 340 — livré** : **ÉCHÉANCE PÉRIODIQUE (9e mesure) + BILAN
  330-339**. Smoke complet : **8×200, 0 erreur console/pageerror,
  client-log 0** ; 6 tailles sur 8 identiques aux références. Les deux
  écarts sont expliqués, pas arrondis : `/journal` 3 690 (le desk local
  porte les trades de la sonde du lot 305 ; MD5 du HTML servi inchangé
  — tranché au lot 330) et **`/system` 4 123 au lieu de 4 124-4 126 :
  conséquence attendue du lot 328**, qui a retiré les deux caractères
  `__` du libellé `__DESK_KEYS`. La référence n'avait pas été rebasée →
  **nouvelle fourchette 4 122-4 124**. Ce n'est pas une dérive, c'est le
  lot 328 qui devient enfin visible dans la mesure de taille.
  **Les 8 MD5 conformes** ; `/sw.js` sert `td-shell-v187` ; suite
  **2501 / 2**.
  **BILAN de la tranche — « le retour au régime de croisière »** : une
  échéance (330) puis neuf cycles de veille (331-339) où le travail
  consistait surtout à **ne pas en inventer**. Une règle les a
  structurés : **ne pas re-mesurer ce qui n'a pas bougé** — le lot 330
  avait tout mesuré, aucun octet n'a changé ensuite ; refaire le smoke à
  chaque réveil aurait produit neuf pages de chiffres identiques, du
  bruit déguisé en preuve. Les rapports le disent au lieu de faire
  semblant d'avoir vérifié. Chiffres : suite **2501 constante sur les
  10 lots**, SW **v187 constant**, terminal.py **inchangé à 7 153 l.**,
  **10 PR fusionnées (#362 → #371)**, 0 changement produit, 0 défaut
  détecté. Prochaine échéance ~lot 350. Pas de bump.

- **Lot 339 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour ea14e1d, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (la 9e mesure est pour le lot 340). Docs seulement, pas de
  bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 338 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 780ec58, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 330). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 337 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 07171f7, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 330). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 336 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour ec8444d, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 330). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 335 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 9c61b24, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 330). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 334 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 96e4fc5, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 330). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 333 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour e9108ed, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 330). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 332 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 9f466cd, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle ; pas de
  re-mesure (aucun octet n'a bougé depuis le lot 330). Docs seulement,
  pas de bump. Quatre dossiers toujours en attente de décision humaine.

- **Lot 331 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 5e6809e, arbre propre, suite **2501 / 2**
  verte) ; aucun signal, aucune piste calibrée nouvelle. Pas de
  re-mesure : le lot 330 vient de mesurer l'état complet et aucun octet
  n'a bougé depuis — re-mesurer serait du bruit, pas une preuve. Docs
  seulement, pas de bump. Quatre dossiers toujours en attente de
  décision humaine (É2, É3, les 24 fonctions, les 5 modules reliques).

- **Lot 330 — livré** : **ÉCHÉANCE PÉRIODIQUE (8e mesure) + BILAN
  320-329**. Smoke complet : **8×200, 0 erreur console/pageerror,
  client-log 0** ; 7 tailles sur 8 identiques aux références.
  **`/journal` à 3 690 au lieu de 2 676 — expliqué, pas masqué** : le
  `desk_data.json` local porte les 3 trades laissés par la sonde du lot
  305, et le texte rendu le dit mot pour mot (« 3 trade(s) clôturé(s) :
  33 % de réussite, P&L cumulé -700 »). Preuve que ce n'est pas une
  régression : **le MD5 du HTML servi pour `/journal` est INCHANGÉ**
  (243699ace2d5) — le serveur envoie les mêmes octets, tout l'écart
  naît de l'hydratation locale. **Les 8 MD5 conformes** (dont `/system`
  73e917c0f2d0) ; `/sw.js` sert `td-shell-v187` ; suite **2501 / 2**.
  **BILAN de la tranche — « celle qui a enfin coupé »** : après dix lots
  de croisière, le blocage de permissions est tombé et la tranche est
  passée au travail de fond — purge É1 (**-33 % de terminal.py**, 82
  défs), hygiène des imports (terminal.py puis les 183 modules de
  vertex/, 2 gardiens AST posés), 3 pistes instruites dont une laissée à
  l'humain, `CLAUDE.md` remis au vrai avec correction de ma propre
  erreur du 323, libellé périmé corrigé avec bump SW assumé, puis
  vérification que c'était un cas isolé. Chiffres : suite **2516 →
  2501** (les 17 tests retirés étaient écrits POUR la purge), SW **v186
  → v187**, **10 PR fusionnées (#352 → #361)**, terminal.py **-3 590
  lignes**. Leçon de fond : **trois fois le réflexe évident aurait été
  une erreur** (l'import `BROKER` qui EST un diagnostic, les 24 façades
  IBKR qui sont le chemin de lecture du compte réel, ma propre règle qui
  citait un fichier mort) — un compteur ne distingue pas le mort de
  l'endormi. Prochaine échéance ~lot 340. Pas de bump.

- **Lot 329 — livré** : LE LOT 328 ÉTAIT-IL UN CAS ISOLÉ ? **Oui — SAIN,
  rien touché.** Après le retrait de 82 définitions, d'autres libellés
  pouvaient citer des noms qui n'existent plus. La mesure est faite
  **dans le navigateur, sur le texte RENDU** (`document.body.innerText`)
  et non sur le HTML brut — une bonne part des libellés est écrite par
  le JS après hydratation. **16 vues** balayées : les 8 racines, la
  fiche `/analysis/NVDA`, les 3 sous-vues Système (données, réglages,
  archive), Marchés → ampleur, Opportunités → anomalies, Portefeuille →
  risque, Journal → track-record. Extraction des jetons ressemblant à un
  identifiant technique (snake_case, noms de fichiers), puis
  confrontation au code réel : **30 identifiants affichés, 0
  introuvable**. `__DESK_KEYS` était bien un cas isolé, corrigé au lot
  328. MD5 des 8 pages identiques aux références (dont `/system`
  73e917c0f2d0), `/sw.js` sert `td-shell-v187`, suite **2501 / 2
  skipped**. Pas de bump.

- **Lot 328 — livré** : HONNÊTETÉ D'AFFICHAGE. La page Système annonçait
  à l'utilisateur « Clés synchronisées — 17 (contrat **`__DESK_KEYS`** —
  aucune clé renommée) ». Ce symbole a **disparu avec la purge É1** : il
  nommait la liste qui vivait dans le JS des pages mortes. Le contrat
  existe toujours, il s'appelle `DESK_KEYS` (vx_kit + vx-entities).
  L'affirmation n'était pas fausse sur le fond, mais elle nommait un
  symbole **introuvable dans le code** — un trader qui irait vérifier ne
  trouverait rien. Invariant n°4. Repéré au lot 327, mis en réserve
  parce qu'il change un octet servi ; traité ici avec le protocole
  complet. Correctif = **une chaîne**. Preuve chirurgicale : **7 MD5
  identiques, seul `/system` change** (85d1cb065d2e → **73e917c0f2d0**,
  nouvelle référence) ; le HTML servi contient `contrat DESK_KEYS` et
  **0 occurrence de `__DESK_KEYS`** ; smoke 8×200, 0 erreur console,
  client-log 0. **Bump SW `td-shell-v186` → `td-shell-v187`** + les
  5 gardiens SW mis à jour. Suite **2501 / 2 skipped**.

- **Lot 327 — livré** : **`CLAUDE.md` REDEVIENT VRAI**. Les lots 323-325
  ont retiré 33 % de terminal.py ; la documentation de pilotage — le
  fichier que chaque session lit en premier — décrivait encore l'état
  d'avant. Trois affirmations vérifiées, trois fausses.
  (1) « Monolithe ~10 500 lignes » → **7 153** (historique 10 743
  conservé pour que le chiffre reste interprétable).
  (2) « Pages extraites : nav, options_lab, journal, vault, signals,
  sync_center, vx_kit, design_system » — vérification consommateur par
  consommateur : `nav`, `vx_kit`, `sync_center`, `design_system` et
  `home_art` sont servis ; **`options_lab`, `journal`, `vault`,
  `signals` et `strategy_os` ont 0 consommateur en production**. Ce sont
  des reliques — **non supprimées**, elles rejoignent le dossier ouvert
  du lot 326.
  (3) **Correction de ma propre erreur du lot 323** : j'y avais annoncé
  `vertex/ui/journal.py` comme l'une des « 3 listes servies » de clés de
  sync desk. Il **n'est pas servi** — je l'avais repris du gardien sans
  vérifier. Les listes réellement servies sont `vx_kit.py` (source de
  vérité), `vx-entities.js`, et **le repli `deskKeys()` de
  `system_page.py`** — cette troisième n'était citée nulle part, c'est
  celle qu'on aurait pu oublier. Aucune donnée utilisateur en jeu :
  `vxJournal` est géré en production par `vx-entities.js`.
  Mis en réserve pour un lot dédié : la page Système affiche « contrat
  `__DESK_KEYS` », symbole disparu avec la purge É1 — le corriger change
  un octet servi, donc bump SW + 5 gardiens assumés.
  Suite **2501 / 2 skipped**, pas de bump (docs seulement).

- **Lot 326 — livré** : TROIS PISTES INSTRUITES, **aucun code touché**.
  (a) Fichiers statiques : 51 CSS/JS, chacun cherché par nom dans tout
  le dépôt → **0 non référencé**, SAIN. (b) Routes : **186 routes**
  d'`app.url_map`, préfixe statique cherché dans le JS servi et les
  modules qui construisent l'UI → **0 orpheline**, SAIN.
  (c) Fonctions top-level jamais citées ailleurs (décorateurs exclus) :
  **24 fonctions / 258 lignes** — data_sources 9, research 5, scanner 1,
  anomalies 2, observability 3, strategy 4. **DOSSIER OUVERT, rien
  retiré** : le gros est constitué des façades d'intégration IBKR
  (`fetch_positions`, `fetch_snapshot`, `fetch_daily_bars`,
  `fetch_expirations`, `qualify_stock`…), c'est-à-dire le chemin de
  lecture du compte réel via TWS. « Jamais citée » ne veut pas dire
  « morte » : ça peut vouloir dire « porte d'une intégration pas encore
  recâblée », et supprimer serait détruire du travail d'intégration, pas
  nettoyer. C'est la leçon du lot 325 (`BROKER`) à plus grande échelle :
  **un compteur ne distingue pas le mort de l'endormi.** Trancher demande
  une décision produit — elle appartient à l'utilisateur, comme É2 et É3.
  Suite **2501 / 2 skipped**, pas de bump.

- **Lot 325 — livré** : L'AUDIT D'IMPORTS ÉTENDU À TOUT `vertex/`
  (183 modules). Premier chiffre trompeur : 192 « orphelins », dont
  **180 sont `from __future__ import annotations`** — une directive du
  compilateur, jamais référencée par un nom. Faux positif écarté ; il
  restait **12 suspects**, chacun vérifié individuellement (0 ré-import
  ailleurs, 1 seule occurrence dans son fichier).
  **1 des 12 n'était pas mort** : `from vertex.services.live_stream
  import BROKER` dans `services/startup.py` — **l'import EST le
  diagnostic** : s'il échoue, l'étape de démarrage bascule en DEGRADED.
  Le retirer aurait produit un « READY » inconditionnel, donc un
  mensonge sur l'état du flux SSE. Conservé, marqué `# noqa: F401` et
  commenté pour qu'aucun nettoyage futur ne le reprenne. C'est le seul
  intérêt réel du lot : la différence entre un import mort et un import
  qui travaille sans être lu ne se voit pas dans un compteur.
  **11 retraits** effectifs (SEV_INFO, time, Iterable, os,
  CATEGORY_BALANCED, CATEGORY_BEARISH_TACTICAL, vol, np,
  LifecycleError, any_blocking, STATUSES) — tous ces symboles restent
  définis et utilisés ailleurs. **MD5 des 8 pages identiques aux lots
  323/324** → zéro octet servi modifié, **pas de bump SW** ; smoke
  8×200, 0 erreur console, client-log 0. **Gardien étendu** :
  `test_no_orphan_imports_in_vertex_package`, exclusions minimales et
  documentées (`import *`, `# noqa`, `annotations`, `__init__.py`).
  Suite **2501 / 2 skipped**.

- **Lot 324 — livré** : HYGIÈNE POST-PURGE. Une purge de -33 % laisse
  des résidus : audit AST de `terminal.py` → **11 imports orphelins**
  (10 créés par É1 — leurs consommateurs étaient dans les 82 défs
  retirées — et 1 antérieur, `strategy.config`). Retirés après trois
  vérifications faites AVANT de toucher : aucun effet de bord d'import
  perdu (les 5 modules `vertex/ui/*` concernés sont des bibliothèques
  de rendu pures, sans route ni blueprint), **0 consommateur en
  production** (les tests les importent directement), et les 4 modules
  moteur/service restent importés ailleurs dans `vertex/`. Les
  ré-exports déclarés (`import *`, `# noqa: F401`) sont volontairement
  épargnés — y toucher serait un pari. terminal.py 7 164 → **7 153
  lignes**. **MD5 des 8 pages identiques au lot 323** → zéro octet
  servi modifié, **pas de bump SW** ; smoke 8×200, 0 erreur console,
  client-log 0. **Gardien neuf** : `test_terminal_imports_lot324.py`
  (AST — le monolithe ne réaccumulera plus d'imports morts en
  silence). Suite **2500 / 2 skipped**.

- **Lot 323 — livré** : **PURGE É1 FAITE** — le blocage de permissions
  qui durait depuis le lot 285 est levé (il visait la commande
  composée, pas le retrait). Les **82 définitions mortes** sont
  retirées de `terminal.py` : **10 743 → 7 164 lignes (-3 579,
  -33,3 %)**, **-415 573 octets**, diff **100 % soustractif**.
  Preuves : outil de chiffrage rejoué → **borne basse 0 déf / 0 ligne**
  (É1 close) ; **MD5 des 8 pages servies IDENTIQUES avant/après** —
  zéro octet servi modifié, donc **pas de bump SW** ; smoke navigateur
  8×200, 0 erreur console, client-log 0 ; `compileall` 0 ; import à
  chaud 1 805 → 1 981 ms = **aucun gain mesurable, dit honnêtement**
  (l'import est dominé par pandas/yfinance ; le gain est de
  lisibilité). Effet de bord traité : les 3 copies de la liste de clés
  de sync desk que `terminal.py` portait vivaient dans le JS des pages
  mortes → parties avec ; la sync réelle est intacte (vx_kit /
  journal / vx-entities), règle critique n°1 de CLAUDE.md passée de
  « 4 listes » à « 3 listes servies », **5 gardiens re-ciblés et
  durcis** (dont un qui exige désormais que terminal.py ne ressuscite
  aucune liste). Nouvelle référence de suite : **2499 / 2 skipped**
  (-17 = tests de caractérisation retirés par la moitié 1/2, écrits
  pour ce moment). Reste É2 (25 défs, 1 866 l., boucles d'injection
  par chaîne) et É3 (dépendances croisées) — décisions humaines.

- **Lot 322 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 5ced46e, arbre propre, suite 2516/2
  verte) ; aucun signal, aucune piste nouvelle ; rapport minimal.
  Docs seulement, pas de bump. É1 : GO acquis, toujours en attente.

- **Lot 321 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 2e5c14b, arbre propre, suite 2516/2
  verte) ; aucun signal, aucune piste nouvelle ; rapport minimal.
  Docs seulement, pas de bump. É1 : GO acquis, toujours en attente.

- **Lot 320 — livré** : ÉCHÉANCE PÉRIODIQUE (7e mesure) — SMOKE
  PARFAIT (2e consécutif) : 8×200, 0 erreur, client-log 0, **les 8
  tailles STRICTEMENT identiques aux références 300/310** — la base
  sert des octets stables sur 3 échéances ; suite 2516/2. MINI-BILAN
  310-319 : « régime de croisière » — 1 smoke parfait (310) + 9
  cycles de veille active honnête (311-319), suite 2516/2 constante,
  SW v186 constant, 10 PR fusionnées (#342→#351), 0 changement,
  0 défaut. Prochaine échéance ~lot 330. Docs seulement, pas de
  bump. É1 : GO acquis, toujours en attente de déblocage
  permissions.

- **Lot 319 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour d9b23d5, arbre propre, suite 2516/2
  verte) ; aucun signal, aucune piste nouvelle ; rapport minimal.
  Docs seulement, pas de bump. É1 : GO acquis, toujours en attente.
  Prochain lot : ÉCHÉANCE PÉRIODIQUE (7e mesure + bilan 310-319).

- **Lot 318 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 48a44f5, arbre propre, suite 2516/2
  verte) ; aucun signal, aucune piste nouvelle ; rapport minimal.
  Docs seulement, pas de bump. É1 : GO acquis, toujours en attente.

- **Lot 317 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour b692aac, arbre propre, suite 2516/2
  verte) ; aucun signal, aucune piste nouvelle ; rapport minimal.
  Docs seulement, pas de bump. É1 : GO acquis, toujours en attente.

- **Lot 316 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 3eeca4d, arbre propre, suite 2516/2
  verte) ; aucun signal, aucune piste nouvelle ; rapport minimal.
  Docs seulement, pas de bump. É1 : GO acquis, toujours en attente.

- **Lot 315 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 05d06a4, arbre propre, suite 2516/2
  verte) ; aucun signal, aucune piste nouvelle ; rapport minimal.
  Docs seulement, pas de bump. É1 : GO acquis, toujours en attente.

- **Lot 314 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour b7debb0, arbre propre, suite 2516/2
  verte) ; aucun signal, aucune piste nouvelle ; rapport minimal.
  Docs seulement, pas de bump. É1 : GO acquis, toujours en attente.

- **Lot 313 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 7441a7b, arbre propre, suite 2516/2
  verte) ; aucun signal, aucune piste nouvelle ; rapport minimal.
  Docs seulement, pas de bump. É1 : GO acquis, toujours en attente.

- **Lot 312 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour b366fae, arbre propre, suite 2516/2
  verte) ; aucun signal, aucune piste nouvelle ; rapport minimal.
  Docs seulement, pas de bump. É1 : GO acquis, toujours en attente.

- **Lot 311 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour 286a506, arbre propre, suite 2516/2
  verte) ; aucun signal, aucune piste nouvelle ; rapport minimal.
  Docs seulement, pas de bump. É1 : GO acquis, toujours en attente.

- **Lot 310 — livré** : ÉCHÉANCE PÉRIODIQUE (6e mesure) — SMOKE
  PARFAIT : 8×200, 0 erreur console/pageerror, client-log 0, **les 8
  tailles STRICTEMENT identiques aux références du lot 300** (outil
  commité probe_smoke.py, scan terminé avant mesure — piège du froid
  évité, vertex_ready=20) ; suite 2516/2. MINI-BILAN 300-309 :
  « prouver que tout est sain, puis assumer la veille » — robustesse
  outillée (301), fix clavier topbar SW v186 (302), première
  baseline « contenu utile » (304), round-trip desk + CAMPAGNE
  D'AUDITS CLOSE (305), cartographie moteur→UI complète (306),
  veille honnête (307-309). 10 PR fusionnées (#332→#341), 1 défaut
  réel corrigé, 3 outils de validation commités, 0 changement
  gratuit. Prochaine échéance ~lot 320. Docs seulement, pas de bump.
  É1 : GO acquis, toujours en attente de déblocage permissions.

- **Lot 309 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour c38c903, arbre propre, suite 2516/2
  verte) ; aucun signal, aucune piste nouvelle ; rapport minimal.
  Docs seulement, pas de bump. É1 : GO acquis, toujours en attente.
  Prochain lot : ÉCHÉANCE PÉRIODIQUE (smoke + mini-bilan 300-309).

- **Lot 308 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour ca944e1, arbre propre, suite 2516/2
  verte) ; aucun signal utilisateur, aucune piste calibrée nouvelle ;
  rapport minimal. Docs seulement, pas de bump. É1 : GO acquis,
  toujours en attente de déblocage permissions. Prochain jalon :
  échéance périodique au lot 310.

- **Lot 307 — livré** : VEILLE ACTIVE — état vérifié : 0 doublon
  trigger, integration à jour (51e3874), arbre propre, suite 2516/2
  verte sur base fraîche, PR ouvertes = uniquement les 3 brouillons
  intentionnels historiques (#15/#13/#5). Posture assumée : audits
  292-305 clos + cartographie moteur→UI complète → veille honnête
  plutôt que travail fabriqué (œil sur déblocage É1, signaux
  d'usage, échéance périodique ~lot 310). Docs seulement, pas de
  bump. É1 : GO acquis, toujours en attente de déblocage
  permissions.

- **Lot 306 — livré** : CARTOGRAPHIE moteur → UI (calibrage strict :
  payloads réels des API en DEMO vs code des pages). 6 pistes
  « donnée servie mais non affichée » vérifiées : adjustments du
  régime AFFICHÉS (Marchés chips + Aujourd'hui), notes[] toujours
  vides en régime connu / déjà éditorialisées en inconnu,
  top_stocks + bloc vertex (p_win, edge) AFFICHÉS (Opportunités),
  vx_* AFFICHÉS, validation (DSR/PBO/dégradation) AFFICHÉE
  (Intelligence), portfolio_score consommé UNIQUEMENT par les pages
  legacy ORPHELINES de terminal.py — un argument de PLUS pour la
  purge É1 (données calculées pour du code mort). **Couverture
  moteur → UI complète — aucune lacune ne justifie un changement.**
  Suite **2516 passed / 2 skipped**. Docs seulement, pas de bump.
  É1 : GO acquis, toujours en attente de déblocage permissions.

- **Lot 305 — livré** : ROUND-TRIP DESK prouvé de bout en bout
  (dernier angle d'audit) — par le chemin RÉEL du store :
  VXEntities.toggleFavorite → localStorage → push débouncé → serveur
  /api/desk data.myFavs=["AAPL"] (6 clés intactes) →
  localStorage.clear + reload → **le pull au boot RESTAURE le
  favori** → nettoyage → serveur []. 0 erreur ; 2 imprécisions de MA
  sonde corrigées en route. Verdict SAIN — le contrat desk
  (last-writer-wins) tient. **CAMPAGNE D'AUDITS CLOSE (292-305)** :
  tactile, honnêteté, a11y, clavier, robustesse API, textes FR,
  performance, écriture locale — tous sains après 8 défauts corrigés
  et 3 sondeurs outillés → retour aux améliorations produit
  calibrées. Suite **2516 passed / 2 skipped**. Docs seulement, pas
  de bump. É1 : GO acquis, toujours en attente de déblocage
  permissions.

- **Lot 304 — livré** : PERFORMANCE PERÇUE mesurée (pas supposée) —
  DCL 264-341 ms sur les 8 pages (baseline lot 72 <300 ms tenue,
  /system 311 marginal ; le 630 ms initial de / était un artefact de
  FROID, re-mesuré isolément 341/300/188 ms) ; **PREMIÈRE baseline
  « temps avant contenu utile »** : 362-1055 ms selon la page (méthode
  : texte ≥60 % du final ET 0 squelette, échantillonnage 250 ms) ;
  0 squelette visible à 1 s partout. Verdict SAIN → 0 changement
  produit ; livrable = outil commité tools/probe_perceived_perf.py
  (usage, piège du froid, baselines en en-tête — les prochaines
  mesures ont un point de comparaison). compileall vert. Suite
  **2516 passed / 2 skipped**. Pas de bump. É1 : GO acquis, toujours
  en attente de déblocage permissions.

- **Lot 303 — livré** : DOUBLE AUDIT sain. (1) Clavier PROFOND :
  Entrée sur un bouton ticker de la shortlist → navigation réelle
  vers /analysis/ABNB (vrais boutons, activation native) ; délégués
  d'Aujourd'hui tous tabbables ; pairs de la fiche câblés (le seul
  sous-test ambigu = flake de sonde sur re-rendu, pas un défaut).
  (2) Qualité des textes FR (jamais balayé) : motifs typos sur le
  texte servi de 10 pages — 9 occurrences remontées, TOUTES fausses
  au tri (« réécrites »/« réévaluation » = français correct ;
  frontières d'éléments innerText ; artefact DEMO ticker=nom).
  0 défaut sur les deux angles → 0 changement (gratuit refusé).
  Suite **2516 passed / 2 skipped**. Docs seulement, pas de bump.
  É1 : GO acquis, toujours en attente de déblocage permissions.

- **Lot 302 — livré** : LOT PRODUIT — CLAVIER desktop (jamais
  balayé). Sondeur 25 tabulations sur / : skip-link premier arrêt et
  fonctionnel, focus visible 100 %, ordre logique — MAIS le Tab sur
  le champ de recherche ouvrait la palette DE FORCE (gestionnaire
  focus → blur+openPalette) : les 4 boutons du topbar (Ajouter,
  Connexions, Notifications, Actualiser) étaient INATTEIGNABLES au
  clavier. Corrigé dans vx-shell.js : plus d'ouverture au focus ;
  clic/tap inchangé (chemin tactile lot 288 préservé) + FRAPPE dans
  le champ (caractère/Entrée/↓) → palette ouverte et AMORCÉE avec le
  caractère saisi. Gardien 288 évolué (documenté) + gardien neuf
  test_keyboard_topbar_lot302 (2 tests). Preuves : 24 tabs sans
  ouverture forcée, les 4 boutons ATTEINTS, frappe « a » → palette
  amorcée « a », tap 390 OK (non-régression), 0 erreur, capture
  envoyée. Bump SW v185 → v186 + 5 gardiens. Suite **2516 passed /
  2 skipped (+2)**. É1 : GO acquis, toujours en attente de
  déblocage permissions.

- **Lot 301 — livré** : ROBUSTESSE (angle neuf) — 7 cas « API coupée
  en vol » (abort réseau + 9 s d'attente) : **SAIN partout**. États
  honnêtes quand la donnée manque (« indisponible », « ERREUR »),
  0 squelette éternel, 0 texte cassé, 0 erreur console inattendue.
  2 faits d'architecture mesurés : /markets n'appelle PAS
  /api/market/summary au chargement ; /opportunities privée de
  /scan reste complète (le radar vit de /api/command) — résilience
  par endpoint réel. Aucun défaut → 0 changement produit ; livrable
  = sondeurs OUTILLÉS et commités (tools/probe_smoke.py protocole
  251 + tools/probe_error_states.py, en-têtes d'usage + références
  — le scratchpad s'efface entre conteneurs). compileall vert.
  Suite **2514 passed / 2 skipped**. Pas de bump. É1 : GO acquis,
  toujours en attente de déblocage permissions.

- **Lot 300 — livré** : ÉCHÉANCE PÉRIODIQUE (5e mesure) — SMOKE-CHECK
  SAIN + MINI-BILAN 288-299. Smoke : 8×200, 0 erreur, client-log 0,
  healthz ok ; 5 tailles identiques, 3 écarts EXPLIQUÉS (/options
  +5 = lot 296 « board d'options » ; / +1 = calendrier daté DEMO ;
  /system 4124↔4126 = bruit d'horodatage) ; mesuré 2 fois — la 1re
  mesure était partie avant la fin du scan, refaite à conditions
  égales. Bilan de tranche : « le terminal devient utilisable au
  pouce et ne ment plus » — palette tactile complète (288/289/291),
  audit shell sain (292), 18 vues sans cible <32px (293-295), 2
  mensonges corrigés + gardien transversal (296-298), a11y 26 vues
  (299) ; suite 2496→2514 (+18, 9 gardiens neufs), SW v177→v185 (8
  bumps réels), 12 PR (#320→#331), 0 changement gratuit. Prochaine
  échéance ~lot 310. Docs seulement, pas de bump. É1 : GO acquis,
  toujours en attente de déblocage permissions.

- **Lot 299 — livré** : LOT PRODUIT — A11Y. Balayage des noms
  accessibles sur 26 vues (8 racines + 18 profondes ; dernier
  balayage a11y = lot 73) : 25/26 PARFAITES (0 bouton/lien/champ
  sans nom — l'hygiène des lots 73/209 a tenu). 2 défauts réels sur
  la fiche Analyse : #an-cp-q (question du copilote) et #an-pt-amt
  (montant du ticket pré-trade) n'avaient qu'un placeholder — pas
  une étiquette (disparaît à la saisie, lecture inconstante par les
  lecteurs d'écran) → aria-label FR sur les deux. Gardien neuf
  test_analysis_inputs_a11y_lot299 (2 tests). Preuves : aria-labels
  lus dans le DOM, 0 champ sans étiquette restant, 0 erreur,
  capture envoyée. Bump SW v184 → v185 + 5 gardiens. Suite
  **2514 passed / 2 skipped (+2)**. É1 : GO acquis, toujours en
  attente de déblocage permissions.

- **Lot 298 — livré** : GARDIEN TRANSVERSAL — plus jamais un
  « live » menteur. La leçon des lots 296/297 (mode de fraîcheur
  codé en dur pour des données qui ont un repli/une variante démo)
  codifiée à l'échelle de l'app : inventaire complet (`,'live')` +
  `mode:'live'` sur terminal.py + vertex/ui/** + static/js/**) → 2
  sites restants dans system_page, jugés HONNÊTES (état interne du
  serveur : registre des jobs, rapport de démarrage — ni repli ni
  variante démo possible). Gardien neuf
  test_freshness_mode_guard_lot298 (2 tests) avec exceptions
  DOCUMENTÉES (system_page + widget_lab, bibliothèque figée =
  spécimens d'exposition). 1er run rouge — le gardien a attrapé
  widget_lab, exception ajoutée avec justification. Suite
  **2512 passed / 2 skipped (+2)**. Tests seuls, pas de bump. É1 :
  GO acquis, toujours en attente de déblocage permissions.

- **Lot 297 — livré** : LOT PRODUIT — HONNÊTETÉ des 18 vues
  profondes. Sondeur du lot 296 étendu (étiquette démo, .vx-update,
  chasse aux revendications « réel » en DEMO) : ~30 occurrences
  triées, presque toutes légitimes. UN défaut de la même classe que
  le 296 : /portfolio?view=risk affichait « risk_engine (positions
  réelles) · Live » en plein DEMO — le mode « live » était codé EN
  DUR (portfolio_page.py L801) alors que les 4 cartes jumelles
  suivent window.__pfLive. Corrigé (live/fallback selon
  /api/pos-quotes) ; « positions réelles » conservé (vocabulaire
  établi : positions déclarées vs candidats du scanner). Gardien
  neuf test_risk_footer_mode_lot297 (2 tests — plus aucun ,'live')
  en dur dans la page). Preuves : « Secours » affiché en DEMO
  (__pfLive:false), 0 erreur, capture envoyée. Bump SW v183 → v184
  + 5 gardiens. Suite **2510 passed / 2 skipped (+2)**. É1 : GO
  acquis, toujours en attente de déblocage permissions.

- **Lot 296 — livré** : LOT PRODUIT — HONNÊTETÉ des données. Audit
  des lignes source/fraîcheur des 8 pages en DEMO : étiquette démo
  visible partout, toutes les lignes .vx-update renseignées, 0
  placeholder — SAUF un mensonge : /options affichait « À l'instant
  · multileg_lab (board réel) » en plein mode DEMO (étiquette codée
  EN DUR dans options-structure.js, alors que d.demo était connu
  juste à côté). Corrigé sur 4 sites : source du payoff + pied de
  Carte-Verdict → ternaires démo/réel ; 2 textes statiques
  d'options_intel_page (servis identiques dans les deux modes) →
  « depuis le board d'options », sans revendiquer « réel ». Gardien
  neuf test_options_board_label_lot296 (2 tests ; 1er run rouge sur
  mon propre décompte — corrigé, re-prouvé). Preuves : « board
  démo » affiché en DEMO, « board réel » absent, 0 erreur, capture
  envoyée. Bump SW v182 → v183 + 5 gardiens. Suite **2508 passed /
  2 skipped (+2)**. É1 : GO acquis, toujours en attente de
  déblocage permissions.

- **Lot 295 — livré** : LOT PRODUIT — balayage tactile TERMINÉ. Les
  12 vues profondes restantes sondées à 390 (rotation, indices,
  shortlist, positions, performance, journal, hypotheses, lab,
  screener, connections, health, /tracking) : 10/12 SAINES ;
  2 défauts réels : boutons tickers `.vx-link` de la shortlist à
  **21px** (cibles principales de la table, classe sans aucun CSS) →
  min-height:40px ; lien nu `.vx-dim a` (Journal → Hypothèses,
  16px) → même padding que `.vx-meta a` (règle séparée, gardien 293
  intact). Re-balayage : plus AUCUNE cible <32px, 0 erreur,
  0 débordement, 0 texte cassé — **18 vues profondes couvertes au
  total (lots 293/294/295)**. Gardien neuf
  test_ticker_links_touch_lot295 (2 tests). Capture envoyée. Bump
  SW v181 → v182 + 5 gardiens. Suite **2506 passed / 2 skipped
  (+2)**. É1 : GO acquis, toujours en attente de déblocage
  permissions.

- **Lot 294 — livré** : LOT PRODUIT — vues profondes : contrôles
  segmentés TAPPABLES. Sondeur du lot 293 réutilisé sur 6 vues
  ?view= à 390 (breadth, calendar, risk, track-record, positions,
  settings) : 5/6 SAINES ; défaut réel sur /system?view=settings —
  les 7 contrôles segmentés (densité, navigation latérale,
  animations) mesuraient 26px, `.vx-segmented button` échappant à la
  règle tactile mobile faute de classe vx-btn → min-height:40px en
  ≤640px, aligné sur la règle existante, desktop intact. Gardien
  neuf test_segmented_touch_lot294 (2 tests). Preuves : les 7
  boutons sortis de la liste <32px, 0 erreur, 0 débordement, les 5
  autres vues re-balayées saines, capture envoyée. Bump SW
  v180 → v181 + 5 gardiens. Suite **2504 passed / 2 skipped (+2)**.
  É1 : GO acquis, toujours en attente de déblocage permissions.

- **Lot 293 — livré** : LOT PRODUIT — fiche Analyse : liens
  d'approfondissement TAPPABLES. Calibrage du parcours profond le
  plus central (/analysis/AAPL, sondeur complet) : sain partout SAUF
  « Calendrier complet → », « Risque complet → », « Journal
  complet → » à **15px de haut** à 390 — quasi intappables au pouce
  (4 sites du motif `.vx-meta > a`). Correctif mobile ≤640px :
  `.vx-meta a{display:inline-block;padding:13px 0}` → cible 41px,
  ligne inline, desktop intact. Gardien neuf
  test_meta_links_touch_lot293 (2 tests). Preuves : les 3 liens
  sortis de la liste <32px, 0 erreur, 0 texte cassé, 0 débordement,
  capture envoyée. Bump SW v179 → v180 + 5 gardiens. Suite
  **2502 passed / 2 skipped (+2)**. É1 : GO acquis, toujours en
  attente de déblocage permissions.

- **Lot 292 — livré** : AUDIT TACTILE du shell (390, navigateur
  réel) — après la complétion du parcours palette (288/289/291), les
  3 autres parcours tactiles calibrés avec l'intention d'y livrer
  une amélioration : « Plus » (tiroir 3 espaces, liens 357×40,
  navigation réelle /options vérifiée), « Connexions » (contenu
  honnête : IBKR Hors ligne, DÉMO étiquetée), « Notifications »
  (état vide honnête). Fermetures tactiles OK, 0 erreur,
  0 débordement. **Verdict : les 3 sont SAINS — aucun changement
  fait** (un changement gratuit est pire que pas de changement).
  Capture envoyée. Suite 2500/2. Docs seulement, pas de bump. É1 :
  GO acquis, toujours en attente de déblocage permissions.

- **Lot 291 — livré** : LOT PRODUIT — la palette se ferme d'un TAP
  SUR LE FOND. Les lots 288/289 avaient soigné l'entrée tactile ; le
  calibrage de la SORTIE a montré un piège : `.vx-palette` plein
  écran ne se fermait que par Échap (inexistant au tactile) ou en
  choisissant un item — le clic vx-overlay ferme aussi mais cet
  overlay n'est jamais affiché pour la palette. Correctif standard :
  `e.target===palette → close` dans vx-shell.js. Gardien neuf
  test_palette_backdrop_close_lot291 (2 tests). Preuves 390 tactile
  + 1440 : ouverture → tap fond → fermée → réouverture → tap item →
  fermée ; 0 erreur, 0 débordement, capture envoyée. Bump SW
  v178 → v179 + 5 gardiens. Suite **2500 passed / 2 skipped (+2)**.
  É1 : GO acquis, toujours en attente de déblocage permissions.

- **Lot 290 — livré** : ÉCHÉANCE PÉRIODIQUE — smoke-check complet
  SAIN (4e mesure, protocole lot 251) : 8 pages × HTTP 200, 0 erreur
  console/pageerror, client-log count:0, healthz ok. 7 tailles sur 8
  STRICTEMENT identiques aux mesures 251/270/280 ; /system 3897→4124
  (+227) EXPLIQUÉ : la vue par défaut de /system est `connections`,
  seule vue modifiée depuis (carte « Verrou d'accès », lot 283) —
  écart = fonctionnalité livrée, base saine. Nouvelle référence
  /system = 4124. Suite 2498/2. Prochaine échéance ~lot 300. Docs
  seulement, pas de bump. É1 : GO acquis, toujours en attente de
  déblocage permissions.

- **Lot 289 — livré** : LOT PRODUIT — cible TACTILE du champ de
  recherche. Suite directe du lot 288 : le champ est LE chemin
  tactile vers la palette, or il mesurait 33px de haut à 390px, sous
  la règle des cibles ≥40px que responsive.css impose déjà aux
  boutons → min-height:40px + icône loupe recentrée (calée en absolu
  pour 33px), bloc ≤640px seulement — topbar 62px inchangé, desktop
  intact. Gardien neuf test_search_touch_target_lot289 (2 tests).
  Preuves : 390 champ 40px + icône centrée (écart 0px) + palette au
  tap (12 items), 1440 inchangé (33px), 0 débordement, 0 erreur,
  capture envoyée. Bump SW v177 → v178 + 5 gardiens. Suite
  **2498 passed / 2 skipped (+2)**. É1 : GO acquis, toujours en
  attente de déblocage permissions.

- **Lot 288 — livré** : LOT PRODUIT — palette de commandes au
  TACTILE. Le calibrage navigateur a montré que le chemin existe
  déjà (tap sur le champ de recherche → openPalette ; vérifié à
  390px : 12 items, 0 erreur) → aucun bouton ajouté, changement
  gratuit évité. Vrai défaut mesuré : à 390px le champ ne fait que
  93px et la pastille « ⌘K » s'affiche quand même — affordance
  CLAVIER mensongère au tactile (~30px mangés) → masquée en ≤640px
  (responsive.css), desktop intact. Gardien neuf
  test_palette_touch_lot288 (2 tests : tap câblé + ⌘K masqué en
  mobile). Preuves : 390 pastille masquée + palette au tap, 1440
  pastille visible + palette au clic, 0 débordement, 0 erreur,
  capture envoyée. Bump SW v176 → v177 + 5 gardiens. Suite
  **2496 passed / 2 skipped (+2)**. É1 : GO acquis, toujours en
  attente de déblocage permissions.

- **MINI-BILAN 281-286 (lot 287, rattrapage)** : tranche « la boucle
  repart en développement ». 281-282 : veille ; 283 : carte Verrou
  d'accès (v174) ; 284 : carte Application (v175) ; 285 : **GO PURGE
  É1 reçu** — tests faits et poussés, retrait terminal.py bloqué par
  le classifieur de permissions (3 approches refusées, utilisateur
  informé) ; 286 : verdict de version (v176). Suite 2486→2494 (+8) ;
  3 cartes réelles = 3 bumps ; 0 défaut produit ; 1 bug de timing
  attrapé avant livraison. É1 : GO ACQUIS, travail PRÊT, blocage
  ENVIRONNEMENTAL — à la reprise : re-générer la table des spans,
  appliquer, prouver, une PR. Docs seulement, pas de bump.

- **Lot 286 — livré** : LOT PRODUIT — la carte Application porte
  désormais un VERDICT DE VERSION : version locale (caches de
  l'appareil) vs **version publiée lue de /sw.js servi à l'instant**
  (fetch no-store — donnée réelle, aucun endpoint nouveau) → badge
  « à jour » / « mise à jour disponible » (n/d honnête si une lecture
  manque). Preuves navigateur : « locale td-shell-v176 · publiée
  td-shell-v176 · à jour », 0 erreur console, 0 débordement, capture
  envoyée. Gardien neuf test_app_version_check_lot286 (2 tests).
  Bump SW v175 → v176 + 5 gardiens. Suite **2494 passed / 2 skipped
  (+2)**.

- **Lot 285 — PURGE É1 : GO reçu, moitié 1/2 faite, moitié 2/2
  BLOQUÉE (permissions)** : le « Go » utilisateur a lancé l'Étape 1.
  Tests adaptés (cat. B : 3 fichiers de caractérisation supprimés +
  épingles retirées ; cat. C : asserts d'alias supprimés retirés, les
  alias vivants gardent les leurs) — commit b8d3842 poussé sur
  `agent/skyler-v2-lot-285`, PAS de PR (une PR = l'étape complète).
  Le retrait des 82 défs / 5 236 lignes dans terminal.py (spans prêts,
  table de l'outil commité) a été refusé 3 fois par le classifieur de
  permissions du mode auto → utilisateur informé (déblocage : règle
  Bash, mode interactif, ou « réessaie »). LE GO RESTE ACQUIS — la
  purge s'exécute en priorité dès déblocage.

- **Lot 284 — livré** : LOT PRODUIT — carte **« Application »** dans
  Système → Réglages. Comble la douleur documentée à chaque rapport
  (« iPhone : vider le cache à la main pour recevoir SW vNNN ») :
  **version du shell RÉELLE** lue des caches du navigateur
  (caches.keys() → td-shell-vN, jamais un numéro codé en dur — le
  gardien interdit tout td-shell-vN en dur dans le JS de page) + état
  du service worker + **bouton « Forcer la mise à jour de l'app »**
  (désinscrit le SW, vide CacheStorage, recharge — NE TOUCHE JAMAIS
  localStorage : les données desk survivent, gardien le fige). Bug de
  timing trouvé au navigateur (première lecture « n/d » pendant que
  le SW installait encore son cache) → cause VÉRIFIÉE avant correctif
  (le cache s'appelait bien td-shell-v175) → re-render sur
  serviceWorker.ready. Preuves : « td-shell-v175 · actif (hors-ligne
  prêt) » affichés, clic RÉEL testé (reload, caches vidés puis SW
  réinstallé), 0 débordement 1440/390, 0 erreur console, capture
  envoyée. Gardien neuf test_app_update_card_lot284 (3 tests).
  **Bump SW v174 → v175** + 5 gardiens. Suite **2492 passed /
  2 skipped (+3)**.

- **Lot 283 — livré** : DIRECTIVE « Continue à développer encore » →
  sortie de veille, LOT PRODUIT. Carte **« Verrou d'accès »** dans
  Système → Connexions — la seule amélioration produit en attente
  (lot 259 : le bouton de verrouillage ne vivait que dans
  PAGE_SETTINGS, page héritée jamais routée). Rendu dynamique selon
  l'état RÉEL du verrou (AUTH_ON, lu à la requête) : actif → badge +
  faits vérifiés (session 30 j, anti-force-brute, temps constant) +
  bouton « 🔓 Se déconnecter & verrouiller cet appareil » → /logout ;
  inactif → état honnête SANS bouton (repli 127.0.0.1, marche à
  suivre VERTEX_CODE/.env). Classes existantes uniquement, 0 littéral
  couleur, HTML entités (pas d'apostrophe nue). Gardien neuf
  test_lock_card_lot283 (3 tests : les 2 états + domicile unique).
  Preuves navigateur (DEMO) : carte visible, badge « inactif »,
  bouton absent comme attendu, 0 débordement 1440/390, 0 erreur
  console, capture envoyée. **Bump SW v173 → v174** + 5 gardiens.
  Suite **2489 passed / 2 skipped (+3)**.

- **Lot 282 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour, 0 PR oubliée, arbre propre, suite
  2486/2). Rien à toucher, rapport minimal. Pas de bump.

- **Lot 281 — livré** : VEILLE ACTIVE — état vérifié post-échéance
  (0 doublon trigger, integration à jour, 0 PR oubliée, arbre propre,
  suite 2486/2). Rien à toucher, rapport minimal. Pas de bump.

- **Lot 280 — livré** : ÉCHÉANCE PÉRIODIQUE honorée — SMOKE-CHECK
  complet SAIN (protocole lot 251 : 8 pages × HTTP 200, 0 erreur
  console/pageerror, client-log count:0, healthz ok) avec des valeurs
  STRICTEMENT identiques au lot 270 — trois mesures périodiques
  (251, 270, 280), trois résultats identiques : la base intégrée est
  STABLE. + MINI-BILAN 276-280 : 4 cycles de veille (276-279,
  rapports minimaux, 0 travail fabriqué) + cette échéance ; défauts
  produit 0 (48 lots depuis le 232) ; code produit 0 ligne (35 lots,
  246-280) ; suite 2486/2 ; SW v173 ; 5 PR (#309→#313). Prochaine
  échéance périodique ~lot 290. Pas de bump.

- **Lot 279 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour, 0 PR oubliée, arbre propre, suite
  2486/2). Rien à toucher, rapport minimal. Prochain lot (280) :
  échéance périodique (smoke-check complet + mini-bilan 276-280).
  Pas de bump.

- **Lot 278 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour, 0 PR oubliée, arbre propre, suite
  2486/2). Rien à toucher, rapport minimal. Échéance périodique dans
  2 lots. Pas de bump.

- **Lot 277 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour, 0 PR oubliée, arbre propre, suite
  2486/2). Rien à toucher, rapport minimal. Pas de bump.

- **Lot 276 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour, 0 PR oubliée, arbre propre, suite
  2486/2). Rien à toucher, rapport minimal. Échéance périodique
  ~lot 280. Pas de bump.

- **MINI-BILAN 271-275 (lot 275)** : tranche « la veille en régime de
  croisière » — première tranche entièrement en veille après
  l'échéance du lot 270. 4 cycles identiques (271-274 : état vérifié
  à chaque fois, rapports minimaux, 0 travail fabriqué) + ce bilan.
  Défauts produit : 0 (43 lots depuis le 232) ; code produit :
  0 ligne (30 lots, 246-275) ; suite 2486/2 vérifiée à chaque cycle ;
  SW v173 ; 5 PR (#304→#308). Prochaine échéance périodique :
  smoke-check complet ~lot 280. ATTENDENT L'HUMAIN (inchangé) :
  « GO purge étape 1 » (dossier exécutable), « Nettoie les branches
  de lots » (277), bouton verrouillage (sur demande), validation
  physique TWS/iPhone, merge main.

- **Lot 274 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour, 0 PR oubliée, arbre propre, suite
  2486/2). Rien à toucher, rapport minimal. Mini-bilan 271-275 au
  prochain lot. Pas de bump.

- **Lot 273 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour, 0 PR oubliée, arbre propre, suite
  2486/2). Rien à toucher, rapport minimal. Pas de bump.

- **Lot 272 — livré** : VEILLE ACTIVE — état identique (0 doublon
  trigger, integration à jour, 0 PR oubliée, arbre propre, suite
  2486/2). Rien à toucher, rapport minimal. Pas de bump.

- **Lot 271 — livré** : VEILLE ACTIVE — état vérifié (0 doublon
  trigger, integration à jour, 0 PR oubliée, arbre propre, suite
  2486/2). Rien à toucher (échéance périodique honorée au lot
  précédent), rapport minimal. Pas de bump.

- **Lot 270 — livré** : SMOKE-CHECK PÉRIODIQUE COMPLET (échéance
  annoncée depuis le lot 263, honorée) + MINI-BILAN 266-270. Protocole
  du lot 251 rejoué : **8 pages racines × HTTP 200, 0 erreur
  console/pageerror, /api/client-log count:0, healthz ok (8
  moteurs)** — résultat IDENTIQUE au lot 251 (±1 caractère
  d'horodatage) → 0 défaut, 0 changement de code. Bilan de tranche :
  cycles de veille 3-6 (266-269, rapports minimaux, 0 travail
  fabriqué) + cette échéance ; défauts produit 0 (38 lots depuis le
  232) ; code produit 0 ligne (25 lots, 246-270) ; suite 2486/2 et SW
  v173 inchangés ; 5 PR (#299→#303). Le régime de veille TIENT :
  cycles courts entre les échéances, échéance honorée avec une vraie
  mesure navigateur. Prochaine échéance périodique ~lot 280. Pas de
  bump.

- **Lot 269 — livré** : VEILLE ACTIVE, cycle 6 — état IDENTIQUE aux
  cycles 1-5 (0 doublon trigger, integration à jour, 0 PR oubliée,
  arbre propre, suite 2486/2). Rien à toucher, rapport minimal.
  Prochain lot (270) : smoke-check périodique COMPLET + mini-bilan
  266-270. Pas de bump.

- **Lot 268 — livré** : VEILLE ACTIVE, cycle 5 — état IDENTIQUE aux
  cycles 1-4 (0 doublon trigger, integration à jour, 0 PR oubliée,
  arbre propre, suite 2486/2). Rien à toucher, rapport minimal.
  Smoke-check complet dans 2 lots (~270). Pas de bump.

- **Lot 267 — livré** : VEILLE ACTIVE, cycle 4 — état IDENTIQUE aux
  cycles 1-3 (0 doublon trigger, integration à jour, 0 PR oubliée,
  arbre propre, suite 2486/2). Rien à toucher, rapport minimal.
  Pas de bump.

- **Lot 266 — livré** : VEILLE ACTIVE, cycle 3 — état IDENTIQUE aux
  cycles 1-2 (0 doublon trigger, integration à jour, 0 PR oubliée,
  arbre propre, suite 2486/2). Rien à toucher, rapport minimal.
  Smoke-check périodique prévu ~lot 270. Pas de bump.

- **MINI-BILAN 261-265 (lot 265)** : tranche « la boucle atterrit en
  veille ». 261 : CLAUDE_VERTEX_REBUILD.md neutralisé (dernier risque
  documentaire — un ordre de mission périmé pouvait détourner une
  future session ; les 6 .md racine sont sains) ; 262 : constat
  honnête d'épuisement des pistes → VEILLE ACTIVE + inventaire jamais
  fait (303 branches distantes dont 277 mortes, nettoyage proposé sur
  demande) ; 263-264 : deux cycles de veille prouvés — courts,
  honnêtes, zéro travail fabriqué ; 265 : ce bilan. Défauts produit :
  0 (33 lots depuis le 232) ; code produit : 0 ligne (20 lots,
  246-265) ; suite 2486/2 et SW v173 inchangés ; 5 PR (#294→#298).
  RÉCAP de ce qui attend l'humain : « GO purge étape 1 » (dossier
  complet exécutable avec baseline de gain) ; « Nettoie les branches
  de lots » (277, commande prête) ; bouton de verrouillage visible
  (sur demande) ; validation physique TWS/iPhone (SW v173) ; merge
  main (accord explicite).

- **Lot 264 — livré** : VEILLE ACTIVE, cycle 2 — état IDENTIQUE au
  cycle 1 (0 doublon trigger, integration à jour, 0 PR oubliée, arbre
  propre, suite 2486/2). Aucun code produit changé, aucun signal, rien
  à toucher. Rapport minimal conformément au régime de veille. Pas de
  bump.

- **Lot 263 — livré** : VEILLE ACTIVE, cycle 1. État vérifié : 1 seul
  trigger actif (0 doublon), integration à jour (lot 262 fusionné),
  0 PR oubliée, arbre propre, suite **2486 passed / 2 skipped**.
  Constat honnête : aucun code produit changé depuis v173 → aucune
  re-mesure due (prochain smoke-check périodique raisonnable ~lot
  270), aucun signal d'anomalie — RIEN À TOUCHER ce cycle (le toucher
  aurait été du travail fabriqué). Docs seulement, pas de bump.

- **Lot 262 — livré** : CONSTAT D'ÉTAT — les pistes autonomes sont
  ÉPUISÉES (produit mesuré correct depuis le lot 232, invariants tous
  audités, 6 .md racine sains, baseline perf posée, dossier de purge
  complet et exécutable) → la boucle passe en **VEILLE ACTIVE** :
  entretien espacé, constats courts, toute directive exécutée
  immédiatement. Mesure du lot (jamais faite) : **303 branches
  distantes**, dont 266 `agent/skyler-v2-lot-*` fusionnées squash +
  11 rc-periodique = **277 branches mortes sûres à supprimer** (leur
  contenu vit dans integration et les PR #1→#294) — nettoyage
  PROPOSÉ, PAS exécuté (action de masse sur l'infra partagée →
  déclenchable sur demande : « Nettoie les branches de lots »).
  Vérifications légères : 1 seul trigger actif (0 doublon),
  integration à jour, aucune PR ouverte oubliée. Docs seulement, pas
  de bump. Suite **2486 passed / 2 skipped**.

- **Lot 261 — livré** : CLAUDE_VERTEX_REBUILD.md NEUTRALISÉ. Le
  dernier .md racine non audité n'était pas une doc d'accueil mais un
  ORDRE DE MISSION pour Claude datant de l'ère Total Rebuild, resté
  actif à la racine : « travaille sur agent/vertex-total-rebuild » +
  livrables d'époque — en CONTRADICTION directe avec la gouvernance
  CLAUDE.md (skill vertex-skyler-v2, branche integration, anciennes
  branches = références historiques). Risque réel : une future session
  pouvait suivre l'ancien ordre. Calibrage avant de trancher : fichiers
  pointés existants, branche encore sur origin, document référencé par
  les audits d'époque → PAS de suppression — bannière d'obsolescence
  en tête qui neutralise l'ordre et redirige vers la gouvernance
  actuelle. **Les 6 .md racine sont désormais tous audités et sains.**
  Docs seulement, pas de bump. Suite **2486 passed / 2 skipped**.

- **MINI-BILAN 256-260 (lot 260)** : tranche « mesurer le neuf,
  aligner les portes d'entrée ». 256 : baseline perf serveur jamais
  chiffrée (import 11,68 s à froid / ~2 s à chaud ; TTFB 8 pages
  1,3-1,9 ms — le coût du mort est à l'IMPORT, métrique avant/après
  purge) ; 257-259 : audit systématique des docs d'ACCUEIL contre le
  code — **10 défauts corrigés (4 README + 3 DEMARRER_ICI + 3
  SECURITE), dont 2 touchant la sécurité** (« écoute 0.0.0.0 »
  prétendue ; bouton de déconnexion fantôme dans une page orpheline) ;
  .env.example audité EXACT. Défauts produit : 0 (28 lots depuis le
  232) ; 0 ligne de code produit touchée (15 lots, 246-260) ; suite
  2486/2 et SW v173 inchangés ; 5 PR (#289→#293) ; 1 redémarrage
  worker (256) repris sans perte. LEÇON : les docs d'accueil dérivent
  silencieusement jusqu'à contredire la sécurité réelle — l'audit
  « affirmation par affirmation, tracée vers la ligne de code » les a
  remis au vrai. ATTEND L'HUMAIN : « GO purge étape 1 » (dossier
  complet avec baseline de gain) ; bouton de verrouillage visible sur
  demande ; validation physique TWS/iPhone ; merge main sur accord.

- **Lot 259 — livré** : SECURITE.md ↔ RÉALITÉ (dernier .md racine
  d'accueil non audité). VRAI et vérifié dans la source : cookie 30 j
  httponly/SameSite=Lax (terminal.py L133-134), comparaison à temps
  constant (auth.py L127 hmac.compare_digest), anti-force-brute
  5 essais → verrou progressif min(300, 15×(n-4)) s (auth.py L133).
  **3 corrections** : le « bouton Se déconnecter & verrouiller dans
  Paramètres » est un BOUTON FANTÔME — il ne vit que dans
  PAGE_SETTINGS (terminal.py L7477), page héritée orpheline (0 routée,
  preuve lot 248) → doc corrigée vers la route /logout qui, elle,
  fonctionne ; « désactiver le verrou → l'app redevient ouverte »
  omettait le repli 127.0.0.1 sans code (lot 218) → précisé ; liste
  des pages publiques complétée sur la vraie PUBLIC_PATHS (auth.py
  L28-30 : + /logout, /api/healthz, webhook TradingView signé).
  CONSTAT à l'humain : le bouton de verrouillage n'a jamais été
  recâblé dans la nouvelle UI — /logout couvre le besoin ; bouton
  visible dans Système = petit lot produit SUR DEMANDE. Docs
  seulement, pas de bump. Suite **2486 passed / 2 skipped**.

- **Lot 258 — livré** : DEMARRER_ICI.md ↔ RÉALITÉ (suite de l'audit
  des portes d'entrée). **3 défauts corrigés** : nom de dossier périmé
  `IBKT-DASHBORD-` (×2) → `Vertex-` ; table des espaces PRÉ-REFONTE
  (Overview/Matinal/Comité/Recherche/Décisions/Santé/Fiche titre) →
  les 8 espaces canoniques réels ; « badge 🟢 LIVE IBKR en haut à
  droite » inexistant → l'état de source réel « Live/Différé/Hors
  ligne » du panneau d'état (vx-shell.js L205-209, vérifié AVANT de
  trancher). **`.env.example` audité ligne par ligne : EXACT, non
  touché** (sémantique VERTEX_CODE conforme au comportement gardé lot
  218 ; READONLY énoncé ; sections à jour). Lanceurs DEMO vérifiés
  existants — section conservée. Les 3 portes d'entrée du dépôt
  (README lot 257, DEMARRER_ICI, .env.example) sont désormais alignées
  sur la réalité. Docs seulement, pas de bump. Suite **2486 passed /
  2 skipped**.

- **Lot 257 — livré** : README ↔ RÉALITÉ — la vitrine du dépôt n'avait
  jamais été auditée contre les faits mesurés. **4 défauts corrigés,
  dont 1 de SÉCURITÉ** : le README affirmait « le serveur écoute déjà
  sur tout le réseau local (0.0.0.0) » alors que la réalité durcie et
  GARDÉE (test_network_binding_lot218) est l'écoute 127.0.0.1 par
  défaut, LAN seulement via VERTEX_CODE (verrou) ou VERTEX_LAN=1 →
  section réécrite avec la vraie procédure ; liste de pages
  pré-refonte (/titre, /entreprises, /watchlist) → les 8 espaces
  canoniques + note de redirection ; « 57 leaders US » → univers réel
  S&P 500 ∪ Nasdaq 100 ∪ Dow (~500 titres, healthz 517) ; structure
  périmée → routes/pages/moteurs actuels. Calibrage AVANT correction :
  ib_reader.py vérifié réel et branché (sa ligne était correcte —
  conservée), fichiers pointés tous existants, 0 test n'épingle le
  README. Docs seulement, pas de bump. Suite **2486 passed / 2
  skipped**.

- **Lot 256 — livré** : BASELINE de performance SERVEUR avant-purge
  (jamais chiffrée formellement — le lot 72 mesurait le client).
  Import de terminal.py : **11,68 s à froid, ~2 s à chaud** (3
  passes) ; TTFB des 8 pages racines : **1,3-1,9 ms** (3 mesures
  chacune, HTML 22-86 ko) ; healthz 3 ms. Lecture honnête : le
  SERVICE est instantané (pages = chaînes préconstruites — rien à
  corriger) ; le coût du code mort est à l'IMPORT, payé à chaque
  démarrage pour construire notamment des pages héritées jamais
  servies — c'est LA métrique que la purge devrait améliorer, à
  re-mesurer avec le même protocole après É1/É2. Reprise après
  redémarrage du worker en début de lot (état vérifié : lot 255
  fusionné, 0 trigger actif — rien perdu). 0 changement de code,
  docs seulement, pas de bump. Suite **2486 passed / 2 skipped**.

- **MINI-BILAN 251-255 (lot 255)** : tranche « consolider sans
  fabriquer ». 251 : smoke-check santé post-merges SAIN (8 pages ×
  200, 0 erreur console, client-log 0) ; 252 : outil de chiffrage
  rendu rejouable de partout (1 défaut d'OUTILLAGE prouvé puis corrigé,
  chiffres identiques au lot 249) ; 253 : annexe É1 — liste exacte des
  82 défs triée A/B/C, le « GO » devient exécutable sans
  reconstruction ; 254 : audit invariant « fichiers runtime jamais
  commités » TENU (0 traqué, 0 incohérence, .gitignore 100 % des
  sites d'écriture) ; 255 : ce bilan. **10 lots consécutifs (246-255)
  sans toucher au code produit** — chaque lot une mesure ou un outil,
  jamais du remplissage. Suite 2486/2 et SW v173 inchangés ; 5 PR
  (#284→#288) ; défauts produit : 0 (23 lots consécutifs). État : la
  purge est PRÊTE (preuves + fourchette 31,4-48,7 % + outil robuste +
  liste triée) et bloquée PAR CONCEPTION sur « GO purge étape 1 » ;
  les pistes autonomes restantes sont de l'entretien périodique que la
  boucle ESPACE plutôt que d'en fabriquer.

- **Lot 254 — livré** : AUDIT de l'invariant « fichiers runtime jamais
  commités » (règle Git de CLAUDE.md — le seul invariant jamais audité
  formellement). 3 volets mesurés : `git ls-files` × motifs interdits
  → **0 fichier runtime traqué** (unique match : un fichier de TEST au
  nom similaire) ; `ls-files -ci` → **0 incohérence** traqué/ignoré ;
  croisement .gitignore ↔ sites d'écriture RÉELS de l'app →
  **couverture 100 %** (skyler_memory/sessions/decisions.json +
  alerts_fired.json listés nommément ; les 3 caches couverts par
  `*_cache.json` ; les jokers du rituel de nettoyage = ceinture-
  bretelles, aucun fichier réel ne correspond aux variantes).
  INVARIANT TENU → 0 correctif. Docs seulement, pas de bump. Suite
  **2486 passed / 2 skipped**.

- **Lot 253 — livré** : ANNEXE É1 — la liste EXACTE des retraits de
  l'Étape 1, générée et triée (`ANNEXE-E1-RETRAITS.md`, **0 purge**).
  Mode `--e1` ajouté à l'outil officiel : 82 défs du périmètre borne
  basse (spans de lignes, tailles) + fichiers de tests impactés,
  régénérable à volonté. Triage en 3 catégories d'action : A retrait
  sec ; B retrait avec les tests de caractérisation (lot183/184/185 +
  épingles — écrits POUR ce moment) ; **C re-cibler le test PUIS
  retirer l'alias** — découverte du lot : `_rsi`/`_atr`/`_adx`/
  `_demo_one`/`_vehicle_of`/`_swing_project` sont des alias de
  compatibilité vers des moteurs VIVANTS (vertex/engines/indicators,
  vertex/data/demo, strategy_fit, swing) — les tests fonctionnels qui
  les importent gardent leur valeur, seul l'import change. 2 faux
  positifs de grep (`home` : fonction locale d'un test + mot de
  commentaire) vérifiés dans la source et marqués à ignorer. Dossier
  de décision mis à jour (ligne É1 → annexe). Aucun code produit
  touché, pas de bump. Suite **2486 passed / 2 skipped**.

- **Lot 252 — livré** : ROBUSTESSE de l'outil de décision
  `tools/purge_e2_sizing.py` (l'instrument officiel du chiffrage,
  rejoué à É1/É2). Défaut PROUVÉ avant de toucher : lancé depuis
  `docs/` → FileNotFoundError (open/grep/import relatifs au cwd).
  Correctif minimal : racine du dépôt ancrée sur `__file__` +
  `os.chdir`. Preuve : rejoué depuis docs/ ET depuis la racine —
  chiffres identiques entre eux et IDENTIQUES au lot 249 (5 236 l. /
  48,7 % ; 107 défs) → la mesure est STABLE et reproductible. Aucun
  code produit touché, pas de bump. Suite **2486 passed / 2 skipped**.

- **Lot 251 — livré** : SMOKE-CHECK santé post-tranche en conditions
  réelles. Après les 5 merges docs-only (246-250), re-mesure en vrai
  navigateur (serveur DEMO, Playwright 1440×900, écoute console +
  pageerror) : **8 pages racines × HTTP 200, 0 erreur console,
  /api/client-log count:0, healthz ok** (8 moteurs, scan démo 20/517).
  Verdict SAIN → 0 changement de code. Docs seulement, pas de bump.
  Suite **2486 passed / 2 skipped**.

- **MINI-BILAN 246-250 (lot 250)** : tranche « du prouver au préparer
  la décision ». 246 : 4e parcours métier (journalisation d'une
  décision d'un trait, écriture réelle prouvée) ; 247 : grande synthèse
  de la campagne 214-246 (produit MESURÉ correct) ; 248 : dossier de
  décision de purge (21 fonctions héritées / 0 routée / 21 orphelines) ;
  249 : chiffrage outillé É2 (fourchette 31,4-48,7 % de terminal.py
  mort, outil commité, 2 pièges gravés) ; 250 : ce bilan. **0 ligne de
  code produit touchée sur les 5 lots** — le produit est prouvé et la
  règle « jamais de changement gratuit » a tenu. Suite 2486/2 et SW
  v173 inchangés ; 5 PR (#279→#283) ; 3 faux positifs d'outils
  attrapés avant conclusion. État honnête : les pistes autonomes
  s'amincissent ; le seul gros chantier restant (purge chiffrée) est
  bloqué PAR CONCEPTION sur « GO purge étape 1 » — la boucle continue
  en entretien utile sans fabriquer du travail.

- **Lot 249 — livré** : CHIFFRAGE OUTILLÉ de l'Étape 2 de la purge —
  **AUCUNE purge**, l'estimation « 25-30 % » du dossier devient une
  FOURCHETTE MESURÉE. Outil commité (`docs/refactor/validation/tools/
  purge_e2_sizing.py`, mark-and-sweep AST : racines = 14 fonctions
  routées mesurées en runtime + 18 décorées + 26 module-level +
  externes ; 2 passes). Résultat sur terminal.py (10 743 l.) : borne
  BASSE certaine **3 370 lignes mortes (31,4 %) / 408 ko (33,4 %)**
  (82 défs) ; borne HAUTE **5 236 lignes (48,7 %) / 692 ko (56,6 %)**
  (107 défs) si les boucles d'injection partent avec. DEUX PIÈGES
  mesurés et gravés au dossier (§ 1d) : 12 constantes PAGE_*
  référencées par CHAÎNE via `globals()[_pg]` (l. ~6537-6588 — retrait
  sans adaptation = KeyError à l'import) ; dépendance croisée NOUVELLE
  `PAGE_ENTREPRISES` → `_OPP_BRIEF_JS` → injecté dans `PAGE_DAILY`
  (l. ~6088-6097) → Étape 3, pas avant. Doctrine tenue : 1er passage à
  49,2 % avec 4 faux positifs (fonctions décorées after_request/
  errorhandler) — vérifiés dans la source, script corrigé AVANT
  publication du chiffre. Décision inchangée : « GO purge étape 1 »
  attendue. Docs + outil seulement, pas de bump. Suite
  **2486 passed / 2 skipped**.

- **Lot 248 — livré** : DOSSIER DE DÉCISION DE PURGE de terminal.py
  (TERMINAL-PURGE-DECISION.md) — **0 code touché**, tout est preuve
  et plan. PREUVE DÉCISIVE mesurée ce lot : croisement runtime
  app.url_map × fonctions retournant PAGE_* → **21 fonctions de rendu
  héritées trouvées, 0 routée, 21 ORPHELINES** — aucun utilisateur ne
  peut les atteindre (cohérent avec les 43 « route migrée » et le
  constat du lot 246). Les 32 constantes PAGE_* ne sont référencées
  hors terminal.py QUE par les tests de caractérisation écrits POUR
  ce moment (lot 183 + épingles). Une exception cartographiée :
  PAGE_DAILY ↔ home_art.py/vault.py (hérités eux-mêmes) → étape
  dédiée. PLAN en 3 étapes sûres — É1 fonctions orphelines + PAGE_*
  + tests de caractérisation sans objet ; É2 blocs BODY/CSS/JS
  révélés non référencés (chiffrage outillé) ; É3 dépendances
  croisées — une PR par étape, rollback = revert, pytest 100 % +
  navigateur 8 pages à chaque étape. **DÉCISION DEMANDÉE À L'HUMAIN :
  « GO purge étape 1 » — rien ne sera purgé sans.** Docs seulement,
  pas de bump. Suite **2486 passed / 2 skipped**.

- **Lot 247 — livré** : GRANDE SYNTHÈSE DE LA CAMPAGNE DE PREUVE
  (lots 214 → 246, 33 lots, PR #247 → #279). Après la clôture de la
  tournée graphique TV (204), la boucle a basculé de « construire » à
  « PROUVER ». Chiffres : suite 2472 → **2486** (+14), SW v171 →
  **v173** (2 bumps, chacun porté par un correctif réel), **6
  gardiens neufs**, **3 correctifs produit** (tous
  mesurés-minimaux-vérifiés), ~30 protocoles navigateur. PROUVÉ :
  les 8 invariants CLAUDE.md (8/8 tenus, 3 lacunes de garde
  comblées) ; le rendu honnête (0 NaN affiché) ; la navigation
  (31 liens, 177 boutons) ; le responsive COMPLET (3 débordements
  réels corrigés, 0 faux correctif) ; le shell interactif entier ;
  l'infrastructure (SW réel — doctrine bump=déploiement prouvée,
  desk sync round-trip client) ; les 4 PARCOURS métier (analyse,
  contrat, GEX, journal-écriture). **0 défaut produit depuis le lot
  232 : le produit est MESURÉ correct, du pixel au blob de sync.**
  RESTE EN ATTENTE HUMAINE : (1) purge de terminal.py (~25-30 % mort
  cartographié, dont la page Journal héritée) — accord explicite
  requis ; (2) validation physique TWS réel + iPhone (vider le cache
  pour SW v173) ; (3) merge vers main — accord explicite requis.
  Docs seulement, pas de bump. Suite **2486 passed / 2 skipped**.

- **Lot 246 — livré** : PARCOURS JOURNAL D'UN TRAIT — le dernier flux
  d'ÉCRITURE du produit prouvé de bout en bout. /journal?view=journal
  → bouton « Ajouter une entrée » → formulaire de décision →
  NVDA + Enregistrer → **1 entrée dans vxJournal local** → NVDA
  présent dans le blob /api/desk (push VXEntities) → rechargement :
  l'entrée **persiste et s'affiche** → nettoyage PAR LE PROTOCOLE
  (retirée du store, poussée, absente du serveur — desk_data.json
  jamais édité à la main). 0 erreur console. Calibrage honnête : deux
  fausses pistes écartées — le jTicker/jSave de vertex/ui/journal.py
  appartient à la page Journal HÉRITÉE (PAGE_JOURNAL de terminal.py,
  plus servie par /journal — candidate connue à la purge en attente
  d'accord) ; le VRAI produit passe par performance_page
  (j-ticker/j-confirm, store VXEntities) — c'est lui qui est prouvé.
  Les QUATRE parcours sont prouvés : les 3 lectures (analyse 241,
  contrat 242, GEX 243) ET l'écriture (journal 246). Constat honnête,
  aucun code touché, pas de bump. Suite **2486 passed / 2 skipped**.

- **Lot 245 — livré** : MINI-BILAN 241-245. Tranche de 5 lots
  (PR #274 → #278) : suite **2486 / 2 skipped stable**, SW **v173
  STABLE** (0 bump — 5 lots de preuve pure). Réalisations : les
  3 PARCOURS MÉTIER prouvés d'un trait — (1) plan d'analyse actions :
  clic ACN → /analysis/ACN, plan complet, 8 canvas LWC + 32 SVG
  (241) ; (2) contrat options : radar 50 → détail payoff/R:R/théta/IV
  avec « estimation modèle, pas une promesse », note de méthode
  canvas∉innerText gravée (242) ; (3) positionnement GEX : radar
  18/18 avec « n/d » honnête → détail cohérent (243) ; (4) vues
  Système internes 4/4 → couverture des vues EXHAUSTIVE (244). FAIT
  MARQUANT : **le produit ENTIER est mesuré correct** — après le
  shell (236-240), ce sont les chemins de VALEUR qui sont prouvés ;
  3 tranches de preuve sans un seul défaut produit depuis le lot
  232 : le socle est sain et DÉMONTRÉ tel. Doctrine : 5 lots, 0 ligne
  de code produit, 0 bump, chaque faux positif d'outil corrigé avant
  conclusion. Docs seulement, pas de bump.
  Suite **2486 passed / 2 skipped**.

- **Lot 244 — livré** : VUES SYSTÈME INTERNES — les deux dernières
  vues jamais balayées du produit (/system?view=connections et
  /system?view=archive), au protocole discriminant, à 390 px ET
  1440 px, en contexte navigation. RÉSULTAT : **4/4 propres** —
  0 overflowX, 0 dépassement droit, 0 marqueur malhonnête (texte DOM
  et SVG balayés), 0 erreur console. La couverture des VUES est
  désormais EXHAUSTIVE : 8 pages racines (390+768) + 6 secondaires +
  15 vues internes — auxquelles s'ajoutent états vides (219),
  liens/boutons (221), composants et flux du shell (229-236), SW
  (237), sync (239) et les 3 parcours métier (241-243). Constat
  honnête, aucun code touché, pas de bump.
  Suite **2486 passed / 2 skipped**.

- **Lot 243 — livré** : PARCOURS GEX D'UN TRAIT — le 3e parcours
  métier prouvé de bout en bout. /options?view=positioning → radar
  de positionnement rendu (**18/18 titres exploitables** : SPOT,
  NET GEX en M$, régime stabilisant/accélérateur, biais, bascule Ø-Γ
  avec **« n/d » honnête** quand inconnue — jamais un chiffre
  inventé —, murs call/put, max pain) → saisie ACN dans #vx-gx-sym →
  détail GEX rendu : murs call/put, gamma, flip, spot, 10 barres,
  chips de valeurs — cohérent avec la ligne ACN du radar
  (bascule 192,92 · mur call 198,2 · mur put 189,4). 0 marqueur
  malhonnête (texte DOM ET texte SVG balayés — leçon du lot 242),
  client-log 0, 0 erreur console. Capture envoyée. Les TROIS parcours
  métier sont prouvés d'un trait : plan d'analyse actions (241),
  contrat options (242), positionnement GEX (243). Constat honnête,
  aucun code touché, pas de bump. Suite **2486 passed / 2 skipped**.

- **Lot 242 — livré** : PARCOURS CONTRAT OPTIONS D'UN TRAIT — le 2e
  cœur métier prouvé de bout en bout. /opportunities?view=options →
  radar rendu (**50 contrats**) → clic sur un contrat → détail
  COMPLET : payoff canvas hachuré zones PERTE/GAIN avec **chip
  BE 136.98** et ligne spot (« Breakeven 136.98 · prime 3812 ») ;
  matrice R:R simulé 7 scénarios × J+0→J+28 avec la mention
  d'honnêteté « MODEL_ESTIMATE — estimation modèle, pas une
  promesse » ; décomposition temps hachurée + chip Min ; sensibilité
  IV avec dominante en chip. 0 vocabulaire d'ordre, client-log 0,
  0 erreur console. NOTE DE MÉTHODE honnête : le premier passage
  textuel déclarait « payoff absent » — FAUX POSITIF de l'outil (les
  libellés d'un canvas ne vivent pas dans innerText) ; la
  vérification VISUELLE a corrigé le classement avant toute
  conclusion (réflexe du lot 238 : jamais déclarer un défaut sur une
  heuristique). Capture envoyée. Les DEUX cœurs métier (analyse
  actions 241, contrat options 242) sont prouvés. Constat honnête,
  aucun code touché, pas de bump. Suite **2486 passed / 2 skipped**.

- **Lot 241 — livré** : PARCOURS D'ANALYSE COMPLET — le cœur métier
  de Vertex (voir un titre → ouvrir son analyse → lire le plan)
  prouvé d'UN SEUL trait en navigateur, alors que les pages n'avaient
  été validées qu'isolément. Parcours réel : clic sur le menu
  d'entité ACN depuis / → « Ouvrir l'analyse » → navigation vers
  /analysis/ACN → **plan complet rendu** : verdict, niveaux
  (entrée/stop/objectif), conviction, comité, scénario/cône —
  **8 canvas LWC** (le vendor chargé par cette seule page) +
  **32 graphiques SVG** hydratés, 0 marqueur malhonnête, 32 états
  honnêtes —/n/d, /api/client-log count 0, 0 erreur console. Capture
  du plan envoyée. Le chemin de valeur quotidien — délégué de clic →
  navigation → vendor → hydratation → plan lisible — est prouvé de
  bout en bout. Constat honnête, aucun code touché, pas de bump.
  Suite **2486 passed / 2 skipped**.

- **Lot 240 — livré** : MINI-BILAN 236-240. Tranche de 5 lots
  (PR #269 → #273) : suite **2486 / 2 skipped stable**, SW **v173
  STABLE** (0 bump — 5 lots de preuve pure, rien à déployer).
  Réalisations : (1) modal d'ajout 3 étapes prouvé, écriture réelle
  au store + READONLY affirmé dans l'UI même — « Vertex n'envoie
  JAMAIS un ordre » (236) ; (2) service worker v173 prouvé en vrai —
  actif, seul cache présent (nettoyage prouvé), 32/32 statiques
  servies du cache en 2e visite : la doctrine bump=déploiement est
  prouvée (237) ; (3) docs : 0 référence morte sur 94 fichiers, les
  17 signalements d'heuristique tous résolus individuellement (238) ;
  (4) desk sync round-trip côté client réel — push au ts exact, pull
  au boot qui restaure tout après localStorage.clear (239). FAIT
  MARQUANT : **la preuve du shell est TOTALE** — composants (229/231/
  234), flux (236), infrastructure (237/239), navigation et
  responsive (219-233) : chaque mécanisme de l'expérience quotidienne
  déroulé en conditions réelles, 0 défaut trouvé sur la tranche — le
  produit tient. Doctrine : 5 lots, 0 ligne de code produit, 0 bump,
  et chaque lot a produit du SAVOIR vérifié. Docs seulement, pas de
  bump. Suite **2486 passed / 2 skipped**.

- **Lot 239 — livré** : DESK SYNC ROUND-TRIP CÔTÉ CLIENT RÉEL —
  l'invariant n° 1 (17 clés / 4 listes) et la préférence utilisateur
  centrale (« tout synchronisé automatiquement au lancement ») sont
  gardés côté serveur depuis longtemps, mais le CHEMIN CLIENT n'avait
  jamais été prouvé en navigateur. Protocole (avec sauvegarde
  préalable de desk_data.json et nettoyage PAR LE PROTOCOLE — règle
  n° 6, jamais d'édition à la main) : (1) écriture locale
  toggleFavorite('TSLA') ; (2) push débouncé 1200 ms → **ts serveur =
  ts client à la milliseconde près** et TSLA dans myFavs du blob ;
  (3) localStorage.clear() + rechargement (« appareil neuf ») → le
  pull au boot **restaure TSLA, deskTs et 5 clés desk** ;
  (4) nettoyage : favori retiré → push → TSLA retiré du serveur.
  La chaîne écriture → débounce → POST /api/desk → persistance →
  pull → réhydratation fonctionne exactement comme conçue. 0 erreur
  console. Constat honnête, aucun code touché, pas de bump.
  Suite **2486 passed / 2 skipped**.

- **Lot 238 — livré** : LIENS .md DANS docs/ HORS VALIDATION — la
  piste proposée cinq fois, enfin prise. 94 fichiers .md balayés
  (validation/ exclu — déjà gardé au lot 228) : 1 lien markdown
  formel → valide ; 162 mentions backticks → 17 signalées par
  l'heuristique de chemin, puis CHAQUE signalement vérifié par
  recherche du nom dans tout le dépôt : 14 fichiers EXISTANTS
  ailleurs (docs/refactor/, docs/release/,
  .claude/skills/vertex-skyler-v2/references/, .claude/FRAMEWORK.md)
  et 3 gabarits/raccourcis de prose (placeholder SKYLER-LOT-XX,
  plage « 08A.md à 08E.md »). **0 référence réellement morte** — pas
  un seul « mort » déclaré sur la foi d'une heuristique de chemin.
  Gardien non pertinent ici (les mentions par nom seul sont un usage
  légitime ; la zone à risque est gardée depuis le 228). Constat
  honnête, aucun code touché, pas de bump.
  Suite **2486 passed / 2 skipped**.

- **Lot 237 — livré** : SERVICE WORKER v173 VÉRIFIÉ EN NAVIGATEUR
  RÉEL — le SW est bumpé et gardé depuis 173 versions mais son
  comportement n'avait JAMAIS été vérifié en vrai (littéraux de
  source seulement). Protocole : 1re visite / (enregistrement,
  activation, caches), 2e visite /markets (nouvelle page, même
  contexte). RÉSULTAT : SW enregistré + ACTIF (scope /) ;
  **td-shell-v173 est le SEUL cache présent** — le nettoyage des
  caches périmés à l'activation est prouvé ; precache 5 entrées
  (coquille : manifest, icône, fonts) ; 2e visite : page CONTRÔLÉE
  par le SW et **32/32 ressources statiques servies du cache**
  (transferSize=0) — le cache runtime fait exactement le travail
  conçu (hasShellJs=false au precache n'est PAS un défaut : les JS
  entrent au cache à la 1re requête). La doctrine « bump =
  déploiement » qui gouverne la boucle depuis 173 versions est
  désormais PROUVÉE, pas supposée. 0 erreur console. Constat honnête,
  aucun code touché, pas de bump. Suite **2486 passed / 2 skipped**.

- **Lot 236 — livré** : MODAL D'AJOUT D'ENTITÉ — le dernier flux
  interactif du shell jamais testé en navigateur, avec la vérif
  READONLY la plus sensible (c'est le SEUL endroit du produit où
  l'utilisateur saisit une « position »). Parcours réel : bouton + →
  modal « Ajouter » (barre d'étapes 1/0/0) → NVDA + Continuer → 6
  destinations (1/1/0) → Watchlist → formulaire priorité/zone/thèse/
  catalyseur (1/1/1) → Confirmer → modal fermé et **NVDA réellement
  écrit dans la watchlist du store** (VXEntities.watchlist() le
  contient). READONLY : texte des 3 étapes balayé, y compris le
  formulaire Position → **0 vocabulaire d'ordre** ET la mention
  « Registre déclaratif — Vertex n'envoie JAMAIS un ordre » est
  affirmée DANS l'interface, au seul endroit où la confusion serait
  possible. 0 erreur console. TOUS les flux interactifs du shell sont
  prouvés (drawer/modal 229, palette 231, menu 234, ajout 236).
  Constat honnête, aucun code touché, pas de bump.
  Suite **2486 passed / 2 skipped**.

- **Lot 235 — livré** : MINI-BILAN 231-235. Tranche de 5 lots
  (PR #264 → #268) : suite **2486 / 2 skipped stable**, SW v172 →
  **v173** (1 seul bump, porté par le seul correctif réel de la
  tranche). Réalisations : (1) palette de commande prouvée
  comportementalement — Ctrl+K, filtre, flèches, Entrée navigue,
  câblage VXEntities vivant (231) ; (2) vues internes 390 balayées,
  1 débordement réel soldé — .vx-update REPLIE, ellipse refusée sur
  une info d'honnêteté (232) ; (3) couverture responsive COMPLÈTE :
  8 racines (390+768) + 6 secondaires + 13 vues — campagne totale
  3 défauts réels corrigés, 2 bumps justifiés, 0 faux correctif
  (233) ; (4) menu contextuel prouvé + READONLY vérifié — 0 action
  d'ordre dans les libellés (234). FAIT MARQUANT : TOUS les
  composants interactifs du shell sont prouvés en conditions réelles
  (drawer/modal 229, palette 231, menu 234) — le shell n'est plus
  supposé correct, il est MESURÉ correct. Doctrine : 4 lots de
  constat sans code produit, 1 correctif mesuré-minimal-vérifié.
  Docs seulement, pas de bump. Suite **2486 passed / 2 skipped**.

- **Lot 234 — livré** : MENU CONTEXTUEL D'ENTITÉ — le dernier
  composant interactif jamais testé en navigateur, avec vérif
  READONLY explicite. Calibrage instructif : les déclencheurs
  [data-entity-menu] vivent dans le DOM hydraté de / (3) et /markets
  (20) — pas sur /opportunities en démo. Parcours réel sur / (bouton
  ACN) : menu ouvert (11 actions, focus DANS le menu, entièrement
  dans le viewport) ; flèches ↓↓ suivies (data-active + focus sur
  l'item actif) ; clic-dehors ferme. **READONLY vérifié : 0 action
  d'ordre** — balayage des libellés contre {acheter, vendre, ordre,
  buy, sell, transmettre, passer} → vide ; « Ajouter une position »
  est un ENREGISTREMENT au journal personnel (localStorage/desk
  sync), pas un ordre — l'invariant tient jusque dans le vocabulaire.
  0 erreur console. TOUS les composants interactifs du shell sont
  désormais prouvés en conditions réelles (drawer/modal 229, palette
  231, menu 234). Constat honnête, aucun code touché, pas de bump.
  Suite **2486 passed / 2 skipped**.

- **Lot 233 — livré** : DERNIÈRES VUES À 390px — la couverture
  responsive navigateur est COMPLÈTE. Les 3 vues jamais balayées
  (/journal?view=journal, /journal?view=track-record,
  /intelligence?view=committee) au protocole discriminant, en
  contexte navigation : **3/3 propres** (0 overflowX, 0 dépassement
  droit, 0 marqueur malhonnête, 0 erreur console). CAMPAGNE SOLDÉE :
  8 pages racines (390 au lot 222 + 768 au lot 224) + 6 pages
  secondaires (223) + 13 vues internes (232 + 233) — tout le produit
  navigable balayé. Bilan de la campagne : **3 défauts réels trouvés
  et corrigés** (crumb /tracking 433px, bouton retour /portfolio
  403px intermittent, ligne de fraîcheur knowledge graph 591px),
  2 bumps SW justifiés (v172, v173), 0 faux correctif. Constat
  honnête, aucun code touché, pas de bump.
  Suite **2486 passed / 2 skipped**.

- **Lot 232 — livré** : VUES INTERNES À 390px — le protocole
  discriminant du 222 appliqué aux 10 vues à onglets JAMAIS balayées
  (opportunités options/anomalies/calendrier, options volatilité/
  positionnement, marchés secteurs/volatilité/breadth, portefeuille
  watchlist/risque), en contexte navigation. RÉSULTAT : 9/10 propres,
  **1 débordement RÉEL** trouvé — /portfolio?view=risk : la ligne de
  fraîcheur/source .vx-update du knowledge graph (nowrap, 562px)
  finissait à 591px, 201px coupés hors écran. Correctif MINIMAL scopé
  ≤768px : .vx-update REPLIE (white-space:normal + overflow-wrap) —
  l'ellipse REFUSÉE délibérément : c'est une info d'HONNÊTETÉ (la
  traçabilité de la source doit rester entièrement lisible). Vérifié :
  ligne repliée à 361px ≤ 390, les 10 vues rejouées → 0 défaut,
  0 erreur console. Captures avant/après envoyées. Bump SW
  **v172 → v173** + 5 gardiens (composant de toutes les cartes — le
  correctif doit se déployer). Suite **2486 passed / 2 skipped**.

- **Lot 231 — livré** : PALETTE DE COMMANDE — le constat
  comportemental complet d'un composant JAMAIS testé en navigateur
  (seuls des littéraux de source étaient gardés). Parcours réel en
  démo : **Ctrl+K** ouvre (input focusé, 11 items en 3 groupes
  Positions/Pages/Actions — la position réelle ACN du store y figure :
  le câblage VXEntities est vivant, pas décoratif) ; filtre « march »
  → 4 items ; **flèches** ↓↓↑ suivies par aria-selected (idx 0→2→1) ;
  **Échap** ferme ; le clic sur la barre de recherche ouvre aussi
  (blur→openPalette) ; « archive » + **Entrée** → navigation RÉELLE
  vers /system?view=archive, palette fermée. 0 erreur console.
  Constat honnête, aucun code touché, pas de bump.
  Suite **2486 passed / 2 skipped**.

- **Lot 230 — livré** : MINI-BILAN 226-230. Tranche de 5 lots
  (PR #259 → #263) : suite 2482 → **2486** / 2 skipped (+4), SW
  **v172 STABLE** (0 bump — 5 lots de constat/garde, rien à
  déployer). Réalisations : (1) budgets JS mesurés — chart-core.js
  57,2/64 kB (89 %, marge 6,8 kB, +18 kB coût légitime de la tournée
  TV), calibration du gardien recalibrée + consigne « discuter le
  budget AVANT de le crever » (226) ; (2) dette TODO : 0 marqueur
  dans tout le code produit + perf serveur : 16 routes, médianes
  1,2-2,9 ms (227) ; (3) mémoire de la boucle GARDÉE : 218 références
  d'index → 0 morte, périmètre 01-09 enfin écrit, gardien
  index↔rapports — le rituel est un invariant testé (228) ; (4) cycle
  drawer/modal au clavier prouvé comportementalement — focus revenu
  au déclencheur, closeAll referme les deux (229). Doctrine : tranche
  100 % « mesurer avant de toucher » — 0 ligne de code produit
  modifiée, 1 gardien neuf, 2 recalibrations de vérité, chaque
  constat chiffré. Docs seulement, pas de bump.
  Suite **2486 passed / 2 skipped**.

- **Lot 229 — livré** : CYCLE DRAWER/MODAL AU CLAVIER — le constat
  COMPORTEMENTAL qui manquait aux lots 209/210 (eux prouvaient les
  attributs, celui-ci déroule le vrai parcours). Protocole Playwright
  sur `/` : clic RÉEL sur Notifications → drawer ouvert (attributs
  levés, overlay, focus DANS le panneau) → Échap → fermé, attributs
  reposés, **focus revenu au déclencheur** (vx-notifs-btn) ; modal
  via le chemin produit VX.shell.openModal → même cycle impeccable ;
  les DEUX ouverts + UN SEUL Échap → les deux reposent
  aria-hidden/inert (focus → body : closeAll ne peut pas choisir un
  déclencheur — limitation connue, pas un défaut). Observation
  classée : le modal s'ouvre SANS l'overlay partagé — VOULU (son
  conteneur est plein écran fixed inset:0 ; l'overlay sert au
  drawer). 0 erreur console. Le retour de focus lastFocus posé au 209
  est prouvé en conditions réelles. Constat honnête, aucun code
  touché, pas de bump. Suite **2486 passed / 2 skipped**.

- **Lot 228 — livré** : INTÉGRITÉ SKYLER-INDEX ↔ RAPPORTS — la
  mémoire de la boucle vérifiée puis GARDÉE. Mesure : 218 références
  citées dans l'index → **0 morte** (tous les rapports existent) ;
  231 rapports sur disque → 13 sans ligne d'index = les lots 01-09
  (batch correctness pré-Institutional+), hors champ PAR CONSTRUCTION
  (l'index commence au lot 10, STATUS retrace le début) — mais ce
  périmètre n'était écrit nulle part. Livré : (1) périmètre documenté
  dans l'en-tête de l'index ; (2) gardien
  test_skyler_index_integrity_lot228 (4 tests — références mortes
  cassent la suite, rapports orphelins cassent la suite (exemption
  01-09 bornée par regex), périmètre documenté, anti-vide ≥ 200
  références réellement vérifiées). Le rituel « rapport + ligne
  d'index à chaque lot » n'est plus une habitude : c'est un invariant
  TESTÉ. Docs/tests seulement, pas de bump. (Lot repris proprement
  après un redémarrage du worker en début d'exécution.)
  Suite **2486 passed / 2 skipped** (2482 + 4).

- **Lot 227 — livré** : DETTE TODO + PERF SERVEUR — double constat
  mesuré, 0 défaut. (1) Balayage TODO/FIXME/XXX/HACK (mot entier) sur
  TOUT le code produit (terminal.py + vertex/** py/js/css, vendor
  exclu) : **0 occurrence** — aucune dette auto-documentée éparpillée ;
  la dette CONNUE vit où elle doit (rapports de purge, en attente
  d'accord humain). (2) Chronométrage réel (urllib, 5 passes/route,
  DEMO chaud) des 8 routes HTML + 8 API critiques : **16/16 en 200,
  médianes 1,2 à 2,9 ms, pire cas 8 ms** (premier hit de /) — la
  génération serveur (HTML en chaînes Python) est négligeable devant
  le budget DCL < 300 ms du lot 72 ; le coût du chargement est côté
  navigateur, déjà budgété et gardé (72 + dérive mesurée au 226).
  Constat honnête, aucun code touché, pas de bump.
  Suite **2482 passed / 2 skipped**.

- **Lot 226 — livré** : BUDGETS JS/CSS STATIQUES — la piste proposée
  trois fois, enfin prise. Mesure de vertex/static/** contre les
  gardiens du lot 72 (64 kB/fichier première partie, vendor isolé).
  VERDICT : gardien VERT, aucune violation — mais dérive réelle
  documentée : **chart-core.js 39 → 57,2 kB** (+18 kB, coût LÉGITIME
  de la tournée TV 189-213 : jauge, hachures, chips, extrêmes, radar
  dominant, levelLines) soit **89 % du budget**, marge restante
  6,8 kB ; options-intel 39,1 kB (61 %) ; neon-glass.css 47 kB
  (73 %) ; vendor 160 kB toujours chargé par /analysis seule (gardien
  d'isolement vert). CONTRE-VÉRITÉ corrigée : le commentaire de
  calibration du gardien affirmait encore « chart-core 39 kB » —
  recalibré aux valeurs mesurées, avec consigne explicite : au
  prochain palier, discuter le budget AVANT de le crever (pas de
  hausse en douce — c'est la dérive que le gardien ferme).
  Tests/docs seulement, pas de bump.
  Suite **2482 passed / 2 skipped**.

- **Lot 225 — livré** : MINI-BILAN 221-225. Tranche de 5 lots
  (PR #254 → #258) : suite **2482 / 2 skipped stable**, SW v171 →
  **v172** (1 seul bump, porté par le SEUL correctif réel de la
  tranche). Le balayage NAVIGATEUR systématique du produit est
  SOLDÉ — l'audit a porté là où pytest ne voit rien (DOM hydraté,
  contexte de navigation) et la méthode a payé : (1) liens/boutons —
  31 liens internes × HTTP 200, 177 boutons tous câblés (221) ;
  (2) 2 débordements RÉELS du topbar mobile trouvés et soldés — crumb
  /tracking 433px + bouton retour /portfolio 403px INTERMITTENT
  (reproduit en navigation) → ellipse scopée ≤768px, bump v172
  (222) ; (3) pages secondaires 390 en navigation : 6 pages 0 défaut
  (223) ; (4) tablette 768 au point de rupture exact du media query :
  8 pages 0 défaut (224). Couverture navigateur cumulée depuis 219 :
  états vides ✔, liens ✔, boutons ✔, 390 principal + secondaires ✔,
  768 ✔. Doctrine tenue : 4 lots sans code produit dits honnêtement ;
  le seul correctif mesuré, minimal, vérifié dans le contexte
  défaillant rejoué. Docs seulement, pas de bump.
  Suite **2482 passed / 2 skipped**.

- **Lot 224 — livré** : RESPONSIVE 768px (TABLETTE) — chasse aux
  cousins des défauts topbar du lot 222, au point de rupture EXACT du
  media query du correctif (max-width:768px — là où un défaut de bord
  serait le plus probable), protocole discriminant en contexte
  navigation sur les 8 espaces. RÉSULTAT : **0 défaut partout** —
  overflowX 0, 0 dépassement droit d'élément visible, 0 erreur
  console. Le correctif 222 s'applique bien à 768 inclus (fil
  d'Ariane et bouton retour tronquent aussi en tablette) et aucune
  autre famille de défauts n'apparaît à ce viewport. Constat honnête,
  aucun code touché, pas de bump. (Lot exécuté sur ordre « continue »,
  trigger réarmé.) Suite **2482 passed / 2 skipped**.

- **Lot 223 — livré** : PAGES SECONDAIRES À 390px — le protocole
  discriminant du lot 222 étendu aux pages JAMAIS balayées en
  responsive, et en CONTEXTE DE NAVIGATION (2 pages visitées avant →
  bouton retour visible — précisément le contexte qui piégeait
  /portfolio au 222). Balayage : /titre/AAPL, /company/AAPL,
  /analysis/ACN, /intelligence, /login, /design-system. RÉSULTAT :
  **0 défaut sur les 6 pages** — overflowX 0, 0 dépassement droit
  d'élément visible, 0 marqueur malhonnête (NaN/undefined/Infinity),
  0 erreur console. Le correctif du 222 (fil d'Ariane + bouton retour
  en ellipse, shell partagé) couvre bien ces pages. Constat honnête,
  aucun code touché, pas de bump.
  Suite **2482 passed / 2 skipped** (référence maintenue).

- **Lot 222 — livré** : RESPONSIVE 390px — 2 DÉBORDEMENTS RÉELS du
  topbar trouvés et SOLDÉS (le spot-check navigateur a enfin payé).
  Mesure : overflowX document = 0 partout (les gardes tiennent), MAIS
  en discriminant off-canvas voulu / dépassement droit réel :
  (1) /tracking — le crumb « Approfondissement du Portefeuille »
  (nowrap 213px) finissait à 433px, texte passant SOUS les boutons ;
  (2) /portfolio en NAVIGATION — le libellé du bouton retour (nowrap
  155px) poussait le cluster droit à 403px (refresh coupé de 13px) ;
  intermittent car le bouton retour n'apparaît qu'en navigation —
  reproduit en visitant 3 pages avant. Correctif MINIMAL scopé ≤768px
  (responsive.css) : .vx-breadcrumb flex:1/overflow hidden + enfants
  min-width:0/ellipsis ; .vx-back-btn span idem — fil et libellé
  TRONQUENT au lieu de passer dessous. Vérifié : contexte défaillant
  rejoué → cluster à 378px ≤ 390 ✔ ; balayage 8 pages → 0 dépassement,
  0 erreur console ; captures avant/après envoyées. Bump SW
  **v171 → v172** + 5 gardiens (CSS du shell — le correctif doit se
  déployer). Suite **2482 passed / 2 skipped**.

- **Lot 221 — livré** : LIENS INTERNES + BOUTONS — balayage
  NAVIGATEUR des 8 pages en démo (DOM hydraté — les gardiens
  existants ne voient que la source servie). Protocole : serveur DEMO
  (healthz ok/demo), Playwright 1440×900, extraction des a[href]
  internes dédupliqués + GET réel sur chaque cible, et inventaire des
  button avec détection de câblage (onclick, data-* des délégués
  globaux, submit, aria-controls). RÉSULTAT : **31 liens internes
  uniques → 31 × HTTP 200 (0 lien mort)** ; **177 boutons
  (18+55+39+12+10+20+13+10) → 0 sans câblage détectable**. Cohérent
  avec l'architecture des délégués clavier/clic posés aux lots
  précédents. Constat honnête, aucun code touché, pas de bump.
  Suite **2482 passed / 2 skipped** (référence maintenue).

- **Lot 220 — livré** : MINI-BILAN 216-220. Tranche de 5 lots
  (PR #249 → #253) : suite 2472 → **2482** / 2 skipped (+10 : 3+4+3),
  SW **v171 STABLE** — 5 lots sans bump (doctrine des constats : rien
  à déployer, dit honnêtement). Réalisations : (1) AUDIT D'INVARIANTS
  CLAUDE.md TERMINÉ — 8 invariants vérifiés par constat mesuré, 0
  violation ; (2) 3 gardiens NEUFS sur lacunes réelles (invariants
  documentés mais épinglés par aucun test) : RequestTimeout=45
  anti-blocage IBKR (216), scan_state jamais réassigné — scan AST des
  3 formes interdites (217), écoute réseau 127.0.0.1 sans code (218) ;
  (3) audit navigateur des états vides honnêtes (219, piste jamais
  réalisée) : 8 pages, 0 marqueur malhonnête, 0 erreur console ;
  (4) doctrine tenue — aucun code produit modifié sur toute la
  tranche, calibrage avant de toucher. Docs seulement, pas de bump.
  Suite **2482 passed / 2 skipped**.

- **Lot 219 — livré** : ÉTATS VIDES HONNÊTES EN DÉMO — l'audit
  NAVIGATEUR jamais réalisé (le DOM après hydratation JS est hors de
  portée du test_client — c'est là que NaN/undefined apparaîtraient).
  Protocole : serveur DEMO (healthz data_source:demo), Playwright
  1440×900 (domcontentloaded + 4500 ms) sur les 8 espaces ; par page :
  recherche des marqueurs malhonnêtes affichés (NaN, undefined, null,
  Infinity), comptage des états honnêtes (—/n/d), étiquette démo,
  erreurs console. RÉSULTAT : **0 marqueur malhonnête sur les 8
  pages**, états honnêtes présents partout (1 à 21 par page),
  étiquette démo confirmée serveur sur les 8, **0 erreur console**,
  /api/client-log count:0 après balayage complet. Invariant n° 4
  (« jamais de chiffre inventé affiché comme réel ») TENU — constat
  honnête, aucun code touché, pas de bump.
  Suite **2482 passed / 2 skipped** (référence maintenue).

- **Lot 218 — livré** : FIN DE L'AUDIT D'INVARIANTS CLAUDE.md (lots
  214/216/217/218). (1) Filet desk_data.json : TENU et déjà gardé par
  test_desk_backup_lot178 (8 tests — snapshot quotidien créé AVANT le
  premier écrasement du jour, jamais réécrit ensuite, rotation 7 j,
  validation stricte du restore) — rien à ajouter. (2) Écoute réseau
  (« sans code d'accès, le serveur n'écoute que 127.0.0.1 ») : règle
  TENUE dans _start_app (lan_ok = AUTH_ON ou VERTEX_LAN=1 ou $PORT →
  0.0.0.0 ; sinon 127.0.0.1) MAIS gardée par AUCUN test (grep lan_ok/
  0.0.0.0/VERTEX_LAN dans tests/ → 0) — on pouvait exposer le desk à
  tout le Wi-Fi sans casser la suite. Livré :
  test_network_binding_lot218 (3 tests — source épinglée, table de
  vérité sur la même expression avec VERTEX_LAN=0 ≠ opt-in, message
  config honnête). BILAN DE L'AUDIT : 8 invariants vérifiés par
  constat, 3 lacunes de garde réelles comblées (RequestTimeout=45,
  scan_state, écoute réseau), 0 violation. Tests seulement, pas de
  bump. Suite **2482 passed / 2 skipped** (2479 + 3).

- **Lot 217 — livré** : INVARIANT scan_state « muté en place — ne
  JAMAIS réassigner » (state.py / CLAUDE.md) — constat mesuré + gardien
  AST. Scan du code produit (terminal.py + vertex/**, trois formes
  interdites : réassignation module-level hors state.py, affectation
  d'attribut .scan_state, global scan_state) → **0 offenseur** ; les 5
  `scan_state = scan_state or {}` des moteurs sont des rebinds LOCAUX
  de paramètres (ils ne touchent pas l'objet partagé — légitimes).
  Lacune : AUCUN des ~30 fichiers de tests utilisant scan_state ne
  vérifiait CET invariant, alors que le casser est silencieux et grave
  (boucle de fond et routes garderaient des objets différents — pages
  figées sans erreur). Livré : test_scan_state_invariant_lot217
  (4 tests — scan AST, domicile unique documenté, gardien-du-gardien
  sur exemple synthétique qui prouve que le scanner détecte bien les 3
  formes, et non-faux-positif sur le rebind local). Tests seulement,
  pas de bump. Suite **2479 passed / 2 skipped** (2475 + 4).

- **Lot 216 — livré** : INVARIANTS n° 2 + IBKR (suite de l'audit du
  lot 214) — constat mesuré + UN gardien neuf sur lacune réelle.
  (1) Règle n° 2 (JS généré valide / apostrophes) : TENUE et déjà
  gardée en entier par test_js_syntax_sweep_lot182 (chaque bloc
  <script> inline de 16 routes au vrai parseur node --check + chaînes
  JS des modules + garde-fou de volume ≥12 blocs) — rien à ajouter.
  (2) IBKR : readonly=True TENU, codé en dur (READONLY = True +
  connect readonly=True) et gardé par 3 tests (test_no_orders balayage
  dépôt, strategy_os_final_guards, data_sources). MAIS lacune RÉELLE
  mesurée : grep RequestTimeout tests/ → 0 occurrence — l'invariant
  CLAUDE.md « RequestTimeout=45 (ne pas retirer — anti-blocage) »
  n'était épinglé par AUCUN test. Livré :
  test_ibkr_timeout_lot216 (3 tests) — valeur 45, les DEUX bornes
  appliquées dans la façade readonly (ib.RequestTimeout + timeout du
  connect), et scheduler DEFAULT_TIMEOUT_S aligné sur le gateway (si
  l'un bouge sans l'autre, le test casse). Tests seulement, pas de
  bump. Suite **2475 passed / 2 skipped** (2472 + 3).

- **Lot 215 — livré** : MINI-BILAN 211-215 + vérif cohérence SW.
  Tranche de 5 lots (PR #244 → #248) : suite 2466 → **2472** / 2
  skipped (+6), SW v168 → **v171** (bumps 211/212/213 ; 214/215 =
  constats sans bump). Réalisations : (1) chasse aux hex nus COMPLÈTE
  — 5 littéraux soldés sur 4 sites (movers Système, étiquettes RRG,
  bordure démo Opportunités, texte des tuiles treemap) ; (2) 2
  gardiens pérennes BORNÉS verrouillent la chaîne entière (pages
  Python lot 212 + builders JS lot 213) — plus aucun endroit où un
  hex nu peut se glisser sans casser la suite ; (3) invariants
  CLAUDE.md vérifiés par constat mesuré (desk sync 17 clés/4 listes,
  sanitize_news 6 sorties SANITIZED + faux positif écarté) ;
  (4) doctrine tenue — 2 lots de constat sans code produit, dits
  honnêtement. Entretien du lot : cohérence SW vérifiée —
  td-shell-v171 identique dans system.py L211 ET les 5 gardiens,
  aucune dérive de version. Docs seulement, pas de bump.
  Suite **2472 passed / 2 skipped**.

- **Lot 214 — livré** : AUDIT D'INVARIANTS CLAUDE.md par CONSTAT
  MESURÉ (pas sur parole). (1) Desk sync (règle n° 1) : gardien
  test_desk_sync_keys_single_source_of_truth relancé → 1 passed ;
  comptage direct : __DESK_KEYS (terminal.py) = 17 clés, DESK_KEYS
  (vx_kit.py) = 17 identiques, et journal.py porte les 17 inline dans
  le JS jvSyncPush — exactement ce que le gardien vérifie. TENU.
  (2) sanitize_news (règle n° 5) : cartographie exhaustive — les 6
  points de sortie de contenu news (content.py, api_skyler, api_events,
  skyler_sweep.py, terminal.py ×2) passent TOUS par sanitize_news ; le
  signalement system_status_ep écarté comme FAUX POSITIF après lecture
  du corps réel (le champ 'news' y est un seuil de fraîcheur interne —
  thresholds 3600 s, et build_system_status ne sert que age_s + enum
  _freshness : aucun texte externe ne transite). Gardien XSS lot 177
  relancé → 6 passed. TENU. Docs seulement, pas de bump (doctrine des
  lots de constat). Suite **2472 passed / 2 skipped**.

- **Lot 213 — livré** : GARDIEN HEX NU ÉTENDU AUX BUILDERS JS
  (charts/*.js + pages/*.js — test_no_bare_hex_static_js_lot213,
  3 tests), calibré AVANT d'écrire : 49 occurrences → 40 =
  DÉFINITIONS de palette (le bloc C.colors de chart-core + le thème
  obsidian-copper entier — la source des tokens doit bien porter les
  hex quelque part ; exemptions BORNÉES par leurs marqueurs exacts et
  testées : si les bornes bougent, le test casse au lieu de scanner à
  côté), 8 = lookups col(VC,'n','#hex') légitimes, et 1 littéral
  RÉELLEMENT nu soldé : le texte des tuiles du treemap
  (fill="#f3f1ed" → var(--vx-text-primary,#F8F5F3), SVG var() natif,
  repli d'inventaire sûr). Avec le lot 212, la chaîne COMPLÈTE est
  couverte (pages Python + builders JS) — plus aucun endroit où un
  hex nu peut se glisser sans casser la suite. Bump SW v170 → v171 +
  5 gardiens (le texte des tuiles change subtilement — déploiement).
  Capture treemap envoyée, 0 erreur console.
  Suite **2472 passed** / 2 skipped (2469 + 3).

- **Lot 212 — livré** : GARDIEN « AUCUN HEX NU DANS LES PAGES » —
  le balayage des lots 211-212 pérennisé en pytest
  (test_no_bare_hex_pages_lot212, 3 tests) : tout hex quoté dans
  vertex/ui/pages/*.py est REFUSÉ hors formes de repli légitimes
  (var(--…,#hex), cc/col/cssv('…','#hex'), lookup||'#hex'), avec
  exemption DOCUMENTÉE et testée de widget_lab.py (bibliothèque
  design FIGÉE, palette de mise en scène délibérée). CORRECTION
  HONNÊTE au passage : le « balayage complet » du lot 211 était
  incomplet — la calibration a trouvé 2 littéraux nus de plus,
  soldés : étiquettes RRG de Marchés ('#bab4ac' →
  VXCharts.colors.muted||'#8A8284', repli dans l'inventaire sûr) et
  bordure démo d'Opportunités ('#FFC857' → VXCharts.colors.warning).
  Calibré contre l'état réel avant commit : 10 occurrences → 2
  réelles (soldées) + 8 widget_lab (exemptées) → gardien vert à 0.
  Bump SW v169 → v170 + 5 gardiens (deux pages visibles changent
  subtilement — déploiement). Captures RRG + Opportunités envoyées,
  0 erreur console. Suite **2469 passed** / 2 skipped (2466 + 3).

- **Lot 211 — livré** : ENTRETIEN — deux choses. (1) Le constat
  « movers absents en démo » du lot 199 ré-examiné et CLOS : pas un
  trou silencieux — l'hôte n'est créé que si movers.length, et
  l'absence de cotations est déjà couverte par l'état honnête de la
  table (« Aucune cotation web pour l'instant… »). (2) Dette RÉELLE
  trouvée dans le même bloc et soldée : les barres movers coloraient
  en HEX NUS ('#36c889'/'#ed655c') — le DERNIER littéral couleur nu
  des pages (balayage complet : toutes les autres occurrences sont
  des lookups de tokens avec fallback, motif légitime) → remplacés
  par VXCharts.colors.positive/negative (VXCharts garanti présent
  par la garde de la branche). Bump SW v168 → v169 + 5 gardiens : le
  rendu peut changer subtilement (hex figé → vraie valeur du token)
  et le correctif doit atteindre les clients en cache. Note honnête :
  pas de capture possible (movers exigent des cotations web,
  absentes en démo) — preuve par code + balayage.
  Suite 2466 passed / 2 skipped.

- **Lot 210 — livré** : PREUVE NAVIGATEUR du cycle a11y du MODAL et
  du chemin closeAll (complément du 209 qui n'avait prouvé que le
  drawer) : modal fermé {aria-hidden:true, inert} → ouvert {retirés}
  → refermé {reposés} ; closeAll (Échap/overlay) avec modal + drawer
  ouverts ensemble → les DEUX reposent leurs attributs (délégation à
  panelClose par construction) ; 0 erreur console. AUCUN code à
  changer — ce lot prouve au lieu de supposer. Docs seulement, pas
  de bump. + MINI-BILAN 206-210 (ci-dessous).
  Suite 2466 passed / 2 skipped (inchangée).

### MINI-BILAN tranche 206-210

5 lots, PR #239 → #243, suite 2461 → 2466 (+5 gardiens a11y),
SW v167 → v168 (un seul bump — le vecteur de déploiement du correctif
a11y, pas un bump cosmétique). Tranche d'APRÈS-TOURNÉE, entièrement
dans la doctrine « mesurer avant de toucher » : tour responsive
complet MESURÉ (lots 206-207 — 9 espaces × 5 viewports = 45/45
cellules sans débordement ni erreur console, 0 correctif nécessaire),
cohérence de la grammaire TV vérifiée par INVENTAIRE mesuré (208 —
divergences toutes justifiées, 0 retouche gratuite), accessibilité
des panneaux hors-canvas CORRIGÉE et gardée (209 — aria-hidden +
inert + 5 gardiens ; 210 — cycle prouvé modal + closeAll). Trois lots
sur cinq n'ont pas touché une ligne de code produit : le produit
était déjà droit, et la boucle l'a prouvé au lieu de le décorer.
EN ATTENTE de directive : purge terminal.py (~25-30 % mort,
cartographié, accord humain requis) ; sinon entretien continu.

- **Lot 209 — livré** : ACCESSIBILITÉ des panneaux hors-canvas
  (l'observation du lot 206 corrigée) : le drawer d'entité et le
  modal FERMÉS portent désormais aria-hidden="true" + inert dans le
  markup servi par le shell, et vx-shell.js les bascule proprement
  (panelOpen retire les deux attributs, panelClose les repose — même
  chemin pour les deux panneaux, retour de focus préservé). Sidebar
  mobile laissée hors périmètre en connaissance de cause : visible
  sur desktop, repli piloté par media query CSS — un aria-hidden JS
  risquerait une régression desktop pour un gain nul (rapporté).
  Cycle PROUVÉ en navigateur : fermé {aria-hidden:true, inert} →
  ouvert {retirés} → refermé {reposés}, 0 erreur console. Gardien
  test_a11y_drawer_lot209.py (5 tests : HTML servi, source JS,
  identité dialogue, focus). Bump SW v167 → v168 + 5 gardiens —
  JUSTIFIÉ : le HTML du shell change, sans bump les clients en cache
  ne recevraient jamais le correctif (le bump est le vecteur de
  déploiement). Suite **2466 passed** / 2 skipped (2461 + 5).

- **Lot 208 — livré** : INVENTAIRE MESURÉ DE COHÉRENCE (option 2 de
  la proposition lot 205) : script d'analyse des builders charts +
  pages sur 4 axes — (1) police des chips : tvEdgeChip fontSize 9
  PARTOUT, chips canvas 700 9px uniformes, libellés de zones 8.5 sur
  viewBox denses ; (2) hachures : alphas IDENTIQUES SVG/canvas
  (.08/.38), tuiles 6 vs 8 et traits 1.6 vs 1.4 = équivalence
  visuelle voulue entre userSpace SVG et pixels canvas ; (3) rayons
  ≈ h/2 partout (coins pleinement arrondis cohérents) ; (4) pieds de
  cartes : 3 classes à 3 RÔLES distincts (vx-chart-foot = pied
  graphique avec fraîcheur, vx-meta = note, vx-muted = secondaire) —
  une sémantique, pas une divergence. Seul point suspect vérifié :
  fontSize 11 de candlestick-lwc = config d'AXES de Lightweight
  Charts (faux positif de grep). VERDICT : toutes les divergences
  sont JUSTIFIÉES → AUCUNE retouche (harmoniser serait un changement
  gratuit — risque sans gain). Option 2 SOLDÉE par constat. AUCUN
  code touché, AUCUN bump SW. Suite 2461 passed / 2 skipped.

- **Lot 207 — livré** : TOUR RESPONSIVE 2/2 (mesuré, même protocole
  que le 206) : /portfolio, /options, /journal, /system,
  /intelligence × 5 viewports — 0 px de débordement de page sur les
  25 cellules, 0 erreur console, seuls les panneaux hors-canvas
  voulus signalés (mécanisme translateX déjà vérifié).
  ★ VERDICT GLOBAL DU TOUR (lots 206-207) : 9 espaces × 5 viewports
  = **45/45 cellules propres** — aucune page de Vertex ne défile
  horizontalement entre 390 et 1920 px, aucune erreur console, tous
  les habits TV de la tournée tiennent à toutes les tailles.
  L'option 1 de la proposition du lot 205 est SOLDÉE en 2 lots sans
  un seul correctif nécessaire — la discipline responsive des
  refontes précédentes a tenu. AUCUN code touché, AUCUN bump SW.
  Captures de contrôle Portefeuille 1920 + Intelligence 390
  envoyées. Suite 2461 passed / 2 skipped.

- **Lot 206 — livré** : TOUR RESPONSIVE post-tournée 1/2 (mesuré,
  option par défaut de la proposition du lot 205) : 4 espaces
  (Aujourd'hui, Marchés, Opportunités, Analyse) × 5 viewports
  (390/768/1024/1440/1920), mesure Playwright de (a) débordement
  horizontal de page, (b) éléments hors viewport (hors défilement
  voulu et fixed), (c) erreurs console. VERDICT : 0 défaut réel —
  débordement de page 0 px sur les 20 cellules, 0 erreur console ;
  tous les éléments signalés sont des panneaux hors-canvas VOULUS
  (sidebar mobile repliée à gauche à 390, drawer d'entité fermé par
  translateX à 768+ — vérifiés au style calculé). Les habits TV de
  la tournée (chips, hachures, dégradés, dominantes) passent
  proprement du mobile au 1920. Observation rapportée sans agir :
  le drawer fermé n'a pas d'aria-hidden (piste accessibilité, pas un
  défaut de layout). AUCUN code touché, AUCUN bump SW. Captures de
  contrôle 1920 + 390 envoyées. Suite 2461 passed / 2 skipped.

- **Lot 205 — livré** : BILANS — mini-bilan 201-205 + BILAN DE
  CLÔTURE de la tournée graphique TV (ci-dessous) + proposition de
  suite chiffrée (décision humaine). Aucun code produit touché —
  vérification visuelle des dernières captures sans défaut évident,
  donc pas de changement gratuit ni de bump SW. Suite 2461 passed /
  2 skipped (inchangée).

### MINI-BILAN tournée 201-205

5 lots, PR #234 → #238, suite stable 2461 passed / 2 skipped,
SW v164 → v167 (stable depuis le 204 — deux lots de constats sans
changement visible, la règle de bump respectée dans les deux sens).
Réalisations : radar à sommet dominant (201), price-chart — canonique
LWC constaté TV natif + repli levelLines en chips au bord droit
(202), cône de mouvement σ hachuré + murs GEX en dominantes à chips
(203), dernier balayage en 3 constats honnêtes et INVENTAIRE 100 %
TRAITÉ (204), bilans et passation (205).

### ★ BILAN DE CLÔTURE — TOURNÉE GRAPHIQUE TV (lots 189 → 204)

Directive utilisateur (lot 188) : « que tout Vertex ressemble à ça —
fluide, beau, parfait » (langage visuel TradingView). Livré en
16 lots (189-204), PR #222 → #237, SW v153 → v167, suite verte
2461/2 à CHAQUE lot, 0 erreur console à chaque capture.

**Grammaire commune créée (chart-core & co)** :
- jauge TV : arc ENTIER en dégradé continu + pointeur blanc court
  (189) — héritée par 6+ jauges (santé, VIX, breadth, comité, risque,
  environnement options) ;
- `tvHatch` (SVG) + `hatchPattern` (canvas) : la texture « estimation,
  pas un réel » (189/197) — cône de projection, payoff, théta, cône σ ;
- `tvEdgeChip` + chips canvas : étiquettes pleine couleur à texte
  sombre (189) — bords du cône, treemap, niveaux du plan, extrêmes,
  barres dominantes, murs GEX, rails, radar, runway ;
- `tvExtremesPlugin` : chips Max/Min sur les extrêmes RÉELS (195) —
  équité, drawdown, série de référence ;
- `.vx-rail-chip` : chip de valeur sur pointeur de rail (198).

**Règles transverses appliquées partout** :
- DOMINANTE EN ÉVIDENCE (jamais sur singleton) : consensus, heatmap,
  staleness, barres, radar, GEX, stress tests (préexistant) ;
- ESTIMATION HACHURÉE : toute projection assume sa texture ;
- CHIPS DE VALEURS RÉELLES : les chiffres clés se lisent sur le
  graphique, pas à côté.

**Héritages gratuits constatés** (un builder aligné = ses pages
alignées) : scénarios Options (via heatmap), discipline Journal +
sensibilité IV + leadership + movers (via C.bars), jauges (via
C.gauge), équité/drawdown/série de référence (via C.area).

**Honnêteté tenue de bout en bout** : constats démo rapportés sans
agir (prime aberrante, tuiles sans P&L, movers/journal vides, env
options absent), « n/d » sur régime indéterminé, pas de sparkline
sans série, pas de dominante inventée. Un correctif structurel au
passage : __VXVOCAB injecté par le shell (191).

### Proposition de suite (décision humaine — rien n'est lancé)

1. **Tour responsive complet post-tournée** : 8 espaces × 5 viewports
   (390→1920), vérification visuelle des nouveaux chips/hachures aux
   petites tailles, corrections des débordements trouvés
   (~2-3 lots). ← choix par défaut de la boucle si rien n'est dit.
2. **Polish transverse de cohérence** : uniformiser les pieds de
   cartes, les tailles de chips et les densités de hachures entre
   pages (~2 lots).
3. **PURGE de terminal.py** : ~25-30 % du monolithe mort cartographié
   et figé par tests (lots 183-185) — EN ATTENTE D'ACCORD HUMAIN
   EXPLICITE, jamais lancée sans.
4. **Attente de directive** : la boucle continue sur des lots
   d'entretien (gardiens, honnêteté, petites dettes).

- **Lot 204 — livré** : TOURNÉE TV — DERNIER BALAYAGE de
  l'inventaire (lot de CONSTATS, aucun code produit modifié) :
  (1) « double probabilité » = la colonne P(doubler) du scanner
  d'options, une estimation DÉJÀ étiquetée « EST. » avec sa
  définition en pied — la doctrine de la tournée y était ; (2) barres
  S+/S/A/B et stress tests Portefeuille DÉJÀ conformes — vérifié
  navigateur : le pire scénario (TOP_SECTOR_MINUS_15, −15 %) porte
  la dominante (libellé rouge gras + halo) depuis le lot 131, la
  concentration sa mini-barre à repère (lot 138) ; (3) sparklines
  des tuiles KPI d'Aujourd'hui : AUCUN payload ne fournit de série
  par KPI → pas de sparkline inventée, constat honnête (reporté à
  une évolution moteur, jamais à une invention UI).
  → **TV-CHARTS-INVENTORY.md : 100 % des lignes traitées** (refaites,
  héritées ou constatées conformes/honnêtes). Décision fidèle aux
  règles : AUCUN bump SW (aucun changement de shell visible).
  Captures stress tests (dominante) + tuiles KPI + risque 1440
  envoyées, 0 erreur console. Suite 2461 passed / 2 skipped
  (inchangée — docs seulement).

- **Lot 203 — livré** : TOURNÉE TV — la volatilité et le
  positionnement Options. (1) CÔNE DE MOUVEMENT ATTENDU : les bandes
  1σ (brand) et 2σ (copper) sont une estimation lognormale
  (σ = spot·IV_ATM·√(DTE/365)) → remplissages HACHURÉS
  (C.hatchPattern lot 197 — la texture commune au cône de projection,
  au payoff et au théta), repli translucide propre si le helper est
  absent ; médiane, tooltips et légende inchangés. (2) GEX PAR
  STRIKE : les deux niveaux que le trader cherche — MUR CALL (max
  call GEX) et MUR PUT (max |put GEX|), calculés seulement s'il y a
  ≥ 2 strikes — deviennent les dominantes : barre pleine intensité
  (1 vs .55) + valeur RÉELLE en chip pleine couleur (texte sombre,
  borné au viewBox) au bout de la barre ; axe, strikes, spot
  pointillé et pied honnête inchangés. SW v166 → v167 + 5 gardiens.
  Captures cône hachuré (spot 180) + GEX ACN (chips « 15.59 M$ » /
  « −6.24 M$ ») + Volatilité 1440/390 envoyées, 0 erreur console.
  Suite 2461 passed / 2 skipped. Inventaire TV : vol cone ✔, GEX ✔.

- **Lot 202 — livré** : TOURNÉE TV — le PRICE-CHART d'Analyse.
  CONSTAT sur le canonique : le graphique principal est rendu par
  TradingView Lightweight Charts et ses niveaux du plan sont DÉJÀ des
  étiquettes natives de l'échelle de prix (TP1 206.37 vert, Entrée
  198.00, Résistance, Stop 189.63 rouge, dernier prix, volume —
  vérifié navigateur sur /analysis/ACN) : le langage TV d'origine.
  REPLI Chart.js ALIGNÉ : C.levelLines (chart-core) passe du texte
  plat à gauche aux CHIPS pleine couleur au BORD DROIT (texte sombre
  gras, anti-collision verticale par empilement quand deux niveaux se
  chevauchent, bornage à la zone de tracé) — l'échelle de repli
  (bougies invalides → priceCard) parle désormais la même langue que
  le canonique. Lignes pointillées et couleurs par kind inchangées ;
  gardiens lot 52/54 (C.levelLines/multiLine) toujours verts. Note
  honnête : le repli n'est pas capturable en démo (le canonique
  fonctionne) — preuve par le code + suite. SW v165 → v166 +
  5 gardiens. Capture chandeliers ACN + Analyse 1440/390 envoyées,
  0 erreur console. Suite 2461 passed / 2 skipped. Inventaire TV :
  price-chart ✔.

- **Lot 201 — livré** : TOURNÉE TV — le RADAR de scores (C.radar,
  scorecard de la fiche Analyse) reçoit la règle « dominante en
  évidence » : le sommet à la valeur MAXIMALE réelle porte un anneau
  de focus (couleur, opacité .55) et sa valeur en CHIP pleine couleur
  (tvEdgeChip, texte sombre) posé VERS LE CENTRE le long du rayon —
  jamais sur les libellés d'axes. Grille dégressive, remplissage
  radial, points et libellés inchangés ; chip = valeur réelle
  arrondie (« 100 » sur l'axe Risque d'ACN en démo). JAUGE
  ENVIRONNEMENT OPTIONS : ✔ par héritage STRUCTUREL — mountEnvGauge
  appelle VXCharts.gauge directement (chemin unique vers la jauge TV
  lot 189) ; en démo l'hôte n'est pas rendu (données environnement
  absentes → état honnête), héritage prouvé par le code. SW v164 →
  v165 + 5 gardiens. Capture radar ACN + Analyse 1440/390 envoyées,
  0 erreur console. Suite 2461 passed / 2 skipped. Inventaire TV :
  radar ✔, jauge env. options ✔.

- **Lot 200 — livré** : TOURNÉE TV — la SÉRIE DE RÉFÉRENCE de
  Marchés (120 séances, SPY ou proxy honnête) reçoit les chips
  Max/Min : passthrough `extremes` de C.areaCard vers C.area (opt-in
  — aucun autre appelant modifié) + activation sur la carte de
  référence — les bornes RÉELLES de la période (Max 443,69 /
  Min 351,41 en démo) se lisent sur la courbe avec la pilule de
  dernière valeur, comme sur TV. DISCIPLINE Journal : ✔ par HÉRITAGE
  STRUCTUREL — les barres du Journal/Performance appellent
  VXCharts.bars directement (3 sites) → elles ont reçu le lot 199
  (dominante liserée + chip) sans modification ; journal démo vide →
  états vides honnêtes, héritage prouvé par le chemin de code
  unique. SW v163 → v164 + 5 gardiens. Captures série de référence +
  Marchés 1440/390 + Journal envoyées, 0 erreur console.
  Suite 2461 passed / 2 skipped. Inventaire TV : aires de référence ✔,
  discipline ✔.

### MINI-BILAN tournée 196-200

5 lots, PR #229 → #233, suite stable 2461 passed / 2 skipped,
SW v159 → v164. La tranche a rendu TRANSVERSES les règles de la
grammaire TV : « dominante en évidence » appliquée à la staleness
Système (196 — tuile liserée + âge en chip du plus rassis), aux
barres partagées C.bars (199 — liseré + valeur en chip, hérité par
6 familles) ; texture « estimation » hachurée généralisée
(C.hatchPattern + option hatch de C.area, 197 — théta Options) ;
chips de valeur sur les pointeurs de rails (198 — VIX réel, « n/d »
honnête sur régime indéterminé) ; chips Max/Min sur les extrêmes
réels des aires (200 — série de référence Marchés). Deux ✔ par
HÉRITAGE constaté sans code : scénarios Options (197, via heatmap
194) et discipline Journal (200, via C.bars 199) — la grammaire
paye : chaque builder partagé aligné aligne ses pages gratuitement.
Honnêteté tenue partout (movers/journal vides rapportés, jamais de
dominante sur singleton). Reste à l'inventaire : price-chart
niveaux, radar, vol cone, GEX, double probabilité, sparklines KPI.

- **Lot 199 — livré** : TOURNÉE TV — les BARRES du builder partagé
  C.bars reçoivent la règle « dominante en évidence » : la barre au
  |valeur| max (calculée seulement s'il y a ≥ 2 barres — jamais une
  dominante sur singleton) porte un liseré appuyé (couleur pleine
  1.6 px vs alpha 80 / 1 px pour les autres) et sa VALEUR en chip
  pleine couleur (texte sombre — plugin canvas dans la grammaire
  tvEdgeChip, posé au bout de la barre, borné à la zone de tracé,
  vertical et horizontal gérés). Hérité par TOUS les appelants :
  sensibilité IV (Options), S+/S/A/B (Portefeuille), leadership
  (Marchés), discipline (Journal), movers (Système), recherche
  (Intelligence). Matière verre, survol, axes et formats inchangés ;
  la valeur du chip est la donnée RÉELLE formatée par le yFmt de
  l'appelant. Constat honnête : #vx-brain-movers ne se rend pas en
  démo (pas de mouvements) — rapporté sans agir. SW v162 → v163 +
  5 gardiens. Capture sensibilité IV GOOGL (chip rouge « −23.4 % »
  sur le choc −20 %, liseré appuyé) + Système 1440 + 390 envoyées,
  0 erreur console. Suite 2461 passed / 2 skipped. Inventaire TV :
  barres ✔ (sensibilité IV ✔ par héritage constaté).

- **Lot 198 — livré** : TOURNÉE TV — les RAILS de Marchés reçoivent
  le chip de valeur : nouvelle classe réutilisable
  .vx-rail-chipline/.vx-rail-chip (cockpit.css) — chip posé au-dessus
  du pointeur du rail, fond clair/texte sombre/gras 800/chiffres
  tabulaires (le même langage que le pointeur blanc des jauges lot
  189 et les chips de bord), positionné par --vx-rail-pos et BORNÉ
  aux extrémités (clamp) pour ne jamais déborder. Calme↔Stress : la
  valeur RÉELLE du VIX (12.7 en démo) à sa position sur l'échelle
  10→40 ; Défense↔Attaque : la confiance réelle du régime en %, et
  « n/d » HONNÊTE quand le régime est indéterminé — jamais un
  pourcentage inventé sur UNKNOWN. Dégradés des rails et flèches
  inchangés. SW v161 → v162 + 5 gardiens. Captures carte VIX (jauge +
  rail + chip 12.7) + rail positionnement (chip n/d) + 1440 + 390
  envoyées, 0 erreur console. Suite 2461 passed / 2 skipped.
  Inventaire TV : bandes linéaires ✔.

- **Lot 197 — livré** : TOURNÉE TV — le THÉTA Options assume sa
  texture de PROJECTION : nouveau C.hatchPattern (chart-core) =
  équivalent canvas du tvHatch (teinte .08 + rayures 45° .38),
  réutilisable par tous les builders Chart.js via la nouvelle option
  `hatch` de C.area (opt-in — défaut inchangé, aucun graphique
  modifié sans opt-in). option-theta : hatch + chip Min — la
  décroissance temps vient du scenario_pricer (un MODÈLE), l'aire est
  hachurée comme le payoff (192) et le cône (190), le chip Min marque
  le point le plus bas de la projection. SCÉNARIOS Options : ✔ par
  HÉRITAGE constaté (option-scenarios passe par C.heatmapCard → il a
  reçu le lot 194 sans modification — texte coloré par intensité,
  pire cellule −66 % en dominante, pied « estimation modèle, pas une
  promesse »). SW v160 → v161 + 5 gardiens. Captures théta hachuré
  (chip « Min 23,3 ») + matrice scénarios + 1440 + 390 envoyées,
  0 erreur console. Suite 2461 passed / 2 skipped. Inventaire TV :
  théta ✔, scénarios ✔. (Lot exécuté immédiatement sur ordre
  utilisateur — trigger annulé puis réarmé pour le 198.)

- **Lot 196 — livré** : TOURNÉE TV — FRAÎCHEUR PAR DOMAINE (Système,
  vue Données) : la règle « dominante en évidence » appliquée à la
  staleness — le domaine le PLUS RASSIS (âge max connu, calculé
  seulement s'il y a ≥ 2 âges connus, jamais un « pire » inventé sur
  un singleton) porte : tuile de la heatmap de fraîcheur au liseré
  appuyé (1.6 px) dans sa couleur d'état, et âge en CHIP pleine
  couleur (texte sombre, gras 800 — grammaire tvEdgeChip) à côté de
  sa barre dans la table. Les autres domaines restent adoucis ;
  domaine sans âge → ni barre ni chip (honnêteté du lot 142
  préservée). Âges/états strictement réels (/api/live/status), aucun
  seuil inventé. SW v159 → v160 + 5 gardiens. Capture : « companies »
  (20 952 min hors ligne) en chip rouge + tuile liserée, domaines à
  22 s adoucis — 1440 + 390 envoyées, 0 erreur console.
  Suite 2461 passed / 2 skipped. Inventaire TV : staleness ✔.

- **Lot 195 — livré** : TOURNÉE TV — ÉQUITÉ & DRAWDOWN (Portefeuille)
  avec chips Max/Min sur les extrêmes RÉELS : nouveau
  C.tvExtremesPlugin (chart-core) — chips canvas dans la grammaire
  tvEdgeChip (fond plein, texte sombre), Max au-dessus du point, Min
  en dessous, bornés à la zone de tracé ; opt-in `extremes` de
  C.area (true | 'max' | 'min') — AUCUN autre graphique modifié sans
  opt-in. equity-chart : Max + Min (les deux chiffres du drawdown se
  lisent sur la courbe) ; drawdown-chart : Min seul = le PIRE creux
  réel. Pilule de dernière valeur, glow, crosshair, arithmétique et
  états vides honnêtes intacts. Preuve : série d'exemple semée
  LOCALEMENT dans le navigateur de test (add_init_script, jamais
  commitée) — la page reste honnêtement vide sans clôtures
  déclarées. SW v158 → v159 + 5 gardiens. Captures chips
  « Max 11510 »/« Min 10040 » et « Min −4 % » + 1440 + 390 envoyées,
  0 erreur console. Suite 2461 passed / 2 skipped. Inventaire TV :
  equity ✔, drawdown ✔.

### MINI-BILAN tournée 191-195

5 lots, PR #224 → #228, suite stable 2461 passed / 2 skipped,
SW v154 → v159. Tranche entièrement consacrée à la TOURNÉE GRAPHIQUE
TV (directive utilisateur du lot 188) : 9 signatures livrées —
barres de consensus du comité (191, style « Note des analystes »),
regimeAura aligné + payoff hachuré GAIN/PERTE (192), catalystRunway
en piste dégradée hachurée à chip J-x (193), heatmap à texte
d'intensité + cellule dominante et treemap à chips de part (194,
builders partagés → héritage large), équité/drawdown à chips
Max/Min sur extrêmes réels (195, opt-in). Un CORRECTIF STRUCTUREL
au passage : __VXVOCAB injecté par le shell de la refonte (191) —
libellés FR sur toutes les pages, gardien anti-XSS respecté.
Doctrine tenue : dégradés fondus, hachures = estimation, chips de
bord = chiffres clés, dominante en évidence ; données RÉELLES
uniquement (les constats démo — prime aberrante, tuiles sans P&L —
sont rendus honnêtement et RAPPORTÉS sans agir). Reste à l'inventaire :
sparklines KPI, aires indices, barres leadership, price-chart,
radar, vol cone, barres S+/S/A/B, GEX/scénarios/théta/IV options,
discipline Journal, staleness Système.

- **Lot 194 — livré** : TOURNÉE TV — la HEATMAP alignée (builder
  partagé C.heatmapCard — hérité par secteurs Marchés, P&L mensuel
  Portefeuille, scénarios/IV Options) : (1) le texte de chaque
  cellule porte la COULEUR de son intensité (alpha fondu .45 → 1 sur
  |t|, gras 700) — la grille se lit sans regarder les fonds, comme
  les cartes secteurs TV ; (2) la cellule DOMINANTE de TOUTE la
  grille (|t| max, une seule) en évidence — liseré appuyé 1.6 px +
  gras 800, les autres adoucies (même langage que la barre dominante
  du consensus lot 191). TREEMAP (chart-core) : la part « x % » des
  grandes tuiles passe du texte translucide au chip tvEdgeChip
  pleine couleur de la tuile (texte sombre) — grammaire des chips de
  bord. Tuiles verre, cellules nulles et navigation inchangées.
  Constat démo honnête : tuiles treemap neutres (P&L absent — la
  couleur ne s'invente pas). SW v157 → v158 + 5 gardiens. Captures
  heatmap secteurs (+1,28 % vert / −1,58 % rouge, dominante liserée)
  + treemap (chips 65 %/35 %) + 1440 + 390 envoyées, 0 erreur
  console. Suite 2461 passed / 2 skipped. Inventaire TV : heatmap ✔,
  treemap ✔.

- **Lot 193 — livré** : TOURNÉE TV — catalystRunway (Aujourd'hui)
  aligné sur la grammaire : (1) piste DTE en dégradé CONTINU
  (imminence rouge → jaune ancré à la frontière ≤ 5 j réelle →
  horizon éteint — le risque temporel est dans la matière de la
  piste) ; (2) zone ≤ 5 j HACHURÉE (tvHatch — la texture
  estimation/risque commune au cône lot 190 et au payoff lot 192) ;
  (3) le PROCHAIN catalyseur porte son échéance en chip tvEdgeChip
  pleine couleur d'impact (texte sombre), les suivants en texte.
  Anti-collision lot 61, anneau de focus, verdict tonal et état vide
  honnête STRICTEMENT inchangés ; helpers TV gardés par test
  d'existence. SW v156 → v157 + 5 gardiens. Capture piste (chip J-0
  rouge Emploi US, J-3/J-5/J-6/J-7) + 1440 + 390 envoyées, 0 erreur
  console. Suite 2461 passed / 2 skipped. Inventaire TV : runway ✔.

- **Lot 192 — livré** : TOURNÉE TV — deux graphiques alignés. (1)
  regimeAura (Aujourd'hui) rejoint la grammaire TV : l'arc de
  confiance ENTIER en dégradé continu de la tonalité du régime
  (fondu .18 → .95), POINTEUR blanc court posé sur l'arc à la
  position de la confiance (même langage que l'aiguille C.gauge du
  lot 189), « x % confiance » en évidence colorée gras 800 — halo,
  chips de grammaire et verdict inchangés, état honnête intact
  (sans régime → vide). (2) PAYOFF Options hachuré : _hatch(color) =
  équivalent CANVAS du tvHatch SVG (teinte .08 + rayures 45° .38),
  zones gain/perte du payoff en motifs hachurés (le payoff à
  l'échéance est une ESTIMATION) + libellés « GAIN »/« PERTE » de
  part et d'autre du breakeven selon C/P — arithmétique du contrat
  STRICTEMENT inchangée, contrat incomplet → vide honnête. Constat
  démo rapporté sans agir : prime GOOGL aberrante (3812) → P&L
  ≈ −100 % partout, rendu honnête des chiffres fournis. SW v155 →
  v156 + 5 gardiens. Captures Aujourd'hui 1440+390 + carte aura +
  carte payoff envoyées, 0 erreur console.
  Suite 2461 passed / 2 skipped. Inventaire TV : aura ✔, payoff ✔.

- **Lot 191 — livré** : TOURNÉE TV — les BARRES DE CONSENSUS du
  comité (charts/consensus-bars.js, nouveau builder
  VXCharts.consensusBars) — le « Note des analystes » TradingView
  nourri par les comptes RÉELS des verdicts du comité : libellé à
  gauche, barre pleine à bout arrondi proportionnelle au max, compte
  à droite ; la barre DOMINANTE en pleine intensité et gras 800, les
  autres adoucies (.45) ; total honnête en pied (« N dossiers passés
  en revue — comptes réels ») ; vide → état vide honnête. CORRECTIF
  STRUCTUREL découvert par la 1re capture : __VXVOCAB n'était injecté
  que par l'ancien pipeline mort → désormais injecté par le SHELL de
  la refonte (`<script id="vx-vocab">` — l'id satisfait le gardien
  anti-XSS du lot 43), libellés FR (« Éviter », « Surveiller la
  cassure », « Attendre ») disponibles sur TOUTES les pages. Branché
  vue Comité d'Intelligence (remplace le tally ad hoc). SW v154 →
  v155 + 5 gardiens. Captures /intelligence?view=committee 1440+390
  + carte cadrée envoyées, 0 erreur console.
  Suite 2461 passed / 2 skipped. Inventaire TV : consensus ✔.

- **Lot 190 — livré** : TOURNÉE TV — le CÔNE DE PROJECTION
  (charts/projection-cone.js, nouveau builder VXCharts.projectionCone)
  — la signature « prix cible » TradingView nourrie par les niveaux
  RÉELS du plan moteur : trait blanc des clôtures réelles → point
  actuel, éventail HAUSSIER hachuré (tvHatch) entre TP1 et TP3 avec
  médiane pointillée TP2, faisceau de RISQUE vers le stop, frontière
  « PROJECTION — plan moteur », chips de bord tvEdgeChip (TP3 +x %,
  TP2, TP1, Actuel, Stop −x % — pourcentages CALCULÉS). Sans plan
  complet → état vide honnête ; pied « une carte de risque, pas une
  prévision de marché ». Branché en tête de la carte « Plan &
  niveaux clés » de la fiche Analyse. Marge chips ajustée après la
  1re capture. SW v153 → v154 + gardiens. Captures /analysis/ACN
  1440+390 + carte cadrée envoyées, 0 erreur console.
  Suite 2461 passed / 2 skipped. Inventaire TV : cône ✔.

### MINI-BILAN tournée 186-190

5 lots, PR #219 → #223, suite 2450 → 2461 passed, SW v152 → v154.
Bascule en cours de tranche : après les gardiens transverses (186 :
31 fichiers JS src= node --check + ≥40 assets 0 lien mort + 0
externe ; 188 : 54 endpoints d'API fetchés 0 mort) et un DÉFAUT RÉEL
corrigé (187 : le design-system affichait des hex périmés → hex
DÉRIVÉS de tokens.css, la double source a disparu), la DIRECTIVE
UTILISATEUR a ouvert la TOURNÉE GRAPHIQUE TV (« que tout Vertex
ressemble à ça — fluide, beau, parfait ») : fondation livrée (189 —
inventaire complet, grammaire tvHatch/tvEdgeChip, JAUGE TV à arc
dégradé continu et pointeur blanc héritée par 6 appelants) puis la
première grande signature (190 — le cône de projection du plan sur
la fiche Analyse). Doctrine tenue : données RÉELLES uniquement (pas
de plan → vide honnête, jamais un consensus inventé), tokens
uniquement (les gardiens couleur ont refusé 2 fallbacks — corrigés),
captures envoyées à chaque lot. Suite de l'inventaire : consensus
comité, regimeAura, payoff hachuré, treemap, equity/drawdown,
heatmap, GEX.

- **Lot 189 — livré** : TOURNÉE GRAPHIQUE TV — FONDATION (directive
  confirmée par l'utilisateur en cours de lot : « que tout Vertex
  ressemble à ça — fluide, beau, parfait »). Inventaire complet des
  graphiques vivants (TV-CHARTS-INVENTORY.md, statuts + plan des
  lots), grammaire TV dans chart-core (tvHatch « estimation »,
  tvEdgeChip d'étiquette de bord) et PREMIÈRE SIGNATURE refaite : la
  JAUGE passe au style TradingView — arc entier en dégradé CONTINU
  (couleurs des bandes fondues, rouge→jaune→vert), pointeur blanc
  court posé sur l'arc (ajusté après 1re capture pour ne jamais
  couvrir le texte), état coloré en évidence sous l'arc. API 100 %
  compatible : les 6 appelants (Marchés ×3, Portefeuille, Système,
  Intelligence, options-intel) héritent sans changement. Les
  gardiens couleur ont refusé 2 fallbacks hors inventaire →
  conformes (#121214). Captures Breadth/Volatilité 1440+390
  envoyées, 0 erreur console. SW v152 → v153 + gardiens.
  Suite 2461 passed / 2 skipped.
- **Lot 188 — livré** : gardien des LIENS D'API des pages vivantes
  (54 endpoints fetchés par les 11 pages servies — 0 mort, motifs
  paramétrés gérés) + invariants d'intelligence_page (662 l, la
  moins gardée) : 6 vues 200 avec UN SEUL onglet actif le bon, vue
  inconnue → défaut jamais cassée, 0 id dupliqué, ≥ 12 VX.states,
  page saine. 5 tests. Suite 2456 → 2461 passed / 2 skipped.

## ⚡ DIRECTIVE UTILISATEUR ACTIVE (reçue au lot 188) — TOURNÉE GRAPHIQUE TV

L'utilisateur (captures TradingView SKHY à l'appui) demande la
REFONTE DE TOUS LES GRAPHIQUES de Vertex, lot par lot, un par un,
dans le langage visuel TradingView : jauges semi-circulaires
DÉGRADÉES à aiguille (Strong sell → Strong buy), cône de projection
prix cible min/moy/max en éventail, barres de consensus analystes,
zones d'ESTIMATION hachurées sur les barres de prévision, doubles
axes annotés, tableaux réels vs estimations — « moderne, équilibré,
voyant, beau, structuré au mieux ». Chaque graphique, chaque widget.
Protocole par lot : grammaire commune d'abord (chart-core), puis 1-2
builders refaits par lot AVEC serveur DEMO + captures navigateur +
SendUserFile + SW bump + gardiens. Données RÉELLES uniquement
(absent → n/d), tokens seulement, aucun littéral couleur nouveau.

- **Lot 187 — livré** : DÉFAUT RÉEL CORRIGÉ sur la page de référence
  /design-system (254 l, zéro test dédié) — elle affichait des hex
  PÉRIMÉS recopiés à la main : 10+ étiquettes divergeaient de
  tokens.css (--vx-black affiché #020202, réel #060405 ; les tokens
  devenus alias var() montraient l'ancienne valeur). Correctif
  STRUCTUREL minimal : les hex sont désormais DÉRIVÉS de tokens.css
  à l'import (alias résolus) — la double source a disparu, la page
  LIT la vérité et ne peut plus mentir. 6 tests : preuve rouge/vert
  (≥ 30 swatches, 0 divergence), variables toutes existantes (un
  renommage CSS fait échouer la référence), alias montrés résolus,
  ids uniques + littéraux interdits absents + data-ds-copy ≥ 20 +
  état vide au libellé produit exact. SW v151 → v152 (changement
  visible) + 4 gardiens de version mis à jour. Moteurs intacts.
  Suite 2450 → 2456 passed / 2 skipped.
- **Lot 186 — livré** : GARDIEN DES JS STATIQUES et des liens
  d'assets (extension du lot 182 : le sweep couvrait l'inline, pas
  les fichiers src=). 5 tests figent : les 31 fichiers JS du
  produit (chart-core, regime-aura, catalyst-runway, vx-shell…)
  parsent TOUS par node --check (seul exclu documenté : la
  bibliothèque tierce minifiée vendor) ; les ≥ 40 assets référencés
  par les 13 routes servies résolvent TOUS en 200 — aucun lien
  mort ; AUCUN asset http(s) externe (l'autonomie hors-ligne des
  lots 81-85 est désormais gardée en continu) ; chaque builder
  charts s'enregistre sur VXCharts (exception documentée : le thème
  → VXChartTheme, miroir de palette.py déjà gardé). Constat : état
  présent sain — 0 invalide, 0 lien mort, 0 externe. Aucun code
  modifié, pas de bump SW. Suite 2445 → 2450 passed / 2 skipped.
- **Lot 185 — livré** : cartographie de mort, volet FONCTIONS
  (clôture 183-185, rien supprimé). Méthode PRUDENTE (un doute =
  vivant ; racines = décorées, référencées au module, vues actives,
  références externes) : 29 des 91 fonctions top-niveau de
  terminal.py sont mortes — 62 lignes seulement, QUE des stubs de
  vues legacy (≤ 4 lignes : return PAGE_* morte, redirection ou
  render migré) + _rail + _legacy_pages_redirect ; AUCUNE logique
  métier morte. Les 9 boucles de fond sont CLASSÉES VIVANTES (garde
  anti-faux-positif testée). 5 tests figent l'inventaire, la garde,
  la nature des stubs, le recoupement endpoints et le poids chiffré.
  Aucun code modifié, pas de bump SW.
  Suite 2440 → 2445 passed / 2 skipped.

### MINI-BILAN tournée 181-185 — « UI vivante + cartographie de mort »

5 lots, PR #214 → #218, suite 2416 → 2445 passed (+29 tests), SW
stable v151 (tournée tests pure). Deux fils : (1) les couches UI
VIVANTES gardées — home_art caractérisée (injection, progressive
enhancement, VIX narratif) et la règle critique n°2 SYSTÉMATISÉE
(chaque bloc <script> inline de chaque page servie passe au vrai
parseur node --check, garde anti-vide) ; (2) la CARTOGRAPHIE DE MORT
de terminal.py, prudente et prouvée (AST + introspection Flask +
recoupement empirique) : 25 pages (~2 265 l) + 35 couches JS/CSS +
29 fonctions stubs (62 l) + 2 helpers — morts, orphelins,
inventaires EXACTS figés par tests (ressusciter ou supprimer =
décision explicite), aucun vieux lien utilisateur ne tombe dans le
vide (39 redirections vérifiées). AUCUNE logique métier morte — le
poids mort est du HTML/JS d'anciennes pages. DÉCISION HUMAINE EN
ATTENTE : autoriser le lot de purge (≈ 25-30 % du monolithe) ?

- **Lot 184 — livré** : vie/mort des COUCHES JS/CSS du monolithe
  (extension du lot 183, rien supprimé). Par AST + recoupement
  empirique : les 35 chaînes _*_JS/_*_CSS de terminal.py ne
  nourrissent QUE les 25 pages mortes — chaque assignation qui les
  consomme vise une PAGE_* morte ou une autre couche ; _vpage (20
  appels module-niveau, tous vers des pages mortes) et _rail (défini
  mais appelé NULLE PART — helper mort) sont les seuls à les
  toucher ; les marqueurs signés (hmHost, artBoard) sont absents des
  11 pages réellement servies. 5 tests figent l'inventaire exact et
  ces preuves. Bilan cumulé du poids mort de terminal.py : 25 pages
  + 35 couches + 2 helpers (~2 265+ lignes) — purge = décision
  humaine (question ouverte depuis le lot 183). Aucun code modifié,
  pas de bump SW. Suite 2435 → 2440 passed / 2 skipped.
- **Lot 183 — livré** : VÉRIFICATION DE VIE des pages legacy de
  terminal.py — CONSTAT STRUCTUREL documenté, rien supprimé : par
  introspection des vues Flask ACTIVES, les 25 blobs PAGE_*
  (~2 265 lignes de HTML/JS) ne sont plus servis par AUCUNE route —
  la refonte (vertex/ui/pages + redesign) a tout repris, les 39
  anciennes URLs redirigent vers les 8 espaces canoniques, et aucun
  module n'importe terminal.PAGE_* (mortes ET orphelines). 5 tests
  figent : l'inventaire EXACT des 25 mortes (ressusciter ou
  supprimer = mise à jour explicite de l'inventaire) ; l'orphelinat
  prouvé ; les 39 redirections vers leur cible exacte ; les
  destinations = les 8 espaces canoniques, toutes 200 (aucun vieux
  lien ne tombe dans le vide) ; aucune chaîne de redirections.
  QUESTION OUVERTE à l'utilisateur : autoriser un futur lot de
  PURGE de ces ~2 265 lignes mortes ? Aucun code modifié, pas de
  bump SW. Suite 2430 → 2435 passed / 2 skipped.
- **Lot 182 — livré** : GARDIEN GLOBAL DE SYNTAXE JS — la règle
  critique n°2 (« tout JS généré depuis Python doit être valide —
  deux SyntaxError silencieuses ont déjà vécu ») SYSTÉMATISÉE
  (survey honnête : tracking_page/vault/sync_center ont leurs
  gardiens de contenu, la lacune était transverse). 6 tests : les
  16 routes HTML canoniques répondent toutes 200 et CHAQUE bloc
  <script> inline de chaque page est validé par node --check —
  0 erreur tolérée (une apostrophe française non échappée fait
  désormais échouer la suite) ; garde anti-vide (≥ 12 blocs
  réellement contrôlés — le gardien ne peut pas passer en tournant
  à vide) ; sync_center.JS et le _HEATMAP_JS du vault validés AVANT
  injection ; l'extracteur lui-même testé unitairement (src/json
  ignorés, inline gardé). Constat : tout l'état présent parse — le
  gardien empêche la régression. Aucun code modifié, pas de bump
  SW. Suite 2424 → 2430 passed / 2 skipped.
- **Lot 181 — livré** : caractérisation de la COUCHE ARTISTIQUE de
  l'accueil `vertex/ui/home_art.py` (171 lignes, ZÉRO test —
  VIVANTE : appliquée sur PAGE_DAILY et PAGE_STRATEGIE ; survey
  honnête : ibkr_scheduler/source_router couverts par 22 tests,
  quant_engine par 17, swing/events aussi). 8 tests figent :
  l'injection pure (apply() → <style>+<script> UNE fois avant
  </body>, sans </body> → no-op silencieux ; apply_desk() → CSS
  SEUL) ; la syntaxe JS RÉELLE validée par node --check (règle
  critique n°2 — deux SyntaxError silencieuses ont déjà vécu, un
  vrai parseur garde désormais cette couche) ; le progressive
  enhancement (catch → tout visible, arrêt propre sans #ovMarket,
  reduced-motion dans les deux CSS) ; le contrat de données
  (fetch /api/market/summary, rafraîchi 90 s SEULEMENT onglet
  visible, chiffres fr-FR, bandes narratives VIX ≤14/≥22 distinctes
  des bandes de données 16/22 du lot 153, VIX absent → tiret
  honnête) ; le câblage réel prouvé (artBoard dans PAGE_DAILY,
  DESK_CSS dans PAGE_STRATEGIE qui reste sans script). Aucun code
  modifié, pas de bump SW. Suite 2416 → 2424 passed / 2 skipped.
- **Lot 180 — livré** : caractérisation des DONNÉES ANALYSTES
  PROFONDES `vertex/data_sources/analyst_deep.py` (226 lignes, ZÉRO
  test, servi par la fiche titre — scheduler/live_stream déjà
  couverts lots 109/99, traces/logging dormants sans appelant :
  écartés à dessein). 10 tests HORS LIGNE (faux ticker pandas, faux
  yfinance injecté dans sys.modules, cache isolé) figent : le NaN
  écarté (jamais un chiffre fantôme) ; les révisions BPA (net30 +
  tendance, repli '0y' → '0q') ; les surprises (le trimestre À VENIR
  séparé en `next`, beats 2/3 + moyenne 5.6 exacte) ; les notes
  d'analystes (récentes d'abord, cap 6, firm bornée 40) ; les
  initiés (solde + biais, non classable → None) ; et la politique de
  cache — cache FRAIS servi sans AUCUN appel réseau (faux yfinance
  qui explose si touché : prouvé), yfinance mort → le cache PÉRIMÉ
  servi plutôt que rien, échec TOTAL jamais persisté. Aucun code
  modifié, pas de bump SW. Suite 2406 → 2416 passed / 2 skipped.

### MINI-BILAN tournée 176-180 — « surfaces de sécurité »

5 lots, PR #209 → #213, suite 2375 → 2416 passed (+41 tests), SW
stable v151 (tournée tests pure). Après la clôture des routes
(lot 176 : funnel fail-honest, copilot jamais une 500, live
parsing), la tranche a durci les surfaces de sécurité : le gardien
XSS DE BOUT EN BOUT (lot 177 — payload injecté dans les états,
neutralisé à CHAQUE sortie HTTP, + gardien statique ≥ 6 sites
sanitize_news) ; le filet du desk (lot 178 — snapshot quotidien
jamais réécrit, rotation 7, restore anti-traversal, ts neuf qui
gagne le LWW) ; l'observabilité bornée en mémoire (lot 179 —
percentiles exacts, anneau 200, timer qui propage) ; et les données
analystes (lot 180 — périmé plutôt que rien, échec jamais caché,
zéro réseau prouvé). Constats honnêtes en série : auth.py (15
tests), webhook TradingView (12), config (secrets jamais renvoyés,
lot 111), startup (lot 105), client-log (lot 94) étaient DÉJÀ
blindés — les surfaces de sécurité du produit sont désormais toutes
gardées par des tests. Prochaine direction au survey du lot 181.

- **Lot 179 — livré** : caractérisation de l'OBSERVABILITÉ du
  Strategy OS (§37) — `vertex/observability/metrics.py` (ZÉRO test
  direct) et les sections de `diagnostics.py` (le webhook TradingView,
  candidat prévu, s'est révélé complet avec 12 tests — constat
  honnête, repli sur la vraie lacune). 9 tests figent : les
  compteurs qui CUMULENT vs les jauges qui ÉCRASENT ; les
  percentiles EXACTS (100 mesures 1..100 → p50 51.0/p95 95.0/max
  100.0, échantillon unique → confondus) ; l'anneau de 200 mesures
  (250 envoyées → fenêtre 51..250, p50 151.0 — bornage mémoire) ;
  le timer contextuel qui mesure ET propage l'exception (jamais
  avalée, durée enregistrée quand même) ; le snapshot COPIE isolée ;
  les sections de system_diagnostics STRICTEMENT optionnelles (sans
  dépendance → {metrics} seul, rien d'inventé) ; data_quality_report
  qui compte TOUS les paquets mais borne les dégradés à 20 et les
  warnings à 3. Aucun code modifié, pas de bump SW.
  Suite 2397 → 2406 passed / 2 skipped.
- **Lot 178 — livré** : FILET DE SÉCURITÉ DU DESK — backup quotidien
  + /api/desk/restore de `desk.py` (règle critique n°6 ; le candidat
  auth.py s'est révélé déjà très couvert — 15 tests force-brute/
  open-redirect — constat honnête, repli sur la vraie lacune).
  8 tests figent : le snapshot quotidien créé au PREMIER écrasement
  du jour avec le contenu d'AVANT le push, jamais réécrit par les
  pushs suivants (le snapshot du matin protège la journée), rotation
  à 7 (les plus vieux purgés) ; le restore qui refuse TOUT nom hors
  motif strict (../../etc/passwd, date incomplète, suffixe — le
  path traversal est impossible), introuvable → 404, illisible →
  500 SANS toucher le desk courant, réussi → données du snapshot
  avec un ts DE MAINTENANT (gagne le last-writer-wins sur tous les
  appareils) ; la liste triée du plus récent au plus ancien. Aucun
  code modifié, pas de bump SW. Suite 2389 → 2397 passed /
  2 skipped.
- **Lot 177 — livré** : GARDIEN XSS DE BOUT EN BOUT (règle critique
  n°5 : « tout texte externe passe par sanitize_news avant d'être
  servi »). Le lot 102 figeait la FONCTION ; rien ne prouvait que
  chaque ROUTE applique l'assainissement. 6 tests injectent un
  payload malveillant (script, img onerror, lien javascript:) dans
  les états partagés et vérifient chaque point de sortie :
  /news-feed sert le titre SANS balise avec quotes échappées, la
  traduction vidée, le lien javascript: supprimé et le lien https
  %-encodé (sûr en href ET window.open) ; le filtre serveur ?sym=
  ne contourne PAS l'assainissement ; /api/events/<sym> et
  /api/skyler/<sym> ne servent JAMAIS le payload brut (le texte
  survit neutralisé à travers evidence/events) ; un gardien
  statique compte les sites d'appel sanitize_news( en production
  (≥ 6 — content, analysis_api ×2, skyler_sweep, terminal ×2) :
  retirer un assainissement fait échouer la suite. Aucun code
  modifié, pas de bump SW. Suite 2383 → 2389 passed / 2 skipped.
- **Lot 176 — livré** : CLÔTURE de la tournée « honnêteté des
  routes » — les trois lacunes minces restantes en un lot
  (opportunities_api, ai_api /api/copilot/ask POST, live_api).
  8 tests figent : les 7 étages EXACTS de l'entonnoir (universe →
  … → positions) et son chemin d'erreur fail-honest (moteur en
  panne → 500 avec structure VIDE + erreur nommée, jamais un
  entonnoir à moitié inventé) ; le copilote qui n'explose JAMAIS
  (body vide OU JSON corrompu → 200 ok False « question vide ») et
  son repli sans clé DOUBLEMENT étiqueté (le label ET l'étiquette
  dans la réponse elle-même — le contenu varie selon le scan,
  l'étiquette jamais) ; le contrat du rapport live {lines,
  requested, ts}, le parsing des domaines (espaces/vides purgés,
  ordre gardé), le domaine inconnu → rien relancé mais demande
  tracée ; aucun verbe d'ordre dans les 3 modules. Leçon encodée :
  figer les INVARIANTS stables (parsing, étiquettes), pas les états
  transitoires (kicked dépend de l'état du moteur). Aucun code
  modifié, pas de bump SW. Suite 2375 → 2383 passed / 2 skipped.
- **Lot 175 — livré** : honnêteté HTTP de la SESSION D'ANALYSE
  `vertex/app/routes/session_api.py` (la logique de RESTAURATION de
  /api/session/digest était la lacune — moteur digest et manifest
  déjà couverts). 8 tests figent : le démarrage à froid → 'analyzing'
  servi tel quel ; le digest prêt → servi, mémorisé ET persisté ;
  l'écriture disque THROTTLÉE (2 appels < 30 s → 1 écriture) ; le
  scan retombé « pas prêt » → instantané 'restored' avec l'as_of
  absolu conservé mais l'ÂGE EFFACÉ (jamais un âge faussement
  frais) ; la restauration sert une COPIE (le mémo reste 'ready') ;
  session_id_for refuse bool et chaîne ; la couverture plafonnée à
  100 % sur univers périmé (600/517 → 100, jamais 116) ; aucun
  verbe d'ordre. Aucun code modifié, pas de bump SW.
  Suite 2367 → 2375 passed / 2 skipped.

### MINI-BILAN tournée 171-175 — « honnêteté des routes »

5 lots, PR #204 → #208, suite 2338 → 2375 passed (+47 tests, dont
les 10 du lot 171 déjà comptés dans 2338 : tranche réelle 2328 →
2375), SW stable v151 (tournée tests pure). La NOUVELLE DIRECTION
ouverte au lot 171 a figé la couche HTTP des routes les plus
sensibles — les moteurs étaient couverts, le câblage ne l'était
pas : positions_api (desk vide/corrompu honnête, IBKR hors ligne ne
clôture JAMAIS, introuvable → 200 + erreur documenté) ·
decision_api (params corrompus avalés, seuils -20/-25 % intacts par
HTTP, pas de covered call sans actions) · tracking_api (DATA_REQUIRED
sans prix inventé, étiquette HYPOTHÉTIQUE imposée, stop gèle,
restart n'écrase pas) · planning_api (le ticket d'ordre COMMENCE
par le disclaimer READONLY, stop « non transmis », la concentration
bloque même à budget correct) · session_api (instantané restauré à
l'âge EFFACÉ, throttle disque). Fil rouge prouvé partout : état
vide → réponse honnête, entrée corrompue → jamais un crash, donnée
absente → jamais inventée, AUCUN verbe d'ordre dans aucun module de
routes. Reste mince : opportunities funnel, copilot/ask POST,
live report — à balayer ou clore au lot 176.

- **Lot 174 — livré** : honnêteté HTTP du TICKET DE PRÉPARATION
  D'ORDRE `vertex/app/routes/planning_api.py` (/api/planning/ticket
  — la route la plus sensible au READONLY : elle prépare un texte à
  COPIER dans IBKR sans jamais transmettre) et de la RECHERCHE
  /api/search de feeds.py. 10 tests figent : sans symbole → 400 ;
  le plan du scan repris tel quel avec dimensionnement EXACT
  (100 k × 1 % = 1 000, risque unitaire 5 → 200 actions, rr 3.0
  transmis) ; la CONCENTRATION qui bloque même avec un budget de
  risque correct (poids projeté 20 % > 15 % → blocked + blocker
  explicite) ; le body qui prime sur le plan du scan ; les refus
  honnêtes (sans compte → sizing None sans blocage, stop au-dessus
  de l'entrée → « risque non défini », option sans prime → « prime
  indisponible ») ; l'option dimensionnée sur la prime (250 par
  contrat → 4) ; l'INVARIANT PRODUIT : chaque copy_text COMMENCE
  par « PRÉPARATION UNIQUEMENT — Vertex est en lecture seule et ne
  transmet aucun ordre » et le stop y est « (référence, non
  transmis) » ; la recherche (vide → [], insensible à la casse,
  plafond dur 20). Aucun code modifié, pas de bump SW.
  Suite 2357 → 2367 passed / 2 skipped.
- **Lot 173 — livré** : honnêteté HTTP du moteur de SUIVI
  `vertex/app/routes/tracking_api.py` (le cycle de vie
  /api/tracking/<id>, /performance, /stop, /restart, /history était
  à ZÉRO test — seuls la liste et la création étaient couverts).
  10 tests figent : les refus explicites (404 « suivi introuvable »
  sur les 5 sous-routes, 400 « symbol requis ») ; la création
  honnête (action inconnue du scan → 201 mais DATA_REQUIRED avec
  reference_price None — JAMAIS un prix inventé ; action cotée →
  référence LAST/« scan » tracée, benchmark SPY, is_hypothetical
  True ; option → MID exact du body) ; la performance au prix
  courant RÉEL du scan avec l'étiquette IMPOSÉE « Suivi
  HYPOTHÉTIQUE : aucune position réelle… », l'option exigeant son
  mark en paramètre (sans mark → None, jamais un chiffre sans
  source) ; le stop qui GÈLE le résultat (final_price/return/MFE/MAE
  exacts) ; le restart à identifiant NEUF laissant l'ancien suivi
  gelé ; aucun verbe d'ordre. Aucun code modifié, pas de bump SW.
  Suite 2347 → 2357 passed / 2 skipped.
- **Lot 172 — livré** : honnêteté HTTP des DÉCISIONS DE POSITION
  `vertex/app/routes/decision_api.py` (deux endpoints à ZÉRO test :
  /api/position-decision/<sym> et /api/options-for/<sym> — les
  moteurs servis sont couverts par le lot 87, la lacune était le
  câblage HTTP). 9 tests figent : le symbole inconnu → HOLD avec
  sous-jacent étiqueté DATA_INSUFFICIENT (jamais inventé) ; le stop
  touché via query params → EXIT 78 ; les paramètres corrompus
  (entry=abc, dte=) avalés en None — JAMAIS un crash ; les seuils de
  discipline traversant la couche HTTP intacts (action -20 % EXIT,
  option -20 % HOLD, -25 % EXIT) ; le thêta qui commande à ≤14 j ;
  le board vide → note explicite sans contrat inventé ; les 5 rôles
  exacts pour une position action (CALL/PUT/LEAPS/COVERED_CALL/
  PROTECTIVE_PUT) réduits à 3 pour une option détenue (pas de call
  couvert sans actions) ; jamais un contrat d'un autre titre ; aucun
  verbe d'ordre. Aucun code modifié, pas de bump SW.
  Suite 2338 → 2347 passed / 2 skipped.
- **Lot 171 — livré** : NOUVELLE DIRECTION « honnêteté des routes » —
  caractérisation de la couche HTTP Position Intelligence
  `vertex/app/routes/positions_api.py` (249 lignes ; survey préalable :
  options/ et research/ déjà couverts, mais 4 endpoints à ZÉRO test —
  /api/positions/state, /report, /audit, /reconcile — alors que les
  moteurs sous-jacents ont 41 tests directs). 10 tests figent : le
  desk vide → live False DIT, P&L/delta/theta None (jamais un 0
  inventé) ; la position réelle recalculée au prix RÉEL du scan
  ((200−150)×10 = 500), cible dépassée → action DESCRIPTIVE
  « SÉCURISER » mais décision ATTENDRE (Vertex n'exécute jamais) ;
  IBKR hors ligne → « aucune clôture automatique », 0 réparation ;
  desk corrompu → 200 + vide honnête (state ET stress) ; introuvable
  → HTTP 200 + erreur explicite DOCUMENTÉ tel quel (pas 404) ; le
  diff « ce qui a changé » (baseline puis +5 % → MAJOR, snapshot
  persisté) ; aucun verbe d'ordre dans la source. Aucun code modifié,
  pas de bump SW. Suite 2328 → 2338 passed / 2 skipped.
- **Lot 170 — livré** : caractérisation de l'UNIVERS
  `data/universe.py` (324 lignes — données pures : l'univers scanné,
  la watchlist, les cartographies GICS/industrie ; DERNIER module de
  la file du périmètre ai/data/strategy/portfolio). 9 tests figent
  les INVARIANTS DE COHÉRENCE : univers dédupliqué ≥ 400 tickers,
  LIVE_SYMBOLS == UNIVERSE == INDEX_MEMBERS['union'] (une seule
  vérité), INDEX_SOURCE ∈ {live, cache, cache-stale, static} ;
  normalisation yfinance (AUCUN point dans l'univers US ni la
  watchlist — BRK-B ; les suffixes de place vivent exclusivement
  dans _EUROPE/_ASIA, toutes suffixées) ; _GICS exactement 11
  secteurs miroir des 11 ETF ; AUCUN ticker dans deux secteurs ni
  deux industries, aplatis couvrant exactement les déclarés ;
  watchlist 57 sans doublon ; TREND_SET == set(_TREND_EXTRA).
  Aucun code modifié, pas de bump SW.
  Suite 2319 → 2328 passed / 2 skipped.

### MINI-BILAN tournée 166-170

5 lots, PR #199 → #203, suite 2271 → 2328 passed (+57 tests), SW
stable v151 (tournée tests pure). Couverts : la couche IA optionnelle
(briefs — dégradation IA → Google → texte d'origine, jamais un texte
perdu, clé réelle exigée) ; le copilote d'analyse (chemin Claude
mocké, réponse étiquetée « estimation, pas une donnée broker »,
contexte mort → erreur honnête) ; la stratégie options personnalisée
legacy_adapter (VIVANTE — PUT imposé en régime dangereux, sorties
±50 %, portefeuille à arithmétique fermée) ; le profil d'entreprise
(segments curés sommant 100 %, schéma _v force le re-fetch, « jamais
de page vide ») ; et l'univers (une seule vérité par ticker, une
seule liste servie au live). La file du périmètre est ÉPUISÉE : tous
les modules de vertex/engines, market, quant, services, ai, data,
strategy et portfolio ont désormais des tests directs — plus aucun
moteur sans caractérisation. Prochaine direction à choisir au lot
171 (honnêteté des routes, sécurité, options/, research/).

- **Lot 169 — livré** : caractérisation du PROFIL D'ENTREPRISE
  `data/company.py` (340 lignes — cache hebdo + couche curée hors
  ligne + fetch yfinance côté utilisateur ; testé HORS LIGNE,
  _fetch_profile monkeypatché). 9 tests figent : l'INVARIANT des
  segments curés (les 20 répartitions somment toutes à 100 %) ; la
  démo qui sert la couche curée avec stale True SIGNALÉ ; le
  symbole inconnu → squelette honnête (None partout, jamais
  inventé) ; l'ordre cache/fetch/curé (fetch réussi → cache écrit,
  second appel sans réseau, schéma antérieur → re-fetch
  automatique, fetch mort → secours curé « jamais de page vide ») ;
  les pairs de la même industrie (soi-même exclu, cap 4) ; les
  médianes sectorielles (seuil 3 membres, PE < 250 strict,
  conversions en %, memo qui tient même vide — le cache 1.4 Mo
  n'est pas reparsé). Aucun code modifié, pas de bump SW.
  Suite 2310 → 2319 passed / 2 skipped.
- **Lot 168 — livré** : caractérisation de la STRATÉGIE OPTIONS
  PERSONNALISÉE `legacy_adapter.py` (272 lignes, 0 test — VIVANTE :
  servie par command et terminal ; échelle 1/2/3/6/9/12 mois,
  mark-to-market Black-Scholes en cours de route, constructeur de
  portefeuille). 21 tests figent : le régime (mots-clés + seuils
  exacts 60/40, {} → neutral) ; les briques (IV bornée [0.22,
  1.10], pas de strike 1/2.5/5/10, détention ~1/3 bornée 5-45 j) ;
  la jambe d'option (breakeven call = strike+prime / put =
  strike−prime, sorties EXACTES +50 %/−50 %, alerte théta clampée,
  scénarios ORDONNÉS pess < prob < except, cible technique du plan
  valorisée en route) ; le RÉGIME DANGEREUX qui impose le PUT même
  sur conviction haussière (défense d'abord) ; le portefeuille
  cœur×3/satellites×2 à arithmétique FERMÉE (cash = capital −
  déployé, maxloss = déployé, risque/position ~10 % borné) et le
  portefeuille vide honnête sans candidats. Aucun code modifié,
  pas de bump SW. Suite 2289 → 2310 passed / 2 skipped.
- **Lot 167 — livré** : caractérisation étendue du COPILOTE
  D'ANALYSE `ai/copilot.py` (159 lignes — répond en français ancré
  dans les nombres réels ; Anthropic entièrement mocké). 8 tests
  figent les LACUNES des 5 tests existants : les positions du desk
  (cap 20, filtre par symbole, stop repris du snapshot d'entrée,
  desk illisible → [] jamais inventé) ; le contexte sans symbole
  réduit à digest + positions ; le post-mortem chiffré inclus
  quand des trades clôturés existent ; le symbole normalisé
  (majuscules, 12 max) ; le chemin Claude mocké — succès étiqueté
  « estimation, pas une donnée broker » readonly True, texte vide
  ou exception API → repli déterministe étiqueté (jamais
  d'exception propagée) ; contexte indisponible → ok False avec
  erreur honnête et answer None. Aucun code modifié, pas de bump
  SW. Suite 2281 → 2289 passed / 2 skipped.
- **Lot 166 — livré** : caractérisation de la COUCHE IA OPTIONNELLE
  `ai/briefs.py` (178 lignes — traduction FR des news, mini-profils,
  descriptions ; dégradation IA → Google gratuit → texte d'origine).
  10 tests entièrement HORS LIGNE (_google_fr monkeypatché selon son
  contrat) : available exige une clé RÉELLE (absence, placeholder
  sk-ant-xxxx et mauvais préfixe rejetés) ; fr_news sans clé →
  repli Google avec CACHE (aucun second appel pour les mêmes
  titres), désalignement de lignes → titres anglais d'origine
  (fidélité > traduction), échec réseau → origine ; company_brief
  sans clé/résumé → {} (jamais un profil inventé) ; fr_label et
  fr_desc cachés avec repli sur l'origine (jamais un texte perdu).
  Aucun code modifié, pas de bump SW. Suite 2271 → 2281 passed /
  2 skipped.
- **Lot 165 — livré** : caractérisation du MOTEUR DE RISQUE du
  portefeuille RÉEL `risk_engine.py` (§26, servi par strategy_os —
  la chaîne du risque est désormais COMPLÈTE : correlation +
  stress_tests + basket_risk + risk_engine). 8 tests figent : la
  garde de provenance (snapshot 'SCANNER' → ValueError — le risque
  ne se calcule JAMAIS sur les candidats du scanner) ; les agrégats
  exacts (surpoids 66.67 % > 15 %, HHI 0.4623, secteur 80 % > 40 %
  averti, bêta pondéré 1.07 ; aucun bêta connu → None jamais un
  1.0 inventé) ; les règles de discipline aux bornes INCLUSES
  (drawdown -25 % pile → no_new_risk True « AUCUN nouveau risque » ;
  titre -23.1 % ≤ -20 % → revue obligatoire) ; le plafond d'options
  (4 > 3 → blocage) avec agrégat de greeks HONNÊTE (somme des seuls
  connus, gamma absent → None pas un 0, greeks_partial signalé) ;
  le contrat 14 clés. Aucun code modifié, pas de bump SW.
  Suite 2263 → 2271 passed / 2 skipped.

### MINI-BILAN tournée 161-165

5 lots, PR #194 → #198, suite 2239 → 2271 passed (+32 tests), SW
stable v151 (tournée tests pure). Couverts : les constituants
d'indices (« le démarrage n'est jamais bloqué » désormais PROUVÉ
par l'ordre de résolution cache → live → stale → static) ; le trio
audit/contexte/rôles (le journal IA borné, et les 4 RAPPELS
D'INVARIANTS READONLY injectés dans chaque analyse IA figés mot
pour mot) ; l'exposition factorielle et le moteur de remplacement
(« décision humaine requise » — jamais une exécution) ; la
vérification de vie des deux legacy (TOUS DEUX VIVANTS — aucun code
mort) ; le risque de panier (cap infaisable → somme n × cap,
concentration non détectée sur petit panier, FAIL-OPEN sur erreur
— trois limites documentées) ; et le moteur de risque réel (chaîne
du risque complète, bornes de discipline incluses, provenance
gardée). Le périmètre ai/data/strategy/portfolio n'a plus que
briefs/copilot/company/universe (couvertures partielles) et
legacy_adapter en file. Tout changement futur de ces sémantiques
fera échouer la suite.

- **Lot 164 — livré** : caractérisation du RISQUE DE PANIER
  `legacy_basket_risk.py` (99 lignes, 0 test — VIVANT malgré son
  nom : servi par analysis_api, command et risk_engine ; le
  « no-trade de concentration »). 8 tests figent : les gardes
  (panier < 2 séries → note honnête sans blocage, série < 40
  points exclue) ; le drapeau de corrélation (paire clonée 0.92 →
  no_new_risk True + top_pair expliquée ; panier diversifié →
  aucun drapeau) ; TROIS LIMITES documentées — cap infaisable
  (n × 15 % < 100 % → somme des poids = n × cap, pas de
  renormalisation), concentration sectorielle NON détectée sur
  petit panier (2 titres mono-secteur capés à 30 % restent sous le
  seuil 40 %), et FAIL-OPEN sur erreur (entrée illisible →
  no_new_risk False, l'analyse ne bloque pas quand elle ne peut
  pas conclure) ; la redistribution _cap_weights (somme 1 quand
  faisable). Aucun code modifié, pas de bump SW.
  Suite 2255 → 2263 passed / 2 skipped.
- **Lot 163 — livré** : caractérisation de l'EXPOSITION FACTORIELLE
  `factor_exposure.py` et du MOTEUR DE REMPLACEMENT
  `replacement_engine.py` (§25, zéro-test, dépendances research/
  monkeypatchées) + VÉRIFICATION DE VIE des deux legacy : TOUS
  DEUX VIVANTS (legacy_basket_risk → analysis_api + command +
  risk_engine ; legacy_adapter → command + terminal) — aucun code
  mort à signaler, candidats à caractérisation future. 8 tests
  figent : la pondération par les poids RÉELS (1.5 exact), la
  couverture partielle SIGNALÉE (« exposition indicative »),
  value None sans donnée (jamais un zéro inventé), les 10 facteurs
  toujours présents ; côté remplacement : place disponible → rien,
  bloqué → la plus faible du rôle avec « décision humaine
  requise » (jamais une exécution), candidat moins bon →
  « déconseillé », rôle sans membre → pool global documenté, sans
  scores → départage au défaut 50 mais score affiché None. Aucun
  code modifié, pas de bump SW. Suite 2247 → 2255 passed /
  2 skipped.
- **Lot 162 — livré** : caractérisation du TRIO zéro-test —
  `ai/audit.py` (journal des appels IA servi par strategy_os),
  `ai/strategy_context.py` (contexte injecté dans chaque analyse
  IA) et `portfolio/team_roles.py` (rôles §25). 8 tests figent :
  le journal BORNÉ à 200 entrées avec erreurs tronquées à 5 (pas
  de fuite verbeuse), les stats ok/fallbacks, le journal neuf
  honnêtement vide ; le contrat 10 clés du contexte avec bornes
  cohérentes ET les 4 RAPPELS D'INVARIANTS figés mot pour mot
  (« lecture seule absolue: aucun ordre », « moteur exécutif
  déterministe », « aucune promesse de performance », « jamais
  inventer » — les affaiblir cassera ce test) ; les 4 rôles dans
  l'ordre terrain, cohérents avec ROLE_TARGETS (une seule vérité
  d'effectifs), DEFENDER/GOALKEEPER sans horizon. Aucun code
  modifié, pas de bump SW. Suite 2239 → 2247 passed / 2 skipped.
- **Lot 161 — livré** : caractérisation des CONSTITUANTS D'INDICES
  `data/constituents.py` (112 lignes, 0 test — nourrit l'univers
  des titres au démarrage : Wikipedia + cache disque + snapshot
  statique). 9 tests SANS réseau (fetch monkeypatché, cache isolé) :
  normalisation yfinance (BRK.B → BRK-B), filtrage des tickers
  implausibles avec dédup ordonnée, intégrité du snapshot statique
  (≥ 400/80/25 ET déjà normalisé), et surtout l'ORDRE DE RÉSOLUTION
  complet — sans cache + réseau mort → static (démarrage JAMAIS
  bloqué), cache frais prioritaire (aucun appel réseau), force=True
  qui retente puis retombe sur cache-stale, liste vide dans le
  cache → repli statique PAR INDICE, fetch réussi → live + cache
  persisté ; garde-fou parsing (listes < 400/80/25 → ValueError
  explicite). Aucun code modifié, pas de bump SW.
  Suite 2230 → 2239 passed / 2 skipped.
- **Lot 160 — livré** : caractérisation de la famille RISQUE
  PORTEFEUILLE — `correlation.py` (consommé par risk_engine →
  drapeau du Command Center) et `stress_tests.py` (route
  strategy_os, §26), deux modules zéro-test. 11 tests figent :
  bornes ±1.0 exactes, gardes (< 30 points / variance nulle →
  None), paires triées, seuils high_pairs ≥ 0.8 et avertissement
  ≥ 0.7, matrice vide honnête ; côté stress : l'hypothèse
  DOCUMENTÉE bêta inconnu = 1.0 (SPY -5 % → -4.17 % exact), le
  secteur dominant, CORRELATIONS_TO_ONE qui ne choque QUE les
  actions (le cash protège), la sensibilité taux inconnue → None
  honnête, le REFUS des stress sans équité calculable, le
  worst_case et l'alerte drawdown, les 10 scénarios déclarés
  présents. Aucun code modifié, pas de bump SW.
  Suite 2219 → 2230 passed / 2 skipped.

### MINI-BILAN tournée 156-160

5 lots, PR #189 → #193, suite 2178 → 2230 passed (+52 tests), SW
stable v151 (tournée tests pure). Couverts : la structure par
pivots (les 5 signaux du plan, anti-chasse 1.2 ATR), les
indicateurs techniques purs (quatre philosophies de trous de
données DOCUMENTÉES : SMA se réinitialise, EMA traverse, ATR
recopie, VWAP resservi ; RSI golden Wilder 70.5), la règle de
fraîcheur du Live Engine (bornes STRICTES des 7 domaines — à la
borne on bascule déjà), l'horloge de marché (borne 4h00, limite
jours fériés documentée), et la famille risque portefeuille
(corrélations + stress tests : bêta inconnu = 1.0, le cash protège,
refus honnête sans équité). Le nouveau périmètre ai/data/strategy/
portfolio est inventorié : 11 modules zéro-test, file publiée au
lot 159. Tout changement futur de ces sémantiques fera échouer la
suite et devra être assumé explicitement.

- **Lot 159 — livré** : complément de l'HORLOGE DE MARCHÉ
  `market_clock.py` (5 tests : borne pré-marché 4h00 exacte,
  vendredi 20h00 → fermé jusqu'au lundi, format « 09:05 ET »
  zéro-paddé, et une LIMITE documentée — pas de calendrier de
  jours fériés : le 1er janvier en semaine est affiché « open »,
  ajouter un calendrier NYSE = décision explicite que ce test
  rendra visible) + INVENTAIRE du nouveau périmètre
  (vertex/ai/, data/, strategy/, portfolio/) : 11 modules à ZÉRO
  test découverts, dont la FAMILLE RISQUE PORTEFEUILLE
  (correlation 42 l, factor_exposure 29 l, replacement_engine
  36 l, stress_tests 85 l) priorisée pour le lot 160, puis
  data/constituents (112 l), ai/audit, ai/strategy_context, et
  deux legacy à vérifier (legacy_basket_risk, legacy_adapter).
  Aucun code modifié, pas de bump SW. Suite 2214 → 2219 passed /
  2 skipped.
- **Lot 158 — livré** : caractérisation de la RÈGLE DE FRAÎCHEUR du
  LIVE ENGINE `live_engine.py` (258 lignes — le moteur de
  synchronisation dont dépendent toutes les pages ; les 13 tests
  existants couvrent les flux, ce lot fige les BORNES de la partie
  pure). 19 tests : les bornes STRICTES des 7 domaines (à la borne
  exacte on bascule déjà — age == frais → stale, age == rassis →
  offline ; seuils figés : prices 5 min/30 min, options 1 h/6 h,
  companies 48 h/8 j, news 2 h/12 h, calendar 1 j/4 j, weekly
  8 j/15 j, ai 5 min/30 min) ; les défauts du domaine inconnu
  (600/3600) ; les bascules de libellés EXACTES (59s → « 59s »,
  60 → « 1 min », 3600 → « 1 h », 86400 → « 1 j ») ; l'âge None →
  « jamais synchronisé » honnête ; le forçage de cycle (wait_force
  réveillé → True et l'événement CONSOMMÉ ; force_event rend le
  même objet par domaine). Aucun code modifié, pas de bump SW.
  Suite 2195 → 2214 passed / 2 skipped.
- **Lot 157 — livré** : caractérisation des INDICATEURS TECHNIQUES
  purs `market/indicators.py` (155 lignes, §12 — SMA/EMA/RSI/ATR/
  Bollinger/VWAP sans pandas ; seules les LACUNES des 11 tests
  existants sont figées). 9 tests : robustesse (non-numérique →
  None traversant, fenêtre nulle → tout None) ; les ASYMÉTRIES de
  trous de données DOCUMENTÉES — SMA se réinitialise (honnêteté de
  fenêtre), EMA traverse (pas de fenêtre à invalider), ATR recopie
  la dernière valeur, VWAP resservi sur volume nul — deux
  philosophies assumées, les unifier = décision explicite ;
  longueurs H/L/C tronquées au minimum ; la valeur GOLDEN du RSI
  sur la série classique de Wilder (70.5 — prouve le lissage de
  Wilder, pas une SMA) ; le multiplicateur Bollinger à écart
  symétrique exact. Aucun code modifié, pas de bump SW.
  Suite 2186 → 2195 passed / 2 skipped.
- **Lot 156 — livré** : caractérisation de la STRUCTURE PAR PIVOTS
  `pivots.py` (124 lignes, ratio 0.65 — structure() appelée par
  analysis.py : sommets/creux fractals, tendance, logique d'entrée,
  stop STRUCTUREL du plan). 8 tests figent, chacun par un zigzag
  déterministe : les 5 signaux — EN_TENDANCE (milieu de mouvement →
  pas d'entrée), REFUS_DOWNTREND (rebond en baisse = piège, aucun
  niveau émis), RANGE (cassure confirmée exigée), BREAKOUT
  (franchissement RÉCENT ≤ 1.2 ATR anti-chasse → stop sous le
  dernier creux, cible = extension measured-move, rr cohérent),
  REPLI_REPRIS (repli ≤ 1.8 ATR sur le creux PUIS reprise → cible
  le sommet) ; les gardes (série courte / entrée invalide → None) ;
  le repli ATR à 1 % du cours (jamais de ÷0) ; le contrat 16 clés
  avec fenêtres swing bornées à 4. Aucun code modifié, pas de bump
  SW. Suite 2178 → 2186 passed / 2 skipped.
- **Lot 155 — livré** : caractérisation du BRIEF ÉDITORIAL
  `editorial.py` (202 lignes, ratio 0.34 — le narratif de séance
  §10 en tête d'Aujourd'hui ; scoring.py écarté car déjà couvert
  finement par le lot 97). 17 tests figent : les seuils EXACTS des
  phrases d'indices (±0.15), le leadership technologique à écart
  STRICT > 0.2 (0.2 pile ne déclenche pas) et la rotation
  cyclique ; les trois phrases VIX aux bornes 18/25 ; la frontière
  breadth 55 (saine/sélectivité) ; la PRIORITÉ des risques
  (RISK-OFF avant breadth étroite ; breadth < 45 strict, 45 pile →
  aucun risque déclaré) ; la branche calls IV chère ; le titre
  « À la une » borné à 180 caractères ; les sources triées et
  dédupliquées ; l'opportunité prioritaire qui saute les REFUSER.
  Aucun code modifié, pas de bump SW. Suite 2161 → 2178 passed /
  2 skipped.

### MINI-BILAN tournée 151-155

5 lots, PR #184 → #188, suite 2098 → 2178 passed (+80 tests), SW
stable v151 (tournée tests pure). Les modules minces HORS engines/
sont couverts : les SIX à zéro test (regime_features — le cerveau
physique qui modifie le score, sectors, ml_calibration, context,
news_impact, news_pipeline) plus editorial (0.34). Découvertes clés
désormais VERROUILLÉES par des tests : une droite pure n'a pas
d'exposant de Hurst (analyze(droite) = NEUTRE malgré efficience
1.0) ; les bornes humbles de la probabilité de gain [0.05, 0.85]
(jamais une promesse) ; le verdict météo « participation ?% »
honnête ; la limite de sous-chaîne du classement d'actualités
('ai' matche dans « mountain ») ; les bandes VIX 16/22 (données)
vs 18/25 (narratif) ; les bornes RORO ±8 ; la hiérarchie des
risques éditoriaux (régime indéterminé > RISK-OFF > breadth < 45).
Tout changement futur de ces sémantiques fera échouer la suite.

- **Lot 154 — livré** : caractérisation des ACTUALITÉS (§15) —
  `news_impact.py` (classement par mots-clés + importance +
  direction potentielle) et `news_pipeline.py` (validation/dédup/
  tri), deux modules zéro-test servis par daily_brief. 20 tests
  figent : la priorité du PREMIER match (MACRO gagne sur RESULTATS)
  et le défaut ENTREPRISE ; une LIMITE documentée — matching par
  SOUS-CHAÎNE, le mot-clé 'ai' matche dans « mountain »/« rain » →
  SECTEUR (passer aux frontières de mots = décision explicite) ;
  l'arithmétique d'importance EXACTE (base 30, corroborations
  plafonnées +30, portefeuille +25, bonus catégorie, plafond 100) ;
  les seuils de direction ±0.15 EXACTS avec confiance plafonnée
  0.7 (humble, jamais une causalité affirmée) ; les rejets du
  pipeline COMPTÉS jamais masqués ; le doublon fusionné en
  corroborations (2 → importance 80 recomposée) ; sym en
  majuscules, fr vide → None, tri décroissant, état vide honnête.
  L'assainissement XSS reste chez news_plus (déjà couvert). Aucun
  code modifié, pas de bump SW. Suite 2141 → 2161 passed /
  2 skipped.
- **Lot 153 — livré** : caractérisation du CONTEXTE MARCHÉ
  `context.py` (105 lignes, 0 test — la « météo » du jour servie
  par decision_api et terminal : régime du SPY lui-même, bandes
  VIX, Risk-On/Off cycliques vs défensifs, breadth des leaders,
  verdict du jour). 15 tests figent : la robustesse totale (5 ×
  None → contrat complet, verdict quand même émis avec
  « participation ?% » honnête — limite documentée) ; le régime
  SPY (rampe → TREND ADX 100, oscillation → CHOP) ; les bandes VIX
  à bornes EXACTES (15.9 calme / 16.0 normal / 21.9 normal / 22.0
  stress ; 1 seul point → None) ; la breadth réelle (nh pos52 ≥ 98,
  nl ≤ 5) ; les bornes RORO EXACTES ±8 (gap 8 RISK-ON, 7 NEUTRE,
  -8 RISK-OFF ; sans secteurs → 50/50 NEUTRE) ; le verdict complet
  composé. Aucun code modifié, pas de bump SW.
  Suite 2126 → 2141 passed / 2 skipped.
- **Lot 152 — livré** : caractérisation combinée de la ROTATION
  SECTORIELLE `sectors.py` (83 lignes, 0 test — servie par le
  comité et la fiche Analyse) et de la CALIBRATION ML
  `ml_calibration.py` (92 lignes, 0 test — probabilité de gain
  consommée par quant_engine). 13 tests figent : agrégats exacts
  (avg_score, pct_buy, breadth depuis les signaux), tri décroissant,
  symbole hors mapping exclu, bornes risk_band exactes (<3 Low,
  3-5 Med, >5 High), delta vs veille (scores None ignorés, sans
  baseline → None), défauts neutres sans détail moteur ; côté ML :
  point NEUTRE edge 54 → 0.500, calibration annoncée figée
  (86 → 0.736, 30 → 0.317), bornes HUMBLES [0.05, 0.85] (jamais
  une promesse), ajustement Monte-Carlo first-touch, et deux
  limites documentées — bloc None → proba neutre 0.468 mais edge
  NON NUMÉRIQUE → prédiction entière None (pas de repli partiel).
  Aucun code modifié, pas de bump SW. Suite 2113 → 2126 passed /
  2 skipped.
- **Lot 151 — livré** : NOUVELLE DIRECTION — modules minces HORS
  engines/. Inventaire par ratio : six modules à ZÉRO test direct
  (market/context, news_impact, news_pipeline, regime_features,
  sectors, quant/ml_calibration). Choisi : `regime_features.py`
  (179 lignes) — le CERVEAU PHYSIQUE importé par analysis.py, dont
  la rétroaction score_adjust MODIFIE le score Vertex. 15 tests
  figent : Hurst persistant > 0.56 / anti-persistant < 0.2 + LIMITE
  documentée (une droite PURE n'a pas d'exposant — différences
  décalées constantes → None, d'où analyze(droite) = NEUTRE malgré
  efficience 1.0) ; entropie (constants → 0.0, concentré < dispersé,
  garde 30 points) ; efficience de Kaufman (monotone → 1.0 exact,
  aller-retour → 0.0, plat → None) ; demi-vie OU (rappel fort →
  courte, tendance → None honnête) ; états TENDANCE
  FRACTALE/RETOUR MOYENNE avec notes ; rétroaction EXACTE (+4/+7,
  -7, -3/-6, -2 entropie extrême — extrêmes réels +7/-9, marge
  sous les bornes [-10,+8]) ; physique absente → (0, ''). Séries
  déterministes à graines fixes (PCG64 stable). Aucun code modifié,
  pas de bump SW. Suite 2098 → 2113 passed / 2 skipped.
- **Lot 150 — livré** : caractérisation du DIGEST DE SESSION
  `session_digest.py` (116 lignes, ratio 0.80 — dernier de la file
  des moteurs minces ; servi par /api/session/digest, affiché en
  tête d'Aujourd'hui). 8 tests figent : la garde RISK-ON + S&P en
  CHOP → NEUTRE (un risk-on dans un marché haché n'est pas un feu
  vert) ; RISK-OFF prioritaire même seul ; le score /100 branché
  sur l'unique source market_lens.climate (93 — jamais réinventé) ;
  les dte booléens/texte ignorés sans masquer les catalyseurs
  valides (tri croissant) ; scan_ts booléen → âge None (même garde
  que le lot 142 côté UI) ; build(None, None) honnêtement
  'analyzing' ; top borné à 3 avec compte complet ; contrat de
  sortie exact. Aucun code modifié, pas de bump SW.
  Suite 2090 → 2098 passed / 2 skipped.

### MINI-BILAN tournée 146-150

5 lots, PR #179 → #183, suite 2033 → 2098 passed (+65 tests), SW
stable v151 (aucun changement de shell — tournée moteur pure). La
file des moteurs par couverture croissante est ÉPUISÉE : analysis
(ratio 0.19), strategy_fit (0.35), postmortem (0.61), market_lens
(0.66), stats (0.77), session_digest (0.80) — tous caractérisés
sur leurs branches, gardes, bornes exactes et comportements
limites. Découvertes clés désormais VERROUILLÉES par des tests :
divergence des seuils FAVORABLE (62 au climat market_lens vs 65 au
tilt strategy_fit — même formule) ; Spearman à rangs ordinaux (une
série constante « corrèle » à 1.0) ; break-even classé perte ;
profit factor None jamais infini ; booléens rejetés par toutes les
gardes numériques ; Socle défensif exige un ext_atr explicite ;
l'inconnu n'est jamais investissable (plancher scorecard 18/40 <
seuil B). Tout changement futur de sémantique sur ces points fera
échouer la suite et devra être assumé explicitement.

- **Lot 149 — livré** : caractérisation du PRISME MARCHÉ
  `market_lens.py` (77 lignes — source unique du score marché /100,
  servie par feeds/decision_api/command) + `stats.py` (Spearman de
  l'edge, médianes secteur). 13 tests figent : les bornes EXACTES
  des bandes du climat (FAVORABLE ≥62, DANGEREUX <40) avec une
  DIVERGENCE réelle documentée (même formule que le tilt
  strategy_fit mais seuil 62 ici contre 65 là-bas) ; climat sur
  None ET {} → None (pas de climat inventé) ; le tiers supérieur
  porteur (n=2 → seul le rang 1) ; le score de secteur non
  numérique classé dernier avec avg_score None honnête ; la
  frontière titre fort à 70 STRICTE ; « 2 verts dont le titre » →
  partiellement aligné (pas contre-courant) ; la frontière Spearman
  8 points ; une LIMITE documentée — rangs ordinaux sans rangs
  fractionnaires : une série constante « corrèle » à 1.0
  (pathologique en réel, la changer = décision explicite) ; les
  bornes strictes 0 < PE < 250 et l'exclusion des secteurs sans
  valorisation. Aucun code modifié, pas de bump SW.
  Suite 2077 → 2090 passed / 2 skipped.
- **Lot 148 — livré** : caractérisation étendue du POST-MORTEM du
  Journal `postmortem.py` (151 lignes, ratio 0.61 — fonction pure
  servie par /api/journal/postmortem, affichée dans
  Journal/Discipline). 10 tests figent : la coercition numérique
  (cost=True REJETÉ — bool est un int, un flag ne devient jamais
  un coût ; chaînes numériques OK ; inf/0/négatif inexploitables) ;
  deux limites DOCUMENTÉES — break-even classé PERTE (win_rate 0,
  PF None sans ÷0) et échantillon 100 % gagnant → PF None (indéfini
  honnête, PAS infini) avec narrative sans phrase PF ; le drapeau
  « win rate élevé mais P&L négatif » ; les récidives triées par
  nombre de pertes décroissant ; les dates inversées (abs) et non
  parsables (None exclu de la moyenne — pas de 0 inventé) ; les 8
  dernières erreurs du journal tronquées à 140 ; le contrat de
  sortie identique plein/vide avec generator déterministe. Aucun
  code modifié, pas de bump SW. Suite 2067 → 2077 passed / 2
  skipped.
- **Lot 147 — livré** : caractérisation étendue de la COUCHE
  STRATÉGIE `strategy_fit.py` (161 lignes, ratio 0.35 — source
  unique : terminal.py délègue vehicle_of / attach_vehicle /
  strat_score ; c'est elle qui choisit ACTION vs OPTION et oriente
  les playbooks). 17 tests figent : la branche AU CHOIX et le
  message « IV chère » ; les défauts EXACTS du strat_score (score
  seul → 50, ligne vide → 22, clamp 0) ; la PRIORITÉ des 6
  playbooks (Momentum avant Qualité) + limite documentée (Socle
  défensif exige un ext_atr explicite — le calme non prouvé n'est
  pas calme) ; attach_vehicle (meilleur CALL par qualité, PUT
  ignoré, board vide → ACTION) ; le seuil rr_ok ≥ 2 STRICT (1.99
  échoue) avec repli plan → vx_rr et R:R inconnu honnête ; les 3
  bandes du tilt à l'arithmétique exacte (93 FAVORABLE / 50 NEUTRE
  avec round bancaire / DANGEREUX). Aucun code modifié, pas de
  bump SW. Suite 2050 → 2067 passed / 2 skipped.
- **Lot 146 — livré** : caractérisation étendue du CŒUR analytique
  `analysis.py` (333 lignes — la couverture la plus mince de
  vertex/engines/, ratio tests/moteur 0.19 : le golden figeait UN
  scénario, aucune branche de détection couverte). 17 tests
  figent : robustesse aux flux sans Volume (indices/ETF) et à
  l'historique court (repli SMA→EWM, JSON sans NaN) ; profils
  DÉFENSIF et ÉQUILIBRÉ ; radar d'anomalies (gap, pic de volume)
  avec FORMULE du score figée (min(100, Σ sév × 16)) et niveaux
  cohérents ; cassure confirmée (volume ≥1.5× exigé) ; régime
  CHOP ; invariants du plan (stop sous l'entrée, échelle exacte
  1R/2R/3R, setup_quality borné) ; transparence du score
  (score == clamp(base + struct_adj [-12,+10])) ; checklist des
  9 signaux + sigcount. Aucun code modifié, pas de bump SW.
  Suite 2033 → 2050 passed / 2 skipped.
- **Lot 145 — livré** : caractérisation du moteur `scorecard.py`
  (254 lignes) — vérifié VIVANT : importé par terminal.py (alias
  `ibkr`), `verdict()` appelé pendant le scan ; produit le score
  /40, les niveaux S+/S/A/B + allocations, l'entry timing, le
  no-chase et le verdict affichés dans Opportunités ; c'était le
  DERNIER moteur à zéro référence dans tests/. 36 tests figent :
  grille des niveaux à bornes exactes (36/32/28/22 + allocations),
  les 4 raisons no-chase isolées, les 6 états d'entry timing, le
  plancher neutre 18/40 → rejeté (l'inconnu n'est jamais
  investissable), la fenêtre catalyseur earnings (7-45 j idéale),
  verdict({}) → None (falsy — pas de données, pas de verdict),
  somme des composantes == score40 (une seule vérité), robustesse
  aux valeurs pourries. Aucun code modifié, pas de bump SW.
  Suite 1997 → 2033 passed / 2 skipped.

### MINI-BILAN tournée 141-145

5 lots, PR #174 → #178, SW stable v150 → v151 : fourchette
analystes en rail à repères (141) · staleness par domaine en barre
relative + garde Number(null) (142) · tournée de vérification
transversale : AUCUN défaut restant, l'esthétique 124-143 est
déclarée COMPLÈTE sur preuves (143) · pivot vers les
caractérisations moteur : timeframes.py figé en 13 tests (144) ·
scorecard.py — le dernier moteur à zéro test — figé en 36 tests
(145). Suite 1984 → 2033 passed / 2 skipped : plus AUCUN moteur de
vertex/engines/ sans test direct ; les deux contributeurs au score
(confluence ±5, scorecard /40) ont désormais leurs contrats,
gardes et planchers neutres verrouillés par des tests qui rendent
tout changement de sémantique explicite.

- **Lot 144 — livré** : retour aux caractérisations moteur —
  `timeframes.py` (confluence journalier × hebdo, contribue ±5 au
  score Vertex, drapeau `mtf` du scan) n'avait AUCUN test direct.
  13 tests figent : les 5 états et leurs contributions exactes
  (ALIGNÉ HAUSSIER +5 · REPLI DANS TENDANCE +3 · REBOND
  CONTRE-TENDANCE -4 · ALIGNÉ BAISSIER -5 · NEUTRE 0, cette
  dernière branche construite empiriquement : prix > EMA30 hebdo
  mais EMA10 qui se retourne) ; gardes < 32 semaines → None et
  entrée non ré-échantillonnable → None ; contrat de sortie 9 clés
  typées ; comportement limite série plate DOCUMENTÉ (ALIGNÉ
  BAISSIER, RSI 100 — pathologique, le changer = décision
  explicite). Aucun code moteur/UI modifié, pas de bump SW.
  Suite 1984 → 1997 passed / 2 skipped.
- **Lot 143 — livré** : tournée de VÉRIFICATION transversale des
  8 espaces (clôture de la directive esthétique maximale) : 8
  captures desktop 1440 fraîches (une par espace, 0 erreur console
  chacune) inspectées à la recherche des derniers défauts — chiffres
  nus, chevauchements, barres plates, badges débordants, étiquettes
  coupées. Constat honnête : AUCUN défaut restant ; les fixes des
  lots 125/129/133/142 tiennent tous ; le treemap Portefeuille
  neutre est l'honnêteté (marques IBKR indisponibles), pas un
  défaut. Lot documentaire — aucun code modifié, PAS de bump SW
  (v151 courante). La tournée esthétique 124 → 143 est COMPLÈTE.
  Suite 1984/2, RC GO, parcours 14/14, responsive 0 défaut.
- **Lot 142 — livré** : passe graphique n°17 — Système/Données :
  l'ÂGE de la fraîcheur par domaine n'est plus un texte nu —
  mini-barre de verre de STALENESS relative (échelle = âge max
  connu) : les domaines frais restent discrets, le plus rassis
  (companies, 20 481 min) saute aux yeux en pleine barre negative.
  Couleur par état ; sans âge connu → pas de barre (garde
  d.age_s == null AVANT Number(), car Number(null) = 0).
  Automatisations vérifiée (badges + honnêteté déjà corrects).
  SW v150 → v151 + 4 gardiens. Captures avant/après envoyées.
  Suite 1984/2, RC GO.
- **Lot 141 — livré** : passe graphique n°16 — fiche Analyse,
  section Sentiment : la FOURCHETTE des objectifs analystes n'est
  plus du texte nu — RAIL de verre low → high avec deux repères
  halotés : le COURS en cyan et l'OBJECTIF MOYEN en warning. On
  voit d'un coup d'œil où le prix vit dans la fourchette (cours 198
  AU-DESSUS de l'objectif 179 → potentiel négatif expliqué).
  Repères clampés aux bords, bornes affichées, title au survol.
  SW v149 → v150 + 4 gardiens. Captures + zoom envoyés.
  Suite 1984/2, RC GO.
- **Lot 140 — livré** : passe graphique n°15 — Top/Flop 10 de la Vue
  d'ensemble Marchés : chaque variation gagne sa mini-barre SIGNÉE
  de verre (positive → verte depuis la gauche, négative → rouge
  alignée à droite ; échelle relative au max de la liste) — la
  hiérarchie des mouvements se lit sans les pourcentages (ABT -6,3 %
  pèse visiblement 3× ALGN -1,3 %). SW v148 → v149 + 4 gardiens.
  Captures avant/après envoyées. Suite 1984/2, RC GO.

### MINI-BILAN tournée 136-140

5 lots, suite constante **1984 passed / 2 skipped**, PR #169 → #173,
SW v144 → v149 : comparaison des candidats en verre + score Skyler
/40 en barre graduée (136) · poids de position avec repère du
plafond de tier (137) · concentration avec repère prudent ~15 %
(138) · leadership sectoriel avec halo du meneur (139) · Top/Flop
10 en barres signées (140). Le patron « mini-barre de verre
color-mix sur tokens » est GÉNÉRALISÉ — plus un seul chiffre nu
structurant sur les 8 espaces ; chaque barre porte désormais soit
une graduation (seuils moteur), soit un signe (axe zéro), soit un
repère (plafond/seuil prudent), soit un halo (meilleur/pire/meneur).

- **Lot 139 — livré** : passe graphique n°14 — Vue d'ensemble
  Marchés : le Leadership sectoriel passe en VERRE — chaque barre
  est un dégradé de sa propre couleur (color-mix) et le secteur
  MENEUR garde l'ember avec un halo doux (le leadership se voit
  avant de lire le score). Hiérarchie par intensité conservée.
  Aujourd'hui vérifiée : Aura, Runway, listes et tuiles KPI déjà
  au niveau (tuiles gardées — non touchées). SW v147 → v148 +
  4 gardiens. Captures avant/après envoyées. Suite 1984/2, RC GO.
- **Lot 138 — livré** : passe graphique n°13 — Synthèse
  Portefeuille : la tuile KPI CONCENTRATION n'est plus un chiffre
  nu — mini-barre de verre avec le REPÈRE prudent (~15 % par titre,
  celui cité par le Risque dominant) au tick : < 15 % positive,
  15-25 warning, > 25 negative + halo. Le 65 % d'ACN vire au rouge,
  la donnée et son seuil se parlent enfin. n/d honnête conservé.
  SW v146 → v147 + 4 gardiens. Captures avant/après envoyées.
  Suite 1984/2, RC GO.
- **Lot 137 — livré** : passe graphique n°12 — Positions
  Portefeuille : le POIDS de chaque position devient une mini-barre
  de verre avec REPÈRE DU PLAFOND du tier (tick à 60 % du rail =
  plafond, ex. 15 % Constitution ; sous 80 % → positive, proche →
  warning, au-dessus → negative + halo). Sans tier connu : échelle
  simple, aucun plafond inventé. Le chiffre éducatif d'un poids,
  c'est sa distance au plafond. SW v145 → v146 + 4 gardiens.
  Captures avant/après envoyées. Suite 1984/2, RC GO.
- **Lot 136 — livré** : passe graphique n°11 — Radar Opportunités :
  (a) la Comparaison des meilleurs candidats passe en VERRE — chaque
  barre est un dégradé de sa propre couleur et le MEILLEUR du
  critère gagne un halo doux ember (le gagnant se voit sans lire
  les nombres) ; (b) le score canonique /40 du Classement Skyler
  gagne sa mini-barre graduée (≥ 28 positive, 16-27 warning, < 16
  negative). Watchlist vérifiée : états vides honnêtes en démo.
  SW v144 → v145 + 4 gardiens. Captures avant/après envoyées.
  Suite 1984/2, RC GO.
- **Lot 135 — livré** : passe graphique n°10 — scan Actions
  (Opportunités) : le SCORE n'est plus un chiffre nu — mini-barre de
  verre GRADUÉE 0-100 (≥ 70 positive = actionnable, 40-69 warning =
  à surveiller, < 40 negative = rejeté — les seuils réels du
  moteur), dégradé color-mix sur tokens, valeur tabulaire conservée.
  La hiérarchie de la liste de travail quotidienne se lit d'un coup
  d'œil. SW v143 → v144 + 4 gardiens. Captures avant/après
  envoyées. Suite 1984/2, RC GO.

### MINI-BILAN tournée 131-135

5 lots (passes noyau → widgets faits main), suite constante
**1984 passed / 2 skipped**, PR #164 → #168, SW v139 → v144 :
stress tests verre + pire scénario mis en avant (131) · anomalies
en mini-barres + calendrier avec imminence ≤ 7 j (132) · payoff de
structure Options — 2 bugs préexistants tués, spot/BE enfin tracés
(133) · net GEX en barre signée depuis l'axe zéro (134) · score du
scan en barre graduée (135). Le patron « mini-barre de verre
color-mix sur tokens » est devenu la réponse standard aux chiffres
nus ; 3 bugs visuels réels tués sur la tournée (stats collées,
rails invisibles, plugins payoff jamais exécutés).

- **Lot 134 — livré** : passe graphique n°9 — radar de positionnement
  du desk Options : le net GEX n'est plus un nombre nu — mini-barre
  SIGNÉE de verre depuis l'axe zéro (positif → droite en positive =
  stabilisant ; négatif → gauche en negative = accélérateur ;
  dégradé color-mix sur tokens, échelle relative au max du radar,
  valeur M$ conservée à côté). L'œil voit qui pousse où et avec
  quelle force. Vue LEAPS vérifiée (rien de plat). SW v142 → v143
  + 4 gardiens. Captures avant/après envoyées. Suite 1984/2, RC GO.
- **Lot 133 — livré** : passe graphique n°8 — payoff de structure du
  desk Options : **2 bugs préexistants tués** — (a) le 3e argument
  `[refPlugin]` passé à `C.mount` (qui n'en prend que 2) était
  silencieusement ignoré : les repères spot/breakeven ne
  s'affichaient JAMAIS ; (b) `getPixelForValue(prix)` sur un axe
  catégorie attend un index → mapping prix→index ajouté. Repères
  désormais sur tokens (spot info, BE warning — grammaire lot 124,
  les rgba orphelins morts), zones gain/perte teintées, trait 1.6 +
  halo. SW v141 → v142 + 4 gardiens. Captures avant/après + zoom
  envoyées (BE 153.23 et spot 180 enfin visibles). Suite 1984/2,
  RC GO.
- **Lot 132 — livré** : passe graphique n°7 — Opportunités : (a) la
  table des ANOMALIES perd ses chiffres nus — l'intensité devient
  une mini-barre de verre (dégradé warning via color-mix, échelle
  relative au max du scan) + valeur tabulaire ; (b) le CALENDRIER
  gagne l'IMMINENCE visuelle — tout événement à ≤ 7 jours porte un
  liseré warning et sa date en warning gras (dte réel earnings,
  écart de dates macro ; option `urgent` ajoutée au builder
  timelineCard). SW v140 → v141 + 4 gardiens. Captures avant/après
  envoyées. Suite 1984/2, RC GO.
- **Lot 131 — livré** : passe graphique n°6 — Portefeuille/Risque :
  les barres des STRESS TESTS passent en matière VERRE (dégradé de
  leur propre couleur via color-mix sur tokens, doux au zéro → dense
  à l'impact) et le PIRE scénario est mis en avant (libellé négatif
  gras + halo + aria « pire scenario ») — le chiffre éducatif d'un
  stress test. Vue Performance vérifiée : états vides honnêtes en
  démo, jauge HHI et donut sectoriel héritent déjà du noyau.
  SW v139 → v140 + 4 gardiens. Captures avant/après envoyées.
  Suite 1984/2, RC GO.
- **Lot 130 — livré** : passe graphique n°5 — fiche Analyse : le bloc
  « Performance multi-horizons » (1 sem./1 mois/1 trim./1 an) passe
  en matière VERRE — chaque barre est un dégradé de sa propre
  couleur, doux au centre (zéro) → dense à l'extrémité de la valeur,
  construit par color-mix sur les tokens (aucun littéral nouveau).
  Reste de la fiche vérifié : radar, chandeliers+plan, runway,
  price-chart, timeline déjà au niveau. SW v138 → v139 + 4 gardiens.
  Captures avant/après envoyées. Suite 1984/2, RC GO.

### MINI-BILAN tournée 126-130

5 lots (fin de 1re tournée + 4 passes noyau), suite constante
**1984 passed / 2 skipped**, PR #159 → #163, SW v134 → v139 :
jauge verre + libellés kv protégés + badge adaptatif (126) ·
heatmaps verre sur tokens — derniers rgba hors palette éliminés
(127) · donut à chiffre central éducatif (128) · rails sémantiques
rétablis + courbe des taux cyan + anti-collision endDots (129) ·
multi-horizons verre de la fiche Analyse (130). Deux BUGS visuels
réels tués : stats collées « Trades3 » (125) et rails invisibles
sous override noir !important (129). Le noyau graphique (barres,
jauges, heatmaps, donuts, lignes, aires, radar, treemap, entonnoir,
payoff) est désormais ENTIÈREMENT en grammaire verre sur tokens.

- **Lot 129 — livré** : passe graphique n°4 — **bug visuel réel
  corrigé** : les rails CALME↔STRESS et DÉFENSE↔ATTAQUE de Marchés
  étaient INVISIBLES (une règle neon-glass `background:rgba(0,0,0,.28)
  !important` écrasait le dégradé sémantique — vérifié au navigateur,
  backgroundImage:none) → override supprimé, dégradés rétablis.
  Courbe des taux US : « Actuelle » passe en cyan (elle se détache
  enfin de l'ombre grise de la veille). C.endDotsPlugin : anti-
  collision des noms de série (≥ 11 px d'écart — toutes les
  multiLine héritent). SW v137 → v138 + 4 gardiens. Captures
  avant/après envoyées (Volatilité + Macro). Suite 1984/2, RC GO.
- **Lot 128 — livré** : passe graphique n°3 — le donut gagne SON
  chiffre éducatif : la catégorie dominante et sa part (« 55 % /
  AVOID ») s'affichent au CENTRE de l'anneau, dans la couleur de son
  arc (plugin vxDonutCenter ; rien si total nul — aucune donnée
  inventée ; signature lot 53 intacte). Tous les donuts héritent.
  Tour des autres builders : anomaly-scan, équité/drawdown,
  sparkline déjà au niveau. SW v136 → v137 + 4 gardiens. Captures
  avant/après envoyées. Suite 1984/2, RC GO.
- **Lot 127 — livré** : passe graphique n°2 — heatmaps matière VERRE
  (`C.heatmapCard`) : les DERNIERS rgba verts/rouges hors palette du
  système graphique remplacés par les tokens (convertis en rgb à
  l'exécution), chaque cellule devient une tuile de verre (dégradé
  diagonal de sa propre couleur, liseré inset, coins arrondis),
  grille aérée (border-spacing 3px). Héritent : matrice scénarios
  options (Stop/Flat/TP × temps), heatmap secteurs Marchés, P&L
  mensuel Portefeuille. Theta et sensibilité IV vérifiés — ils
  héritaient déjà des lots 120/125. SW v135 → v136 + 4 gardiens.
  Captures avant/après envoyées. Suite 1984/2, RC GO.
- **Lot 126 — livré** : amélioration graphique n°8 (Système) — **1re
  tournée esthétique TERMINÉE (8 pages / 8)**. Jauge `C.gauge` en
  matière VERRE (arc de valeur = dégradé de sa propre couleur, doux →
  dense, posé sur un halo large ; point de lecture avec halo — toutes
  les jauges héritent : Santé moteurs, Participation Marchés…) ;
  libellés clé/valeur protégés dans utilities.css (une valeur longue
  n'écrase plus le libellé en « Ét at » — gardien lot 57 respecté) ;
  badge des canaux en colonne adaptative (CONFIGURATION_MISSING
  s'affiche entier). Aucun littéral couleur nouveau. SW v134 → v135
  + 4 gardiens. Captures avant/après envoyées. Suite 1984/2, RC GO.

### MINI-BILAN tournée 121-125

5 lots graphiques (directive esthétique maximale), suite stable
**1984 passed / 2 skipped**, PR #154 → #158, SW v129 → v134 :
entonnoir monochrome + scatter teinté (Opportunités) · radar radial
(Analyse) · treemap verre (Portefeuille) · payoff breakeven/spot
(Options) · barres verre + stats stylées (Journal). Grammaire
commune installée : dégradé dense → doux de la propre couleur de
l'objet, liseré fin, UN chiffre éducatif par graphique, tokens
uniquement. Reste : Système (lot 126), puis nouvelles passes
(scénarios options, vol cone, heatmaps, gauges…).

### MINI-BILAN tournée 91-95

5 lots, 36 tests, suite 1771 → 1807, **1 défaut réel de moteur corrigé**
(committee : fenêtre « DANS LA ZONE D'ACHAT » = code mort → s'ouvre
enfin), skyler_core jamais touché : decide figé (9) · committee défaut
réel + 9 · pivots figé (8) · contrat POST figé (4) · filtres durs
options figés (6).

### MINI-BILAN tournée 86-90 — « moteurs blindés » COMPLET

5 lots, 46 caractérisations nées vertes, suite 1725 → 1771, 0 ligne de
logique modifiée, fichiers runtime jamais touchés. Toute la chaîne
« données → preuves (evidence) → décision (stack) → affichage
(recommendation/__VXVOCAB) → auto-notation (track_record) → persistance
(persist) → états (connections) » est figée par la suite : tout
changement futur de sémantique cassera les tests.

### MINI-BILAN tournée 81-85

Polices auto-hébergées (0 requête externe prouvé) · offline RÉEL
corrigé (défaut MAJEUR : le shell canonique n'enregistrait jamais le
service worker) · 26 contrôles interactifs 0 inerte · cycle desk 6/6
sans perte possible · alertes+SSE 4/4 sains. Suite 1714 → 1725,
SW v125 → v127, 4 outils d'audit rejouables versionnés dans tools/.

## Index des lots

Voir `docs/refactor/validation/SKYLER-INDEX.md` — tableau complet 10 → 23.

## Programme Institutional+ — TERMINÉ (RC sur intégration)

Les 12 lots + audit sont livrés sur `integration/vertex-skyler-v2`.
Verdict RC : **GO AVEC RÉSERVES** — voir `SKYLER-LOT-12.md` §11.

## Prochaine action unique

Validation humaine de la RC sur appareil physique (TWS réel, pages, iPhone).
Ensuite, avec accord explicite UNIQUEMENT, merge `integration/vertex-skyler-v2`
→ `main`.

**Arrêt — validation humaine requise.**
