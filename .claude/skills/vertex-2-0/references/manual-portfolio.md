# Portefeuille manuel et souveraineté utilisateur

## Principe

Le portefeuille Vertex est une déclaration volontaire de l'utilisateur. Il
n'est ni une copie du courtier ni un agrégateur bancaire. Les données saisies
restent propriétaires et ne sont jamais écrasées par IBKR, TradingView, Claude
ou un import implicite.

## Objets cibles

- `ManualAccount` : identifiant interne, nom libre, type, devise d'affichage,
  notes et ordre ; aucune référence broker obligatoire ;
- `DeclaredPosition` : compte interne, instrument, classe d'actif, quantité,
  coût déclaré, devise, dates, statut, stratégie, horizon et tags ;
- `Thesis` : raison, catalyseurs, invalidation, scénarios, conviction,
  prochaine revue et historique ;
- `DeclaredCash` : montant volontaire par enveloppe, facultatif ;
- `ManualTransaction` : ajout, réduction, clôture, revenu ou ajustement déclaré,
  seulement si le store existant le supporte ou après migration dédiée ;
- `MarketValuation` : cote externe, timestamp, source, FX, qualité et valeur
  estimée ; séparée de la déclaration.

Ne pas créer un nouveau modèle parallèle si `myTrades`, desk sync, vault,
journal ou les stores existants peuvent être migrés vers ce contrat.

## Provenance visible

Chaque champ porte l'une des origines : `SAISIE`, `MARCHÉ`, `MOTEUR`,
`ESTIMATION`. Une valeur composée expose ses intrants. L'interface emploie
`Patrimoine déclaré`, `Position saisie`, `Valeur estimée au marché` et
`Dernière mise à jour manuelle`.

## Parcours

- créer, renommer, ordonner et archiver une enveloppe ;
- ajouter une position Action, ETF, Option, Forex ou fonds supporté ;
- modifier une déclaration avec prévisualisation du diff ;
- déclarer une réduction ou clôture ;
- relier thèse, stratégie, documents, alertes et calendrier ;
- dupliquer une hypothèse vers le Simulateur sans modifier le portefeuille ;
- déclarer explicitement une simulation comme position, avec confirmation
  humaine et formulaire complet ;
- importer un CSV seulement sur action explicite, avec mapping, aperçu,
  déduplication, sauvegarde et rollback. Aucun import automatique.

## Calculs et limites

Réutiliser uniquement les moteurs existants pour valeur, P&L, allocation,
exposition, stress, corrélation et Greeks. Si une donnée manque, afficher la
couverture et ne pas remplir par zéro. La saisie manuelle ne rend pas un calcul
vrai si prix, FX, multiplicateur ou historique manquent.

## Migration et sécurité

- sauvegarder le desk avant toute migration ;
- versionner le schéma et rendre la migration idempotente ;
- préserver IDs, timestamps, pièces, thèses, journal et clés de sync ;
- tester old → new → rollback sur fixture anonymisée ;
- chiffrer ou protéger le stockage selon le modèle d'accès réel avant de
  promettre une confidentialité forte ;
- ne jamais inclure le portefeuille dans télémétrie, crash report ou prompt IA
  sans minimisation et action attendue de l'utilisateur.

## Séparation des populations

Ne jamais fusionner dans un KPI : positions déclarées, trades déclarés,
signaux moteurs, idées suivies, simulations et tracking hypothétique. Chaque
série conserve type, source, période, échantillon et limites.
