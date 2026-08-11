# SKYLER LOT 454 — Les six phrases `action` sont des ordres d'entrée chiffrés, calculés à chaque scan, sérialisés, envoyés au navigateur — et **lus par personne**

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-454` (base : lot 453 fusionné,
c1e5f04)

Trente-cinquième lot de la veine, quatrième de la tranche 450-459. Trois lots de
balayage structurel d'affilée (451 appelants, 452 atteignabilité, 453 contrats de
route), le dernier refermé négativement : **la règle du 416 s'applique — changer
de famille.** Retour aux **moteurs et aux phrases**, sur le plus gros bloc non
ouvert de la carte du 444 : **`action`**, 6 phrases, 3 écrans annoncés.

**Aucun code, aucun gardien, aucun test.**

## Étape 0 — que veut dire le champ, et un détecteur qui a failli mentir

Première passe AST, sur les **dictionnaires littéraux** seulement :

```text
`action` — phrases COMPOSÉES au serveur : 0
`action` — valeurs littérales : 19   'ATTAQUER' · 'RÉDUIRE / DÉFENSIF' · 'BUY'
                                     'SELL' · 'HOLD' · 'REEVALUATE'
                                     'DATA_REPAIR_REQUIRED' · …
```

**J'allais publier un zéro faux.** Le détecteur ne connaissait qu'**une** forme
d'écriture. Élargi à **quatre** — `{'action': …}`, `d['action'] = …`,
`f(action=…)`, et l'**affectation de variable** `action = …` :

```text
action     6 composées   [dict 0 · d[k]= 0 · kwarg 0 · variable 6]
   engines/decide.py:115, :119                    f-string
   engines/scorecard.py:233, :235, :237, :239     f-string
```

Les six sont des **affectations de variable nues**, la seule forme que la
première passe ignorait. **Neuvième récidive du piège « un détecteur qui ne
connaît qu'UNE forme fabrique de faux manquants »** (414, 429, 436, 441),
arrêtée avant publication. Le compte des faux arrêtés passe de **24 à 25**.

### Le sens du champ — vérifié AVANT de bâtir le plan (leçon 451)

```python
# decide.py:115
action = (f"Entrée vers ${plan.get('entry')}, stop ${plan.get('stop')} "
          f"({plan.get('stop_type', '')}), objectifs ${plan.get('tp1')} / "
          f"${plan.get('tp2')} / ${plan.get('tp3')}.")
# scorecard.py:237
action = f"Entrée optimale sur repli vers ${opt_e} · agressive sur cassure > ${agg_e} · stop ${inval}."
```

Ce ne sont pas des étiquettes : ce sont des **consignes d'entrée chiffrées** —
prix d'entrée, stop, trois objectifs. Sur un terminal d'analyse en lecture seule,
c'est la famille de phrases la plus engageante du dépôt.

**Et `action` désigne au moins quatre charges utiles différentes** — ligne de
recommandation, ligne de réconciliation (`DATA_REPAIR_REQUIRED`), ligne de note
d'analyste, entrée de connexion. **Septième récidive du piège « un nom, plusieurs
payloads ».**

## Étape 1 — l'affichage d'abord

Les deux moteurs sont **atteignables** depuis `terminal.py` (instrument du 452).
Corpus mesuré : **42 objets servis** — 8 pages + `/analysis/AAPL` + 33 JS
statiques non-vendor.

```text
lectures `.action` présentes dans les octets servis
   portfolio_page.py:459   r.action   ligne de RÉCONCILIATION  (.replace(/_/g,' '))
   analysis_page.py:714    r.action   ligne de NOTE D'ANALYSTE (r.to || r.pt_action || r.action)

lectures de la charge utile des DEUX MOTEURS
   decision.action · dec.action · v.action      CITÉES NULLE PART
```

Les deux lectures servies portent sur d'**autres** payloads. **Aucune lecture du
champ produit par `decide` ou `scorecard` n'existe dans les octets servis.**

## Étape 2 — où vont les six phrases, alors ?

**Les quatre de `scorecard.verdict()`** entrent dans `scan_state['recommendations']` :

```python
terminal.py:591-598
   v = ibkr.verdict(d, opt, fu)                      # ibkr = engines.scorecard
   recs.append({… 'raison': v['raison'], 'action': v['action'], …})
terminal.py:614
   scan_state.update({… 'recommendations': recs, …})
```

`/scan` transporte bien la clé (`'recommendations' in payload : True`) et `/scan`
**est** consommé. Mais :

```text
occurrences du mot « recommendations » dans les 42 objets servis : 1
   → /journal, et c'est un AUTRE payload : analysis_api.py:295
     _dm.recommendations(patterns, aggs), lu comme r.proposal
```

**Huitième récidive du piège de nom.** Aucun écran ne lit la liste
`recommendations` du scan.

**Les deux de `decide.decide()`** entrent dans `options_pack()` :

```python
terminal.py:1595   out['decision'] = engine.decide(_d, out)
   servi par  /options/<sym>  (terminal.py:2040)  et  /api/ticker/<sym>  (:1747)
```

`/api/ticker/` **est** consommé — `analysis_page.py:297` — et c'est l'un des 40
sites **sains** du 453 : il lit `company`, `detail`, `in_universe`, `risk_map`.
**Pas `decision`.**

### Le témoin positif : les champs VOISINS de la même ligne, eux, sont lus

```text
champ de la ligne `recs`     présent dans les octets servis
   niveau      OUI   markets · analysis · portfolio · journal · system · 6 builders
   raison      OUI   accueil · markets · opportunities · portfolio · options · journal
   alloc       OUI   portfolio
   action      NON   (les 2 occurrences appartiennent à d'autres payloads)
   score40     NON
```

C'est le contrôle qui rend le verdict solide : l'instrument **distingue**, dans le
**même dictionnaire**, les champs lus de ceux qui ne le sont pas. `raison` et
`niveau`, écrits à la ligne d'à côté, atteignent des écrans. `action` non.

## Classement

**Rang 4.** Six phrases composées à chaque scan, chiffrées, sérialisées dans deux
charges utiles servies, **jamais lues**. C'est la famille 411/424/435/436/446 —
*une conséquence CALCULÉE, SÉRIALISÉE et ENVOYÉE n'est toujours pas AFFICHÉE*.

**Rien de faux n'est montré**, et c'est pour cela que ce n'est pas plus haut. Le
coût est ailleurs : deux moteurs composent des ordres d'entrée chiffrés que
personne ne voit, et un lecteur du code croit raisonnablement l'inverse.

### Ce que cela ne réveille PAS

La phrase de `decide.py` fond `plan.get('stop_type', '')` et
`plan.get('resistance')` dans son texte. **Cela ne rétablit pas** le verdict
« `stop_type` atteint un écran », retiré au 444 : la phrase qui le contient
n'atteint aucun écran. Je le dis pour que le résultat ne soit pas sur-lu.

## Trouvaille annexe — six routes de `feeds.py` que rien ne cite

En cherchant qui consomme `/api/cockpit` (qui sert `{'action': top, …}`, la ligne
de recommandation entière), j'ai mesuré tout le fichier :

```text
vertex/app/routes/feeds.py — 9 routes, citation dans les OCTETS SERVIS
   /api/market/summary     CITÉE   (accueil, markets, vx-core.js)      ← témoin
   /api/market/context     CITÉE                                       ← témoin
   /api/options            CITÉE   (options-structure.js)              ← témoin
   /api/cockpit            citée nulle part
   /api/watchlist          citée nulle part
   /api/search             citée nulle part
   /api/weekly             citée nulle part
   /api/strategie          citée nulle part
   /api/comite             citée nulle part
```

**Trois citées, six non — le témoin positif est dans le même fichier** (motif
451). `/api/cockpit` est maintenue vivante par `tests/test_smoke.py:36` et
`tests/test_feeds_routes.py`, qui vérifie jusqu'à `'/api/cockpit' in rules` :
**un gardien qui impose l'existence d'une route qu'aucun écran n'appelle** —
motif 436/451. **Rang 3.**

### Une correction d'instrument, au passage

Le crible du 453 aurait rangé `/api/options` parmi les non-consommées : son appel
est un `.then(function (d) {...})`, l'une des **15 formes échappées**. **La
recherche de l'URL littérale dans les octets servis n'a pas cet angle mort** et
la retrouve. Je corrige donc, publiquement, une conclusion que le 453 n'a pas
publiée mais que son outil aurait produite.

## Portée

- Je mesure la **citation d'une URL** et la **lecture d'un champ** dans les
  **octets servis** — 42 objets. Une lecture par **déstructuration**, par
  **crochets** ou via un helper à paramètre échapperait (leçon 436) ; **non
  quantifié ici**.
- Une route non citée par un écran peut être appelée **à la main** ou par un
  outil externe. Je mesure ce que le produit appelle, pas ce qui est appelable.
- `scan_state` est **vide au démarrage** : les six phrases n'ont donc pas été
  **exécutées**, elles ont été **lues à la source**. Ce lot établit **où va la
  valeur**, pas ce qu'elle vaut — aucun banc n'était nécessaire, et je n'en ai
  pas fabriqué un pour faire nombre.
- **Aucun navigateur ouvert.**
- Sur les 110 phrases concluantes du 444, **83 restent fermées** (89 − 6).

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; scripts du scratchpad
  avec `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`. Routes en **GET** uniquement, `persist` redirigé ;
  **`/options/<sym>` volontairement NON appelée** (appel réseau sortant).
  Analyse `ast`, `app.url_map` et lecture de source en mémoire.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; restauration vérifiée par **md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Cinquante-septième lot court, quatrième de la tranche.

Le changement de famille a payé au sens où il a rendu un résultat **net et
vérifiable** dès la première mesure, là où les trois balayages précédents
demandaient quatre corrections d'instrument chacun. Mais il faut être exact : le
résultat est un **rang 4**, pas un rang 1. La veine des phrases composées rend
maintenant surtout du **poids mort** — c'est le troisième lot d'affilée
(449 `tradingview_signal_store`, 451 `source`, 454 `action`) où la phrase examinée
n'atteint aucun écran.

Le fait le plus utile du lot est peut-être ailleurs : **le détecteur a failli
publier un zéro**, parce qu'il ne connaissait qu'une forme d'affectation sur
quatre. C'est la neuvième fois.

Comptes séparés : résultats faux **arrêtés avant publication** **25** (+1) ;
**publiés puis corrigés** **3**, inchangé.

**Six bilans — n°9, n°10, n°11, n°12, n°13 et n°14 — attendent une réponse.**
