# Vertex Ultimate Institutional OS — Baseline

Date : 2026-07-11 · Branche : `claude/vertex-strategy-os-h17dso`

> La mission demande `feature/vertex-ultimate-institutional-os` ;
> l'environnement de session n'autorise le push que sur la branche dédiée
> ci-dessus — tous les commits de cette passe s'y ajoutent, petits et
> réversibles. `main` n'est jamais modifié.

## État Git
- Commit initial de la passe : `ef6bf06` (fin de la passe Experience OS)
- Arbre de travail : propre.

## Tests initiaux
`python -m pytest tests/ -q` → **543 passed, 0 failed**.
Gardiens actifs : zéro nom personnel, zéro chemin d'ordre (appels et
définitions), IBKR `readonly=True` en dur, moteur de décision unique,
17 clés de sync canoniques, service worker v8, 27 tests UI canoniques.

## Architecture actuelle
- Monolithe `terminal.py` (boucles de fond + 13 routes legacy) +
  Blueprints `vertex/app/routes/` (auth, feeds, content, desk,
  analysis_api, command, options_lab_api, live_api, system, strategy_os,
  decision_api, tv_webhooks, redesign).
- Moteurs : `vertex/{strategy,options,portfolio,market,scanner,anomalies,
  data_sources,research,validation,ai,alerts,engines,observability,
  catalysts,quant,services,data}`.
- UI : shell unique + 8 pages (`vertex/ui/pages`), design system V3
  (13 feuilles CSS), 24 modules graphiques Chart.js, thème orange/ambre.

## Routes
9 pages + 21 sous-vues + 42 redirections 301 + ~60 routes API
(`docs/VERTEX_ROUTE_MATRIX.md`).

## État des intégrations (environnement cloud de la session)
- **IBKR** : hors ligne (pas de TWS) — passerelle `readonly=True` codée en
  dur, dégradé honnête vérifié (`ok:false`, marques « indisponibles »).
- **TradingView** : webhook actif (secret/anti-replay/dédup), secret absent
  → 503 honnête.
- **Claude runtime** : clé absente → repli déterministe étiqueté.
- **Stockage/sync** : `/api/desk` last-writer-wins + backups quotidiens.
- **Frontend** : 0 erreur console (8 pages, Chromium), 0 débordement sur
  7 viewports, télémétrie `/api/client-log` active.

## Captures
`docs/redesign/v3-after/` (8 pages × 5 tailles) = état de départ visuel
de cette passe (thème orange/ambre V3, AVANT Obsidian Copper Deep).

## Écarts identifiés vs la présente spécification (avant-travaux)
Voir `VERTEX_ULTIMATE_AUDIT.md` — notamment : R:R minimal à 1.5 (spec : 2),
régime UNKNOWN affichant « nouveau risque autorisé », bleu encore
identitaire (liens, série graphique n° 2), Brief sans actualités réelles,
pas de scheduler formalisé ni de flux SSE, pas d'analyse par position
option, compteurs CALLS/PUTS non séparés.
