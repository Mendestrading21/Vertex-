# WORK_MANIFEST — Lot 5 · Contrats instrument, source et unité

## Objectif

Porter l'enveloppe `ProvenancedValue` au contrat canonique du skill
(`connection-and-resilience-matrix.md`) : `unit`, `currency`,
`instrument_id`, `observed_at`/`received_at`, `entitlement`,
`schema_version`, `lineage`, `error` — **sans casser une seule fixture** :
tous les nouveaux champs ont un défaut, `to_dict()` reste un superset.
Garder « UNKNOWN n'est jamais zéro » par un gardien.

## Constat d'audit

L'enveloppe existe (`vertex/data_sources/models.py`) et porte déjà
value/source/mode/timestamp/age/quality/fallback/warnings + un
`AnalyticsPacket` par symbole. Manquent, contre le contrat : l'unité, la
devise, l'identité d'instrument, la séparation observation/réception,
l'entitlement, la version de schéma et le lineage.

`stamp()`/`missing()` sont les deux constructeurs ; `missing()` rend déjà
`value=None, quality=MISSING` — jamais un zéro. À garder tel quel, et à
prouver.

## Portée — et ce qui n'y est pas

- **Dans le lot** : l'enveloppe elle-même + le gardien anti-zéro + la
  migration du producteur le plus central (`cotation_unifiee`) qui posera
  `unit`/`currency`/`instrument_id`/`lineage` réels.
- **Hors lot** : la migration des autres producteurs (route par route, lots
  suivants), la quarantaine, le snapshot atomique (lot 6).

## Fichiers autorisés

`vertex/data_sources/models.py` · `vertex/data_sources/cotation_unifiee.py` ·
`tests/test_enveloppe_lot05.py` (neuf) · `docs/vertex-2-0/lot-05/**`.

## Tests

Rouge d'abord (champs absents), vert après ; compat : `to_dict()` d'une
enveloppe legacy inchangé sur ses clés historiques ; suite complète.

## Rollback

Revert — champs additifs uniquement, aucun consommateur ne les exige.
