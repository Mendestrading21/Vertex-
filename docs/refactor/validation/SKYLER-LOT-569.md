# SKYLER LOT 569 — les 123 clauses `catch` du 568, enfin lues : **41 font quelque chose, 13 signalent l'échec par un canal que le 541 ne connaissait pas** — et **le piège que j'avais écrit généralisait à partir d'un seul témoin**

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-569` (base : lot 568 fusionné,
`918600cd`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé. Aucune route appelée** — le corpus
des 8 pages était déjà sur disque.

## Le choix

**(oo)** — la liste des sept chiffres lourds est close ; il fallait un objet
neuf, et le 568 venait d'en produire un **en second contrôle, sans en lire une
seule ligne** : 123 clauses `catch` distinctes ne passent par aucun état du
vocabulaire mesuré, dont 82 au corps vide.

C'est l'invariant produit le plus fort du dépôt — « donnée absente → état
honnête » — pris par son angle mort : **ce que fait le code quand il attrape une
erreur sans afficher d'état.**

## Reproduction (556-B)

```text
CALIB 1 · REPRODUCTION  539 clauses en cumul · 522 sans `states`
          · 369 vides · 123 distinctes · 82 vides distinctes       OK
CALIB 2 · POSITIF       les deux témoins LUS dans le code servi :
          `vx-entities.js:27` `catch (e) { return fallback; }` → **repli**
          `vx-entities.js:30` `catch (e) {}`                   → **vide**   OK
CALIB 3 · NÉGATIF       aucune clause à `states` dans le corpus des 123  OK
```

## Le premier constat — **ce que font les 123**

Classement **structurel**, par une priorité écrite avant la mesure — jamais par
une liste de mots (521-B) :

```text
vide            82
repli           21     `return null` · `return []` · `return fallback` · `favs=[]`
appelle         10     `VX.toast(…)` · `emptyCard(…)` · `fallbackPolling()` · `hard(href)`
ecrit-dom        7     bannière `vx-error-banner`, `vx-insight`, ou `innerHTML=''`
relance          1     `if (e.name === 'AbortError') throw e`
journalise       1     `console.error('[vx-refresh]', label, e)`
autre            1     `continue`
               ───
               123
```

**Quarante et une clauses sur 123 font quelque chose**, et vingt et une rendent
une **valeur de repli explicite**.

## Le second — **« sans état mesuré » n'est pas « sans état »**

```text
appellent un canal LU dans le corpus (`VX.toast`, `emptyCard`,
   `setStatus`, `setNet`)                                        7
écrivent un CONTENU dans le DOM (bannière d'erreur, encart)      5
marquent un bouton en état d'erreur (`dataset.state = 'error'`)  1
                                                               ───
signalent l'échec par un canal HORS de l'instrument du 541      13
   (distinctes, sans double compte)

écrivent une chaîne VIDE — effacement, PAS un signalement         2
```

Le 541 ne connaissait que `VX.states.error` et `VX.states.empty`. **Il existe un
second canal de signalement dans le produit** — `VX.toast(…, 'error')`,
`emptyCard(…)`, la bannière `vx-error-banner` — et **treize clauses l'utilisent**.
Le seau « sans état mesuré » du 568 était donc exact dans son nom, et il aurait
été faux dans n'importe quelle lecture plus large.

Les deux effacements (`innerHTML = ''`) sont comptés **à part** : effacer une
zone n'est pas dire ce qui manque.

## L'arrêt du lot — **mon propre piège généralisait à partir d'un témoin**

J'avais écrit, avant de mesurer : « **un `catch` vide n'est pas une faute** — il
peut garder une fonctionnalité optionnelle, témoin `vx-entities.js:30` :
`try { localStorage.setItem(…) } catch (e) {}` ». Le témoin est réel, lu dans le
fichier servi. **Mais il prouve un cas, pas quatre-vingt-deux.**

Relevé — pas deviné — de ce que les 82 gardent réellement :

```text
`try` à gestionnaire vide, distincts               82
noms appelés distincts relevés                     94

   VX.fetch                18        localStorage.getItem     8
   JSON.stringify          14        fetch                    7
   localStorage.setItem    13        Number                   6

gardes portant un accès `localStorage`             20
gardes dont le bloc n'appelle rien                  1
```

**Le motif du témoin couvre 20 des 82 — moins d'un quart.** Le premier appelé du
classement n'est pas `localStorage` mais **`VX.fetch`, dans 18 gardes**.

Publier « un `catch` vide n'est pas une faute » en tête d'un seau de 82 aurait
transformé un témoin en règle. **568-B disait que le piège se vérifie comme le
reste ; celui-ci ne s'est pas vérifié.**

**Arrêtés avant publication : 194 → 195 (+1).**

## Le troisième — **la classe est une priorité, pas une nature**

```text
porte vide 82 · retour 23 · appel 15 · dom 7 · affect 6 · throw 1 · console 1
clauses portant PLUSIEURS traits à la fois        11
```

Onze clauses auraient pu tomber dans deux seaux — une qui écrit dans le DOM
*et* rend une valeur, par exemple. **Publier les sept seaux sans les traits bruts
aurait suggéré une partition naturelle là où il n'y a qu'un ordre écrit à la
main.** Les deux sont donnés ensemble.

## Second contrôle (481) — la bibliothèque exclue

```text
clauses `catch` dans `chart.umd.min.js` (cumul)     8
signatures distinctes                               1
dont corps vide                                     1
```

**Une seule.** La même restriction avait écarté **25** atténuations au 565 ; ici
elle n'écarte presque rien. **Le coût d'une restriction dépend de ce qu'on
mesure, pas de la restriction** (563-C, encore).

## Où vivent les 82 corps vides

```text
16  /system   (inline)          9  /portfolio (inline)      3  vx-router.js
16  vx-core.js                  7  vx-entities.js           3  /markets  (inline)
11  vx-shell.js                 5  /         (inline)       3  chart-core.js
                                3  /opportunities (inline)  … 15 fichiers en tout
```

## Ce que le dépôt fait bien, mesuré

- **Un second canal d'erreur existe et sert** : toast, bannière, encart —
  treize clauses l'utilisent.
- **Vingt et une clauses rendent une valeur de repli explicite** (`null`, `[]`,
  `{}`, `fallback`) plutôt que de laisser une variable indéfinie.
- **Une seule clause se contente de `console.error`** : le produit ne prend pas
  la console pour un canal utilisateur.
- **Une seule relance**, et elle est conditionnelle (`AbortError`) — les
  annulations ne sont pas confondues avec des pannes.

## Portée — ce que ce lot NE dit PAS

- **Les 82 corps vides ne sont pas jugés.** Savoir ce qu'ils gardent n'est pas
  savoir si le silence est justifié : un `try` peut contenir bien plus que
  l'appel relevé, et `VX.fetch` dans un bloc gardé **ne prouve pas** qu'une
  panne réseau est avalée.
- **Rien n'est corrigé, rien n'est vidé, rien n'est rempli.** Aucun
  `VX.states.*` n'est ajouté.
- Le corpus reste celui du 541 — les 8 pages en DÉMO, telles qu'enregistrées.
- Les noms de canaux (`VX.toast`, `emptyCard`…) sont **lus dans les 41 clauses
  affichées**, pas devinés d'avance.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**, aucun banc tronqué avant d'avoir écrit son JSON.
- **Aucun fichier de production touché** (`git status` : seuls les documents).
  Pas de bump. SW : `td-shell-v187`.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers ; **3 modifiés par la suite de tests** (`ai_enrichment.json`, `desk_data.json`,
  `weekly_snapshot.json`), **restaurés — écart final AUCUN**, aucun fichier apparu ni disparu
- Suite : **2864 passed / 0 skipped**, lancée **après** les documents

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier. Premier lot après la clôture des sept chiffres lourds, et il a
produit exactement ce qu'un recomptage ne produit pas : **un objet du produit,
lu**.

Ce que je retiens : **mon garde-fou s'est retourné contre moi, et c'est la
meilleure chose qui pouvait arriver.** J'avais écrit « un `catch` vide n'est pas
une faute » pour m'empêcher de crier au scandale ; la phrase était juste sur son
témoin et fausse comme généralité — le motif `localStorage` couvre vingt cas sur
quatre-vingt-deux. Un garde-fou qui n'est pas mesuré devient un préjugé
rassurant, exactement symétrique de celui qu'il prévient.

Trois règles neuves :

- **569-A · UN TÉMOIN PROUVE UN CAS, PAS UNE CATÉGORIE** — `localStorage`
  couvre 20 des 82 ; le premier appelé relevé est `VX.fetch`, dans 18 gardes.
- **569-B · UNE CLASSIFICATION PAR PRIORITÉ N'EST PAS UNE PARTITION NATURELLE** —
  11 clauses portent plusieurs traits ; les seaux ne se publient qu'avec les
  traits bruts à côté.
- **569-C · « SANS ÉTAT MESURÉ » N'EST PAS « SANS ÉTAT »** — 13 clauses
  signalent l'échec par un canal que l'instrument du 541 ne connaissait pas.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **les 82 corps vides, comptés et situés mais NON
JUGÉS** ; **les 18 gardes portant un `VX.fetch`** ; **le second canal d'erreur
(`VX.toast`, `emptyCard`, `vx-error-banner`), jamais inventorié pour lui-même** ;
**les 63 `empty` distincts du 568, jamais lus un par un** ; **les 42 refus du
567** ; **les 4 refus non-JSON du 542** ; **les 74 variables serveur sans
atténuation** ; **les 67 atténuations non affichées** ; **les 25 atténuations de
la bibliothèque tierce** ; **`/options|chips`, douzième limite jamais levée ni
nommée** ; **`renderCalendar`, exécutée hors périmètre au 537** ; **les 4 limites
distinctes du 564** ; **les 12 signatures partagées du 562** ; **les 5 cas de
réponse absents du corpus du 561** ; **les 8 unités encore ambiguës** ; **les 10
cas non tranchés du 559** ; **les 16 sous-clés du 558** ; **les 5 chaînes nues** ;
**les 10 chaînes ambiguës** ; **les 35 clés du contrat non gardé** ; **les 28
candidates** ; **les 6 clés sans lecture observée** ; **les 26 routes à lectures
ambiguës** ; **les 4 collisions de nom** ; **les 3 ombres de `briefing.py`** ;
**les 5 routes affamées du 556** ; **les 14 candidates du 554, en attente d'un
GO** ; **les 4 routes construites `/api/options/…` et les 3 préfixes
illisibles** ; **`/api/ticker/`, hors corpus** ; **les 7 routes sans filet du
554/555** ; **les 128 clés servies non nommées du 552** ; **`/api/weekly` rend un
objet vide en DÉMO** ; **les 6 points d'entrée du 551** ; **les 15 points
d'entrée au statut seul du 550** ; **les 43 points d'entrée couverts par
personne** ; **les 11 identifiants de `/intelligence`, `/tracking` et
`pf-risk-gauge`** ; **les 4 zones sous attente du 545** ; **le contrat d'ÉCHEC
serveur, jamais observé** ; **les 4 noms de clé du 542** ; **les 15 messages
d'erreur du 541** ; **`initSettings`** ; **les 8 appels hors de toute fonction** ;
**les 36 accès DOM non suivis** ; **la définition du corpus de routes du
511-A** ; **l'ampleur du 518-A** ; **les 42 cas indéterminés du 528** ; **les 25
rangs fragiles** ; **les 33 identifiants reconstruits** ; **les 92 rapports non
additionnés du 526** ; **les quinze lots exposés du 525** ; **le « 7 barèmes » du
491** ; **mesurer les 23 routes — outil prêt, en attente d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 195 (+1)** ; publiés
puis corrigés **33** ; interprétations retirées **10**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
