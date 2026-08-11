# SKYLER LOT 469 — Les deux dettes du 468 soldées, et l'une CONTRE ma propre inclinaison : le board sélectionne bien des contrats sous le minimum absolu de la Constitution, par une SECONDE source de configuration qui la contredit

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-469` (base : lot 468 fusionné,
a302701)

Quarante-neuvième lot de la veine, **dernier lot de la tranche 460-469**. Un
dernier lot solde, il n'ouvre pas de front (modèle 449/459/465). Le 468 laissait
deux dettes, toutes deux nommées et non classées. **Les deux sont soldées.**

**Aucun code, aucun gardien, aucun test.**

## Dette (a) — le seuil DTE : ATTEIGNABLE, et je m'étais trompé

Le 468 écrivait, dans sa Portée : « un contrat à moins de 60 jours **n'atteint
probablement jamais** le board ». **C'est faux, et la mesure le dit sans
ambiguïté.**

### La chaîne, remontée jusqu'au bout

```text
scan_state['options_board']
   ← legacy_engine.build_board / terminal.py:1073 / :1586 / weekly.py:222
   ← best_for_symbol(sym, spot, target, direction, …, buckets=…)
   ← _pick_expiries(list(tk.options), now, buckets)
   ← yf.Ticker(sym).option_chain(exp)          ← LA CHAÎNE BRUTE, DIRECTEMENT
```

**`best_for_symbol` va chercher sa chaîne lui-même chez le fournisseur. Il ne
passe NI par `chain_loader`, NI par `contract_filter`** — les deux modules qui
appliquent `dte_within_constitution`. Ceux-là servent `call_selector` et
`bearish_tactical`, **pas** le board.

Le filtre DTE réellement appliqué est donc `OPTION_BUCKETS`, dans
`vertex/strategy/config.py:31` :

```text
court  min  25  ·  target  45  ·  max   75
moyen  min  75  ·  target  90  ·  max  135
long   min 150  ·  target 210  ·  max  400

Constitution V2   options_profile.dte.absolute_minimum = 60
computeVerdict    avertit en dessous de 20
```

### Et les quatre écrivains du board demandent tous le bucket court

```text
terminal.py:1073-1074   buckets=('court', 'moyen', 'long')     focus
terminal.py:1586-1587   buckets=('court', 'moyen', 'long')     rotation
legacy_engine.py:336    buckets=('court', 'moyen', 'long')     build_board (calls)
weekly.py:222           buckets=('court', 'long')              hebdo
```

**Un contrat à 25 jours atteint donc le board, et la CIBLE du bucket court est
45 jours — sous le plancher de 60 de la Constitution.** Ce n'est pas un cas
limite : c'est la zone visée.

### Ce que ce n'est PAS — et c'est ce qui décide du rang

J'ai cherché si l'écran affiche la borne de 60 :

```text
« DTE absolu » · « absolute_minimum » · « 60-540 »  →  AUCUN OBJET SERVI
```

Le seul rendu qui l'affiche, `intelligence_page.py:513`, appartient à un module
**non servi** (`/vertex-intelligence` est une redirection 301, mesuré aux
466/467). **Aucun nombre faux n'est donc à l'écran**, et le seuil de 20 de
`computeVerdict` ne contredit rien d'affiché.

### Classement — rang 3

Ce qui est établi : **le produit sélectionne, de façon nominale et voulue, des
contrats sous le minimum absolu de sa propre Constitution**, et il le fait par
une **seconde source de configuration** qui la contredit. Le commentaire de
`config.py:29` l'assume :

> « Le profil = options 6-12M (long, défaut). L'utilisateur veut AUSSI explorer
> le court (1-3 mois, tactique, théta violent). »

C'est **une décision de produit consignée dans un commentaire, pas dans la
Constitution** — laquelle pose `absolute_minimum: 60` **sans exception**, et est
verrouillée par `tests/test_constitution_v2.py`. Deux configurations se
contredisent, et **le code suit celle qui n'est pas la Constitution**.

Rang 3 et pas plus : rien de faux à l'écran. Rang 3 et pas moins : la politique
de sélection réelle diffère du document que le reste de l'application traite
comme faisant autorité.

**Genre neuf : DEUX SOURCES DE CONFIGURATION QUI SE CONTREDISENT, ET LE CODE
SUIT CELLE QUI N'EST PAS LA CONSTITUTION.**

Et un fait mesuré qui le rend net : **le dépôt possède un sélecteur qui respecte
la Constitution (`contract_filter.dte_within_constitution`, appliqué par
`call_selector` et `bearish_tactical`) et un qui l'ignore — et c'est le second
qui remplit le board.**

## Dette (b) — l'équivalence d'échelle : RÉFUTÉE

Le 468 se demandait si « À surveiller » à 56/100 tombait sous le plancher de
refus 24 de la Constitution. **Mesuré : la question ne se pose pas.**

```text
analysis.py:228   score = int(max(0, min(100, base_score + struct_adj)))   → /100
skyler_score.blocks = {5,5,6,4,4,6,6,4}  somme = 40                        → /40
conviction_levels   score_min 36 · 32 · 28 · 24                            → /40
```

**Deux moteurs, deux grandeurs.** Le score du scan (`analysis.py`, technique) et
le score de conviction (`skyler_core`, décisionnel) ne mesurent pas la même
chose et ne l'ont jamais prétendu. Les seuils 72/66/56 de `bucketOf` portent sur
le premier ; les 36/32/28 de la Constitution sur le second.

**L'insinuation du 468 est retirée.** Et la conversion défensive de `tierOf`
(`sc<=40 ? sc : Math.round(sc/2.5)`) **confirme** que le dépôt connaît la
dualité et s'en protège.

**Onzième récurrence du piège des homonymes** — et d'une forme nouvelle : jusqu'ici
c'était *un même nombre n'est pas une même grandeur* ; ici c'est **un même NOM de
champ — `score` — qui désigne deux grandeurs produites par deux moteurs.**

## Mes comptes, et celui-ci n'est pas confortable

Le 468 a **publié** — dans sa Portée, hedgé d'un « probablement », et sans
classer — que le contrat court « n'atteint probablement jamais le board ».
**Un lecteur du 468 en serait reparti avec une croyance fausse.**

**Je le compte : publiés puis corrigés, 3 → 4.** Le fait de ne pas l'avoir
classé n'efface pas de l'avoir écrit. Ce qui a sauvé le dossier, c'est d'avoir
écrit « non tranché » **dans le verdict** au lieu de « inatteignable » — la
prudence dans la conclusion a rattrapé l'imprudence dans la marge.

Symétriquement, la dette (b) était nommée « non tranché, non compté » : sa
réfutation ne coûte rien, **parce que rien n'avait été affirmé.**

## Ce que le lot ne prétend pas

- La chaîne est établie **par lecture** : `best_for_symbol` appelle
  `yf.Ticker(...).option_chain(...)`, et **je n'ai appelé aucun réseau** pour le
  vérifier. Ce qui est prouvé, c'est l'**absence de `chain_loader` et de
  `contract_filter` sur ce chemin**, et les **quatre sites** qui passent
  `('court', …)`.
- Je n'ai **pas** mesuré la proportion réelle de contrats sous 60 jours dans un
  board réel : `scan_state['options_board']` est vide au démarrage. Ce qui est
  établi, c'est que **le bucket court les demande et que sa cible est 45**.
- Le bucket est un **choix assumé** dans un commentaire. **Je ne juge pas ce
  choix** — je mesure qu'il n'est pas dans la Constitution et qu'il la contredit.
- L'absence d'affichage de la borne 60 est établie sur les **42 objets servis**.
- **Aucun navigateur ouvert. Aucun réseau. Aucun écrivain appelé.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; scripts du scratchpad
  avec `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`. `constitution.load_profile()` et lecture de
  `strategy/config.py` en mémoire ; pages en **GET** ; `persist` redirigé ;
  **`/options/<sym>`, `/api/analyst/`, `/api/correlations/`, `/desc/<sym>` NON
  appelées**.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; restauration vérifiée par **md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle — fin de la tranche 460-469

Soixante-douzième lot court, **dixième et dernier de la tranche**.

Il fait ce qu'un dernier lot doit faire : il **solde**, et il solde **dans les
deux sens**. Une dette est confirmée **contre mon inclinaison** — le board va
bien chercher sous la Constitution — et l'autre est **réfutée**, l'insinuation
retirée.

Le fait de méthode est le plus inconfortable de la tranche, et c'est le bon
moment pour l'écrire, à la veille du bilan : **l'atteignabilité a tué trois
candidats dans cette tranche (462, 465, 468) et j'ai commencé à m'en servir
comme d'un réflexe.** Le quatrième cas montre le prix de ce réflexe : **j'ai
supposé l'inatteignabilité au lieu de la mesurer, et j'ai eu tort.**

*L'atteignabilité est un test, pas une intuition. Elle doit se mesurer dans les
deux sens — et une chaîne « probablement filtrée » qui n'a pas été remontée
jusqu'au fournisseur n'est pas filtrée du tout.*

Comptes séparés : résultats faux **arrêtés avant publication** **40** ;
**publiés puis corrigés** **4** (+1, le « probablement inatteignable » du 468) ;
**interprétations retirées** **2** (+1, l'insinuation d'échelle du 468).

**Sept bilans — n°9, n°10, n°11, n°12, n°13, n°14 et n°15 — attendent une
réponse ; le bilan n°16 sera écrit au lot 470.**
