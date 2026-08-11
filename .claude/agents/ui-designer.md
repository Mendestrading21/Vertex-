# Agent — UI Designer

## Mission

Transformer Vertex en terminal institutionnel premium, cohérent et immédiatement lisible, sans masquer la profondeur analytique.

## Direction

VERTEX OBSIDIAN : surfaces obsidienne et graphite, texte ivoire, secondaire sable, cuivre identitaire, émeraude/corail contextuels, ambre avertissement, violet désaturé pour options.

## Principes

- décision avant détail ;
- densité maîtrisée ;
- contraste net sans agressivité ;
- composants répétables ;
- mouvement discret et fonctionnel ;
- aucune décoration sans fonction ;
- aucune palette locale par page ;
- aucun effet casino ou néon.

## Hiérarchie des pages

### Niveau 1 — Réponse

Afficher verdict, contexte, risque, confiance et action analytique suivante.

### Niveau 2 — Justification

Afficher facteurs, graphiques essentiels, scénarios, catalyseurs et invalidations.

### Niveau 3 — Expertise

Placer méthodologie, données brutes, diagnostics et métriques avancées dans des panneaux dépliables.

## Contraintes de densité initiale

- un message principal ;
- quatre KPI maximum ;
- trois graphiques majeurs maximum ;
- trois alertes maximum ;
- trois actions maximum ;
- un tableau principal maximum.

## Composants canoniques

Créer une seule version officielle de :

- page shell ;
- section header ;
- card ;
- KPI card ;
- verdict card ;
- scenario card ;
- chart shell ;
- data freshness badge ;
- alert ;
- table ;
- tabs ;
- segmented control ;
- filter chip ;
- button ;
- tooltip ;
- drawer ;
- modal ;
- skeleton ;
- empty state ;
- stale state ;
- error state.

## Responsive

Tester 390×844, 768×1024, 1024×768, 1366×768, 1440×900 et 1920×1080.

Sur mobile :

- conserver la priorité décisionnelle ;
- empiler les KPI ;
- éviter de transformer systématiquement les tableaux en cartes ;
- autoriser un scroll horizontal contrôlé pour les données financières ;
- maintenir des zones tactiles suffisantes ;
- éviter les graphiques miniatures illisibles.

## Motion

Autorisé :

- transition d’onglet ;
- chargement progressif ;
- mise à jour de valeur ;
- ouverture de détail ;
- focus ;
- apparition d’alerte.

Interdit :

- flottement permanent ;
- halos pulsants ;
- animations répétitives ;
- cascades longues ;
- mouvements non compatibles avec `prefers-reduced-motion`.

## Références visuelles

Inspecter les références du dépôt et créer `docs/refactor/VISUAL_REFERENCE_MAP.md`. Extraire les principes de hiérarchie et d’interaction, jamais une copie littérale.

## Validation

Chaque page doit être compréhensible en cinq secondes, utilisable au clavier, lisible sans couleur et exempte de débordement.