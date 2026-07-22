# Règles d'édition sûre et de lecture seule

## Invariant absolu

- Vertex ne passe jamais d'ordre, live ou paper.
- `READONLY=True` reste figé dans `vertex/app/config.py`.
- Chaque connexion IBKR conserve `readonly=True`.
- Le « Desk » prépare et simule ; il ne transmet rien.
- Tout vocabulaire ou CTA suggérant une exécution est un défaut P0.

Référence : `docs/canonical/READONLY.md`. Gardien principal :
`tests/test_no_orders.py`.

## Avant de modifier

- Lire les producteurs, consommateurs et tests du comportement ciblé.
- Ne jamais mélanger refonte visuelle, moteur trading, données et connexion IBKR.
- Ne jamais supprimer une fonctionnalité parce qu'elle paraît inutilisée sans
  rechercher routes, imports, scripts et tests.
- Ne jamais désactiver un test pour faire passer un lot.

## Pièges du dépôt

- Apostrophes françaises dans les chaînes JS embarquées : les échapper.
- `scan_state` est muté en place et jamais réassigné.
- Changement du shell : bump du service worker et de ses gardiens.
- Nouvelle clé desk : mettre à jour le registre canonique et tous ses miroirs.
- Texte externe rendu en HTML : passer par `news_plus.sanitize_news()`.
- `desk_data.json` : aucune édition manuelle ; utiliser backups et restauration.

## Validation par lot

1. Annoncer problème, périmètre, fichiers et risque.
2. Appliquer un changement cohérent et limité.
3. Exécuter `python -m compileall -q terminal.py vertex`.
4. Exécuter `python -m pytest tests/ -q` à 100 %.
5. Démarrer en démo, vérifier `/healthz`, `/api/client-log` et le navigateur.
6. Mettre à jour `docs/vertex-v4/STATUS.md`.
7. Produire un commit atomique sans secret ni donnée personnelle.

## Secrets et données locales

Ne jamais committer `.env`, `.vertex_secret`, `desk_data.json`, caches, backups,
inventaires de positions, identifiants de compte ou captures non anonymisées.
