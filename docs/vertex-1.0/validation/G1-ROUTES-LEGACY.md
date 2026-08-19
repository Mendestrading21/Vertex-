# G1 · #779 — Quatre routes LEGACY sortent, et la passerelle IBKR avec

Modules : `vertex/app/ibkr_state.py`, `vertex/app/routes/live_state_api.py`,
`vertex/app/routes/track_record_api.py`
Gardien : `tests/test_vertex_1_0_routes_legacy_parity.py` (10 tests, 6 mutations)

---

## La mesure qui a changé le plan

Le premier arbitrage annonçait : *« 11 routes LEGACY, 2 à 5 dépendances chacune,
patron `make_blueprint` requis »*. Ce chiffre comptait **toutes** les dépendances,
sans distinguer celles qui vivent dans `terminal.py` de celles qu'il ne fait
qu'importer depuis le paquet.

En les classant par **origine**, le tableau devient bien plus favorable :

| route | deps totales | deps **locales** au monolithe |
| --- | --- | --- |
| `api_track_record` | 2 | **0** — `_track` et `scan_state` sont du paquet |
| `api_alerts_status` | 1 | 1 — `_ALERTS_FIRED` |
| `ibkr_ep` | 1 | 1 — `_ibkr_snapshot` |
| `quotes_ep` | 3 | 1 — `_sync_ibkr_state`… qui n'en avait aucune |

`_sync_ibkr_state` a donc pu **partir avec** : ses deux entrées, `_live_meta` et
`scan_state`, avaient déjà un domicile dans le paquet
(`vertex/app/caches.py`, `vertex/app/state.py`). Elle restait dans le monolithe
par habitude, pas par couplage.

```text
routes LEGACY      11 → 7
lignes terminal.py 7 174 → 7 169
blueprints du registre déclaratif  15 → 16
blueprints à injection             6 → 7
```

## Pourquoi une passerelle de quatre lignes méritait son propre module

`_sync_ibkr_state` est le **seul chemin** par lequel l'état réel du socket IBKR
atteint la page Système : `vertex/services/connections.py` lit
`scan_state['ibkr_connected']` et `['ibkr_live']`, que personne d'autre n'écrit.
La perdre afficherait un état de *configuration* — « IBKR activé » — au lieu d'un
état de *session*, c'est-à-dire exactement le mensonge que `connections.py`
existe pour éviter.

Son garde-fou de fraîcheur n'est pas cosmétique non plus : un worker figé garde
`connected: True` dans `_live_meta` — le socket n'est pas fermé, il ne répond
simplement plus. Sans borne d'âge, l'écran annoncerait « live » sur des ticks
vieux de plusieurs heures.

## `/quotes` refuse de servir des cours périmés

Au-delà de `ibkr_state.FENETRE_S`, la route rend **`quotes: {}}`** plutôt qu'une
table ancienne. Servir des cours d'il y a deux heures avec `fresh: true` serait
une valeur inventée au sens de la règle « données réelles uniquement » ; rendre
un objet vide est l'aveu honnête.

**Le seuil est emprunté, jamais recopié.** La route appelle
`ibkr_state.frais()` au lieu de réécrire `75`. Deux tables divergeraient au
premier ajustement, et `/quotes` servirait des cours que la page Système déclare
périmés — c'est précisément le défaut mesuré aux lots 62-64 sur les étiquettes de
fraîcheur, transposé du client au serveur. Un test interdit tout littéral `75`
dans la route.

## Le partage par référence, et pourquoi un test le vérifie

La boucle d'alertes **mute `_ALERTS_FIRED` en place**. Si `make_blueprint` en
prenait une copie, `/api/alerts/status` servirait l'état du démarrage pour
toujours — **et rien ne planterait**. C'est la même famille de défaut que
l'invariant `scan_state` (« muter en place, jamais réassigner ») : une rupture de
partage est silencieuse par nature. Le test mute le dictionnaire *après*
construction du blueprint et vérifie que la route le voit.

## Un détail d'ordre qu'il fallait mesurer

`live_state_api` n'est **pas** enregistré avec les six autres blueprints à
injection : ses deux dépendances (`_ibkr_snapshot`, `_ALERTS_FIRED`) sont
définies plus bas dans `terminal.py`, et l'enregistrer plus haut lèverait un
`NameError` à l'import. L'ordre est neutre pour le dispatch — mesuré : le dépôt
compte 4 règles en double, dont trois sont deux méthodes HTTP du même blueprint
et **aucune** ne concerne ces trois chemins.

## `track_record_api` : un module à lui seul, et pourquoi

La question s'était posée au lot précédent, qui avait laissé `/api/track-record`
en place faute de bon domicile. `tracking_api` gère des suivis **hypothétiques**
— « si j'avais pris cette position » ; celui-ci note le moteur sur ses verdicts
**passés**. Les ranger ensemble aurait fait gagner un chiffre à l'inventaire et
perdu la distinction, qui est exactement celle que #783 doit tenir entre mémoire
des résultats et simulation.

## Preuves

```text
compileall                     exit 0
pytest tests/ -q               3 299 passed        (3 289 avant le lot)
pytest tests/test_no_orders.py 3 passed
mutations du gardien           6/6 mordent, contrôle vert
```

Les six : `/quotes` sert des cours périmés · le garde-fou de fraîcheur saute ·
la fabrique copie le dictionnaire d'alertes · la route recopie le seuil ·
le monolithe reprend sa propre passerelle · `track_record_api` retiré du registre.

Serveur réel, `DEMO=1 NO_IBKR=1`, service workers bloqués :

```text
huit espaces                 200 · 0 débordement · 0 erreur console
/api/client-log              count: 0
/quotes /ibkr /api/alerts/status /api/track-record   200
```

## Les sept LEGACY restantes, et ce qu'il leur faut

| route | ce qui la retient |
| --- | --- |
| `/scan`, `/api/rescan` | la porte anti-rafale (`_rescan_evt`, `_rescan_gate_lock`, `RESCAN_COOLDOWN_SEC`, `_rescan_cooldown_remaining`) — un groupe **cohérent et déplaçable** |
| `/options/<sym>`, `/api/ticker/<sym>` | `options_pack`, une fonction du monolithe partagée par les deux |
| `/api/correlations/<sym>` | le trio `_CORR_MAP` / `_corr_benchmarks` / `_to_naive` |
| `/desc/<sym>` | le trio de cache de descriptions `_DESC_PATH` / `_FR_DESC` / `_desc_lock` |
| `/weekly-regen` | `WEEKLY_PATH` et `_earnings_map` |

Aucune n'est bloquée : chacune attend qu'un petit groupe de helpers auto-suffisant
parte avec elle, comme la passerelle IBKR l'a fait ici. C'est le même geste,
répété — pas un obstacle de nature différente.

**G1 reste non déclaré PASS.**
