# Blueprint pages, graphiques et intelligence

## Usage

Cette référence définit la composition cible, pas une promesse de capacité.
Claude commence chaque page par la question utilisateur, mesure les données et
moteurs réellement disponibles, puis classe chaque bloc `RÉEL`, `PARTIEL`,
`DÉGRADÉ`, `ABSENT` ou `NON_IMPLÉMENTÉ`. Un widget sans contrat de données reste
hors de la page.

## Règle de composition

Chaque page possède exactement :

1. une question principale compréhensible en cinq secondes ;
2. une visualisation ou table dominante ;
3. trois à cinq preuves secondaires au maximum au-dessus du pli ;
4. une provenance locale et une fraîcheur visible ;
5. une action primaire non financière ;
6. les états loading, vide, partiel, stale, delayed, offline et erreur ;
7. une table ou liste accessible pour tout graphique décisionnel.

Les KPI ne sont pas des décorations. Tout KPI indique population, période,
unité, source et variation comparable. Ne jamais additionner signaux théoriques,
simulations, suivis et positions déclarées.

## Matrice cible

| Page | Question | Zone dominante | Widgets utiles | Action primaire | Mobile |
|---|---|---|---|---|---|
| Aujourd'hui | Que dois-je comprendre ou revoir maintenant ? | `DecisionTrace` condensée + fil d'attention | `MarketPulseStrip`, `SessionTimeline`, `AlertRail`, `PortfolioSnapshot` manuel | Ouvrir le dossier prioritaire | attention → événements → risques → contexte |
| Calendrier | Quels événements peuvent modifier mes thèses ? | agenda chronologique filtrable | `CalendarHeatmap`, sessions, résultats, macro, dividendes, expirations, revues | Ajouter une revue/alerte | liste par jour, filtres en drawer |
| Marchés | Quel régime et quelles zones bougent ? | `MarketHeatmap` ou `BreadthBoard` | courbes indices/taux/FX, secteurs, volumes, leaders/retardataires, `DataLedger` | Explorer un instrument | résumé → heatmap/table → listes |
| Opportunités | Quels candidats méritent une analyse ? | `OpportunityRankTable` | funnel, raisons/gates, catalyseurs, mini-courbes, contradictions | Ouvrir l'analyse | filtres compacts + cartes/table |
| Analyse | Quelle est la thèse, sa preuve et son invalidation ? | `PriceWorkbench` + `ThesisRail` | `AdviceResult`, preuves, scénarios, événements, fondamentaux, options, risques | Comparer les scénarios | conclusion → prix → thèse → preuves |
| Options | Que dit la chaîne et quel contrat est exploitable analytiquement ? | `OptionChainGrid` | term structure, skew, OI, volume, spread, Greeks, GEX si réel, drawer contrat | Simuler le contrat | expiration → chaîne empilée → drawer |
| Simulateur | Quel résultat théorique sous mes hypothèses ? | `ScenarioComposer` + `ScenarioCompare` | payoff, spot×temps, sensitivités, impact portefeuille, hypothèses | Mettre à jour la simulation | entrées essentielles → résultats → risque |
| Portefeuille | Où sont mes expositions déclarées et mes concentrations ? | `PortfolioSnapshot` + `PositionTable` | allocation, contribution, devises, secteurs, corrélation, couverture des marks | Ajouter/modifier une position | résumé → positions → expositions |
| Suivi | Qu'est-ce qui a changé depuis ma dernière revue ? | table des thèses et alertes | changements, invalidations, catalyseurs, prochaine revue, mini-courbes | Réviser une thèse | en retard → déclenché → à venir |
| Performance | Qu'est-ce qui fonctionne, sur quelle population et avec quel risque ? | equity/drawdown synchronisés | heatmap mensuelle, distribution, rolling, setup/régime, benchmark | Comparer une population | KPI → equity/drawdown → diagnostics |
| Vertex IA | Que peut expliquer Vertex à partir des preuves disponibles ? | réponse structurée + `DecisionTrace` | citations, contradictions, manques, outils appelés, historique | Poser une question | réponse → preuves → limites |
| Système | La machine est-elle saine et quelles données puis-je croire ? | `SourceHealthGrid` | jobs, caches, budgets, erreurs, versions, sécurité, stockage | Diagnostiquer une source | incidents → sources → détails |

## Analyse en neuf lentilles

Le dossier Analyse projette les sorties existantes dans neuf lentilles. Une
lentille absente ne reçoit ni score neutre ni remplissage IA.

1. **Identité et liquidité** : instrument, place, devise, session, spreads et
   qualité de données.
2. **Fondamentaux** : publications, croissance, marges, bilan, valorisation et
   comparables lorsque disponibles.
3. **Prix et structure** : tendance, niveaux, volatilité réalisée, volume et
   régime depuis moteurs canoniques.
4. **Catalyseurs** : résultats, macro, dividendes, décisions, échéances et
   événements sourcés.
5. **Options et volatilité** : IV, term structure, skew, OI, Greeks et
   liquidité avec unités explicites.
6. **Contexte transversal** : secteur, indices, taux, devise et corrélations
   point-in-time.
7. **Thèse et contre-thèse** : faits confirmants, contradictions, inconnues,
   invalidation et horizon.
8. **Impact portefeuille** : poids et risques depuis les positions saisies
   manuellement, jamais depuis IBKR.
9. **Décision et suivi** : orientation canonique, gates, scénario, prochaine
   revue et événements à surveiller.

## Hiérarchie visuelle Black Glass

- Niveau 0 : fond noir profond, sans glow global.
- Niveau 1 : shell et grands canvases vitrés presque noirs.
- Niveau 2 : cartes fonctionnelles avec séparation par lumière, contraste et
  espace ; pas de grille de bordures.
- Niveau 3 : couleur sémantique locale uniquement sur donnée, sélection,
  événement ou risque.
- Cyan signal : navigation active, donnée live et liens analytiques.
- Violet options : volatilité, options et simulation avancée seulement.
- Vert/rouge : variation favorable/défavorable dans un contexte nommé, jamais
  seuls porteurs de sens.
- Ambre : attention, stale, événement proche ou donnée partielle.
- Blanc froid : texte principal et courbes neutres.

Au-dessus du pli, limiter les accents simultanés à deux familles. Les graphiques
conservent une grille faible, un crosshair net, des axes lisibles et une seule
série mise en avant. Le glow est une conséquence locale de la lumière, jamais
un contour permanent.

## Cohérence transversale

- Le contexte instrument, timeframe, snapshot et scénario suit le parcours
  Opportunités → Analyse → Options → Simulateur → Suivi.
- Un drawer Instrument, Contrat, Source, Thèse et Position possède un seul
  propriétaire chacun.
- La période, la source, le statut de fraîcheur et le mode de données occupent
  toujours le même emplacement.
- Une sélection graphique met à jour les preuves liées sans recalcul métier
  dans le navigateur.
- La recherche globale distingue instrument, ETF, contrat, thèse, position et
  page avant navigation.
- Les préférences de densité et colonnes sont cohérentes, versionnées et
  migrées ; aucune nouvelle clé locale improvisée.

## Test de retrait

Retirer tout widget qui ne répond pas à une question, duplique une métrique,
masque sa population, dépend d'une donnée absente, pousse une action financière
ou rend la page moins lisible à 390 px. Une page premium est dense en preuves,
pas en cartes.
