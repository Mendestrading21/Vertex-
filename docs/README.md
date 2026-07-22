# Documentation Vertex — index canonique

> **Status: ACTIVE**
> Last verified: 2026-07-22
> Branch: `integration/vertex-v4-clean`

Cet index indique ce qui fait autorité. Un document absent de la colonne
**ACTIVE** ne doit jamais contredire une source active.

## Sources actives

| Sujet | Source unique |
|---|---|
| Produit et stratégie | [`canonical/PRODUCT.md`](canonical/PRODUCT.md) |
| Architecture | [`canonical/ARCHITECTURE.md`](canonical/ARCHITECTURE.md) |
| Lecture seule et sécurité | [`canonical/READONLY.md`](canonical/READONLY.md) |
| Contrôle d'accès | [`canonical/ACCESS_CONTROL.md`](canonical/ACCESS_CONTROL.md) |
| Données et provenance | [`canonical/DATA_CONTRACT.md`](canonical/DATA_CONTRACT.md) |
| Graphiques | [`canonical/CHART_CONTRACT.md`](canonical/CHART_CONTRACT.md) |
| Routes | [`canonical/ROUTES.md`](canonical/ROUTES.md) |
| Design V4 | [`vertex-v4/VERTEX_V4_MASTER_SPEC.md`](vertex-v4/VERTEX_V4_MASTER_SPEC.md) |
| Décisions V4 | [`vertex-v4/DECISIONS.md`](vertex-v4/DECISIONS.md) |
| Avancement V4 | [`vertex-v4/STATUS.md`](vertex-v4/STATUS.md) |
| Migration du legacy visuel | [`vertex-v4/MIGRATION_MAP.md`](vertex-v4/MIGRATION_MAP.md) |

## Références

`reference/` contient des détails métier ou techniques valides, mais non
canoniques : calculs, options, portefeuille, opérations et inventaires UI. Ces
documents éclairent une implémentation ; ils ne remplacent jamais les contrats
ci-dessus.

## Audits

`audits/current/` contient l'audit avant consolidation et le résultat vérifié du
Lot 0. Les anciens audits ont été retirés de la branche active pour éviter que
Claude Code ne suive une recommandation dépassée.

Résultat courant :
[`CONSOLIDATION_RESULT_2026-07-22.md`](audits/current/CONSOLIDATION_RESULT_2026-07-22.md).

## Archives

Les anciens design systems et captures ne vivent plus dans l'arbre actif. Leur
point de récupération est documenté dans [`archive/README.md`](archive/README.md).

## Règle de mise à jour

Pour toute nouvelle documentation :

1. choisir `ACTIVE`, `REFERENCE`, `SUPERSEDED` ou `ARCHIVED` ;
2. indiquer le commit ou la date de dernière vérification ;
3. mettre à jour cet index si le fichier devient canonique ;
4. ne jamais créer deux documents `ACTIVE` sur le même sujet.
