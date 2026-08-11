# SKYLER LOT 452 — 85 modules sur 299 sont injoignables depuis `terminal.py`, et le balayage tombe sur une COLLISION DE ROUTE : la carte « Anomalies » de `/analysis` lit un contrat servi par une route masquée, donc elle affiche « Aucune anomalie détectée » quoi qu'il arrive

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-452` (base : lot 451 fusionné,
723cb69)

Trente-troisième lot de la veine, deuxième de la tranche 450-459. Le 451 avait
trouvé **269 lignes mortes sans les chercher**. Ce lot généralise : **combien de
modules de `vertex/` le produit n'atteint jamais ?** Le balayage répond — et il
mène, par la chaîne des anomalies, à un défaut affiché d'une nature nouvelle.

**Aucun code, aucun gardien, aucun test.**

## L'instrument, et ses cinq contrôles avant tout chiffre

Mesure : graphe d'imports par **AST** (299 modules `vertex/`, 609 fichiers `.py`
analysés, **0 échec de parse**), puis **clôture transitive depuis la seule vraie
entrée produit, `terminal.py`**.

Le compte des **importeurs directs** ne suffit pas : un module mort qui en importe
un autre le ferait passer pour vivant. Le paquet `research` en donne sept cas.
**C'est l'atteignabilité qui est mesurée, pas le nombre d'importeurs.**

```text
TÉMOIN POSITIF 1   14 / 14 modules de page servis            ATTEIGNABLES
TÉMOIN POSITIF 2   21 / 21 blueprints de vertex/app/routes   ATTEIGNABLES
TÉMOIN POSITIF 3    7 /  7 moteurs canoniques de CLAUDE.md   ATTEIGNABLES
                          (decision_stack, recommendation, skyler_core,
                           track_record, evidence, app.state, services.persist)
TÉMOIN 327          5 /  5 modules reliques de CLAUDE.md     MORTS   (attendu)
TÉMOIN 451          2 /  2 modules du lot précédent          MORTS   (attendu)
                          vol_surface, tool_registry — retrouvés SEULS
```

Le cinquième contrôle est celui qu'exigeait la règle du 443 : **l'instrument
retrouve sans qu'on le guide la trouvaille du lot précédent**. Le quatrième
retrouve une trouvaille de la documentation, écrite au lot 327.

### Ce qui échappe, quantifié

Les imports **dynamiques** échappent à une analyse AST. Mesuré : dans tout le
dépôt, **deux fichiers** contiennent `importlib` ou `__import__`, et un seul est
de production :

```python
vertex/data/company.py:231    __import__('datetime')      # bibliothèque standard
tests/test_promesses_imbriquees_lot393.py                 # un test
```

**Aucun module `vertex/` n'est importé dynamiquement.** L'angle mort existe ; il
est vide, et je l'ai mesuré plutôt que de le supposer.

## Le recensement

```text
modules vertex/ au total                            299
ATTEIGNABLES depuis terminal.py (clôture)           214
NON ATTEIGNABLES                                     85     6 192 lignes
   dont couverts par au moins un TEST                55     4 869 lignes
   dont aucun test                                   30     1 323 lignes

fichiers de tests important au moins un module mort  33 / 301   (4 433 lignes)
```

```text
non atteignables par paquet
   research         23 modules ·   785 lignes
   data_sources     12 modules ·   860 lignes
   options           9 modules ·   867 lignes
   strategy          8 modules ·   164 lignes
   ai                7 modules ·   311 lignes
   ui                5 modules ·  1 578 lignes   ← les 5 reliques du 327
   scanner           4 modules ·   317 lignes
   catalysts         3 · observability 3 · portfolio 3 · anomalies 2
   validation 2 · visualization 2 · engines 1 · market 1
```

**Le 451 n'était pas isolé.** Ses 269 lignes sont **4,3 %** du total. Le motif
qu'il décrivait — *du code mort figé par ses propres gardiens* — porte ici sur
**55 modules et 4 869 lignes**, défendus par **33 fichiers de tests**.

### Ce que ce chiffre ne dit PAS

Un module non atteignable **n'est pas nécessairement à supprimer** : `research/`
et `research/institutional/` ressemblent à une bibliothèque de travaux en attente
de branchement, pas à des reliques. Le balayage mesure **l'atteignabilité**, pas
l'intention. Et il mesure des **modules**, jamais des **fonctions** : un module
atteignable peut contenir des fonctions sans appelant — c'était le cas du 451, et
ce lot-ci ne le mesure pas.

## Où le balayage a mené : une phrase servie qui nomme deux moteurs morts

`vertex/anomalies/option_anomalies.py` et `vertex/options/vol_surface.py` sont
**tous deux non atteignables**. Or `/opportunities` les nomme, en **texte
visible** :

```javascript
$('op-anom').innerHTML = VX.states.empty(`Anomalies « ${group} » : détectées par
  symbole — ouvrir une analyse pour le détail (moteurs option_anomalies /
  vol_surface / portefeuille).`, …)
```

Mesuré sur les octets servis : `/opportunities` **200, 67 278 o, md5
6a22a6abbd03** (identique à la référence), la phrase **présente, 1 occurrence**,
et les **six** puces servies. Deux puces ont un rendu propre — `Actions` (table du
scan) et `Données` (`/api/data-quality`). **Les quatre autres — Options,
Volatilité, Portefeuille, Modèles — tombent dans le `else` et affichent cette
phrase.**

**Témoin positif sur le même écran** : la puce `Actions` est servie par
`vertex/anomalies/stock_anomalies.py`, **atteignable** (`terminal.py:38`). Sur la
même carte, un groupe vivant et quatre groupes qui renvoient à des moteurs que le
produit n'exécute jamais.

## La trouvaille : deux routes GET sur la même URL, et la carte lit la perdante

En vérifiant la promesse « ouvrir une analyse pour le détail », je suis tombé sur
autre chose.

```text
règles enregistrées sur /api/anomalies/<sym>   : 2
   analysis_api.api_anomalies      GET
   strategy_os.anomalies_for       GET
endpoint RÉELLEMENT résolu par Flask           : analysis_api.api_anomalies
```

Les deux rendent des **formes différentes** :

```text
analysis_api.api_anomalies   (GAGNANTE, mesurée en direct)
   as_of closes empty events extreme generator n_spikes narrative
   points reason series_source streak symbol vol_ratio
   → PAS de clé 'anomalies', PAS de clé 'note'

strategy_os.anomalies_for    (MASQUÉE, jamais atteinte)
   {'symbol', 'anomalies': [...], 'note': '...'}
```

Et voici ce que `/analysis/<sym>` fait de cette réponse, dans `loadDossier()`
(appelée au chargement, `analysis_page.py:929`, et rafraîchie toutes les 180 s) :

```javascript
const a = await VX.fetch('/api/anomalies/' + SYM, {ttl:120000});
body('an-anomalies', (a.anomalies && a.anomalies.length)
  ? a.anomalies.map(x => `<span class="vx-badge" title="${esc(x.impact||'')}">${x.code}</span>`).join('')
    + `<div class="vx-meta vx-mt2">${esc(a.note||'')}</div>`
  : VX.states.empty('Aucune anomalie détectée sur la série disponible.'));
```

`a.anomalies` et `a.note` sont **les deux clés de la route masquée**. Sur la route
qui répond réellement, elles sont **absentes** — vérifié par lecture exhaustive :
`engines/anomaly.py` n'a que **deux** `return`, et **aucun des deux** ne porte
`anomalies` ; la route n'ajoute que `symbol`, `series_source`, `as_of`.

**La carte « Anomalies » de `/analysis/<sym>` affiche donc, en toutes
circonstances, « Aucune anomalie détectée sur la série disponible. »**

### Le banc : ce que le produit dit, contre ce que le produit sait

Moteur réel `vertex/engines/anomaly.scan()`, cas sain et cas dégradé côte à côte :

```text
A. série 81 clôtures, choc +16 % en dernière barre
   n_spikes    1
   vol_ratio   11.84
   extreme     high
   narrative   « 1 mouvement(s) statistiquement anormal(aux) détecté(s) sur la
                 fenêtre (dernier : +16.0 %, z=8.4). La volatilité récente est
                 ×11.8 la normale — dimensionnement à adapter. … »

   ce que la carte « Anomalies » affiche :
               « Aucune anomalie détectée sur la série disponible. »

B. série 10 clôtures (sous MIN_POINTS = 21)
   empty True · points 10 · reason « série trop courte (10 points, 21 requis) »
   ce que la carte affiche : « Aucune anomalie détectée sur la série disponible. »

   → la carte rend le MÊME texte dans les deux cas : elle ne distingue pas
     « rien d'anormal » de « anomalie détectée » ni de « série trop courte ».
```

Le cas sain tombe juste : le moteur **détecte**, il le dit, il le chiffre. C'est
la carte qui ne le lit pas.

### Le témoin positif est sur la MÊME PAGE

`/analysis/<sym>` porte **deux** cartes d'anomalies, servies par la **même**
requête :

```text
id="an-anomaly"    « Scanner d'anomalies — qu'est-ce qui sort de l'ordinaire ? »
                   rendue par charts/anomaly-scan.js
                   lit d.closes · d.events · d.narrative · d.reason   → HONNÊTE

id="an-anomalies"  « Anomalies »  (vx-card, vx-col-7)
                   lit a.anomalies · a.note                            → JAMAIS PRÉSENTES
```

Les deux sont dans les octets servis de `/analysis/AAPL` (200, 75 829 o). La
carte honnête est **à quelques centimètres** de celle qui se tait. L'instrument
distingue, sur le même écran, la lecture juste de la lecture morte.

### Et un témoin NÉGATIF, gratuit : trois autres doublons d'URL sont légitimes

```text
/api/anomalies/<sym>          GET   +  GET      ← collision RÉELLE
/api/client-log               GET   +  POST     légitime
/api/tracking                 GET   +  POST     légitime
/api/tracking/<tracking_id>   GET   +  PATCH    légitime
```

Quatre URL portent deux règles ; **une seule** oppose deux `GET`. Le détecteur ne
crie pas au loup sur les trois séparations de méthode.

## Les gardiens : deux verts, un de chaque côté de la collision

```text
tests/test_strategy_os_routes.py::test_anomalies_route
    monte un Flask NU avec le SEUL blueprint strategy_os → pas de collision
    assert isinstance(data['anomalies'], list)            → VERT

tests/test_anomaly_engine.py::test_anomalies_route_reads_real_series
    utilise terminal.app RÉEL → obtient la route gagnante
    assert d['n_spikes'] >= 1                             → VERT

tests/test_anomaly_engine.py::test_analysis_page_has_anomaly_card
    assert 'an-anomaly' in body                           → VERT
    (la carte SINGULIER, l'honnête ; jamais 'an-anomalies')
```

Le premier prouve le contrat que la page lit, **sur une application où la route
n'est pas masquée**. Le second prouve le contrat servi, **sans le comparer à ce
que la page lit**. Le troisième vérifie la carte voisine. **Aucun des trois ne
peut voir le défaut** — chacun s'arrête juste avant. C'est le motif 381/385/414/415
dans sa forme la plus nette : *un gardien vert parce que son périmètre s'arrête
avant le défaut*. **Aucun test du dépôt ne compte les règles d'une même URL.**

## Classement

- **Carte « Anomalies » de `/analysis/<sym>` toujours vide → rang 1.** C'est une
  **affirmation fausse affichée** : « Aucune anomalie détectée » alors que la
  charge utile que la carte vient de lire en signale une, chiffrée. Elle ment
  **du côté qui rassure** — famille 432/433. Et elle confond trois états
  distincts en un seul texte.
- **Collision de route `/api/anomalies/<sym>` → cause, classée avec le rang 1.**
  Genre nouveau, à ajouter à la nomenclature : **DEUX ROUTES GET SUR LA MÊME URL,
  LA CONSOMMATRICE LISANT LE CONTRAT DE LA PERDANTE.**
- **Phrase de `/opportunities` nommant deux moteurs morts → rang 2.** Rien de
  chiffré n'est faux ; mais c'est **affiché**, sur quatre puces sur six, et cela
  oriente vers un détail que la page cible **ne peut pas** montrer.
- **85 modules / 6 192 lignes non atteignables, dont 55 testés → rang 3.** Poids
  mort quantifié, et **33 fichiers de tests** qui le figent.

Corrections pressenties — **aucune n'est engagée, aucun GO n'est demandé** :
faire lire à la carte les clés réellement servies (`events`/`narrative`) **ou**
retirer la règle masquée ; retirer des trois autres puces de `/opportunities` la
mention de moteurs que le produit n'exécute pas. Le tri du poids mort est une
**décision de produit**, pas une correction.

## Ce que je ne prétends pas avoir mesuré

- L'atteignabilité est **statique**. Elle est calculée depuis `terminal.py` seul ;
  `verifier_vertex.py`, `ib_reader.py`, `test_connection.py` sont des **outils**,
  volontairement exclus des entrées — les compter aurait gonflé le vivant.
- Le banc appelle le **moteur réel** sur une série **fabriquée** : il établit le
  comportement du **code**, jamais la fréquence des cas réels. `scan_state['detail']`
  est vide au démarrage et je ne l'ai pas peuplé.
- **Aucun navigateur ouvert.** Les deux chaînes d'affichage sont établies sur les
  **octets servis** et sur la lecture de champ, jamais observées au rendu.
- Je mesure des **modules**, pas des **fonctions** : un module atteignable peut
  contenir du code mort, ce lot ne le voit pas.
- Sur les 110 phrases concluantes du 444, **89 restent fermées** — ce lot n'en
  ouvre aucune ; il a changé de veine.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant chaque mesure ;
  scripts du scratchpad avec `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`. `anomaly.scan`, `option_anomalies.*`,
  `stock_anomalies.detect_stock_anomalies` et l'analyse `ast` appelés en mémoire ;
  routes en **GET** ; `persist` redirigé vers un répertoire temporaire.
- **MD5 des 8 pages remesurés : 8 / 8 identiques** aux références.
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; les trois fichiers ré-horodatés par la suite **restaurés à l'octet
  près et revérifiés par md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Cinquante-cinquième lot court, deuxième de la tranche.

Le 451 avait trouvé du code mort **en remontant un champ**. Ce lot en fait une
mesure : **85 modules, 6 192 lignes, 33 fichiers de tests**. Le pari du réveil —
« soit une liste, soit *le 451 était isolé* » — tombe du premier côté, largement.

Mais le résultat qui compte n'est pas le recensement : c'est ce vers quoi il a
conduit. En vérifiant une **promesse affichée** — « ouvrir une analyse pour le
détail » — le balayage a mis à nu une **collision de route** que trois gardiens
verts ne pouvaient pas voir, parce que chacun teste son côté de la collision et
qu'aucun ne les compare. Le péage du 446 tient une cinquième fois :
c'est en partant de l'écran, pas du graphe, que le rang 1 est apparu.

Comptes séparés, inchangés : résultats faux **arrêtés avant publication** **20** ;
**publiés puis corrigés** **3**.

**Six bilans — n°9, n°10, n°11, n°12, n°13 et n°14 — attendent une réponse.**
