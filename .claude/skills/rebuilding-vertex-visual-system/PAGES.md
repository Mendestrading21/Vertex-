# Vertex Pages — master rebuild specification

## Sommaire
- Ordre de reconstruction
- Shell
- Aujourd’hui
- Marchés
- Opportunités
- Analyse
- Portefeuille
- Options
- Journal
- Système
- Passe finale

## Ordre de reconstruction
Toujours suivre cet ordre sauf bug bloquant : shell → Aujourd’hui → Marchés → Opportunités → Analyse → Portefeuille → Options → Journal → Système → passe finale.

L’objectif est d’éviter qu’une page reconstruite dépende de primitives encore instables.

## 0. Shell global
### Question
`Où suis-je, que puis-je chercher et quel est l’état des données ?`

### À construire
- Sidebar cohérente avec 8 espaces.
- Topbar simple.
- Recherche globale.
- Command palette.
- Compte/statut données.
- Collapse desktop.
- Mobile nav.
- Drawer/modal/toasts communs.

### À supprimer
- doubles navigations ;
- actions répétées dans chaque page ;
- icônes de familles différentes ;
- topbar surchargée.

## 1. Aujourd’hui
### Question
`Qu’est-ce qui mérite mon attention maintenant ?`

### Hiérarchie cible
1. Signal du jour.
2. Régime marché + risque global.
3. Top 3–5 opportunités.
4. Catalyseurs des 90 jours / très proches.
5. Portefeuille : changements et alertes.
6. Brief éditorial court.

### Widgets privilégiés
- regime aura ;
- catalyst runway ;
- décision/grade cards ;
- alert strip ;
- mini market pulse.

### À éviter
Copier toute la page Marchés. Aujourd’hui est un résumé décisionnel.

## 2. Marchés
### Question
`Quel environnement récompense ou pénalise la stratégie ?`

### Vues
- Vue d’ensemble.
- Macro.
- Secteurs / leadership.
- Breadth.
- Volatilité.

### Structure
1. Régime.
2. Indices/rates/FX/commodities essentiels.
3. Leadership secteur/facteurs.
4. Breadth.
5. Volatilité / stress.
6. Calendrier macro pertinent.

### Graphiques
Courbes, barres de ranking, heatmap, yield/vol comparison. Aucun graphique sans question/conclusion.

## 3. Opportunités
### Question
`Quels dossiers ont la meilleure asymétrie maintenant ?`

### Structure
1. Filtres principaux.
2. Top S+/S.
3. Tableau/scanner complet.
4. Catalyseurs.
5. Anomalies / nouveaux signaux.

### Carte opportunité
Ticker, grade, score, verdict, risque max., probable, exceptionnel, catalyseur, invalidation, liquidité si option.

### Interactions
Analyser, comparer, suivre, alerte, voir options. Aucun achat.

## 4. Analyse
### Question
`La thèse mérite-t-elle du capital et à quel risque ?`

### Structure cible
1. Identity strip : ticker, prix, variation, grade, score, fraîcheur.
2. Verdict en une phrase.
3. Asymétrie : pessimiste / probable / exceptionnel.
4. Price chart TradingView-grade.
5. Catalyseurs.
6. Fondamentaux / qualité.
7. Technique.
8. Positionnement / institutions si disponible.
9. Risques / invalidation.
10. Options adaptées.
11. Notes / suivi / journal.

### Règle
La page ne doit pas demander de lire 20 cartes avant de connaître le verdict et le risque.

## 5. Portefeuille
### Question
`Où suis-je exposé, qu’est-ce qui menace le capital et que faut-il revoir ?`

### Structure
1. Valeur / P&L / cash / drawdown.
2. Risque global et concentration.
3. Positions prioritaires à revoir.
4. Allocation/exposition secteurs/facteurs.
5. Table positions.
6. Watchlist / candidats remplacement.
7. Alertes et prochains catalyseurs.

### Règle
Le portefeuille doit mettre les risques avant les statistiques décoratives.

## 6. Options
### Question
`Où la convexité justifie-t-elle le coût et le risque ?`

### Structure
1. Environnement options : IV, term structure, liquidité.
2. Candidats LEAPS / structures observées.
3. Filtres delta/DTE/OI/spread.
4. Scénarios payoff.
5. Theta / IV sensitivity.
6. Risques événementiels.
7. Watchlist options.

### Profil de lecture
Mettre en avant delta, DTE, spread, OI, break-even, coût, perte max., scénario probable/exceptionnel.

## 7. Journal
### Question
`Qu’est-ce qui améliore ou dégrade la qualité des décisions ?`

### Structure
1. Track record séparant signaux et positions réelles.
2. Décisions récentes.
3. Résultats par grade / setup / horizon.
4. Erreurs répétées.
5. Learnings.
6. Notes et historique.

### Visualisation
Equity curve, drawdown, win/loss par bucket, distribution de résultats, calibration score→résultat.

## 8. Système
### Question
`Puis-je faire confiance aux données et à l’état du terminal ?`

### Structure
1. Connexions : IBKR, sources.
2. Santé des données.
3. Fraîcheur / dernières mises à jour.
4. Paramètres UI.
5. Archive / logs utiles.
6. Mode démo/offline.

### Règle
Page technique mais lisible. L’utilisateur doit comprendre le problème sans connaître l’implémentation.

## Passe finale
Après les 8 pages :
- cohérence des titres ;
- cohérence des icônes ;
- mêmes composants pour mêmes usages ;
- palettes charts synchronisées ;
- responsive complet ;
- accessibilité ;
- command palette ;
- handlers ;
- zéro overflow inattendu ;
- zéro console error ;
- PWA cache ;
- suppression CSS/JS legacy devenu inutile.
