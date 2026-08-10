# SKYLER LOT 534 — **Un vrai analyseur JavaScript existait déjà dans la machine.** Il voit 178 appels là où mes comptages en voyaient 120 — et sur les 28 « non protégés » du 533, **quatre étaient faux**. Le dossier 531-A, lui, ne bouge pas d'un chargeur

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-534` (base : lot 533 fusionné,
`a61ddd0d`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé.**

## Le choix

**(v)** — changer de registre. Neuf arrêts en trois lots (531, 532, 533) sur la
**même** famille : collisions de noms et cribles textuels trop larges. Élargir
une dixième expression régulière, c'était refaire la faute une quatrième fois.

**acorn 8.15.0 est EMBARQUÉ dans Node 22** — c'est le parseur que Node utilise
pour lui-même, atteignable par `--expose-internals`. **Rien à installer.**

```text
/opt/node22/bin/node --expose-internals -e "require('internal/deps/acorn/…')"
   -> ACORN OK  8.15.0
113 programmes analysés · 3 345 728 octets · ÉCHECS D'ANALYSE : 0
```

## Six témoins — dont deux où le comptage d'accolades se trompe

```text
                                                    ANALYSEUR   ACCOLADES
t1 POSITIF     appel hors try                       non prot.   non prot.  OK
t2 NÉGATIF     appel dans un try                    try         protégé    OK
t3 DISCRIMINANT `try` en commentaire ET en chaîne    non prot.   protégé    OK
t4 RESTRICTION appel construit (`w['fe'+'tch']`)     invisible   invisible  OK
t5 RESTRICTION clôture imbriquée dans un try         non prot.   protégé    OK
t6 DISCRIMINANT homonyme `get` = `localStorage`      aucun appel non prot.  OK
```

**t3 et t5 sont deux classes de faux « protégé »** du comptage d'accolades : un
`try` en commentaire, et un `try` qui n'entoure que la *pose* d'une clôture, pas
son exécution. **t4 nomme ce que l'analyseur ne voit pas** — un appel dont le nom
est fabriqué à l'exécution. Limite nommée, pas cachée.

Sur le produit, les deux témoins imposés :

```text
POSITIF   /opportunities renderRadar     1 appel · protection : AUCUNE     OK
NÉGATIF   /opportunities renderCalendar  1 appel · protection : try        OK
```

## Trois arrêts — dont la faute 532-A refaite **à l'intérieur du parseur**

**1. Mon premier témoin `t5` attendait la mauvaise attribution.** L'analyseur
rangeait l'appel d'une clôture anonyme sous « (anonyme) », et le chargeur
disparaissait. J'ai séparé deux notions qui n'en faisaient qu'une :
**propriétaire** (la fonction qui contient directement l'appel — c'est elle qui
décide de la protection, car une frontière de fonction coupe un `try`) et
**porteur** (la première fonction *nommée* en remontant — c'est elle qu'on
attribue à un chargeur).

**2. Ma règle de helper ratait `VX.fetch`.** J'exigeais un `return` contenant
l'appel ; or `VX.fetch` fait son `fetch` dans une flèche anonyme interne et
retourne une promesse. **Les deux témoins produit imposés ont échoué** — c'est
exactement à ça qu'ils servent. Règle corrigée : *le résultat du `fetch` n'est
pas jeté dans un `ExpressionStatement`*, ce qui écarte proprement `reportError`,
`vaultSet` et `wireCopilot` (qui **postent** un journal).

**3. Un vrai parseur ne résout pas les portées tout seul — et j'ai refait la
faute 532-A avec lui.** Premier jet : je cherchais les helpers **par nom**, sur
tout le dépôt. Résultat : **104 appels de `get(`** comptés, alors que `get` n'est
un helper que sur `/options` ; ailleurs c'est une lecture de `localStorage`.
acorn donne l'**arbre**, pas les **liaisons** : il a fallu construire la table
des portées et résoudre chaque identifiant.

**Arrêtés avant publication : 143 → 146.**

## La mesure, à corpus IDENTIQUE

Le crible du 533 est ré-exécuté **dans le même processus**, sur les **mêmes
octets** : la comparaison ne repose sur aucun chiffre recopié (**524-A**).

```text
                                  A · accolades+regex   B · acorn
   fonctions appelant un helper          102               130
   appels au total                       120               178
   appels NON PROTÉGÉS                    28                51
   fonctions NON PROTÉGÉES                22                33
   REPRODUCTION DU 533                    OK
```

**Le crible du 533 voyait environ deux tiers de ce que voit un analyseur.**

## La feuille des écarts — 71 divergences, 5 causes, **0 inexpliqué**

```text
FORME INVISIBLE AU CRIBLE · flèche / affectation / méthode        32
FORME INVISIBLE AU CRIBLE · appel hors de toute fonction           8
ATTRIBUTION · B donne l'appel à une fermeture nommée interne      16
ATTRIBUTION · A compte AUSSI les appels des fermetures internes    5
FENÊTRE DE 400 CARACTÈRES · le `.catch(` est plus loin             4
HELPER INCONNU DE A · trouvé par point fixe                        5
A le voit, B le classe HELPER (récupération écrite en ligne)       1
                                                            TOTAL 71
                                              à expliquer (17+45+9) 71
```

Une feuille qui s'additionne (**526-A**), et **aucun reste**.

## La correction : **quatre des 28 « non protégés » du 533 étaient faux**

Le 533 déclarait un appel protégé si `.catch(` apparaissait dans les **400
caractères** qui suivent. Une fenêtre fixe n'est pas une portée. Distances
réelles, mesurées :

```text
loadOverview      `.catch(` à   914 caractères de l'appel   PROTÉGÉ
loadScenarios     `.catch(` à 3 976                          PROTÉGÉ
loadStrategies    `.catch(` à 4 081                          PROTÉGÉ
renderVolCharts   `.catch(` à   443                          PROTÉGÉ
```

**Ces quatre chargeurs d'`/options` sont protégés ; le 533 les comptait nus.**

**Publiés puis corrigés : 21 → 22.**

## Le produit : l'analyseur accuse **dix** chargeurs — l'exécution en disculpe quatre

```text
SQUELETTES PERPÉTUELS POTENTIELS (analyseur)   10   (533, aux accolades : 6)
   dont NOUVEAUX                                3   tous sur /portfolio
   cas du 533 que l'analyseur ne retient pas    0
```

**Un risque quantifié n'est pas un risque réalisé** (**524-B**). Les six
chargeurs de `/portfolio` ont donc été **exécutés** en régime d'échec, avec les
deux témoins habituels :

```text
CALIB 1 · POSITIF   renderAnomalies (muet, confirmé aux 531/532)   0 car.  OK
CALIB 2 · NÉGATIF   renderCalendar  (protégé)                     50 car.  OK

/portfolio   renderSynthese      2 conteneurs   221 caractères
/portfolio   renderPositions     2               61
/portfolio   renderPerformance   6              569
/portfolio   renderOptions       2              147
/portfolio   renderRisk          1              125
/portfolio   renderWatchlist     1              340
```

**Les quatre accusés de `/portfolio` peignent tous.** Ils appellent
`quotesFor(...)` sans protection — mais leur code écrit **avant** l'appel
fragile, exactement comme `loadConnections` et `loadData` au 532.

**Le dossier 531-A garde donc EXACTEMENT son ampleur : quatre chargeurs, tous sur
`/opportunities`.** C'est la **troisième** mesure indépendante qui le borne là —
et la première faite avec un vrai analyseur.

## Ce que le dépôt fait bien, mesuré

- **3,3 Mo de JavaScript servi, 113 programmes, zéro erreur de syntaxe.** Aucun
  script servi n'est cassé.
- **La couche d'accès aux données reste concentrée** : sur 178 appels, l'immense
  majorité passe par `VX.fetch`, `rawFetch`, `pull` et `get`.
- **Quatre chargeurs d'`/options` que je croyais nus sont protégés** — le produit
  était **meilleur** que ce que mon instrument en disait.
- **Sur les six chargeurs de `/portfolio` non protégés, six peignent.** La page
  ne ment pas sur son état.

## Portée — ce que ce lot NE dit PAS

- **L'analyseur est statique.** Un appel dont le nom est construit à l'exécution
  lui échappe (témoin t4). **Il ne remplace pas l'exécution** — c'est d'ailleurs
  l'exécution, pas lui, qui a tranché les quatre accusés de `/portfolio`.
- **Il ne modélise pas les portées de bloc** (`let`/`const` dans un `if`) : il
  approxime par la portée de fonction.
- **51 appels non protégés ne sont pas 51 défauts** : la plupart écrivent dans
  des zones sans squelette, ou peignent avant l'appel.
- **Rien n'a été installé.** acorn était déjà dans Node.
- **Aucun navigateur, aucun réseau** : `VX.fetch` stubé, `globalThis.fetch` lève.
- **Aucune correction engagée**, ni sur 531-A, ni sur le mot du 519, ni ailleurs.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**.
- **Aucun fichier de production touché** (`git diff --stat` sur `vertex/`,
  `terminal.py`, `tests/` : AUCUN). Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** ; harnais d'exécution pris dans
  `l523_balayage.py` (**531-B**) et contrôlé non vide.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les documents.

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 3, 0, 0, 0**.

Aucun dossier. Le lot fait trois choses : il **remplace l'instrument** par un
vrai analyseur, sans rien installer ; il **corrige quatre chiffres publiés au
533** ; et il **confirme une troisième fois** que 531-A ne dépasse pas
`/opportunities`.

Ce qu'il faut dire sans le maquiller : **le changement d'instrument n'a pas
supprimé la faute — il l'a déplacée.** J'ai refait la 532-A *à l'intérieur du
parseur*, en cherchant les helpers par nom. Un meilleur outil ne dispense pas de
la discipline ; il rend seulement l'erreur mesurable.

Trois règles neuves :

- **534-A · UN PARSEUR DONNE UN ARBRE, PAS DES LIAISONS** — sans table des
  portées, un vrai analyseur refait la faute du crible textuel : 104 appels de
  `get(` comptés à tort.
- **534-B · UNE FENÊTRE FIXE N'EST PAS UNE PORTÉE** — les 400 caractères du 533
  ont produit quatre faux « non protégés » ; le `.catch(` de `loadStrategies` est
  à 4 081 caractères.
- **534-C · ATTRIBUER UN APPEL À TOUTE FONCTION QUI LE CONTIENT TEXTUELLEMENT,
  C'EST LE COMPTER PLUSIEURS FOIS** — 21 des 71 écarts viennent de là.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**, inchangée après trois
mesures indépendantes).

Dettes nommées restantes : **`loadLeaps`** ; **`loadStructure` et ses 7
caractères** ; **la définition du corpus de routes du 511-A** ; **l'ampleur du
518-A** ; **les 42 cas indéterminés du 528** ; **les 25 rangs fragiles** ; **les
33 identifiants reconstruits** ; **les 92 rapports non additionnés du 526** ;
**les quinze lots exposés du 525** ; **le « 7 barèmes » du 491** ; **mesurer les
23 routes — outil prêt, en attente d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 146 (+3)** ;
**publiés puis corrigés 22 (+1)** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
