# Architecture cible de la plateforme

## Positionnement

Vertex est la couche d'intelligence située au-dessus des sources et du courtier. IBKR détient comptes, positions et données autorisées. TradingView fournit des alertes/contextes. Les autres sources apportent macro, fondamentaux, news, calendrier ou signaux. Vertex normalise, vérifie, analyse, relie et explique ; l'humain décide et agit hors de Vertex.

## Pipeline canonique

```text
Sources réelles
→ normalisation + identités + provenance + fraîcheur
→ stores et snapshots point-in-time
→ moteurs déterministes spécialisés
→ packet de décision versionné
→ hard gates + scénarios + impact portefeuille
→ verdict canonique
→ explication IA sourcée
→ pages + suivi + journal + audit
→ performance + apprentissages confirmés humainement
```

## Objets transversaux

- `Instrument` : action, ETF, indice, option, devise ou autre actif reconnu.
- `MarketSnapshot` : valeur, source, timestamp, mode et qualité.
- `Opportunity` : candidat détecté, raisons, score, fraîcheur, gates et statut.
- `AnalysisDossier` : faits, dimensions, scénarios, décision et limites.
- `Thesis` : raison, catalyseurs, invalidation, horizon, prochaine revue et historique.
- `PositionView` : source, coût, mark, exposition, P&L, rôle et risque.
- `OptionContractView` : contrat, quote, Greeks, IV, liquidité, multiplicateur et provenance.
- `DecisionPacket` : sortie immuable et versionnée des moteurs.
- `FollowUp` : objet surveillé, échéance, événement, changement et état.
- `PerformanceRecord` : signal théorique, suivi ou trade réel explicitement typé.

Réutiliser les modèles existants et créer un adaptateur canonique avant un nouveau modèle parallèle.

## Expérience transversale

- Recherche globale par ticker, société, ETF, position, thèse ou décision.
- Command palette pour navigation et actions non destructives.
- Drawers de détail réutilisables pour instrument, position, contrat, source et décision.
- Centre de notifications interne : fraîcheur, événement, thèse à revoir, risque ou job en échec.
- Provenance, timestamp et mode de donnée accessibles partout.
- Préférences de densité, colonnes et vues cohérentes sur toutes les tables.

## Frontières

- Le frontend ne recalcule aucun verdict.
- L'IA ne devient jamais un moteur canonique.
- Un provider ne devient jamais silencieusement la vérité unique.
- Les données utilisateur et signaux théoriques ne partagent pas un KPI sans séparation explicite.
- Les pages composent des vues ; elles ne possèdent pas les stores ni la logique métier.

