# SKYLER LOT 566 — cinquième chiffre lourd : **156 se reproduit**, c'est un cumul par page — **79 variables distinctes** — et le **« vingt-six fois plus » du 540 divise deux objets différents** : le vrai facteur est **1,25**

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-566` (base : lot 565 fusionné,
`747e681b`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé. Aucune route appelée** — le corpus
était déjà sur disque depuis le 540.

## Le choix

**(ll)** — cinquième des sept chiffres lourds : les **156 variables serveur du
540**. Suite directe du 565, parce que le 540 a tourné sur **exactement le même
corpus** que le 539.

## Le périmètre reçu, vérifié à la réception (564-B)

```text
parties du corpus du 539                      113
parties du corpus du 540                      113
présentes au 539 et absentes au 540             0
présentes au 540 et absentes au 539             0
```

**Identique, mesuré.** Contrairement au 538, le 540 n'a pas hérité d'un périmètre
amputé. Un zéro **mesuré**, pas une absence de mesure (560-C).

## Ce que le JSON du 540 porte — et ce qu'il ne porte pas

`l540_ast.json` garde le point fixe sous la forme d'un **scalaire** :
`variablesServeur: 156`. Pas de liste, pas de page, pas de position. **Rien n'est
vérifiable à partir du fichier sauvegardé** — il a fallu rejouer le point fixe
avec le **même prédicat**, en enregistrant l'identité de chaque marquage
(`l566_serveur.js`). `l540_ast.js` n'est pas touché : c'est une preuve.

```text
CALIB 1 · REPRODUCTION  156 serveur · 112 atténuations · 272 honnêtes
                        · 2 072 neutres · 105 programmes · 0 erreur       OK
CALIB 2 · POSITIF       paramètre 50 · calcul local 37 · appel local 10
                        · objet reconstruit 5 · non déclarée 4 = 106      OK
CALIB 3 · NÉGATIF       une signature FABRIQUÉE                           OK
```

## Le premier constat — **156 est un cumul par page ; les variables distinctes sont 79**

```text
marquages (page, fichier, scope, nom) — publié   156
signatures distinctes                             79
   signatures vues sur plus d'une page            11
   unités en double                               77
   signatures dans un fichier `/static/**`        15
   signatures dans un script inline               64
```

Onze signatures sont chargées par les 8 pages — `tick` dans `live-updates.js`,
`_warm`/`data`/`p`/`r` dans `vx-core.js`, `d`/`r` dans `vx-entities.js`,
`st`/`a`/`tickers` dans `vx-shell.js`. **11 × 7 = 77. 156 − 77 = 79.**

## L'arrêt du lot — **le « vingt-six fois plus » divise deux objets différents**

Le 540 publie :

```text
variables classées SERVEUR au point fixe        156   (539, base seule : 6)
```

puis, en toutes lettres : « **Vingt-six fois plus de variables serveur**, et pas
une seule atténuation qui change de camp. »

**Mais le « 6 » du 539 n'a jamais été un compte de variables.** C'est le nombre
d'**atténuations** dont la racine était serveur (`dont racine SERVEUR prouvée
6`) — le banc du 539 ne comptait aucune variable et n'en gardait pas la liste.
Le tableau met donc **un compte de variables et un compte d'atténuations dans la
même colonne**, et le ratio les divise.

Mesuré : la règle de **base seule** (`await` ou `.fetch(` dans le
`VariableDeclarator`), sans aucune propagation.

```text
                                cumul   distinct
règle de BASE seule              125         55
point fixe complet               156         79
   ajouté par la propagation      31         24
base incluse dans le total       OUI        OUI

rapport publié                  156 / 6  = 26
rapport cumul / cumul           156 / 125 = 1,25
rapport distinct / distinct      79 / 55  = 1,44
```

**Le point fixe n'a pas multiplié les variables serveur par vingt-six : il les a
multipliées par environ 1,3.** L'inclusion stricte de la base dans le total est
vérifiée dans les deux comptages, donc les 31 marquages ajoutés sont bien
l'apport de la propagation — pas un artefact.

**Ce que cela ne remet PAS en cause** (548-A, sens de l'erreur vérifié) : la
mesure « **0 atténuation reclassée** » est indépendante, et elle tient. La règle
**540-A** — « un point fixe peut ne rien changer, et c'est un résultat » — reste
juste. C'est **la preuve qui l'accompagnait** qui était surdimensionnée d'un
facteur vingt : l'étonnement annoncé (« vingt-six fois plus, et rien ne bouge »)
était bien plus modeste que ce qui a été écrit.

**Publiés puis corrigés : 30 → 31 (+1).**

## Le second arrêt — **mon propre banc affichait déjà le nombre faux suivant**

Ma première sortie imprimait, en toute confiance, « rapport entre deux grandeurs
distinctes : **13,2** » — c'est-à-dire 79 / 6. **Le même défaut, réparé à
moitié** : j'avais corrigé le numérateur en distinct et gardé un dénominateur qui
ne comptait pas des variables. Publier 13,2 aurait remplacé un chiffre faux par
un autre.

C'est en allant mesurer ce que la règle de base marque **vraiment** (55, pas 6)
que le second faux a été arrêté.

**Arrêtés avant publication : 191 → 192 (+1).**

## Le troisième — **les 6 atténuations serveur reposent sur 5 variables**

```text
atténuations à racine serveur (539, publié)      6
variables distinctes derrière ces 6              5
   /markets   r.confidence||0                    2 clés distinctes
   /journal   tr.entries||0 + tr.resolved||0     1 seule variable `tr`
   /journal   d.n_outcomes||0                    1
   /system    r.ts||0                            1
```

**Ce n'est pas une correction du 565**, qui comptait des **atténuations** et
mesurait 6 publié = 6 distinct — exact. Ici je compte des **variables**. Deux
atténuations de `/journal` s'appuient sur la même variable `tr`. Deux objets, deux
comptes, aucun conflit (564-C).

## Second contrôle (481) — ce que coûte la sur-approximation

```text
variables serveur distinctes                     79
   dont racine d'au moins une atténuation `|| 0`  5
   dont AUCUNE atténuation ne s'y rattache       74
```

Le 540 assume une sur-approximation **à sens unique** (536-A) : un paramètre est
marqué serveur dès qu'**un seul** appelant lui passe une valeur réseau. Le coût
de cette réserve n'avait jamais été chiffré. Il l'est : **74 des 79 variables
réseau ne touchent aucun `|| 0`**.

## Ce que le dépôt fait bien, mesuré

- **Le périmètre du 540 est exactement celui du 539** — zéro écart dans les deux
  sens.
- **La feuille des origines s'additionne encore** — 50 + 37 + 10 + 5 + 4 = 106,
  vingt-six lots plus tard, au marquage près.
- **La base est strictement incluse dans le total**, dans les deux comptages : le
  point fixe n'a rien perdu en route.
- **Aucune des variables réseau n'alimente un `|| 0` au-delà des cinq connues** —
  la conclusion de fond du 540 est intacte.

## Portée — ce que ce lot NE dit PAS

- **Rien n'est corrigé dans le 540** : la correction est **en ajout**, ici.
- **Les 74 variables sans atténuation ne sont pas suspectes** — elles sont hors
  sujet pour la question du `|| 0`. Le lot les compte, il ne les juge pas.
- La signature est (fichier, position de scope, nom) : deux fichiers statiques
  identiques servis sous deux URL seraient comptés deux fois.
- **Deux chiffres lourds restent** : 103 états (541), 53 refus (542).

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
0, 0, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier. **Cinq chiffres lourds sur sept sont reproduits et qualifiés**, et
les cinq étaient des cumuls par page. Mais celui-ci est le premier qui ne se
contente pas d'être un cumul : **il portait un ratio faux**, et le ratio était la
phrase la plus citée du rapport.

Ce que je retiens : **j'ai failli corriger un chiffre faux par un autre.** Le
réflexe naturel, après quatre lots de cumuls, était de recompter le numérateur en
distinct et de republier le rapport. C'était encore faux, pour une raison qui
n'avait rien à voir avec le cumul : le dénominateur ne comptait pas la même chose
que le numérateur. Il a fallu aller mesurer ce que la règle de base marque
vraiment — un banc de plus, quinze lignes — pour voir que le « 6 » était un
compte d'atténuations déguisé en compte de variables.

Trois règles neuves :

- **566-A · UN RATIO SE VÉRIFIE PAR SES DEUX TERMES, JAMAIS PAR SON RÉSULTAT** —
  « 156 sur 6, soit vingt-six » est arithmétiquement juste et sémantiquement
  vide : les deux termes ne comptaient pas le même objet.
- **566-B · UN CHIFFRE SAUVEGARDÉ EN SCALAIRE EST UN SOUVENIR, PAS UNE MESURE** —
  `variablesServeur: 156` sans liste : vingt-six lots plus tard, rien n'était
  vérifiable sans tout rejouer.
- **566-C · CORRIGER UN CHIFFRE FAUX PEUT EN PRODUIRE UN AUTRE** — le 13,2 que mon
  propre banc affichait était faux exactement comme le 26 ; une correction
  partielle porte le défaut d'origine.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **DEUX chiffres lourds encore NON RECOMPTÉS** — 103
états (541), 53 refus (542) ; **les 74 variables serveur sans aucune
atténuation** ; **les 67 atténuations non affichées, toujours non lues** ; **les
25 atténuations de la bibliothèque tierce** ; **`/options|chips`, douzième limite
jamais levée ni nommée** ; **`renderCalendar`, exécutée hors périmètre au 537** ;
**les 4 limites distinctes du 564** ; **les 12 signatures partagées du 562** ;
**les 5 cas de réponse absents du corpus du 561** ; **les 8 unités encore
ambiguës** ; **les 10 cas non tranchés du 559** ; **les 16 sous-clés du 558, dont
12 sur des routes au contrat non mesuré** ; **les 5 chaînes nues** ; **les 10
chaînes ambiguës** ; **les 35 clés du contrat non gardé** ; **les 28
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

Comptes séparés : résultats faux **arrêtés avant publication 192 (+1)** ;
**publiés puis corrigés 31 (+1)** ; interprétations retirées **9**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
