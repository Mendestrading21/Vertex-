# VERTEX — Règles d’exécution de la refonte

## Invariants

- Vertex reste en lecture seule.
- `READONLY=True` ne doit jamais être affaibli.
- Aucun chemin d’ordre, achat, vente ou transmission broker ne doit être ajouté.
- Les calculs, moteurs et contrats de données ne sont pas modifiés pour satisfaire un visuel.
- Donnée absente = `—`, `n/d`, état vide, partiel ou stale honnête.
- Ne jamais confondre signaux théoriques, positions déclarées et portefeuille IBKR.
- Les news et textes externes restent sanitizés.
- Toute nouvelle clé desk doit respecter les listes de synchronisation existantes.
- Tout changement visible du shell/statique implique le bump du service worker dans `vertex/app/routes/system.py`.
- Les tests doivent passer avant chaque commit.
- Vérification navigateur réelle et console vide obligatoire.

## Architecture actuelle à respecter

- Python/Flask ;
- shell commun `vertex/ui/shell/` ;
- pages Python dans `vertex/ui/pages/` ;
- CSS dans `vertex/static/vertex/css/` ;
- graphiques JS dans `vertex/static/vertex/js/charts/` ;
- scripts de page dans les pages Python et `vertex/static/vertex/js/pages/` ;
- Chart.js et TradingView Lightweight Charts ;
- données via `VX.fetch`, endpoints Flask, localStorage et desk sync.

## Méthode Git

1. travailler sur une branche dédiée ;
2. capturer l’état initial ;
3. commits petits et thématiques ;
4. une phase = un ou plusieurs commits isolés ;
5. ne jamais pousser sur `main` sans accord explicite ;
6. conserver un rollback clair.

## Méthode de travail

Pour chaque phase :

1. lire le code concerné ;
2. cartographier les données ;
3. écrire un mini-plan ;
4. modifier les fondations avant les pages ;
5. vérifier desktop et laptop ;
6. vérifier les états réels, vides, stale et error ;
7. lancer les tests ciblés ;
8. lancer la suite complète ;
9. vérifier le navigateur ;
10. committer avec un message explicite.

## Interdiction de « maquillage »

Ne pas remplacer un problème de données par :

- un nombre exemple ;
- une courbe fantôme présentée comme réelle ;
- un score calculé dans l’UI ;
- une valeur par défaut colorée ;
- un texte généralisé qui ressemble à un verdict moteur.

## Priorité de migration

1. tokens et surfaces ;
2. shell ;
3. primitives ;
4. charts core ;
5. Briefing ;
6. Marchés ;
7. Opportunités ;
8. Portefeuille ;
9. Analyse ;
10. Options ;
11. Performance ;
12. Intelligence ;
13. Système ;
14. Tracking et routes secondaires ;
15. responsive, a11y, QA finale.
