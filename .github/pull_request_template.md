## Objectif

Décrire le problème utilisateur et le résultat mesurable.

## Périmètre / non-objectifs

- Inclus:
- Exclu:

## Architecture et données

- propriétaire canonique avant/après:
- sources, fraîcheur et provenance:
- migration/compatibilité:

## Sûreté

- [ ] analyse uniquement;
- [ ] aucun chemin d'ordre;
- [ ] aucune donnée inventée;
- [ ] hard gates intacts;
- [ ] secrets et données de compte exclus.

## Preuves

- [ ] compileall;
- [ ] pytest complet;
- [ ] test anti-ordre isolé;
- [ ] health/client-log/UI si concernés.

## Risques et rollback

Risques:

Rollback:

## Limites et décisions humaines

Lister explicitement ce qui n'a pas été vérifié. Ne jamais déclarer la release
finale sans CI verte et acceptation humaine du même SHA.
