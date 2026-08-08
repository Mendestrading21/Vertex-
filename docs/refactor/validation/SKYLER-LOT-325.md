# SKYLER LOT 325 — L'audit d'imports étendu à tout `vertex/` : 11 morts, 1 piège évité

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-325` (base : lot 324 fusionné,
233c376)

## La piste

Le lot 324 a nettoyé le monolithe. La question honnête : le reste du dépôt
est-il dans le même état ? Audit AST des **183 modules** de `vertex/`.

Premier passage : 192 « orphelins » — chiffre trompeur. **180 d'entre eux sont
`from __future__ import annotations`**, une directive du compilateur qui n'est
jamais référencée par un nom. Faux positif, exclu.

Reste **12 imports réellement suspects** dans 12 modules. Chacun vérifié
individuellement : aucun n'est ré-importé ailleurs (`from <module> import <nom>`
→ 0 hit pour les 12), et chaque nom n'apparaît qu'une fois dans son fichier :
la ligne d'import elle-même.

## Le piège évité — 1 des 12 n'était pas mort

`vertex/services/startup.py` L82 :

```python
def live():
    try:
        from vertex.services.live_stream import BROKER
        return 'READY', 'flux SSE prêt (repli polling côté client)'
    except Exception:
        return 'DEGRADED', 'SSE indisponible — polling seul'
```

**L'import EST le diagnostic.** Le retirer aurait fait passer l'étape de
démarrage « live_stream » en READY inconditionnel — un mensonge sur l'état du
flux SSE, exactement le genre de chose que l'invariant « données réelles »
interdit. Il est **conservé**, marqué `# noqa: F401` et commenté pour qu'aucun
nettoyage futur (le mien comme un autre) ne le reprenne.

C'est le seul intérêt réel de ce lot : la différence entre un import mort et un
import qui travaille sans être lu ne se voit pas dans un compteur.

## Les 11 retraits

| module | import mort |
|---|---|
| `anomalies/data_anomalies.py` | `SEV_INFO` |
| `app/routes/tracking_api.py` | `time` |
| `data_sources/source_router.py` | `Iterable` |
| `engines/track_record.py` | `os` |
| `options/contract_scorer.py` | `CATEGORY_BALANCED`, `CATEGORY_BEARISH_TACTICAL` |
| `options/environment.py` | `volatility as vol` |
| `quant/pivots.py` | `numpy as np` |
| `research/hypothesis.py` | `LifecycleError` |
| `scanner/stages.py` | `any_blocking` |
| `strategy/memory/store.py` | `STATUSES` |

Tous ces noms restent définis et utilisés **ailleurs** (par ex. `SEV_INFO` est
bien consommé par `vol_surface.py` et `stock_anomalies.py`, qui l'importent
depuis `anomalies/models.py`) : ce sont des imports locaux devenus inutiles, pas
des symboles supprimés.

## Preuves

- `compileall terminal.py vertex` exit 0 ; diff sur `vertex/` : **14 deletions /
  8 insertions** sur 11 fichiers (les insertions = lignes d'import raccourcies
  + les 2 lignes de commentaire du `noqa`).
- **MD5 des 8 pages servies IDENTIQUES aux références des lots 323/324** :
  `/` fc15688d1af6 · `/markets` c0bb91c6971a · `/opportunities` 6a22a6abbd03 ·
  `/analysis` 113827718e99 · `/portfolio` f1b41b665d4a · `/options` 6387210de785 ·
  `/journal` 243699ace2d5 · `/system` 85d1cb065d2e → **pas de bump SW**.
- Navigateur (`tools/probe_smoke.py`) : 8 × HTTP 200, **0 erreur
  console/pageerror**, `client-log count: 0`.
- Suite : **2501 passed / 2 skipped** (2500 + le second gardien).

## Le gardien étendu

`tests/test_terminal_imports_lot324.py` gagne
`test_no_orphan_imports_in_vertex_package` : même analyse AST sur les 183
modules. Exclusions **documentées et minimales** — `import *`, lignes `# noqa`,
`from __future__ import annotations`, et les `__init__.py` dont ré-exporter est
le métier.

## Décision SW

**Pas de bump** (`td-shell-v186`) : MD5 identiques, zéro octet servi modifié.

## Invariants

READONLY intact, aucune logique modifiée (seules des lignes d'import changent),
`main` non touchée, aucun fichier runtime commité.

## Suite

LOT 326 : veille active (référence de suite **2501 / 2**). É2/É3 de la purge
restent en attente de GO explicite. Prochaine échéance périodique : ~lot 330.
