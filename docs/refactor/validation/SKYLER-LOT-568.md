# SKYLER LOT 568 — septième et dernier chiffre lourd : **103 est un cumul par page — 91 états distincts** — les douze doublons sont **tous dans le seau que le 541 n'a pas lu**, et **le piège que j'avais écrit d'avance était faux**

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-568` (base : lot 567 fusionné,
`b10b4fcf`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé. Aucune route appelée** — le corpus
des 8 pages était déjà sur disque depuis le 541.

## Le choix

**(nn)** — le dernier des sept chiffres lourds : les **103 états du 541**. Après
lui, la liste ouverte au 562 est close. Ce n'est pas une victoire ; c'est une
liste qui se termine.

## Reproduction (556-B)

`l541_ast.json` porte `appels` — page, fichier, forme, texte, mots, action —
**mais pas la position**, comme le 539 (563-A). Un banc neuf relit
`l541_corpus.json` avec le **même prédicat**, mot pour mot, et ajoute `pos`.
`l541_ast.js` n'est pas touché : c'est une preuve.

```text
CALIB 1 · REPRODUCTION  103 = 28 `error` + 75 `empty` · 105 programmes
          · 0 erreur · causes 8 / 17 / 1 / 2 = 28
          · 15 littérales de 3 mots ou moins                        OK
CALIB 2 · POSITIF       le témoin « Registre indisponible : » ressort
                        bien en forme « construite »                OK
CALIB 3 · NÉGATIF       une signature FABRIQUÉE                     OK
```

## Le premier constat — **103 est un cumul par page ; les états distincts sont 91**

```text
entrées (page, fichier, position) — publié      103
signatures distinctes                            91
   signatures vues sur plus d'une page            6
   unités en double                              12
   signatures dans un fichier `/static/**`       17
   signatures dans un script inline              74
```

Six signatures partagées, dont une seule sur les 8 pages :

```text
vx-shell.js                  pos 14190   8 pages   « Aucune notification pour le moment »
option-iv-sensitivity.js     pos   342   2 pages   « Sensibilité IV indisponible. »
option-payoff.js             pos  1440   2 pages   « Contrat incomplet — payoff non traçable »
option-scenarios.js          pos   400   2 pages   « Simulation moteur indisponible… »
option-theta.js              pos   478   2 pages   « Décomposition temps indisponible. »
timeline-chart.js            pos  1321   2 pages   « Aucun événement à venir. »
```

**103 − 12 = 91.** C'est le plus faible taux de duplication des sept : les états
d'échec sont écrits page par page, pas mutualisés.

**Publiés puis corrigés : 32 → 33 (+1).**

## Le second — **les douze doublons sont tous dans le seau non lu**

```text
                      publié   distinct
`VX.states.error`         28         28
`VX.states.empty`         75         63
feuille distincte : 28 + 63 = 91
```

Le 541 a lu ses **28 erreurs une par une** — formes, mots, préfixes. Il n'a pas
lu les 75 `empty`. **Les 28 sont exacts au marquage près ; les 12 doublons sont
intégralement dans les 75.**

C'est le même motif qu'au 565, où les 28 doublons des atténuations tombaient tous
dans le seul seau jamais ouvert. **Deux fois n'est pas une loi** — c'est une
observation mesurée deux fois, et 563-C interdit d'en faire une règle générale.

## L'arrêt du lot — **le piège que j'avais écrit d'avance était faux**

Avant de mesurer, j'avais écrit : « le titre du 541 dit *103 états, dont 28
erreurs, huit disent le POURQUOI, quinze ne disent que le QUOI* ; 8 + 15 = 23 et
28 − 23 = 5 ; **ce 5 n'est pas un troisième objet** — le 15 est un sous-ensemble
filtré des 18 littérales. »

La mesure dit autre chose :

```text
construites (le « huit »)                        8
littérales de 3 mots ou moins (le « quinze »)   15
littérales + repli littéral                     18
   les 15 sont-ils INCLUS dans les 18          OUI
   recouvrement entre les 15 et les 8          ZÉRO
littérales de PLUS de 3 mots                     3
non lisibles                                     2
                                               ───
8 + 15 + 3 + 2 = 28
```

**Le 5 existe bien** : c'est 3 littérales longues + 2 non lisibles. Ma prédiction
était fausse sur ce point. Mais ce que la mesure établit est plus utile que ce
que j'attendais : **le 5 est arithmétiquement le complément, et sémantiquement
une fusion.** Il colle ensemble deux catégories que le 541 sépare
*délibérément* — les non lisibles sont « comptées à part, jamais rangées parmi
les pauvres », c'est un arrêt que ce rapport avait fait au nom de la règle 481.
Publier « 5 » aurait défait cet arrêt.

**Arrêtés avant publication : 193 → 194 (+1).**

## Second contrôle (481) — ce que la restriction laisse dehors

Le 541 ne compte que `VX.states.error` et `VX.states.empty`. Mesuré,
structurellement :

```text
clauses `catch` du corpus (cumul)                539
   dont aucun appel `X.states.*` dans le corps   522
   dont corps littéralement vide (cumul)         369
en signatures distinctes
   `catch` sans `states`                         123
   dont corps vide                                82
```

**Ce seau ne s'appelle pas « échecs silencieux »** (550-B). Un `catch` peut
journaliser, réessayer, ou remplir le DOM autrement ; le nommer d'après ce qu'il
fait demanderait de le lire un par un, ce que ce lot ne fait pas. Il s'appelle ce
qu'il est : **des clauses `catch` qui ne passent par aucun état du vocabulaire
mesuré**, et elles sont **123 distinctes, dont 82 au corps vide**.

Une coïncidence à ne pas lire comme un lien (565-C) : le corpus contient **539**
clauses `catch`, et il existe un **lot 539**. Aucun rapport.

## Ce que le dépôt fait bien, mesuré

- **Le plus faible taux de duplication des sept chiffres** : 12 doublons sur 103,
  contre 28 sur 112 et 77 sur 156. Les états d'échec sont écrits au plus près de
  leur page.
- **Les 28 erreurs sont exactes** — le seau que le 541 a lu une par une ne bouge
  pas d'une unité.
- **Le témoin se reproduit** : « Registre indisponible : » + message réel reste
  la forme la plus riche, trente lots plus tard.
- **La feuille du 541 s'additionne toujours**, y compris en distinct :
  28 + 63 = 91.

## Portée — ce que ce lot NE dit PAS

- **Rien n'est corrigé dans le 541** : la correction est **en ajout**.
- **Les 123 `catch` ne sont pas jugés** — ni lus, ni classés. Le lot les compte.
- Les 63 `empty` distincts restent non lus un par un, comme les 75 l'étaient.
- La signature est (fichier, position) : deux fichiers statiques identiques
  servis sous deux URL seraient comptés deux fois.

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
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier. **Les sept chiffres lourds sont reproduits et qualifiés.**

```text
« 178 appels »            (534)  →  94 sites distincts      cumul par page
« 25 fonctions »          (537)  →  18 distinctes           cumul par page
« 11 limites »            (538)  →   4 distinctes           cumul par page
« 112 atténuations »      (539)  →  84 distinctes           cumul par page
« 156 variables »         (540)  →  79 distinctes           cumul par page
« 53 refus »              (542)  →  42 distincts            cumul par RÈGLE
« 103 états »             (541)  →  91 distincts            cumul par page
```

**Sept reproductions exactes, sept chiffres qui rétrécissent, zéro conclusion
renversée.** Aucun des sept rapports d'origine ne précisait ce que son nombre
comptait, et aucun des sept ne se trompait sur ce qu'il affirmait. C'est la seule
synthèse honnête : les mesures étaient bonnes, les unités n'étaient pas dites.

Ce que je retiens de ce lot en particulier : **le piège écrit avant la mesure
était faux, et l'écrire a quand même servi.** Il m'a fait aller vérifier le
recouvrement, et c'est en le vérifiant que j'ai trouvé mieux que ce que je
cherchais — non pas « ce 5 n'existe pas », mais « ce 5 fusionne deux catégories
qu'un arrêt précédent avait séparées exprès ». Un garde-fou n'a pas besoin
d'avoir raison pour être utile ; il a besoin d'être vérifié comme le reste.

Trois règles neuves :

- **568-A · UNE DIFFÉRENCE PEUT ÊTRE ARITHMÉTIQUEMENT JUSTE ET SÉMANTIQUEMENT
  FAUSSE** — 28 − 8 − 15 = 5, et ce 5 est bien le reste ; mais il colle ensemble
  3 littérales longues et 2 non lisibles, que le rapport séparait volontairement.
- **568-B · LE PIÈGE ÉCRIT AVANT LA MESURE SE VÉRIFIE COMME LE RESTE** — il
  protège de la surprise, pas de l'erreur ; le mien était faux et a tout de même
  conduit au bon endroit.
- **568-C · LE MÊME MOTIF DEUX FOIS N'EST PAS UNE LOI** — les doublons dans le
  seau non lu, au 565 puis au 568 : deux mesures, pas une règle.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **les 123 clauses `catch` sans état mesuré, dont 82 au
corps vide** ; **les 63 `empty` distincts, jamais lus un par un** ; **les 42
refus, jamais relus un par un** ; **les 4 refus non-JSON du 542** ; **les 74
variables serveur sans aucune atténuation** ; **les 67 atténuations non
affichées** ; **les 25 atténuations de la bibliothèque tierce** ;
**`/options|chips`, douzième limite jamais levée ni nommée** ; **`renderCalendar`,
exécutée hors périmètre au 537** ; **les 4 limites distinctes du 564** ; **les 12
signatures partagées du 562** ; **les 5 cas de réponse absents du corpus du
561** ; **les 8 unités encore ambiguës** ; **les 10 cas non tranchés du 559** ;
**les 16 sous-clés du 558, dont 12 sur des routes au contrat non mesuré** ; **les
5 chaînes nues** ; **les 10 chaînes ambiguës** ; **les 35 clés du contrat non
gardé** ; **les 28 candidates** ; **les 6 clés sans lecture observée** ; **les 26
routes à lectures ambiguës** ; **les 4 collisions de nom** ; **les 3 ombres de
`briefing.py`** ; **les 5 routes affamées du 556** ; **les 14 candidates du 554,
en attente d'un GO** ; **les 4 routes construites `/api/options/…` et les 3
préfixes illisibles** ; **`/api/ticker/`, hors corpus** ; **les 7 routes sans
filet du 554/555** ; **les 128 clés servies non nommées du 552** ;
**`/api/weekly` rend un objet vide en DÉMO** ; **les 6 points d'entrée du 551** ;
**les 15 points d'entrée au statut seul du 550** ; **les 43 points d'entrée
couverts par personne** ; **les 11 identifiants de `/intelligence`, `/tracking`
et `pf-risk-gauge`** ; **les 4 zones sous attente du 545** ; **le contrat d'ÉCHEC
serveur, jamais observé** ; **les 4 noms de clé du 542** ; **les 15 messages
d'erreur du 541** ; **`initSettings`** ; **les 8 appels hors de toute fonction** ;
**les 36 accès DOM non suivis** ; **la définition du corpus de routes du
511-A** ; **l'ampleur du 518-A** ; **les 42 cas indéterminés du 528** ; **les 25
rangs fragiles** ; **les 33 identifiants reconstruits** ; **les 92 rapports non
additionnés du 526** ; **les quinze lots exposés du 525** ; **le « 7 barèmes » du
491** ; **mesurer les 23 routes — outil prêt, en attente d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 194 (+1)** ;
**publiés puis corrigés 33 (+1)** ; interprétations retirées **10**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
