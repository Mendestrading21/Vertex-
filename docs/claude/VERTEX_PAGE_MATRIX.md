# VERTEX — Matrice des pages et sous-vues

| Espace | Route | Fichier principal | Sous-vues actuelles | Question métier |
|---|---|---|---|---|
| Briefing / Dashboard | `/` | `vertex/ui/pages/briefing.py` | page unique personnalisable | Que dois-je comprendre et surveiller aujourd’hui ? |
| Marchés | `/markets` | `vertex/ui/pages/markets_page.py` | overview, macro, sectors, breadth, volatility | Dans quel environnement la stratégie opère-t-elle ? |
| Opportunités | `/opportunities` | `vertex/ui/pages/opportunities_page.py` | radar, stocks, options, anomalies, calendar | Quelles opportunités méritent réellement une analyse ? |
| Portefeuille | `/portfolio` | `vertex/ui/pages/portfolio_page.py` | team, positions, options, risk, watchlist | Que possède le portefeuille et comment doit-il évoluer ? |
| Analyse | `/analysis` + fiche ticker | `vertex/ui/pages/analysis_page.py` | index + fiche canonique | Ce dossier mérite-t-il du capital maintenant ? |
| Options | `/options` | `vertex/ui/pages/options_intel_page.py` | overview, volatility, radar, scenarios, events | Où est la meilleure convexité et quel événement la menace ? |
| Performance | `/performance` | `vertex/ui/pages/performance_page.py` | overview, journal, track-record, learnings | La méthode fonctionne-t-elle et est-elle correctement exécutée ? |
| Intelligence | `/intelligence` | `vertex/ui/pages/intelligence_page.py` | analyst, committee, strategy, impacts, research, memory | Comment Vertex raisonne-t-il et évolue-t-il ? |
| Système | `/system` | `vertex/ui/pages/system_page.py` | connections, data, automations, settings, archive | Le système est-il sain et branché sur du réel ? |
| Tracking | `/tracking` | script/page tracking existant | suivis hypothétiques | Les idées suivies tiennent-elles mieux que SPY ? |
| Design system | `/design-system` | page de démonstration existante | référence interne | Le système visuel est-il cohérent ? |

## Incohérences de documentation à corriger

- `vertex/ui/shell/__init__.py` indique encore « huit espaces » alors que `PRIMARY_NAV` contient neuf entrées.
- `vertex/ui/pages/options_intel_page.py` affirme encore qu’Options n’est pas un neuvième espace, alors que le shell l’inclut.
- `.interface-design/system.md` décrit encore « Obsidian Copper », tandis que `tokens.css` est devenu « Signal Terminal ».
- `tokens.css` utilise le vert comme couleur de marque, alors que la direction validée réserve désormais le vert au positif.

Ces divergences doivent être traitées dans la phase Fondations avant toute refonte page par page.
