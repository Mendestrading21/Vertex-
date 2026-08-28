# Définition de terminé

## Pour un contrat ou service

- propriétaire unique, API et consommateurs inventoriés ;
- données, unités, provenance, fraîcheur, erreurs et états documentés ;
- tests rouges du défaut puis tests de contrat, panne et sécurité verts ;
- aucune route UI bloquée par un réseau lent ;
- migration idempotente et rollback si données ou schéma changent ;
- métriques avant/après et observabilité sans information privée ;
- ancien propriétaire retiré seulement après parité.

## Pour IBKR et le portefeuille

- gateway IBKR limité structurellement aux données de marché ;
- double hostile prouvant zéro appel compte/position/P&L/ordre ;
- aucun objet IB brut, route compte, cache personnel ou prompt implicite ;
- portefeuille exclusivement déclaré et sauvegardé par l'utilisateur ;
- origine de position et source de prix séparées ;
- panne/activation IBKR ne modifie aucune déclaration.

## Pour une décision ou fonction IA

- un seul `AdviceResult`, versionné, rejouable et consommé partout ;
- faits, calculs, estimations et interprétations distincts ;
- hard gates fail-closed et inconnues jamais neutralisées ;
- aucune règle ou verdict recalculé dans l'UI ;
- Claude passe par la gateway contrôlée et explique sans remplacer le moteur ;
- probabilité, scénario, options et R:R ont unités, méthode et limites.

## Pour un composant

- propriétaire visuel unique et API de présentation documentée ;
- tokens canoniques, tous états, clavier/touch, responsive et HiDPI ;
- aucune logique financière ajoutée dans HTML/CSS/JavaScript ;
- démontré sur `/design-system` si réutilisable ;
- tests ou preuve navigateur proportionnés.

## Pour une page

- question et point focal compris en cinq secondes ;
- données, fonctions et `AdviceResult` viennent des propriétaires canoniques ;
- loading, empty, missing, partial, delayed, stale, offline, demo et error
  selon applicabilité ;
- deep links, retour, filtres et préférences stables ;
- clavier, zoom, reduced motion et largeurs 1600/1024/390 ;
- console, réseau, `/api/client-log` et health sans erreur liée au lot ;
- captures avant/après sur mêmes données, route, viewport et état ;
- tests ciblés, accessibilité et budgets verts.

## Pour un lot

- contrat, baseline, fichiers, consommateurs, données et rollback renseignés ;
- aucune capacité perdue, collision ou fausse fonctionnalité ajoutée ;
- compile, tests ciblés/complets, no-orders, privacy et sécurité exécutés ;
- mesures de performance et états dégradés vérifiés ;
- diff relu depuis zéro, sans secret, donnée personnelle ou changement hors lot ;
- les contrôles applicables de `audit-150.md` ont une preuve ;
- PR brouillon documentant résultats exacts, écarts et limites ;
- décision humaine avant fusion ou release.

Ne jamais déclarer « 100 % terminé » depuis une suite verte seule. Il faut
preuve runtime, navigateur, contrats, données, rollback et acceptation humaine.
