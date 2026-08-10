# SKYLER LOT 567 — sixième chiffre lourd : **53 n'est PAS un cumul par page** — la prédiction tient — mais c'est un **cumul par RÈGLE** : onze refus comptés deux fois, **42 distincts**

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-567` (base : lot 566 fusionné,
`df2f5a1e`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé. Rien installé. Aucune route appelée** — la partie du
542 qui produit le 53 lit des fichiers Python sur disque.

## Le choix, et la prédiction écrite avant de mesurer

**(mm)** — sixième des sept chiffres lourds : les **53 refus JSON du 542**.

Les cinq chiffres déjà recomptés (178, 25, 11, 112, 156) portaient tous sur le
**JavaScript servi des 8 pages**, où un fichier statique est relu une fois par
page : le cumul y est structurel. **Le 53 est un compte serveur — du Python lu
une seule fois par fichier.** La prédiction, écrite avant toute mesure : **53 =
53, aucun cumul par page.** Et si elle se confirmait, il fallait la publier telle
quelle sans chercher un angle qui « rende » quelque chose (540-A).

## Reproduction (556-B)

```text
CALIB 1 · REPRODUCTION  53 expliqués · 4 nus · 101 `jsonify({...})`
          · six formes exactes (drapeau négatif 21 · 404 11 · 400 9
          · 500 9 · 422 2 · 401 1)                                    OK
CALIB 2 · POSITIF       relevé BRUT 7 noms · ∩ RAISON = 4 publiés     OK
CALIB 3 · NÉGATIF       un fichier FABRIQUÉ                           OK
```

## La prédiction — **tenue**

```text
refus publiés                                 53
signatures (fichier, ligne, colonne)          53
fichiers distincts portant un refus           11
fichiers du corpus, chemins distincts      22 / 22
```

**Aucun cumul par page.** Le corpus est du Python lu une fois par fichier ; il
n'existe aucun mécanisme de relecture. Le défaut des cinq lots précédents **ne se
transpose pas** (563-C), et c'est un résultat.

## Le premier constat — **mais c'est un cumul par RÈGLE**

En lisant le prédicat **littéral** de `l542_contrat.py`, une chose saute aux
yeux : `expliques` est rempli par **deux branches indépendantes** dans la même
boucle `ast.walk` —

- **(A)** un `Return` d'un tuple `(jsonify({…}), code ≥ 400)` portant un message ;
- **(B)** un `Call` à `jsonify({…})` portant un drapeau négatif **et** un message.

`ast.walk` visite le `Return`, **puis le `Call` qu'il contient**. Un refus qui
porte **à la fois** un drapeau négatif et un code ≥ 400 est donc compté deux fois.

Mesuré par **contenance réelle dans l'arbre** — remontée des ancêtres, identité
de nœud :

```text
branche A — `Return` (jsonify, code ≥ 400) avec message      32
branche B — `jsonify` à drapeau négatif avec message         21
A + B — le chiffre publié                                    53
couples PROUVÉS (le `jsonify` de B descend du `Return` de A) 11
refus réellement distincts                                   42
```

Le témoin de l'instrument : **21 `jsonify` sont contenus dans un `Return` compté
par A sans être retenus par B** — la remontée d'ancêtres ne marque donc pas tout
ce qu'elle croise.

Vérifié dans le code, pas déduit :

```python
# vertex/app/routes/desk.py:77
return jsonify({'ok': False, 'err': 'payload invalide'}), 400
```

Drapeau négatif **et** code 400 : un seul refus, deux comptes.

## Ce que la correction change — et ce qu'elle ne change pas

**Sens de l'erreur vérifié (548-A)** : les deux bornes du 542 s'appliquaient à
**la même liste**, donc elles rétrécissent ensemble. « 53 sur 53 » devient
**« 42 sur 42 »**, et **la conclusion tient intégralement : zéro refus JSON
muet.** Le dépôt explique toujours 100 % de ses refus.

Ce qui bouge :

```text
                                    publié  double  distinct
vertex/app/routes/analysis_api.py       17       7        10
vertex/app/routes/desk.py               10       4         6
les 9 autres fichiers                   26       0        26
                                       ───     ───       ───
                                        53      11        42
```

Le 542 écrit : « **`desk.py`, le point le plus sensible du produit, est celui qui
explique le plus : dix refus, tous nommés.** » Ils sont **six**. L'éloge reste
mérité — six refus tous nommés, dont quatre doublement explicites — mais le
chiffre était gonflé.

La répartition par forme l'est aussi : les 11 doubles sont comptés **une fois
dans « drapeau négatif » et une fois dans un code** (400 × 6, 404 × 4, 500 × 1).

**Publiés puis corrigés : 31 → 32 (+1).**

## L'arrêt du lot — **la proximité de ligne n'est pas la contenance**

Mon premier banc appariait A et B par **intervalle de lignes**
(`a.lineno ≤ b.lineno ≤ a.end_lineno`) et sortait déjà « 11 ». Le nombre était
juste ; **la preuve ne l'était pas** : deux instructions peuvent partager une
ligne, et un `Return` multi-lignes peut contenir un *autre* `jsonify` que celui
testé. J'ai refait la mesure par remontée d'ancêtres avec **identité de nœud**,
plus le témoin des 21.

Publier un 11 obtenu par proximité aurait été un bon chiffre avec une mauvaise
raison — et personne n'aurait pu le distinguer d'un vrai.

**Arrêtés avant publication : 192 → 193 (+1).**

## Le second — **mon attente sur le vocabulaire était fausse**

J'attendais que le relevé brut du 542 redonne les **quatre** noms publiés. Il en
rend **sept**.

```text
relevé BRUT (toute clé à valeur chaîne)   7   err, error, final_decision,
                                              label, login, note, reason
publié par le rapport                     4   err, error, note, reason
écartés                                   3   final_decision, label, login
```

Ce n'est **pas** un échec de reproduction : c'est mon attente qui était fausse
(556-B). Le banc alimente son vocabulaire avec toute clé à valeur chaîne, et le
rapport publie ensuite l'**intersection avec une liste `RAISON` écrite à la
main**.

Et le rapport **nomme les trois écartés** deux sections plus haut — arrêt n°2 :
« ma règle de repli ramassait `final_decision`, `label`, `login`, qui ne sont pas
des raisons ». **Rien n'est caché.** Mais la section qui publie le 4 s'intitule
« **relevé et non deviné** », alors que le passage de 7 à 4 se fait précisément
par une liste de noms devinée. Le chiffre est juste, le qualificatif est trop
fort.

**Interprétations retirées : 9 → 10 (+1).**

## Second contrôle (481) — ce que le « 53 » n'inclut pas

```text
appels `jsonify({...})` au total              101
   dont refus (branche B)                      21
   donc réponses NOMINALES                     80
refus NUS, hors JSON — comptés à part           4
   analysis_api.py  404  l.483 · l.491 · l.556
   terminal.py      404  l.1697
```

Le 542 écrit « les pages d'erreur HTML sont citées mais pas comptées dans le
53 ». **Elles sont quatre**, toutes des `render_shell` en 404, et le rapport les
cite nommément (« Groupe inconnu », « Cellule inconnue », « Décision inconnue »).
Le « 0 à 0 » du tableau porte donc bien sur les refus **JSON**, et il est exact —
mais **le chiffre 4 n'apparaît nulle part**.

## Le ratio « 53 sur 53 », vérifié par ses deux termes (566-A)

```text
borne BASSE — au moins une clé de raison      53
borne HAUTE — toute clé à valeur chaîne       53
les deux portent sur le MÊME ensemble        OUI (identité mesurée)
```

Contrairement au « 156 sur 6 » du 540, **les deux termes comptent le même
objet** : ce sont deux filtres appliqués à la même liste. Le ratio ne dit rien
d'arithmétique, mais il est juste — le filtre étroit ne retire personne. Après
correction, il devient **42 sur 42**, avec la même propriété.

## Ce que le dépôt fait bien, mesuré

- **Zéro refus JSON muet, sur 42 comme sur 53.** La conclusion du 542 survit
  intacte à la correction de son propre compte.
- **Onze refus sont doublement explicites** — drapeau négatif **et** code HTTP.
  C'est précisément ce zèle qui a fait doubler leur comptage : le défaut de
  l'instrument venait d'une qualité du code.
- **`desk.py` explique toujours 100 % de ses refus**, avec quatre messages
  distincts (« nom invalide », « backup introuvable », « payload invalide »,
  « backup illisible »).
- **Aucun cumul par page** : le corpus serveur est lu proprement, une fois par
  fichier.

## Portée — ce que ce lot NE dit PAS

- **Rien n'est corrigé dans le 542** : la correction est **en ajout**, ici.
- **Le contrat d'ÉCHEC reste non observé** — le 542 le disait déjà, et ce lot ne
  provoque aucun échec.
- Les 42 ne sont pas relus un par un : le lot **recompte**, il ne réévalue pas
  le contenu des messages.
- **Un chiffre lourd reste** : 103 états (541).

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
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0**.

Aucun dossier. **Six chiffres lourds sur sept sont reproduits et qualifiés.**

Ce que je retiens, et c'est inconfortable : **j'avais raison, et ça n'a pas
suffi.** La prédiction — « pas de cumul par page, c'est du Python » — était
exacte, vérifiée, et publiable telle quelle. Elle m'aurait fait fermer le lot sur
un « 53 confirmé ». Le double compte était ailleurs, dans une propriété du
prédicat que seule la lecture ligne à ligne du banc pouvait révéler : deux règles
sur un même parcours, sans rien pour les empêcher de se recouvrir. **Une
prédiction juste protège du faux qu'on attendait, pas de celui qu'on n'attendait
pas.**

Trois règles neuves :

- **567-A · UNE PRÉDICTION JUSTE NE PROTÈGE PAS DU DÉFAUT VOISIN** — « pas de
  cumul par page » était vrai ; un cumul par règle se tenait à côté.
- **567-B · DEUX RÈGLES SUR UN MÊME PARCOURS SE RECOUVRENT SI RIEN NE
  L'INTERDIT** — `ast.walk` visite le `Return` puis le `Call` qu'il contient ;
  sans marquage, un nœud qui satisfait les deux est compté deux fois.
- **567-C · LA PROXIMITÉ DE LIGNE N'EST PAS LA CONTENANCE** — le bon nombre par
  la mauvaise preuve reste indistinguable d'un faux ; seule l'identité de nœud
  tranche.

Feuille : **37 ou 38 dossiers annoncés — non tranché** ; relevé strict **35 + 5
candidats ambigus + 531-A** (ampleur **quatre chargeurs**).

Dettes nommées restantes : **UN chiffre lourd encore NON RECOMPTÉ** — 103 états
(541) ; **les 42 refus, jamais relus un par un** ; **les 4 refus non-JSON du
542** ; **les 74 variables serveur sans aucune atténuation** ; **les 67
atténuations non affichées** ; **les 25 atténuations de la bibliothèque tierce** ;
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

Comptes séparés : résultats faux **arrêtés avant publication 193 (+1)** ;
**publiés puis corrigés 32 (+1)** ; **interprétations retirées 10 (+1)**.

**Dix bilans — n°9 à n°18 — attendent une réponse. La question du 521 reste
posée : m'autorisez-vous à appeler les 23 routes, verrou réseau posé ? Et le
531-A attend toujours un GO pour être corrigé.**
