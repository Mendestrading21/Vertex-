# Validation — PR n°3 : Refonte Aujourd'hui + Marchés

> Branche `agent/vertex-total-rebuild`. Première refonte produit **visible**.
> Aujourd'hui **résume**, Marchés **explique** ; une donnée = un seul domicile.
> Conforme à `VERTEX_CONSTITUTION.md`, `VERTEX_PRODUCT_BIBLE.md` (§3.1, §3.2),
> `PRODUCT_EXPERIENCE_REVIEW.md`. Aucun moteur financier modifié, IBKR READONLY
> intact, pas de migration big-bang.

## 1. Fichiers modifiés

- `vertex/ui/pages/briefing.py` — refonte complète (596 → 375 lignes).
- `vertex/ui/pages/markets_page.py` — dé-duplication des graphiques (secteurs,
  breadth, volatilité).
- `vertex/app/routes/system.py` — bump service worker `td-shell-v45 → v46`.
- Tests : `tests/test_cockpit.py` (structure refondue), + gardiens SW
  (`test_production_guards_canonical.py`, `test_ui_v3.py`, `test_redesign_ui.py`).

## 2. Structure avant / après

### Aujourd'hui (`/`)
| Avant | Après |
|---|---|
| Brief hero + Régime + **strip indices** + **Pouls (3 jauges)** + **SPY area + breadthCard** + **Top/Flop** + Opportunités + **R:R bars** + **posture donut** + **rotation** + Alertes + Portefeuille + Calendrier | **Hero éditorial** (phrase + régime + confiance + Freshness Badge + risque + opportunité) + **4 KPI cliquables** (Régime/Breadth/VIX/Meilleure opp.) + **1 action** · **Diff « depuis ta dernière visite »** + Régime (jauge) · ≤3 Opportunités + ≤3 Alertes · Catalyseurs (≤3) + Portefeuille (changements) |
| Densité anarchique, ~13 blocs, recopie de Marchés | Résumé hiérarchisé (Réponse → Justification), aucun doublon de Marchés |

### Marchés (`/markets`)
| Vue | Avant | Après |
|---|---|---|
| Secteurs | bar + heatmap + treemap + RRG (**4**) | **RRG + heatmap (2)** |
| Breadth | jauge + **breadthCard(1-barre)** + trend + verdicts + funnel + **rings** + waterfall (**7**) | jauge + trend + verdicts + funnel + waterfall (**5**) |
| Volatilité | jauge VIX + **jauge régime** + **jauge breadth** (**3**) | **jauge VIX** + rail stress + régime (texte) (**1**) |
| Vue d'ensemble / Macro | inchangées (régime, SPY, indices, taux, calendrier) | inchangées (domicile canonique de SPY/indices/macro) |

## 3. Graphiques supprimés

- **Aujourd'hui** : 3 jauges Pouls (VIX/Breadth/Régime), SPY areaCard,
  breadthCard (1-barre), rotation sectorCard, R:R bars, posture donut,
  sparklines du strip. *(Top/Flop tables retirées aussi.)*
- **Marchés** : sectorCard (bar secteurs), treemap secteurs, breadthCard
  (1-barre), rings (anneaux participation), jauge régime (volatilité), jauge
  breadth (volatilité).

## 4. Graphiques fusionnés / consolidés

- Secteurs : 4 grammaires pour un même message `scan.sectors` → **2** (RRG
  décisionnel + heatmap de détail).
- Régime/VIX/Breadth : plus **aucune jauge dupliquée** entre Aujourd'hui,
  Marchés-Vue d'ensemble et Marchés-Volatilité. Chaque métrique a **un domicile**
  (Aujourd'hui n'en montre qu'un **résumé cliquable**).

## 5. Graphiques reconstruits

- **Aujourd'hui** : `régime gauge` conservé (dans le résumé), `catalyst timeline`
  reconstruite avec conclusion (« Prochain : … ») et ≤3 items.
- **Nouveaux composants** : Hero éditorial, 4 KPI-résumé cliquables, **Diff
  honnête** (baseline localStorage ; « Aucun historique de comparaison
  disponible » au premier passage), Freshness Badge dans le Hero.

## 6. Nombre de graphiques avant / après

| Espace | Avant | Après | Δ |
|---|---|---|---|
| **Aujourd'hui** | **11** | **2** | −9 |
| **Marchés** | **~19** | **13** | −6 |
| **Total** | 30 | 15 | **−15 (−50 %)** |

Duplications inter-pages supprimées (Aujourd'hui↔Marchés) : SPY, breadth,
rotation, VIX/régime jauges, calendrier détaillé → **résumés cliquables** pointant
vers le domicile canonique.

## 7. Composants utilisés

Hero éditorial · Freshness Badge (`vx-freshness`) · KPI cliquable (`vx-kpi`
`vx-card--compact`) · Diff « depuis la dernière visite » · Alert rows ·
Opportunity rows · Catalyst Timeline (`timelineCard`) · Régime gauge · États
Empty/Error/Demo (`VX.states`, `vx-demo-banner`) · Chart Shell (`C.card` :
titre/question/conclusion/source/fraîcheur) sur les graphiques conservés.

## 8. Tests exacts

- `python -m compileall -q terminal.py vertex` → **exit 0**.
- `python -m pytest tests/ -q` → **908 passed, 2 skipped**.
- Gardiens mis à jour : `test_markets_volatility_single_reading` (jauges
  dupliquées absentes), `test_breadth_selection_funnel_real_data` (rings + barre
  absentes, funnel/tendance présents), `test_cockpit_directional_value_semantics_in_briefing`
  (VIX jamais coloré directionnellement), `test_briefing_is_summary_not_markets_copy`
  (Hero+diff présents, duplications Marchés absentes). Routes Aujourd'hui/Marchés
  200 (`test_every_primary_route_returns_200`, `test_subviews_return_200`).

## 9. Contrôle navigateur (390 / 768 / 1440)

Overflow réel (contenu hors conteneur de scroll intentionnel) :

| Viewport | today | markets | mk-sectors | mk-breadth | mk-vol |
|---|---|---|---|---|---|
| **390 mobile** | OK | OK | OK | OK | OK |
| **768 tablet** | OK | OK | OK | OK | OK |
| **1440 desktop** | OK | OK | OK | OK | OK |

- **0 erreur console applicative** (la refonte JS d'Aujourd'hui s'exécute
  proprement) ; `/api/client-log` = `{"count":0,"errors":[]}`.
- Démo : badge DÉMO présent ; sans-IBKR : états honnêtes (pas de zéro inventé).
- Diff honnête vérifié : « Aucun historique de comparaison disponible » au premier
  passage, puis deltas.
- Captures : scratchpad `pr3shots/` (desktop + mobile de Aujourd'hui et
  Marchés-Secteurs).

## 10. Captures desktop / mobile

Voir `pr3shots/desktop-today.png`, `pr3shots/mobile-today.png`,
`pr3shots/desktop-mk-sectors.png`, `pr3shots/mobile-mk-sectors.png`.

## 11. Erreurs restantes

- Console applicative : **0**. (`ERR_CONNECTION_RESET` = Google Fonts via proxy
  sandbox, non applicatif.)

## 12. Risques

- **Densité/personnalisation retirées d'Aujourd'hui** : simplification assumée
  (les blocs personnalisables n'existent plus). Aucune donnée perdue ; les détails
  vivent dans leur espace canonique.
- **Réduction Marchés partielle** : la Vue d'ensemble et Macro n'ont pas été
  retouchées (SPY/indices/taux y sont canoniques) ; d'autres consolidations
  (funnel/verdicts/waterfall de Breadth) restent possibles en finition.
- **Scripts de charts inutilisés** encore inclus dans Marchés (sector-chart.js,
  breadth-chart.js) — factories dormantes, retrait cosmétique différé.
- Validation Chromium **headless** (pas d'appareil physique).

## 13. Prochaine PR recommandée : Opportunités + Analyse

- **Opportunités** : entonnoir → short-list S+/S en tête ; `op-radar` renommé en
  **scatter** explicite ; scoreBar HTML → Chart Shell ; 1 tableau principal trié ;
  action ligne « → Ouvrir le dossier » (≤2 clics vers Analyse).
- **Analyse** : **Carte-Verdict** (verdict + score/40 + confiance + entrée +
  invalidation) + **Carte-Scénario** (pessimiste/probable/exceptionnel) en tête ;
  intégrer le **raisonnement du comité** (depuis Intelligence) ; radar scorecard
  unique ; chandeliers LWC conservés.
- Cible : chaque graphique avec conclusion ; 0 débordement 390/768/1440 ; 0
  console ; contexte ticker préservé ; SW bump ; READONLY intact ; captures
  avant/après + comptes de graphiques.

## Verdict

**GO.** Aujourd'hui et Marchés sont désormais complémentaires (résumé vs
explication), sans duplication ; **30 → 15 graphiques (−50 %)** ; 908 tests verts ;
0 débordement ; 0 erreur console. Fondations produit posées pour la refonte
d'Opportunités + Analyse.
