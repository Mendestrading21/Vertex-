# Vertex Visual System

## Sommaire
- Intention
- Palette
- Typographie
- Surfaces
- Grille et espacements
- Formes et bordures
- Densité
- Navigation
- Icônes
- Motion
- Responsive
- Anti-patterns

## Intention
Vertex doit évoquer un terminal d’investissement institutionnel moderne : sombre, précis, calme, rapide. Les références visuelles autorisent la densité, les cartes modulaires, les graphiques riches et les contrastes forts, mais pas le bruit décoratif.

## Palette sémantique
Toujours partir des tokens existants. Ne pas introduire une seconde palette locale.

### Rôles
- Canvas : presque noir, neutre.
- Surface 1 : premier niveau de carte.
- Surface 2 : carte active / sous-surface.
- Border : contraste faible mais visible.
- Text primary : blanc cassé, jamais blanc éclatant partout.
- Text secondary : gris froid.
- Brand : violet Vertex.
- Positive : vert émeraude.
- Negative : rouge corail.
- Warning : jaune.
- Technical : cyan.
- Neutral chart : gris.

### Discipline
Une couleur sémantique ne change jamais de sens selon la page. Le violet peut identifier la série principale ou la sélection, pas une hausse. Le vert signifie favorable/positif. Le rouge signifie défavorable/risque.

## Typographie
### Hiérarchie
- Page title : 28–32 px desktop, 24–28 mobile, 650–750.
- Section title : 16–18 px, 600–700.
- Card title : 13–15 px, 600.
- KPI : 26–38 px selon importance, tabular nums si disponible.
- Body : 13–14 px.
- Meta : 11–12 px.
- Table : 12–13 px.

### Règles
- Maximum trois tailles fortes sur un écran.
- Chiffres financiers alignés et faciles à scanner.
- Utiliser les majuscules avec parcimonie pour badges/labels courts uniquement.
- Éviter le tracking exagéré.

## Surfaces
### Carte standard
- Fond mat.
- Border 1 px faible contraste.
- Rayon cohérent 12–16 px.
- Padding 16–20 px desktop, 14–16 px mobile.
- Aucune ombre forte. Ombre seulement pour popover/modal/floating surfaces.

### Carte dominante
Peut utiliser une légère teinte violet/noir ou une bordure plus présente. Une seule carte dominante par zone.

### Sous-surface
Utiliser fond légèrement différent, pas une carte complète imbriquée si une séparation suffit.

## Grille
- Shell desktop : sidebar fixe + contenu flexible.
- Contenu max width cohérent ; ne pas étirer les cartes de lecture sur écrans ultra larges.
- Grille 12 colonnes implicite.
- Gaps : 12 / 16 / 20 / 24 ; éviter valeurs arbitraires.
- Une ligne de KPI ne dépasse pas 4 blocs de poids égal sauf cas justifié.
- Les gros graphiques prennent 2/3 ou toute la largeur ; éviter les graphiques minuscules illisibles.

## Densité
Vertex peut montrer beaucoup de données si :
1. la hiérarchie est claire ;
2. les titres sont courts ;
3. les contrôles sont regroupés ;
4. les métadonnées secondaires sont visuellement faibles ;
5. les détails sont progressifs.

## Formes
- Radius principal : 14 px environ.
- Pills réservées aux filtres, badges, timeframes et états.
- Boutons standard pas systématiquement pill.
- Inputs : 10–12 px de rayon.
- Ne pas mélanger radius 4, 8, 20, 32 sans logique.

## Navigation
### Sidebar
- Logo/wordmark simple.
- 8 espaces canoniques.
- Groupe principal + Système en pied possible.
- Icône + label ; état actif via surface/border/brand, pas glow.
- Collapse autorisé si labels restent accessibles.

### Topbar
- Recherche centrale ou gauche dominante.
- Command palette/shortcut visible discrètement.
- Statut de données/compte à droite.
- Maximum 3 icônes utilitaires visibles.

## Icônes
Une seule famille outline. Stroke uniforme. Pas d’illustrations décoratives dans les cartes analytiques.

Mapping recommandé :
- Aujourd’hui : spark/compass.
- Marchés : activity/chart.
- Opportunités : target/radar.
- Analyse : search-chart.
- Portefeuille : briefcase/pie.
- Options : layers/curve.
- Journal : notebook/history.
- Système : sliders/settings.

## Motion
- 120–220 ms pour hover/selection.
- Pas de bounce.
- Pas de parallax.
- Respect `prefers-reduced-motion`.
- Animations de graphique discrètes, désactivables.

## Responsive
### ≥ 1280
Sidebar + 2/3 colonnes de contenu.

### 768–1279
Sidebar compacte ou rail ; grilles 2 colonnes ; tableaux scrollables.

### < 768
Navigation mobile ; une colonne principale ; header réduit ; contrôles secondaires dans menu/drawer ; KPI prioritaires en premier ; graphiques 280–340 px de haut.

## Anti-patterns
- Dashboard rempli de cartes de même importance.
- Texte gris trop faible pour être lu.
- KPI sans unité/contexte.
- 6 couleurs de série sans besoin.
- Icônes multicolores façon crypto template.
- Gros gradient décoratif derrière chaque widget.
- Bordure/glow violets sur toutes les cartes.
- Tables qui forcent le zoom mobile.
