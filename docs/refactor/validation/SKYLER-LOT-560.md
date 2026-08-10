# SKYLER LOT 560 — le marquage par fichier **ne s'est pas propagé** : un seul banc sur sept était touché, et le mécanisme partagé est mesuré sans faute — 353 sites d'appel, zéro mal attribué

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-560` (base : lot 559 fusionné,
`7e31710a`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé. Aucune route appelée.**

## Le choix

**(ff)** — le 559 a établi que `l552_ambigus.py` marquait les variables **par
fichier et non par fonction**, faisant entrer 8 valeurs de moteur parmi 21
« tests de réponse ». Question : **combien d'autres chiffres publiés reposent
sur le même marquage ?**

## L'arrêt du lot — **le témoin du brief est faux, et de la même façon qu'au 559**

Le brief annonce : « témoin POSITIF attendu : `l552_contrat.py` doit ressortir
*par fichier* ». Lecture du banc : **`l552_contrat.py` ne lit aucun fichier de
test.** Ses champs nommés viennent de `l551_etendue.json` (lignes 62-65) ; son
seul travail propre est d'appeler les 23 routes sûres. Le marquage par fichier
était dans **`l552_ambigus.py`** — un **autre** banc du même lot.

**Un lot après avoir constaté que « les 21 du 551 » venaient en réalité du 552,
le brief attribue à nouveau un défaut au mauvais artefact.** La règle 559-A
s'applique à elle-même : une dette se vérifie à sa source, y compris quand la
source est un banc et non un rapport.

**Arrêtés avant publication : 185 → 186 (+1).**

## La mesure — ce que chaque banc fait, lu dans son code

```text
banc                     lit les tests   fonction de portée
l548_couverture.py            oui              NON
l549_construits.py            oui              NON
l549_garde.py                 NON              NON
l550_profondeur.py            oui              oui
l551_etendue.py               oui              oui
l552_contrat.py               NON              NON
l552_ambigus.py               oui              NON
```

**Cinq bancs lisent les tests ; deux scopent par fonction.** Et parmi les trois
qui ne le font pas, la lecture montre qu'ils ne marquent pas la même chose :

- **`l548_couverture.py`** mesure des **sites d'appel** (`client.get('/route')`),
  pas des variables de réponse. Un appel est un appel : rien à propager.
- **`l549_construits.py`** marque des **variables de boucle** sur des listes de
  littéraux — une portée naturellement locale à la boucle.
- **`l552_ambigus.py`** est le seul à construire un ensemble de **variables
  contenant une réponse JSON**, et le seul à le faire par fichier. **C'est le
  banc fautif, et il est le seul.**

Les deux plus gros chiffres de la série — les **388 champs du 551** et la
**profondeur des assertions du 550** — sont mesurés **par fonction**. Ils ne sont
pas touchés.

## Le mécanisme réellement partagé, mesuré

Quatre bancs (548, 550, 551, 552) reconnaissent les **noms de client de test**
par fichier. C'est la seule chose que le défaut aurait pu contaminer ailleurs.
Mesuré plutôt que supposé :

```text
sites d'appel `client.<verbe>(…)` reconnus            353
   dont le nom est LIÉ DANS la fonction               353
   dont le nom n'est client que PAR LE FICHIER          0
   dont le site est HORS de toute fonction              0
```

**Zéro site mal attribué sur 353.** Dans ce dépôt, chaque test lie son client
dans sa propre fonction — le marquage par fichier n'a jamais eu l'occasion de
déraper sur ce mécanisme-là.

## Second contrôle (481) — ce que cette mesure ne décide pas

- **Mon détecteur de portée cherche une fonction nommée `portee` ou
  `englobante`.** C'est un détecteur **par nom** — exactement le péché que je
  dénonce depuis le 559-B. Il n'est acceptable que parce que je l'ai
  **corroboré en lisant** les trois bancs sans portée : `l548` n'a aucun
  scoping, `l549_construits` marque des variables de boucle, `l552_ambigus`
  marque un ensemble de fichier. **Un banc qui scoperait en ligne, sans aide
  nommée, échapperait au détecteur.**
- Le zéro des 353 **borne le risque, il ne le constate pas** : un nom « client
  par le fichier seul » pourrait venir d'une fixture pytest ou d'une variable de
  module parfaitement légitimes. Ici, le cas ne se présente simplement jamais.
- **Seuls les bancs sauvegardés du 548 au 552 sont examinés.** Les bancs
  antérieurs ne sont pas dans ce périmètre.

## Ce que le dépôt fait bien, mesuré

- **353 sites d'appel sur 353 lient leur client localement** : la suite de tests
  n'a pas d'état partagé implicite entre fonctions de test.
- **Le défaut ne s'est pas propagé** : un banc sur sept, sur un seul mécanisme.
- Les deux bancs qui portaient les chiffres les plus lourds **avaient déjà la
  bonne portée** — ce n'est pas de la chance, `portee()` y est écrite
  explicitement.

## Portée — ce que ce lot NE dit PAS

- **Le plancher du 551 n'est toujours pas recalculé** (dette du 559).
- Rien n'est corrigé : `l552_ambigus.py` reste tel quel, sa mesure ayant déjà
  été reprise au 559.
- **Aucune route appelée, aucun navigateur, aucune correction engagée.**

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
0, 0, 0, 0, 0**.

Aucun dossier. Et pour une fois, la réponse à la question du lot est **rassurante
et vérifiée** : le défaut du 559 ne s'est pas répandu. Un seul banc sur sept,
sur un seul mécanisme, et le mécanisme partagé sort à **zéro faute sur 353**.

Ce qu'il faut dire quand même : **j'ai failli refaire au 560 l'erreur que je
venais de nommer au 559.** Le brief désignait `l552_contrat.py` avec assurance,
et il aurait suffi de le croire pour publier une deuxième mauvaise attribution
d'affilée. La règle 559-A n'a pas tenu parce qu'elle est écrite — elle a tenu
parce que j'ai ouvert le fichier.

Trois règles neuves :

- **560-A · UN DÉFAUT D'INSTRUMENT NE SE GÉNÉRALISE PAS PAR ANALOGIE** — sept
  bancs se ressemblent ; un seul portait le défaut, et il fallait les lire un
  par un pour le savoir.
- **560-B · UN DÉTECTEUR PAR NOM DOIT ÊTRE CORROBORÉ PAR LECTURE** — chercher
  une fonction appelée `portee` est commode et faillible ; le résultat ne vaut
  que parce que les trois bancs sans portée ont été ouverts.
- **560-C · UN ZÉRO MESURÉ VAUT MIEUX QU'UN RISQUE SUPPOSÉ** — « le marquage
  par fichier pourrait fausser les appels » était plausible ; 353 sur 353 dit
  que non.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **le plancher du 551, non recalculé** ; **les 10 cas
non tranchés du 559** ; **les 16 sous-clés du 558, dont 12 sur des routes au
contrat non mesuré** ; **les 5 chaînes nues** ; **les 10 chaînes ambiguës** ;
**les 35 clés du contrat non gardé** ; **les 28 candidates** ; **les 6 clés sans
lecture observée** ; **les 26 routes à lectures ambiguës** ; **les 4 collisions
de nom** ; **les 3 ombres de `briefing.py`** ; **les 5 routes affamées du 556** ;
**les 14 candidates du 554, en attente d'un GO** ; **les 4 routes construites
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

Comptes séparés : résultats faux **arrêtés avant publication 186 (+1)** ; publiés
puis corrigés **29** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
