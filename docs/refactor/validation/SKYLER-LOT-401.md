# SKYLER LOT 401 — Un gardien qui passe selon l'ordre : la clé documentée que la remise en état supprimait

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-401` (base : lot 400 fusionné,
00e40c9)

Point de contrôle **jamais balayé** : les tests qui mutent un état global sans le
remettre en état. Le lot 387 en avait trouvé **un**, par hasard ; le périmètre
entier n'avait jamais été mesuré.

## Deux instruments, tous deux corrigés avant de servir

**1. Détecteur statique (AST).** État global retenu, liste explicite :
`scan_state` (le dict partagé documenté par `CLAUDE.md`), `os.environ`, et les
attributs de module importés. Sûrs : `monkeypatch`, restauration dans un
`finally`, fixture `yield` avec teardown.

```text
fonctions analysées                                  3034
   mutant un état global                               50
      protégées (monkeypatch / finally / teardown)     36
      NUES                                             14
```

Témoin obligatoire : un fichier de contrôle avec 3 mutations nues, une protégée
par `finally`, une par `monkeypatch`, une fixture à teardown. Les 3 nues sont
signalées, les 3 sûres restent muettes.

**Mais ces 14 ne sont que des hypothèses** : une fonction d'aide qui mute
`scan_state` peut être appelée depuis un test protégé. Seule l'exécution tranche.

**2. Détecteur d'exécution.** Empreinte de l'état global avant/après **chaque**
test. Il a fallu le corriger **deux fois**, et les deux corrections comptent :

- première version : `pytest_runtest_teardown` s'exécute **avant** les finalizers
  de `monkeypatch` → **84 « fuites »**, dont 42 étaient des restaurations
  parfaitement faites. Corrigé en enveloppant `pytest_runtest_protocol` ;
- le témoin négatif mordait aussi : `PYTEST_CURRENT_TEST` est réécrit par pytest
  à chaque phase de chaque test. Exclu de l'empreinte.

Et un témoin insuffisant a été refait : le premier cas « monkeypatch » écrivait
une valeur **déjà présente** — écriture idempotente, donc invisible, donc
concluante à tort (leçon du 389). Rejoué avec une valeur réellement différente
et une assertion prouvant la mutation effective, `monkeypatch` reste muet : sûr,
**vérifié**.

```text
avec l'instrument corrigé :  84 → 8 fuites réelles sur 2 864 tests
```

## La trouvaille — un gardien vert pour une mauvaise raison

Parmi les 8, une seule change **l'ensemble des clés** de `scan_state` par
suppression : `test_skyler_sweep_x1.py::test_sweep_route_and_no_journaling`.

```python
saved = {k: scan_state.get(k) for k in ('detail', 'market', 'market_ctx')}
…
finally:
    for k, v in saved.items():
        if v is None:
            scan_state.pop(k, None)     # ← confond « valeur None » et « clé absente »
```

`vertex/app/state.py` initialise `'market_ctx': None`. La clé **existe** et sa
valeur légitime **est** `None`. La remise en état la **supprimait** donc du dict
partagé, définitivement, pour le reste de la session.

Conséquence, prouvée par la plus petite reproduction possible — **deux
fichiers** :

```text
pytest tests/test_skyler_sweep_x1.py tests/test_state.py   →  1 failed
pytest tests/test_skyler_sweep_x1.py                       →  9 passed
pytest tests/test_state.py                                 →  4 passed
```

```text
AssertionError: assert 'market_ctx' in {'rows': [...], 'detail': {}, ...}
tests/test_state.py:14
```

Le test qui tombe est `test_scan_state_has_expected_keys` — **le gardien dont le
métier est précisément de vérifier que les 8 clés documentées existent**. Il
passe dans la suite complète, et échoue dès qu'on rejoue un sous-ensemble : son
verdict dépendait de l'ordre d'exécution.

Mesuré aussi : la queue de **66 fichiers** qui suit ce test échouait de la même
façon (`1 failed, 664 passed`).

*Une hypothèse écartée en la testant* : j'ai d'abord cru que la suite complète
passait grâce à une seconde fuite (`test_market_context.py`) laissant
`market_ctx` non-`None`. **Faux** — placer ce fichier devant laisse l'échec. Je
ne sais pas quel test, dans la suite complète, recrée la clé ; je le dis plutôt
que de l'inventer. Ce qui est établi ne dépend pas de cette réponse : la
suppression a lieu, et le gardien y est sensible.

## Le correctif

Mémoriser la **présence** de la clé, pas sa vérité :

```python
saved = {k: (k in scan_state, scan_state.get(k))
         for k in ('detail', 'market', 'market_ctx')}
…
finally:
    for k, (presente, v) in saved.items():
        if presente:
            scan_state[k] = v
        else:
            scan_state.pop(k, None)
```

```text
repro minimale (2 fichiers)        1 failed → 13 passed
queue de 66 fichiers               1 failed → 665 passed
[témoin] ancienne logique remise    1 failed  — c'est bien elle qui décidait
suite complète                     2864 passed / 0 skipped
```

Un seul fichier de test modifié. **Aucune production touchée.**

## Les 7 autres fuites — mesurées, pas corrigées

```text
tests/test_gamma_surveillance.py   3 tests   scan_state
tests/test_market_context.py       1 test    scan_state (+ clés)
tests/test_options_routes.py       1 test    scan_state
tests/test_portfolio_stress.py     1 test    scan_state
tests/test_pretrade.py             1 test    scan_state (+ clés)
```

Vérifié : **aucune ne retire une clé documentée** — elles ajoutent ou écrasent
des valeurs. Rejouées ensemble puis suivies du gardien : `72 passed`. Ce sont des
pollutions **latentes**, pas des défauts actifs ; les corriger à l'aveugle
changerait ce que ces tests mesurent, pour un bénéfice non démontré. **Classées.**

## Un dossier que ce lot ouvre — et n'exécute pas

La 8ᵉ fuite est d'une autre nature. `tests/test_refus_variable_lot392.py` (mon
propre lot 392) porte une fixture **de portée module** qui fait :

```python
persist._BASE_DIR = tempfile.mkdtemp(prefix='lot392-')
```

sans jamais restaurer. La persistance est donc redirigée vers un dossier
temporaire **pour tout le reste de la session** — mesuré : **678 tests**, soit
24 % de la suite, s'exécutent après.

**Et ce défaut protège aujourd'hui plus qu'il ne nuit.** Rejouée seule, avec un
`_BASE_DIR` réel, cette queue écrit dans **`skyler_decisions.json` et
`skyler_memory.json`** — deux fichiers runtime du dépôt. Autrement dit :

> restaurer naïvement `_BASE_DIR` **réintroduirait** des écritures réelles dans
> le stockage de l'utilisateur.

Le bon correctif n'est donc pas « remettre en état » mais décider **où** la
persistance doit pointer pendant la suite — et ce choix n'est pas neutre :
certains tests lisent délibérément le **vrai** `desk_data.json`
(`test_funnel_positions_match_desk` compare l'entonnoir au desk réel). Une
redirection globale changerait leur sens. **Décision, pas réparation : classé au
rang 2.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure
  (leçon du 400).
- **Aucun fichier de production touché** — un seul fichier de test. Pas de
  preuve MD5 requise, pas de bump. SW : `td-shell-v187`.
- Snapshot des 22 fichiers runtime avec contrôle d'apparition. Les sondes de ce
  lot ont écrit `skyler_decisions.json` et `skyler_memory.json` (queue rejouée
  avec un `_BASE_DIR` réel) en plus des trois horodatages habituels : tous
  restaurés depuis le snapshot. Écart final **aucun**, aucun fichier apparu.
- Suite : **2864 passed / 0 skipped**, inchangée — aucun test ajouté, et c'est
  délibéré.

## Portée

Les deux détecteurs ne voient que l'état global **listé explicitement**
(`scan_state`, `os.environ`, attributs des trois modules connus pour être
détournés). Un test qui polluerait un autre singleton — un cache mémoire, une
variable de module non listée — passerait au travers. Et « 8 fuites » ne vaut que
parce que l'instrument a été validé par témoin, puis corrigé deux fois.

## Où en est la boucle

Sixième lot court d'affilée, sixième point de contrôle distinct. Celui-ci a
trouvé un **gardien vert pour une mauvaise raison** — le genre de défaut qu'une
suite verte ne signale jamais.

La question du **bilan n°9 (lot 400) attend toujours une réponse** : aucun GO
depuis le lot 388, tous les dossiers de rang 1 à l'arrêt.
