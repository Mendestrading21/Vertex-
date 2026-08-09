# SKYLER LOT 483 — Les six derniers « dossiers à classer » lus un par un : UN SEUL est encore à classer, et aucun des six n'est une correction

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-483` (base : lot 482 fusionné,
`0d08c478`)

Suite directe du 482, qui avait retiré quatre numéros d'une liste de dix en
montrant que **chaque rapport se déclarait lui-même non-dossier**. Restaient six.
Ce lot les lit tous, **et vérifie en plus dans le code d'aujourd'hui** que le
défaut décrit existe encore — un rapport écrit soixante lots plus tôt peut
décrire un site depuis corrigé (leçon 473).

**Aucun code, aucun gardien, aucun test.**

## Les deux contrôles, selon la règle du 481

**Contrôle 1 — cas dont la réponse est connue.** Témoin positif : le site de
persistance breadth du 391, que je sais présent (reproduit deux fois, au 391 et
au 396). Témoin négatif : une chaîne inventée. Les deux écrits **dans le code du
détecteur** (leçon 463) avec sortie en cas d'échec.

```text
POSITIF  READONLY dans config.py            attendu PRESENT -> PRESENT  OK
NEGATIF  chaine inventee zzz_inexistant     attendu ABSENT  -> ABSENT   OK
391      _bh[-1] = _snap                    PRESENT, terminal.py:508, aucune garde DEMO
```

**Contrôle 2 — un cas que l'instrument EXCLUT.** Mon instrument lit la liste
d'attente **par ses étiquettes** : « 388 (MSFT) ». Or le rapport 388 ouvre
**deux** pistes, et l'étiquette n'en nomme qu'une — la seconde
(`skyler_sessions.json` pollué par les tickers synthétiques SKYX/TSTQ, « versé
aux dossiers ») **est invisible à une lecture par étiquette**.

Mesuré : **19 fichiers citent SKYX ou TSTQ** (dont 9 `.pyc`), **3 sources
touchent le journal de sessions — et les 3 redirigent leur stockage**.

```text
tests/test_caches_runtime_lot388.py    redirige=True   touche_sessions=True
tests/test_skyler_core.py              redirige=True   touche_sessions=True
tests/test_xss_exits_lot177.py         redirige=True   touche_sessions=True
-> fichiers touchant les sessions SANS redirection : 0
```

**Et la lecture est confirmée PAR EXÉCUTION** — le passage de suite de ce cycle
même : les fichiers runtime modifiés sont `ai_enrichment.json`, `desk_data.json`
et `weekly_snapshot.json`, **les trois horodatages connus**.
`skyler_sessions.json` **n'y figure pas**. Le détecteur statique disait « tous
redirigent » ; la suite le prouve (leçon 476 — l'exécution décide).

**Le second volet du 388 est SOLDÉ.** L'exclusion par étiquette était donc sans
conséquence **cette fois** — et je le dis ainsi plutôt que « justifiée » : elle
l'a été par chance, pas par construction. Si le volet avait été ouvert, une
lecture par étiquette l'aurait perdu.

## Les six, un par un

### 363 — « points réels du scan » → NON-DOSSIER (le rapport le dit)

Site vivant : `markets_page.py:600`, `'…(points réels du scan, non interpolés).'`.
Mais le 363 titre lui-même la section **« Une observation, pas un défaut »** et
écrit : « Ce n'est donc **pas une fausse affirmation**, mais le mot est ambigu à
côté d'un badge « démo » … **à vous de trancher**. »

Ce « réels » qualifie une **méthode** (maturités effectives, points non
interpolés), pas une provenance ; la carte porte par ailleurs `source: demo` en
mode démo. **Question de style sur un octet servi, pas défaut d'honnêteté.**

### 379 — `context()` sur univers vide → DOSSIER, et le SEUL encore à classer

Le seul des six dont le comportement méritait d'être **réexécuté**. Fait
aujourd'hui, moteur réel :

```text
context(None, None, [], {}, [])
  vix, vix_band, spy_regime  -> None                       ← honnête
  roro                       -> 'NEUTRE'
  roro_gap                   -> 0
  breadth                    -> {above50:0, above200:0, adv:0, dec:1, …}
  verdict                    -> 'MARCHÉ · NEUTRE · participation 0% au-dessus MM50'
```

**Le comportement du 379 tient à l'identique**, soixante-quatre lots plus tard.

Ce que le 379 n'avait pas établi et que ce lot ajoute — **la chaîne jusqu'à
l'écran** : `terminal.py:558` appelle `market.context(...)` dans le scan vivant,
`:612` verse le résultat dans `scan_state['market_ctx']`, et **trois pages
servies le lisent** : `briefing.py:33-36` (phrase de régime), `markets_page.py:268`
(« Risk-on / risk-off »), `intelligence_page.py:375` (ligne « RoRo »). Le verdict
affirmatif **atteint le produit**.

Ce que je n'établis PAS : **le cas déclencheur**. Le site d'appel n'a **aucune
garde sur `rows`**, mais un scénario où le benchmark se télécharge et où les
517 autres échouent tous n'est **pas démontré**. L'accessibilité est un test, pas
une intuition (469) — et je ne l'ai pas fait tourner.

**→ rang 3**, avec les critères **absolus** exigés par le 480 : (a) la sortie est
**servie** sur 3 pages — établi ; (b) elle **affirme** une mesure au lieu de
s'abstenir, ce que l'invariant n°4 interdit — établi ; (c) **le cas déclencheur
n'est pas établi** — c'est ce troisième point, et lui seul, qui l'empêche de
monter. Aucune comparaison à un autre dossier n'entre dans ce rang.

### 386 — le marqueur `src = 'ibkr'` → NON-DOSSIER (décision produit)

`terminal.py:2249` pose bien `e['src'] = 'ibkr'` avec le commentaire
« provenance temps réel (honnêteté §4) ». Remesuré aujourd'hui :

```text
indices_live   dans vertex/ui/ + static/js : 0 occurrence
['src']        dans vertex/ui/ + static/js : 0 occurrence
.src           2 occurrences — vx-router.js, l'attribut src d'une balise <script>
```

Et les trois rendus « TEMPS RÉEL IBKR » du dépôt tombent **tous dans des
constantes `PAGE_*` mortes** — `PAGE_DAILY` (L3807), `PAGE_WATCHLIST` (L4161),
`PAGE_ME` (L5029), les constantes du 374 qu'aucune route ne renvoie.

Le rapport conclut lui-même : « Ce n'est **pas** une malhonnêteté … **Rien à
corriger sans décision produit** (afficher un badge de provenance changerait des
octets servis). » Un cours différé reste un cours réel. **Décision, pas défaut.**

Second volet du 386 (`bret = 0.0` dans `edge_backtest`) : le rapport le classe
« **caractérisation, pas correction** », avec trois faits qui l'empêchent d'être
une faute — défaut **déclaré** de la fonction, chemin de scan vivant passant un
`bench_ret` réel, `scan_state['edge']` **lu par aucune page servie**.
**NON-DOSSIER**, déjà gelé par gardien.

### 388 — les 7 points MSFT fabriqués → DÉCISION sur donnée runtime, pas code

Encore présents, vérifiés aujourd'hui dans `gex_history_cache.json` : la clé
`MSFT` porte des points aux valeurs **strictement identiques** (`net_gex`
36 784 000, `spot` 440.0, `zero_gamma` 429.6) là où `ACN` et `ADBE` varient. Le
rapport : « **je ne la supprime pas de ma propre initiative** … une décision à
prendre, pas un effet de bord d'un lot. » **La cause de code est corrigée depuis
le 388 lui-même** ; ce qui reste est une purge de données de l'utilisateur.

### 391 / 396 — le scan DEMO écrivant l'historique breadth

**391 = DOSSIER RÉEL, et il porte DÉJÀ un rang** : « le dossier part au **rang 1**
du classement du lot 390 ». Site vérifié aujourd'hui, `terminal.py:503-512`,
**aucune garde `DEMO` dans les quatorze lignes qui précèdent**, et l'écrasement
`_bh[-1] = _snap` toujours là. C'est une **décision** (trois issues défendables,
énumérées par le 391), pas une correction évidente.

**396 = NON-DOSSIER.** Son en-tête : « **Aucun code. Aucun gardien. Aucun test
ajouté.** » C'est un lot de vérification qui **reproduit** le 391 et le nomme
comme tel. Même genre que les 411/426 du 482 : **recoupement**.

### 456 + 459 — `symbols_usable` → DOSSIER, DÉJÀ CLASSÉ rang 2

Sites vérifiés : `options_intel_api.py:133` `top=30`, `gex_scan.py:74`
`'symbols_usable': len(rows)`. Et le 459 écrit noir sur blanc :
« **Requalification : rang 4 « par lecture » → RANG 2, établi par exécution.** »

**Il n'était pas « à classer » — il est classé depuis le 459, par exécution.** Ce
qui lui manque est un **chiffrage**, comme au 422 et au 431. La liste le portait
au mauvais rayon.

## Le compte

```text
entrée        verdict de ce lot                          destination
363           NON-DOSSIER (« observation, pas défaut »)   décision de style
379           DOSSIER — rang 3 posé ici                   décision (moteur)
386 badge     NON-DOSSIER (décision produit)              décision
386 bret      NON-DOSSIER (caractérisation gelée)         —
388 MSFT      NON-DOSSIER de code (donnée runtime)        décision
388 SKYX      SOLDÉ (0 fichier sans redirection)          clos
391           DOSSIER — rang 1 DÉJÀ posé au 390           décision
396           NON-DOSSIER (recoupement du 391)            clos
456+459       DOSSIER — rang 2 DÉJÀ posé au 459           à chiffrer
```

**Dossiers en attente de CLASSEMENT : 6 → 0.** Un seul rang a été posé
aujourd'hui (le 379). Deux étaient déjà posés et mal rangés. Quatre entrées ne
portaient aucun défaut propre.

**Et le résultat le plus net : aucun des six n'est une correction ordinaire.**
Tout ce qui survit est une **décision** — de conception (391), de moteur (379),
de produit (386), de données (388), de style (363). La liste « à classer »
n'attendait pas un classement : elle attendait **des arbitrages humains**.

## Mutualisation — cherchée, et absente

Trois des six partagent une **famille** : le produit affirme quelque chose qu'il
n'a pas établi (363 le mot « réels », 379 le verdict sur rien, 386-bret une force
relative devenue absolue). Deux rapports emploient même le mot : le 379 se dit
« jumeau du 363 », le 386 « jumelle du dossier `context()` du 379 ».

**Mesuré : la parenté est de FAMILLE, pas de SITE.** `markets_page.py:600`,
`vertex/market/context.py`, `terminal.py` `edge_backtest` — trois fichiers, trois
mécanismes, **aucune ligne commune, aucun correctif commun**. Fusionner sur le mot
« jumeau », comme le 478 l'a fait à raison pour 406+407 qui partageaient une
cause, serait **ici une erreur**.

**Fait de méthode : « jumeau » dans un rapport est une affirmation de FAMILLE ;
la traiter comme une affirmation de SITE fusionnerait deux dossiers qui n'ont ni
correctif ni fichier en commun.** C'est la dix-septième récurrence du piège de
l'homonyme, sous une forme neuve — non plus deux choses portant le même nom, mais
**un même mot désignant tantôt une ressemblance, tantôt une identité**.

## Un défaut de mon propre instrument, attrapé en lisant sa sortie

Mon localisateur de constantes `PAGE_*` indexait les intervalles **dans un
dictionnaire par NOM**. Il y a **huit affectations `PAGE_DAILY`** : les sept
premières étaient écrasées par la dernière, et la ligne 3807 ressortait « hors
constante » alors qu'elle est dans `PAGE_DAILY`.

Corrigé en liste de triplets — 18 affectations, **18 intervalles distincts** — et
recalibré sur une réponse connue (la ligne 4741, début déclaré de `PAGE_ME` au
386, doit tomber dans `PAGE_ME` : **OK**). **ÉCRASER N'EST PAS ACCUMULER**, pour
la troisième fois après les 464 et 465, et cette fois dans un dictionnaire Python
de mon propre script.

**Arrêté avant publication 47 → 48.**

## Portée

- **Je n'ai pas rejoué les mesures internes des six rapports** (les 46 et 38
  `except: pass`, les 12 fractions, les 16 points breadth). J'ai vérifié **ce que
  chaque rapport DIT être** et **si son site de code existe encore**. Deux
  épreuves, pas trois.
- Le seul comportement **réexécuté** est `context()` sur univers vide. Les autres
  vérifications sont des **lectures de site** (`grep` line-exact), pas des bancs.
- **L'accessibilité du cas déclencheur du 379 n'est PAS établie** — c'est écrit
  dans son rang.
- Les numéros de ligne des rapports 386 et 456 sont **périmés** (L621 → 2249,
  L165-168 → 167) : `terminal.py` fait 7 153 lignes après la purge É1. Les sites
  ont été retrouvés par **motif**, pas par ligne. Confirmation directe de la
  leçon 473.
- Le verdict « `PAGE_*` mortes » est **repris** du 374, pas remesuré ici ; ce que
  je mesure, c'est que les trois rendus IBKR **y tombent**.
- **Aucun navigateur ouvert.** Aucune conclusion visuelle.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; scripts du scratchpad
  avec `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier de production touché** — pas de preuve MD5 requise par le
  rituel ; remesurée quand même. Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé **et vérifié** (`cache_path()` suit la redirection).
  `context()` appelé en mémoire — il n'écrit que dans son `out`. **Aucun écrivain
  appelé, aucune route réseau sortante.**
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; restauration vérifiée par **md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Le 482 avait vidé quatre entrées sur dix ; ce lot vide les six restantes. **La
liste « dossiers en attente de classement » est close.**

Ce qu'elle laisse derrière elle n'est pas rien, mais ce n'est pas ce que son nom
promettait : **sept arbitrages humains** et **un chiffrage**. La boucle a passé
des dizaines de lots à accumuler une liste dont l'intitulé — « à classer » —
suggérait un travail d'agent, alors que son contenu réel appelait des décisions
qui ne m'appartiennent pas.

Comptes séparés : résultats faux **arrêtés avant publication 48 (+1)** ; publiés
puis corrigés **8** ; interprétations retirées **3**.

**Huit bilans — n°9 à n°16 — attendent une réponse.**
