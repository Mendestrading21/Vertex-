# Vertex Master Redesign — Baseline

Date : 2026-07-11
Branche de travail : `claude/vertex-strategy-os-h17dso`

> Note : la mission demandait une branche `feature/vertex-master-redesign-os`.
> L'environnement d'exécution de cette session impose de développer et pousser
> uniquement sur la branche dédiée `claude/vertex-strategy-os-h17dso` — la
> refonte y est donc livrée, en commits distincts et réversibles, à la suite
> des commits Strategy OS.

## Commande

```
python -m pytest tests/ -q
```

## Résultat

```
414 passed
```

Commit de départ : `58956cc` (test+docs(vertex): system-wide regression guards
and Strategy OS documentation).

## État initial de l'interface

- Monolithe `terminal.py` : pages HTML/CSS/JS générées en chaînes Python,
  navigation « rail » injectée, ~20 routes de pages (dont plusieurs cachées).
- Pages extraites : `vertex/ui/*.py` (nav, journal, options_lab, vault,
  signals, sync_center, vx_kit, design_system, home_art, strategy_os).
- Assets statiques : `static/chart.umd.min.js` (Chart.js), icône PWA.
- Service worker : `td-shell-v5`.
- Données personnelles utilisateur : localStorage (`myTrades`, `myFavs`,
  `vxAlerts`, `vxJournal`…) synchronisé serveur via `/api/desk`
  (last-writer-wins + `deskTs`).
- Captures avant refonte : `docs/redesign/before/`.
