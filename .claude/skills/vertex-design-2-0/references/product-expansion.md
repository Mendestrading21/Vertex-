# Extension produit et nouvelles surfaces

## Principe

Une refonte maximale ne signifie pas tout afficher simultanément. Vertex doit donner accès à toute la profondeur utile au moyen d'un premier écran décisionnel, de sous-vues cohérentes et de détails progressifs. Réutiliser les données et moteurs existants ; créer un endpoint de présentation seulement si nécessaire pour exposer une sortie déjà canonique.

## Centre Options complet

### Navigation

`Vue d'ensemble · Chaîne · Volatilité · Scénarios · Positions · Événements`

### Vue Chaîne

Créer une surface professionnelle dédiée, accessible depuis Options et chaque fiche ticker. Elle comprend :

- symbole, sous-jacent, heure/source du mark, état live/delayed/stale et sélection d'échéance ;
- filtres DTE, moneyness, CALL/PUT, delta, volume, open interest, spread, IV et liquidité ;
- disposition CALL à gauche / strike central / PUT à droite sur desktop ;
- mode table empilée sur tablette, sans écraser les colonnes ;
- strikes proches de l'ATM mis en évidence de façon neutre ;
- headers et colonnes clés sticky ; densité réglable ; colonnes configurables ;
- recherche et export non destructif si déjà autorisé par le produit.

Colonnes disponibles selon les données réellement reçues : bid, ask, mid, last, spread absolu/%, volume, open interest, IV, delta, gamma, theta, vega, valeur intrinsèque/extrinsèque, breakeven, DTE, multiplicateur, score de liquidité, qualité et fraîcheur. Une colonne absente n'est ni estimée ni remplacée par zéro.

Le clic sur un contrat ouvre un drawer : résumé, qualité du mark, spread, Greeks, IV, événement dans l'échéance, payoff, sensibilité spot/temps/IV, risques, limites et provenance. Aucun bouton d'achat/vente et aucun ticket broker.

### Volatilité

- term structure par échéance ;
- smile/skew par strike ;
- open interest et volume par strike ;
- IV vs historique/percentile uniquement si fournis ;
- expected move et événement uniquement depuis les moteurs ;
- conclusion textuelle courte et limites.

### Scénarios

- payoff à expiration ;
- matrice spot × temps ;
- theta decay ;
- sensibilité IV ;
- comparaison de contrats ;
- composition multi-jambes strictement comme simulation analytique, sans préparation d'ordre.

### Positions Options

Livre des options détenues : sous-jacent, contrat, échéance, quantité, coût total, mark et source, P&L, Greeks, breakeven, gain/perte max lorsque défini, événement, concentration et fraîcheur. Conserver la distinction prix par action / multiplicateur / coût total.

## Portefeuille avancé

### Synthèse

- valeur, cash, exposition nette/brute, P&L jour/latent/réalisé selon disponibilité ;
- allocation par actif, secteur, devise, pays, thème et rôle ;
- concentration, corrélations, bêta, drawdown, liquidité et risque options ;
- principaux contributeurs/détracteurs ;
- alertes et décisions à revoir ;
- fraîcheur et réconciliation IBKR visibles.

### Positions

Table configurable : ticker, nom, type, quantité, prix d'entrée, mark, valeur, poids, P&L, performance, thèse, score, risque, stop/invalidation, cible, prochaine revue, source et fraîcheur. Drawer par position : graphique, historique, thèse, catalyseurs, scénarios, portefeuille, journal et décisions passées.

### Risque

- concentration HHI et top positions ;
- exposition secteur/devise/facteur ;
- corrélations et diversification ;
- stress tests et scénarios ;
- Greeks agrégés pour options ;
- risque événementiel et calendrier ;
- limites réelles, breaches et plans de surveillance.

### Watchlist et suivi

Transformer la watchlist en système de suivi : statut, thèse, pourquoi maintenant, catalyseur, invalidation, prix/zone observée, horizon, priorité, prochaine revue, événements et historique des changements. Distinguer « à étudier », « en attente », « prête », « invalidée » et « archivée » sans confondre cela avec un verdict moteur.

Créer un **Centre de suivi** dans Performance : idées actives, positions, options, thèses à revoir, événements proches, données stale et décisions en retard. Tracking hypothétique reste séparé des trades réels et du portefeuille IBKR.

## Tables professionnelles

Toutes les grandes tables utilisent la même infrastructure :

- colonnes configurables et ordre mémorisé ;
- tri multi-critères si utile ; filtres combinables ; recherche ;
- vues enregistrées localement sans nouvelle clé sync non déclarée ;
- densité compacte/confortable ; headers sticky ; pagination ou virtualisation ;
- sélection neutre, navigation clavier, ligne ouvrant un drawer ;
- export uniquement des données réellement visibles et autorisées ;
- états loading/empty/partial/stale/error ;
- formatters centralisés pour devise, prix, %, dates, DTE et Greeks.

Tables prioritaires : opportunités actions, chaîne d'options, positions, watchlist, journal, tracking, événements, alertes, jobs système et décisions/mémoire.

## Nouvelles routes secondaires possibles

Créer seulement après vérification de l'absence d'une route canonique équivalente :

- chaîne détaillée d'un symbole ;
- détail d'une position ;
- détail d'une thèse/watchlist ;
- détail d'un suivi hypothétique ;
- détail auditable d'une décision ;
- calendrier transversal filtré par portefeuille/watchlist.

Ces routes ne deviennent pas automatiquement des entrées de sidebar. Elles sont atteintes depuis leur espace propriétaire et conservent breadcrumb, retour et contexte.

## États et données manquantes

Une interface complète doit également être excellente lorsqu'IBKR est déconnecté ou qu'une chaîne est partielle. Afficher les dimensions disponibles, les colonnes manquantes, la cause, l'âge, la source et l'action sûre possible. Ne jamais remplir un tableau avec des exemples présentés comme réels.

