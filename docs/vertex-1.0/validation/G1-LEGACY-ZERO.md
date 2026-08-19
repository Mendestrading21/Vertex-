# G1 · #779 — Les trois dernières routes LEGACY : **0**

Modules : `vertex/data/descriptions_fr.py`, `vertex/app/routes/descriptions_api.py`,
`vertex/options/pack.py`, `vertex/app/routes/ticker_api.py`
Gardien : `tests/test_vertex_1_0_legacy_zero_parity.py` (10 tests, 5 mutations)

---

```text
routes LEGACY      3 → 0        ← l'objectif de #779
lignes terminal.py 7 082 → 6 789
routes canoniques  151 → 154
stores du monolithe 3 → 2
```

`terminal.py` ne sert plus **aucune** route. Depuis le début de #779 :
**14 → 0**, et 7 276 → 6 789 lignes.

## Le défaut que ce lot a introduit — et que la parité a attrapé

En retirant `/api/ticker`, la coupe est allée du décorateur jusqu'au commentaire
de section suivant. **L'enregistrement du blueprint `desk` vivait dans cet
intervalle.** Sept routes du poste personnel — synchronisation, sauvegardes,
restauration, cotation des positions — ont disparu du service.

Rien n'a levé d'erreur : Flask ne se plaint pas d'un blueprint qu'on
n'enregistre pas. La suite était verte. Le compte de règles est passé de 194 à
**187**, et c'est le **diff avant/après de l'ensemble complet** qui l'a montré.

C'est exactement la raison d'être du filet posé au premier lot de #779 :
comparer toutes les règles, pas seulement celles qu'on croit toucher. Le test le
plus important de ce lot rejoue cette vérification à l'endroit précis où elle a
mordu.

## Ce qui est parti avec quoi, et pourquoi ensemble

| ce qui partait | ce qui devait partir avec | pourquoi |
| --- | --- | --- |
| `/desc/<sym>` | `_FR_DESC` → `vertex/data/` | c'est une **donnée**, pas un helper : 20 fiches d'activité écrites à la main, qui servent en démo et en secours de throttle |
| `/desc/<sym>` | son cache disque | le chemin passe par `persist.cache_path` — un `dirname(__file__)` l'aurait fait pointer dans `routes/` |
| `/options`, `/api/ticker` | `options_pack` (143 l.) | mesuré : sur 18 symboles utilisés, **3** seulement étaient locaux |
| `options_pack` | `_i` / `_f` **et leurs deux garde-fous** | le `0` des coerceurs n'est inoffensif **que** parce que `if iv <= 0 or oi <= 0` et `if K < lo or K > hi` l'écartent avant tout calcul servi |
| `options_pack` | `_OPTALL_CACHE` → 9ᵉ cache canonique | partagé par **trois** parties : chargement disque, `_opt_loop`, fiche ouverte |

Le monolithe **remplit** ce cache (`.update(...)`) au lieu de le réassigner :
une réassignation séparerait la boucle de la route sans qu'aucune erreur ne soit
levée — le même piège que `scan_state`.

## Quinze gardiens maison ont réagi — aucun contourné

Le lot était trop gros ; le nombre de conséquences le dit mieux que moi. Chacune
a été traitée en visant ce qu'elle protège, jamais en desserrant :

| gardien | ce qu'il a vu | traitement |
| --- | --- | --- |
| `test_xss_exits_lot177` | 5 sites de `sanitize_news` au lieu de 6 | le 6ᵉ vivait **dans** `options_pack` et a déménagé avec lui — l'assainissement suit le code qui sert la donnée. Périmètre étendu |
| `test_replis_racine_lot385` ×4 | coercitions et garde-fous introuvables dans `terminal.py` | ils ont déménagé **ensemble**, ce qui préserve le raisonnement. Recensement et gardes retargetés |
| `test_replis_exception_lot378` | deux replis numériques non recensés dans `vertex/` | ce sont `_i`/`_f`, arrivés avec leur appelant. Recensés, avec leur justification |
| `test_pass_terminal_lot386` | 35 → 32 `except: pass` | les 3 sont partis **avec** le code qu'ils entouraient |
| `test_pass_et_contexte_lot379` | 47 → 50 dans `vertex/` | mêmes 3 handlers, de l'autre côté de la frontière. Le total des deux périmètres est stable ; c'est la frontière qui a bougé |
| `test_option_price_integrity` | patchait `terminal.options_pack` | la route résout le nom dans **son** espace ; patcher le monolithe ne l'atteint plus |
| `test_refus_variable_lot392` | patchait `terminal._DESC_PATH` | retargeté sur le module qui tient la route |
| `test_vertex_1_0_caches_parity` | un 9ᵉ cache non déclaré | déclaré, avec une nature nouvelle : `cache-persiste` — un cache mémoire perdu se reconstruit, un cache disque périmé sert des chaînes d'hier |
| `test_terminal_imports_lot324` | `math`, `jsonify` orphelins | retirés |
| `test_namespace_guards` ×2 | un verbe français dont une sous-chaîne est le prénom surveillé — **dans mon rapport du lot précédent**, où je décrivais déjà ce faux positif | reformulé, deux fois |
| `test_vertex_1_0_factory_parity` | 19 → 21 entrées | mis à jour |

## Preuves

```text
compileall                     exit 0
pytest tests/ -q               3 330 passed        (3 320 avant le lot)
pytest tests/test_no_orders.py 3 passed
diff des règles avant/après    194 = 194, seuls les 3 propriétaires changent
mutations                      5/5 mordent, contrôle vert
```

Les cinq : l'enregistrement du blueprint `desk` saute (**la vraie régression**) ·
le monolithe réassigne le cache d'options · un garde-fou reste derrière ·
`/desc` mémorise aussi les échecs · la politique du 9ᵉ cache disparaît.

Serveur réel, `DEMO=1 NO_IBKR=1` :

```text
huit espaces        200 · 0 débordement · 0 erreur console
/api/client-log     count: 0
/desc /options /api/ticker                    200
/api/desk /api/desk/backups /api/watchlist-tv 200   ← les routes rescapées
```

## État de G1

| responsabilité | propriétaire |
| --- | --- |
| factory Flask | `vertex/app/factory.py::create_app` |
| routes | `factory.BLUEPRINTS` (21 sans injection) + 7 à injection **documentées** |
| lifecycle / workers | `vertex/app/lifecycle.py` |
| scheduler | `vertex/scheduler/registry.py` |
| **routes LEGACY** | **0** |

Ce qui reste dans `terminal.py` : les 13 boucles de service, 7 blueprints à
injection dont l'état y vit encore, et les pages HTML incorporées.

**G1 n'est toujours pas déclaré PASS** — la décision revient à l'humain, sur le
SHA candidat.
