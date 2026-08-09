# SKYLER LOT 463 — Les promesses de provenance : l'historique GEX journalise les profils de DÉMO dans un fichier de 120 jours et les ressert sous la légende « points réels uniquement » — la seule promesse qui SURVIT au retour en mode réel

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-463` (base : lot 462 fusionné,
6ee3b95)

Quarante-troisième lot de la veine, troisième de la tranche 460-469. Le 462 avait
signalé **hors calibrage et sans le compter** une phrase affirmant une propriété
(« sur données réelles ») qu'un repli pouvait démentir. Ce lot prend cette piste :
**les phrases servies qui affirment une propriété de provenance ou de fraîcheur.**

**Aucun code, aucun gardien, aucun test.**

## Le calibrage, posé AVANT la première mesure

Une **PROMESSE DE PROVENANCE SERVIE** **(a)** porte du texte visible, **(b)**
contient un marqueur pris dans une **liste fermée**, et **(c)** **AFFIRME** —
elle dit que la donnée est réelle / live / non inventée / non recalculée — au
lieu de **NOMMER** une source.

Le critère **(c)** est le cœur : « Connexions (IBKR, TradingView, Claude) »
**nomme**, « points réels uniquement » **affirme**.

Exclus d'emblée, nommés : les phrases qui nomment sans affirmer · celles dont
l'émission est **déjà conditionnelle** à la provenance (branche `demo ? … : …`) —
honnêtes par construction · l'habillage sans texte visible.

**Bornage annoncé d'avance** : plusieurs cas allaient relever de **dossiers déjà
ouverts**. Ils sont nommés comme **connus** et **ne comptent pas** comme
trouvailles neuves.

## La correction d'instrument — troisième de la série 461-462-463

Première mesure : **88 phrases**. Le contrôle obligatoire passait. C'est la
**lecture de la liste** qui a trahi l'instrument : `live` appariait
`live-updates.js`, `connected-live`, `data-live=` ; `ibkr` appariait
`vx-conn-ibkr-badge` et `/api/ibkr/positions`. **Le critère (c) était posé dans le
calibrage mais n'était imposé nulle part dans le code du détecteur.**

Corrigé : les marqueurs deviennent des **tournures d'affirmation** (`données
réelles`, `points réels`, `aucun chiffre inventé`, `aucun indicateur recalculé`…)
et les URL, identifiants et jetons sans espace sont exclus **par forme**.

```text
88 phrases  →  31        vraisemblance : 0,74 par objet servi
```

**Un faux arrêté avant publication. Total : 31 → 32.** Et une leçon qui complète
le corollaire du 462 : ici la taille (88, soit 2,1 par objet) n'était **pas
invraisemblable** — c'est la **lecture** qui a révélé le bavardage. *La taille
détecte le bavardage grossier ; le bavardage modéré ne se voit qu'en lisant la
liste.*

## Ce que la famille contient — et elle re-surface surtout du connu

Sur les **31** promesses retenues, **22 sont tranchées** et **9 sont nommées sans
être tracées** (`Risque complet (positions réelles)`, le ledger immuable, le
post-mortem, « aucun indicateur recalculé côté UI », « Aucune valeur inventée »
du risk-on/off, « Champs moteur réels », « valeur de marché », « Signaux
descriptifs (données réelles) », « prix réels » des stress-scénarios). **Elles ne
sont comptées dans aucun total.**

```text
verdict                                                              n
phrases émises dans une BRANCHE D'ABSENCE (« rien d’inventé »)      11   honnêtes par construction
phrases CONDITIONNELLES à la provenance (`demo ? … : …`)              5   honnêtes par construction
re-surfaçages de DOSSIERS DÉJÀ OUVERTS                                4   425 · 363 · 407 · 386/431
vérifiée au lot précédent (« moyenne réelle … n≥5 »)                  1   concorde
NOUVELLE TROUVAILLE                                                   1   ← l'historique GEX
                                                                     ──
                                                                     22
```

**Onze des vingt-deux sont les états vides du produit** — « Données macro non
fournies par le scan — rien d'inventé », « P&L latent indisponible … aucun
chiffre inventé », « Aucun verdict à répartir — le consensus n'est jamais
inventé ». Ces phrases affirment au moment précis où la donnée manque :
**elles sont la promesse tenue, pas la promesse trahie.** C'est le témoin positif
de la famille, et il est massif.

**Le bornage demandé est donc rendu : cette famille ne creuse pas de terrain
neuf, elle re-nomme surtout des dossiers ouverts.** Une exception, et une seule.

## La trouvaille : une promesse qui SURVIT au retour en mode réel

`vertex/options/gex_history.py` journalise le profil GEX du jour dans
`gex_history_cache.json`, **120 jours**, un point par jour et par symbole. Sa
propre docstring pose **deux** promesses :

> « on n'enregistre QUE des profils **réels** **non vides** (jamais de point
> inventé) »

**La garde implémentée n'en couvre qu'une.** Mesuré :

```text
signature                       record(profile)      — aucun paramètre de provenance
mentionne demo/synth/source ?   False
seule garde                     `if not isinstance(profile, dict)
                                 or profile.get('empty')
                                 or not profile.get('symbol'): return False`
```

**Banc (persist redirigé vers un `tempfile.mkdtemp()`, aucune écriture dans le
dépôt)** :

```text
record({'symbol':'DEMOX', 'net_gex_total': -1234567.0, …})  →  True
gex_history_cache.json écrit :
  {"DEMOX":[{"date":"2026-08-09","net_gex":-1234567,"call_gex":1000, …}]}
series('DEMOX')  →  le point est relu et servi
```

L'appelant ne garde pas davantage — et son commentaire promet ce que le code ne
fait pas :

```python
# Journal quotidien du GEX (best-effort, réel seulement) → série « Daily GEX ».
    _gh.record(profile)
    history = _gh.series(sym)
return jsonify({… 'demo': bool(DEMO_MODE), … 'history': history})
```

**La même fonction sert `'demo': bool(DEMO_MODE)` dans la même réponse.** Le
contrats est alimenté par `_board()`, c'est-à-dire `scan_state['options_board']` :
en mode DEMO, ce board est synthétique.

### Et la légende, elle, est inconditionnelle

`options-gex.js` :

```javascript
:32   var demo = d.demo ? '<span class="vx-demo-tag">DÉMO</span> ' : '';   // la page SAIT
…
:107  … + n + ' jour(s) journalisé(s) — points réels uniquement.</div>';   // 75 lignes plus bas
```

**Le même fichier, la même charge utile, la même fonction : à la ligne 32 la page
étiquette honnêtement DÉMO, à la ligne 107 elle affirme « points réels
uniquement » sans consulter le drapeau qu'elle tient en main.** C'est la famille
433/457 — l'information honnête est déjà calculée — **portée à son degré le plus
net : elle est déjà UTILISÉE soixante-quinze lignes plus haut.**

### Ce qui en fait un défaut distinct, et non le dossier 391/396 redit

En mode DEMO, **tout** l'affichage dérivé du scan est synthétique : c'est le
dossier ouvert **391/396**, et compter chaque phrase « réelle » de l'interface
comme un défaut séparé **gonflerait le résultat de quinze cas imaginaires**. Je
ne le fais pas.

Ce qui distingue celui-ci : **il ne se contente pas d'AFFICHER de la donnée de
démo sous une légende réelle — il la PERSISTE.** Le point écrit en démo au jour
D‑30 reste dans le fichier **120 jours**. Au jour D en mode réel, `d.demo` vaut
`false`, l'étiquette DÉMO de la ligne 32 **disparaît**, et la frise affiche des
points de démo et des points réels **côte à côte**, sous « points réels
uniquement », **sans aucun signal**.

**C'est un SECOND SITE du genre 391/396** — dossier qui porte, lui, sur
`breadth_history.json`. Même forme, autre fichier d'historique, légende plus
explicite. **Rang 2**, et non rang 1 : il faut avoir tourné en DEMO au moins une
fois, et le défaut n'inverse pas une décision d'entrée comme la borne du 457.

**Le gardien existe et il couvre l'AUTRE promesse.** `tests/test_gex_history.py`
compte quatre tests, dont `test_empty_profile_never_recorded` : la docstring
promet « réels **non vides** », le test verrouille **« non vides »** et **rien ne
verrouille « réels »**. Une garde sur la bonne fonction, sur la mauvaise
propriété.

Correction pressentie : passer la provenance à `record()` — `DEMO_MODE` est dans
la portée de l'appelant — ou étiqueter le point. **Aucun GO, rien n'est engagé.**

## Ce que le lot ne prétend pas

- **9 promesses sur 31 ne sont pas tracées.** Nommées, **exclues de tout total**.
- La liste des tournures d'affirmation est **fermée** : une promesse formulée
  autrement échapperait. **Non quantifié.**
- Le banc appelle `record()` sur un profil **fabriqué** : il établit que la
  fonction **n'a aucune garde de provenance**, pas la fréquence des points de
  démo dans un fichier réel. `gex_history_cache.json` **existe sur le disque** et
  **n'a pas été ouvert** — la sonde interdit d'y toucher, et son contenu n'est pas
  nécessaire à la démonstration.
- L'atteignabilité du mode DEMO est établie **par lecture** (`DEMO_MODE =
  os.environ.get('DEMO', …) == '1'`), pas par exécution d'un serveur.
- **Aucun navigateur ouvert.** La co-visibilité des lignes 32 et 107 est établie
  sur les **octets servis**, pas observée au rendu.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; scripts du scratchpad
  avec `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`. `gex_history.record()` appelé **avec `persist` redirigé
  vers un `tempfile.mkdtemp()`** ; routes en **GET** ; **`/options/<sym>`,
  `/api/analyst/` et `/api/correlations/` NON appelées**.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; restauration vérifiée par **md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Soixante-sixième lot court, troisième de la tranche.

Le lot rend le **bornage** que l'orientation demandait : sur 31 promesses de
provenance, **onze sont des états vides honnêtes**, **cinq sont conditionnelles**,
**quatre re-nomment des dossiers déjà ouverts** — la famille re-surface du connu
plutôt qu'elle n'ouvre du terrain. **Cinquième bornage consécutif.**

Et elle laisse **une** trouvaille, qui vaut par ce qui la distingue : le défaut
n'est pas d'afficher de la démo sous une légende réelle — ce serait le dossier
391/396 redit — **c'est de l'ÉCRIRE dans un fichier qui vit 120 jours, où elle
cesse d'être signalée dès le retour en mode réel.** Un mensonge affiché se
corrige en rafraîchissant ; un mensonge **journalisé** se corrige en purgeant un
fichier.

Le fait de méthode complète le corollaire d'hier. Le 462 disait : *le contrôle
détecte la cécité, la taille détecte le bavardage.* Ici la taille — 2,1 phrases
par objet — **n'avait rien d'invraisemblable**, et l'instrument bavardait quand
même. **Troisième détecteur consécutif faux à la première écriture, et la seule
parade qui ait fonctionné trois fois sur trois est de LIRE LA LISTE avant de la
compter.**

Genre neuf pour la nomenclature : **UNE PROMESSE DE PROVENANCE QUE LE JOURNAL
PERPÉTUE** — la donnée de démo persistée survit à l'étiquette qui la signalait.

Comptes séparés : résultats faux **arrêtés avant publication** **32** (+1) ;
**publiés puis corrigés** **3** ; **interprétations retirées** **1**.

**Sept bilans — n°9, n°10, n°11, n°12, n°13, n°14 et n°15 — attendent une
réponse.**
