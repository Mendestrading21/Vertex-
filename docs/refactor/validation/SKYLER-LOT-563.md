# SKYLER LOT 563 — deuxième chiffre lourd : **25 se reproduit**, c'est un cumul par page — **18 fonctions distinctes** — et le banc du 537 avait exécuté **une fonction hors de son propre périmètre**

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-563` (base : lot 562 fusionné,
`15b9e514`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé. Aucune route appelée** — tout est
relu sur disque.

## Le choix

**(ii)** — deuxième des sept chiffres lourds, même méthode qu'au 562 : la bonne
question n'est pas « le nombre est-il faux ? » mais **« que désigne-t-il
exactement ? »**. Cible : les **25 fonctions exécutées du 537**.

## Vérifié à la source (559-A) — les bancs existent

`l537_execution.py/.json`, `l537_arite.py/.json`, `_l537_run.js`, `_l537b_run.js`
sont tous conservés. **Reproduction, pas reconstruction.**

`SKYLER-LOT-537.md:63-65` publie : « Les 33 entrées du 534 se répartissent
d'abord en **8 appels hors de toute fonction** et **25 fonctions nommées** »,
puis la feuille **9 peignent + 4 muettes + 12 limites = 25, FEUILLE : OK**.

`l537_execution.json` porte la répartition d'**avant** le second banc —
**8 + 6 + 11 = 25** — celle du rapport étant d'**après** (`loadLeaps` disculpé,
`chips` expliqué par ses arguments). **La feuille s'additionne dans les deux
états.** Reproduction du 534 : **33 couples non protégés, exactement.**

## Le premier constat — **une fonction exécutée hors du périmètre**

```text
couples NON PROTÉGÉS au 534                    33
entrées exécutées au 537 (res + programme)     34
   exécutées sans être non protégées            1   /opportunities|renderCalendar
   présentes dans `res` mais dans AUCUN seau    1   /opportunities|renderCalendar
```

`renderCalendar` a été **exécutée par le banc du 537** alors qu'elle ne figurait
pas parmi les 33 couples non protégés, et elle n'est classée dans aucun des
trois seaux. **Le 25 publié reste juste** — la feuille ne compte que les trois
seaux. Mais **une fonction a été exécutée hors du périmètre du lot, et personne
ne l'a dit.**

## Le second — **25 est un cumul par page ; les fonctions distinctes sont 18**

```text
couples (page, fonction) — le chiffre publié   25
signatures (fonction, position) distinctes     18
   signatures vues sur plus d'une page          1
   unités en double                             7
   couples sans position retrouvée              0
```

Une seule fonction est réellement partagée : **`navigate`, position 8160, sur
les 8 pages** — sept unités en double à elle seule. **25 − 7 = 18.**

Le contraste avec le 562 mérite d'être noté : là-bas, 12 signatures partagées
faisaient tomber 178 à 94 ; ici, **une seule** fait tomber 25 à 18. Le même
défaut de lecture, des ampleurs très différentes — **on ne peut pas en déduire
l'un depuis l'autre** (560-A).

**Interprétations retirées : 6 → 7 (+1).**

## L'arrêt du lot — **grouper par nom aurait fusionné deux homonymes**

```text
noms portant PLUSIEURS positions distinctes     2
   boot            2 positions différentes
   renderOptions   2 positions différentes
```

`boot` existe sur `/` et `/markets`, `renderOptions` sur `/opportunities` et
`/portfolio` — **à des positions différentes : ce sont des homonymes, pas des
fonctions partagées.** Grouper par nom aurait donné **17** au lieu de 18, et
aurait affirmé un partage là où il n'y en a pas. C'est exactement le 559-B :
**le lieu fait la mesure, pas le nom.**

**Arrêtés avant publication : 188 → 189 (+1).**

## Ce que le dépôt fait bien, mesuré

- **La feuille du 537 s'additionne dans ses deux états** — avant et après la
  correction du second banc, 25 des deux côtés.
- **Zéro couple sans position retrouvée** : les 25 se rattachent tous à une
  entrée du 534, vingt-six lots plus tard.
- **Une seule fonction partagée sur 25** : le JavaScript des pages est
  très majoritairement spécifique à sa page.

## Second contrôle (481) — ce que ce lot ne décide pas

- La position vient du 534 : **deux fonctions réellement distinctes qui
  partageraient nom ET position seraient fusionnées.** Le cas n'est pas exclu
  par construction.
- **Le sort de `renderCalendar` n'est pas arbitré** : pourquoi le banc du 537
  l'a exécutée reste à établir, et **rien n'est corrigé**.
- **Cinq chiffres lourds restent** : 112 atténuations, 103 états, 53 refus,
  156 variables serveur, 11 limites levées.

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
0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier. **Deux chiffres lourds sur sept sont désormais reproduits et
qualifiés** — et les deux étaient des cumuls par page, ce qu'aucun des deux
rapports d'origine ne précisait.

Ce qui mérite d'être dit franchement : **la méthode du 562 a marché, mais elle
aurait donné un chiffre faux si je l'avais appliquée mécaniquement.** Grouper
par nom était le geste naturel — c'est ce que fait la mémoire, pas la mesure — et
il aurait transformé deux homonymes en une fonction partagée. Il a fallu aller
chercher la position dans un JSON de vingt-six lots d'âge.

Trois règles neuves :

- **563-A · UNE MÉTHODE QUI A MARCHÉ NE SE REJOUE PAS LES YEUX FERMÉS** — le
  562 groupait par (fonction, position, helper, forme) ; ici le 537 ne fournit
  que (page, fonction), et il a fallu retourner au 534 pour la position.
- **563-B · UN BANC PEUT DÉBORDER SON PROPRE PÉRIMÈTRE EN SILENCE** —
  `renderCalendar` a été exécutée sans figurer parmi les 33, et sans apparaître
  dans aucun seau : la feuille additionnait juste, l'exécution non.
- **563-C · L'AMPLEUR D'UN DÉFAUT NE SE TRANSPOSE PAS** — 12 signatures
  partagées au 562, **une seule** ici ; le même biais, deux ordres de grandeur.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **CINQ chiffres lourds encore NON RECOMPTÉS** — 112
atténuations (539), 103 états (541), 53 refus (542), 156 variables serveur
(540), 11 limites levées (538) ; **`renderCalendar`, exécutée hors périmètre au
537** ; **les 12 signatures partagées du 562** ; **les 5 cas de réponse absents
du corpus du 561** ; **les 8 unités encore ambiguës** ; **les 10 cas non
tranchés du 559** ; **les 16 sous-clés du 558, dont 12 sur des routes au contrat
non mesuré** ; **les 5 chaînes nues** ; **les 10 chaînes ambiguës** ; **les 35
clés du contrat non gardé** ; **les 28 candidates** ; **les 6 clés sans lecture
observée** ; **les 26 routes à lectures ambiguës** ; **les 4 collisions de nom** ;
**les 3 ombres de `briefing.py`** ; **les 5 routes affamées du 556** ; **les 14
candidates du 554, en attente d'un GO** ; **les 4 routes construites
`/api/options/…` et les 3 préfixes illisibles** ; **`/api/ticker/`, hors
corpus** ; **les 7 routes sans filet du 554/555** ; **les 128 clés servies non
nommées du 552** ; **`/api/weekly` rend un objet vide en DÉMO** ; **les 6 points
d'entrée du 551** ; **les 15 points d'entrée au statut seul du 550** ; **les 43
points d'entrée couverts par personne** ; **les 11 identifiants de
`/intelligence`, `/tracking` et `pf-risk-gauge`** ; **les 4 zones sous attente du
545** ; **le contrat d'ÉCHEC serveur, jamais observé** ; **les 4 noms de clé du
542** ; **les 15 messages d'erreur du 541** ; **les 95 atténuations non
affichées** ; **`initSettings`** ; **les 8 appels hors de toute fonction** ;
**les 36 accès DOM non suivis** ; **la définition du corpus de routes du
511-A** ; **l'ampleur du 518-A** ; **les 42 cas indéterminés du 528** ; **les 25
rangs fragiles** ; **les 33 identifiants reconstruits** ; **les 92 rapports non
additionnés du 526** ; **les quinze lots exposés du 525** ; **le « 7 barèmes » du
491** ; **mesurer les 23 routes — outil prêt, en attente d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 189 (+1)** ; publiés
puis corrigés **30** ; interprétations retirées **7 (+1)**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
