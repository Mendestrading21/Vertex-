# Navigation et pages définitives

## Shell global

La cible à douze pages est une décision produit Vertex 2.0, pas l'état actuel.
Lire `runtime-page-manifest.md` avant toute modification : il distingue les
pages servies, redirigées, absentes et internes. Le runtime actuel reste servi
pendant la migration. Un `NavigationManifest` unique doit produire
sidebar desktop, barre mobile, tiroir Plus, palette, breadcrumbs, aliases,
sous-vues et tests ; aucun tableau Python/JS recopié ne reste propriétaire.

### Sidebar

**Piloter**

- Aujourd'hui — `/`
- Calendrier — `/calendar`

**Explorer**

- Marchés — `/markets`
- Opportunités — `/opportunities`
- Analyse — `/analysis`
- Options — `/options`
- Simulateur — `/simulator`

**Gérer**

- Portefeuille — `/portfolio`
- Suivi — `/follow-up`
- Performance — `/performance`

**Intelligence**

- Vertex IA — `/intelligence`

**Bas de sidebar**

- Système — `/system`

Design System reste `/design-system`, accessible en développement seulement.
Les anciennes routes Journal et Tracking ne redirigent vers leurs sous-vues
canoniques qu'après migration et preuve de parité ; elles servent encore du
contenu dans la baseline.

### Topbar

Recherche globale/ticker, fraîcheur globale, statut marché, bouton Calendrier, centre d'alertes, raccourci Vertex IA, profil/préférences. Aucun gros bouton décoratif.

## Contrat commun d'une page

1. `PageHeader` : titre, question métier, périmètre, fraîcheur et actions sûres.
2. `ContextBar` : période, univers, filtres et source.
3. `DecisionZone` : un point focal principal.
4. `EvidenceZone` : métriques et graphiques qui expliquent.
5. `WorkZone` : table, suivi ou interaction principale.
6. `DepthZone` : historique, méthode et détails.

## 1. Aujourd'hui

**Question :** que dois-je comprendre, surveiller et revoir maintenant ?

Premier écran : état des données/séance, régime, risque principal, décisions à revoir, cinq prochains événements, top opportunités et snapshot portefeuille. Le point focal est une `DecisionTrace` quotidienne, pas une grille de KPI égaux.

Sections : Brief IA sourcé, Marchés, Opportunités, Portefeuille, Options, Alertes, Calendrier. Chaque carte renvoie vers son propriétaire ; aucune logique dupliquée.

## 2. Calendrier

**Question :** qu'est-ce qui arrive et qu'est-ce que cela touche ?

Vues : Aujourd'hui, Semaine, Mois, Agenda, Portefeuille, Macro, Options. Premier écran : timeline de séance + événements touchant positions/watchlist + filtres actifs. Table principale : heure/fuseau, événement, type, importance, statut, instruments concernés, consensus/réel si disponibles, source et fraîcheur.

## 3. Marchés

**Question :** dans quel environnement la stratégie opère-t-elle ?

Sous-vues : Synthèse, Macro, Indices & cross-asset, Secteurs, Participation, Volatilité. Premier écran : régime, risques, leadership, indices et changements. Une visualisation dominante par sous-vue ; les preuves secondaires ne répètent pas la même information.

## 4. Opportunités

**Question :** quels dossiers méritent une analyse maintenant ?

Sous-vues : Radar, Actions, ETF, Options, Anomalies, Catalyseurs. Premier écran : entonnoir de détection, changements depuis le scan, top candidats et gates. Table principale configurable ; drawer expliquant score, preuves, contradictions, événement, fraîcheur et impact portefeuille préliminaire.

## 5. Analyse

**Question :** ce dossier mérite-t-il du capital potentiel et sous quelles conditions ?

Index : recherche, récents, favoris et comparateur. Dossier : Orientation,
Graphique, Thèse, Scénarios, Fondamentaux, Technique, Sentiment/News, Options,
Portefeuille déclaré, Historique. Premier écran : identité/quote,
`AdviceResult`/gates, `DecisionTrace`, graphique dominant et rail
thèse/risque/invalidation. Aucun second moteur n'est affiché comme autorité.

## 6. Options

**Question :** quelle exposition optionnelle est compréhensible, liquide et compatible avec le risque ?

Sous-vues : Vue d'ensemble, Chaîne, Volatilité, Scanner, Scénarios, Positions, Événements. Premier écran : sous-jacent, état de la quote/chaîne, régime IV, liquidité, événement et meilleurs contrats. La chaîne CALL/strike/PUT est la table spécialisée principale.

## 7. Simulateur

**Question :** que pourrait devenir une position sous plusieurs scénarios explicites, et quel serait son impact sur le portefeuille ?

Sous-vues : Simple, Avancé, Comparer, Historique seulement si une persistance existe déjà. Classes : Actions, ETF, Options et Forex, selon les données réellement disponibles. Premier écran : paramètres à gauche, scénario central, résultats/risques à droite, hypothèses et provenance toujours visibles. Les sorties sont des simulations, jamais une prédiction certaine, une recommandation ou un ticket d'ordre.

Lire `position-simulator.md`. Une fonction absente reste un état manquant documenté ; aucun calcul financier n'est créé dans l'UI.

## 8. Portefeuille

**Question :** que possède le portefeuille, pourquoi et avec quels risques ?

Sous-vues : Synthèse, Enveloppes, Positions, Allocation, Options, Risque,
Thèses. Premier écran : patrimoine déclaré, valorisation estimée, couverture des
cotes, risque principal, concentration, contributeurs et revues urgentes.
Tables positions et options séparées ; saisie/édition manuelle et drawer par
position. IBKR n'apparaît que comme source possible des marks de marché.

## 9. Suivi

**Question :** quelles thèses, idées et décisions exigent une attention ?

Sous-vues : À revoir, Watchlist, Opportunités suivies, Positions, Options, Alertes, Archives. Premier écran : éléments en retard, prochains événements, changements moteurs et données stale. Table principale : type, objet, statut workflow, verdict séparé, priorité, prochaine revue, catalyseur, invalidation, événement et fraîcheur.

## 10. Performance

**Question :** la méthode fonctionne-t-elle et est-elle bien appliquée ?

Sous-vues : Synthèse, Journal, Trades réels, Signaux théoriques, Tracking hypothétique, Apprentissages. Premier écran adapté à la population sélectionnée : échantillon, période, benchmark, equity/drawdown et limites. Aucun KPI mélangeant les populations.

## 11. Vertex IA

**Question :** comment Vertex comprend-il la situation, où sont les contradictions et que manque-t-il ?

Sous-vues : Assistant, Brief quotidien, Orientation, Recherche, Mémoire.
Premier écran : conversation contextuelle + contexte actif + sources/packet.
Les détails montrent preuves, contradictions, gates, versions et audit trail ;
un comité éventuel reste une preuve interne, jamais une décision concurrente.

## 12. Système

**Question :** Vertex est-il sain, alimenté et correctement configuré ?

Sous-vues : Connexions, Données, Jobs, Alertes techniques, Préférences, Sécurité, Archives, Design System. Premier écran : READONLY, santé globale, sources dégradées, fraîcheur par domaine, jobs en échec et stockage/sync.

## Routes secondaires

Utiliser deep links pour ticker, contrat, position, thèse, événement, suivi et décision. Chaque route secondaire garde breadcrumb, contexte d'origine et retour prévisible. Préférer un drawer lorsque la tâche est de comparer ou scanner ; préférer une page lorsque le contenu exige historique, onglets ou URL partageable.
