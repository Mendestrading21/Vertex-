# SKYLER LOT 524 — La borne du 523 est levée : **62 % → 81 % des chargeurs peignent**. Les dix-sept libérés n'apportent **aucun défaut** et **une seule occasion**. Et j'ai failli créditer le résolveur d'un écart causé par ma propre charge

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-524` (base : lot 523 fusionné,
`cfb8c165`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé.**

## Le choix

**(b)** — le 523 a livré une mesure honnête mais **bornée à 62 %** : 55 chargeurs
sur 89 peignaient, **34 restaient muets**, et la cause dominante était **mienne**
— le résolveur automatique reprenait les **fonctions** voisines mais pas les
**déclarations de module**. Une réparation d'instrument petite, identifiée, à
fort rendement.

## L'extracteur de déclarations, calibré avant tout usage

Retrouver le **nom** ne suffit pas : c'est la **valeur** qui compte (**516-A**).

```text
CALIB 1 · POSITIF, VALEUR EXACTE   `SCAN_ACTION` rendue caractère pour
          caractère, identique à markets_page.py:221                    OK
CALIB 2 · NÉGATIF                  une constante FABRIQUÉE ne rend rien  OK
CALIB 3 · SYNTAXE                  5 / 5 déclarations extraites sont du
          JS valide (chargées par node sans erreur)                     OK
CALIB 4 · VARIÉTÉ                  formes distinctes retrouvées :
          chaîne ×2 · tableau ×2 · objet ×1                             OK
```

## Le gain, mesuré à charge identique

```text
                                     chargeurs qui peignent
523 — résolveur FONCTIONS seules          55 / 89      62 %
524 — FONCTIONS + DÉCLARATIONS            72 / 89      81 %
                                          +17 · aucun perdu

déclarations reprises   67 reprises · 10 noms distincts
texte peint (régime riche)   7 553 → 11 410 caractères   × 1,5
```

Les dix-sept libérées : `loadBreadth`, `loadSectors`, `loadVix`, `loadYield`,
`loadStrip`, `loadRisk`, `loadLeader`, `loadMacroKpis`, `loadMultiIndex`,
`loadSpyChart` (Marchés) · `loadDist`, `loadHypotheses`, `loadLearnings`,
`loadReal` (Journal) · `renderTiles` (Options) · `loadBrain`, `renderVault`
(Système).

## Ce que les dix-sept apportent : rien de mauvais, presque rien de mesurable

```text
défauts apportés par les 17 nouvelles parlantes        0
occasions F1 apportées par les 17                      1   (« 1 pt »)
```

- **F1 · accord numérique** : **5 occasions** en JavaScript (« 1 titre »,
  « 1 PUT » ×2, « 1 pt », « 1 erreur ») **+ 1 côté serveur** (« 1 Fondamental »).
  **Six occasions, six accords justes.** Une de plus qu'au 523. **C'est toujours
  une preuve mince**, et l'élargissement de 62 % à 81 % ne l'a presque pas
  épaissie : le français à compteur est **rare** dans ce produit.
- **F2 · fuite technique** : exactement les **trois mêmes fonctions** qu'au 523,
  **déjà réfutées comme artefacts de ma charge**. Reproduites à l'identique,
  **aucune nouvelle**.

## L'arrêt du lot : j'ai failli créditer le résolveur d'un écart qui venait de moi

En recopiant la charge du 523, j'ai **perdu une clé** : l'alias `entries`. Sans
lui, `loadTrack` cessait de peindre `[object Object]` — et j'aurais annoncé que
**le résolveur avait fait disparaître un défaut**. Il n'y était pour rien.

**Deux choses changeaient à la fois. Charge réalignée, balayage refait.**
**Arrêtés avant publication : 125 → 126.**

## Second contrôle — le résolveur peut-il injecter la MAUVAISE déclaration ?

Famille **521-B**. Le résolveur prend la **première** déclaration portant le nom
cherché ; si le nom est porté plusieurs fois, il injecte un autre contexte.

```text
déclarations en début de ligne dans le JS servi des 8 pages    2 977
   dont AMBIGUËS (même nom, même page, plusieurs fois)           729
      `el` ×25 · `t` ×14 · `col` ×13 · `g` ×13 …
noms RÉELLEMENT repris par le résolveur                           10
   dont ambigus                                                    0
```

**Le risque est réel et chiffré ; il ne s'est pas réalisé.** Les dix noms pris
sont tous distinctifs (`SCAN_ACTION`, `IDX_MAIN`, `MACRO_NAMES`, `BRAIN_TONE`,
`JOURNAL_ACTION`, `TV_BULL2`, `TV_BEAR2`, `_board`, `money`,
`vaultTypeFilter`) et **chacun est unique dans sa page**. Le résolveur n'est
piloté par **aucune liste de noms** : il ne reprend que ce que l'exécution
réclame (**521-B respectée**).

Une précision honnête : mon motif accepte une indentation, donc les 2 977
comptées ne sont **pas toutes « de premier niveau »** — les `el`, `t`, `g` sont
des déclarations **internes à des fonctions**. Parler de « déclarations de
module » aurait été faux.

## Troisième contrôle — le résidu a changé de propriétaire

Dix-sept chargeurs restent muets. **La cause n'est plus le résolveur.**

```text
 7  stub incomplet du HARNAIS      `VX.fetch.peek`, `(rows||[]).filter`,
                                   `rich.filter`, `keys.forEach`
 4  sortie réellement VIDE         loadCalendar · loadMacroCal ·
                                   loadBreadthInternals · renderFunnel
 4  forme de MA charge             renderDiff · renderScenarios ·
                                   renderPayoff · loadContinuity
 2  symbole NON résolu             `PARAMS`, sur /opportunities
```

**Les deux derniers ont une cause précise** : `PARAMS` est déclarée en **seconde
instruction d'une ligne** — `const VIEW=…;const PARAMS=…;` — et mon motif exige
un **début de ligne**. Borne connue, nommée, non levée.

**La dette du résolveur est donc quasi soldée** : sur les 34 muets du 523, **17
parlent, 2 relèvent encore du résolveur, et 15 relèvent de ma charge ou de mes
stubs**.

## Les quatre chargeurs silencieux — vérifiés durement, aucun dossier

Quatre chargeurs ne peignent rien **sans lever**. Deux comportements opposés du
point de vue produit : **masquer** le conteneur (honnête) ou **retourner en
silence** (le conteneur garde ce qu'il avait).

```text
CALIB · loadBreadthInternals → MASQUE le conteneur   (réponse connue)  OK
CALIB · renderFunnel         → RETOUR SEC            (réponse connue)  OK

/               loadCalendar           RETOUR SEC
/markets        loadMacroCal           RETOUR SEC
/markets        loadBreadthInternals   MASQUE le conteneur
/opportunities  renderFunnel           RETOUR SEC
```

Trois retours secs : c'est le candidat le plus désirable du lot, donc celui à
vérifier le plus durement (**520-B**). **Vérifié, il tombe.**

- `/api/opportunities/funnel` — **route sûre, appelée** — rend **7 étages** et
  une clé **`zero_actionable_is_valid`** : le cas zéro est **explicitement
  traité par le moteur**. Le retour sec n'est pas atteint.
- Le conteneur `vx-calendar` est servi **vide, sans squelette**. Un retour
  silencieux laisserait donc une zone vide, **pas une barre de chargement
  éternelle**.

**Aucun dossier.** Le risque existe si une route se dégrade ; l'établir
demanderait de forcer des dégradations que je ne force pas. **Candidat nommé,
non promu.**

## Ce que le dépôt fait bien, mesuré

- **`loadBreadthInternals` masque sa carte** au lieu de laisser un rectangle
  vide — exactement la bonne réponse à une donnée absente.
- Le moteur du funnel porte un drapeau **`zero_actionable_is_valid`** : « zéro
  opportunité » est un **cas pensé**, pas un oubli.
- **72 chargeurs s'exécutent jusqu'au bout** sous trois régimes sans casser, et
  les dix-sept nouveaux venus n'introduisent **aucun défaut de langue**.

## Portée — ce que ce lot NE dit PAS

- **19 % des chargeurs restent muets.** Leur français n'est pas mesuré.
- **F1 n'a que six occasions au total.** Conclure « le produit accorde juste »
  reste une extrapolation de tirage (**516-C**).
- **Deux familles seulement** : genre, registre, typographie, anglicismes ne
  sont pas mesurés — et un anglicisme n'est pas un défaut par principe
  (**515-C**).
- Les charges restent **fabriquées** ; les trois F2 le rappellent.
- **Aucun navigateur, aucun POST, aucune route interdite.** Une seule route
  appelée, `/api/opportunities/funnel`, de la liste sûre.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**.
- **Aucun fichier de production touché** (`git diff --stat` : AUCUN). Pas de
  bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** avant tout import, dans les quatre bancs.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0**.

Aucun dossier. Une borne annoncée au lot précédent est **levée et re-bornée** —
c'est la règle **517-C** appliquée à mon propre outil. Le résultat le plus utile
n'est pas le gain de couverture : c'est que **l'élargissement n'a rien trouvé**.
Quand on ouvre 19 points de couverture et qu'aucun défaut n'apparaît, la
probabilité que le français peint soit sain monte — sans être démontrée.

Quatre règles neuves :

- **524-A · QUAND ON COMPARE DEUX PASSAGES, UNE SEULE CHOSE DOIT CHANGER** —
  une clé perdue en recopiant, et le mérite change de propriétaire.
- **524-B · UN RISQUE QUANTIFIÉ N'EST PAS UN RISQUE RÉALISÉ** — 729 noms
  ambigus, zéro parmi les dix effectivement repris ; mesurer les deux.
- **524-C · MESURER LE RÉSIDU PAR CAUSE, PAS PAR NOMBRE** — « 17 muets » ne dit
  rien ; « 2 du résolveur, 15 de ma charge » dit à qui est la dette.
- **524-D · UN `id` TROUVÉ DANS LE HTML SERVI PEUT VIVRE DANS UN GABARIT JS** —
  vérifier qu'on lit le DOM et non une chaîne de caractères.

Feuille **inchangée : 37 dossiers · seize rang 1 · douze rang 2 · cinq rang 3 ·
cinq rang 4**.

Dettes nommées restantes : **les 17 chargeurs encore muets, ventilés par cause** ;
**les trois retours secs, candidat nommé non promu** ; **le « 7 barèmes » du 491,
non re-vérifiable sans instrument neuf** ; **mesurer les 23 routes — outil prêt,
en attente d'un GO** ; **l'assemblage entre fonctions** ; **la condition `k ≤ 5`
sur un scan réel** ; **le compte des rangs relatifs postérieurs au 480**.

Comptes séparés : résultats faux **arrêtés avant publication 126 (+1)** ; publiés
puis corrigés **17** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. Et la question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ?**
