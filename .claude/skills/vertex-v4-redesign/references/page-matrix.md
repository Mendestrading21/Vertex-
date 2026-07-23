# Vertex V4 — matrice des pages

| Lot | Espace | Route | Renderer baseline / cible | Sous-vues principales |
|---:|---|---|---|---|
| 05 | Briefing | `/` | `briefing.py` | synthèse, alertes, calendrier, news |
| 06 | Marchés | `/markets` | baseline : ancres Briefing ; cible : renderer de présentation dédié | overview, macro, secteurs, breadth, volatilité |
| 07 | Opportunités | `/opportunities` | `opportunities_page.py` | radar, actions, options, anomalies, calendrier |
| 08 | Portefeuille | `/portfolio` | `portfolio_page.py` | équipe, positions, risque, watchlist |
| 09 | Analyse | `/analysis`, `/analysis/<sym>` | `analysis_page.py` | recherche, fiche titre |
| 10 | Options | `/options`, `/options/<sym>` | `options_intel_page.py`, `options_symbol_page.py` | overview, volatilité, radar, scénarios, événements |
| 11 | Performance | `/performance` | `performance_page.py` | overview, journal, track-record, learnings |
| 12 | Intelligence | `/intelligence` | `intelligence_page.py` | analyste, comité, stratégie, impacts, recherche, mémoire |
| 13 | Système | `/system` | `system_page.py` | connexions, données, automatisations, réglages, archive |

`/tracking` et `/design-system` sont des vues de soutien. Elles suivent les mêmes
fondations et sont couvertes par les lots 14 et 15.

Avant chaque lot, confirmer les routes et fichiers dans le code réel ; cette
matrice décrit l'intention, pas une autorisation de recréer un module absent.
