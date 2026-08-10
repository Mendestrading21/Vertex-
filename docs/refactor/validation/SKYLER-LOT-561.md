# SKYLER LOT 561 — le plancher du 551 recalculé **par vérification et non par soustraction** : 367 devient **380**, et sur les 21 cas ambigus **huit seulement** existaient dans le corpus

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-561` (base : lot 560 fusionné,
`4e412feb`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé. Aucune route appelée** — les mesures
du 551 et du 559 sont sur disque.

## Le choix

**(gg)** — dette créée par le 559 et laissée intacte par le 560. Le 552 avait
écrit : « les 388 champs du 551 sont une **borne haute** ; **367 est le
plancher** si les 21 ambigus étaient tous des sous-chaînes ». Or les 21 sont
**13**. **Personne n'avait recalculé.**

## Vérifié à la source avant toute mesure (559-A)

- `SKYLER-LOT-551.md:67` publie « champs JSON distincts nommés · TOTAL cumulé
  **388** ». Ouverture de `l551_etendue.json` : `champs` est un dictionnaire de
  **141 points d'entrée**, et la somme de leurs tailles vaut exactement **388**.
- `SKYLER-LOT-552.md:43` : « **367 est le plancher** » — c'est-à-dire 388 − 21.

## L'arrêt du lot — **une fourchette n'est pas une soustraction**

Le brief proposait de retirer 13 au lieu de 21, soit 375. **C'était le même
geste, avec un autre nombre.** La soustraction suppose que chaque cas ambigu ait
apporté **exactement une unité** au corpus des 388 — et rien ne le garantit :
une chaîne cherchée peut ne pas avoir été retenue par le crible du 551, et deux
tests peuvent apporter le même couple.

Vérifié couple par couple (point d'entrée, chaîne cherchée) :

```text
cas ambigus au total                                     21
   sur une RÉPONSE HTTP (559)                            13
   sur un APPEL DIRECT à un moteur (559)                  8

couples réellement COMPTÉS dans les 388
   venant d'une réponse                                   8
   venant d'un appel direct                               0
```

**Huit unités, pas vingt et une, pas treize.**

```text
borne haute publiée au 551                              388
plancher publié au 552  (388 − 21)                      367
plancher RECALCULÉ      (388 − 8, vérifié)              380
```

La fourchette se resserre de **21 points à 8**. Publier 375 aurait été faux —
d'un cran plus juste que 367, et faux quand même.

**Arrêtés avant publication : 186 → 187 (+1).**
**Correction d'un chiffre publié — le plancher du 552 : 367 → 380.**
**Publiés puis corrigés : 29 → 30 (+1).** Le rapport 552 n'est pas réécrit ; la
correction est portée ici, en ajout.

## Les cinq cas de réponse qui n'étaient pas dans le corpus

Sur les 13 cas portant sur une vraie réponse, **cinq n'apportent aucune unité** :

```text
command.api_portefeuille        'RISK-OFF'
analysis_api.api_skyler         'PCX'
positions_api.positions_reconc  'aucune clôture automatique…'
content.news_feed_ep            'IBKR'
live_api.live_refresh           'Réponse assemblée par…'
```

Le crible du 551 ne les a pas retenues. **Le fait est constaté, il n'est pas
expliqué** : savoir pourquoi demanderait de rejouer le crible du 551 cas par
cas, ce que ce lot ne fait pas.

## Une seconde imprécision, dans le 551 lui-même

`SKYLER-LOT-551.md:121` écrit « **388 champs JSON distincts sont nommés** par la
suite ». Mesuré :

```text
somme des champs PAR POINT D'ENTRÉE      388
noms GLOBALEMENT distincts               257
```

**Les deux nombres sont vrais, ils ne désignent pas la même chose** (546-A). La
ligne 67 dit « TOTAL cumulé » et reste exacte ; la ligne 121 dit « distincts »
sans le cumul, et **cette qualification-là ne tient pas**. Le nombre reste 388 ;
c'est le mot « distincts » qui est retiré.
**Interprétations retirées : 4 → 5 (+1).**

## Second contrôle (481) — le corpus du 551 mélange-t-il deux natures ?

```text
couples issus d'un APPEL DIRECT et pourtant comptés dans les 388      0
cas comptés deux fois sur le même couple                              0
```

**Zéro.** Le 559 avait montré que le banc du 552 mélangeait réponses HTTP et
retours de moteur ; **le corpus des 388 du 551, lui, ne les mélange pas.** C'est
cohérent avec le 560 : le 551 marque ses variables **par fonction**. Un zéro
mesuré, pas un risque supposé (560-C).

## Ce que le dépôt fait bien, mesuré

- **Le corpus du 551 est propre** : aucune chaîne issue d'un appel direct n'y
  figure, alors que huit tests en produisaient.
- **La borne haute 388 tient** : elle n'a jamais été contestée, seulement son
  plancher.
- Les huit unités réellement en cause sont **nommées une par une** — la
  fourchette est désormais vérifiable ligne à ligne.

## Portée — ce que ce lot NE dit PAS

- **Les 8 unités ne sont pas déclarées fausses** : elles restent ambiguës — clé
  ou sous-chaîne, la lecture du 559 n'a tranché que 3 cas sur 13.
- **Pourquoi cinq cas de réponse manquent au corpus n'est pas expliqué.**
- Rien n'est recalculé au-delà du plancher : la médiane, le maximum et les
  autres chiffres du 551 ne sont pas retouchés.
- **Aucune route appelée, aucune correction engagée.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**, aucun banc tronqué avant d'avoir écrit son JSON.
- **Aucun fichier de production touché** (`git status` : seuls les documents).
  Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** avant tout import.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers ; **3 modifiés par la suite de tests** (`ai_enrichment.json`, `desk_data.json`,
  `weekly_snapshot.json`), **restaurés — écart final AUCUN**, aucun fichier apparu ni disparu
- Suite : **2864 passed / 0 skipped**, lancée **après** les documents

## Où en est la boucle

La série des rangs devient
**1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0**.

Aucun dossier. Trois lots ont suivi la même chaîne : le 559 a trouvé que les 21
étaient 13, le 560 a vérifié que le défaut ne s'était pas propagé, le 561
recalcule enfin le plancher. **Et le recalcul ne donne ni 367 ni 375, mais 380**
— parce qu'à chaque étape la tentation était de refaire une soustraction sur un
corpus qu'on n'avait pas ouvert.

Ce qu'il faut dire nettement : **le 552 et le brief ont commis la même faute à
un lot d'intervalle, et moi la troisième fois j'ai failli la commettre aussi.**
Retirer N d'un total est un geste si naturel qu'il se fait sans qu'on remarque
l'hypothèse qu'il contient.

Trois règles neuves :

- **561-A · UNE BORNE SE VÉRIFIE PAR APPARTENANCE, JAMAIS PAR SOUSTRACTION** —
  retirer 21 puis 13 d'un corpus qui n'en contenait que 8 revient à retirer du
  vide.
- **561-B · « DISTINCTS » ET « CUMULÉS » NE SONT PAS LE MÊME NOMBRE** — 388 par
  point d'entrée, 257 globalement ; le même corpus, deux grandeurs.
- **561-C · UN CORPUS PROPRE SE CONSTATE, IL NE SE PRÉSUME PAS** — le banc du
  552 mélangeait deux natures, celui du 551 non ; seule la mesure le disait.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **les 5 cas de réponse absents du corpus, non
expliqués** ; **les 8 unités encore ambiguës** ; **les 10 cas non tranchés du
559** ; **les 16 sous-clés du 558, dont 12 sur des routes au contrat non
mesuré** ; **les 5 chaînes nues** ; **les 10 chaînes ambiguës** ; **les 35 clés
du contrat non gardé** ; **les 28 candidates** ; **les 6 clés sans lecture
observée** ; **les 26 routes à lectures ambiguës** ; **les 4 collisions de nom** ;
**les 3 ombres de `briefing.py`** ; **les 5 routes affamées du 556** ; **les 14
candidates du 554, en attente d'un GO** ; **les 4 routes construites
`/api/options/…` et les 3 préfixes illisibles** ; **`/api/ticker/`, hors
corpus** ; **les 7 routes sans filet du 554/555** ; **les 128 clés servies non
nommées du 552** ; **`/api/weekly` rend un objet vide en DÉMO** ; **les 6 points
d'entrée du 551** ; **les 15 points d'entrée au statut seul du 550** ; **les 43
points d'entrée couverts par personne** ; **les 11 identifiants de
`/intelligence`, `/tracking` et `pf-risk-gauge`** ; **les 4 zones sous attente du
545** ; **les SEPT chiffres lourds encore NON RECOMPTÉS** ; **le contrat d'ÉCHEC
serveur, jamais observé** ; **les 4 noms de clé du 542** ; **les 15 messages
d'erreur du 541** ; **les 95 atténuations non affichées** ; **`initSettings`** ;
**les 8 appels hors de toute fonction** ; **les 36 accès DOM non suivis** ; **la
définition du corpus de routes du 511-A** ; **l'ampleur du 518-A** ; **les 42 cas
indéterminés du 528** ; **les 25 rangs fragiles** ; **les 33 identifiants
reconstruits** ; **les 92 rapports non additionnés du 526** ; **les quinze lots
exposés du 525** ; **le « 7 barèmes » du 491** ; **mesurer les 23 routes — outil
prêt, en attente d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 187 (+1)** ; publiés
puis corrigés **30 (+1)** ; interprétations retirées **5 (+1)**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
