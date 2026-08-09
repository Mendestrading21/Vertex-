# SKYLER LOT 456 — Les fractions affichées : la carte « Qualité des données » de `/system` plafonne son dénominateur à 200 pour un univers de 517, et son camembert ne peut afficher qu'une seule part à 100 %

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-456` (base : lot 455 fusionné,
2547fec)

Trente-septième lot de la veine, sixième de la tranche 450-459. La veine des
phrases composées est close ; le 455 a désigné la famille suivante — **un compte
affiché dont les numérateurs ne couvrent pas tout le dénominateur**. Ce lot
attaque la classe entière : **les fractions affichées**.

**Aucun code, aucun gardien, aucun test.**

## L'instrument : partir de l'écran, par construction

Balayage des **42 objets servis** (8 pages + `/analysis/AAPL` + 33 JS statiques
non-vendor, **841 916 caractères**) à la recherche des gabarits qui **affichent
une fraction** : `${A}/${B}`, `A+'/'+B`, « sur N », « n= », « /max ».

Le péage du 446 est respecté **par construction** : on ne part pas d'un champ
qu'on espère affiché, on part de ce qui **est** affiché.

```text
12 gabarits de fraction relevés dans les octets servis
    5 tracés jusqu'au producteur   → 2 PLAFONNÉS · 3 SAINS
    7 nommés, NON tracés ce lot    → ni comptés, ni conclus
```

**Les 7 non tracés, nommés** (règle 448) : `battu ${sm.beats}/${sm.total} trim.`
(notes d'analyste), `${diag.ai.ok}/${diag.ai.total} analyses OK` (`vx-shell.js`),
`b.points/b.max` et `p.v/p.max` et `rating_mean/5` (**barèmes** : x sur un
maximum, pas une population), `favorable points sur pts.length`
(`options-structure.js`), `CALLS n · PUTS m / 1 max` (`/portfolio`).

## Les trois fractions saines — le témoin positif

```text
options/environment.py:122-123    known = [d for d in dims if d['known']]
                                  dimensions_known / dimensions_total     MÊME liste
company/risk_map.py:137-138       known = [r for r in risks if r['known']]
                                  known_count / total_count               MÊME liste
markets_page.py (conclusion)      top[0][1] + ' titre(s) sur ' + rows.length
                                  numérateur et dénominateur du MÊME tableau client
```

Trois fractions dont le numérateur est une **compréhension filtrée du
dénominateur lui-même**. Sans elles, un instrument qui rendrait « tout est
plafonné » serait indistinguable d'un instrument juste.

## La trouvaille : `/api/data-quality` plafonne à 200, l'univers en compte 517

```python
vertex/app/routes/strategy_os_api.py:165-168
    packets = [{'symbol': s, 'quality': {...}} for s in list(detail)[:200]]
    report = data_quality_report(packets)

vertex/observability/diagnostics.py:44
    return {'total': len(packets), 'by_quality': by_quality, …}
```

`total` **est** le nombre de paquets, et les paquets sont **les 200 premiers**.
`len(UNIVERSE) = 517`.

**Banc — la route RÉELLE exécutée en GET, `scan_state['detail']` peuplé en
mémoire puis restauré :**

```text
detail 260 · source 'stooq' → total 200 · by_quality {'RECENT': 200}
detail 517 · source 'stooq' → total 200 · by_quality {'RECENT': 200}
detail 300 · source 'demo'  → total 200 · by_quality {'DEMO': 200}
detail 300 · source ''      → total 200 · by_quality {'MISSING': 200}

detail   5 → total   5      detail 150 → total 150      detail 200 → total 200
                            → le plafond mord à partir de 201
```

Et voici ce que `/system` en fait (`system_page.py:699-701`) :

```javascript
title:      'Qualité des données (' + dq.total + ' titres)',
question:   'Les données sont-elles utilisables pour décider ?',
conclusion: 'Dominante : ' + dominant + ' (' + byQ[dominant] + ' / ' + dq.total + ')'
```

### Deux défauts distincts sur la même carte

**(i) Le titre présente un plafond d'échantillon comme un compte de titres.**
Avec 517 symboles scannés, la carte annonce « Qualité des données (**200**
titres) ». Ce n'est pas un chiffre faux — 200 titres **ont** été évalués — c'est
un **échantillon présenté comme la population**, la famille du 417. **Le plafond
de 200 n'est mentionné nulle part à l'écran.** → **rang 2**.

**(ii) Le camembert ne peut afficher qu'une seule part, toujours à 100 %.** La
route calcule **une seule** qualité, au niveau du scan
(`overall = 'DEMO' if is_demo else ('RECENT' if source else 'MISSING')`), puis
l'estampille sur **chaque** symbole. Mesuré : `by_quality` ne contient **jamais
qu'une clé**. La conclusion est donc **toujours** de la forme
« Dominante : X (200 / 200) » — une répartition **qui ne peut pas se répartir**.
C'est un champ à **un seul écrivain littéral, constant par construction**
(famille 442). → **rang 3**.

**Ce qui atténue, et que je dis** : la route sert, à côté, une note **honnête et
co-visible** — « qualité au niveau scan (source unique) — la provenance valeur
par valeur arrive avec le routage data_sources ». Elle avoue exactement le point
(ii). **Elle ne dit rien du plafond de 200**, et c'est pourquoi (i) reste un
rang 2 quand (ii) descend au rang 3.

## La seconde fraction plafonnée — établie par LECTURE, pas par exécution

```python
vertex/options/gex_scan.py:53-55, :73-74
    rows.sort(key=lambda r: abs(r['net_gex'] or 0), reverse=True)
    if top:
        rows = rows[:max(1, int(top))]
    …
    'symbols_scanned': len(by_sym),
    'symbols_usable':  len(rows),
```

La troncature est **trois lignes au-dessus** du comptage, et la route passe
`top=30` — mesuré, `options_intel_api.py:133`. `options-gex.js` rend :

> « Climat : … · `symbols_usable`/`symbols_scanned` **titres exploitables**. »

Sur un board de plus de 30 sous-jacents exploitables, le numérateur est donc
**le plafond d'affichage**, pas une mesure d'exploitabilité — alors que le mot
« exploitables » en promet une.

**Je n'ai PAS établi ce cas par exécution.** Deux tentatives de banc ont échoué :
la première fabriquait la clé `symbol` alors que `gex_scan` lit `sym` ; la
seconde, corrigée, donne bien `symbols_scanned` mais `symbols_usable = 0` parce
que `gex.compute` rejette mes contrats fabriqués. **C'est donc une LECTURE** —
la règle 447 s'applique, la troncature et le comptage sont sur la même page de
code — et **je le classe rang 4 en l'état, à requalifier si un banc l'exécute.**
Je préfère le dire que gonfler le résultat.

## Ce que le lot ne prétend pas

- **7 des 12 fractions relevées ne sont pas tracées** : elles sont nommées, et
  **elles ne sont comptées dans aucun total**.
- Le balayage cherche des **gabarits littéraux** dans les octets servis. Une
  fraction construite par un helper (`pct(a, b)`) ou par une déstructuration
  **échapperait** (leçon 436) — **non quantifié**.
- Le banc de `/api/data-quality` **exécute la route**, mais sur un `detail`
  **fabriqué** : il établit le comportement du **code**, pas la taille réelle du
  scan en usage. Ce qu'il établit sans ambiguïté, c'est que **le plafond mord dès
  201 symboles**, et que l'univers en compte **517**.
- **Aucun navigateur ouvert.** Les deux chaînes d'affichage sont établies sur les
  octets servis (`system_page.py:699-701`, `options-gex.js`, line-exact).
- `scan_state` a été **muté en mémoire puis restauré** : `detail` 0 → 0 entrée,
  `source` `None` → `None`. Aucune écriture disque.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; scripts du scratchpad
  avec `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`. Routes en **GET** ; `persist` redirigé ;
  **`/options/<sym>`, `/api/analyst/` et `/api/correlations/` NON appelées**
  (réseau sortant).
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; restauration vérifiée par **md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Cinquante-neuvième lot court, sixième de la tranche.

La famille désignée par le 455 a payé **au premier lot** : sur 12 fractions
affichées, 5 tracées, **2 plafonnées** — dont une mesurée sur la route réelle. Et
elle a produit un genre neuf, qui manquait à la nomenclature : **un PLAFOND
D'ÉCHANTILLON AFFICHÉ COMME UNE POPULATION**.

Le second résultat est plus inconfortable et je le laisse tel quel : la carte qui
demande « Les données sont-elles utilisables pour décider ? » y répond par un
camembert **qui ne peut jamais montrer qu'une seule part**. Sa note l'avoue. Le
graphique, lui, donne l'impression d'une mesure par titre qui n'existe pas.

Comptes séparés, inchangés : résultats faux **arrêtés avant publication** **25** ;
**publiés puis corrigés** **3**.

**Six bilans — n°9, n°10, n°11, n°12, n°13 et n°14 — attendent une réponse.**
