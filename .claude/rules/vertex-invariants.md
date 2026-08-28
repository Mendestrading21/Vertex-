# Invariants permanents Vertex

- Charger `.claude/skills/vertex-2-0/SKILL.md` pour tout chantier Vertex.
- `READONLY=True`, `ANALYSIS_ONLY=True` ; aucun ordre live/paper, ticket broker,
  transfert, exécution ou bouton transactionnel.
- IBKR fournit uniquement des données de marché. Interdire comptes, cash, NAV,
  positions, portefeuille, P&L, ordres, exécutions et objet client brut.
- Le portefeuille est uniquement déclaré par l'utilisateur ; aucune source
  externe ne crée, ferme ou modifie une position.
- Jamais de chiffre inventé : zéro, absent, estimation, delayed, stale, démo et
  erreur sont distincts.
- Une valeur critique porte valeur, unité, devise, source, timestamp,
  fraîcheur, qualité, fallback et lineage.
- Un seul `AdviceResult` fait autorité ; Claude explique, l'humain décide.
- Une capacité sans exécuteur réel vaut `NON_IMPLÉMENTÉ`.
- Aucun secret, identifiant ou patrimoine dans Git, logs, captures, cache,
  télémétrie ou prompt IA implicite.
- Supprimer uniquement après consommateurs, migration, parité et rollback.
- PR brouillon ; aucune fusion, release ou suppression distante automatique.
