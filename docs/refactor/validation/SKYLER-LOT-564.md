# SKYLER LOT 564 — troisième chiffre lourd : **11 se reproduit**, c'est un cumul par page — **4 limites distinctes** — et la **douzième limite du 537 n'a jamais été nommée**

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-564` (base : lot 563 fusionné,
`7b8fe6f5`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé. Aucune route appelée** — tout est
relu sur disque.

## Le choix

**(jj)** — troisième des sept chiffres lourds, le plus petit des restants : les
**11 limites levées du 538**.

## Vérifié à la source (559-A) — les six bancs existent

`l538_limites.py/.json`, `l538_src.js/.json`, `l538_corpus.json`, `_l538_run.js`
sont tous conservés. **Reproduction, pas reconstruction.**
`res` contient **11** couples, et **2 levées + 9 restantes = 11**. Exact.

## Le premier constat — **la douzième limite n'est nommée nulle part**

Le **corps** du 538 (lignes 96-103) est exact :

```text
limites d'instrument (537)                           12
   dont levées ou résolues au 538                    11
   dont AUCUNE n'est un chargeur muet                11
```

Il dit bien **douze**, dont onze levées. Mais :

- son **titre** annonce « **Les onze limites d'instrument du 537** sont
  levées » — comme s'il n'y en avait que onze ;
- **`chips` n'apparaît pas une seule fois dans le rapport** (`grep` : 0
  occurrence).

Identifiée par différence : la douzième est **`/options|chips`**. Le second banc
du 537 l'avait déplacée de « muettes » vers « limites » (11 → 12) ; le banc du
538 a reçu la liste d'**avant** cette correction.

```text
limites du 537 AVANT correction (JSON)        11
limites du 537 APRÈS correction (rapport)     12
couples traités par le 538                    11
   non traitées                                1   /options|chips
   traitées sans être une limite               0
```

**Le chiffre 11 est juste ; c'est le titre qui déborde, et la douzième qui reste
sans nom.**
**Interprétations retirées : 7 → 8 (+1).**

## Le second — **11 est un cumul par page ; les limites distinctes sont 4**

```text
couples (page, fonction) — le chiffre publié   11
signatures (fonction, position) distinctes      4
   signatures vues sur plus d'une page          1
   unités en double                             7
   couples sans position retrouvée              0
```

`navigate`, position 8160, sur les **8 pages** — sept unités à elle seule. Les
trois autres sont sur une seule page : `boot`, `initSettings`, `risk`.
**11 − 7 = 4.**

## L'arrêt du lot — **ce quatre n'est pas le « quatre » de 531-A**

Le 538 conclut sur « le **quatre** de 531-A devient définitif ». Ce quatre-là
désigne les **quatre chargeurs muets** — `renderRadar`, `renderStocks`,
`renderOptions`, `renderAnomalies`. Le mien désigne **quatre limites
d'instrument distinctes**. Publier « 4 » sans le dire aurait laissé croire à une
confirmation.

Vérifié plutôt que supposé : **aucun des quatre muets ne figure dans les 11
limites.** Recouvrement **zéro**. **Deux quatre différents, mesurés comme tels.**

**Arrêtés avant publication : 189 → 190 (+1).**

## Second contrôle (481) — le banc du 538 déborde-t-il ?

```text
couples traités hors de la liste reçue du 537     0
```

**Zéro.** Contrairement au banc du 537 — qui avait exécuté `renderCalendar` hors
de son périmètre (563) — **le banc du 538 a traité exactement la liste qu'il
avait reçue**. Un zéro **mesuré**, pas une absence de mesure (560-C).

La nuance compte : **le 538 n'a pas débordé, il a hérité d'un périmètre déjà
incomplet.** Le défaut est en amont, dans le passage de relais entre les deux
bancs du 537.

## Ce que le dépôt fait bien, mesuré

- **Le corps du 538 dit 12 et 11** : la feuille était juste, seul le titre
  simplifie.
- **Zéro couple traité hors périmètre** — le banc du 538 est discipliné.
- **Zéro couple sans position retrouvée** : les 11 se rattachent tous à une
  entrée du 534, vingt-six lots plus tard.
- Sur les 4 limites distinctes, **trois ne concernent qu'une seule page** :
  l'instrumentation ne butait pas sur un obstacle général.

## Portée — ce que ce lot NE dit PAS

- **`chips` n'est pas levée dans ce lot** : elle est **nommée**, pas traitée. La
  lever demanderait d'exécuter la fonction, ce que ce lot ne fait pas.
- **Le « quatre » de 531-A n'est pas remis en cause** — il porte sur autre chose.
- Deux fonctions distinctes partageant nom **et** position seraient fusionnées.
- **Quatre chiffres lourds restent** : 112 atténuations, 103 états, 53 refus,
  156 variables serveur.

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
0, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier. **Trois chiffres lourds sur sept sont reproduits et qualifiés**, et
les trois étaient des cumuls par page — 178 → 94, 25 → 18, 11 → 4. Aucun des
trois rapports d'origine ne le précisait.

Ce que je retiens de ce lot : **le piège que j'avais écrit avant de mesurer s'est
effectivement présenté.** Le décompte distinct tombe sur quatre, et le 538
conclut sur « le quatre de 531-A ». Sans la phrase d'avertissement rédigée en
tête du banc, j'aurais pu publier un chiffre qui se lisait comme une
confirmation et n'en était pas une. **Écrire le piège avant la mesure, c'est ce
qui l'a rendu inoffensif.**

Trois règles neuves :

- **564-A · UN TITRE SIMPLIFIE PLUS VITE QU'UN TABLEAU** — le corps du 538 dit
  « 12, dont 11 » ; son titre dit « les onze limites ». Le tableau était juste,
  la phrase de couverture non.
- **564-B · UN PÉRIMÈTRE HÉRITÉ SE VÉRIFIE À LA RÉCEPTION** — le banc du 538
  n'a pas débordé : il a reçu onze éléments d'une liste qui en comptait douze,
  sans que rien ne le signale.
- **564-C · DEUX NOMBRES ÉGAUX NE SONT PAS LE MÊME NOMBRE** — quatre limites
  distinctes et quatre chargeurs muets, recouvrement zéro ; il fallait le
  mesurer pour pouvoir l'écrire.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **QUATRE chiffres lourds encore NON RECOMPTÉS** — 112
atténuations (539), 103 états (541), 53 refus (542), 156 variables serveur
(540) ; **`/options|chips`, douzième limite jamais levée ni nommée** ;
**`renderCalendar`, exécutée hors périmètre au 537** ; **les 12 signatures
partagées du 562** ; **les 5 cas de réponse absents du corpus du 561** ; **les 8
unités encore ambiguës** ; **les 10 cas non tranchés du 559** ; **les 16
sous-clés du 558, dont 12 sur des routes au contrat non mesuré** ; **les 5
chaînes nues** ; **les 10 chaînes ambiguës** ; **les 35 clés du contrat non
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
d'erreur du 541** ; **les 95 atténuations non affichées** ; **`initSettings`** ;
**les 8 appels hors de toute fonction** ; **les 36 accès DOM non suivis** ; **la
définition du corpus de routes du 511-A** ; **l'ampleur du 518-A** ; **les 42 cas
indéterminés du 528** ; **les 25 rangs fragiles** ; **les 33 identifiants
reconstruits** ; **les 92 rapports non additionnés du 526** ; **les quinze lots
exposés du 525** ; **le « 7 barèmes » du 491** ; **mesurer les 23 routes — outil
prêt, en attente d'un GO**.

Comptes séparés : résultats faux **arrêtés avant publication 190 (+1)** ; publiés
puis corrigés **30** ; interprétations retirées **8 (+1)**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
