# SKYLER LOT 464 — Le ledger qui produit le track record affiché ne peut pas distinguer un verdict de DÉMO d'un verdict réel : trois écrivains append-only sur quatre ont perdu la provenance, et le quatrième la garde

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-464` (base : lot 463 fusionné,
dcd4c88)

Quarante-quatrième lot de la veine, quatrième de la tranche 460-469. Le 463 a
nommé **une promesse de provenance que le journal perpétue**. Ce lot attaque la
classe que cette forme désigne : **les écrivains de fichiers runtime et leur
garde de provenance.**

**Aucun code, aucun gardien, aucun test.**

## Le calibrage, posé AVANT la première mesure

Un **ÉCRIVAIN PERSISTANT** est un site d'appel qui écrit un fichier runtime.

**Critère décisif n°1, posé d'avance** : un écrivain n'entre dans la population
que si ce qu'il persiste est **dérivé d'une donnée de marché** — donc
susceptible d'être synthétique en DEMO. Les données **utilisateur**,
**configuration** et **méta** n'ont pas de question de provenance : exclues,
nommées, comptées dans aucun total. Sans ce critère, `desk_data.json` et ses
sauvegardes gonfleraient le total de cas où « garde de démo » ne veut rien dire.

**Critère décisif n°2, trouvé en lisant la liste et posé avant tout comptage** —
et c'est lui qui donne au genre du 463 sa portée exacte :

> **ÉCRASER n'est pas ACCUMULER.** Un *cache* est réécrit en entier à chaque
> cycle : il reflète le mode courant, et un mensonge de démo **n'y survit pas**
> au cycle suivant. Un *journal* accumule : le mensonge y **reste**.

**Le genre du 463 ne concerne donc que les écrivains QUI ACCUMULENT.**

## La mesure

```text
sites d'écriture persistante trouvés (AST, `save_json` / `_save_json`)   28
fichiers runtime distincts visés                                         21

   ÉCRASENT à chaque cycle — un mensonge de démo n'y survit pas          14
      macro_cache · options_cache ×2 · optall_cache · radar_cache
      cal_cache · fund_cache ×2 · edge_cache · market_context_last
      session_digest_cache · ai_enrichment · position_inventory · tracking
   SANS OBJET (donnée utilisateur / méta)                                 3
      desk_data ×2 (navigateur) · track_meta (`{last_day, last_n}`)
   ACCUMULENT de la donnée dérivée du marché                              7   ← la population
```

**Le bornage est là : sur 21 fichiers, 14 sont des caches qui s'écrasent.**
Compter chacun comme un défaut aurait produit vingt et un cas là où il y en a
sept à examiner — la leçon du 463, appliquée avant de compter.

## La correction d'instrument — quatrième de la série 461-464, et d'une forme neuve

Mon détecteur AST cherchait `save_json` / `_save_json`. **Il a manqué
`track_record.record()`, qui écrit son ledger par un `open(chemin, 'a')` brut** —
il n'apparaissait dans la liste que par son *méta*-fichier, `track_meta.json`.

C'est le piège du détecteur à une seule forme (454, 461), **transposé aux
écritures** : je cherchais un mécanisme d'écriture, il y en avait deux. Et c'est
la **lecture de la liste** — pas sa taille — qui l'a révélé, exactement comme au
463.

**Un faux arrêté avant publication. Total : 32 → 33.**

## Les sept écrivains qui accumulent — et le verdict

```text
fichier                    écrivain                      provenance      verdict
breadth_history.json       terminal.py:512  scan         aucune          DÉJÀ CONNU (391/396)
gex_history_cache.json     gex_history.record            aucune          DÉJÀ CONNU (463)
skyler_memory.json         decision_memory.freeze        'demo' STOCKÉ   GARDÉ   ← témoin
edge_ledger.jsonl          track_record.record           aucune          NON GARDÉ ← trouvaille
skyler_decisions.json      skyler_journal.record         PERDUE          NON GARDÉ ← trouvaille
skyler_sessions.json       session_log.record_close      IMPOSSIBLE      NON GARDÉ ← trouvaille
alerts_fired.json          terminal.py:7049 _alerts_loop aucune          pressenti au 462
```

**Les deux premiers ne sont pas recomptés** : ce sont les dossiers ouverts.

### Le témoin positif : la mémoire décisionnelle, elle, étiquette

`decision_memory.freeze()` stocke **`'demo': bool(p.get('demo'))` comme champ
lisible** du record figé, et fait même entrer le drapeau dans le hachage de
`decision_id` — deux décisions identiques, l'une en démo l'autre en réel,
**coexistent séparément**. C'est exactement ce qu'il fallait faire, et cela prouve
que la contrainte était connue de l'auteur.

**C'est ce témoin qui rend le lot lisible** : sur le même chemin de code, dans
les mêmes `try`, quatre écritures append-only — **une seule retient la
provenance que la route a calculée.**

## La trouvaille : le ledger du track record

`vertex/app/routes/analysis_api.py:102` lit `DEMO_MODE as _demo` et le passe aux
moteurs (`decide(..., demo=_demo)`, `build_packet(..., demo=_demo)`). **La
décision SAIT qu'elle est de démo.** Puis :

```text
skyler_journal.record(j, decision, …)   la décision porte demo=True
                                        → l'entrée écrite a 8 champs :
                                          symbol · decision · as_of · score_total
                                          level · capped_by_gate · price · recorded_at
                                        MESURÉ : 'demo' in entrée  →  False
                                        LE DRAPEAU EST REÇU PUIS JETÉ.

session_log.record_close(log, sym, date, close)
                                        MESURÉ : la signature n'a AUCUN
                                        paramètre de provenance ; l'entrée
                                        stockée est {'date': …, 'close': …}.
                                        LA PROVENANCE EST INEXPRIMABLE.
```

Et le plus grave, `vertex/engines/track_record.py` :

```python
def record(state):                       # signature MESURÉE : (state)
    …
    with open(_ledger_path(), 'a', encoding='utf-8') as f:      # APPEND-ONLY
        rec = {'ts': …, 'ticker': sym, 'price': …, 'decision': d.get('verdict'),
               'score': …, 'entry': …, 'stop': …, 'targets': …,
               'market_regime': …, 'sector_regime': …, 'features': …,
               'outcome': None}                                 # 12 champs, AUCUNE provenance
```

**Banc (persist redirigé vers un `tempfile.mkdtemp()`, `cache_path` vérifié
redirigé, aucune écriture dans le dépôt)** :

```text
record(état synthétique)                    →  2 ligne(s) écrites
clés de l'entrée : decision entry features market_regime outcome price score
                   sector_regime stop targets ticker ts
champ de provenance présent ?               →  False
evaluate() appelle _load_ledger ?           →  True
evaluate() filtre-t-elle sur la provenance ?→  False
```

**L'appelant ne garde pas non plus** : `terminal.py:1430`, dans `_edge_loop`,
`_track.record(scan_state)` toutes les 6 heures, **sans condition sur
`DEMO_MODE`** — alors que le même fichier teste `DEMO_MODE` à seize autres
endroits.

### Ce que l'écran en fait

`/journal` affiche (chaînes relevées dans les octets servis, vérifiées au 462) :

> « … verdict(s) enregistré(s), … résolu(s) — **minimum 5 par verdict** »
> « **moyenne réelle des verdicts résolus (n≥5) — mesure, pas une promesse** »

Ces chiffres sortent de `evaluate()`, qui lit le ledger **sans filtre de
provenance** parce qu'**il n'y a rien à filtrer**.

### Classement — rang 1

Je le classe au-dessus du 463, et je dis sur quel critère : **le consommateur.**
Une frise GEX fausse **désinforme** ; un track record contaminé **change ce que
l'utilisateur croit que le moteur vaut** — et il est présenté comme *la mesure
honnête*, par opposition explicite à une promesse.

Trois aggravations mesurées : le ledger est **append-only** (aucune purge n'existe
dans le module) ; la contamination est **indétectable** (aucun champ ne la porte) ;
et elle est **définitive** — le `/journal` déclare par ailleurs « Ledger immuable —
les décisions historiques ne sont jamais réécrites ».

**La précondition, dite franchement** : il faut avoir tourné au moins une fois en
DEMO. `DEMO_MODE = os.environ.get('DEMO', '1' if os.environ.get('NO_IBKR') == '1'
else '0') == '1'` — **la démo est le défaut dès que `NO_IBKR=1`**, ce qui est le
cas d'un lancement sans TWS. Ce n'est pas un mode exotique.

Correction pressentie : passer `demo` à `record()` — il est dans la portée de
l'appelant — et l'écrire dans la ligne, comme `decision_memory` le fait déjà.
**Aucun GO, rien n'est engagé.**

**Aucun gardien** : aucun test ne vérifie qu'une donnée de démo n'entre pas dans
un journal accumulant. Le dossier ouvert **417** porte sur les *dénominateurs* du
track record, **pas** sur sa provenance — ce lot ne le recoupe pas.

## Ce que le lot ne prétend pas

- Le banc écrit un état **fabriqué** : il établit que `record()` **n'a aucune
  garde de provenance** et que `evaluate()` **ne filtre pas**, **pas** la
  proportion de lignes de démo dans un ledger réel. **`edge_ledger.jsonl` n'a pas
  été ouvert** — la sonde l'interdit, et son contenu n'est pas nécessaire.
- L'atteignabilité du mode DEMO est établie **par lecture** de `config.py`, pas
  par exécution d'un serveur.
- Le recensement porte sur les écritures **repérables par AST** dans
  `vertex/**` et `terminal.py`. Une écriture par un chemin encore différent
  échapperait — **c'est déjà arrivé une fois dans ce lot même**, et je n'ai pas
  quantifié le reste.
- `alerts_fired.json` est **nommé, pas tranché** : il accumule, sa provenance
  vient de `_alert_price` (signalé au 462), et je ne l'ai pas tracé ce lot.
- Les 14 caches sont classés « écrasent » **par lecture de leur écrivain**, pas
  par observation d'un cycle réel.
- **Aucun navigateur ouvert.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; scripts du scratchpad
  avec `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`. `track_record.record()`, `skyler_journal.record()`,
  `session_log.record_close()` appelés **avec `persist` redirigé vers un
  `tempfile.mkdtemp()`** (`cache_path` vérifié redirigé) ; **`/options/<sym>`,
  `/api/analyst/` et `/api/correlations/` NON appelées**.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; restauration vérifiée par **md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Soixante-septième lot court, quatrième de la tranche.

Le lot rend **le premier rang 1 depuis le 457** — et il le rend en **bornant**,
pas en élargissant : quatorze caches écartés parce qu'un mensonge n'y survit pas,
trois fichiers sans objet, deux dossiers déjà connus non recomptés. **Sixième
bornage consécutif.** Sur les sept écrivains qui accumulent, **un seul garde
correctement**, et c'est lui qui prouve que la contrainte était comprise.

Le fait de méthode est le même qu'hier et il se confirme : **c'est en LISANT la
liste, pas en la comptant, que le défaut de l'instrument s'est vu** — ici un
écrivain qui n'utilisait pas le mécanisme d'écriture que je cherchais. Quatrième
détecteur consécutif faux à la première écriture ; quatrième fois que la lecture
le rattrape.

Et le critère « écraser n'est pas accumuler » **borne rétroactivement le 463** :
le genre qu'il a nommé ne s'applique qu'aux journaux, ce qui **divise par trois**
la surface que l'on aurait pu lui prêter.

Genre confirmé, pas neuf — **UNE PROMESSE DE PROVENANCE QUE LE JOURNAL
PERPÉTUE**, avec un troisième, quatrième et cinquième site, dont un qui alimente
la mesure de performance publiée.

Comptes séparés : résultats faux **arrêtés avant publication** **33** (+1) ;
**publiés puis corrigés** **3** ; **interprétations retirées** **1**.

**Sept bilans — n°9, n°10, n°11, n°12, n°13, n°14 et n°15 — attendent une
réponse.**
