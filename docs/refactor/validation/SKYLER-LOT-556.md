# SKYLER LOT 556 — la portée ne réduit pas le contrat non gardé : **elle exhume un point d'entrée entier que l'espace de noms plat avait affamé** — et met au jour une quatrième cellule que le 553 ne comptait pas

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-556` (base : lot 555 fusionné,
`ddcd0b00`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé. Aucune route appelée** — les mesures
du 552 et le corpus JS du 553 sont sur disque.

## Le choix

**(bb)** — le 555 a prouvé sur 7 routes que l'espace de noms plat du 553
fabrique des reproches. Les 3 collisions mesurées touchent aussi
`/api/portfolio/*`, `/api/journal/*`, `/api/skyler/*`. Question : **une fois la
portée appliquée à tout le corpus, que deviennent les 19 clés du contrat non
gardé — et combien des 20 candidates étaient des artefacts de collision ?**

Prédicat **identique** au 553 (546-A). Une seule chose change : `lues_portee`
(555) au lieu du plat. Le banc **reproduit d'abord exactement 17 / 19 / 20**
avant de recompter — sinon il s'arrête.

## L'arrêt du lot — **les trois seaux du 553 ne partitionnent pas**

Le 553 écrivait `ni = s - lu - nm`. Une clé **nommée par un test mais NON lue
par la page** n'entre alors dans **aucun** des trois seaux : ni dans A (lue et
nommée), ni dans B (lue non nommée), ni dans C (ni lue ni nommée, puisque `nm`
est retranché). En espace de noms plat, la somme `a+b+c` passait donc pour « le
total des clés servies ».

**Elle ne l'était pas.** Mesuré : cette quatrième cellule valait **déjà 5** dans
la mesure plate. Le 553 a publié « les 56 clés servies de ces 9 points
d'entrée » ; le vrai total est **61**.

**Correction d'un chiffre publié : « 56 » devient « 61 ».** Le rapport 553
n'est pas réécrit — la correction est portée ici, en ajout.
**Publiés puis corrigés : 25 → 26. Arrêtés avant publication : 179 → 180.**

## La mesure

```text
                                        553 (plat)   556 (portée)
points d'entrée communs                       9            10
A · LUE par la page ET NOMMÉE par un test    17            17
B · LUE, NON NOMMÉE — contrat non gardé      19            22
C · ni lue ni nommée — CANDIDATE             20            23
D · NOMMÉE mais NON LUE — 4e cellule          5             8
total des clés servies de ces routes         61            70
```

**Le total A inchangé à 17 est une coïncidence**, et il fallait la défaire
avant de publier quoi que ce soit. Décomposition :

```text
sur les 9 points d'entrée d'origine   A 15 · B 19 · C 20 · D 7
sur le 10ᵉ, exhumé par la portée      A  2 · B  3 · C  3 · D 1
```

**Sur le périmètre d'origine, B et C ne bougent PAS** : le contrat non gardé
reste **19**, les candidates restent **20**. La réponse à la question du lot est
donc nette : **zéro** des 20 candidates était un artefact de collision. Deux
clés seulement changent de case — `score` (`/api/market/summary`) et `domains`
(`/api/live/status`) quittent A pour la quatrième cellule : un test les nomme,
la page ne les lit pas.

## Ce que l'espace de noms plat cachait vraiment

Pas une inflation diffuse : une **absorption totale**, et six routes réduites au
silence.

```text
groupe de collision           plat        portée
/api/portfolio/context         27   →       11
/api/portfolio/stress           0   →        6
/api/skyler/graph               0   →        5
/api/journal/postmortem        27   →       11
/api/skyler/calibration         0   →        5
/api/skyler/memory              0   →        9
/api/system/automations         8   →        1
/api/system/connections         0   →        1
/api/tradingview/signals        0   →        1
```

Dans chaque groupe, **une route absorbait tout et deux étaient affamées à
zéro**. Six routes affichaient « aucune clé lue » alors qu'elles en lisent 5, 6,
9, 1, 1 et 5.

Une seule de ces six est aussi servie parmi les 23 routes mesurées au 552 :
**`/api/skyler/calibration`**. C'est pourquoi exactement **un** point d'entrée
entre dans le périmètre — avec **9 clés servies**, dont **3 d'un contrat non
gardé** (`by_decision`, `demo`, `outcomes`).

**Le 553 ne disait pas que `/api/skyler/calibration` n'était pas lue. Il ne la
voyait pas du tout.**

## Le contrat non gardé, après la portée

```text
/api/market/summary        breadth · regime · roro · roro_gap · vix · vix_band · vix_chg
/api/market/regime         confidence · dimensions_used · secondary
/api/session/manifest      age_s · as_of · scanned · source
/api/opportunities/funnel  actionable_symbols · note
/api/skyler/calibration    by_decision · demo · outcomes          ← nouveau
/api/positions/alerts      active
/api/live/status           demo
/api/data-quality          note
```

**Constat non arbitré**, borné à 22 clés sur 10 points d'entrée. **Rien n'est
corrigé** — écrire un test est une modification de production, qui demande un GO.

## Second contrôle (481) — ce que la portée ne décide pas

```text
points d'entrée que la portée VIDE de toute lecture              0
OMBRES — nom marqué, redéclaré dans une fonction imbriquée       3
appels `VX.fetch.peek` (enveloppe {data, age, ts})               8
   clés lues sur une valeur de `peek`                     `data` seule
   points d'entrée communs servant `data`/`age`/`ts`               0
```

**Les 3 ombres.** Ma portée est une **contenance syntaxique** : elle ne modélise
pas l'ombre. Lu dans `briefing.py` — `loadSummary` lie `sum`, `reg`, `cmd` par
`VX.fetch`, et la flèche imbriquée `paint=(sum,reg,cmd)=>{…}` **redéclare les
trois noms** comme paramètres. Les lectures `reg.confidence`, `sum.vix`… portent
donc sur les **paramètres**, pas sur les liaisons que j'ai marquées.
**L'attribution est juste par SUBSTANCE et non par construction** : `paint` est
appelée avec la valeur de ces mêmes routes (`paint(sum,reg,cmd)` et
`paint(cs&&cs.data, cr&&cr.data, cc&&cc.data)`). Je le dis parce que **le témoin
positif de ce lot — `confidence` — tient exactement par cette ombre.**

**L'enveloppe de `peek`.** Lu dans `vx-core.js:316`, `VX.fetch.peek(url)` rend
`{data, age, ts}` — **pas la charge utile de la route**. Le 553 traitait `peek`
comme `fetch` : une lecture de premier niveau sur une valeur de `peek` est un
champ d'enveloppe, pas une clé de contrat. **Effet mesuré : nul** — la seule clé
ainsi lue est `data`, et aucun point d'entrée commun ne sert `data`, `age` ni
`ts`, si bien que le filtre par `SERVI` l'écartait déjà. **Défaut réel, effet
nul : ce n'est donc pas un arrêt** (553-B).

**Zéro point d'entrée vidé par la portée** : aucune route ne perd toutes ses
lectures — le cas `/api/system/config` du 555 ne se reproduit pas ici.

## Ce que le dépôt fait bien, mesuré

- **Le contrat non gardé ne s'est pas aggravé sur le périmètre d'origine** :
  19 hier, 19 aujourd'hui, malgré un instrument entièrement refait.
- **Aucune candidate n'était un artefact** : les 20 tiennent après correction.
- Les six routes affamées **lisent toutes quelque chose** — le produit ne
  contient pas, ici, de route appelée pour rien.
- **La partition est désormais vérifiée par une assertion** dans le banc :
  A + B + C + D = clés servies, point d'entrée par point d'entrée.

## Portée — ce que ce lot NE dit PAS

- **10 points d'entrée seulement** : l'intersection entre les 23 routes mesurées
  au 552 et ce que les pages lisent. Les 5 autres routes affamées ne sont pas
  dans cette intersection — **leur contrat n'est pas mesuré**, seulement leur
  nombre de clés lues.
- **Premier niveau uniquement**, des deux côtés (546-A).
- **La portée n'est pas une analyse de portées JavaScript** : ni ombre, ni
  hissage, ni fermeture capturée hors du corps.
- **550-B** : aucune clé du seau C n'est déclarée inexistante. « Candidate »
  reste le mot.
- **Aucune route appelée, aucun navigateur, aucune correction engagée.**

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
0**.

Aucun dossier. Et il faut dire franchement ce que ce lot fait à la thèse du
précédent. Le 555 concluait qu'un instrument mal lu **produit des reproches**.
Ici, l'instrument corrigé ne retire **aucun** reproche : les 19 restent 19, les
20 restent 20. Ce qu'il retire, c'est autre chose — **un angle mort entier** :
six routes que le crible affichait à zéro clé lue, dont une qui portait trois
clés d'un contrat non gardé jamais comptées.

**Un espace de noms plat ne fait pas que mal attribuer : il fait disparaître.**
Et la disparition est plus dangereuse que l'accusation, parce qu'elle ne laisse
aucune trace à vérifier.

Trois règles neuves :

- **556-A · UNE COLLISION AFFAME AUTANT QU'ELLE ABSORBE** — dans chaque groupe,
  une route prenait 27, 27 et 8 clés, et deux affichaient zéro. Le zéro était
  l'artefact, pas le nombre élevé.
- **556-B · DES SEAUX QUI NE PARTITIONNENT PAS MENTENT SUR LEUR TOTAL** — la
  quatrième cellule valait déjà 5 au 553 ; la somme publiée comme « total des
  clés servies » en oubliait cinq. Une partition se **vérifie par assertion**.
- **556-C · UN TOTAL INCHANGÉ PEUT CACHER DEUX MOUVEMENTS ÉGAUX** — A reste à
  17 parce que 2 clés le quittent et 2 y entrent. Publier « inchangé » sans
  décomposer aurait été exact et trompeur.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **les 22 clés du contrat non gardé — constat, non
arbitré** ; **les 23 candidates** ; **les 8 clés nommées par un test et non lues
par la page** ; **les 5 routes affamées hors intersection, dont le contrat n'est
pas mesuré** ; **les 3 ombres de `briefing.py`** ; **les 14 candidates du 554, en
attente d'un GO** ; **les 4 routes construites `/api/options/…` et les 3
préfixes illisibles** ; **`/api/ticker/`, appelé par `/analysis/<symbole>`, hors
corpus** ; **les 7 routes sans filet du 554/555** ; **les 21 tests de membre
ambigus du 551** ; **les 128 clés servies non nommées du 552** ; **`/api/weekly`
rend un objet vide en DÉMO** ; **les 6 points d'entrée du 551** ; **les 15 points
d'entrée au statut seul du 550** ; **les 43 points d'entrée couverts par
personne** ; **les 11 identifiants de `/intelligence`, `/tracking` et
`pf-risk-gauge`** ; **les 4 zones sous attente du 545** ; **les SEPT chiffres
lourds encore NON RECOMPTÉS** ; **le contrat d'ÉCHEC serveur, jamais observé** ;
**les 4 noms de clé du 542** ; **les 15 messages d'erreur du 541** ; **les 95
atténuations non affichées** ; **`initSettings`** ; **les 8 appels hors de toute
fonction** ; **les 36 accès DOM non suivis** ; **la définition du corpus de
routes du 511-A** ; **l'ampleur du 518-A** ; **les 42 cas indéterminés du 528** ;
**les 25 rangs fragiles** ; **les 33 identifiants reconstruits** ; **les 92
rapports non additionnés du 526** ; **les quinze lots exposés du 525** ; **le
« 7 barèmes » du 491** ; **mesurer les 23 routes — outil prêt, en attente d'un
GO**.

Comptes séparés : résultats faux **arrêtés avant publication 180 (+1)** ; publiés
puis corrigés **26 (+1)** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
