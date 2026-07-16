# VERTEX — Plan directeur complet de refonte « Black Glass Institutional »

## 0. Contexte réel du dépôt

Vertex est un terminal d’analyse de trading local en Python/Flask, démarré par `terminal.py` sur le port 5002. Il lit IBKR en mode `readonly=True`, utilise un shell commun, des pages Python qui assemblent HTML/JS, Chart.js, TradingView Lightweight Charts, des moteurs Python et un stockage utilisateur localStorage synchronisé vers le desk.

La refonte demandée n’est pas une migration de framework. Elle doit exploiter l’architecture existante et consolider les composants déjà présents.

### Sources principales du design actuel

- `vertex/ui/shell/__init__.py`
- `vertex/static/vertex/css/tokens.css`
- `vertex/static/vertex/css/base.css`
- `vertex/static/vertex/css/layout.css`
- `vertex/static/vertex/css/components.css`
- `vertex/static/vertex/css/buttons.css`
- `vertex/static/vertex/css/charts.css`
- `vertex/static/vertex/css/responsive.css`
- `vertex/static/vertex/js/charts/`
- `.interface-design/system.md`

### Conflit à résoudre en premier

Le dépôt porte plusieurs identités successives :

1. documentation « Obsidian Copper » ;
2. tokens « Signal Green » ;
3. direction utilisateur validée « noir + verre gris transparent ».

La nouvelle source de vérité doit devenir « Black Glass Institutional ». La marque et la sélection passent en argent/blanc/graphite. Le vert redevient exclusivement sémantique positif.

---

# 1. Architecture cible

## 1.1 Shell

Conserver le shell actuel, mais le normaliser :

- sidebar matte black ;
- topbar noire et légèrement transparente ;
- navigation active en verre gris argenté ;
- recherche globale plus lisible ;
- statut marché discret ;
- actions secondaires ghost ;
- bouton principal neutre, sauf action sémantique ;
- drawers, modales, palette et toasts sur le même système de verre.

## 1.2 Système de surfaces

Créer les classes :

- `.vx-glass-subtle`
- `.vx-glass-card`
- `.vx-glass-elevated`
- `.vx-glass-interactive`
- `.vx-glass-selected`
- `.vx-glass-critical`

Éviter les styles inline pour les surfaces, espacements, couleurs et hauteurs répétées.

## 1.3 Primitives

Normaliser :

- cartes ;
- KPI ;
- badges ;
- statuts ;
- tabs ;
- segmented controls ;
- champs ;
- tables ;
- toolbars ;
- drawers ;
- modales ;
- empty states ;
- skeletons ;
- freshness badges ;
- data provenance ;
- chart cards.

## 1.4 Grille

- 12 colonnes ;
- largeur max adaptée aux écrans 1440–1920 ;
- mode Confort par défaut ;
- densité pilotée par attribut racine ;
- points de rupture explicites ;
- aucune carte trop haute sans contenu ;
- les pages doivent utiliser toute la largeur sans perdre la lecture.

---

# 2. Système global des graphiques

## 2.1 Refactor transversal

Avant les pages, auditer tous les modules de `vertex/static/vertex/js/charts/`.

Créer une couche de thème unique :

- couleurs depuis CSS variables ;
- tooltip commun ;
- axes communs ;
- formatters communs ;
- registry de destruction ;
- resize observer ;
- mode reduced motion ;
- légendes et titres communs ;
- états communs.

## 2.2 Palette graphique

- série principale : argent clair ;
- série secondaire : gris moyen ;
- benchmark : gris chaud ;
- positif : vert ;
- négatif : rouge ;
- seuil/prudence : orange ;
- options : motifs/nuances neutres d’abord.

## 2.3 Refus des graphiques décoratifs

Chaque graphique doit contenir :

- une question ;
- une conclusion ;
- une source ;
- un timestamp ;
- un état de fraîcheur ;
- une limite méthodologique lorsqu’elle est importante.

---

# 3. Plan par page

## 3.1 Briefing / Dashboard — `/`

### État actuel

`vertex/ui/pages/briefing.py` contient un long cockpit : brief, régime, market strip, pouls, graphiques marché/breadth, top/flop, opportunités, rotation, alertes, portefeuille et calendrier.

### Nouvelle hiérarchie

#### Première hauteur d’écran

1. titre et question du jour ;
2. cinq KPI marché compacts ;
3. grande carte « Régime de marché » ;
4. grande table « Opportunités actives » ;
5. trois cartes : portefeuille, flux/options, performance.

#### Deuxième niveau

6. Brief Vertex ;
7. Pouls du marché ;
8. breadth/participation ;
9. top/flop ;
10. rotation et alertes ;
11. calendrier.

### Composants

- `MarketKpiStrip`
- `MarketRegimePanel`
- `ActiveOpportunitiesTable`
- `PortfolioSnapshot`
- `OptionsFlowSnapshot`
- `PerformanceSnapshot`
- `BriefPanel`
- `MarketPulsePanel`

### Graphiques

- sparklines neutres avec couleur uniquement sur variation ;
- jauge de régime avec zones gris/orange/rouge/vert ;
- portefeuille : ligne neutre, delta vert/rouge ;
- performance : courbe argent + benchmark gris ;
- options flow : donut sobre, légende lisible ;
- breadth : historique + moyenne et seuils.

### Acceptation

- décision principale visible sans scroll sur 1440×900 ;
- personnalisation conserve les mêmes clés ;
- aucune fausse actualité ou donnée.

---

## 3.2 Marchés — `/markets`

Fichier : `vertex/ui/pages/markets_page.py`.

### Vue overview

- régime ;
- leadership sectoriel ;
- risque du jour ;
- strip indices/cross-asset ;
- S&P 500 dominant ;
- comparaison multi-indices ;
- top/flop.

### Vue macro

- appétit risk-on/risk-off ;
- KPIs régime/VIX/MM50/MM200 ;
- courbe des taux ;
- calendrier macro.

La hausse des taux et du VIX ne doit jamais être automatiquement colorée en vert.

### Vue sectors

- classement sectoriel ;
- performance ;
- heatmap ;
- rotation quadrant ;
- treemap poids × performance.

Éviter les visualisations redondantes et prévoir une sélection croisée des secteurs.

### Vue breadth

- participation globale ;
- MM50/MM200 ;
- tendance historique ;
- distribution des scores ;
- internals ;
- waterfall santé.

Expliciter que l’univers est partiel.

### Vue volatility

- VIX niveau et régime ;
- rail calme ↔ stress ;
- contexte participation/régime ;
- historique VIX si disponible ;
- lien vers IV par symbole.

Ne pas inventer de term structure marché.

---

## 3.3 Opportunités — `/opportunities`

Fichier : `vertex/ui/pages/opportunities_page.py`.

### Vue radar

- top opportunités ;
- entonnoir ;
- scatter qualité × timing ;
- décomposition des sous-scores ;
- détail au clic dans un drawer.

### Vue stocks

- table principale ;
- colonnes configurables ;
- score, verdict, R:R, secteur, fraîcheur ;
- mini-sparkline ;
- quick actions non destructives.

### Vue options

- meilleurs contrats ;
- qualité ;
- DTE ;
- IV ;
- prime ;
- liquidité ;
- risque événement ;
- lien vers Options Intelligence.

### Vue anomalies

- type ;
- intensité ;
- récence ;
- source ;
- impact potentiel ;
- filtres ticker/secteur.

### Vue calendar

- earnings et événements ;
- vue chronologique ;
- proximité des positions/watchlist ;
- état des données.

---

## 3.4 Portefeuille — `/portfolio`

Fichier : `vertex/ui/pages/portfolio_page.py`.

### Synthèse commune

- valeur ;
- P&L latent ;
- exposition nette/brute ;
- cash ;
- concentration ;
- risque ;
- fraîcheur IBKR.

### Vue team

- allocation treemap ;
- rôles Offensive/Noyau/Défense/Options ;
- contributeurs P&L ;
- places disponibles ;
- règles de composition.

### Vue positions

- table détaillée ;
- P&L ;
- poids ;
- entrée ;
- stop ;
- thèse ;
- risque ;
- fraîcheur ;
- filtres ;
- drawer de détail.

### Vue options

- capital engagé ;
- CALL/PUT ;
- échéance ;
- payoff combiné par sous-jacent ;
- gain/perte max ;
- breakevens ;
- Greeks ;
- données indisponibles clairement signalées.

### Vue risk

- HHI/concentration ;
- exposition sectorielle ;
- stress tests ;
- bêta ;
- drawdown ;
- Greeks agrégés ;
- alertes de concentration.

### Vue watchlist

- catégories ;
- priorité ;
- thèse ;
- déclencheurs ;
- invalidation ;
- statut.

### Règles critiques

- `t.cost` reste un coût total ;
- les marques options restent par action avant multiplication ;
- positions déclarées et IBKR restent distinguées ;
- aucun P&L inventé hors ligne.

---

## 3.5 Analyse — `/analysis` et fiche ticker

Fichier : `vertex/ui/pages/analysis_page.py`.

### Index

- recherche ;
- récents ;
- favoris ;
- accès rapide ;
- explication courte des dimensions.

### Fiche canonique

1. hero décisionnel ;
2. graphique dominant ;
3. rail décision/plan/risques ;
4. thèse ;
5. scorecard dimensions ;
6. fondamental ;
7. catalyseurs ;
8. technique ;
9. sentiment ;
10. anomalies/TradingView ;
11. scénarios ;
12. options ;
13. compatibilité portefeuille ;
14. historique.

### Graphique principal

Conserver Lightweight Charts avec chandeliers, volume, MM20/50/200, entrée/stop/TP/résistance, crosshair, zoom, timeframe, source et fallback Chart.js.

### Améliorations

- supprimer les styles inline répétés ;
- éviter la duplication non justifiée de la décision ;
- scorecard compacte ;
- sticky rail stable ;
- navigation ancrée ;
- sections longues repliables ;
- IA séparée des verdicts déterministes ;
- scénarios conditionnels, jamais prédictions certaines.

---

## 3.6 Options — `/options`

Fichier : `vertex/ui/pages/options_intel_page.py`.

### Correction préalable

Mettre à jour les docstrings/commentaires obsolètes : Options est un espace principal dans `PRIMARY_NAV`.

### Vue overview

- environnement options ;
- CALL/PUT ;
- qualité moyenne ;
- liquidité ;
- IV ;
- événement ;
- meilleurs contrats.

### Vue volatility

- term structure ;
- smile/skew ;
- OI par strike ;
- IV vs historique si fourni ;
- lecture cher/neutre/bon marché uniquement depuis le moteur.

### Vue radar

- table/radar des contrats ;
- filtres DTE, type, liquidité, score ;
- conviction bars ;
- détail en drawer.

### Vue scenarios

- heatmap spot × temps ;
- theta decay ;
- IV sensitivity ;
- payoff ;
- multi-jambes ;
- PoP ;
- gain/perte max ;
- breakevens ;
- Greeks, Vanna, Vomma.

### Vue events

- résultats ;
- événement dans l’échéance ;
- expected move ;
- couverture ;
- risque gap ;
- timeline.

### Règles

- aucune action d’ordre ;
- premiums et multiplicateurs vérifiés ;
- données manquantes refusées honnêtement ;
- violet retiré comme accent global ;
- distinguer CALL/PUT par label, forme et motif, pas uniquement par couleur.

---

## 3.7 Performance — `/performance`

Fichier : `vertex/ui/pages/performance_page.py`.

### Vue overview

- progression avant le minimum de trades ;
- KPI une fois seuil atteint ;
- equity curve ;
- benchmark ;
- drawdown ;
- rendement mensuel ;
- distribution ;
- période.

### Vue journal

- table de trades ;
- filtres ticker/setup/régime/date ;
- création/édition ;
- erreurs déclarées ;
- MAE/MFE si réels ;
- lien avec une thèse.

### Vue track-record

Séparer visuellement les signaux théoriques moteur et les trades réels déclarés. Ne jamais mélanger les deux séries ou KPI.

### Vue learnings

- leçons ;
- erreurs récurrentes ;
- setups ;
- régime ;
- règles proposées ;
- lien vers Mémoire.

### Graphiques

- equity argent ;
- benchmark gris ;
- drawdown rouge sous zéro ;
- monthly heatmap ;
- distribution ;
- performance par verdict/setup.

---

## 3.8 Intelligence — `/intelligence`

Fichier : `vertex/ui/pages/intelligence_page.py`.

### Analyst

- formulaire compact ;
- verdict déterministe ;
- explication IA ;
- scorecard ;
- audit trail ;
- provenance.

### Committee

- convergence ;
- répartition des verdicts ;
- matrice ;
- filtres ;
- désaccords moteurs ;
- détails au clic.

### Strategy

- constitution ;
- hard gates ;
- options autorisées ;
- versions ;
- changements ;
- confirmation humaine.

### Impacts

- flux événements ;
- chaîne d’impact ;
- confiance ;
- cible ;
- distinction corrélation/causalité.

### Research

- pipeline IDEA → APPROVED ;
- résultats OOS ;
- PSR/DSR/PBO ;
- statut ;
- aucune règle active sans confirmation.

### Memory

- thèses ;
- notes ;
- règles observed/proposed/confirmed ;
- recherche ;
- versioning ;
- provenance.

La frontière moteurs déterministes / IA explicative / mémoire / recherche / décision humaine doit être immédiatement visible.

---

## 3.9 Système — `/system`

Fichier : `vertex/ui/pages/system_page.py`.

### Connections

- santé moteurs ;
- IBKR ;
- TradingView ;
- Claude ;
- sync ;
- stockage ;
- preuve de connexion ;
- READONLY.

### Data

- qualité ;
- fraîcheur par domaine ;
- dernier scan ;
- titres dégradés ;
- sources.

### Automations

- jobs ;
- priorité ;
- statut ;
- dernier/prochain run ;
- erreur ;
- startup report ;
- configuration sans secret.

### Settings

- densité ;
- sidebar ;
- notifications ;
- export/import ;
- langue ;
- préférences ;
- sécurité.

### Archive

- coffre ;
- recherche ;
- tags ;
- export ;
- création ;
- sync.

Conserver `/design-system` et le mettre à jour pour servir de page de QA vivante.

---

## 3.10 Tracking — `/tracking`

- KPI suivis actifs/résolus ;
- performance vs SPY ;
- alpha ;
- statut ;
- verdict initial ;
- date ;
- horizon ;
- barres signées ;
- détail ;
- archive ;
- rappels « hypothétique ».

---

# 4. Plan technique par phases

## Phase 0 — Baseline

- branche dédiée ;
- captures de toutes les pages ;
- inventaire routes et graphiques ;
- tests de base ;
- console ;
- performance ;
- IBKR connecté/hors ligne ;
- démo/partiel.

## Phase 1 — Source de vérité design

- `tokens.css` ;
- `.interface-design/system.md` ;
- `/design-system` ;
- tests palette ;
- tokens glass ;
- marque neutral silver ;
- alias legacy ;
- suppression des hex inline.

## Phase 2 — Shell

- sidebar ;
- topbar ;
- recherche ;
- status ;
- drawers ;
- modale ;
- palette ;
- mobile bar ;
- correction huit/neuf espaces.

## Phase 3 — Primitives

- cartes ; KPI ; boutons ; tabs ; tables ; forms ; states ; badges ; fraîcheur ; provenance.

## Phase 4 — Charts core

- thème ; card wrapper ; tooltips ; axes ; registry ; resize ; fallbacks ; couleurs ; tests.

## Phases 5–14 — Pages

1. Briefing
2. Marchés
3. Opportunités
4. Portefeuille
5. Analyse
6. Options
7. Performance
8. Intelligence
9. Système
10. Tracking et routes secondaires

## Phase 15 — Responsive et accessibilité

- 1920, 1440, 1280, 1024, tablette ;
- clavier ; focus ; reduced motion ; contrastes.

## Phase 16 — QA et release

- tests complets ;
- navigateur ;
- console ;
- screenshots ;
- données réelles ;
- IBKR hors ligne ;
- démo ;
- stale ;
- PWA/service worker ;
- documentation ;
- rollback.

---

# 5. Conditions de sortie

La refonte n’est terminée que lorsque :

- toutes les pages utilisent les mêmes surfaces ;
- tous les graphiques utilisent le même thème ;
- aucune sélection non sémantique n’est verte ;
- aucun bleu n’est dominant ;
- tous les états de données sont honnêtes ;
- les pages critiques sont vérifiées avec et sans IBKR ;
- les tests passent ;
- la console reste vide ;
- le service worker est à jour ;
- la page Design System reflète le produit réel.
