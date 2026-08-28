# Architecture cible de la plateforme

Cette référence définit la cible. Toute migration suit les lots, tests de
parité et rollbacks du skill maître ; elle n'autorise aucun big bang.

## Positionnement

Vertex est la couche d'intelligence située au-dessus des sources de marché.
IBKR fournit seulement les données de marché autorisées. Le portefeuille et
les enveloppes sont déclarés par l'utilisateur dans Vertex. TradingView fournit
des événements/contextes de réévaluation. Les autres sources apportent macro,
fondamentaux, news et calendrier. Vertex normalise, vérifie, calcule, relie et
explique ; l'humain décide et agit hors de Vertex.

## Pipeline canonique

```text
Sources réelles
→ normalisation + identités + provenance + fraîcheur
→ stores et snapshots point-in-time
→ moteurs déterministes spécialisés
→ packet de décision versionné
→ hard gates + scénarios + impact portefeuille
→ AdviceResult canonique
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
- `DeclaredPosition` : saisie utilisateur, coût déclaré, rôle, thèse et risque.
- `MarketValuation` : mark externe, source, fraîcheur, qualité, FX et valeur
  estimée ; ne modifie jamais la déclaration.
- `OptionContractView` : contrat, quote, Greeks, IV, liquidité, multiplicateur et provenance.
- `DecisionPacket` : sortie immuable et versionnée des moteurs.
- `FollowUp` : objet surveillé, échéance, événement, changement et état.
- `PerformanceRecord` : signal théorique, suivi ou trade réel explicitement typé.

La migration réutilise les modèles sains, choisit un propriétaire par objet et
retire les parallèles seulement après parité. Une adaptation UI ne calcule ni
ne persiste de logique financière.

## Expérience transversale

- Recherche globale par ticker, société, ETF, position, thèse ou décision.
- Command palette pour navigation et actions non destructives.
- Drawers de détail réutilisables pour instrument, position, contrat, source et décision.
- Centre de notifications interne : fraîcheur, événement, thèse à revoir, risque ou job en échec.
- Calendrier global : macro, résultats, dividendes, expirations, catalyseurs, positions et revues, agrégé sans duplication.
- Provenance, timestamp et mode de donnée accessibles partout.
- Préférences de densité, colonnes et vues cohérentes sur toutes les tables.

## Frontières

- Le frontend ne recalcule aucun verdict.
- Aucune route utilisateur n'attend une collecte réseau lente.
- Aucun objet client IBKR brut ne franchit la façade market-data-only.
- L'IA ne devient jamais un moteur canonique.
- Un provider ne devient jamais silencieusement la vérité unique.
- Les données utilisateur et signaux théoriques ne partagent pas un KPI sans séparation explicite.
- Les pages composent des vues ; elles ne possèdent pas les stores ni la logique métier.
