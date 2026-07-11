# Vertex Full Production OS — Baseline

Date : 2026-07-11 · Branche : `claude/vertex-strategy-os-h17dso`

> La mission demandait `feature/vertex-full-production-os` ; l'environnement
> de session impose la branche dédiée ci-dessus (seule branche autorisée au
> push). Les commits de cette passe s'y ajoutent, petits et réversibles.

## État Git
- Commit initial de la passe : `01e58ef` (test(ui)+docs(ui): browser
  journeys, after-captures, sync flush, final documentation)
- Arbre de travail : propre (aucune modification locale non commitée)

## Tests
- `python -m pytest tests/ -q` → **448 passed**, 0 failed
- Gardiens actifs : zéro nom personnel, zéro chemin d'ordre, IBKR readonly,
  décision unique, clés de sync canoniques (17), service worker v6.

## Erreurs connues / limitations déclarées (avant cette passe)
Voir `docs/VERTEX_MASTER_REDESIGN_IMPLEMENTATION.md` §12 : OHLC non exposé
par le scan (candlestick en repli clôtures), MM en série non fournies,
comparateur multi-titres redirigé, simulateur paper legacy sans UI dédiée,
secteurs en anglais dans les filtres, brief IA branchable non branché.

## Routes connues
8 espaces (`/`, `/markets`, `/opportunities`, `/portfolio`, `/analysis[/sym]`,
`/performance`, `/intelligence`, `/system`) + 21 sous-vues + 43 redirections
301 + ~45 routes API (matrice complète : `docs/VERTEX_ROUTE_MATRIX.md`).

## Captures initiales
`docs/redesign/before/` (20, avant refonte) et `docs/redesign/after/`
(29, état actuel — servent de référence visuelle à cette passe).

## État des intégrations (mode d'exécution de la session : cloud démo)
- IBKR : hors ligne dans cet environnement (pas de TWS) — mode dégradé
  vérifié, `readonly=True` codé en dur, `order_execution: disabled-by-design`.
- TradingView : webhook actif mais `TRADINGVIEW_SECRET` absent → 503 honnête.
- Claude (runtime Vertex) : clé absente → repli déterministe vérifié.
- Service worker : `td-shell-v6`.

## Vérification noms personnels
`rg -ni --hidden --glob '!.git/**' '(elio|mendes)' .` → **0 occurrence**.
