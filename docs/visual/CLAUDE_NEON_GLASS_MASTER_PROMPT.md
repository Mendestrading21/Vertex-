# Claude Master Prompt — Vertex Neon Glass

## Mission

Refondre visuellement Vertex en terminal financier premium, moderne, lisible et cohérent, avec un langage **Neon Glass Orange** appliqué à tous les widgets et à tous les graphiques utiles.

La référence visuelle finale est :

- fond noir profond légèrement bleuté ;
- cartes glass clairement séparées ;
- orange néon comme couleur identitaire principale ;
- surfaces chaudes, bordures cuivre, ombres très discrètes ;
- typographie moderne, large, nette et respirante ;
- graphiques plus compréhensibles, plus vivants et plus élégants ;
- sensation de terminal institutionnel premium, jamais casino.

## Branche obligatoire

`agent/vertex-neon-glass-graphs`

Ne jamais travailler sur `main`.
Ne jamais fusionner.
Ne jamais modifier les moteurs financiers pour des raisons esthétiques.
IBKR reste strictement READONLY.

## Palette officielle

- Orange néon principal : `#FF6D29`
- Cuivre sombre : `#453027`
- Noir surface : `#161316`
- Gris texte secondaire : `#BABABA`
- Blanc : `#FFFFFF`
- Canvas global recommandé : `#05070C`

Sémantique stricte :

- vert = gain, confirmation, état sain ;
- rouge = perte, risque, invalidation, erreur ;
- ambre = attente, prudence, alerte ;
- violet = options / volatilité uniquement lorsque pertinent ;
- orange = identité, sélection, navigation, interaction, point actif ;
- aucun bleu identitaire.

## Principes non négociables

1. Chaque carte doit être identifiable immédiatement.
2. Chaque widget doit répondre à une seule question.
3. Chaque graphique doit avoir une hiérarchie claire : question, conclusion, preuve.
4. Aucun graphique ne doit être décoratif.
5. Aucun glow permanent partout.
6. Le glow est réservé au live, au point actif, à la sélection et aux alertes.
7. Les cartes glass doivent rester lisibles : blur local, bordure fine, profondeur discrète.
8. Pas de gradients décoratifs sans fonction.
9. Les données manquantes, périmées, démo ou insuffisantes doivent rester honnêtes.
10. Mobile 390 px, tablette 768 px, desktop 1440/1920 sans débordement.

## Graph System V2

Tous les graphiques doivent utiliser le Chart Shell canonique avec :

- titre ;
- question ;
- conclusion ;
- période ;
- unité ;
- source ;
- fraîcheur ;
- légende ;
- aide ;
- résumé accessible ;
- loading ;
- empty ;
- stale ;
- error ;
- demo ;
- insufficient ;
- offline.

## Style des graphiques

### Courbes / area charts

- ligne principale orange néon ou sémantique selon le contexte ;
- area fill très discret ;
- grille faible contraste ;
- point actif visible ;
- tooltip glass ;
- labels directs lorsque possible ;
- aucune surcharge de légende.

### Chandeliers

- moteur canonique TradingView Lightweight Charts ;
- bougies intégrées au glass system ;
- entrée, invalidation, objectifs et événements clairement annotés ;
- volume secondaire et discret ;
- aucune couleur décorative.

### Jauges

- uniquement pour une métrique bornée ;
- semi-circulaire ou ring compact ;
- texte central dominant ;
- conclusion sous la valeur ;
- pas de jauge si un KPI suffit.

### Heatmaps

- saturation contrôlée ;
- texte toujours lisible ;
- échelle explicite ;
- période affichée ;
- conclusion sur les zones dominantes.

### Bar charts

- coins légèrement arrondis ;
- hiérarchie par intensité et non par arc-en-ciel ;
- valeurs directes ;
- animations courtes ;
- comparaison claire.

### Scatter / quadrants

- axes nommés ;
- quadrants interprétés ;
- labels essentiels ;
- point actif orange ;
- conclusion textuelle.

### Payoff options

- zone de perte rouge sombre ;
- zone favorable verte ;
- breakevens et spot visibles ;
- coût, perte max et gain max directement reliés au graphique ;
- distinction échéance / avant échéance.

### Donuts / allocation

- sobres ;
- anneau fin ;
- labels externes lisibles ;
- conclusion sur concentration ;
- pas de donut sans message.

### Timelines

- axe horizontal clair ;
- événements importants hiérarchisés ;
- orange pour le point actif ;
- rouge pour risque ;
- ambre pour attente ;
- texte compact mais lisible.

## Widgets premium à standardiser

- Hero Market Regime ;
- KPI Glass ;
- Market Pulse ;
- Opportunity Card ;
- Analysis Verdict Card ;
- Scenario Card ;
- Portfolio Health ;
- Position Card ;
- Options Verdict ;
- Greeks Card ;
- Catalyst Timeline ;
- System Health ;
- Journal Progress ;
- Live Status ;
- Risk Alert ;
- Data Quality Badge ;
- Chart Card V2.

## Typographie

Utiliser une typographie moderne et très lisible, proche de Neue Montreal / General Sans / Inter.

Hiérarchie :

- H1 : fort, large, respirant ;
- H2 : section ;
- H3 : carte ;
- nombres : tabular-nums, JetBrains Mono ou équivalent ;
- labels secondaires discrets mais lisibles ;
- aucune micro-typographie illisible.

## Motion

Autoriser seulement :

- reveal court ;
- skeleton vers contenu ;
- changement de période ;
- point actif ;
- hover léger ;
- pulse live bref ;
- drawer / modal.

Durée : 120–240 ms.
Respect strict de `prefers-reduced-motion`.

## Ordre de migration

1. Aujourd’hui
2. Marchés
3. Opportunités
4. Analyse
5. Portefeuille
6. Options
7. Journal
8. Système

Pour chaque espace :

- audit avant ;
- wireframe ;
- migration carte par carte ;
- migration graphe par graphe ;
- captures avant/après ;
- responsive 390/768/1440/1920 ;
- console 0 ;
- tests complets ;
- READONLY ;
- service worker bump si nécessaire ;
- rapport de validation dédié ;
- arrêt pour validation humaine.

## Périmètre immédiat

Reprendre **Marchés** car la première proposition n’est pas validée visuellement.

Objectif : produire une page Marchés beaucoup plus moderne, propre et premium, en appliquant entièrement ce document.

### Marchés doit contenir

- Hero régime du marché ;
- risque du jour ;
- participation / breadth ;
- secteurs ;
- macro ;
- cross-asset ;
- volatilité ;
- anomalies ;
- indices principaux ;
- conclusions textuelles.

### Marchés doit éviter

- grandes cartes vides ;
- jauges sans information ;
- labels UNKNOWN sans explication ;
- cartes toutes identiques ;
- bordures trop plates ;
- espaces morts ;
- widgets ternes ;
- graphiques génériques posés dans une boîte ;
- couleurs non cohérentes ;
- typographie faible ;
- densité mal organisée.

## Validation attendue pour Marchés

Créer :

`docs/refactor/validation/NEON-GLASS-02-MARKETS.md`

Le rapport doit inclure :

- structure avant/après ;
- graphiques avant/après ;
- widgets créés ;
- composants canoniques réutilisés ;
- captures desktop/tablette/mobile ;
- tests exacts ;
- résultats console ;
- résultats responsive ;
- service worker ;
- risques ;
- éléments différés.

## Interdictions

- pas de big-bang ;
- pas de nouveau moteur ;
- pas de modification de calcul pour l’esthétique ;
- pas de donnée inventée ;
- pas de nouvelle route métier ;
- pas de duplication ;
- pas de suppression sans preuve ;
- pas de merge main ;
- pas de tag ;
- pas de release.

## Critère de qualité final

Une capture de Vertex doit être immédiatement reconnaissable.

Le produit doit donner l’impression d’un terminal institutionnel premium, moderne, confortable, cohérent et vivant.

Chaque carte doit être belle, utile et compréhensible.
Chaque graphique doit conduire à une décision.
