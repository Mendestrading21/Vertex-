# Calendrier central et alertes

Contrat de présentation uniquement : composer les événements et alertes déjà fournis ; ne créer ni source, ni type d'alerte, ni état persistant, ni calcul, ni job.

## Mission

Répondre à : **qu'est-ce qui arrive, quand, quels instruments ou positions sont concernés, quel est le niveau d'importance et quelle préparation analytique est nécessaire ?**

Le Calendrier est une surface transversale accessible depuis la topbar, Aujourd'hui et les pages concernées. Il agrège des événements réels sans devenir un second moteur ni dupliquer les données.

## Types d'événements

- macro : inflation, emploi, PIB, PMI, ventes, confiance et publications réellement disponibles ;
- banques centrales : décisions, minutes, discours et conférences ;
- résultats : date, session, estimation/réel lorsque fournis, guidance et lien au dossier ;
- dividendes : ex-date, paiement et montant/devise lorsque disponibles ;
- options : expirations, événements dans l'échéance et proximité d'une position ;
- portefeuille/watchlist : catalyseurs, invalidations, prochaine revue et événements suivis ;
- performance/journal : revues planifiées et suivis en retard ;
- système : jobs ou renouvellements techniques seulement s'ils nécessitent une action utilisateur.

Ne pas afficher rumeurs ou dates incertaines comme confirmées. Conserver source, timestamp, statut confirmé/estimé et dernière mise à jour.

## Vues

- **Aujourd'hui** : chronologie de séance dans le fuseau choisi, avec maintenant/prochain.
- **Semaine** : événements regroupés par jour et priorité.
- **Mois** : densité d'événements et accès au détail, sans surcharge de texte.
- **Agenda** : table filtrable et exportable si autorisé.
- **Portefeuille** : uniquement événements touchant positions et options détenues.
- **Watchlist/Opportunités** : événements des dossiers surveillés.
- **Macro** : calendrier économique et banques centrales.
- **Options** : expirations et risques événementiels par échéance.

## Filtres et recherche

Type, importance, pays/devise, symbole, secteur, portefeuille, watchlist, opportunité, confirmé/estimé, période et source. Les filtres sont partageables entre widget compact et page complète sans nouvelle clé de sync non déclarée.

## Carte événement

Chaque événement expose : titre français, type, date/heure et fuseau, importance, statut, instruments/positions concernés, source, fraîcheur, consensus/réel/précédent si réels, contexte, risque potentiel et liens vers dossier/position/options. L'IA peut expliquer l'enjeu depuis les faits disponibles, jamais prédire le résultat comme certain.

## Alertes

Composer visuellement un centre d'alertes non transactionnel à partir des alertes et états déjà présents. Si un type, un snooze ou une résolution n'existe pas, afficher la capacité manquante et ne pas l'implémenter dans ce chantier :

- événement proche pour position ou option ;
- thèse ou position à revoir ;
- donnée stale/delayed/offline ;
- hard gate ou risque réellement déclenché ;
- changement significatif d'un dossier selon moteur ;
- expiration proche ;
- job/source en échec.

Afficher type, sévérité, cause, source, timestamp, objet lié et, lorsqu'ils existent déjà, état lu/non lu, snooze et résolution. Acquitter une alerte ne modifie pas le verdict ou le moteur.

## Intégration dans les pages

- Aujourd'hui : cinq prochains événements et risques de séance.
- Marchés : macro et banques centrales.
- Opportunités/Analyse : catalyseurs et résultats du dossier.
- Portefeuille : calendrier agrégé des positions et thèses.
- Options : événement dans l'échéance et expirations.
- Performance : revues et suivis en retard.
- Intelligence : explication des impacts et contradictions.

## Fuseaux horaires

Conserver les timestamps et fuseaux fournis par les contrats existants ; afficher selon la préférence utilisateur sans réécrire la donnée. Toujours montrer le fuseau lorsque l'heure influence une décision. Vérifier le rendu au changement d'heure et pour les événements sans heure précise. Ne jamais supposer que la date fournisseur est locale.

## États

Loading, empty, partial, stale, offline et error. Un calendrier vide distingue « aucun événement » de « source indisponible ». En mode partiel, indiquer les catégories couvertes et manquantes.
