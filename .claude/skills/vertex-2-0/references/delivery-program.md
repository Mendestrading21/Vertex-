# Programme de livraison visuelle Vertex 2.0

Chaque lot modifie uniquement la présentation. Les moteurs, calculs, données, endpoints, intégrations, stores et règles financières restent inchangés.

## Lot 0 — Baseline visuelle

Relever SHA/CI/PR. Inventorier toutes les routes et sous-vues existantes, leurs données consommées, actions, composants, styles inline, états et captures desktop/mobile. Vérifier chaque page dans le navigateur avant de dessiner sa cible.

Livrables : matrice page × fonction existante × bloc visuel × état × largeur ; captures avant ; liste des contradictions visuelles ; aucune modification runtime.

## Lot 1 — Source de vérité

Finaliser tokens, Geist/Geist Mono, palette, densité, surfaces, Decision Trace, iconographie, microcopy et page /design-system. Aligner .interface-design/system.md, règles Claude et documents actifs. Les aliases legacy restent tant que leurs consommateurs ne sont pas migrés.

## Lot 2 — Shell et navigation

Refondre sidebar groupée Piloter/Explorer/Gérer/Intelligence, topbar, recherche, calendrier, alertes, drawers, modales et mobile bar. Préserver routes, handlers, IDs DOM, clés et contrats existants.

## Lot 3 — Primitives

Consolider visuellement cartes, KPI, badges, boutons, tabs, filtres, formulaires, tables, tooltips, états et drawers. Faire converger les multiples familles de cartes/métriques sans déplacer leur logique.

## Lot 4 — Graphiques

Unifier uniquement thème, conteneurs, axes, tooltips, légendes, formats d'affichage, resize, destruction, fallbacks et accessibilité. Les séries, valeurs, calculs et sources ne changent pas.

## Lot 5 — Aujourd'hui

Réordonner les fonctions existantes en command center : décision, marché, risques, revues, calendrier, opportunités, portefeuille, options et brief IA. Aucun nouveau calcul.

## Lot 6 — Calendrier et Marchés

Créer la vue Calendrier seulement avec événements/endpoints déjà présents ; sinon composer les catégories disponibles et marquer les manques. Refaire les sous-vues Marchés avec une visualisation dominante et preuves secondaires.

## Lot 7 — Opportunités et Analyse

Réorganiser radar/tables/drawers et dossier ticker. Conserver scores, gates, verdicts, loaders et endpoints exactement. Ajouter clarté, sources, fraîcheur et liens existants.

## Lot 8 — Options

Refondre visuellement Vue d'ensemble, Chaîne, Volatilité, Scanner, Scénarios, Positions et Événements. Présenter les champs réellement fournis ; aucune Greek, IV, quote, score ou stratégie calculée dans l'UI.

## Lot 9 — Simulateur

Composer la page multi-actifs Actions/ETF/Options/Forex depuis les capacités de simulation existantes. Construire paramètres, scénarios, comparaison, risques, impact portefeuille et provenance. Aucun nouveau moteur, calcul de prix, prédiction, store ou action broker.

## Lot 10 — Portefeuille et Suivi

Réordonner Synthèse, Positions, Allocation, Options, Risque et Thèses. Créer la page visuelle Suivi en composant watchlist/tracking/journal existants ; ne pas créer de nouveau store ni état métier.

## Lot 11 — Performance et Vertex IA

Séparer visuellement les populations existantes. Refaire Journal, courbes, tables, Assistant, Comité, Décisions, Recherche et Mémoire sans modifier packet, prompt métier, moteur ou persistance.

## Lot 12 — Système

Clarifier Connexions, Données, Jobs, Préférences, Sécurité, Archives et Design System. Ne changer aucune connexion, job, secret, backup ou sync.

## Lot 13 — Responsive et accessibilité

Vérifier 390, 430, 768, 1024, 1280, 1440, 1600 et écran large ; clavier, zoom 200 %, touch, focus, reduced motion, contrastes, tableaux et graphiques. Corriger seulement la couche visuelle.

## Lot 14 — Nettoyage visuel

Après recherche des consommateurs, retirer CSS/classes/docs de design devenus sans usage. Ne supprimer aucun moteur, route, endpoint, fonction métier ou actif de données.

## Lot 15 — Acceptation

Comparer avant/après sur le même SHA fonctionnel ; exécuter les 150 contrôles de `audit-150.md`, tests complets, no-orders, healthz, client-log, console, modes live/delayed/stale/demo/offline/missing, service worker et rollback. PR brouillon ; aucune fusion automatique.

## Commande Claude

    /vertex-2-0 lot:0

Claude continue le premier lot visuel non terminé. Il implémente et vérifie page par page, sans ouvrir plusieurs lots dépendants simultanément et sans étendre le périmètre au backend.
