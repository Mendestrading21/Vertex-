# Simulateur de position et scénarios

## Mission

Répondre à : **si j'expose un montant à cet instrument et que tel scénario se produit, quel serait le résultat théorique et l'impact sur mon portefeuille ?**

Le Simulateur est analytique, multi-actifs et strictement séparé de l'exécution. Employer `scénario`, `hypothèse`, `simulation` et `résultat théorique`. Ne jamais présenter une sortie comme une prévision certaine, une promesse, un signal ou une recommandation personnalisée.

## Séparation moteur / interface

La page compose les calculateurs, scénarios, quotes et positions déclarées du
contrat canonique. Le lot moteur peut consolider les calculateurs existants ;
la page ne crée ni pricing, conversion, Greek, probabilité, forecast, store ou
endpoint dans JavaScript.

Si un calcul manque, afficher `Calcul non disponible dans Vertex` avec les données nécessaires et consigner le besoin hors périmètre. Aucun calcul approximatif dans JavaScript ou le template.

## Navigation

Route principale visuelle : `/simulator`, sous **Explorer**. Deep links depuis Analyse, Options, Portefeuille, Opportunités et Position. Conserver le contexte d'origine et permettre le retour.

Vues :

- **Simple** : une position, trois scénarios, résultat et risque ;
- **Avancé** : hypothèses complètes et matrices disponibles ;
- **Comparer** : jusqu'à trois positions/scénarios sur la même base ;
- **Historique** : uniquement si Vertex possède déjà une persistance canonique de simulations.

## Paramètres communs

- classe : Action, ETF, Option ou Forex ;
- instrument/symbole et marché ;
- sens analytique : long/short seulement si supporté ;
- montant en devise ou quantité, avec bascule explicite ;
- prix de référence, source, timestamp et état ;
- horizon/date d'évaluation ;
- scénario A/B/C existant ou hypothèses manuelles autorisées ;
- portefeuille de référence facultatif ;
- devise d'affichage et conversion uniquement si fournie par une source canonique.

Toute valeur préremplie est étiquetée `Marché`, `Portefeuille`, `Moteur` ou `Saisie`.

## Contrats par classe d'actif

### Actions

Entrées possibles : montant/quantité, prix d'entrée, variation de prix ou scénarios moteur, horizon, dividendes seulement s'ils sont fournis. Sorties possibles : unités, notionnel, P&L théorique, rendement et impact portefeuille.

### ETF

Même contrat que l'action avec, si disponibles, look-through, frais, devise, concentration et overlap. Ne pas simuler des holdings absents ni une couverture de change non fournie.

### Options

Entrées possibles : sous-jacent, type, strike, échéance, quantité, multiplicateur, débit/crédit, mark/source, spot, date, hypothèse spot/IV. Sorties possibles : payoff, breakeven, gain/perte max lorsque définis, matrice spot × temps, sensibilités et impact Greeks, uniquement depuis les moteurs existants. Multi-jambes seulement si le moteur le supporte déjà.

### Forex

Entrées possibles : paire, devise base/cotation, sens, montant/notionnel, prix de référence, horizon et scénarios de taux. Sorties possibles : exposition, P&L en devise de cotation puis de référence si conversion canonique, variation en pips si déjà calculée. Aucun effet de levier, marge, swap ou rollover inventé.

## Composition desktop

1. `SimulatorHeader` : classe, instrument, fraîcheur, mode et contexte.
2. `ScenarioComposer` à gauche : entrées groupées, libellés et provenance.
3. `ResultCanvas` au centre : payoff, trajectoire ou matrice adaptée.
4. `RiskRail` à droite : résultat A/B/C, perte théorique, limites, événement et manques.
5. `PortfolioImpact` en dessous : avant/après avec dimensions disponibles.
6. `AssumptionLedger` : toutes les hypothèses, valeurs marché, sources et timestamps.
7. `CompareTray` : comparaison optionnelle, même unités et même date de référence.

Le bouton principal est `Mettre à jour la simulation`, jamais `Acheter`, `Vendre`, `Exécuter` ou `Valider l'ordre`.

## Présentation des résultats

- Séparer `Actuel`, `Scénario A`, `B`, `C` et `Donnée manquante`.
- Montrer montant absolu, pourcentage, devise, horizon et unité.
- Afficher les hypothèses à côté du résultat, pas dans une note cachée.
- Utiliser une plage uniquement si le moteur fournit une plage.
- Utiliser une probabilité uniquement si elle est canonique, sourcée et versionnée.
- Marquer les résultats comme théoriques et les données comme live/delayed/stale/demo/offline/missing.
- Conserver actions, ETF, options et forex comparables sans masquer leurs différences.

## Widgets

- Actions/ETF : ScenarioCompare, OutcomeRange, trajectoire et PortfolioImpact.
- Options : PayoffDiagram, SpotTimeHeatmap, GreeksExposure et ContractDrawer.
- Forex : ScenarioCompare, sensibilité taux/spot existante et exposition devise.
- Tous : PositionPreview, AssumptionLedger, DataLedger et table de résultats.

## États et erreurs

Loading, empty, invalid input, partial, stale, delayed, offline, missing engine et error. Une saisie invalide explique le champ, le format et l'unité. Une quote stale n'est pas silencieusement utilisée comme live. Une conversion manquante bloque seulement la vue convertie, pas les résultats dans la devise native.

## Mobile

Ordre : contexte → paramètres essentiels → résultats A/B/C → graphique → risque → impact portefeuille → hypothèses. Les paramètres avancés passent dans un drawer. Les tables deviennent cartes comparatives ou vues horizontales contrôlées ; aucune colonne financière n'est tronquée sans accès au détail.

## Garde-fous

- zéro action broker, export de ticket ou deep link d'exécution ;
- zéro prévision certaine ou vocabulaire promesse ;
- zéro valeur par défaut présentée comme marché réel ;
- zéro sauvegarde si le store n'existe pas ;
- aucune persistance dans une nouvelle clé localStorage non déclarée ;
- aucune modification de position ou portefeuille réel ;
- séparation permanente entre simulation, idée suivie, signal théorique et position réelle.

## Acceptation

Vérifier une simulation par classe disponible, montant et quantité, devise native/convertie, horizon, changement de scénario, données stale/missing, navigation clavier, mobile, retour vers la source, absence d'ordre, résultats identiques avant/après refonte et preuves des moteurs consommés.
