# Architecture de l'information Vertex 2.0

## Navigation cible

La navigation doit rester stable, courte et orientée travail. Ne pas exposer chaque sous-vue comme une destination principale.

### Espaces principaux

1. **Aujourd'hui** — briefing, régime, risques et priorités de la séance.
2. **Marchés** — environnement macro, indices, secteurs, breadth et volatilité.
3. **Opportunités** — radar actions/options, anomalies et calendrier.
4. **Analyse** — recherche et dossier canonique d'un actif.
5. **Portefeuille** — positions, exposition, risque, watchlist et options détenues.
6. **Options** — volatilité, contrats, scénarios et événements.
7. **Performance** — résultats, journal de trades, tracking et apprentissages.
8. **Intelligence** — raisonnement déterministe, comité, recherche et mémoire.

### Utilitaires persistants

- **Journal** peut rester un raccourci direct, mais sa donnée appartient à Performance.
- **Système** reste épinglé en bas de la sidebar.
- **Design System** est une route interne de QA, absente de la navigation utilisateur normale.
- **Tracking** devient une sous-vue de Performance avec redirection de l'ancienne route.

Préserver les routes existantes au moyen de redirects ou d'aliases pendant la migration. Ne jamais casser un favori, un lien interne ou une clé de vue sans plan.

## Structure commune d'une page

1. En-tête : titre français, question métier, fraîcheur globale et actions sûres.
2. Rail de contexte : filtres, période, univers, source ou statut.
3. Zone décisionnelle : 1 hero ou 1 tableau principal, pas deux concurrents.
4. Preuves : KPI et visualisations qui expliquent la décision.
5. Détails : tables, méthodes et historique sous le premier écran.
6. États et provenance : visibles au bon niveau, jamais cachés dans un tooltip unique.

## Règles de hiérarchie

- Un seul point focal par hauteur d'écran.
- Maximum quatre KPI égaux avant regroupement ou défilement raisonné.
- Une page ne répète pas le même verdict dans trois cartes.
- Une sous-navigation apparaît seulement si les vues répondent à des questions différentes.
- Les actions globales restent dans le header ; les actions d'un objet restent près de cet objet.
- Les filtres persistants conservent leur état sans devenir une deuxième barre de navigation.
- Les informations secondaires passent dans un drawer, une section repliable ou une sous-vue ; elles ne disparaissent pas.

## Responsive

- Desktop large : sidebar complète et grille 12 colonnes.
- Laptop : grille adaptative, aucune carte écrasée pour conserver artificiellement une ligne.
- Tablette : sidebar réduite/drawer ; tableaux avec colonnes prioritaires et détail accessible.
- Mobile : mode de consultation sûr, ordre de contenu par décision ; aucun tableau illisible réduit à 320 px.

