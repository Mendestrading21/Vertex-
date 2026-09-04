# Vertex — Catalogue des widgets (V3)

Chaque widget : source de données réelle, états
LOADING/READY/EMPTY/STALE/ERROR, UpdateIndicator, actions contextuelles.
Aucun chiffre inventé — donnée absente = « — »/« n/d » + explication.

## Briefing (`/`)

| Widget | Grille | Source |
|---|---|---|
| Brief Vertex (hero, 8-12 lignes + « ce qui a changé » + preuves) | 8 | `/api/briefing/editorial` (déterministe, étiqueté) |
| Régime de marché (+ ajustements risque) | 4 | `/api/market/regime` |
| KPI indices ×6 (valeur, variation, sparkline, source, mode) | 2 ch. | `/scan` indices |
| Cross-asset regroupé (DXY/pétrole/or/BTC) | 2 | `/scan` (n/d honnête) |
| Marché US série de référence | 8 | `/scan` detail.SPY |
| Breadth | 4 | `/scan` market |
| Opportunités actions / options | 6+6 | `/api/command` |
| Rotation sectorielle (drill-down) | 7 | `/scan` sectors |
| Alertes prioritaires (armée/déclenchée) | 5 | vxAlerts + `/api/alerts/status` |
| Portefeuille résumé (P&L live si marques) | 7 | VXEntities + `/api/pos-quotes` |
| Calendrier (macro + earnings) | 5 | `/cal-feed` |
| Personnalisation (masquer blocs, densité) | — | `vxDashboardLayout` |

## Marchés (`/markets`)

Régime · Leadership sectoriel · Risque du jour · bandeau indices ·
S&P 500 série de référence · **multi-indices rebasés 0 %** · KPI macro ·
calendrier macro · rotation sectorielle · **heatmap performance/momentum
par secteur (cliquable)** · leaders par secteur · breadth · donut des
verdicts du scan · VIX + bande.

## Opportunités (`/opportunities`)

Radar scatter (couleur=décision, taille=intensité, bordure=qualité données)
+ **dossier de sélection** (scores, R:R, setup, secteur + 7 actions
rapides) · table actions filtrable (chips décision/setup/agressivité,
compteur de filtres) · board options + **simulateur** (payoff, matrice
spot×temps, theta, sensibilité IV — moteur `scenario_pricer`) · anomalies ·
calendrier.

## Portefeuille (`/portfolio`)

**Synthèse** (valeur — étiquetée « au coût » sans marques —, P&L latent,
équipe X/10, options X/3) · Équipe par rôles (Offensive/Noyau/Défense-
gardien) + **Options tactiques HORS équipe (jamais gardien)** · donut
répartition · places & règle du remplacement · **contributeurs/détracteurs**
(si marques) · table positions (marques live, clôture déclarative → journal
auto) · risque réel (garde-fous, concentration, Greeks broker, stress
tests) · watchlist (statuts) + suivis + favoris.

## Analyse (`/analysis/<sym>`)

Héro sticky (cours, décision, 5 scores, actions) · **rail sticky**
(décision finale + audit trail, plan & niveaux, risques identifiés) ·
graphique principal (niveaux + earnings, timeframes, alerte au double-clic)
· fondamental · catalyseurs · technique · sentiment · anomalies · signaux
TradingView · scénarios Bull/Base/Bear · options du titre · compatibilité
portefeuille · historique journal.

## Performance (`/performance`)

KPI déclarés (win rate, expectancy, profit factor…) · courbe d'équité ·
drawdown · **heatmap P&L moyen par mois** · **distribution des rendements
par trade** · journal filtrable · track record moteur (séparé des trades
réels) · enseignements.

## Intelligence (`/intelligence`)

Analyste (exemples de questions cliquables, tickers récents/favoris,
double décision moteur+stack) · comité (matrice, filtres, détail) ·
constitution & versions · recherche (expérimentations) · mémoire (thèses,
leçons, statuts OBSERVED→CONFIRMED).

## Système (`/system`)

Connexions métier d'abord (IBKR/TradingView/Claude/sync/stockage : statut,
dernière réussite, erreur, impact, action recommandée) · moteurs
différenciés **prêt / chargé-sans-données / KO** · endpoints techniques en
drawer · qualité des données par domaine · réglages (densité, sidebar,
notifications) · export/import desk · vault.

## Menu widget (⋯) et interactions

Toutes les occurrences de ticker portent le menu universel (12 actions §31).
Widgets interactifs : changer le timeframe, filtrer, trier, drill-down
secteur, créer une alerte depuis un niveau, ouvrir les détails en drawer,
exporter (desk/vault), actualiser (refresh manager).
