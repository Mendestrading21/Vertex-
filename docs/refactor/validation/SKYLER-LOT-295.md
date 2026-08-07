# SKYLER LOT 295 — Balayage tactile terminé : tickers et liens dim tappables

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-295` (base : lot 294 fusionné)

## Contexte — état de la purge É1 (prioritaire, bloquée permissions)

Inchangé : GO acquis, moitié tests poussée (`agent/skyler-v2-lot-285`,
b8d3842), retrait terminal.py en attente de déblocage utilisateur.

## Piste calibrée — les 12 vues profondes restantes (390)

Le sondeur des lots 293/294 étendu aux 12 vues pas encore balayées :
markets rotation/indices, opportunities shortlist, portfolio
positions/performance, journal journal/hypotheses, options
lab/screener, system connections/health, /tracking.

**10 vues sur 12 SAINES.** Deux défauts réels :

1. **Boutons tickers de la shortlist** (`button.vx-link
   [data-open-analysis]`, Opportunités) : **21px** de haut — ce sont
   les cibles principales de la table (ouvrir l'analyse d'un titre).
   `.vx-link` n'a aucune définition CSS et n'est utilisé que là.
2. **Lien nu dans une ligne `vx-dim`** (Journal → Hypothèses,
   « Portefeuille → Performance ») : **16px** — même famille que les
   liens `.vx-meta a` du lot 293, motif différent.

## Livré

`responsive.css` (bloc ≤640px) : `.vx-link{min-height:40px}` +
`.vx-dim a{display:inline-block;padding:13px 0}` (règle séparée pour
laisser le gardien du lot 293 intact). Desktop intact.

## Gardien neuf — `tests/test_ticker_links_touch_lot295.py` (2 tests)

Les deux règles présentes dans le bloc mobile.

## Preuves (navigateur réel, DEMO)

- Re-balayage des 12 vues : **plus aucune cible < 32px, 0 erreur,
  0 débordement, 0 texte cassé**. Capture envoyée.
- Avec les lots 293/294 : **18 vues profondes balayées au total** —
  l'inventaire tactile des pages est couvert.
- Suite complète : **2506 passed / 2 skipped** (+2).

## Décision SW

**Bump v181 → v182** (CSS du shell visible change) + les 5 gardiens.

## Suite

LOT 296 : purge É1 en PRIORITÉ dès déblocage ; sinon développement
(le balayage tactile est terminé — chercher un angle différent).
