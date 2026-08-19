# G1 · #779 — Corrélations et sélection hebdo sortent

Modules : `vertex/app/routes/correlations_api.py`, `vertex/app/weekly_selection.py`,
`vertex/app/routes/weekly_api.py`
Gardien : `tests/test_vertex_1_0_correlations_weekly_parity.py` (9 tests, 6 mutations)

---

```text
routes LEGACY      5 → 3
lignes terminal.py 7 145 → 7 082
routes canoniques  149 → 151
```

## Ce que j'ai cassé en transcrivant, et comment je l'ai vu

La première version de `api_correlations` dans le nouveau module portait **trois
écarts que je n'avais pas décidés** : un `.dropna()` ajouté sur les rendements,
le seuil de points appariés passé de **20 à 30**, et une garde de colonne en plus.

**Aucun test n'aurait échoué.** La route rend une liste, et une liste plus courte
reste une liste. Seules les *corrélations servies* auraient changé — sans que
personne ne l'ait demandé, et sans trace.

Trouvé en comparant les deux corps ligne à ligne, normalisés des seuls
renommages, avant d'aller plus loin. Les deux valeurs sont maintenant
verrouillées par un test dédié, avec deux mutations.

C'est la leçon la plus utile de ce lot : **une extraction qui retouche au
passage n'est plus une extraction**, et c'est précisément le genre de dérive
qu'aucune suite verte ne signale.

## Le piège du chemin, encore — et il n'aurait rien levé

`terminal.py` calculait `WEEKLY_PATH` par
`os.path.join(os.path.dirname(__file__), 'weekly_snapshot.json')`. Recopier
cette formule dans `vertex/app/` la ferait pointer **à côté du code** : le
snapshot de la semaine serait écrit ailleurs, l'ancien ne serait plus jamais
relu, et la sélection repartirait de zéro un lundi — **sans erreur**. Même
famille que le `static_folder` de la fabrique, deux lots plus tôt.

Le chemin passe donc par `persist.cache_path`, qui rend exactement la même
valeur.

## Ce que la carte des résultats refuse de deviner

`dte` absent ⇒ le titre n'est **pas** écarté de la sélection. Ne pas savoir quand
tombent les résultats n'est pas savoir qu'ils tombent cette semaine. Le test
donne les trois formes d'entrée incomplète et vérifie qu'une seule ligne survit.

## Troisième test à moi qui dépendait de l'ordre des autres

`test_le_chemin_du_snapshot_hebdo_n_a_pas_bouge` comparait d'abord
`weekly_selection.CHEMIN` au **retour de `persist.cache_path`** — une fonction
que `tests/test_persist_lot392.py` monkeypatche vers un dossier temporaire. Il
passait seul, échouait dans la suite complète.

L'échec a révélé un fait qui valait d'être écrit : **`CHEMIN` est calculé une
fois à l'import**. Rediriger `cache_path` plus tard ne le déplace pas — c'était
déjà vrai du `WEEKLY_PATH` du monolithe. Le test compare désormais à la racine
du dépôt, et vérifie séparément que la formule employée reste `persist.cache_path`.

## Une limite observée, laissée telle quelle

Quand le réseau ne répond pas, `/api/correlations` rend `corr: []` **sans** clé
`error` : aucune exception n'est levée, la boucle ne trouve simplement rien.
« Impossible de mesurer » devient donc indiscernable de « mesuré, rien de
significatif ». C'est le comportement d'avant, **préservé délibérément** — le
corriger serait un changement de contrat, pas une extraction. Écrit ici pour que
le choix soit visible plutôt que subi.

## Deux gardiens maison ont réagi

| gardien | ce qu'il a vu |
| --- | --- |
| `test_namespace_guards` | mon commentaire contenait un verbe français dont une sous-chaîne est le motif de prénom surveillé. La règle est **zéro occurrence** ; faux positif inévitable en français, reformulé plutôt qu'assoupli — y compris dans ce rapport, qui est tombé une seconde fois pour la même raison |
| `test_pass_terminal_lot386` | 36 → 35 `except: pass` : celui de `_to_naive` est parti **avec** sa fonction |

## Preuves

```text
compileall                     exit 0
pytest tests/ -q               3 320 passed        (3 311 avant le lot)
pytest tests/test_no_orders.py 3 passed
mutations                      6/6 mordent, contrôle vert
```

Les six : `.dropna()` réintroduit · seuil 20 → 30 · chemin hebdo dérivant vers
`vertex/app/` · `dte` inconnu traité comme mesuré · cache local au lieu du cache
partagé · le monolithe garde son propre chemin.

```text
huit espaces            200 · 0 débordement · 0 erreur console
/api/client-log         count: 0
/api/correlations/AAPL  200 · /weekly-regen 200
```

## Les trois LEGACY restantes

`/api/ticker/<sym>`, `/options/<sym>` et `/desc/<sym>`.

Les deux premières partagent `options_pack` — 143 lignes, trois dépendances
locales (`_OPTALL_CACHE`, et les formateurs `_f`/`_i`). La troisième porte
`_FR_DESC`, une **table de données** de descriptions françaises par titre, plus
un cache disque : c'est un actif de données, pas un helper, et son domicile
naturel est `vertex/data/`.

**G1 reste non déclaré PASS.**
