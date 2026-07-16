# VERTEX — Règles d’exécution de la refonte

## Invariants

- Vertex reste en lecture seule.
- `READONLY=True` ne doit jamais être affaibli.
- Aucun chemin d’ordre, achat, vente ou transmission broker.
- Les calculs, moteurs et contrats de données ne sont pas modifiés pour satisfaire un visuel.
- Donnée absente = `—`, `n/d`, empty, partial ou stale honnête.
- Ne jamais confondre signaux théoriques, positions déclarées et portefeuille IBKR.
- Les news et textes externes restent sanitizés.
- Toute nouvelle clé desk respecte les listes de synchronisation.
- Tout changement visible du shell/statique implique le bump du service worker dans `vertex/app/routes/system.py`.
- Tests verts avant chaque commit.
- Vérification navigateur réelle et console vide.

## Architecture à respecter

- Python/Flask ;
- shell `vertex/ui/shell/` ;
- pages `vertex/ui/pages/` ;
- CSS `vertex/static/vertex/css/` ;
- charts `vertex/static/vertex/js/charts/` ;
- Chart.js et TradingView Lightweight Charts ;
- données via `VX.fetch`, endpoints Flask, localStorage et desk sync.

## Méthode Git

1. branche dédiée ;
2. baseline ;
3. commits petits et thématiques ;
4. une phase par commit ou série cohérente ;
5. jamais pousser sur `main` sans accord ;
6. rollback clair.

## Méthode de travail

1. lire le code ;
2. cartographier les données ;
3. écrire le mini-plan ;
4. fondations avant pages ;
5. vérifier desktop/laptop ;
6. vérifier réel/empty/stale/error ;
7. tests ciblés ;
8. suite complète ;
9. navigateur ;
10. commit explicite.

## Interdiction de maquillage

Ne jamais remplacer un problème de données par un nombre exemple, une courbe fantôme présentée comme réelle, un score calculé dans l’UI, une valeur colorée par défaut ou un texte ressemblant à un verdict moteur.

## Priorité

1. tokens/surfaces ;
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
14. Tracking/secondaires ;
15. responsive/a11y/QA.
