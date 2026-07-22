# Architecture d'information — baseline et cible V4

Vertex suit un strangler pattern. Le blueprint `vertex/app/routes/redesign.py`
sert un shell unique `vertex/ui/shell/__init__.py` et des pages sous
`vertex/ui/pages/`. `terminal.py` conserve encore des routes/API historiques.

## Baseline vérifiée

Le shell affiche huit espaces. `/markets` redirige vers les sections Marchés du
Briefing. Cette baseline doit continuer de fonctionner pendant les premiers lots.

## Cible V4

| # | Espace | Route | Question |
|---:|---|---|---|
| 1 | Briefing | `/` | Que faut-il comprendre et surveiller aujourd'hui ? |
| 2 | Marchés | `/markets` | Dans quel régime et environnement la stratégie opère-t-elle ? |
| 3 | Opportunités | `/opportunities` | Quels candidats méritent une analyse ? |
| 4 | Portefeuille | `/portfolio` | Que possède le portefeuille et quels risques porte-t-il ? |
| 5 | Analyse | `/analysis` et `/analysis/<sym>` | Ce dossier mérite-t-il du capital maintenant ? |
| 6 | Options | `/options` et `/options/<sym>` | Où se trouve la meilleure convexité ? |
| 7 | Performance | `/performance` | La méthode fonctionne-t-elle et est-elle bien exécutée ? |
| 8 | Intelligence | `/intelligence` | Comment Vertex raisonne-t-il et apprend-il ? |
| 9 | Système | `/system` | Les connexions et données sont-elles saines ? |

Marchés réutilise les vues, données, APIs et ancres déjà présentes ; sa séparation
ne justifie aucun nouveau moteur. Tracking, watchlist, journal, automatisations et
design system restent des sous-vues, pas des espaces supplémentaires.

## Navigation

`PRIMARY_NAV` devient l'unique registre. Les onglets restent des URLs partageables
avec `?view=`. Conserver breadcrumbs, contexte de retour, recherche globale,
palette de commande, statuts de connexion et accessibilité clavier.
